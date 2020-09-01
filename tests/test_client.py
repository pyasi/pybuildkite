from unittest.mock import patch

import pytest

from pybuildkite.client import Client, Response


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


class TestResponse:
    @pytest.mark.parametrize(
        "url,expected_output",
        [
            ("https://api.buildkite.com/v2/organization/builds?page=2&commit=SHA", 2),
            ("https://api.buildkite.com/v2/page/builds?page=5&commit=SHA", 5),
            ("https://api.buildkite.com/v2/page/builds?commit=SHA", 0),
        ],
    )
    def test_getting_page_from_url(self, url, expected_output):
        response = Response({"Body": "FakeBody"})
        output = response._get_page_number_from_url(url)
        assert output == expected_output

    def test_no_data_added_without_pagination_headers(self):
        response = Response({"Body": "FakeBody"})
        response_headers = ""
        response.append_pagination_data(response_headers)
        assert response.body == {"Body": "FakeBody"}
        assert response.first_page == None
        assert response.last_page == None
        assert response.previous_page == None
        assert response.next_page == None

    def test_pagination_headers_with_next_and_last(self):
        response = Response({"Body": "FakeBody"})
        response_headers = {
            "Date": "Wed, 20 Nov 2019 03:13:27 GMT",
            "Content-Type": "application/json; charset=utf-8",
            "Connection": "keep-alive",
            "Server": "nginx",
            "Link": '<https://api.buildkite.com/v2/builds?access_token=FakeToken&page=2&per_page=100>; rel="next", <https://api.buildkite.com/v2/builds?access_token=FakeToken&page=8&per_page=100>; rel="last"',
            "X-OAuth-Scopes": "read_agents",
        }
        response.append_pagination_data(response_headers)
        assert response.body == {"Body": "FakeBody"}
        assert response.first_page == None
        assert response.last_page == 8
        assert response.previous_page == None
        assert response.next_page == 2


class TestClientRequest:
    """
    Test the request-method of the client class
    """

    def test_request_should_not_include_token_when_not_set(self):
        """
        Test that the access token is not included in the call to
        requests if it isn't actually set.
        """
        fake_client = Client()

        with patch("requests.request") as request:
            request.return_value.json.return_value = {}

            fake_client.request("GET", "http://www.google.com/")

        request.assert_called_once_with(
            "GET",
            "http://www.google.com/",
            headers={},
            json=None,
            params=b"per_page=100",
            stream=False,
        )

    def test_request_should_return_bytes_when_non_json_accept_header_provided(self):
        """
        Test that the accept header is preserved and that bytes are returned
        """
        fake_client = Client()

        with patch("requests.request") as request:
            request.return_value.content = b"response text"

            resp = fake_client.request(
                "GET",
                "http://www.google.com/",
                headers={"Accept": "application/fake_encoding"},
            )

        expected_params = b"per_page=100"
        request.assert_called_once_with(
            "GET",
            "http://www.google.com/",
            headers={"Accept": "application/fake_encoding"},
            json=None,
            params=expected_params,
            stream=False,
        )

        assert resp == b"response text"

    def test_request_should_return_byte_stream_when_requested(self):
        """
        Test that the requests response.iter_content(None, False) is returned
        when stream is requested
        """
        fake_client = Client()

        with patch("requests.request") as request:
            request.return_value.iter_content.return_value = [
                b"response",
                b" ",
                b"text",
            ]

            resp = fake_client.request(
                "GET",
                "http://www.google.com/",
                headers={"Accept": "application/fake_encoding"},
                as_stream=True,
            )

        expected_params = b"per_page=100"
        request.assert_called_once_with(
            "GET",
            "http://www.google.com/",
            headers={"Accept": "application/fake_encoding"},
            json=None,
            params=expected_params,
            stream=True,
        )
        request.return_value.iter_content.assert_called_once_with(
            chunk_size=None, decode_unicode=False
        )

        assert resp == [b"response", b" ", b"text"]

    def test_request_should_return_json_when_json_accept_header_provided(self):
        """
        Test that the requests response.json() decoding is returned when
        no accept header is provided
        """
        fake_client = Client()

        with patch("requests.request") as request:
            request.return_value.json.return_value = {"key": "value"}

            resp = fake_client.request(
                "GET", "http://www.google.com/", headers={"Accept": "application/json"}
            )

        expected_params = b"per_page=100"
        request.assert_called_once_with(
            "GET",
            "http://www.google.com/",
            headers={"Accept": "application/json"},
            json=None,
            params=expected_params,
            stream=False,
        )

        assert resp == {"key": "value"}

    def test_request_should_return_json_when_no_accept_header_provided(self):
        """
        Test that the requests response.json() decoding is returned when
        no accept header is provided
        """
        fake_client = Client()

        with patch("requests.request") as request:
            request.return_value.json.return_value = {"key": "value"}

            resp = fake_client.request("GET", "http://www.google.com/")

        expected_params = b"per_page=100"
        request.assert_called_once_with(
            "GET",
            "http://www.google.com/",
            headers={},
            json=None,
            params=expected_params,
            stream=False,
        )

        assert resp == {"key": "value"}

    def test_request_should_include_token_when_set(self):
        """
        Test that the access token is not included in the call to
        requests if it isn't actually set.
        """
        fake_client = Client()
        fake_client.set_client_access_token("ABCDEF1234")

        with patch("requests.request") as request:
            request.return_value.json.return_value = {"key": "value"}

            resp = fake_client.request("GET", "http://www.google.com/")

        expected_params = b"per_page=100"
        request.assert_called_once_with(
            "GET",
            "http://www.google.com/",
            headers={"Authorization": "Bearer ABCDEF1234"},
            json=None,
            params=expected_params,
            stream=False,
        )

        assert resp == {"key": "value"}
