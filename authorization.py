#!/usr/local/bin/python3

import os
import derp
import globalVars
import tweepy


def initialAuth(original: object) -> object:
    """
    	:type original: object
    	:rtype: object
    	"""

    def wrapper(*args, **kwargs):
        globalVars.auth = derp.hokum()
        globalVars.api = tweepy.API(globalVars.auth)
        globalVars.user = globalVars.api.get_user('SomeClown')
        # Check to see if config file with credentials exists
        # if it does, load our keys from the file and pass them to the
        # auth.set_access_token() method
        try:
            home = os.path.expanduser("~")
            configFile = (home + '/.packetqueue/' + str(globalVars.user.screen_name) + '/.packetqueue')
            with open(configFile, 'r') as inFile:
                accessToken = inFile.readline().strip()
                accessTokenSecret = inFile.readline().strip()
                globalVars.auth.set_access_token(accessToken, accessTokenSecret)

        # If the file doesn't exist, notify user then move through granting access token process
        except IOError:
            print('File .packetqueue doesn\'t exist... \n')

            try:
                redirect_url = globalVars.auth.get_authorization_url()
                print('If a new browser window doesn\'t open, go to this URL: ')
                print(redirect_url)
                print('and authorize this app. Return here with the pin code you receive in order to finish')
                print('authorizing this app to access your account as specified.')
                import webbrowser
                webbrowser.open_new_tab(redirect_url)
                verifyPin = input('Pin Code: ')
                print(verifyPin)
                try:
                    globalVars.auth.get_access_token(verifyPin)
                except tweepy.TweepError:
                    print('Error! Failed to get access token, or incorrect token was entered.')
                    return (1)

                accessToken = globalVars.auth.access_token
                accessTokenSecret = globalVars.auth.access_token_secret

                # Write all of this good authentication stuff to a file
                # so we don't have to do it everytime we run the program
                ifconfigPath = os.path.join(home, '/.packetqueue/', str(globalVars.user.screen_name))
                if not os.path.exists(home + '/.packetqueue/'):
                    os.mkdir(home + '/.packetqueue/')
                    if not os.path.exists(home + '/.packetqueue/' + str(globalVars.user.screen_name)):
                        os.mkdir(home + '/.packetqueue/' + str(globalVars.user.screen_name))

                ifconfigFile = (home + '/.packetqueue/' + str(globalVars.user.screen_name) + '/.packetqueue')
                print(ifconfigFile)
                with open(ifconfigFile, 'w+') as outFile:
                    outFile.write(accessToken + '\n')  # function as a better way to store
                    outFile.write(accessTokenSecret + '\n')  # the data


            # Something is so horribly borked we're just going to say fuck it
            except tweepy.TweepError:
                print('Error! Failed to get request token.')
                return (1)
        return original(*args, **kwargs)

    assert isinstance(wrapper, object)
    return wrapper
