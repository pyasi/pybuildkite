from pybuildkite.client import Client
from pybuildkite.organizations import Organizations
from requests.exceptions import HTTPError
import pytest

class TestOrganization:
    client = Client()
    url = 'https://api.buildkite.com/v2/'

    def test_organization(self):
        org = Organizations(self.client, self.url)
        assert org.client == self.client
        assert org.path == self.url + 'organizations/'

    def test_list_all(self):
        org = Organizations(self.client, self.url)
        with pytest.raises(HTTPError) as e:
            org.list_all()
        assert "HTTPError" in str(e)

    def test_get_org(self):
        org = Organizations(self.client, self.url)
        org_name = 'test'
        with pytest.raises(HTTPError) as e:
            org.get_org(org_name)
        assert "HTTPError" in str(e)