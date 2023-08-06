from unittest.mock import Mock, patch

import pytest

from anyscale.client.openapi_client import Project  # type: ignore
from anyscale.client.openapi_client.models.project_list_response import (  # type: ignore
    ProjectListResponse,
)
from anyscale.controllers.project_controller import ProjectController


@pytest.fixture()  # type: ignore
def mock_api_client(project_test_data: Project) -> Mock:
    mock_api_client = Mock()

    mock_api_client.find_project_by_project_name_api_v2_projects_find_by_name_get.return_value = ProjectListResponse(
        results=[project_test_data]
    )
    mock_api_client.list_sessions_api_v2_sessions_get.return_value.results = []
    mock_api_client.get_project_latest_cluster_config_api_v2_projects_project_id_latest_cluster_config_get.return_value.result.config = (
        ""
    )

    return mock_api_client


def test_clone_project(project_test_data: Project, mock_api_client: Mock) -> None:
    project_controller = ProjectController(api_client=mock_api_client)

    os_makedirs_mock = Mock(return_value=None)
    with patch.multiple("os", makedirs=os_makedirs_mock), patch(
        "anyscale.project._write_cluster_config_to_disk"
    ) as write_cluster_config_mock:
        project_controller.clone(project_name=project_test_data.name)

    mock_api_client.find_project_by_project_name_api_v2_projects_find_by_name_get.assert_called_once_with(
        name=project_test_data.name,
    )
    mock_api_client.get_project_latest_cluster_config_api_v2_projects_project_id_latest_cluster_config_get.assert_called_once_with(
        project_test_data.id,
    )
    os_makedirs_mock.assert_called_once_with(project_test_data.name)
    write_cluster_config_mock.assert_called_once_with(
        project_test_data.id, "", project_test_data.name
    )
