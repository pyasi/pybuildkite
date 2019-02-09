from pybuildkite.client import Client


class Organizations(Client):

    def __init__(self, client, base_url):
        """

        """
        self.client = client
        self.path = base_url + 'organizations/'

    def list_all(self):
        return self.client.get(self.path)

    def get_org(self, org_name):
        return self.client.get(self.path + org_name)
