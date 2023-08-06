from contextlib import contextmanager
import logging
import os
import re
import subprocess
import tempfile
from threading import Event, Thread
from typing import Any, Dict, Iterator, List

from openapi_client.rest import ApiException  # type: ignore
import ray

import anyscale
from anyscale.client.openapi_client.api.default_api import DefaultApi  # type: ignore
from anyscale.util import format_api_exception, get_rsync_command, send_json_request

logging.basicConfig(format=ray.ray_constants.LOGGER_FORMAT)
logger = logging.getLogger(__file__)
logging.getLogger("botocore").setLevel(logging.CRITICAL)

if anyscale.conf.AWS_PROFILE is not None:
    logger.info("Using AWS profile %s", anyscale.conf.AWS_PROFILE)
    os.environ["AWS_PROFILE"] = anyscale.conf.AWS_PROFILE

TIME_BETWEEN_HEARTBEATS = 30  # seconds


@contextmanager
def managed_autosync_session(
    session_id: str, api_client: DefaultApi = None
) -> Iterator[str]:
    # Register to the API that we enabled autosync
    with format_api_exception(ApiException):
        resp = api_client.register_autosync_session_api_v2_autosync_sessions_post(
            session_id
        )

    autosync_session_id = resp.result.id
    heartbeat_thread = AutosyncHeartbeat(autosync_session_id)
    heartbeat_thread.start()

    try:
        yield autosync_session_id
    finally:
        heartbeat_thread.finish.set()
        with format_api_exception(ApiException):
            api_client.deregister_autosync_session_api_v2_autosync_sessions_autosync_session_id_delete(
                autosync_session_id
            )
        heartbeat_thread.join()
        print("Autosync finished.")


class AutosyncHeartbeat(Thread):
    def __init__(self, autosync_session_id: str):
        super().__init__()
        self.autosync_session_id = autosync_session_id
        self.finish = Event()

    def run(self) -> None:
        while not self.finish.is_set():
            try:
                print("heartbeat sending")
                send_json_request(
                    "/api/v2/autosync_sessions/{}/heartbeat".format(
                        self.autosync_session_id
                    ),
                    {},
                    method="POST",
                )
            except Exception as e:
                print("Error sending heartbeat:", e)
            self.finish.wait(TIME_BETWEEN_HEARTBEATS)


def perform_autosync_synchronization(
    fswatch_command: List[str],
    env: Dict[str, Any],
    ssh_command: List[str],
    source: str,
    ssh_user: str,
    head_ip: str,
    target: str,
    sync_git: bool,
) -> None:
    # Check if current directory is a git repo:
    try:
        subprocess.check_call(  # noqa: B1
            ["git", "-C", ".", "rev-parse"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        is_git_repo = True
    except subprocess.CalledProcessError:
        is_git_repo = False

    # Perform synchronization whenever there is a change. We batch together
    # multiple updates and then call rsync on them.
    with subprocess.Popen(
        fswatch_command, stdout=subprocess.PIPE, env=env,
    ) as proc:  # noqa: B1
        while True:
            files = []
            while proc.stdout:
                path = proc.stdout.readline().strip().decode()
                if path == "NoOp":
                    break
                else:
                    relpath = os.path.relpath(path, source)
                    files.append(relpath)
            if files:
                if is_git_repo:
                    # Filter out gitignore files
                    try:
                        ignored_files = subprocess.check_output(  # noqa: B1
                            ["git", "check-ignore", *files]
                        )
                        files_to_ignore = ignored_files.decode().splitlines()
                        for file in files_to_ignore:
                            files.remove(file)
                    except subprocess.CalledProcessError:
                        # Failed check-ignore just means we won't ignore any files
                        # For example, if the directory is not a git repo, this call will fail.
                        pass

                with tempfile.NamedTemporaryFile(mode="w") as modified_files:
                    for f in files:
                        # Avoid rsyncing temporary files that may disappear between
                        # now and when rsync builds a file list.
                        # This matches files ending with: .swp, ~, .tmp or 4913 (neovim)
                        if re.match("(.*(.sw[a-e,g-z]|~|.tmp)$|^4913$)", f):
                            continue
                        modified_files.write(f + "\n")
                    modified_files.flush()
                    command, rsync_env = get_rsync_command(
                        ssh_command,
                        source,
                        ssh_user,
                        head_ip,
                        target,
                        sync_git,
                        modified_files=modified_files,
                    )
                    logger.info("Calling rsync due to detected file update.")
                    logger.debug("Command: {command}".format(command=command))
                    temp_sync = subprocess.run(command, env=rsync_env)  # noqa: B1
                    if temp_sync.returncode != 0:
                        logger.error(
                            f"Secondary sync failed with error code: {temp_sync.returncode}, autosync will continue running."
                        )
