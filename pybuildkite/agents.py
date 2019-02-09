from pybuildkite.client import Client


class Agents(Client):

    def __init__(self, client, base_url):
        """

        """
        self.client = client
        self.path = base_url + 'organizations/{}/agents/'

    def list_all(self, organizations, name=None, hostname=None, version=None):

        query_params = {
            "name": name,
            "hostname": hostname,
            "version": version
        }
        return self.client.get(self.path.format(organizations), query_params)

    def get_agent(self, organization, agent_id):
        return self.client.get(self.path.format(organization) + agent_id)
