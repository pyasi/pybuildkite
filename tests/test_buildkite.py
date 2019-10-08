import pytest
from pybuildkite.buildkite import BuildKite, NoAcccessTokenException

class TestBuildkite:
    """
    Test functionality of the Buildkite class
    """

    def test_access_token_not_set_raises_exception(self):
        """
        Test that exception is raised if no access token is set
        """
        with pytest.raises(NoAcccessTokenException):
            buildkite = BuildKite()
            buildkite.agents()
    
    def test_access_token_set(self):
        """
        Test that methods can be called when access token is set
        """
        buildkite = BuildKite()
        buildkite.set_access_token('FAKE-ACCESS-TOKEN')
        assert buildkite.agents()
