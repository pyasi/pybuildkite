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

    def get(self, url, query_params=None):

        url = self.__create_url(url, query_params)
        response = requests.get(url)
        response.raise_for_status()

        return response.text

    def __create_url(self, url, query_params):
        """

        :param url:
        :param query_params:
        :return:
        """
        query_params["access_token"] = self.access_token
        query_params = urllib.parse.urlencode(query_params)
        return url + "?" + query_params
