from pybuildkite.client import Client


class Emojis(Client):

    def __init__(self, client, base_url):
        """

        """
        self.client = client
        self.path = base_url + "organizations/{}/emojis/"

    def list_emojis(self, organization):
        """

        :param organization:
        :return:
        """
        return self.client.get(self.path.format(organization))
