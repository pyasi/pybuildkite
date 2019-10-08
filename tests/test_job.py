import pytest
from pybuildkite.jobs import Jobs
from pybuildkite.client import Client
from requests.exceptions import HTTPError

class TestJob:

    client = Client()
    url = 'https://api.buildkite.com/v2/'

    def test_Jobs(self) :

        job = Jobs(self.client, self.url)
        assert job.client == self.client
        assert job.path == self.url+"/organizations/{}/pipelines/{}/builds/{}/jobs/{}/"

    def test_get_job_log(self):

        jobs = Jobs(self.client, self.url)
        organization = 'TestOrganization'
        pipeline = 'TestPipeline'
        build = 'TestBuild'
        job = 'TestJob'
        with pytest.raises(HTTPError) as e:
            jobs.get_job_log(organization, pipeline, build, job)
        assert "HTTPError" in str(e)

    def test_get_job_environment_variables(self):

        jobs = Jobs(self.client, self.url)
        organization = 'TestOrganization'
        pipeline = 'TestPipeline'
        build = 'TestBuild'
        job = 'TestJob'
        with pytest.raises(HTTPError) as e:
            jobs.get_job_environment_variables(organization, pipeline, build, job)
        assert "HTTPError" in str(e)



