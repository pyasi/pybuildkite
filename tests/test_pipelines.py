from unittest.mock import Mock

from pybuildkite.pipelines import Pipelines

import pytest


class TestPipelines:
    """
    Test functionality of the Pipelines class
    """

    @pytest.fixture
    def fake_client(self):
        """
        Build a fake API client
        """
        return Mock(get=Mock())

    def test_Pipelines(self, fake_client):
        """
        Test organization classes instances
        """
        pipeline = Pipelines(fake_client, "https://api.buildkite.com/v2/")
        assert pipeline.client == fake_client
        assert (
            pipeline.path == "https://api.buildkite.com/v2/organizations/{}/pipelines/"
        )

    def test_list_pipelines(self, fake_client):
        """
        Test organization class 'list_pipelines()'  Method
        """
        pipelines = Pipelines(fake_client, "https://api.buildkite.com/v2/")
        pipelines.list_pipelines("Test_org")
        fake_client.get.assert_called_with(pipelines.path.format("Test_org"))

    def test_get_pipeline(self, fake_client):
        """
        Test organization class 'get_pipeline()' method
        """
        pipeline = Pipelines(fake_client, "https://api.buildkite.com/v2/")
        pipeline.get_pipeline("Test_org", "Test_pipeline")
        fake_client.get.assert_called_with(
            pipeline.path.format("Test_org") + "Test_pipeline"
        )
