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
        client.set_client_access_token('FAKE-TOKEN')
        assert client.is_access_token_set()

    def test_clean_query_params(self):
        """
        Test that params with None are cleaned
        """
        original_query_params = {
            "name": 'FAKE-NAME',
            "hostname": 'FAKE-HOSTNAME',
            "version": None
        }

        cleaned_query_params = {
            "name": 'FAKE-NAME',
            "hostname": 'FAKE-HOSTNAME'
        }
        
        client = Client()
        original_query_params = client._clean_query_params(original_query_params)
        assert original_query_params == cleaned_query_params