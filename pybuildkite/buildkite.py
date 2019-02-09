from pybuildkite.client import Client
from pybuildkite.organizations import Organizations
from pybuildkite.pipelines import Pipelines
from pybuildkite.builds import Builds, BuildState

class BuildKite(object):

    def __init__(self):
        """

        :param access_token:
        """
        self.client = Client()
        self.base_url = "https://api.buildkite.com/v2/"

    def set_access_token(self, access_token):
        """

        :param access_token:
        :return:
        """
        self.client.set_client_access_token(access_token)

    def requires_token(func):
        def wrapper(self, *args, **kwargs):
            if not self.client.is_access_token_set():
                raise NoAcccessTokenException
            else:
                return func(self, *args, **kwargs)

        return wrapper

    @requires_token
    def organizations(self):
        return Organizations(self.client, self.base_url)

    @requires_token
    def pipelines(self, organization):
        return Pipelines(self.client, self.base_url, organization)

    @requires_token
    def builds(self):
        return Builds(self.client, self.base_url)


class NoAcccessTokenException(Exception):
    pass
