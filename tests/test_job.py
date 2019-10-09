import pytest
from pybuildkite.jobs import Jobs
from pybuildkite.client import Client


@pytest.fixture()
def setup_job(mocker):
    mocker.patch('pybuildkite.client.Client.get', return_value='PASS')
    client = Client()
    url = 'https://api.buildkite.com/v2'
    job = Jobs(client, url)
    yield job


def test_jobs(setup_job) :
    assert setup_job.client == setup_job.client
    assert setup_job.path == 'https://api.buildkite.com/v2/organizations/{}/pipelines/{}/builds/{}/jobs/{}/'


def test_get_job_log(setup_job):
    organization = 'TestOrganization'
    pipeline = 'TestPipeline'
    build = 'TestBuild'
    job = 'TestJob'
    result = setup_job.get_job_log(organization, pipeline, build, job)
    assert "PASS" in result


def test_get_job_environment_variables(setup_job):
    organization = 'TestOrganization'
    pipeline = 'TestPipeline'
    build = 'TestBuild'
    job = 'TestJob'
    result=setup_job.get_job_environment_variables(organization, pipeline, build, job)
    assert "PASS" in result



