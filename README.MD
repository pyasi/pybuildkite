## This is a WIP and not actually available yet

A [Python](https://www.python.org/) library and client for the [Buildkite API](https://buildkite.com/docs/api).

# Usage

To get the package, execute:

```
pip install pybuildkite
```

Simple shortened example for listing all pipelines is provided below, see examples for more.

```python
from pybuildkite.buildkite import BuildKite, BuildState

buildkite = BuildKite()
buildkite.set_access_token('YOUR_API_ACCESS_TOKEN_HERE')

# Get all info about particular org
buildkite.organizations().get_org('my-org')

# get all running builds for a particular pipeline
buildkite.builds().list_all_for_pipeline('my-org', 'my-pipeline', state=BuildState.RUNNING)
```

Note: This API currently only support READ ONLY functionality. It will soon include full CRUD operations.

# License

This library is distributed under the BSD-style license found in the LICENSE file.
