import requests


class Client(object):
    """
    Internal API Client
    """

    def __init__(self):
        """
        Create class
        """
        self.access_token = ""

    def is_access_token_set(self):
        """
        Has this client got an access token set in it

        :return: true or false
        """
        return not self.access_token == ""

    def set_client_access_token(self, access_token):
        """
        Set an access token to use for API calls
        :param access_token: The token
        """
        self.access_token = access_token

    def request(
        self,
        method,
        url,
        query_params=None,
        body=None,
        headers=None,
        with_pagination=False,
    ):
        """
        Make a request to the API

        The request will be authorised if the access token is set

        :param method: HTTP method to use
        :param url: URL to call
        :param query_params: Query parameters to use
        :param body: Body of the request
        :param headers: Dictionary of headers to use in HTTP request
        :param with_pagination: Bool to return a response with pagination attributes
        :return: If headers are set response text is returned, otherwise parsed response is returned
        """

        query_params = self._clean_query_params(query_params or {})

        if self.access_token:
            query_params["access_token"] = self.access_token

        if body:
            body = self._clean_query_params(body)

        query_params["per_page"] = "100"
        query_params = self._convert_query_params_to_string_for_bytes(query_params)
        response = requests.request(
            method, url, headers=headers, params=str.encode(query_params), json=body
        )

        response.raise_for_status()

        if with_pagination:
            response = self._get_paginated_response(response)
            return response
        if method == "DELETE":
            return response.ok
        else:
            return Response(response.json())

    def _get_paginated_response(self, response):
        """
        """
        response_object = Response(response.json())
        response_object.append_pagination_data(response.headers)
        return response_object

    def get(self, url, query_params=None, headers=None, with_pagination=False):
        """
        Make a GET request to the API

        The request will be authorised if the access token is set

        :param url: URL to call
        :param query_params: Query parameters to append to URL
        :param headers: Dictionary of headers to use in HTTP request
        :param with_pagination: Bool to return a response with pagination attributes
        :return: If headers are set response text is returned, otherwise parsed response is returned
        """
        return self.request(
            "GET",
            url=url,
            query_params=query_params,
            headers=headers,
            with_pagination=with_pagination,
        )

    def post(self, url, body=None, headers=None, query_params=None):
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

    def put(self, url, body=None, headers=None, query_params=None):
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

    def delete(self, url, body=None, headers=None, query_params=None):
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


class Response:
    def __init__(self, body):
        """
        """
        self.body = body
        self.next_page = None
        self.last_page = None
        self.first_page = None
        self.previous_page = None

    def append_pagination_data(self, response_headers):
        """
        """
        if "Link" in response_headers and len(response_headers["Link"]) > 0:
            for link in response_headers["Link"].split(", "):
                url, page_value = link.split("; ", 1)
                if page_value == 'rel="next"':
                    self.next_page = self._get_page_number_from_url(url)
                elif page_value == 'rel="last"':
                    self.last_page = self._get_page_number_from_url(url)
                elif page_value == 'rel="first"':
                    self.first_page = self._get_page_number_from_url(url)
                elif page_value == 'rel="prev"':
                    self.previous_page = self._get_page_number_from_url(url)
        return self

    def _get_page_number_from_url(self, url):
        """
        Gets the page number for pagination from a given url
        """
        for segment in url.split("&"):
            if "page" in segment and "api" not in segment:
                segment, number = segment.split("=", 1)
                return int(number)
        return 0
