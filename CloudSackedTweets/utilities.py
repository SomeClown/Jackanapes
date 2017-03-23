#!/usr/local/bin/python3

from functools import wraps
import logging
import time
import progressbar


def logging_wrapper(original_function: object) -> object:
    """
        :type original_function: object
        :rtype: object
        """
    logging.basicConfig(filename='{}.log'.format(original_function.__name__),
                        format='%(asctime)s %(levelname)-8s %(message)s',
                        datefmt='%a, %d %b %Y %H:%M:%S',level=logging.INFO)

    @wraps(original_function)
    def wrapper(*args, **kwargs):
        logging.info(
                'Ran with args: {}, and kwargs: {}'.format(args, kwargs))
        return original_function(*args, **kwargs)
    return wrapper


def progress_bar_wrapper(original_function: object) -> object:
    """

    :param original_function: object
    :rtype: object
    """

    bar = progressbar.ProgressBar(max_value=progressbar.UnknownLength)

    @wraps(original_function)
    def wrapper(*args, **kwargs):
        for i in bar((i for i in range(8))):
            time.sleep(0.1)
            bar.update(i)
        return original_function(*args, **kwargs)
    return wrapper
