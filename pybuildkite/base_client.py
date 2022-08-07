import abc

import requests
from urllib.parse import urlparse

from pybuildkite.constants import APIVersion
from pybuildkite.response import Response


class BaseClient(abc.ABC):
    """
    Base Internal API Client
    """

    def __init__(self, api_version: APIVersion) -> None:
        """
        Create class
        """
        self._token = ""
        self._api_version = api_version

    @abc.abstractmethod
    def _get_authorization_header(self) -> str:
        raise NotImplementedError

    @property
    def token(self) -> str:
        return self._token

    @token.setter
    def token(self, token: str) -> None:
        self._token = token

    @property
    def api_version(self) -> APIVersion:
        return self._api_version

    @api_version.setter
    def api_version(self, api_version: APIVersion) -> None:
        self._api_version = api_version

    def _is_token_set(self) -> bool:
        return not self._token == ""

    def request(
        self,
        method,
        url,
        query_params=None,
        body=None,
        headers={},
        with_pagination=False,
        as_stream=False,
    ):
        """
        Make a request to the API

        The request will be authorised if a token is set

        With no accept header set or if set to "application/json",
        the response will be parsed as Json and returned as a dict.
        With any other accept header, the response will be returned as bytes.
        With as_stream=True you will get an iterator of bytes chunks instead.

        :param method: HTTP method to use
        :param url: URL to call
        :param query_params: Query parameters to use
        :param body: Body of the request
        :param headers: Dictionary of headers to use in HTTP request
        :param with_pagination: Bool to return a response with pagination attributes
        :param as_stream: Bool to stream the bytes response
        :return: response return as parsed json, bytes or bytes chunks iterator
        """
        if headers is None:
            raise ValueError("headers cannot be None")

        if self._token:
            headers["Authorization"] = self._get_authorization_header()

        if body:
            body = self._clean_query_params(body)

        query_params = self._clean_query_params(query_params or {})
        query_params["per_page"] = "100"

        query_params = self._convert_query_params_to_string_for_bytes(query_params)
        response = requests.request(
            method,
            url,
            headers=headers,
            params=str.encode(query_params),
            json=body,
            stream=as_stream,
        )

        response.raise_for_status()

        if with_pagination:
            response = self._get_paginated_response(response)
            return response
        if (
            method == "DELETE"
            or response.status_code == 204
            or response.headers.get("content-type") is None
        ):
            return response.ok
        if headers.get("Accept") is None or headers.get("Accept") == "application/json":
            return response.json()
        elif as_stream:
            return response.iter_content(chunk_size=None, decode_unicode=False)
        else:
            return response.content

    def _get_paginated_response(self, response):
        """
        Return a Response object with pagination data

        :return: Response object
        """
        response_object = Response(response.json())
        response_object.append_pagination_data(response.headers)
        return response_object

    def get(
        self, url, query_params=None, headers={}, with_pagination=False, as_stream=False
    ):
        """
        Make a GET request to the API

        The request will be authorised if the access token is set

        :param url: URL to call
        :param query_params: Query parameters to append to URL
        :param headers: Dictionary of headers to use in HTTP request
        :param with_pagination: Bool to return a response with pagination attributes
        :param as_stream: Bool to stream the response
        :return: If headers are set response text is returned, otherwise parsed response is returned
        """
        return self.request(
            "GET",
            url=url,
            query_params=query_params,
            headers=headers,
            with_pagination=with_pagination,
            as_stream=as_stream,
        )

    def post(self, url, body=None, headers={}, query_params=None):
        """
        Make a POST request to the API

        The request will be authorised if the access token is set

        :param url: URL to call
        :param body: Body of the request
        :param query_params: Query parameters to append to URL
        :param headers: Dictionary of headers to use in HTTP request
        :return: If headers are set response text is returned, otherwise parsed response is returned
        """

        return self.request(
            "POST", url=url, query_params=query_params, body=body, headers=headers
        )

    def put(self, url, body=None, headers={}, query_params=None):
        """
        Make a PUT request to the API

        The request will be authorised if the access token is set

        :param url: URL to call
        :param body: Body of the request
        :param headers: Dictionary of headers to use in HTTP request
        :param query_params: Query parameters to append to URL
        :return: If headers are set response text is returned, otherwise parsed response is returned
        """

        return self.request(
            "PUT", url=url, query_params=query_params, body=body, headers=headers
        )

    def delete(self, url, body=None, headers={}, query_params=None):
        """
        Make a DELETE request to the API

        The request will be authorised if the access token is set

        :param url: URL to call
        :param body: Body of the request
        :param query_params: Query parameters to append to URL
        :param headers: Dictionary of headers to use in HTTP request
        :return: If headers are set response text is returned, otherwise parsed response is returned
        """

        return self.request(
            "DELETE", url=url, query_params=query_params, body=body, headers=headers
        )

    def patch(self, url, body=None, headers={}, query_params=None):
        """
        Make a PATCH request to the API

        The request will be authorised if the access token is set

        :param url: URL to call
        :param body: Body of the request
        :param query_params: Query parameters to append to URL
        :param headers: Dictionary of headers to use in HTTP request
        :return: If headers are set response text is returned, otherwise parsed response is returned
        """
        return self.request(
            "PATCH", url=url, query_params=query_params, body=body, headers=headers
        )

    @staticmethod
    def _clean_query_params(query_params):
        """

        :param query_params:
        :return:
        """
        return {key: value for key, value in query_params.items() if value is not None}

    @staticmethod
    def _convert_query_params_to_string_for_bytes(query_params):
        """
        Required to set multiple build states i.e ?state[]=running&state[]=scheduled

        :param query_params: query parameters
        :return: bytes of query param
        """
        query_string = ""
        for key, value in query_params.items():
            if query_string != "":
                query_string += "&"
            if key == "state":
                query_string += value
            else:
                query_string += key + "=" + str(value)
        return query_string
