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
        self.path = base_url + "organizations/{}/pipelines/{}/builds/{}/"

    def list_artifacts_for_job(self, organization, pipeline, build):
        """
        Returns a paginated list of a job’s artifacts.

        :param organization: organization slug
        :param pipeline: pipeline slug
        :param build: build number
        :return: Returns a paginated list of a job’s artifacts.
        """
        url = self.path + "artifacts/"
        return self.client.get(url.format(organization, pipeline, build))

    def list_artifacts_for_build(self, organization, pipeline, build, job):
        """
        Returns a paginated list of a build’s artifacts across all of its jobs.

        :param organization: organization slug
        :param pipeline: pipeline slug
        :param build: build number
        :param job: job id
        :return: Returns a paginated list of a build’s artifacts across all of its jobs.
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

    def download_artifact(self, organization, pipeline, build, job, artifact):
        """
        Returns a URL for downloading an artifact.

        :param organization: organization slug
        :param pipeline: pipeline slug
        :param build: build number
        :param job: job id
        :param artifact: artifact id
        :return: Returns a URL for downloading an artifact.
        """
        url = self.path + "jobs/{}/artifacts/{}/download/"
        return self.client.get(url.format(organization, pipeline, build, job, artifact))
