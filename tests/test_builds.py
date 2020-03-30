from unittest.mock import Mock

import pytest

from pybuildkite.builds import Builds


class TestBuilds:
    """
    Test functionality of the Builds class
    """

    @pytest.fixture
    def fake_client(self):
        """
        Build a fake API client
        """
        return Mock(get=Mock())

    def test_meta_data_url(self, fake_client):
        """
        Verifies if url is created properly when using meta_data
        """
        meta_data = {"key1": 1,
                     "key2": "2"}
        builds = Builds(fake_client, "base")
        builds.list_all(meta_data=meta_data)

        name, args, kwargs = fake_client.method_calls[-1]
        _, query_params = args
        assert query_params["meta_data[key1]"] == 1
        assert query_params["meta_data[key2]"] == "2"
