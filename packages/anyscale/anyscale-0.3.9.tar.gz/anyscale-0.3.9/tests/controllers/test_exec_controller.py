from unittest.mock import Mock, patch

import pytest

from anyscale.client.openapi_client.models.command_id import CommandId  # type: ignore
from anyscale.client.openapi_client.models.commandid_response import CommandidResponse  # type: ignore
from anyscale.client.openapi_client.models.execute_shell_command_options import (  # type: ignore
    ExecuteShellCommandOptions,
)
from anyscale.controllers.exec_controller import ExecController


@pytest.fixture()  # type: ignore
def mock_api_client(command_id_test_data: CommandId) -> Mock:
    mock_api_client = Mock()

    mock_api_client.execute_interactive_command_api_v2_sessions_session_id_execute_interactive_command_post = Mock(
        return_value=CommandidResponse(result=command_id_test_data)
    )

    return mock_api_client


def test_anyscale_exec(mock_api_client: Mock, command_id_test_data: CommandId) -> None:
    mock_cluster_config = {"provider": {"default": "value"}, "cluster_name": "cname"}
    mock_get_cluster_config = Mock(return_value=mock_cluster_config)
    mock_rsync = Mock(return_value=None)
    mock_check_call = Mock(return_value=None)
    mock_click_echo = Mock(return_value=None)

    with patch.object(
        ExecController,
        "_get_session_name_and_id",
        return_value=("session_name", "session_id"),
    ) as mock_get_session_name_and_id, patch.object(
        ExecController, "_generate_remote_command", return_value="remote_command"
    ) as mock_generate_remote_command, patch.multiple(
        "anyscale.controllers.exec_controller",
        get_cluster_config=mock_get_cluster_config,
        rsync=mock_rsync,
    ), patch.multiple(
        "subprocess", check_call=mock_check_call
    ), patch.multiple(
        "click", echo=mock_click_echo
    ):
        commands = ["cmd1", "cmd2"]
        exec_controller = ExecController(api_client=mock_api_client)
        exec_controller.anyscale_exec(
            "session_name", True, True, (1000,), True, True, commands
        )

    mock_api_client.execute_interactive_command_api_v2_sessions_session_id_execute_interactive_command_post.assert_called_once_with(
        session_id="session_id",
        execute_shell_command_options=ExecuteShellCommandOptions(
            shell_command=" ".join(commands)
        ),
    )
    mock_get_session_name_and_id.assert_called_once_with("session_name")
    mock_generate_remote_command.assert_called_once_with(
        command_id_test_data.command_id,
        commands,
        command_id_test_data.directory_name,
        True,
    )
    mock_get_cluster_config.assert_called_once_with("session_name", mock_api_client)
    mock_rsync.assert_called_once()
    mock_check_call.assert_called_once()
    mock_click_echo.assert_called_once()
