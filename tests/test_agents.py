import pytest

from pybuildkite.agents import Agents


def test_get_agent(fake_client):
    """
    Test the get_agent method
    """
    agents = Agents(fake_client, "base")
    agents.get_agent("org_slug", "agent_id")
    fake_client.get.assert_called_with(agents.path.format("org_slug") + "agent_id")


def test_stop_agent(fake_client):
    agents = Agents(fake_client, "base")
    agents.stop_agent("org_slug", "agent_id")
    fake_client.put.assert_called_with(
        agents.path.format("org_slug") + "agent_id/stop", body={"force": True}
    )


def test_list_all_agents(fake_client):
    agents = Agents(fake_client, "base")
    agents.list_all("org_slug")
    fake_client.get.assert_called_with(
        agents.path.format("org_slug"),
        {"name": None, "hostname": None, "version": None, "page": 0},
        with_pagination=False,
    )
