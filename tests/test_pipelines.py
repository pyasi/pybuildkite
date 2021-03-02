from pybuildkite.pipelines import PipelineException, Pipelines

import pytest


def test_Pipelines(fake_client):
    """
    Test organization classes instances
    """
    pipeline = Pipelines(fake_client, "https://api.buildkite.com/v2/")
    assert pipeline.client == fake_client
    assert pipeline.path == "https://api.buildkite.com/v2/organizations/{}/pipelines/"


def test_list_pipelines(fake_client):
    """
    Test organization class 'list_pipelines()'  Method
    """
    pipelines = Pipelines(fake_client, "https://api.buildkite.com/v2/")
    pipelines.list_pipelines("Test_org")
    fake_client.get.assert_called_with(
        pipelines.path.format("Test_org"),
        query_params={"page": 0},
        with_pagination=False,
    )


def test_get_pipeline(fake_client):
    """
    Test organization class 'get_pipeline()' method
    """
    pipeline = Pipelines(fake_client, "https://api.buildkite.com/v2/")
    pipeline.get_pipeline("Test_org", "Test_pipeline")
    fake_client.get.assert_called_with(
        pipeline.path.format("Test_org") + "Test_pipeline"
    )


def test_create_pipeline(fake_client):
    pipeline = Pipelines(fake_client, "https://api.buildkite.com/v2/")
    pipeline.create_pipeline("test_org", "test_pipeline", "my_repo")
    fake_client.post.assert_called_with(
        pipeline.path.format("test_org"),
        body={
            "name": "test_pipeline",
            "repository": "my_repo",
            "steps": [
                {
                    "type": "script",
                    "name": ":pipeline:",
                    "command": "buildkite-agent pipeline upload",
                }
            ],
        }
    )


def test_create_yaml_pipeline(fake_client):
    pipeline = Pipelines(fake_client, "https://api.buildkite.com/v2/")
    pipeline.create_yaml_pipeline("test_org", "test_pipeline", "my_repo", "steps:\n  - command: ls")
    fake_client.post.assert_called_with(
        pipeline.path.format("test_org"),
        body={
            "name": "test_pipeline",
            "repository": "my_repo",
            "configuration": "steps:\n  - command: ls",
        },
    )


def test_delete_pipeline(fake_client):
    pipeline = Pipelines(fake_client, "https://api.buildkite.com/v2/")
    pipeline.delete_pipeline("test_org", "test_pipeline")
    fake_client.delete.assert_called_with(
        pipeline.path.format("test_org") + "test_pipeline"
    )


def test_update_pipeline(fake_client):
    pipeline = Pipelines(fake_client, "https://api.buildkite.com/v2/")
    pipeline.update_pipeline(
        "test_org",
        "test_pipeline",
        name="Name Change Test",
        env={"TEST_ENV_VAR": "VALUE"},
        skip_queued_branch_builds=True,
    )
    fake_client.patch.assert_called_with(
        pipeline.path.format("test_org") + "test_pipeline",
        body={
            "branch_configuration": None,
            "cancel_running_branch_builds": None,
            "cancel_running_branch_builds_filter": None,
            "default_branch": None,
            "description": None,
            "env": {"TEST_ENV_VAR": "VALUE"},
            "name": "Name Change Test",
            "provider_settings": None,
            "repository": None,
            "steps": None,
            "configuration": None,
            "skip_queued_branch_builds": True,
            "skip_queued_branch_builds_filter": None,
            "visibility": None,
        },
    )

def test_update_pipeline_configuration_and_steps(fake_client):
    with pytest.raises(PipelineException):
        pipeline = Pipelines(fake_client, "https://api.buildkite.com/v2/")
        pipeline.update_pipeline(
            "test_org",
            "test_pipeline",
            name="Name Change Test",
            env={"TEST_ENV_VAR": "VALUE"},
            configuration="",
            steps={}
        )
