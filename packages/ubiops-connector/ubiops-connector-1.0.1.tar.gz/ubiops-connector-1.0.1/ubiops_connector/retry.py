import functools
import logging
import time

from .exceptions import RecoverableConnectorError


logger = logging.getLogger('Retry')


def retry(attempts=3):
    """
    Retry calling the decorated function as many times as the specified number of attempts

    :param int attempts: number of attempts before giving up and passing the exception along. If the argument
        attempts is passed to the decorated function, then this will be used instead.
    """

    def retry_decorator(f):

        @functools.wraps(f)
        def retry_function(*args, **kwargs):

            nonlocal attempts

            attempt = 1

            if 'attempts' in kwargs:
                attempts = kwargs.pop('attempts')

            # Only retry as the number of attempts provided
            while attempt < attempts:
                try:
                    return f(*args, **kwargs)
                except RecoverableConnectorError as e:
                    logger.warning(e)
                    logger.warning(f"Retrying in {attempt * 2:.2f} seconds")
                    time.sleep(attempt * 2)

                    attempt += 1

            # We don't catch exceptions on the final attempt
            return f(*args, **kwargs)

        return retry_function

    return retry_decorator
