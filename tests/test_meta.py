from pybuildkite.meta import Meta


def test_get_meta_information(fake_client):
    """
    Test get user
    """
    meta = Meta(fake_client, "https://api.buildkite.com/v2/")
    meta.get_meta_information()
    fake_client.get.assert_called_with(meta.path)
