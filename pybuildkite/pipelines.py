from pybuildkite.client import Client


class Pipelines(Client):
    """
    Pipeline operations for the Buildkite API
    """

    def __init__(self, client, base_url):
        """
        Construct the class

        :param client:
        :param base_url:
        """
        self.client = client
        self.path = base_url + "organizations/{}/pipelines/"

    def list_pipelines(self, organization, page=0, with_pagination=False):
        """
        Returns a paginated list of an organization’s pipelines.

        :param organization: Organization slug
        :param page: Int to determine which page to read from (See Pagination in README)
        :param with_pagination: Bool to return a response with pagination attributes
        :return: Returns a paginated list of an organization’s pipelines.
        """
        query_params = {"page": page}
        return self.client.get(
            self.path.format(organization),
            query_params=query_params,
            with_pagination=with_pagination,
        )

    def get_pipeline(self, organization, pipeline_name):
        """
        Get a pipeline

        :param organization: Organization slug
        :param pipeline_name: Pipeline slug
        :return: A pipeline
        """
        return self.client.get(self.path.format(organization) + pipeline_name)

    def create_pipeline(
        self,
        organization,
        pipeline_name,
        git_repository,
        build_steps=[
            dict(
                type="script",
                name=":pipeline:",
                command="buildkite-agent pipeline upload",
            )
        ],
    ):
        """
        Create a pipeline for organizations using Web Visual Steps. 
        See `create_yaml_pipeline` if you've migrated to YAML pipelines.
        :param build_steps: list of build pipeline steps
        Command: { "type": "script", "name": "Script", "command": "command.sh" }
        Wait for all previous steps to finish: { "type": "waiter" }
        Block pipeline (see the job unblock API): { "type": "manual" }
        Trigger pipeline: { "type": "trigger", "trigger_project_slug": "a-pipeline" }
        :param organization: Organization slug
        :param pipeline_name:Pipeline slug
        :param git_repository: repo URL
        :return:
        """
        data = {
            "name": pipeline_name,
            "repository": git_repository,
            "steps": build_steps,
        }

        return self.client.post(self.path.format(organization), body=data)

    def create_yaml_pipeline(
        self,
        organization,
        pipeline_name,
        git_repository,
        configuration
    ):
        """
        Create a pipeline for organizations who have migrated to YAML pipelines
        https://buildkite.com/changelog/99-introducing-the-yaml-steps-editor
        :param organization: Organization slug
        :param pipeline_name:Pipeline slug
        :param git_repository: repo URL
        :param configuration: a valid pipeline.yml
        :return:
        """
        data = {
            "name": pipeline_name,
            "repository": git_repository,
            "configuration": configuration,
        }
        return self.client.post(self.path.format(organization), body=data)

    def delete_pipeline(self, organization, pipeline):
        """
        Delete a pipeline
        :param organization: Organization slug
        :param pipeline:Pipeline slug
        :return:
        """
        url = self.path.format(organization) + pipeline
        return self.client.delete(url)

    def update_pipeline(
        self,
        organization,
        pipeline,
        branch_configuration: str = None,
        cancel_running_branch_builds: bool = None,
        cancel_running_branch_builds_filter: str = None,
        default_branch: str = None,
        description: str = None,
        env: dict = None,
        name: str = None,
        provider_settings: dict = None,
        repository: str = None,
        configuration: str = None,
        steps: dict = None,
        skip_queued_branch_builds: bool = None,
        skip_queued_branch_builds_filter: str = None,
        visibility: str = None,
    ):
        """
        Patch a pipeline.
        See https://buildkite.com/docs/apis/rest-api/pipelines#update-a-pipeline
        for documentation on each input

        :param organization: Organization slug
        :param pipeline: Pipeline slug
        :return: Pipeline
        """
        if configuration is not None and steps is not None:
            raise PipelineException("Cannot set both `configuration` and `steps`. If you've migrated to YAML steps, please use `configuration`. Otherwise, use `steps`")

        body = {
            "branch_configuration": branch_configuration,
            "cancel_running_branch_builds": cancel_running_branch_builds,
            "cancel_running_branch_builds_filter": cancel_running_branch_builds_filter,
            "default_branch": default_branch,
            "description": description,
            "env": env,
            "name": name,
            "provider_settings": provider_settings,
            "repository": repository,
            "configuration": configuration,
            "steps": steps,
            "skip_queued_branch_builds": skip_queued_branch_builds,
            "skip_queued_branch_builds_filter": skip_queued_branch_builds_filter,
            "visibility": visibility,
        }
        url = self.path.format(organization) + pipeline
        return self.client.patch(url, body=body)


class PipelineException(Exception):
    pass