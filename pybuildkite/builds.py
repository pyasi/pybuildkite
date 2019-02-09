import datetime
import urllib
from enum import Enum
from pybuildkite.client import Client


class BuildState(Enum):
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
    CREATOR = "creator"
    CREATED_FROM = "created_from"
    CREATED_TO = "created_to"
    FINISHED_FROM = "finished_from"
    STATE = "state"
    META_DATA = "meta_data"
    BRANCH = "branch"
    COMMIT = "commit"


class Builds(Client):

    def __init__(self, client, base_url):
        """

        """
        self.client = client
        self.path = base_url + 'builds'

    def list_all(self, creator=None, created_from=None, created_to=None, finished_from=None,
                 state=None, meta_data=None, branch=None, commit=None):
        """

        :param creator:
        :param created_from:
        :param created_to:
        :param finished_from:
        :param state:
        :param meta_data: Filters the results by the given meta_data. Example: ?meta_data[some-key]=some-value
        :param branch:
        :param commit:
        :return:
        """
        self.__validate_dates([created_from, created_to, finished_from])
        self.__is_valid_state(state)


        query_params = {
            "creator": creator,
            "created_from": created_from,
            "created_to": created_to,
            "finished_from": finished_from,
            "state": state,
            "meta_data": meta_data,
            "branch": branch,
            "commit": commit
        }
        query_params = self.__clean_query_params(query_params)
        return self.client.get(self.path, query_params)

    def __clean_query_params(self, query_params):
        """

        :param query_params:
        :return:
        """
        return {key: value for key, value in query_params.items() if value is not None}


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
    pass


class NotValidBuildState(Exception):
    pass

