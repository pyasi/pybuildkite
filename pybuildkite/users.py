from pybuildkite.client import Client


class Users(Client):
    """
    User operations for the Buildkite API
    """

    def __init__(self, client: Client, base_url: str) -> None:
        """
        Construct the class

        :param client: API Client
        :param base_url: Base Url
        """
        self.client = client
        self.path = base_url + "user"

    def get_current_user(self):
        """
        Returns the current user

        :return: Returns current user
        """
        return self.client.get(self.path)
