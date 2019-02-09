import requests


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

    def get(self, url):
        response = requests.get(url + "?access_token={}".format(self.access_token))
        response.raise_for_status()

        return response.text

