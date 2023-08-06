# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""General purpose utils for AutoML wide code"""
import logging
from typing import Any, Optional, Callable

from azureml.automl.core.shared import logging_utilities


def retry_with_backoff(retries: int,
                       delay: int = 5,
                       backoff: int = 2,
                       raise_ex: bool = True,
                       logger: Optional[logging.Logger] = None) -> 'Callable[..., Callable[..., Any]]':
    """
    Function decorator that attempts to retry the wrapped function a fixed number of times, with exponential backoff.

    Usage:
        @retry_with_backoff(retries=3, delay=5, backoff=2, logger=None)
        def service_request():
            # function logic that may raise an exception, but may
            # return a successful response subsequently

    The above example will retry the function `service_request()` 3 times, at intervals of 5 sec, 10 sec, 20 sec

    Currently a retry will be done for *any* exception thrown. However, as per need, this can be easily extended to
    handle only a specific set of exceptions and pass/raise the others.

    Note: Make sure the exceptions don't contain PII, or in other words, you're in control of the logger.

    Reference: https://wiki.python.org/moin/PythonDecoratorLibrary#Retry

    :param retries: The number of retries to attempt
    :param delay: A fixed delay in seconds to begin with
    :param backoff: Multiplying factor by which to delay the subsequent retries
    :param raise_ex: Whether to raise exception if all retries are exhausted
    :param logger: Optional logger to help log exception details
    :return: Any (whatever the wrapped function returns)
    """
    assert retries > 0, "Number of retries should be greater than 0"

    if logger is None:
        logger = logging.getLogger('retry_with_backoff')

    assert logger is not None

    if delay * backoff == 0:
        logger.warning('Either delay[{}] or backoff[{}] is set to 0, this will result in continuous retries.'.
                       format(delay, backoff))

    def retry_decorator(function: 'Callable[..., Any]') -> 'Callable[..., Any]':
        from functools import wraps
        from time import sleep

        @wraps(function)
        def retry(*args, **kwargs):
            cur_attempt, _delay = 1, delay
            while cur_attempt <= retries:
                try:
                    return function(*args, **kwargs)
                except Exception as e:
                    if logger:
                        logger.warning('Function {} failed at attempt {} with exception of type: {}.'
                                       'Retrying in {} seconds'.
                                       format(function.__name__,
                                              cur_attempt,
                                              e.__class__.__name__,
                                              _delay))
                    cur_attempt += 1
                    if cur_attempt > retries:
                        if raise_ex:
                            raise
                        else:
                            break
                    sleep(_delay)
                    _delay *= backoff
        return retry
    return retry_decorator
