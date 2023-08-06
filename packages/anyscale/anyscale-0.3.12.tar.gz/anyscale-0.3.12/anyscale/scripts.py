import datetime
import json
import logging
import os
import sys
import tempfile
from typing import Any, Dict, List, Optional

import click
from packaging import version
from ray.autoscaler._private.commands import rsync
import ray.ray_constants

from anyscale.api import instantiate_api_client
from anyscale.auth_proxy import app as auth_proxy_app
from anyscale.client.openapi_client.rest import ApiException  # type: ignore
from anyscale.cloudgateway import CloudGatewayRunner
from anyscale.cluster_config import get_cluster_config
from anyscale.commands.cloud_commands import cloud_cli
from anyscale.commands.exec_commands import anyscale_exec
from anyscale.commands.list_commands import list_cli
from anyscale.commands.project_commands import anyscale_clone, anyscale_init
from anyscale.commands.session_commands import (
    anyscale_autosync,
    anyscale_pull,
    anyscale_push,
    anyscale_ssh,
    anyscale_stop,
    anyscale_up,
)
import anyscale.conf
import anyscale.legacy_projects as ray_scripts
from anyscale.project import (
    get_project_id,
    get_project_session,
    load_project_or_throw,
    ProjectDefinition,
)
from anyscale.snapshot import (
    copy_file,
    describe_snapshot,
    get_snapshot_id,
)
from anyscale.util import (
    deserialize_datetime,
    execution_log_name,
    get_endpoint,
    send_json_request,
)


logging.basicConfig(format=ray.ray_constants.LOGGER_FORMAT)
logger = logging.getLogger(__file__)
logging.getLogger("botocore").setLevel(logging.CRITICAL)

if anyscale.conf.AWS_PROFILE is not None:
    logger.info("Using AWS profile %s", anyscale.conf.AWS_PROFILE)
    os.environ["AWS_PROFILE"] = anyscale.conf.AWS_PROFILE


class AliasedGroup(click.Group):
    # This is from https://stackoverflow.com/questions/46641928/python-click-multiple-command-names
    def get_command(self, ctx: Any, cmd_name: str) -> Any:
        try:
            cmd_name = ALIASES[cmd_name].name
        except KeyError:
            pass
        return super().get_command(ctx, cmd_name)


@click.group(
    invoke_without_command=True,
    no_args_is_help=True,
    cls=AliasedGroup,
    context_settings=dict(help_option_names=["-h", "--help"]),
)
@click.option(
    "--version",
    "-v",
    "version_flag",
    is_flag=True,
    default=False,
    help="Current anyscale version.",
)
@click.option(
    "--json",
    "show_json",
    is_flag=True,
    default=False,
    help="Return output as json, for use with --version.",
)
@click.pass_context
def cli(ctx: Any, version_flag: bool, show_json: bool) -> None:
    try:
        api_instance = instantiate_api_client(no_cli_token=True)
        resp = api_instance.get_anyscale_version_api_v2_userinfo_anyscale_version_get()
        curr_version = anyscale.__version__
        latest_version = resp.result.version
        if version.parse(curr_version) < version.parse(latest_version):
            message = "Warning: Using version {0} of anyscale. Please update the package using pip install anyscale -U to get the latest version {1}".format(
                curr_version, latest_version
            )
            print("\033[91m{}\033[00m".format(message), file=sys.stderr)
    except Exception as e:
        if type(e) == ApiException:
            logger.warning(
                "Error {} while trying to get latest anyscale version number: {}".format(
                    e.status, e.reason  # type: ignore
                )
            )
        else:
            logger.warning(e)

    if version_flag:
        ctx.invoke(version_cli, show_json=show_json)


@click.group("project", help="Commands for working with projects.", hidden=True)
def project_cli() -> None:
    pass


@click.group("session", help="Commands for working with sessions.", hidden=True)
def session_cli() -> None:
    pass


@click.group("snapshot", help="Commands for working with snapshot.", hidden=True)
def snapshot_cli() -> None:
    pass


