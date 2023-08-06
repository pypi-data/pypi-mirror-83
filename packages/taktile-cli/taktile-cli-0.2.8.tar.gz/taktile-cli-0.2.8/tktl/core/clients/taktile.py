from collections import defaultdict
from typing import Dict, List, Union

from .. import loggers as sdk_logger
from ..config import settings
from ..exceptions import TaktileSdkError
from ..managers.auth import AuthConfigManager
from ..schemas.repository import (
    Endpoint,
    Repository,
    RepositoryDeployment,
    RepositoryList,
)
from ..utils import flatten, lru_cache
from .http_client import API, interpret_response


class TaktileClient(API):

    SCHEME: str

    def __init__(self, api_url, logger=sdk_logger.MuteLogger()):
        """
        Base class. All client classes inherit from it.
        """
        super().__init__(api_url, logger=logger)
        self.api_url = api_url
        self.api_key = AuthConfigManager.get_api_key()
        self.logger = logger

    @lru_cache(timeout=50, typed=False)
    def __get_repositories(self) -> RepositoryList:
        response = self.get(f"{settings.API_V1_STR}/models")
        return interpret_response(response=response, model=RepositoryList)

    def _get_repositories(self):
        repositories = self.__get_repositories()
        return repositories

    def get_endpoints_for_repository(
        self, repository: str
    ) -> List[Dict[str, Union[Endpoint, RepositoryDeployment]]]:
        repos = self._get_repositories()
        if not repos:
            raise TaktileSdkError("No repos found")
        repo_models = repos.get_repositories()
        repo_endpoints = repos.get_endpoints()
        repo_deployments = repos.get_deployments()
        mapping = defaultdict(list)
        for repo, endpoint, deployment in zip(
            repo_models, repo_endpoints, repo_deployments
        ):
            mapping[f"{repo.repository_owner}/{repo.repository_name}"].append(
                {"endpoint": endpoint, "deployment": deployment}
            )
        if repository not in mapping.keys():
            raise TaktileSdkError(
                f"Repository {repository} not found. Available repos: {list(mapping.keys())}"
            )
        return mapping[repository]
