from unittest.mock import Mock

import pytest

from pybuildkite.builds import Builds


def test_meta_data_url(fake_client):
    """
    Verifies if url is created properly when using meta_data
    """
    meta_data = {"key1": 1, "key2": "2"}
    builds = Builds(fake_client, "base")
    builds.list_all(meta_data=meta_data)

    name, args, kwargs = fake_client.method_calls[-1]
    _, query_params = args
    assert query_params["meta_data[key1]"] == 1
    assert query_params["meta_data[key2]"] == "2"


def test_no_meta_data_url(fake_client):
    """
    Verifies if url is created properly when using meta_data
    """
    builds = Builds(fake_client, "base")
    builds.list_all()

    name, args, kwargs = fake_client.method_calls[-1]
    _, query_params = args
    for key in query_params:
        assert "meta_data" not in key
