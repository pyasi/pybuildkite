from unittest.mock import Mock

import pytest

from pybuildkite.artifacts import Artifacts


class TestArtifacts:
    """
    Test functionality of the Jobs class
    """

    @pytest.fixture
    def fake_client(self):
        """
        Build a fake API client
        """
        return Mock(get=Mock())

    def test_list_artifacts_for_build(self, fake_client):
        """
        Test List Artifacts for build
        """
        artifacts = Artifacts(fake_client, "base")
        artifacts.list_artifacts_for_build("org_slug", "pipe_slug", "build_no")
        url = (
            "baseorganizations/org_slug/pipelines/pipe_slug/builds/build_no/artifacts/"
        )
        fake_client.get.assert_called_with(url)

    def test_list_artifacts_for_job(self, fake_client):
        """
        Test list artifacts for job
        """
        artifacts = Artifacts(fake_client, "base")
        artifacts.list_artifacts_for_job("org_slug", "pipe_slug", "build_no", 123)
        url = "baseorganizations/org_slug/pipelines/pipe_slug/builds/build_no/jobs/123/artifacts/"
        fake_client.get.assert_called_with(url)

    def test_get_artifact(self, fake_client):
        """
        Test get Artifact
        """
        artifacts = Artifacts(fake_client, "base")
        artifacts.get_artifact("org_slug", "pipe_slug", "build_no", 123, "artifact")
        url = "baseorganizations/org_slug/pipelines/pipe_slug/builds/build_no/jobs/123/artifacts/artifact/"
        fake_client.get.assert_called_with(url)

    def test_download_artifact(self, fake_client):
        """
        Test download Artifact
        """
        artifacts = Artifacts(fake_client, "base")
        artifacts.download_artifact(
            "org_slug", "pipe_slug", "build_no", 123, "artifact"
        )
        url = "baseorganizations/org_slug/pipelines/pipe_slug/builds/build_no/jobs/123/artifacts/artifact/download/"
        fake_client.get.assert_called_with(url)
