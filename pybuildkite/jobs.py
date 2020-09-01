from enum import Enum
from posixpath import join as urljoin

from pybuildkite.client import Client


class LogFormat(Enum):
    """
    Valid log formats
    """

    TEXT = "text/plain"
    HTML = "text/html"
    JSON = "application/json"

    def __str__(self):
        return self.value


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
        self.path = urljoin(base_url, "organizations/{}/pipelines/{}/builds/{}/jobs/{}")

    def get_job_log(
        self, organization, pipeline, build, job, log_format=LogFormat.HTML
    ):
        """
        Get a job’s log output

        :param organization: Organization slug
        :param pipeline: Pipeline slug
        :param build: Build number
        :param job: Job id
        :param log_format: Mime type to return log in
        :return: Job log output
        """
        header = {"Accept": str(log_format)}
        return self.client.get(
            self.path.format(organization, pipeline, build, job) + "/log",
            headers=header,
        )

    def get_job_environment_variables(self, organization, pipeline, build, job):
        """
        Get a job's environment variables

        :param organization: Organization slug
        :param pipeline: Pipeline slug
        :param build: Build number
        :param job: Job id
        :return: Environment variables
        """
        return self.client.get(
            self.path.format(organization, pipeline, build, job) + "/env"
        )

    def retry_job(self, organization, pipeline, build, job):
        """
        Retries a failed or timed_out job.
         :param organization: Organization slug
        :param pipeline: Pipeline slug
        :param build: Build number
        :param job: Job id
        :return: response
        """
        retry = "/retry"
        return self.client.put(
            self.path.format(organization, pipeline, build, job) + retry
        )

    def unblock_job(self, organization, pipeline, build, job, fields, unblocker=None):
        """
        Unblocks a build’s "Block pipeline" job.
        :param organization: Organization slug
        :param pipeline: Pipeline slug
        :param build: Build number
        :param job: Job id
        :fields: name and email
        :unblocker: The user id of the person activating the job
        :return: response
        """
        unblock = "/unblock"
        body = {"fields": fields, "unblocker": unblocker}
        return self.client.put(
            self.path.format(organization, pipeline, build, job) + unblock, body=body
        )

    def delete_job_log(self, organization, pipeline, build, job):
        """
        Delete a job’s log output
        :param organization: organization slug
        :param pipeline: pipeline slug
        :param build: Build number
        :param job: job id
        :return: success response 204 No content
        """
        log = "/log"
        return self.client.delete(
            self.path.format(organization, pipeline, build, job) + log
        )
