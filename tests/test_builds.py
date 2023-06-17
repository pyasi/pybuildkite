from unittest.mock import Mock

import pytest

import datetime

from pybuildkite.builds import Builds, BuildState
from pybuildkite.exceptions import (
    BuildStateNotAList,
    NotValidDateTime,
    NotValidBuildState,
)


def test_list_all_builds_single_build_state(fake_client):
    builds = Builds(fake_client, "https://api.buildkite.com/v2/")
    builds.list_all(states=[BuildState.RUNNING])
    fake_client.get.assert_called_with(
        builds.path_for_all,
        {
            "creator": None,
            "created_from": None,
            "created_to": None,
            "finished_from": None,
            "state": "state=running",
            "branch": None,
            "commit": None,
            "include_retried_jobs": None,
            "page": 0,
        },
        with_pagination=False,
    )


def test_list_all_builds_multiple_build_states(fake_client):
    builds = Builds(fake_client, "https://api.buildkite.com/v2/")
    builds.list_all(states=[BuildState.RUNNING, BuildState.FINISHED])
    fake_client.get.assert_called_with(
        builds.path_for_all,
        {
            "creator": None,
            "created_from": None,
            "created_to": None,
            "finished_from": None,
            "state": "state[]=running&state[]=finished",
            "branch": None,
            "commit": None,
            "include_retried_jobs": None,
            "page": 0,
        },
        with_pagination=False,
    )


def test_build_state_must_be_list(fake_client):
    builds = Builds(fake_client, "https://api.buildkite.com/v2/")
    with pytest.raises(BuildStateNotAList):
        builds.list_all(states=BuildState.RUNNING)


def test_build_state_must_be_valid(fake_client):
    builds = Builds(fake_client, "https://api.buildkite.com/v2/")
    with pytest.raises(NotValidBuildState):
        builds.list_all(states=["ran"])


def test_date_must_be_valid(fake_client):
    builds = Builds(fake_client, "https://api.buildkite.com/v2/")
    with pytest.raises(NotValidDateTime):
        builds.list_all(created_from="2017-02-03")


def test_correct_date_formats(fake_client):

    builds = Builds(fake_client, "https://api.buildkite.com/v2/")

    check_correct_dates(builds.list_all_for_org, fake_client, organization="org")
    check_correct_dates(builds.list_all, fake_client)
    check_correct_dates(
        builds.list_all_for_pipeline, fake_client, organization="org", pipeline="pipe"
    )


def check_correct_dates(func, fake_client, **kwargs):
    func(
        **kwargs,
        created_to=datetime.date(2020, 1, 2),
        created_from=datetime.datetime(2020, 1, 1, 10, 10, 10)
    )
    args = fake_client.get.call_args[0][1]
    assert args["created_from"] == "2020-01-01T10:10:10"
    assert args["created_to"] == "2020-01-02"
    assert args["finished_from"] == None


def test_list_all_builds_for_org(fake_client):
    builds = Builds(fake_client, "https://api.buildkite.com/v2/")
    builds.list_all_for_org("org_slug")
    fake_client.get.assert_called_with(
        builds.path_by_org.format("org_slug"),
        {
            "creator": None,
            "created_from": None,
            "created_to": None,
            "finished_from": None,
            "state": None,
            "branch": None,
            "commit": None,
            "include_retried_jobs": None,
            "page": 0,
        },
        with_pagination=False,
    )


def test_list_all_for_pipeline(fake_client):
    builds = Builds(fake_client, "https://api.buildkite.com/v2/")
    builds.list_all_for_pipeline("org_slug", "pipeline_id")
    fake_client.get.assert_called_with(
        builds.path_by_pipeline.format("org_slug", "pipeline_id"),
        {
            "creator": None,
            "created_from": None,
            "created_to": None,
            "finished_from": None,
            "state": None,
            "branch": None,
            "commit": None,
            "include_retried_jobs": None,
            "page": 0,
        },
        with_pagination=False,
    )


def test_get_build_by_number(fake_client):
    builds = Builds(fake_client, "https://api.buildkite.com/v2/")
    builds.get_build_by_number("org_slug", "pipeline_id", "build_number")
    fake_client.get.assert_called_with(
        builds.path_for_build_number.format("org_slug", "pipeline_id", "build_number"),
        query_params={"include_retried_jobs": None},
    )


def test_get_build_by_number_with_retried_jobs(fake_client):
    builds = Builds(fake_client, "https://api.buildkite.com/v2/")
    builds.get_build_by_number(
        "org_slug", "pipeline_id", "build_number", include_retried_jobs=True
    )
    fake_client.get.assert_called_with(
        builds.path_for_build_number.format("org_slug", "pipeline_id", "build_number"),
        query_params={"include_retried_jobs": True},
    )


def test_meta_data_url(fake_client):
    """
    Verifies if url is created properly when using meta_data
    """
    meta_data = {"key1": 1, "key2": "2"}
    builds = Builds(fake_client, "base")
    builds.list_all(meta_data=meta_data)
    name, args, kwargs = fake_client.method_calls[-1]
    _, query_params = args
    assert query_params["meta_data[key1]"] == 1
    assert query_params["meta_data[key2]"] == "2"


def test_no_meta_data_url(fake_client):
    """
    Verifies if url is created properly when using meta_data
    """
    builds = Builds(fake_client, "base")
    builds.list_all()

    name, args, kwargs = fake_client.method_calls[-1]
    _, query_params = args
    for key in query_params:
        assert "meta_data" not in key


def test_create_build(fake_client):
    builds = Builds(fake_client, "https://api.buildkite.com/v2/")
    builds.create_build("org_slug", "pipeline_id", "COMMITSHA", "branch_name")
    fake_client.post.assert_called_with(
        builds.path_by_pipeline.format("org_slug", "pipeline_id"),
        {
            "commit": "COMMITSHA",
            "branch": "branch_name",
            "author": None,
            "clean_checkout": None,
            "env": None,
            "ignore_pipeline_branch_filters": None,
            "message": None,
            "meta_data": None,
            "pull_request_base_branch": None,
            "pull_request_id": None,
            "pull_request_repository": None,
        },
    )


def test_cancel_build(fake_client):
    builds = Builds(fake_client, "https://api.buildkite.com/v2/")
    builds.cancel_build("org_slug", "pipeline_id", "build_number")
    fake_client.put.assert_called_with(
        builds.path_for_build_number.format("org_slug", "pipeline_id", "build_number")
        + "/cancel"
    )


def test_rebuild_build(fake_client):
    builds = Builds(fake_client, "https://api.buildkite.com/v2/")
    builds.rebuild_build("org_slug", "pipeline_id", "build_number")
    fake_client.put.assert_called_with(
        builds.path_for_build_number.format("org_slug", "pipeline_id", "build_number")
        + "/rebuild"
    )


def test_multi_branch(fake_client):
    builds = Builds(fake_client, "https://api.buildkite.com/v2/")
    builds.rebuild_build("org_slug", "pipeline_id", "build_number")

    builds.list_all_for_pipeline(
        organization="org", pipeline="pipe", branch=["main", "master"]
    )

    args = fake_client.get.call_args[0][1]
    assert args["branch"] == "branch[]=main&branch[]=master"


def test_single_branch(fake_client):
    builds = Builds(fake_client, "https://api.buildkite.com/v2/")
    builds.rebuild_build("org_slug", "pipeline_id", "build_number")

    builds.list_all_for_pipeline(organization="org", pipeline="pipe", branch="main")

    args = fake_client.get.call_args[0][1]
    assert args["branch"] == "branch=main"
