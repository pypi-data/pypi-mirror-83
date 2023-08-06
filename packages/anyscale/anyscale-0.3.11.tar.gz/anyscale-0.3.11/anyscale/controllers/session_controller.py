import copy
import json
import os
import subprocess
import sys
import tempfile
from typing import Any, Dict, Optional, Tuple

import click
from openapi_client.rest import ApiException  # type: ignore
from ray.autoscaler._private.commands import rsync
from ray.autoscaler._private.constants import DOCKER_MOUNT_PREFIX
from ray.autoscaler.sdk import get_head_node_ip
import ray.scripts.scripts as autoscaler_scripts
import yaml

from anyscale import ANYSCALE_ENV
from anyscale.api import get_api_client
from anyscale.autosync_heartbeat import (
    managed_autosync_session,
    perform_autosync_synchronization,
)
from anyscale.client.openapi_client import SessionFinishUpOptions, SessionUpOptions, StopSessionOptions  # type: ignore
from anyscale.client.openapi_client.api.default_api import DefaultApi  # type: ignore
from anyscale.cloud import get_cloud_id_and_name
from anyscale.cluster_config import configure_for_session, get_cluster_config
from anyscale.project import (
    get_project_id,
    get_project_session,
    get_project_sessions,
    load_project_or_throw,
)
from anyscale.util import (
    canonicalize_remote_location,
    download_anyscale_wheel,
    format_api_exception,
    get_container_name,
    get_endpoint,
    get_project_directory_name,
    get_rsync_command,
    get_working_dir,
    install_anyscale_hooks,
    populate_session_args,
    validate_cluster_configuration,
    wait_for_session_start,
)


