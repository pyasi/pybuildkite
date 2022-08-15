from pybuildkite.client import Client
from pybuildkite.organizations import Organizations
from pybuildkite.pipelines import Pipelines
from pybuildkite.builds import Builds, BuildState
from pybuildkite.jobs import Jobs, LogFormat
from pybuildkite.agents import Agents
from pybuildkite.emojis import Emojis
from pybuildkite.annotations import Annotations
from pybuildkite.artifacts import Artifacts
from pybuildkite.teams import Teams
from pybuildkite.users import Users
from pybuildkite.access_tokens import AccessTokens
from pybuildkite.meta import Meta
from pybuildkite.decorators import requires_token


class Buildkite(object):
    """
    Public API for Buildkite
    """

    def __init__(self) -> None:
        """
        Create a new client
        """
        self.client = Client()
        self.base_url = "https://api.buildkite.com/v2/"

    def set_access_token(self, access_token: str) -> None:
        """
        Set the access token to be used to authenticate the requests
        :param access_token: The access token
        """
        self.client.set_client_access_token(access_token)

    @requires_token
    def organizations(self) -> Organizations:
        """
        Get Organization operations for the Buildkite API

        :return: Client
        """
        return Organizations(self.client, self.base_url)

    @requires_token
    def pipelines(self) -> Pipelines:
        """
        Get Pipeline operations for the Buildkite API

        :return: Client
        """
        return Pipelines(self.client, self.base_url)

    @requires_token
    def builds(self) -> Builds:
        """
        Get Build operations for the Buildkite API

        :return: Client
        """
        return Builds(self.client, self.base_url)

    @requires_token
    def jobs(self) -> Jobs:
        """
        Get Job operations for the Buildkite API

        :return: Client
        """
        return Jobs(self.client, self.base_url)

    @requires_token
    def agents(self) -> Agents:
        """
        Get Agent operations for the Buildkite API

        :return: Client
        """
        return Agents(self.client, self.base_url)

    @requires_token
    def emojis(self) -> Emojis:
        """
        Get Emoji operations for the Buildkite API
        """
        return Emojis(self.client, self.base_url)

    @requires_token
    def annotations(self) -> Annotations:
        """
        Get Annotation operations for the Buildkite API
        """
        return Annotations(self.client, self.base_url)

    @requires_token
    def artifacts(self) -> Artifacts:
        """
        Get Artifact operations for the Buildkite API
        """
        return Artifacts(self.client, self.base_url)

    @requires_token
    def teams(self) -> Teams:
        """
        Get Team operations for the Buildkite API
        """
        return Teams(self.client, self.base_url)

    @requires_token
    def users(self) -> Users:
        """
        Get User operations for the Buildkite API
        """
        return Users(self.client, self.base_url)

    @requires_token
    def access_tokens(self) -> AccessTokens:
        """
        Get Access Token operations for the Buildkite API

        :return: Client
        """
        return AccessTokens(self.client, self.base_url)

    def meta(self) -> Meta:
        """
        Get Meta operations for the Buildkite API

        :return: Client
        """
        return Meta(self.client, self.base_url)
