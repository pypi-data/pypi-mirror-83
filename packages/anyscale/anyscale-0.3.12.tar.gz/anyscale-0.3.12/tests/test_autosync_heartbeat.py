import subprocess
from subprocess import CalledProcessError
from typing import Any, Dict, List
from unittest.mock import Mock, patch

import pytest

from anyscale.autosync_heartbeat import (
    managed_autosync_session,
    perform_autosync_synchronization,
)


def test_managed_autosync_session() -> None:
    mock_api_client = Mock()
    mock_api_client.register_autosync_session_api_v2_autosync_sessions_post.return_value.result.id = (
        1
    )
    mock_api_client.deregister_autosync_session_api_v2_autosync_sessions_autosync_session_id_delete.return_value = (
        None
    )

    with managed_autosync_session("id", mock_api_client):
        pass

    mock_api_client.register_autosync_session_api_v2_autosync_sessions_post.assert_called_once_with(
        "id"
    )
    mock_api_client.deregister_autosync_session_api_v2_autosync_sessions_autosync_session_id_delete.assert_called_once_with(
        1
    )


# Tests perform_autosync_synchronization for a git repository with nothing ignored
def test_perform_autosync_synchronization() -> None:
    mock_proc = Mock()
    mock_proc.stdout = Mock()

    calls = 0

    def readline(*args: List[Any], **kwargs: Dict[str, Any]) -> bytes:
        nonlocal calls
        if calls == 0:
            calls += 1
            return b"test-file.py"
        else:
            return b"NoOp"

    mock_proc.stdout.readline.side_effect = readline

    with patch(
        "anyscale.autosync_heartbeat.subprocess.check_call"
    ) as mock_check_call, patch(
        "anyscale.autosync_heartbeat.subprocess.Popen"
    ) as mock_popen, patch(
        "anyscale.autosync_heartbeat.subprocess.check_output"
    ) as mock_check_output, patch(
        "anyscale.autosync_heartbeat.subprocess.run"
    ) as mock_run, patch(
        "anyscale.autosync_heartbeat.get_rsync_command"
    ) as mock_get_rsync_command, patch(
        "anyscale.autosync_heartbeat.tempfile.NamedTemporaryFile"
    ) as mock_temp_file:
        mock_check_call.return_value = None
        mock_popen.return_value.__enter__.return_value = mock_proc
        # Git check-ignore returns nothing to ignore
        mock_check_output.return_value = b""
        # Raise exception to exit out of infinite loop
        mock_run.side_effect = Exception()
        mock_get_rsync_command.return_value = (["rsync", "test"], {"test-env": "test"})
        mock_file = Mock()
        mock_temp_file.return_value.__enter__.return_value = mock_file
        mock_file.write.return_value = None

        with pytest.raises(Exception):
            perform_autosync_synchronization(
                ["fswatch"],
                {},
                ["ssh"],
                "project_folder",
                "test-user",
                "1.1.1.1",
                "target_folder",
                False,
            )

        mock_check_call.assert_called_once_with(
            ["git", "-C", ".", "rev-parse"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

        mock_popen.assert_called_once_with(["fswatch"], stdout=subprocess.PIPE, env={})

        mock_check_output.assert_called_once_with(
            ["git", "check-ignore", "../test-file.py"]
        )

        mock_file.write.assert_called_once_with("../test-file.py\n")

        mock_get_rsync_command.assert_called_once_with(
            ["ssh"],
            "project_folder",
            "test-user",
            "1.1.1.1",
            "target_folder",
            False,
            modified_files=mock_file,
        )

        mock_run.assert_called_once_with(["rsync", "test"], env={"test-env": "test"})


# Tests perform_autosync_synchronization for a git repository with a file that is ignored
def test_perform_autosync_synchronization_with_ignored_files() -> None:
    mock_proc = Mock()
    mock_proc.stdout = Mock()

    calls = 0

    def readline(*args: List[Any], **kwargs: Dict[str, Any]) -> bytes:
        nonlocal calls
        if calls == 0:
            calls += 1
            return b"test-file.py"
        else:
            return b"NoOp"

    mock_proc.stdout.readline.side_effect = readline

    with patch(
        "anyscale.autosync_heartbeat.subprocess.check_call"
    ) as mock_check_call, patch(
        "anyscale.autosync_heartbeat.subprocess.Popen"
    ) as mock_popen, patch(
        "anyscale.autosync_heartbeat.subprocess.check_output"
    ) as mock_check_output, patch(
        "anyscale.autosync_heartbeat.subprocess.run"
    ) as mock_run, patch(
        "anyscale.autosync_heartbeat.get_rsync_command"
    ) as mock_get_rsync_command, patch(
        "anyscale.autosync_heartbeat.tempfile.NamedTemporaryFile"
    ) as mock_temp_file:
        mock_check_call.return_value = None
        mock_popen.return_value.__enter__.return_value = mock_proc
        # Git check-ignore returns a file to ignore
        mock_check_output.return_value = b"../test-file.py"
        # Raise exception to exit out of infinite loop
        mock_run.side_effect = Exception()
        mock_get_rsync_command.return_value = (["rsync", "test"], {"test-env": "test"})
        mock_file = Mock()
        mock_temp_file.return_value.__enter__.return_value = mock_file
        mock_file.write.return_value = None

        with pytest.raises(Exception):
            perform_autosync_synchronization(
                ["fswatch"],
                {},
                ["ssh"],
                "project_folder",
                "test-user",
                "1.1.1.1",
                "target_folder",
                False,
            )

        mock_check_call.assert_called_once_with(
            ["git", "-C", ".", "rev-parse"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

        mock_popen.assert_called_once_with(["fswatch"], stdout=subprocess.PIPE, env={})

        mock_check_output.assert_called_once_with(
            ["git", "check-ignore", "../test-file.py"]
        )

        # No modified files (All ignored)
        mock_file.write.assert_not_called()

        mock_get_rsync_command.assert_called_once_with(
            ["ssh"],
            "project_folder",
            "test-user",
            "1.1.1.1",
            "target_folder",
            False,
            modified_files=mock_file,
        )

        mock_run.assert_called_once_with(["rsync", "test"], env={"test-env": "test"})


# Tests perform_autosync_synchronization works when not in a git repository
def test_perform_autosync_synchronization_non_git_repo() -> None:
    mock_proc = Mock()
    mock_proc.stdout = Mock()

    calls = 0

    def readline(*args: List[Any], **kwargs: Dict[str, Any]) -> bytes:
        nonlocal calls
        if calls == 0:
            calls += 1
            return b"test-file.py"
        else:
            return b"NoOp"

    mock_proc.stdout.readline.side_effect = readline

    with patch(
        "anyscale.autosync_heartbeat.subprocess.check_call"
    ) as mock_check_call, patch(
        "anyscale.autosync_heartbeat.subprocess.Popen"
    ) as mock_popen, patch(
        "anyscale.autosync_heartbeat.subprocess.check_output"
    ) as mock_check_output, patch(
        "anyscale.autosync_heartbeat.subprocess.run"
    ) as mock_run, patch(
        "anyscale.autosync_heartbeat.get_rsync_command"
    ) as mock_get_rsync_command, patch(
        "anyscale.autosync_heartbeat.tempfile.NamedTemporaryFile"
    ) as mock_temp_file:
        mock_check_call.side_effect = CalledProcessError(128, "test-cmd")
        mock_popen.return_value.__enter__.return_value = mock_proc
        mock_check_output.return_value = b""
        # Raise exception to exit out of infinite loop
        mock_run.side_effect = Exception()
        mock_get_rsync_command.return_value = (["rsync", "test"], {"test-env": "test"})

        mock_file = Mock()
        mock_temp_file.return_value.__enter__.return_value = mock_file
        mock_file.write.return_value = None

        with pytest.raises(Exception):
            perform_autosync_synchronization(
                ["fswatch"],
                {},
                ["ssh"],
                "project_folder",
                "test-user",
                "1.1.1.1",
                "target_folder",
                False,
            )

        mock_check_call.assert_called_once_with(
            ["git", "-C", ".", "rev-parse"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

        mock_popen.assert_called_once_with(["fswatch"], stdout=subprocess.PIPE, env={})

        # Git check-ignore not called
        mock_check_output.assert_not_called()

        mock_file.write.assert_called_once_with("../test-file.py\n")

        mock_get_rsync_command.assert_called_once_with(
            ["ssh"],
            "project_folder",
            "test-user",
            "1.1.1.1",
            "target_folder",
            False,
            modified_files=mock_file,
        )

        mock_run.assert_called_once_with(["rsync", "test"], env={"test-env": "test"})
