import pytest

from pybuildkite.emojis import Emojis


def test_list_emojis(fake_client):
    emojis = Emojis(fake_client, "https://api.buildkite.com/v2/")
    emojis.list_emojis("org_slug")
    fake_client.get.assert_called_with(
        emojis.path.format("org_slug"), query_params={"page": 0}, with_pagination=False
    )
