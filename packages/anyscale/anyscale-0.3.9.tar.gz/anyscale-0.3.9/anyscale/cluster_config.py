from copy import deepcopy
from functools import partial
import json
import os
from typing import Any, Callable, Dict, MutableMapping, Optional

import click
import wrapt

from anyscale.client.openapi_client.api.default_api import DefaultApi  # type: ignore
from anyscale.project import get_project_id, get_project_session, load_project_or_throw
from anyscale.util import get_working_dir, send_json_request


@wrapt.decorator  # type: ignore
def _with_safe_cluster_config(
    wrapped: Callable[..., MutableMapping[str, Any]],
    instance: Optional[Any],
    args: Any,
    kwargs: Any,
) -> Any:
    # for all our _configure_* functions, the first argument should be the cluster config
    def _configure(
        cluster_config: MutableMapping[str, Any], *args: Any, **kwargs: Any
    ) -> MutableMapping[str, Any]:
        cluster_config = deepcopy(cluster_config)

        return wrapped(cluster_config, *args, **kwargs)

    return _configure(*args, **kwargs)


@_with_safe_cluster_config  # type: ignore
def _configure_cluster_name(
    cluster_config: MutableMapping[str, Any], session_id: str, api_client: DefaultApi
) -> MutableMapping[str, Any]:
    if api_client:
        name = api_client.get_session_details_api_v2_sessions_session_id_details_get(
            session_id
        ).result.cluster_name
    else:
        name = send_json_request("/api/v2/sessions/{}/details".format(session_id), {})[
            "result"
        ]["cluster_name"]

    cluster_config["cluster_name"] = name

    return cluster_config


@_with_safe_cluster_config  # type: ignore
def _configure_ssh_key(
    cluster_config: MutableMapping[str, Any],
    session_id: str,
    api_client: DefaultApi,
    ssh_dir: str = "~/.ssh",
) -> MutableMapping[str, Any]:
    # TODO (yiran): cleanup SSH keys if session no longer exists.
    def _write_ssh_key(name: str, ssh_key: str) -> str:
        key_path = os.path.join(os.path.expanduser(ssh_dir), "{}.pem".format(name))
        os.makedirs(os.path.dirname(key_path), exist_ok=True)

        with open(key_path, "w", opener=partial(os.open, mode=0o600)) as f:
            f.write(ssh_key)

        return key_path

    if api_client:
        ssh_key = api_client.get_session_ssh_key_api_v2_sessions_session_id_ssh_key_get(
            session_id
        ).result
        key_path = _write_ssh_key(ssh_key.key_name, ssh_key.private_key)
    else:
        ssh_key = send_json_request(
            "/api/v2/sessions/{}/ssh_key".format(session_id), {}
        )["result"]
        key_path = _write_ssh_key(ssh_key["key_name"], ssh_key["private_key"])

    cluster_config.setdefault("auth", {})["ssh_private_key"] = key_path

    # Bypass Ray's check for cloudinit key
    cluster_config["head_node"].setdefault(("UserData"), "")
    cluster_config["worker_nodes"].setdefault(("UserData"), "")
    return cluster_config


@_with_safe_cluster_config  # type: ignore
def _configure_autoscaler_credentials(
    cluster_config: MutableMapping[str, Any], session_id: str, api_client: DefaultApi
) -> MutableMapping[str, Any]:
    if api_client:
        credentials = api_client.get_session_autoscaler_credentials_api_v2_sessions_session_id_autoscaler_credentials_get(
            session_id
        ).result.credentials
    else:
        credentials = send_json_request(
            "/api/v2/sessions/{}/autoscaler_credentials".format(session_id), {},
        )["result"]["credentials"]

    cloud_provider = cluster_config["provider"]["type"]
    cluster_config["provider"]["{}_credentials".format(cloud_provider)] = credentials

    return cluster_config


@_with_safe_cluster_config  # type: ignore
def _update_file_mounts(
    cluster_config: Dict[str, Any], project_root_dir: str
) -> Dict[str, Any]:
    project_id = get_project_id(project_root_dir)
    working_dir = get_working_dir(cluster_config, project_id)
    for remote_path, local_path in cluster_config.get("file_mounts", {}).items():
        if remote_path == working_dir and not os.path.samefile(
            local_path, project_root_dir
        ):
            click.confirm(
                '"{remote}: {local}" has been detected in the file mounts.\n'
                'Anyscale needs to sync the local project directory "{proj}" '
                'with "{remote}" in the cluster.\nCan this file mount be replaced for '
                "this command?\nThis action will not change your session "
                "configuration file.".format(
                    remote=remote_path, local=local_path, proj=project_root_dir,
                ),
                abort=True,
            )
    cluster_config.setdefault("file_mounts", {}).update({working_dir: project_root_dir})
    return cluster_config


def configure_for_session(
    session_id: str,
    project_root_dir: str,
    api_client: DefaultApi = None,
    _DO_NOT_USE_RAY_UP_ONLY_cluster_config: Optional[  # noqa: N803
        Dict[str, Any]
    ] = None,
) -> Dict[str, Any]:
    cluster_config: Dict[str, Any] = {}
    if _DO_NOT_USE_RAY_UP_ONLY_cluster_config is not None:
        cluster_config = _DO_NOT_USE_RAY_UP_ONLY_cluster_config
    else:
        if api_client:
            cluster_config = json.loads(
                api_client.get_session_cluster_config_api_v2_sessions_session_id_cluster_config_get(
                    session_id
                ).result.config_with_defaults
            )

        else:
            _resp: Dict[str, Any] = send_json_request(
                "/api/v2/sessions/{}/cluster_config".format(session_id), {}
            )["result"]
            cluster_config = json.loads(_resp["config_with_defaults"])

        cluster_config = _configure_cluster_name(cluster_config, session_id, api_client)

    cluster_config = _configure_ssh_key(cluster_config, session_id, api_client)
    cluster_config = _configure_autoscaler_credentials(
        cluster_config, session_id, api_client
    )
    cluster_config = _update_file_mounts(cluster_config, project_root_dir)

    return cluster_config


def get_cluster_config(
    session_name: Optional[str], api_client: DefaultApi = None
) -> Dict[str, Any]:
    if api_client is None:
        return _get_cluster_config(session_name)

    project_definition = load_project_or_throw()
    project_id = get_project_id(project_definition.root)

    session = get_project_session(project_id, session_name, api_client)

    return configure_for_session(
        session.id, project_definition.root, api_client=api_client
    )


# TODO (jbai): DEPRECATED - will be removed when OpenApi migration is completed
def _get_cluster_config(session_name: Optional[str]) -> Dict[str, Any]:
    project_definition = load_project_or_throw()
    project_id = get_project_id(project_definition.root)

    session = get_project_session(project_id, session_name)

    return configure_for_session(session["id"], project_definition.root)


@_with_safe_cluster_config  # type: ignore
def add_anyscale_node_provider(
    cluster_config: Dict[str, Any], session_id: str
) -> Dict[str, Any]:
    cluster_config["provider"]["anyscale_session_id"] = session_id
    cluster_config["provider"]["type"] = "external"
    cluster_config["provider"]["module"] = (
        # black formats this badly
        "anyscale.autoscaler.aws.node_provider.AnyscaleNodeProvider"
    )
    return cluster_config
