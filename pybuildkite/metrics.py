from posixpath import join as urljoin
from pybuildkite.client import Client
from pybuildkite.constants import APIVersion


class Metrics(Client):
    """
    Metrics operations for the Agent API
    """

    def __init__(self, client: Client, base_url: str):
        """
        Construct the class

        :param client: API Client
        :param base_url: Base Url
        """
        self.client = client
        self.client._api_version = APIVersion.V3
        self.path = urljoin(base_url, "metrics")

    def get_metrics(
        self,
    ):
        """
        Returns a paginated list of an organization’s agents.

        """
        return self.client.get(
            self.path,
        )
