from pybuildkite.client import Client


class Teams(Client):
    """
    Teams operations for the Buildkite API
    """

    def __init__(self, client: Client, base_url: str) -> None:
        """
        Construct the class

        :param client: API Client
        :param base_url: Base Url
        """
        self.client = client
        self.path = base_url + "organizations/{}/teams"

    def list_teams(
        self,
        organization: str,
        user_id: str = None,
        page: int = 0,
        with_pagination: bool = False,
    ):
        """
        Returns a list of all the teams for a given organization

        :param organization: organization slug
        :param page: Int to determine which page to read from (See Pagination in README)
        :param with_pagination: bool to return a response with pagination attributes
        :return: Returns a list of all the teams for a given organization
        """
        query_parms = {"page": page, "user_id": user_id}
        return self.client.get(
            self.path.format(organization),
            query_params=query_parms,
            with_pagination=with_pagination,
        )
