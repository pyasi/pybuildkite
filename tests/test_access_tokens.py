import pytest
from pybuildkite.access_tokens import AccessTokens


def test_get_access_token(fake_client):
    """
    Test Get Access Token
    """
    artifacts = AccessTokens(fake_client, "base")
    artifacts.get_token()
    url = "base/access-token"
    fake_client.get.assert_called_with(url)


def test_revoke_access_token(fake_client):
    """
    Test Get Access Token
    """
    artifacts = AccessTokens(fake_client, "base")
    artifacts.revoke_token()
    url = "base/access-token"
    fake_client.delete.assert_called_with(url)
