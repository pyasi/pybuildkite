from pybuildkite.client import Client


class Jobs(Client):
    """
    Job operations for the Buildkite API
    """

    def __init__(self, client, base_url):
        """
        Construct the class

        :param client: API Client
        :param base_url: Base Url
        """
        self.client = client
        self.path = base_url + "/organizations/{}/pipelines/{}/builds/{}/jobs/{}/"

    def get_job_log(self, organization, pipeline, build, job, get_text=False, get_html=False):
        """
        Get a job’s log output

        :param organization: Organization slug
        :param pipeline: Pipeline slug
        :param build: Build number
        :param job: Job id
        :param get_text: Unused
        :param get_html: Unused
        :return: Job log output
        """
        header = {'Accept': 'text/html'}
        return self.client.get(self.path.format(organization, pipeline, build, job) + "log", headers=header)

    def get_job_environment_variables(self, organization, pipeline, build, job):
        """
        Get a job's environment variables

        :param organization: Organization slug
        :param pipeline: Pipeline slug
        :param build: Build number
        :param job: Job id
        :return: Environment variables
        """
        return self.client.get(self.path.format(organization, pipeline, build, job) + "env")
