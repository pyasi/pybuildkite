import pytest

from pybuildkite.jobs import Jobs, LogFormat


def test_job_logs_can_be_requested_in_a_default_format(fake_client):
    """
    Test job logs can be requested in a default format
    """
    jobs = Jobs(fake_client, "base")
    jobs.get_job_log("org_slug", "pipe_slug", 123, "job_id")
    url = "base/organizations/org_slug/pipelines/pipe_slug/builds/123/jobs/job_id/log"
    fake_client.get.assert_called_with(url, headers={"Accept": "text/html"})


def test_job_logs_can_be_requested_in_a_user_specified_format(fake_client):
    """
    Test job logs can be requested in a user specified format
    """
    jobs = Jobs(fake_client, "base")
    jobs.get_job_log("org_slug", "pipe_slug", 123, "job_id", "some/thing")
    url = "base/organizations/org_slug/pipelines/pipe_slug/builds/123/jobs/job_id/log"
    fake_client.get.assert_called_with(url, headers={"Accept": "some/thing"})


def test_job_logs_can_be_requested_in_a_predefined_format(fake_client):
    """
    Test job logs can be requested in a predefined format
    """
    jobs = Jobs(fake_client, "base")
    jobs.get_job_log("org_slug", "pipe_slug", 123, "job_id", LogFormat.TEXT)
    url = "base/organizations/org_slug/pipelines/pipe_slug/builds/123/jobs/job_id/log"
    fake_client.get.assert_called_with(url, headers={"Accept": "text/plain"})


def test_log_format_can_be_nicely_printed_like_a_string():
    """
    Test that the log can be nicely formatted like a string
    """
    assert str(LogFormat.HTML) == "text/html"


def test_get_job_env(fake_client):
    jobs = Jobs(fake_client, "base")
    jobs.get_job_environment_variables("org_slug", "pipe_slug", 123, "job_id")
    fake_client.get.assert_called_with(
        jobs.path.format("org_slug", "pipe_slug", 123, "job_id") + "/env"
    )


def test_retry_job(fake_client):
    jobs = Jobs(fake_client, "base")
    jobs.retry_job("org_slug", "pipe_slug", 123, "job_id")
    fake_client.put.assert_called_with(
        jobs.path.format("org_slug", "pipe_slug", 123, "job_id") + "/retry"
    )


def test_unblock_job(fake_client):
    jobs = Jobs(fake_client, "base")
    jobs.unblock_job("org_slug", "pipe_slug", 123, "job_id", "name")
    fake_client.put.assert_called_with(
        jobs.path.format("org_slug", "pipe_slug", 123, "job_id") + "/unblock",
        body={"fields": "name", "unblocker": None},
    )


def test_delete_job_log(fake_client):
    jobs = Jobs(fake_client, "base")
    jobs.delete_job_log("org_slug", "pipe_slug", 123, "job_id")
    fake_client.delete.assert_called_with(
        jobs.path.format("org_slug", "pipe_slug", 123, "job_id") + "/log"
    )
