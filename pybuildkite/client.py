from __future__ import annotations

from typing import Any, Dict, Iterator, TypeAlias, TYPE_CHECKING

import requests

from pybuildkite.response import Response

if TYPE_CHECKING:
    _QueryParams: TypeAlias = requests.sessions._Params

_HeadersMapping: TypeAlias = Dict[str, Any]  # TODO: Bad Any.
RequestResponse: TypeAlias = Response | bool | Any | Iterator[Any] | bytes


class Client(object):
    """
    Internal API Client
    """

    def __init__(self) -> None:
        """
        Create class
        """
        self.access_token = ""

    def is_access_token_set(self) -> bool:
        """
        Has this client got an access token set in it

        :return: true or false
        """
        return not self.access_token == ""

    def set_client_access_token(self, access_token: str) -> None:
        """
        Set an access token to use for API calls
        :param access_token: The token
        """
        self.access_token = access_token

    def request(
        self,
        method: str | bytes,
        url: str | bytes,
        query_params: _QueryParams = None,
        body: Any | None = None,
        headers: _HeadersMapping = {},
        with_pagination: bool = False,
        as_stream: bool = False,
    ) -> RequestResponse:
        """
        Make a request to the API

        The request will be authorised if the access token is set.

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

        if self.access_token:
            headers["Authorization"] = "Bearer {}".format(self.access_token)

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
            paginated_response: Response = self._get_paginated_response(response)
            return paginated_response
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

    def _get_paginated_response(self, response: requests.Response) -> Response:
        """
        Return a Response object with pagination data

        :return: Response object
        """
        response_object = Response(response.json())
        response_object.append_pagination_data(response.headers)
        return response_object

    def get(
        self,
        url: str | bytes,
        query_params: _QueryParams = None,
        headers: _HeadersMapping = {},
        with_pagination: bool = False,
        as_stream: bool = False,
    ) -> RequestResponse:
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

    def post(
        self,
        url: str | bytes,
        body: Any = None,
        headers: _HeadersMapping = {},
        query_params: _QueryParams = None,
    ) -> RequestResponse:
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

    def put(
        self,
        url: str | bytes,
        body: Any = None,
        headers: _HeadersMapping = {},
        query_params: _QueryParams = None,
    ) -> RequestResponse:
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

    def delete(
        self,
        url: str | bytes,
        body: Any = None,
        headers: _HeadersMapping = {},
        query_params: _QueryParams = None,
    ) -> RequestResponse:
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

    def patch(
        self,
        url: str | bytes,
        body: Any = None,
        headers: _HeadersMapping = {},
        query_params: _QueryParams = None,
    ) -> Any:
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
    def _clean_query_params(
        query_params: Any,
    ) -> Dict:  # XXX: Bad Any and needs better Dict.
        """

        :param query_params:
        :return:
        """
        return {key: value for key, value in query_params.items() if value is not None}

    @staticmethod
    def _convert_query_params_to_string_for_bytes(query_params: Any) -> str:
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
