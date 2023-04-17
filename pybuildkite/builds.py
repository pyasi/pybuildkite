import datetime
from enum import Enum
from typing import List

from pybuildkite.client import Client
from pybuildkite.exceptions import (
    NotValidBuildState,
    NotValidDateTime,
    BuildStateNotAList,
)


class BuildState(Enum):
    """
    Valid build states

    The finished state is a shortcut to automatically search for builds with passed, failed, blocked, canceled states.
    """

    RUNNING = "running"
    SCHEDULED = "scheduled"
    PASSED = "passed"
    FAILING = "failing"
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
        self.path_for_build_number = (
            base_url + "organizations/{}/pipelines/{}/builds/{}"
        )

    def list_all(
        self,
        creator=None,
        created_from=None,
        created_to=None,
        finished_from=None,
        states=[],
        meta_data=None,
        branch=None,
        commit=None,
        include_retried_jobs=None,
        page=0,
        with_pagination=False,
    ):
        """
        Returns a paginated list of all builds across all the user’s organizations and pipelines. If using
        token-based authentication the list of builds will be for the authorized organizations only. Builds are
        listed in the order they were created (newest first).

        :param creator: Filters the results by the user who created the build
        :param created_from: Filters the results by builds created on or after the given datetime.date
        :param created_to: Filters the results by builds created before the given datetime.date
        :param finished_from: Filters the results by builds finished on or after the given datetime.date
        :param states: Filters the results by build states [List]
        :param meta_data: Filters the results by the given meta_data. Example: ?meta_data[some-key]=some-value
        :param branch: Filters the results by the given branch or branches.
        :param commit: Filters the results by the commit (only works for full sha, not for shortened ones).
        :param include_retried_jobs: Include all retried job executions in each build’s jobs list if True.
               Without this parameter, you'll see only the most recently run job for each step.
        :param page: Int to determine which page to read from (See Pagination in README)
        :param with_pagination: Bool to return a response with pagination attributes
        :return: Returns a paginated list of all builds across all the user’s organizations and pipelines
        """
        self.__validate_dates([created_from, created_to, finished_from])
        self.__are_valid_states(states)

        query_params = {
            "creator": creator,
            "created_from": self.__api_date_format(created_from),
            "created_to": self.__api_date_format(created_to),
            "finished_from": self.__api_date_format(finished_from),
            "state": self.__get_build_states_query_param(states),
            "branch": self.__get_branches_query_param(branch),
            "commit": commit,
            "include_retried_jobs": True if include_retried_jobs is True else None,
            "page": page,
        }
        query_params.update(self.__process_meta_data(meta_data))

        return self.client.get(
            self.path_for_all, query_params, with_pagination=with_pagination
        )

    def list_all_for_org(
        self,
        organization,
        creator=None,
        created_from=None,
        created_to=None,
        finished_from=None,
        states=[],
        meta_data=None,
        branch=None,
        commit=None,
        include_retried_jobs=None,
        page=0,
        with_pagination=False,
    ):
        """
        Returns a paginated list of an organization’s builds across all of an organization’s pipelines. Builds are
        listed in the order they were created (newest first).

        :param organization: Organization slug
        :param creator: Filters the results by the user who created the build
        :param created_from: Filters the results by builds created on or after the given datetime.date
        :param created_to: Filters the results by builds created before the given datetime.date
        :param finished_from: Filters the results by builds finished on or after the given datetime.date
        :param states: Filters the results by build states [List]
        :param meta_data: Filters the results by the given meta_data.
        :param branch: Filters the results by the given branch or branches.
        :param commit: Filters the results by the commit (only works for full sha, not for shortened ones).
        :param include_retried_jobs: Include all retried job executions in each build’s jobs list if True.
               Without this parameter, you'll see only the most recently run job for each step.
        :param page: Int to determine which page to read from (See Pagination in README)
        :param with_pagination: Bool to return a response with pagination attributes
        :return: Returns a paginated list of an organization’s builds across all of an organization’s pipelines.
        """

        self.__validate_dates([created_from, created_to, finished_from])
        self.__are_valid_states(states)

        query_params = {
            "creator": creator,
            "created_from": self.__api_date_format(created_from),
            "created_to": self.__api_date_format(created_to),
            "finished_from": self.__api_date_format(finished_from),
            "state": self.__get_build_states_query_param(states),
            "branch": self.__get_branches_query_param(branch),
            "commit": commit,
            "include_retried_jobs": True if include_retried_jobs is True else None,
            "page": page,
        }
        query_params.update(self.__process_meta_data(meta_data))

        return self.client.get(
            self.path_by_org.format(organization),
            query_params,
            with_pagination=with_pagination,
        )

    def list_all_for_pipeline(
        self,
        organization,
        pipeline,
        creator=None,
        created_from=None,
        created_to=None,
        finished_from=None,
        states=[],
        meta_data=None,
        branch=None,
        commit=None,
        include_retried_jobs=None,
        page=0,
        with_pagination=False,
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
        :param states: Filters the results by build states [List]
        :param meta_data: Filters the results by the given meta_data.
        :param branch: Filters the results by the given branch or branches.
        :param commit: Filters the results by the commit (only works for full sha, not for shortened ones).
        :param include_retried_jobs: Include all retried job executions in each build’s jobs list if True.
               Without this parameter, you'll see only the most recently run job for each step.
        :param page: Int to determine which page to read from (See Pagination in README)
        :param with_pagination: Bool to return a response with pagination attributes
        :return: Returns a paginated list of a pipeline’s builds.
        """

        self.__validate_dates([created_from, created_to, finished_from])
        self.__are_valid_states(states)

        query_params = {
            "creator": creator,
            "created_from": self.__api_date_format(created_from),
            "created_to": self.__api_date_format(created_to),
            "finished_from": self.__api_date_format(finished_from),
            "state": self.__get_build_states_query_param(states),
            "branch": self.__get_branches_query_param(branch),
            "commit": commit,
            "include_retried_jobs": True if include_retried_jobs is True else None,
            "page": page,
        }
        query_params.update(self.__process_meta_data(meta_data))

        return self.client.get(
            self.path_by_pipeline.format(organization, pipeline),
            query_params,
            with_pagination=with_pagination,
        )

    def get_build_by_number(
        self, organization, pipeline, build_number, include_retried_jobs=None
    ):
        """
        Get build by build number

        :param organization: Organization slug
        :param pipeline: Pipeline slug
        :param build_number: Build number
        :param include_retried_jobs: Include all retried job executions in each build’s jobs list if True.
               Without this parameter, you'll see only the most recently run job for each step.
        :return: A build
        """
        query_params = {
            "include_retried_jobs": True if include_retried_jobs is True else None
        }
        return self.client.get(
            self.path_for_build_number.format(organization, pipeline, build_number),
            query_params=query_params,
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

    def cancel_build(self, organization, pipeline, build_number):
        cancel = "/cancel"
        return self.client.put(
            self.path_for_build_number.format(organization, pipeline, build_number)
            + cancel
        )

    def rebuild_build(self, organization, pipeline, build_number):
        rebuild = "/rebuild"
        return self.client.put(
            self.path_for_build_number.format(organization, pipeline, build_number)
            + rebuild
        )

    @staticmethod
    def __process_meta_data(meta_data):
        if not meta_data:
            return {}
        else:
            return {
                "meta_data[{}]".format(name): value for name, value in meta_data.items()
            }

    @staticmethod
    def __validate_dates(datetimes):
        for date in datetimes:
            if date is not None:
                if not isinstance(date, datetime.date):
                    raise NotValidDateTime

    @staticmethod
    def __api_date_format(datetime):
        if datetime is None:
            return None
        return datetime.isoformat()

    @staticmethod
    def __are_valid_states(states):
        if not isinstance(states, List):
            raise BuildStateNotAList
        if not states:
            return
        for state in states:
            if not isinstance(state, BuildState):
                raise NotValidBuildState

    @staticmethod
    def __get_build_states_query_param(states):
        if not states:
            return None
        if len(states) == 1:
            return "state=" + states[0].value
        else:
            param_string = ""
            for state in states:
                param_string += "state[]={}&".format(state.value)
            return param_string[:-1]

    @staticmethod
    def __get_branches_query_param(branches):
        if not branches:
            return None

        if isinstance(branches, List):
            param_string = ""
            for branch in branches:
                param_string += "branch[]={}&".format(branch)
            return param_string[:-1]
        else:
            return "branch=" + branches
