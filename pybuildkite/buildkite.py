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

    def __init__(self):
        """
        Create a new client
        """
        self.client = Client()
        self.base_url = "https://api.buildkite.com/v2/"

    def set_access_token(self, access_token):
        """
        Set the access token to be used to authenticate the requests
        :param access_token: The access token
        """
        self.client.set_client_access_token(access_token)

    @requires_token
    def organizations(self):
        """
        Get Organization operations for the Buildkite API

        :return: Client
        """
        return Organizations(self.client, self.base_url)

    @requires_token
    def pipelines(self):
        """
        Get Pipeline operations for the Buildkite API

        :return: Client
        """
        return Pipelines(self.client, self.base_url)

    @requires_token
    def builds(self):
        """
        Get Build operations for the Buildkite API

        :return: Client
        """
        return Builds(self.client, self.base_url)

    @requires_token
    def jobs(self):
        """
        Get Job operations for the Buildkite API

        :return: Client
        """
        return Jobs(self.client, self.base_url)

    @requires_token
    def agents(self):
        """
        Get Agent operations for the Buildkite API

        :return: Client
        """
        return Agents(self.client, self.base_url)

    @requires_token
    def emojis(self):
        """
        Get Emoji operations for the Buildkite API
        """
        return Emojis(self.client, self.base_url)

    @requires_token
    def annotations(self):
        """
        Get Annotation operations for the Buildkite API
        """
        return Annotations(self.client, self.base_url)

    @requires_token
    def artifacts(self):
        """
        Get Artifact operations for the Buildkite API
        """
        return Artifacts(self.client, self.base_url)

    @requires_token
    def teams(self):
        """
        Get Team operations for the Buildkite API
        """
        return Teams(self.client, self.base_url)

    @requires_token
    def users(self):
        """
        Get User operations for the Buildkite API
        """
        return Users(self.client, self.base_url)

    @requires_token
    def access_tokens(self):
        """
        Get Access Token operations for the Buildkite API

        :return: Client
        """
        return AccessTokens(self.client, self.base_url)

    def meta(self):
        """
        Get Meta operations for the Buildkite API

        :return: Client
        """
        return Meta(self.client, self.base_url)