class SessionController:
    def __init__(self, api_client: Optional[DefaultApi] = None):
        if api_client is None:
            api_client = get_api_client()
        self.api_client = api_client

    def stop(
        self,
        session_name: Optional[str],
        terminate: bool,
        delete: bool,
        workers_only: bool,
        keep_min_workers: bool,
    ) -> None:
        project_definition = load_project_or_throw()
        project_id = get_project_id(project_definition.root)
        sessions = get_project_sessions(project_id, session_name, self.api_client)
        terminate = terminate or delete

        if not session_name and len(sessions) > 1:
            raise click.ClickException(
                "Multiple active sessions: {}\n"
                "Please specify the one you want to stop with --session-name.".format(
                    [session["name"] for session in sessions]
                )
            )

        for session in sessions:
            # Stop the session and mark it as stopped in the database.
            self.api_client.stop_session_api_v2_sessions_session_id_stop_post(
                session.id,
                StopSessionOptions(
                    terminate=terminate,
                    workers_only=workers_only,
                    keep_min_workers=keep_min_workers,
                    delete=delete,
                ),
            )

        session_names = [session.name for session in sessions]
        session_names_str = ", ".join(session_names)
        url = get_endpoint(f"/projects/{project_id}")
        print(f"Session {session_names_str} stopping. View progress at {url}")

    def up(
        self,
        session_name: Optional[str],
        config: Optional[str],
        min_workers: Optional[int],
        max_workers: Optional[int],
        no_restart: bool,
        restart_only: bool,
        disable_sync: bool,
        cloud_id: Optional[str],
        cloud_name: Optional[str],
        yes: bool,
    ) -> None:
        # TODO(ilr) Split this into ~3 functions, look at jbai's comments on #1469
        project_definition = load_project_or_throw()
        project_id = get_project_id(project_definition.root)

        if not session_name:
            session_name = str(
                self.api_client.get_project_default_session_name_api_v2_projects_project_id_default_session_name_get(
                    project_id=project_id,
                ).result.name
            )

        session_list = self.api_client.list_sessions_api_v2_sessions_get(
            project_id=project_id, active_only=False, name=session_name
        ).results

        session_exists = len(session_list) > 0

        if not session_exists:
            config_attribute_provided = True
            if not config:
                config_attribute_provided = False
                config = project_definition.cluster_yaml()

            if not os.path.exists(config):
                if config_attribute_provided:
                    raise ValueError("Config file {} not found".format(config))
                else:
                    raise ValueError(
                        "No config param provided and default config file session-default.yaml not found. Please provide a config file using the --config attribute."
                    )

        cluster_config = None

        if config:
            with open(config) as f:
                cluster_config_filled = populate_session_args(f.read(), config)
                cluster_config = yaml.safe_load(cluster_config_filled)

            validate_cluster_configuration(config, cluster_config, self.api_client)

        cloud_id, _ = get_cloud_id_and_name(self.api_client, cloud_id, cloud_name)
        assert cloud_id is not None, "Failed to get cloud."

        with format_api_exception(ApiException):
            up_response = self.api_client.session_up_api_v2_sessions_up_post(
                session_up_options=SessionUpOptions(
                    project_id=project_id,
                    name=session_name,
                    cluster_config={"config": json.dumps(cluster_config)}
                    if cluster_config
                    else None,
                    cloud_id=cloud_id,
                )
            ).result
        session_id = up_response.session_id

        # Download & write anyscale wheel!
        download_anyscale_wheel(self.api_client, session_id)

        # Get previous head IP
        with format_api_exception(ApiException):
            ip_resp = self.api_client.get_session_api_v2_sessions_session_id_get(
                session_id
            )
        prev_head_ip = ip_resp.result.head_node_ip

        cluster_config = up_response.cluster_config

        if cluster_config["provider"].get("type") != "kubernetes":
            cluster_config = configure_for_session(
                session_id,
                project_definition.root,
                api_client=self.api_client,
                disable_project_sync=disable_sync,
                _DO_NOT_USE_RAY_UP_ONLY_cluster_config=cluster_config,
            )

        install_anyscale_hooks(cluster_config)

        with tempfile.NamedTemporaryFile(mode="w") as config_file:
            renamed_config = copy.deepcopy(cluster_config)
            renamed_config["cluster_name"] = up_response.cluster_name
            json.dump(renamed_config, config_file)
            config_file.flush()
            try:
                # Use the bundled Autoscaler by directly calling the scripts file
                command = [
                    sys.executable,
                    autoscaler_scripts.__file__,
                    "up",
                    config_file.name,
                    "--no-restart" if no_restart else "",
                    "--restart-only" if restart_only else "",
                    "--yes",
                ]
                command_lst = [c for c in command if c]
                if max_workers:
                    command_lst.extend(["--max-workers", f"{max_workers}"])
                if min_workers:
                    command_lst.extend(["--min-workers", f"{min_workers}"])
                proc = subprocess.Popen(
                    command_lst,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    env=ANYSCALE_ENV,
                )
                startup_log = []
                while proc.stdout:
                    line = proc.stdout.readline().decode()
                    if not line:
                        break
                    print(line, end="")
                    startup_log.append(line)
                startup_log_str = "".join(startup_log)
                proc.communicate()

                curr_head_ip = get_head_node_ip(renamed_config)
                # Rsync file mounts and project directory after cluster started
                if not disable_sync:
                    # TODO(ilr) Look into all_nodes=False
                    rsync(
                        config_file.name,
                        source=None,
                        target=None,
                        override_cluster_name=None,
                        down=False,
                        all_nodes=True,
                    )

                if curr_head_ip != prev_head_ip:
                    print("Setting up Jupyter lab, Ray dashboard, and autosync ...")

                self.api_client.session_finish_up_api_v2_sessions_session_id_finish_up_post(
                    session_id=session_id,
                    session_finish_up_options=SessionFinishUpOptions(
                        startup_log=startup_log_str,
                        new_session=curr_head_ip != prev_head_ip,
                        head_node_ip=curr_head_ip,
                    ),
                )

                wait_for_session_start(project_id, session_name, self.api_client)
                url = get_endpoint(f"/projects/{project_id}")
                print(f"Session {session_name} started. View at {url}")
            except Exception as e:
                self.api_client.stop_session_api_v2_sessions_session_id_stop_post(
                    session_id=session_id,
                    stop_session_options=StopSessionOptions(
                        terminate=True, workers_only=False, keep_min_workers=False,
                    ),
                )
                raise click.ClickException("{}\nSession startup failed.".format(e))

    def ssh(self, session_name: str, ssh_option: Tuple[str]) -> None:
        project_definition = load_project_or_throw()
        project_id = get_project_id(project_definition.root)
        session = get_project_session(project_id, session_name, self.api_client)

        cluster_config = get_cluster_config(session_name, self.api_client)

        with format_api_exception(ApiException):
            head_ip = self.api_client.get_session_head_ip_api_v2_sessions_session_id_head_ip_get(
                session.id
            ).result.head_ip

        ssh_user = cluster_config["auth"]["ssh_user"]
        key_path = cluster_config["auth"]["ssh_private_key"]
        container_name = get_container_name(cluster_config)

        command = (
            ["ssh"]
            + list(ssh_option)
            + ["-tt", "-i", key_path]
            + ["{}@{}".format(ssh_user, head_ip)]
            + (
                [f"docker exec -it {container_name} sh -c 'which bash && bash || sh'"]
                if container_name
                else []
            )
        )

        subprocess.run(command)  # noqa: B1

    def autosync(
        self,
        session_name: Optional[str] = None,
        verbose: bool = False,
        sync_git: bool = False,
    ) -> None:
        project_definition = load_project_or_throw()
        project_id = get_project_id(project_definition.root)
        print(f"Active project: {project_definition.root}\n")

        session = get_project_session(project_id, session_name, self.api_client)

        wait_for_session_start(project_id, session.name, self.api_client)

        # Get project directory name:
        directory_name = get_project_directory_name(project_id, self.api_client)

        cluster_config = get_cluster_config(session_name, self.api_client)

        with format_api_exception(ApiException):
            head_ip = self.api_client.get_session_head_ip_api_v2_sessions_session_id_head_ip_get(
                session.id
            ).result.head_ip
        ssh_user = cluster_config["auth"]["ssh_user"]
        ssh_private_key_path = cluster_config["auth"]["ssh_private_key"]

        source = project_definition.root
        target = get_working_dir(cluster_config, project_id, self.api_client)
        if bool(get_container_name(cluster_config)):
            target = f"{DOCKER_MOUNT_PREFIX}/{target}"
            # Legacy mount check
            old_mounts = [
                x
                for x in cluster_config["docker"].get("run_options", [])
                if f"$HOME/{directory_name}" in x
            ]
            if len(old_mounts) == 1:
                target = f"~/{directory_name}"

        print("Autosync with session {} is starting up...".format(session.name))
        with managed_autosync_session(session.id, self.api_client):
            ssh_command = [
                "ssh",
                "-o",
                "StrictHostKeyChecking=no",
                "-o",
                "UserKnownHostsFile={}".format(os.devnull),
                "-o",
                "LogLevel=ERROR",
                "-i",
                ssh_private_key_path,
            ]
            # Performing initial full synchronization with rsync.
            command, rsync_env = get_rsync_command(
                ssh_command, source, ssh_user, head_ip, target, sync_git,
            )
            first_sync = subprocess.run(command, env=rsync_env)  # noqa: B1

            if first_sync.returncode != 0:
                raise click.ClickException(
                    f"First sync failed with error code: {first_sync.returncode}"
                )

            anyscale_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
            if sys.platform.startswith("linux"):
                env: Dict[str, str] = {}
                fswatch_executable = os.path.join(anyscale_dir, "fswatch-linux")
                fswatch_command = [
                    fswatch_executable,
                    source,
                    "--batch-marker",
                    "--monitor=poll_monitor",
                    "-r",
                ]
                if not sync_git:
                    fswatch_command += ["-e", ".*/\.git"]  # noqa: W605
            elif sys.platform.startswith("darwin"):
                env = {"DYLD_LIBRARY_PATH": anyscale_dir}
                fswatch_executable = os.path.join(anyscale_dir, "fswatch-darwin")
                fswatch_command = [
                    fswatch_executable,
                    source,
                    "--batch-marker",
                ]
                if not sync_git:
                    fswatch_command += ["-e", ".*/\.git"]  # noqa: W605
            else:
                raise NotImplementedError(
                    "Autosync not supported on platform {}".format(sys.platform)
                )

            perform_autosync_synchronization(
                fswatch_command,
                env,
                ssh_command,
                source,
                ssh_user,
                head_ip,
                target,
                sync_git,
            )

    def pull(
        self,
        session_name: Optional[str] = None,
        source: Optional[str] = None,
        target: Optional[str] = None,
        config: Optional[str] = None,
    ) -> None:
        project_definition = load_project_or_throw()

        try:
            print("Collecting files from remote.")
            project_id = get_project_id(project_definition.root)
            cluster_config = get_cluster_config(session_name, self.api_client)
            directory_name = get_working_dir(
                cluster_config, project_id, self.api_client
            )
            source_directory = f"{directory_name}/"

            source = canonicalize_remote_location(cluster_config, source, project_id)
            with tempfile.NamedTemporaryFile(mode="w") as config_file:
                json.dump(cluster_config, config_file)
                config_file.flush()

                if source and target:
                    rsync(
                        config_file.name,
                        source=source,
                        target=target,
                        override_cluster_name=None,
                        down=True,
                    )
                elif source or target:
                    raise click.ClickException(
                        "Source and target are not both specified. Please either specify both or neither."
                    )
                else:
                    rsync(
                        config_file.name,
                        source=source_directory,
                        target=project_definition.root,
                        override_cluster_name=None,
                        down=True,
                    )

            if config:
                session = get_project_session(project_id, session_name, self.api_client)
                with format_api_exception(ApiException):
                    resp = self.api_client.get_session_cluster_config_api_v2_sessions_session_id_cluster_config_get(
                        session.id
                    )
                cluster_config = yaml.safe_load(resp.result.config_with_defaults)
                with open(config, "w") as f:
                    yaml.dump(cluster_config, f, default_flow_style=False)

            print("Pull completed.")

        except Exception as e:
            print(e)
            raise click.ClickException(e)  # type: ignore

    def anyscale_push_session(
        self,
        ctx: Any,
        session_name: str,
        source: Optional[str],
        target: Optional[str],
        config: Optional[str],
        all_nodes: bool,
    ) -> None:
        project_definition = load_project_or_throw()
        project_id = get_project_id(project_definition.root)
        session = get_project_session(project_id, session_name, self.api_client)
        session_name = session.name

        cluster_config = get_cluster_config(session_name, self.api_client)
        target = canonicalize_remote_location(cluster_config, target, project_id)
        with tempfile.NamedTemporaryFile(mode="w") as config_file:
            json.dump(cluster_config, config_file)
            config_file.flush()

            if source and target:
                rsync(
                    config_file.name,
                    source=source,
                    target=target,
                    override_cluster_name=None,
                    down=False,
                    all_nodes=all_nodes,
                )
            elif source or target:
                raise click.ClickException(
                    "Source and target are not both specified. Please either specify both or neither."
                )
            else:
                rsync(
                    config_file.name,
                    source=None,
                    target=None,
                    override_cluster_name=None,
                    down=False,
                    all_nodes=True,
                )

        if config:
            validate_cluster_configuration(config, self.api_client)
            print("Updating session with {}".format(config))
            self.up(
                session_name=session_name,
                config=None,
                min_workers=None,
                max_workers=None,
                no_restart=False,
                restart_only=False,
                disable_sync=True,
                cloud_id=session.cloud_id,
                cloud_name=None,
                yes=True,
            )
        url = get_endpoint(f"/projects/{project_id}")
        print(f"Pushed to session {session_name}. View at {url}")
