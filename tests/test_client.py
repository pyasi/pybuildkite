from unittest.mock import patch

import pytest

from pybuildkite.client import Client


class TestClient:
    """
    Test functionality of the client class
    """

    def test_access_token_setting(self):
        """
        Test functionality of is_acces_token_set
        """
        client = Client()
        assert not client.is_access_token_set()
        client.set_client_access_token("FAKE-TOKEN")
        assert client.is_access_token_set()

    def test_clean_query_params(self):
        """
        Test that params with None are cleaned
        """
        original_query_params = {
            "name": "FAKE-NAME",
            "hostname": "FAKE-HOSTNAME",
            "version": None,
        }

        cleaned_query_params = {"name": "FAKE-NAME", "hostname": "FAKE-HOSTNAME"}

        client = Client()
        original_query_params = client._clean_query_params(original_query_params)
        assert original_query_params == cleaned_query_params


class TestClientRequest:
    """
    Test the request-method of the client class
    """

    def test_request_should_not_include_token(self):
        """
        Test that the access token is not included in the call to
        requests if it isn't actually set.
        """
        client = Client()

        with patch("requests.request") as request:
            request.return_value.json.return_value = {}

            client.request("GET", "http://www.google.com/")

        request.assert_called_once_with(
            "GET", "http://www.google.com/", headers=None, json=None, params={}
        )

    def test_request_should_include_token_when_set(self):
        """
        Test that the access token is not included in the call to
        requests if it isn't actually set.
        """
        client = Client()
        client.set_client_access_token("ABCDEF1234")

        with patch("requests.request") as request:
            request.return_value.json.return_value = {}

            client.request("GET", "http://www.google.com/")

        expected_params = {"access_token": "ABCDEF1234"}
        request.assert_called_once_with(
            "GET",
            "http://www.google.com/",
            headers=None,
            json=None,
            params=expected_params,
        )
