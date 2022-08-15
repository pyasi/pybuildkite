from posixpath import join as urljoin
from pybuildkite.client import Client, RequestResponse


class AccessTokens(Client):
    """
    Access Token operations for the Buildkite API
    """

    def __init__(self, client: Client, base_url: str) -> None:
        """
        Construct the class

        :param client: API Client
        :param base_url: Base Url
        """
        self.client = client
        self.path = urljoin(base_url, "access-token")

    def get_token(self) -> RequestResponse:
        """
        Get data on the token used for the request
        """
        return self.client.get(self.path)

    def revoke_token(self) -> RequestResponse:
        """
        Revoke the token that is used for the request.
        """
        return self.client.delete(self.path)
