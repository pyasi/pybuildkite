from unittest.mock import Mock

import pytest

from pybuildkite.agents import Agents


class TestAgents:
    """
    Test functionality of the Agents class
    """

    @pytest.fixture
    def fake_client(self):
        """
        Build a fake API client
        """
        return Mock(get=Mock())

    def test_get_agent(self, fake_client):
        """
        Test the get_agent method
        """
        agents = Agents(fake_client, "base")
        agents.get_agent("org_slug", "agent_id")
        url = "base/organizations/org_slug/agents/agent_id"
        fake_client.get.assert_called_with(url)
