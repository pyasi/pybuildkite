import io

import requests
from requests.adapters import BaseAdapter
from requests.auth import AuthBase

from pybuildkite.buildkite import Buildkite


class RecordingTransport(BaseAdapter):
    def __init__(self):
        self.requests = []

    def send(self, request, **kwargs):
        self.requests.append(request)
        response = requests.Response()
        response.status_code = 200
        response.url = request.url
        response.request = request
        response.headers["Content-Type"] = "application/json"
        response.raw = io.BytesIO(b"{}")
        response._content = b"{}"
        return response

    def close(self):
        pass


class ChangingBearerAuth(AuthBase):
    def __init__(self):
        self.calls = 0

    def __call__(self, r):
        self.calls += 1
        r.headers["Authorization"] = "Bearer token-{}".format(self.calls)
        return r


def install_transport(monkeypatch, transport=None):
    if transport is None:
        transport = RecordingTransport()

    class TestSession(requests.Session):
        def __init__(self):
            super().__init__()
            self.trust_env = False
            self.mount("https://", transport)

    monkeypatch.setattr(requests.sessions, "Session", TestSession)
    return transport


def test_authentication_object_runs_for_each_request(monkeypatch):
    transport = install_transport(monkeypatch)
    auth = ChangingBearerAuth()
    buildkite = Buildkite(auth=auth)

    buildkite.builds().get_build_by_number("org", "pipeline", 1)
    buildkite.builds().get_build_by_number("org", "pipeline", 1)

    assert [request.headers["Authorization"] for request in transport.requests] == [
        "Bearer token-1",
        "Bearer token-2",
    ]
    assert (
        not buildkite.client.is_access_token_set()
    ), "custom auth must not change token inspection"


def test_explicit_access_token_takes_precedence(monkeypatch):
    transport = install_transport(monkeypatch)
    auth = ChangingBearerAuth()
    buildkite = Buildkite(auth=auth)
    buildkite.set_access_token("explicit-token")

    buildkite.builds().get_build_by_number("org", "pipeline", 1)
    assert auth.calls == 0

    buildkite.set_access_token("")
    buildkite.builds().get_build_by_number("org", "pipeline", 1)

    assert [request.headers["Authorization"] for request in transport.requests] == [
        "Bearer explicit-token",
        "Bearer token-1",
    ]


def test_artifact_redirect_does_not_reapply_authentication(monkeypatch):
    class ArtifactTransport(RecordingTransport):
        def send(self, request, **kwargs):
            response = super().send(request, **kwargs)
            if request.url.startswith("https://api.buildkite.com/"):
                response.status_code = 302
                response.headers[
                    "Location"
                ] = "https://downloads.example.invalid/artifact"
                response._content = b""
                response.raw = io.BytesIO(b"")
            else:
                response.headers["Content-Type"] = "application/octet-stream"
                response._content = b"artifact payload"
                response.raw = io.BytesIO(response._content)
            return response

    transport = install_transport(monkeypatch, ArtifactTransport())
    auth = ChangingBearerAuth()
    buildkite = Buildkite(auth=auth)

    stream = buildkite.artifacts().download_artifact(
        "org", "pipeline", 1, "job", "artifact", as_stream=True
    )

    assert b"".join(stream) == b"artifact payload"
    assert auth.calls == 1
    assert [request.headers.get("Authorization") for request in transport.requests] == [
        "Bearer token-1",
        None,
    ]
