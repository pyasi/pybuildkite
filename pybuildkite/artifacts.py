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

    def list_artifacts_for_build(
        self, organization, pipeline, build, page=0, with_pagination=False
    ):
        """
        Returns a paginated list of a build's artifacts across all of its jobs.

        :param organization: organization slug
        :param pipeline: pipeline slug
        :param build: build number
        :param page: Int to determine which page to read from (See Pagination in README)
        :param with_pagination: Bool to return a response with pagination attributes
        :return: Returns a paginated list of a build’s artifacts across all of its jobs.
        """
        url = self.path + "artifacts/"
        query_params = {"page": page}
        return self.client.get(
            url.format(organization, pipeline, build),
            query_params=query_params,
            with_pagination=with_pagination,
        )

    def list_artifacts_for_job(
        self, organization, pipeline, build, job, page=0, with_pagination=False
    ):
        """
        Returns a paginated list of a jobs's artifacts.

        :param organization: organization slug
        :param pipeline: pipeline slug
        :param build: build number
        :param job: job id
        :param page: Int to determine which page to read from (See Pagination in README)
        :param with_pagination: Bool to return a response with pagination attributes
        :return: Returns a paginated list of a job’s artifacts.
        """
        url = self.path + "jobs/{}/artifacts/"
        query_params = {"page": page}
        return self.client.get(
            url.format(organization, pipeline, build, job),
            query_params=query_params,
            with_pagination=with_pagination,
        )

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
