from posixpath import join as urljoin
from pybuildkite.client import Client


class Agents(Client):
    """
    Agent operations for the Buildkite API
    """

    def __init__(self, client, base_url):
        """
        Construct the class

        :param client: API Client
        :param base_url: Base Url
        """
        self.client = client
        self.path = urljoin(base_url, "organizations/{}/agents/")

    def list_all(
        self,
        organization,
        name=None,
        hostname=None,
        version=None,
        page=0,
        with_pagination=False,
    ):
        """
        Returns a paginated list of an organization’s agents.

        :param organization: Organization slug
        :param name: Filters the results by the given agent name
        :param hostname: Filters the results by the given hostname
        :param version: Filters the results by the given exact version number
        :param page: Int to determine which page to read from (See Pagination in README)
        :param with_pagination: Bool to return a response with pagination attributes
        :return: Returns a paginated list of an organization’s agents
        """
        query_params = {
            "name": name,
            "hostname": hostname,
            "version": version,
            "page": page,
        }
        return self.client.get(
            self.path.format(organization),
            query_params,
            with_pagination=with_pagination,
        )

    def get_agent(self, organization, agent_id):
        """
        Get an agent

        :param organization: Organization slug
        :param agent_id: Agent id
        :return: Single agent
        """
        return self.client.get(self.path.format(organization) + agent_id)

    def stop_agent(self, organization, agent_id, force=True):
        """
        Stop an agent

        :param organization: Organization slug
        :param agent_id: Agent id
        :param force: Whether or not to force the agent to stop if processing a job
        :return: no content
        """
        body = {"force": force}
        stop = "/stop"
        return self.client.put(
            self.path.format(organization) + agent_id + stop, body=body
        )
