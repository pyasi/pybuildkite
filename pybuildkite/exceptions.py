class NoTokenException(Exception):
    """
    Indicates that a token was not set when it was required
    """

    pass


# TODO: Rename to NoAccessTokenException.
class NoAcccessTokenException(NoTokenException):
    """
    Indicates that an access token was not set when it was required
    """

    pass


class NoAgentTokenException(NoTokenException):
    """
    Indicates that an agent token was not set when it was required
    """

    pass


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


class BuildStateNotAList(Exception):
    """
    Raised when build state is not passed as a list
    """

    pass
