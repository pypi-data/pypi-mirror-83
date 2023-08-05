import os
from typing import Optional

from anyscale.api import get_api_client
from anyscale.client.openapi_client.api.default_api import DefaultApi  # type: ignore
from anyscale.project import (
    clone_cluster_config,
    get_proj_id_from_name,
)


class ProjectController:
    def __init__(self, api_client: Optional[DefaultApi] = None):
        if api_client is None:
            api_client = get_api_client()
        self.api_client = api_client

    def clone(self, project_name: str) -> None:
        project_id = get_proj_id_from_name(project_name, self.api_client)

        os.makedirs(project_name)
        clone_cluster_config(project_name, project_name, project_id, self.api_client)
