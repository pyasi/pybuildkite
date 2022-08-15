from posixpath import join as urljoin

from pybuildkite.client import Client, RequestResponse


class Meta(Client):
    """
    Meta operations for the Buildkite API
    """

    def __init__(self, client: Client, base_url: str) -> None:
        """
        Construct the class

        :param client: API Client
        :param base_url: Base Url
        """
        self.client = client
        self.path = urljoin(base_url, "meta")

    def get_meta_information(self) -> RequestResponse:
        """
        Returns meta information

        :return: Returns meta information
        """
        return self.client.get(self.path)