@click.command(name="version", help="Display version of the anyscale CLI.")
@click.option(
    "--json", "show_json", is_flag=True, default=False, help="Return output as json."
)
def version_cli(show_json: bool) -> None:
    if show_json:
        print(json.dumps({"version": anyscale.__version__}))
    else:
        print(anyscale.__version__)


@cli.command(
    name="help", help="Display help documentation for anyscale CLI.", hidden=True
)
@click.pass_context
def anyscale_help(ctx: Any) -> None:
    print(ctx.parent.get_help())


def remote_snapshot(
    project_id: str,
    session_name: str,
    tags: List[str],
    project_definition: ProjectDefinition,
    description: Optional[str] = None,
) -> str:
    session = get_project_session(project_id, session_name)

    resp = send_json_request(
        "/api/v2/sessions/{session_id}/take_snapshot".format(session_id=session["id"]),
        {
            "tags": tags,
            "description": description if description else "",
        },  # noqa: E231
        method="POST",
    )
    if "id" not in resp["result"]:
        raise click.ClickException(
            "Snapshot creation of session {} failed!".format(session["name"])
        )
    snapshot_id: str = resp["result"]["id"]
    return snapshot_id


@snapshot_cli.command(name="create", help="Create a snapshot of the current project.")
@click.option("--description", help="A description of the snapshot", default=None)
@click.option(
    "--session-name",
    help="If specified, a snapshot of the remote session"
    "with that name will be taken.",
    default=None,
)
@click.option(
    "--yes", "-y", is_flag=True, default=False, help="Don't ask for confirmation."
)
@click.option(
    "--tag",
    type=str,
    help="Tag for this snapshot. Multiple tags can be specified by repeating this option.",
    multiple=True,
)
def snapshot_create(
    description: Optional[str], session_name: Optional[str], yes: bool, tag: List[str],
) -> None:
    project_definition = load_project_or_throw()
    project_id = get_project_id(project_definition.root)

    if session_name:
        # Create a remote snapshot.
        try:
            snapshot_id = remote_snapshot(
                project_id, session_name, tag, project_definition, description
            )
            print(
                "Snapshot {snapshot_id} of session {session_name} created!".format(
                    snapshot_id=snapshot_id, session_name=session_name
                )
            )
        except click.ClickException as e:
            raise e

    else:
        # Create a local snapshot.
        raise NotImplementedError("Local snapshotting is not supported anymore.")

    url = get_endpoint(f"/projects/{project_id}")
    print(f"Snapshot {snapshot_id} created. View at {url}")


@snapshot_cli.command(
    name="describe", help="Describe metadata and files of a snapshot."
)
@click.argument("name")
def snapshot_describe(name: str) -> None:
    try:
        description = describe_snapshot(name)
    except Exception as e:
        # Describing a snapshot can fail if the snapshot does not exist.
        raise click.ClickException(e)  # type: ignore

    print(description)


@session_cli.command(name="attach", help="Open a console for the given session.")
@click.option("--name", help="Name of the session to open a console for.", default=None)
@click.option("--tmux", help="Attach console to tmux.", is_flag=True)
@click.option("--screen", help="Attach console to screen.", is_flag=True)
def session_attach(name: Optional[str], tmux: bool, screen: bool) -> None:
    project_definition = load_project_or_throw()
    project_id = get_project_id(project_definition.root)

    session = get_project_session(project_id, name)
    ray.autoscaler._private.commands.attach_cluster(
        project_definition.cluster_yaml(),
        start=False,
        use_tmux=tmux,
        use_screen=screen,
        override_cluster_name=session["name"],
        new=False,
    )


