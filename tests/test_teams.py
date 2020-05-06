from pybuildkite.teams import Teams

import pytest


def test_teams(fake_client):
    """
    Test team initialization
    """
    teams = Teams(fake_client, "https://api.buildkite.com/v2/")
    assert teams.client == fake_client
    assert teams.path == "https://api.buildkite.com/v2/organizations/{}/teams"


def test_list_teams_with_no_user_id(fake_client):
    """
    Test get teams
    """
    teams = Teams(fake_client, "https://api.buildkite.com/v2/")
    teams.list_teams("test_org")
    fake_client.get.assert_called_with(
        teams.path.format("test_org"),
        query_params={"page": 0, "user_id": None},
        with_pagination=False,
    )


def test_list_teams_with_user_id(fake_client):
    """
    Test get teams
    """
    teams = Teams(fake_client, "https://api.buildkite.com/v2/")
    teams.list_teams(organization="test_org", user_id="test_user")
    fake_client.get.assert_called_with(
        teams.path.format("test_org", "test_user"),
        query_params={"page": 0, "user_id": "test_user"},
        with_pagination=False,
    )
