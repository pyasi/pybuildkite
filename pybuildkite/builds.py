import datetime
from enum import Enum
from pybuildkite.client import Client


class BuildState(Enum):
    """
    Valid build states

    The finished state is a shortcut to automatically search for builds with passed, failed, blocked, canceled states.
    """

    RUNNING = "running"
    SCHEDULED = "scheduled"
    PASSED = "passed"
    FAILED = "failed"
    BLOCKED = "blocked"
    CANCELED = "canceled"
    CANCELING = "canceling"
    SKIPPED = "skipped"
    NOT_RUN = "not_run"
    FINISHED = "finished"


# TODO needed?
class BuildQueryParams(Enum):
    """
    Query parameters for listing builds
    """

    CREATOR = "creator"
    CREATED_FROM = "created_from"
    CREATED_TO = "created_to"
    FINISHED_FROM = "finished_from"
    STATE = "state"
    META_DATA = "meta_data"
    BRANCH = "branch"
    COMMIT = "commit"


class Builds(Client):
    """
    Build operations for the Buildkite API
    """

    def __init__(self, client, base_url):
        """
        Construct the class

        :param client: API Client
        :param base_url: Base Url
        """
        self.client = client

        self.path_for_all = base_url + "builds"
        self.path_by_org = base_url + "organizations/{}/builds"
        self.path_by_pipeline = base_url + "organizations/{}/pipelines/{}/builds"
        self.path_for_build_number = base_url + "organizations/{}/pipelines/{}/builds/"

    def list_all(
        self,
        creator=None,
        created_from=None,
        created_to=None,
        finished_from=None,
        state=None,
        meta_data=None,
        branch=None,
        commit=None,
    ):
        """
        Returns a paginated list of all builds across all the user’s organizations and pipelines. If using
        token-based authentication the list of builds will be for the authorized organizations only. Builds are
        listed in the order they were created (newest first).

        :param creator: Filters the results by the user who created the build
        :param created_from: Filters the results by builds created on or after the given datetime.date
        :param created_to: Filters the results by builds created before the given datetime.date
        :param finished_from: Filters the results by builds finished on or after the given datetime.date
        :param state: Filters the results by the given build state.
        :param meta_data: Filters the results by the given meta_data. Example: ?meta_data[some-key]=some-value
        :param branch: Filters the results by the given branch or branches.
        :param commit: Filters the results by the commit (only works for full sha, not for shortened ones).
        :return: Returns a paginated list of all builds across all the user’s organizations and pipelines
        """
        self.__validate_dates([created_from, created_to, finished_from])
        self.__is_valid_state(state)

        query_params = {
            "creator": creator,
            "created_from": created_from,
            "created_to": created_to,
            "finished_from": finished_from,
            "state": state.value if state is not None else state,
            "meta_data": meta_data,
            "branch": branch,
            "commit": commit,
        }
        return self.client.get(self.path_for_all, query_params)

    def list_all_for_org(
        self,
        organization,
        creator=None,
        created_from=None,
        created_to=None,
        finished_from=None,
        state=None,
        meta_data=None,
        branch=None,
        commit=None,
    ):
        """
        Returns a paginated list of an organization’s builds across all of an organization’s pipelines. Builds are
        listed in the order they were created (newest first).

        :param organization: Organization slug
        :param creator: Filters the results by the user who created the build
        :param created_from: Filters the results by builds created on or after the given datetime.date
        :param created_to: Filters the results by builds created before the given datetime.date
        :param finished_from: Filters the results by builds finished on or after the given datetime.date
        :param state: Filters the results by the given build state.
        :param meta_data: Filters the results by the given meta_data.
        :param branch: Filters the results by the given branch or branches.
        :param commit: Filters the results by the commit (only works for full sha, not for shortened ones).
        :return: Returns a paginated list of an organization’s builds across all of an organization’s pipelines.
        """

        # TODO dry this?
        self.__validate_dates([created_from, created_to, finished_from])
        self.__is_valid_state(state)

        query_params = {
            "creator": creator,
            "created_from": created_from,
            "created_to": created_to,
            "finished_from": finished_from,
            "state": state.value if state is not None else state,
            "meta_data": meta_data,
            "branch": branch,
            "commit": commit,
        }
        return self.client.get(self.path_by_org.format(organization), query_params)

    def list_all_for_pipeline(
        self,
        organization,
        pipeline,
        creator=None,
        created_from=None,
        created_to=None,
        finished_from=None,
        state=None,
        meta_data=None,
        branch=None,
        commit=None,
    ):
        """
        Returns a paginated list of a pipeline’s builds. Builds are listed in the order they were created (newest
        first).

        :param organization: Organization slug
        :param pipeline: Pipeline slug
        :param creator: Filters the results by the user who created the build
        :param created_from: Filters the results by builds created on or after the given datetime.date
        :param created_to: Filters the results by builds created before the given datetime.date
        :param finished_from: Filters the results by builds finished on or after the given datetime.date
        :param state: Filters the results by the given build state.
        :param meta_data: Filters the results by the given meta_data.
        :param branch: Filters the results by the given branch or branches.
        :param commit: Filters the results by the commit (only works for full sha, not for shortened ones).
        :return: Returns a paginated list of a pipeline’s builds.
        """

        # TODO dry this?
        self.__validate_dates([created_from, created_to, finished_from])
        self.__is_valid_state(state)

        query_params = {
            "creator": creator,
            "created_from": created_from,
            "created_to": created_to,
            "finished_from": finished_from,
            "state": state.value if state is not None else state,
            "meta_data": meta_data,
            "branch": branch,
            "commit": commit,
        }
        return self.client.get(
            self.path_by_pipeline.format(organization, pipeline), query_params
        )

    def get_build_by_number(self, organization, pipeline, build_number):
        """

        :param organization: Organization slug
        :param pipeline: Pipeline slug
        :param build_number: Build number
        :return: A build
        """
        return self.client.get(
            self.path_for_build_number.format(organization, pipeline)
            + str(build_number)
        )

    def create_build(
        self,
        organization,
        pipeline,
        commit,
        branch,
        author=None,
        clean_checkout=None,
        env=None,
        ignore_pipeline_branch_filters=None,
        message=None,
        meta_data=None,
        pull_request_base_branch=None,
        pull_request_id=None,
        pull_request_repository=None,
    ):
        """
        Create a build

        :param organization: Organization slug
        :param pipeline: Pipeline slug
        :param commit: Commit to build
        :param branch: Branch to build
        :param author: Author of the build
        :param clean_checkout: Boolean to perform a clean checkout
        :param env: Any ENV variables for the build
        :param ignore_pipeline_branch_filters: Boolean to Ignore any branch filtering
        :param message: Message of the build
        :param meta_data: Meta Data for the build
        :param pull_request_base_branch: Base branch of a PR build
        :param pull_request_id: ID for a PR build
        :param pull_request_repository: Repository for a PR build
        :return: The created build
        """
        body = {
            "commit": commit,
            "branch": branch,
            "author": author,
            "clean_checkout": clean_checkout,
            "env": env,
            "ignore_pipeline_branch_filters": ignore_pipeline_branch_filters,
            "message": message,
            "meta_data": meta_data,
            "pull_request_base_branch": pull_request_base_branch,
            "pull_request_id": pull_request_id,
            "pull_request_repository": pull_request_repository,
        }
        return self.client.post(
            self.path_by_pipeline.format(organization, pipeline), body
        )

    @staticmethod
    def __validate_dates(datetimes):
        for date in datetimes:
            if date is not None:
                if not isinstance(date, datetime.date):
                    raise NotValidDateTime

    @staticmethod
    def __is_valid_state(state):
        if state is None:
            return
        if not isinstance(state, BuildState):
            raise NotValidBuildState


class NotValidDateTime(Exception):
    """
    Raised when date is not a valid datetime.date
    """

    pass


class NotValidBuildState(Exception):
    """
    Raised when state is not a valid BuildState
    """

    pass
