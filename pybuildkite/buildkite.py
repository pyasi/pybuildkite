from pybuildkite.client import Client
from pybuildkite.organizations import Organizations
from pybuildkite.pipelines import Pipelines
from pybuildkite.builds import Builds, BuildState
from pybuildkite.jobs import Jobs, LogFormat
from pybuildkite.agents import Agents
from pybuildkite.emojis import Emojis
from pybuildkite.annotations import Annotations


class BuildKite(object):
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

    def requires_token(func):
        """
        This annotation protects API calls that require authentication.

        It will cause them to raise NoAcccessTokenException if the token is not set in the client.

        :return: Function decorated with the protection
        """

        def wrapper(self, *args, **kwargs):
            """
            Call func or raise NoAcccessTokenException if no access token is set

            :param self:
            :param args: Optional
            :param kwargs: Optional

            :raises NoAcccessTokenException: If no access token is set
            :return:
            """
            if not self.client.is_access_token_set():
                raise NoAcccessTokenException
            else:
                return func(self, *args, **kwargs)

        return wrapper

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

        :return: Client
        """
        return Emojis(self.client, self.base_url)

    @requires_token
    def annotations(self):
        """
        Get Annotation operations for the Buildkite API
        """
        return Annotations(self.client, self.base_url)


class NoAcccessTokenException(Exception):
    """
    Indicates that an access token was not set when it was required
    """

    pass
