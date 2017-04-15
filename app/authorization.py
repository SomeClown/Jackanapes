#!/usr/local/bin/python3

import os
import globalVars
import tweepy
from functools import wraps
from utilities import logging_wrapper

__author__ = 'SomeClown'


@logging_wrapper
def initial_auth(original: object) -> object:
    """
    :type original: object
    :rtype: object
    """
    @wraps(original)
    def wrapper(*args, **kwargs):
        globalVars.auth = tweepy.OAuthHandler(globalVars.consumer_token, globalVars.consumer_token_secret)
        globalVars.api = tweepy.API(globalVars.auth, retry_count=3, retry_delay=5,
                                    retry_errors={500, 503, 504})
        globalVars.user_id = globalVars.api.get_user(globalVars.user)

        # Try to load with access token, if that doesn't work we must not have valid credentials
        # and we begin the process to call out to Twitter and get new credentials assigned
        try:
            globalVars.auth.set_access_token(globalVars.access_token, globalVars.access_token_secret)

        # Move through granting access token process
        except IOError:
            print('Invalid or missing credentials... \n')

            try:
                redirect_url = globalVars.auth.get_authorization_url()
                print('If a new browser window doesn\'t open, go to this URL: ')
                print(redirect_url)
                print('and authorize this app. Return here with the pin code you receive in order to finish')
                print('authorizing this app to access your account as specified.')
                import webbrowser
                assert isinstance(redirect_url, object)
                webbrowser.open_new_tab(redirect_url)
                verify_pin = input('Pin Code: ')
                assert isinstance(verify_pin, object)
                print(verify_pin)
                try:
                    globalVars.auth.get_access_token(verify_pin)
                except tweepy.TweepError:
                    print('Error! Failed to get access token, or incorrect token was entered.')
                    return 1

                access_token = globalVars.auth.access_token
                access_token_secret = globalVars.auth.access_token_secret

                # Write all of this good authentication stuff to a file
                # so we don't have to do it everytime we run the program
                # TODO: Change this to use os.mkdirs() so this is more concise
                home = ''
                if not os.path.exists(home + '/.jackanapes/'):
                    os.mkdir(home + '/.jackanapes/')
                    if not os.path.exists(home + '/.jackanapes/' + str(globalVars.user.screen_name)):
                        os.mkdir(home + '/.jackanapes/' + str(globalVars.user.screen_name))

                if_config_file = (home + '/.jackanapes/' + str(globalVars.user.screen_name) + '/.jackanapes')
                print(if_config_file)
                with open(if_config_file, 'w+') as outFile:
                    outFile.write(access_token + '\n')  # function as a better way to store
                    outFile.write(access_token_secret + '\n')  # the data

            # Something is so horribly borked we're just going to say fuck it
            except tweepy.TweepError:
                print('Error! Failed to get request token.')
                return (1)
        return original(*args, **kwargs)

    assert isinstance(wrapper, object)
    return wrapper


def main():
    pass
if __name__ == '__main__':
    main()
else:
    pass
