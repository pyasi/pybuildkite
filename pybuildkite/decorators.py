from typing import Callable
from pybuildkite.exceptions import NoAcccessTokenException, NoAgentTokenException


def requires_access_token(func: Callable):
    """
    This annotation protects API calls that require authentication.

    It will cause them to raise NoAcccessTokenException if the token is not set in the client.

    :return: Function decorated with the protection
    """

    def wrapper(self, *args, **kwargs):
        """
        Call func or raise NoAcccessTokenException if no access token is set

        :param self:
        :param args: Optional
        :param kwargs: Optional

        :raises NoAcccessTokenException: If no access token is set
        :return:
        """
        if not self.client.is_access_token_set():
            raise NoAcccessTokenException
        else:
            return func(self, *args, **kwargs)

    return wrapper


def requires_agent_token(func: Callable):
    """
    This annotation protects API calls that require authentication.

    It will cause them to raise NoAgentTokenException if the token is not set in the client.

    :return: Function decorated with the protection
    """

    def wrapper(self, *args, **kwargs):
        """
        Call func or raise NoAgentTokenException if no access token is set

        :param self:
        :param args: Optional
        :param kwargs: Optional

        :raises NoAgentTokenException: If no access token is set
        :return:
        """
        if not self.client.is_agent_token_set():
            raise NoAgentTokenException
        else:
            return func(self, *args, **kwargs)

    return wrapper
