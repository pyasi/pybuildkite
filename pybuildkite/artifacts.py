from pybuildkite.client import Client


class Artifacts(Client):

    def __init__(self, client, base_url):
        """

        """
        self.client = client
        self.path = base_url + "organizations/{}/pipelines/{}/builds/{}/"

    def list_artifacts_for_job(self, organization, pipeline, build):
        """

        :param organization:
        :param pipeline:
        :param build:
        :return:
        """
        url = self.path + "artifacts/"
        return self.client.get(url.format(organization, pipeline, build))

    def list_artifacts_for_build(self, organization, pipeline, build, job):
        """

        :param organization:
        :param pipeline:
        :param build:
        :param job:
        :return:
        """
        url = self.path + "jobs/{}/artifacts/"
        return self.client.get(url.format(organization, pipeline, build, job))

    def get_artifact(self, organization, pipeline, build, job, artifact):
        """

        :param organization:
        :param pipeline:
        :param build:
        :param job:
        :param artifact:
        :return:
        """
        url = self.path + "jobs/{}/artifacts/{}/"
        return self.client.get(url.format(organization, pipeline, build, job, artifact))

    def download_artifact(self, organization, pipeline, build, job, artifact):
        """

        :param organization:
        :param pipeline:
        :param build:
        :param job:
        :param artifact:
        :return:
        """
        url = self.path + "jobs/{}/artifacts/{}/download/"
        return self.client.get(url.format(organization, pipeline, build, job, artifact))
