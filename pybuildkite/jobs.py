from pybuildkite.client import Client


class Jobs(Client):

    def __init__(self, client, base_url):
        """

        """
        self.client = client
        self.path = base_url + "/organizations/{}/pipelines/{}/builds/{}/jobs/{}/"

    def get_job_log(self, organization, pipeline, build, job, get_text=False, get_html=False):
        header = {'Accept': 'text/html'}
        return self.client.get(self.path.format(organization, pipeline, build, job) + "log", headers=header)

    def get_job_environment_variables(self, organization, pipeline, build, job):
        return self.client.get(self.path.format(organization, pipeline, build, job) + "env")
