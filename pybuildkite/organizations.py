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
        self.path = base_url + "organizations/"

    def list_all(self, page=0, with_pagination=False):
        """
        Returns a paginated list of the user’s organizations.

        :param page: Int to determine which page to read from (See Pagination in README)
        :param with_pagination: Bool to return a response with pagination attributes
        :return: Paginated list of the user’s organizations.
        """
        query_params = {"page": page}
        return self.client.get(
            self.path, query_params=query_params, with_pagination=with_pagination
        )

    def get_org(self, org_name):
        """
        Get an organization

        :param org_name: Organisation slug
        :return: Organisation
        """
        return self.client.get(self.path + org_name)
