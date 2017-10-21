"""Module for storage and conversion helpers functions"""
from typing import Callable, Any

from thriftpy.transport import TTransportException


def retry_on_connection_error(func: Callable, max_retries: int = 3) -> Any:
    """Decorator that should retry on HBase connection error

    :param func: function/method which should be wrapped
    :param max_retries: number of max retries which should take place
    :return: value from wrapped function/method
    """
    def func_wrapper(*args: Any, **kwargs: Any) -> Any:
        """Wrapper for a callable function/method

        :param args: arguments to this function/method
        :param kwargs: keyword arguments to this function/method
        :return: value from wrapped function/method
        """
        current_retry = 0

        while current_retry < max_retries:
            try:
                # Try to execute decorated function/method
                return func(*args, **kwargs)

            except (TTransportException, BrokenPipeError):
                # On transport exception (may be a connection failure) give the function a chance to execute properly.
                #  But if it maxed-out the maximum number of reties, let's re-raise the Exception to the parent to
                #  handle it on it's own.
                print('WARNING! Retying broken connection to HBase!')
                current_retry += 1
                if current_retry == max_retries:
                    raise
    return func_wrapper
