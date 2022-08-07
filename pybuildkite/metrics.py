from posixpath import join as urljoin
from pybuildkite.client import AgentClient as Client


class Metrics(Client):
    """
    Metrics operations for the Agent API
    """

    def __init__(self, client: Client, base_url: str) -> None:
        """
        Construct the class

        :param client: API Client
        :param base_url: Base Url
        """
        self.client = client
        self.path = urljoin(base_url, "metrics")

    def get_metrics(self):
        """
        Returns a paginated list of an organization’s agents.

        """
        return self.client.get(self.path)
