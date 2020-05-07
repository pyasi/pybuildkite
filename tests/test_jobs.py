import pytest

from pybuildkite.jobs import Jobs, LogFormat


def test_job_logs_can_be_requested_in_a_default_format(fake_client):
    """
    Test job logs can be requested in a default format
    """
    jobs = Jobs(fake_client, "base")
    jobs.get_job_log("org_slug", "pipe_slug", "build_no", 123)
    url = "base/organizations/org_slug/pipelines/pipe_slug/builds/build_no/jobs/123/log"
    fake_client.get.assert_called_with(url, headers={"Accept": "text/html"})


def test_job_logs_can_be_requested_in_a_user_specified_format(fake_client):
    """
    Test job logs can be requested in a user specified format
    """
    jobs = Jobs(fake_client, "base")
    jobs.get_job_log("org_slug", "pipe_slug", "build_no", 123, "some/thing")
    url = "base/organizations/org_slug/pipelines/pipe_slug/builds/build_no/jobs/123/log"
    fake_client.get.assert_called_with(url, headers={"Accept": "some/thing"})


def test_job_logs_can_be_requested_in_a_predefined_format(fake_client):
    """
    Test job logs can be requested in a predefined format
    """
    jobs = Jobs(fake_client, "base")
    jobs.get_job_log("org_slug", "pipe_slug", "build_no", 123, LogFormat.TEXT)
    url = "base/organizations/org_slug/pipelines/pipe_slug/builds/build_no/jobs/123/log"
    fake_client.get.assert_called_with(url, headers={"Accept": "text/plain"})


def test_log_format_can_be_nicely_printed_like_a_string():
    """
    Test that the log can be nicely formatted like a string
    """
    assert str(LogFormat.HTML) == "text/html"
