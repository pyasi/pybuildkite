import requests
import urllib


class Client(object):

    def __init__(self):
        """

        """
        self.access_token = ''

    def is_access_token_set(self):
        """

        :return:
        """
        return not self.access_token == ''

    def set_client_access_token(self, access_token):
        self.access_token = access_token

    def get(self, url, query_params=None, headers=None):

        url = self._create_url(url, query_params)
        response = requests.get(url, headers=headers)
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
