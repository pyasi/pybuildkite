import datetime
from enum import Enum
from pybuildkite.client import Client


class BuildState(Enum):
    RUNNING = 1
    SCHEDULED = 2
    PASSED = 3
    FAILED = 4
    BLOCKED = 5
    CANCELED = 6
    CANCELING = 7
    SKIPPED = 8
    NOT_RUN = 9
    FINISHED = 10


class Builds(Client):

    def __init__(self, client, base_url):
        """

        """
        self.client = client
        self.path = base_url + 'builds/'

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

    @staticmethod
    def __validate_dates(datetimes):
        for date in datetimes:
            if date is not None:
                if not isinstance(date, datetime.date):
                    raise NotValidDateTime

    @staticmethod
    def __is_valid_state(state):
        if state not in BuildState.__members__:
            raise NotValidBuildState


class NotValidDateTime(Exception):
    pass


class NotValidBuildState(Exception):
    pass