@click.command(
    name="start",
    context_settings=dict(ignore_unknown_options=True,),
    help="Start a session based on the current project configuration.",
    hidden=True,
)
@click.option("--session-name", help="The name of the created session.", default=None)
# TODO(pcm): Change this to be
# anyscale session start --arg1=1 --arg2=2 command args
# instead of
# anyscale session start --session-args=--arg1=1,--arg2=2 command args
@click.option(
    "--session-args",
    help="Arguments that get substituted into the cluster config "
    "in the format --arg1=1,--arg2=2",
    default="",
)
@click.option(
    "--snapshot",
    help="If set, start the session from the given snapshot.",
    default=None,
)
@click.option(
    "--config",
    help="If set, use this cluster file rather than the default"
    " listed in project.yaml.",
    default=None,
)
@click.option(
    "--min-workers",
    help="Overwrite the minimum number of workers in the cluster config.",
    default=None,
)
@click.option(
    "--max-workers",
    help="Overwrite the maximum number of workers in the cluster config.",
    default=None,
)
@click.option(
    "--run", help="Command to run.", default=None,
)
@click.argument("args", nargs=-1, type=click.UNPROCESSED)
@click.option("--cloud-id", help="Id of the cloud to use", default=None)
@click.option("--cloud-name", help="Name of the cloud to use", default=None)
def anyscale_start(
    session_args: str,
    snapshot: Optional[str],
    session_name: Optional[str],
    config: Optional[str],
    min_workers: Optional[int],
    max_workers: Optional[int],
    run: Optional[str],
    args: List[str],
    cloud_id: Optional[str],
    cloud_name: Optional[str],
) -> None:
    command_name = run

    project_definition = load_project_or_throw()
    project_id = get_project_id(project_definition.root)

    if cloud_id and cloud_name:
        raise click.ClickException("Please provide either cloud id or cloud name.")
    elif cloud_name:
        resp_get_cloud = send_json_request(
            "/api/v2/clouds/find_by_name", {"name": cloud_name}, method="POST"
        )
        cloud = resp_get_cloud["result"]
        cloud_id = cloud["id"]

    if not session_name:
        session_list = send_json_request(
            "/api/v2/sessions/", {"project_id": project_id, "active_only": False}
        )["results"]
        session_name = "session-{0}".format(len(session_list) + 1)

    # Parse the session arguments.
    if config:
        project_definition.config["cluster"]["config"] = config

    session_params: Dict[str, str] = {}

    if command_name:
        command_name = " ".join([command_name] + list(args))
    session_runs = ray_scripts.get_session_runs(session_name, command_name, {})

    assert len(session_runs) == 1, "Running sessions with a wildcard is deprecated"
    session_run = session_runs[0]

    # TODO(ilr) Make snapshot_id optional, and have this only check if a snapshot is available
    snapshot_id = None
    if snapshot is not None:
        snapshot_id = get_snapshot_id(project_definition.root, snapshot)

    session_name = session_run["name"]
    resp = send_json_request(
        "/api/v2/sessions/",
        {"project_id": project_id, "name": session_name, "active_only": False},
    )
    if len(resp["results"]) == 0:
        resp = send_json_request(
            "/api/v2/sessions/create_new_session",
            {
                "project_id": project_id,
                "name": session_name,
                "snapshot_id": snapshot_id,
                "session_params": session_params,
                "command_name": command_name,
                "command_params": session_run["params"],
                "shell": True,
                "min_workers": min_workers,
                "max_workers": max_workers,
                "cloud_id": cloud_id,
            },
            method="POST",
        )
    elif len(resp["results"]) == 1:
        if session_params != {}:
            raise click.ClickException(
                "Session parameters are not supported when restarting a session"
            )
        send_json_request(
            "/api/v2/sessions/{session_id}/start".format(
                session_id=resp["results"][0]["id"]
            ),
            {"min_workers": min_workers, "max_workers": max_workers},
            method="POST",
        )
    else:
        raise click.ClickException(
            "Multiple sessions with name {} exist".format(session_name)
        )
    # Print success message
    url = get_endpoint(f"/projects/{project_id}")
    print(f"Session {session_name} starting. View progress at {url}")


