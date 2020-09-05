import pytest

from pybuildkite.artifacts import Artifacts


def test_list_artifacts_for_build(fake_client):
    """
    Test List Artifacts for build
    """
    artifacts = Artifacts(fake_client, "base")
    artifacts.list_artifacts_for_build("org_slug", "pipe_slug", "build_no")
    url = "base/organizations/org_slug/pipelines/pipe_slug/builds/build_no/artifacts/"
    fake_client.get.assert_called_with(
        url, query_params={"page": 0}, with_pagination=False
    )


def test_list_artifacts_for_job(fake_client):
    """
    Test list artifacts for job
    """
    artifacts = Artifacts(fake_client, "base")
    artifacts.list_artifacts_for_job("org_slug", "pipe_slug", "build_no", 123)
    url = "base/organizations/org_slug/pipelines/pipe_slug/builds/build_no/jobs/123/artifacts/"
    fake_client.get.assert_called_with(
        url, query_params={"page": 0}, with_pagination=False
    )


def test_get_artifact(fake_client):
    """
    Test get Artifact
    """
    artifacts = Artifacts(fake_client, "base")
    artifacts.get_artifact("org_slug", "pipe_slug", "build_no", 123, "artifact")
    url = "base/organizations/org_slug/pipelines/pipe_slug/builds/build_no/jobs/123/artifacts/artifact/"
    fake_client.get.assert_called_with(url)


def test_download_artifact(fake_client):
    """
    Test download Artifact
    """
    artifacts = Artifacts(fake_client, "base")
    artifacts.download_artifact("org_slug", "pipe_slug", "build_no", 123, "artifact")
    url = "base/organizations/org_slug/pipelines/pipe_slug/builds/build_no/jobs/123/artifacts/artifact/download/"
    fake_client.get.assert_called_with(
        url, headers={"Accept": "application/octet-stream"}, as_stream=False
    )


def test_download_artifact_as_stream(fake_client):
    """
    Test download Artifact as stream
    """
    artifacts = Artifacts(fake_client, "base")
    artifacts.download_artifact(
        "org_slug", "pipe_slug", "build_no", 123, "artifact", as_stream=True
    )
    url = "base/organizations/org_slug/pipelines/pipe_slug/builds/build_no/jobs/123/artifacts/artifact/download/"
    fake_client.get.assert_called_with(
        url, headers={"Accept": "application/octet-stream"}, as_stream=True
    )
