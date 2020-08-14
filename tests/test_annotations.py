import pytest

from pybuildkite.annotations import Annotations


def test_list_annotations(fake_client):
    annotations = Annotations(fake_client, "https://api.buildkite.com/v2/")
    annotations.list_annotations("org_slug", "pipeline_id", "build_number")
    fake_client.get.assert_called_with(
        annotations.path.format("org_slug", "pipeline_id", "build_number"),
        query_params={"page": 0},
        with_pagination=False,
    )
