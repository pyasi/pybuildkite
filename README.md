# PyBuildkite

[![Build status](https://badge.buildkite.com/89bf10df4492f2f2d61ca707078828824fec3b08cb85192e6d.svg)](https://buildkite.com/pybuildkite/pybuildkite)
[![Coverage Status](https://coveralls.io/repos/github/pyasi/pybuildkite/badge.svg?branch=master)](https://coveralls.io/github/pyasi/pybuildkite?branch=master)
[![PyPI most recent version](https://badge.fury.io/py/pybuildkite.svg)](https://pypi.org/project/pybuildkite/)
[![PyPI downloads](https://img.shields.io/pypi/dm/pybuildkite.svg)](https://pypi.org/project/pybuildkite/)

A [Python](https://www.python.org/) library and client for the [Buildkite API](https://buildkite.com/docs/api).

## Usage

To get the package, execute:

```
pip install pybuildkite
```

Then set up an instance of the Buildkite object, set you access token, and make any available requests.

```python
from pybuildkite.buildkite import Buildkite, BuildState

buildkite = Buildkite()
buildkite.set_access_token('YOUR_API_ACCESS_TOKEN_HERE')

# Get all info about particular org
org = buildkite.organizations().get_org('my-org')

# Get all running and scheduled builds for a particular pipeline
builds = buildkite.builds().list_all_for_pipeline('my-org', 'my-pipeline', states=[BuildState.RUNNING, BuildState.SCHEDULED])

# Create a build
buildkite.builds().create_build('my-org', 'my-pipeline', 'COMMITSHA', 'master', 
clean_checkout=True, message="My First Build!")
```

## Pagination

Buildkite offers pagination for endpoints that return a lot of data. By default this wrapper return `100` objects. However, any request that may contain more than that offers a pagination option.

When `with_pagination=True`, we return a response object with properties that may have `next_page`, `last_page`, `previous_page`, or `first_page` depending on what page you're on.

```python
builds_response = buildkite.builds().list_all(page=1, with_pagination=True)

# Keep looping until next_page is not populated
while builds_response.next_page:
    builds_response = buildkite.builds().list_all(page=builds_response.next_page, with_pagination=True)
```

## Artifacts

Artifacts can be downloaded as binary data. The following example loads the artifact into memory as
[Python bytes](https://docs.python.org/3/library/stdtypes.html#binary-sequence-types-bytes-bytearray-memoryview)
and then writes them to disc:

```python
artifacts = buildkite.artifacts()
artifact = artifacts.download_artifact("org_slug", "pipe_slug", "build_no", 123, "artifact")
with open('artifact.bin', 'b') as f:
  f.write(artifact)
```

Large artifacts should be streamed as chunks of bytes to limit the memory consumption:
```python
stream = artifacts.download_artifact("org_slug", "pipe_slug", "build_no", 123, "artifact", as_stream=True)
with open('artifact.bin', 'b') as f:
  for chunk in stream:
    f.write(chunk)
```

A unicode text artifact can be turned into a string easily:
```python
text = str(artifact)
```

## License

This library is distributed under the BSD-style license found in the LICENSE file.