@click.command(
    name="run",
    context_settings=dict(ignore_unknown_options=True,),
    help="Execute a command in a session.",
    hidden=True,
)
@click.argument("command_name", required=False)
@click.argument("args", nargs=-1, type=click.UNPROCESSED)
@click.option(
    "--session-name", help="Name of the session to run this command on", default=None
)
@click.option(
    "--stop", help="If set, stop session after command finishes running.", is_flag=True,
)
def anyscale_run(
    command_name: Optional[str],
    args: List[str],
    session_name: Optional[str],
    stop: bool,
) -> None:

    if not command_name:
        raise click.ClickException(
            "No shell command or registered command name was specified."
        )
    project_definition = load_project_or_throw()
    project_id = get_project_id(project_definition.root)
    session = get_project_session(project_id, session_name)

    command_name = " ".join([command_name] + list(args))

    send_json_request(
        "/api/v2/sessions/{session_id}/execute_shell_command".format(
            session_id=session["id"]
        ),
        {"shell_command": command_name, "stop": stop},
        method="POST",
    )


@session_cli.command(name="logs", help="Show logs for the current session.")
@click.option("--name", help="Name of the session to run this command on", default=None)
@click.option("--command-id", help="ID of the command to get logs for", default=None)
def session_logs(name: Optional[str], command_id: Optional[int]) -> None:
    project_definition = load_project_or_throw()
    project_id = get_project_id(project_definition.root)
    # If the command_id is not specified, determine it by getting the
    # last run command from the active session.
    if not command_id:
        session = get_project_session(project_id, name)
        resp = send_json_request(
            "/api/v2/session_commands/?session_id={}".format(session["id"]), {}
        )
        # Search for latest run command
        last_created_at = datetime.datetime.min
        last_created_at = last_created_at.replace(tzinfo=datetime.timezone.utc)
        for command in resp["results"]:
            created_at = deserialize_datetime(command["created_at"])
            if created_at > last_created_at:
                last_created_at = created_at
                command_id = command["id"]
        if not command_id:
            raise click.ClickException(
                "No comand was run yet on the latest active session {}".format(
                    session["name"]
                )
            )
    resp_out = send_json_request(
        "/api/v2/session_commands/{session_command_id}/execution_logs".format(
            session_command_id=command_id
        ),
        {"log_type": "out", "start_line": 0, "end_line": 1000000000},
    )
    resp_err = send_json_request(
        "/api/v2/session_commands/{session_command_id}/execution_logs".format(
            session_command_id=command_id
        ),
        {"log_type": "err", "start_line": 0, "end_line": 1000000000},
    )
    # TODO(pcm): We should have more options here in the future
    # (e.g. show only stdout or stderr, show only the tail, etc).
    print("stdout:")
    print(resp_out["result"]["lines"])
    print("stderr:")
    print(resp_err["result"]["lines"])


@session_cli.command(
    name="upload_command_logs", help="Upload logs for a command.", hidden=True
)
@click.option(
    "--command-id", help="ID of the command to upload logs for", type=str, default=None
)
def session_upload_command_logs(command_id: Optional[str]) -> None:
    resp = send_json_request(
        "/api/v2/session_commands/{session_command_id}/upload_logs".format(
            session_command_id=command_id
        ),
        {},
        method="POST",
    )
    assert resp["result"]["session_command_id"] == command_id

    allowed_sources = [
        execution_log_name(command_id) + ".out",
        execution_log_name(command_id) + ".err",
    ]

    for source, target in resp["result"]["locations"].items():
        if source in allowed_sources:
            copy_file(True, source, target, download=False)


@session_cli.command(
    name="finish_command", help="Finish executing a command.", hidden=True
)
@click.option(
    "--command-id", help="ID of the command to finish", type=str, required=True
)
@click.option(
    "--stop", help="Stop session after command finishes executing.", is_flag=True
)
def session_finish_command(command_id: str, stop: bool) -> None:
    with open(execution_log_name(command_id) + ".status") as f:
        status_code = int(f.read().strip())
    send_json_request(
        f"/api/v2/session_commands/{command_id}/finish",
        {"status_code": status_code, "stop": stop},
        method="POST",
    )


