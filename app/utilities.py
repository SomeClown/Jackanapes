#!/usr/bin/env python3

from functools import wraps
import logging
import time
import progressbar
import yaml
import globalVars
import os


__author__ = 'SomeClown'
__license__ = "MIT"
__maintainer__ = "Teren Bryson"
__email__ = "teren@packetqueue.net"


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


def set_config():

    # Load and assign key variables from yaml configuration file
    with open('config.yml', 'r') as my_config_file:
        settings = yaml.load(my_config_file)
        globalVars.access_token = settings['access_token']
        globalVars.access_token_secret = settings['access_token_secret']
        globalVars.consumer_token = settings['consumer_token']
        globalVars.consumer_token_secret = settings['consumer_token_secret']
        globalVars.user = settings['user']
        globalVars.home = settings['home']
        globalVars.followers = settings['followers']
        globalVars.friend_file = settings['friend_file']
        globalVars.no_follow = settings['no_follow']
        globalVars.post_limit = settings['post_limit']
        globalVars.random_limit = settings['random_limit']
        globalVars.output = settings['output']
        globalVars.debugging = settings['debugging']
        globalVars.home_dir = os.path.expanduser('~')
        globalVars.complete_dir_path = os.path.join(globalVars.home_dir, globalVars.home, globalVars.user)
