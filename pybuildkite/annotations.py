from pybuildkite.client import Client


class Annotations(Client):

    def __init__(self, client, base_url):
        """

        """
        self.client = client
        self.path = base_url + "organizations/{}/pipelines/{}/builds/{}/annotations/"

    def list_annotations(self, organization, pipeline, build):
        """

        :param organization:
        :param pipeline:
        :param build:
        :return:
        """
        return self.client.get(self.path.format(organization, pipeline, build))
