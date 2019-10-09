from pybuildkite.client import Client


class Emojis(Client):
    """
    Emoji operations for the Buildkite API
    """

    def __init__(self, client, base_url):
        """
        Construct the class

        :param client: API Client
        :param base_url: Base Url
        """
        self.client = client
        self.path = base_url + "organizations/{}/emojis/"

    def list_emojis(self, organization):
        """
        Returns a list of all the emojis for a given organization

        :param organization: organization slug
        :return: Returns a list of all the emojis for a given organization
        """
        return self.client.get(self.path.format(organization))
