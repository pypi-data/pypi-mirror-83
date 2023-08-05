import datetime
import tempfile
from unittest.mock import Mock

from anyscale.client.openapi_client import Session  # type: ignore
from anyscale.client.openapi_client.models.project import Project  # type: ignore
from anyscale.util import (
    deserialize_datetime,
    download_anyscale_wheel,
    get_project_directory_name,
    get_working_dir,
    wait_for_session_start,
)


def test_deserialize_datetime() -> None:
    date_str = "2020-07-02T20:16:04.000000+00:00"
    assert deserialize_datetime(date_str) == datetime.datetime(
        2020, 7, 2, 20, 16, 4, tzinfo=datetime.timezone.utc
    )


def test_download_anyscale_wheel(base_mock_api_client: Mock) -> None:
    temp_file = tempfile.NamedTemporaryFile("w")
    mock_http_ret_val = Mock()
    mock_http_ret_val.headers = {
        "content-disposition": f'attachment; filename="{temp_file.name}"'
    }
    # This is not UTF-8 decodeable, like the wheel
    mock_http_ret_val.data = b"\x1f\x8b\x08\x08\x1b7\x86_\x02\xffdist/anyscale"
    base_mock_api_client.session_get_anyscale_wheel_api_v2_sessions_session_id_anyscale_wheel_get = Mock(
        return_value=mock_http_ret_val
    )
    download_anyscale_wheel(base_mock_api_client, "session_id")
    with open(temp_file.name, "rb") as result:
        assert result.read() == mock_http_ret_val.data

    base_mock_api_client.session_get_anyscale_wheel_api_v2_sessions_session_id_anyscale_wheel_get.assert_called_once()


def test_wait_for_session_start(
    mock_api_client_with_session: Mock, session_test_data: Session
) -> None:
    result = wait_for_session_start(
        session_test_data.project_id, session_test_data.id, mock_api_client_with_session
    )
    assert result == session_test_data.id


def test_get_project_directory_name(project_test_data: Project) -> None:
    mock_api_client = Mock()
    mock_api_client.get_project_api_v2_projects_project_id_get.return_value.result.directory_name = (
        project_test_data.directory_name
    )

    dir_name = get_project_directory_name(project_test_data.id, mock_api_client)

    assert dir_name == project_test_data.directory_name
    mock_api_client.get_project_api_v2_projects_project_id_get.assert_called_once_with(
        project_test_data.id
    )


def test_get_working_dir(project_test_data: Project) -> None:
    mock_api_client = Mock()
    mock_api_client.get_project_api_v2_projects_project_id_get.return_value.result.directory_name = (
        project_test_data.directory_name
    )

    working_dir = get_working_dir({}, project_test_data.id, mock_api_client)
    assert working_dir == f"~/{project_test_data.directory_name}"

    working_dir = get_working_dir(
        {"metadata": {"anyscale": {"working_dir": "test_working_dir"}}},
        project_test_data.id,
        mock_api_client,
    )
    assert working_dir == "test_working_dir"