@click.command(
    name="cloudgateway",
    help="Run private clusters via anyscale cloud gateway.",
    hidden=True,
)
@click.option("--gateway-id", type=str, required=True)
def anyscale_cloudgateway(gateway_id: str) -> None:
    # Make sure only registered users can start the gateway.
    logger.info("Verifying user ...")
    try:
        send_json_request("/api/v2/userinfo/", {})
    except Exception:
        raise click.ClickException(
            "Invalid user. Did you set up the cli_token credentials?"
            + ' To setup your credentials, follow the instructions in the "credentials" tab'
            + " after logging in to your anyscale account."
        )
    anyscale_address = f"/api/v2/cloudgateway/{gateway_id}"
    cloudgateway_runner = CloudGatewayRunner(anyscale_address)
    logger.info(
        "Your gateway-id is: {}. Store it in the provider section in the".format(
            gateway_id
        )
        + " cluster yaml file of the remote cluster that interacts with this gateway."
        + ' E.g., config["provider"]["gateway_id"]={gateway_id}.'.format(
            gateway_id=gateway_id
        )
    )
    cloudgateway_runner.gateway_run_forever()


@session_cli.command(name="auth_start", help="Start the auth proxy", hidden=True)
def auth_start() -> None:
    from aiohttp import web

    web.run_app(auth_proxy_app)


@cli.command(
    name="rsync-down", help="Download specific files from cluster.", hidden=True
)
@click.argument("session-name", required=False, type=str)
@click.argument("source", required=False, type=str)
@click.argument("target", required=False, type=str)
@click.option(
    "--cluster-name",
    "-n",
    required=False,
    type=str,
    help="Override the configured cluster name.",
)
def anyscale_rsync_down(
    session_name: Optional[str],
    source: Optional[str],
    target: Optional[str],
    cluster_name: Optional[str],
) -> None:
    project_definition = load_project_or_throw()
    project_id = get_project_id(project_definition.root)

    session = get_project_session(project_id, session_name)

    cluster_config = get_cluster_config(session["name"])
    with tempfile.NamedTemporaryFile(mode="w") as config_file:
        cluster_config["cluster_name"] = cluster_name
        json.dump(cluster_config, config_file)
        config_file.flush()
        rsync(
            config_file.name,
            source=source,
            target=target,
            override_cluster_name=None,
            down=True,
        )


@cli.command(name="rsync-up", help="Upload specific files to cluster.", hidden=True)
@click.argument("session-name", required=False, type=str)
@click.argument("source", required=False, type=str)
@click.argument("target", required=False, type=str)
@click.option(
    "--cluster-name",
    "-n",
    required=False,
    type=str,
    help="Override the configured cluster name.",
)
@click.option(
    "--all-nodes",
    "-A",
    is_flag=True,
    required=False,
    help="Upload to all nodes (workers and head).",
)
def anyscale_rsync_up(
    session_name: Optional[str],
    source: Optional[str],
    target: Optional[str],
    cluster_name: Optional[str],
    all_nodes: bool,
) -> None:
    project_definition = load_project_or_throw()
    project_id = get_project_id(project_definition.root)

    session = get_project_session(project_id, session_name)

    cluster_config = get_cluster_config(session["name"])
    with tempfile.NamedTemporaryFile(mode="w") as config_file:
        json.dump(cluster_config, config_file)
        config_file.flush()
        rsync(
            config_file.name,
            source,
            target,
            cluster_name,
            down=False,
            all_nodes=all_nodes,
        )


cli.add_command(project_cli)
cli.add_command(session_cli)
cli.add_command(snapshot_cli)
cli.add_command(cloud_cli)
cli.add_command(version_cli)
cli.add_command(list_cli)

cli.add_command(anyscale_init)
cli.add_command(anyscale_run)
cli.add_command(anyscale_start)
cli.add_command(anyscale_up)
cli.add_command(anyscale_stop)
cli.add_command(anyscale_cloudgateway)
cli.add_command(anyscale_autosync)
cli.add_command(anyscale_clone)
cli.add_command(anyscale_ssh)
cli.add_command(anyscale_rsync_down)
cli.add_command(anyscale_rsync_up)
cli.add_command(anyscale_exec)
cli.add_command(anyscale_pull)
cli.add_command(anyscale_push)
cli.add_command(anyscale_help)

ALIASES = {"h": anyscale_help}


def main() -> Any:
    return cli()


if __name__ == "__main__":
    main()
