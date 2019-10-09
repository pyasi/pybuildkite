import requests
import urllib


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

    def get(self, url, query_params=None, headers=None):
        """
        Make a GET request to the API

        The request will be authorised if the access token is set

        :param url: URL to call
        :param query_params: Query parameters to append to URL
        :param headers: Dictionary of headers to use in HTTP request
        :return: If headers are set response text is returned, otherwise parsed response is returned
        """
        url = self._create_url(url, query_params)
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        # TODO what should be returned
        if headers:
            return response.text
        else:
            return response.json()

    def post(self, url, body=None, headers=None):
        """
        Make a POST request to the API
        
        The request will be authorised if the access token is set

        :param url: URL to call
        :param body: Body of the request
        :param headers: Dictionary of headers to use in HTTP request
        :return: If headers are set response text is returned, otherwise parsed response is returned
        """
        url = self._create_url(url, body)
        body = self._clean_query_params(body)
        response = requests.post(url, json=body, headers=headers)
        response.raise_for_status()

        # TODO what should be returned
        if headers:
            return response.text
        else:
            return response.json()

    def _create_url(self, url, query_params):
        """

        :param url:
        :param query_params:
        :return:
        """
        if query_params is None:
            query_params = {}
        query_params = self._clean_query_params(query_params)
        query_params["access_token"] = self.access_token
        query_params = urllib.parse.urlencode(query_params)
        return url + "?" + query_params

    @staticmethod
    def _clean_query_params(query_params):
        """

        :param query_params:
        :return:
        """
        return {key: value for key, value in query_params.items() if value is not None}
