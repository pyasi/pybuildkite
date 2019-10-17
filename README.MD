## This is a WIP and not actually available yet

A [Python](https://www.python.org/) library and client for the [Buildkite API](https://buildkite.com/docs/api).

# Usage

To get the package, execute:

```
pip install pybuildkite
```

Then set up an instance of the Buildkite object, set you access token, and make any available requests.

```python
from pybuildkite.buildkite import BuildKite, BuildState

buildkite = BuildKite()
buildkite.set_access_token('YOUR_API_ACCESS_TOKEN_HERE')

# Get all info about particular org
buildkite.organizations().get_org('my-org')

# Get all running builds for a particular pipeline
buildkite.builds().list_all_for_pipeline('my-org', 'my-pipeline', state=BuildState.RUNNING)

# Create a build
buildkite.builds().create_build('my-org', 'my-pipeline', 'COMMITSHA', 'master', clean_checkout=True, message="My First Build!")
```



# License

This library is distributed under the BSD-style license found in the LICENSE file.
