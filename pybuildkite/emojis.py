from pybuildkite.client import Client, RequestResponse


class Emojis(Client):
    """
    Emoji operations for the Buildkite API
    """

    def __init__(self, client: Client, base_url: str) -> None:
        """
        Construct the class

        :param client: API Client
        :param base_url: Base Url
        """
        self.client = client
        self.path = base_url + "organizations/{}/emojis/"

    def list_emojis(
        self, organization: str, page: int = 0, with_pagination: bool = False
    ) -> RequestResponse:
        """
        Returns a list of all the emojis for a given organization

        :param organization: organization slug
        :param page: Int to determine which page to read from (See Pagination in README)
        :param with_pagination: Bool to return a response with pagination attributes
        :return: Returns a list of all the emojis for a given organization
        """
        query_parms = {"page": page}
        return self.client.get(
            self.path.format(organization),
            query_params=query_parms,
            with_pagination=with_pagination,
        )
