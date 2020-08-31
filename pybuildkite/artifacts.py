from posixpath import join as urljoin
from pybuildkite.client import Client


class Artifacts(Client):
    """
    Artifacts operations for the Buildkite API
    """

    def __init__(self, client, base_url):
        """
        Construct the class

        :param client: API Client
        :param base_url: Base Url
        """
        self.client = client
        self.path = urljoin(base_url, "organizations/{}/pipelines/{}/builds/{}/")

    def list_artifacts_for_build(self, organization, pipeline, build):
        """
        Returns a paginated list of a build's artifacts across all of its jobs.

        :param organization: organization slug
        :param pipeline: pipeline slug
        :param build: build number
        :return: Returns a paginated list of a build’s artifacts across all of its jobs.
        """
        url = self.path + "artifacts/"
        return self.client.get(url.format(organization, pipeline, build))

    def list_artifacts_for_job(self, organization, pipeline, build, job):
        """
        Returns a paginated list of a jobs's artifacts.

        :param organization: organization slug
        :param pipeline: pipeline slug
        :param build: build number
        :param job: job id
        :return: Returns a paginated list of a job’s artifacts.
        """
        url = self.path + "jobs/{}/artifacts/"
        return self.client.get(url.format(organization, pipeline, build, job))

    def get_artifact(self, organization, pipeline, build, job, artifact):
        """
        Returns an artifact.

        :param organization: organization slug
        :param pipeline: pipeline slug
        :param build: build number
        :param job: job id
        :param artifact: artifact id
        :return: Returns an artifact.
        """
        url = self.path + "jobs/{}/artifacts/{}/"
        return self.client.get(url.format(organization, pipeline, build, job, artifact))

    def download_artifact(
        self, organization, pipeline, build, job, artifact, as_stream=False
    ):
        """
        Returns the content of an artifact as bytes.

        With as_stream=True you get an iterator of bytes chunks.

        :param organization: organization slug
        :param pipeline: pipeline slug
        :param build: build number
        :param job: job id
        :param artifact: artifact id
        :param as_stream: stream the artifact content
        :return: Returns the content of an artifact.
        """
        headers = {"Accept": "application/octet-stream"}
        url = self.path + "jobs/{}/artifacts/{}/download/"
        return self.client.get(
            url.format(organization, pipeline, build, job, artifact),
            headers=headers,
            as_stream=as_stream,
        )

    # TODO Delete artifact
