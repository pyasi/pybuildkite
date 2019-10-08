from pybuildkite.client import Client


class Organizations(Client):
    """
    Organization operations for the Buildkite API
    """
    def __init__(self, client, base_url):
        """
        Construct the class

        :param client: API Client
        :param base_url: Base Url
        """
        self.client = client
        self.path = base_url + 'organizations/'

    def list_all(self):
        """
        Returns a paginated list of the user’s organizations.

        :return: Paginated list of the user’s organizations.
        """
        return self.client.get(self.path)

    def get_org(self, org_name):
        """
        Get an organization

        :param org_name: Organisation slug
        :return: Organisation
        """
        return self.client.get(self.path + org_name)
