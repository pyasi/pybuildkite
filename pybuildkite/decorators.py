from typing import Callable
from pybuildkite.exceptions import NoAcccessTokenException


def requires_token(func: Callable):
    """
    This annotation protects API calls that require authentication.

    It raises NoAcccessTokenException if neither an access token nor a Requests
    authentication object is configured in the client.

    :return: Function decorated with the protection
    """

    def wrapper(self, *args, **kwargs):
        """
        Call func or raise NoAcccessTokenException if no access token is set

        :param self:
        :param args: Optional
        :param kwargs: Optional

        :raises NoAcccessTokenException: If no authentication is configured
        :return:
        """
        if not self.client._is_authentication_configured():
            raise NoAcccessTokenException
        else:
            return func(self, *args, **kwargs)

    return wrapper
