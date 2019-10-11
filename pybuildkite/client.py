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

    def request(self, method, url, query_params=None, body=None, headers=None):
        """
        Make a request to the API

        The request will be authorised if the access token is set

        :param method: HTTP method to use
        :param url: URL to call
        :param query_params: Query parameters to use
        :param body: Body of the request
        :param headers: Dictionary of headers to use in HTTP request
        :return: If headers are set response text is returned, otherwise parsed response is returned
        """

        query_params = self._clean_query_params(query_params or {})

        if self.access_token:
            query_params["access_token"] = self.access_token

        if body:
            body = self._clean_query_params(body)

        response = requests.request(method, url, headers=headers, params=query_params, json=body)
        response.raise_for_status()

        # TODO what should be returned
        if headers:
            return response.text

        return response.json()

    def get(self, url, query_params=None, headers=None):
        """
        Make a GET request to the API

        The request will be authorised if the access token is set

        :param url: URL to call
        :param query_params: Query parameters to append to URL
        :param headers: Dictionary of headers to use in HTTP request
        :return: If headers are set response text is returned, otherwise parsed response is returned
        """

        return self.request("GET", url=url, query_params=query_params, headers=headers)

    def post(self, url, body=None, headers=None, query_params=None):
        """
        Make a POST request to the API

        The request will be authorised if the access token is set

        :param url: URL to call
        :param body: Body of the request
        :param headers: Dictionary of headers to use in HTTP request
        :return: If headers are set response text is returned, otherwise parsed response is returned
        """

        return self.request("POST", url=url, query_params=query_params, body=body, headers=headers)

    def put(self, url, body=None, headers=None, query_params=None):
        """
        Make a PUT request to the API

        The request will be authorised if the access token is set

        :param url: URL to call
        :param body: Body of the request
        :param headers: Dictionary of headers to use in HTTP request
        :return: If headers are set response text is returned, otherwise parsed response is returned
        """

        return self.request("PUT", url=url, query_params=query_params, body=body, headers=headers)

    @staticmethod
    def _clean_query_params(query_params):
        """

        :param query_params:
        :return:
        """
        return {key: value for key, value in query_params.items() if value is not None}
