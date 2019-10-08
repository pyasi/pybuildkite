import pytest
from pybuildkite.buildkite import BuildKite

class TestClient:
    """
    Test functionality of the cleint class
    """

    @staticmethod
    def setup_method():
        print('setup')
    @staticmethod
    def teardown_method():
        print('teardown')

    def test_access_token_not_set(self):
        """

        :return:
        """
        buildkite = BuildKite()
        buildkite.agents().get('FAKE-ORG')
