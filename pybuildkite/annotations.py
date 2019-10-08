from pybuildkite.client import Client


class Annotations(Client):
    """
    Annotation operations for the Buildkite API
    """
    def __init__(self, client, base_url):
        """
        Construct the class

        :param client: API Client
        :param base_url: Base Url
        """
        self.client = client
        self.path = base_url + "organizations/{}/pipelines/{}/builds/{}/annotations/"

    def list_annotations(self, organization, pipeline, build):
        """
        Returns a paginated list of the user’s annotations.

        :param organization: organization slug
        :param pipeline: pipeline slug
        :param build: build number
        :return: Returns a paginated list of the user’s annotations.
        """
        return self.client.get(self.path.format(organization, pipeline, build))
