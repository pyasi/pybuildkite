import pytest

from pybuildkite.agents import Agents


def test_get_agent(fake_client):
    """
    Test the get_agent method
    """
    agents = Agents(fake_client, "base")
    agents.get_agent("org_slug", "agent_id")
    url = "base/organizations/org_slug/agents/agent_id"
    fake_client.get.assert_called_with(url)
