import pytest
from pybuildkite.agent import (
    Agent,
    Metrics,
)
from pybuildkite.exceptions import NoAgentTokenException


def test_access_token_not_set_raises_exception():
    """
    Test that exception is raised if no access token is set
    """
    with pytest.raises(NoAgentTokenException):
        buildkite = Agent()
        buildkite.metrics()


def test_access_token_set():
    """
    Test that methods can be called when access token is set
    """
    buildkite = Agent()
    buildkite.set_agent_token("FAKE-ACCESS-TOKEN")
    assert buildkite.metrics()


@pytest.mark.parametrize(
    "function_name, expected_type",
    [
        ("metrics", Metrics),
    ],
)
def test_eval(function_name, expected_type):
    buildkite = Agent()
    buildkite.set_agent_token("FAKE-ACCESS-TOKEN")
    pipelines = getattr(buildkite, function_name)()
    assert isinstance(pipelines, expected_type)
