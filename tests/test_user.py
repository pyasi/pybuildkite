from pybuildkite.users import Users

import pytest


def test_get_current_user(fake_client):
    """
    Test get user
    """
    users = Users(fake_client, "https://api.buildkite.com/v2/")
    users.get_current_user()
    fake_client.get.assert_called_with(users.path)
