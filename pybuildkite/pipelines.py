from pybuildkite.client import Client


class Pipelines(Client):
    """
    Pipeline operations for the Buildkite API
    """

    def __init__(self, client, base_url):
        """
        Construct the class

        :param client:
        :param base_url:
        """
        self.client = client
        self.path = base_url + "organizations/{}/pipelines/"

    def list_pipelines(self, organization):
        """
        Returns a paginated list of an organization’s pipelines.

        :param organization: Organization slug
        :return: Returns a paginated list of an organization’s pipelines.
        """
        return self.client.get(self.path.format(organization))

    def get_pipeline(self, organization, pipeline_name):
        """
        Get a pipeline

        :param organization: Organization slug
        :param pipeline_name: Pipeline slug
        :return: A pipeline
        """
        return self.client.get(self.path.format(organization) + pipeline_name)

    def create_pipeline(self, organization, pipeline_name, git_repository):
        """
        Create a pipeline
        :param organization: Organization slug
        :param pipeline_name:Pipeline slug
        :param git_repository: repo URL
        :return:
        """
        data = {'name': pipeline_name,
                'repository': git_repository,
                'steps': [dict(type='script', name=':pipeline:', command='buildkite-agent pipeline upload')]}

        return self.client.post(self.path.format(organization), body=data)

    def delete_pipeline(self, organization, pipeline):
        """
        Delete a pipeline
        :param organization: Organization slug
        :param pipeline_name:Pipeline slug
        :return:
        """
        url = self.path.format(organization) + pipeline
        return self.client.delete(url)
