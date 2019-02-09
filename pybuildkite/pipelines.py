from pybuildkite.client import Client


class Pipelines(Client):

    def __init__(self, client, base_url):
        """

        """
        self.client = client
        self.path = base_url + "organizations/{}/pipelines/"

    def list_pipelines(self, organization):
        """

        :param organization:
        :return:
        """
        return self.client.get(self.path.format(organization))

    def get_pipeline(self, organization, pipeline_name):
        """

        :param organization:
        :param pipeline_name:
        :return:
        """
        return self.client.get(self.path.format(organization) + pipeline_name)
