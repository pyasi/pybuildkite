from pybuildkite.constants import APIVersion
from pybuildkite.base_client import BaseClient

# Preserve backwards-compatibility when this module exported the Response class.
from pybuildkite.response import Response


# TODO: Rename to BuildkiteClient.
class Client(BaseClient):
    """
    Internal API Client for the Buildkite REST API
    """

    def __init__(self, api_version: APIVersion = APIVersion.V2) -> None:
        super().__init__(api_version)

    def is_access_token_set(self):
        """
        Has this client got an access token set in it

        :return: true or false
        """
        return self._is_token_set()

    def set_client_access_token(self, access_token):
        """
        Set an access token to use for API calls
        :param access_token: The token
        """
        self.access_token = access_token

    @property
    def access_token(self) -> str:
        return self._token

    @access_token.setter
    def access_token(self, access_token: str) -> None:
        self._token = access_token

    def _get_authorization_header(self) -> str:
        return "Bearer {}".format(self.access_token)


class AgentClient(BaseClient):
    """
    Internal API Client for the Agent REST API
    """

    def __init__(self, api_version: APIVersion = APIVersion.V3) -> None:
        super().__init__(api_version)

    def is_agent_token_set(self) -> bool:
        """
        Has this client got an access token set in it

        :return: true or false
        """
        return self._is_token_set()

    def set_client_agent_token(self, agent_token: str) -> None:
        """
        Set an access token to use for API calls
        :param access_token: The token
        """
        self.agent_token = agent_token

    @property
    def agent_token(self) -> str:
        return self._token

    @agent_token.setter
    def agent_token(self, agent_token: str) -> None:
        self._token = agent_token

    def _get_authorization_header(self) -> str:
        return "Token {}".format(self.agent_token)
