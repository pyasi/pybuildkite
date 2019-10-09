import pytest
from pybuildkite.organizations import Organizations
from pybuildkite.client import Client


@pytest.fixture()
def setup_org(mocker):
    mocker.patch('pybuildkite.client.Client.get', return_value='PASS')
    client = Client()
    url = 'https://api.buildkite.com/v2'
    org = Organizations(client, url)
    yield org

def test_organization(setup_org):
    assert setup_org.client == setup_org.client
    assert setup_org.path == 'https://api.buildkite.com/v2'+ 'organizations/'

def test_list_all(setup_org):
    result = setup_org.list_all()
    assert "PASS" in result

def test_get_org(setup_org):
    org_name = 'test'
    result = setup_org.get_org(org_name)
    assert "PASS" in result