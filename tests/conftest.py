import pytest
from unittest.mock import Mock


@pytest.fixture
def fake_client() -> Mock:
    """
    Build a fake API client
    """
    return Mock(get=Mock())
