from unittest.mock import Mock

from anyscale.autosync_heartbeat import managed_autosync_session


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
