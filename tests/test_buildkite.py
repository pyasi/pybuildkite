import pytest
from pybuildkite.buildkite import (
    Buildkite,
    Pipelines,
    Agents,
    Builds,
    Jobs,
    Emojis,
    Annotations,
    Artifacts,
    Teams,
    Users,
    Organizations,
    Meta,
)
from pybuildkite.exceptions import NoAcccessTokenException


def test_access_token_not_set_raises_exception():
    """
    Test that exception is raised if no access token is set
    """
    with pytest.raises(NoAcccessTokenException):
        buildkite = Buildkite()
        buildkite.agents()


def test_access_token_set():
    """
    Test that methods can be called when access token is set
    """
    buildkite = Buildkite()
    buildkite.set_access_token("FAKE-ACCESS-TOKEN")
    assert buildkite.agents()


@pytest.mark.parametrize(
    "function, expected_type",
    [
        (Buildkite().pipelines, Pipelines),
        (Buildkite().builds, Builds),
        (Buildkite().jobs, Jobs),
        (Buildkite().agents, Agents),
        (Buildkite().emojis, Emojis),
        (Buildkite().artifacts, Artifacts),
        (Buildkite().teams, Teams),
        (Buildkite().users, Users),
        (Buildkite().annotations, Annotations),
        (Buildkite().organizations, Organizations),
        (Buildkite().meta, Meta),
    ],
)
def test_eval(function, expected_type):
    # buildkite = Buildkite()
    # buildkite.set_access_token("FAKE-ACCESS-TOKEN")
    function.__self__.set_access_token("FAKE-ACCESS-TOKEN")
    pipelines = function()
    assert isinstance(pipelines, expected_type)
