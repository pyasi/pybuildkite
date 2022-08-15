from pybuildkite.client import Client, RequestResponse


class Annotations(Client):
    """
    Annotation operations for the Buildkite API
    """

    def __init__(self, client: Client, base_url: str) -> None:
        """
        Construct the class

        :param client: API Client
        :param base_url: Base Url
        """
        self.client = client
        self.path = base_url + "organizations/{}/pipelines/{}/builds/{}/annotations/"

    def list_annotations(
        self,
        organization: str,
        pipeline: str,
        build: int | str,
        page: int = 0,
        with_pagination: bool = False,
    ) -> RequestResponse:
        """
        Returns a paginated list of the user’s annotations.

        :param organization: organization slug
        :param pipeline: pipeline slug
        :param build: build number
        :return: Returns a paginated list of the user’s annotations.
        """
        query_params = {"page": page}
        return self.client.get(
            self.path.format(organization, pipeline, build),
            query_params=query_params,
            with_pagination=with_pagination,
        )
