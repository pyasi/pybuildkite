from posixpath import join as urljoin

from pybuildkite.client import Client


class Meta(Client):
    """
    Meta operations for the Buildkite API
    """

    def __init__(self, client, base_url):
        """
        Construct the class

        :param client: API Client
        :param base_url: Base Url
        """
        self.client = client
        self.path = urljoin(base_url, "meta")

    def get_meta_information(self):
        """
        Returns meta information

        :return: Returns meta information
        """
        return self.client.get(self.path)
