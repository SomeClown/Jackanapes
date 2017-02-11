#!/usr/local/bin/python3

def logging_wrapper(original_function: object) -> object:
    """
        :type original: object
        :rtype: object
        """
    import logging
    logging.basicConfig(filename='{}.log'.format(original_function.__name__), level=logging.INFO)

    def wrapper(*args, **kwargs):
        logging.info(
                'Ran with args: {}, and kwargs: {}'.format(args, kwargs))
        return original_function(*args, **kwargs)
    return wrapper
