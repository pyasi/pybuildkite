from pybuildkite.client import Client


class Pipelines(Client):

    def __init__(self, client, base_url, organization):
        """

        """
        self.client = client
        self.path = base_url + 'organizations/' + organization + "/pipelines/"

    def list_pipelines(self):
        """

        :return:
        """
        return self.client.get(self.path)

    def get_pipeline(self, pipeline_name):
        """

        :param pipeline_name:
        :return:
        """
        return self.client.get(self.path + pipeline_name)
