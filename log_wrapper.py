#!/usr/local/bin/python3

from functools import wraps

def logging_wrapper(original_function: object) -> object:
    """
        :type original: object
        :rtype: object
        """
    import logging
    logging.basicConfig(filename='{}.log'.format(original_function.__name__), 
            format='%(asctime)s %(levelname)-8s %(message)s', 
            datefmt='%a, %d %b %Y %H:%M:%S',level=logging.INFO)

    @wraps(original_function)
    def wrapper(*args, **kwargs):
        logging.info(
                'Ran with args: {}, and kwargs: {}'.format(args, kwargs))
        return original_function(*args, **kwargs)
    return wrapper
