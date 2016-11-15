#!/usr/local/bin/python3
# Command line twitter client in the style of traditional unix shell commands
# Extensible so it can run as a bot, or be integrated into another application

__author__ = 'SomeClown'

import curses.textpad
import json
import os
import re
import time
import globalVars
import sys

from authorization import initialAuth

from derp import *


def _mkdir_recursive(self, path):
    sub_path = os.path.dirname(path)
    if not os.path.exists(sub_path):
        self._mkdir_recursive(sub_path)
        if not os.path.exists(path):
            os.mkdir(path)


@initialAuth
def printFriends(number: object) -> object:
    """

    :rtype: object
    """
    try:
        globalVars.screen.nodelay(True)
        globalVars.screen.addstr('\n')
        globalVars.screen.addstr('-------------------------------------------------------' + '\n')
        globalVars.screen.addstr(str(globalVars.user.screen_name) + '\n')
        globalVars.screen.addstr('-------------------------------------------------------')
        globalVars.screen.addstr('\n')
        globalVars.screen.addstr('Friends Count: ' + str(globalVars.user.followers_count) + '\n')
        if number == 0:
            return
        else:
            for friend in globalVars.user.friends(count=number):
                globalVars.screen.addstr('\t' + friend.screen_name + '\n')
        globalVars.screen.addstr('\n')
        globalVars.screen.addstr('-------------------------------------------------------')
        globalVars.screen.addstr('\n')
        globalVars.screen.refresh()  # Refresh screen now that strings added
    except curses.error:
        Cleanup(1)

    finally:
        globalVars.screen.addstr('\n Press q to exit program...')
        while True:
            key = globalVars.screen.getch()
            if key == ord('q'):
                Cleanup(0)

    return None


@initialAuth
def printTimeline(number):
    # Print user's public timeline
    """

    :param number:
    :return:
    """
    public_tweets = globalVars.api.home_timeline(count=number)
    try:
        globalVars.screen.addstr('\n')
        if number == 0:
            return
        else:
            for tweet in public_tweets:
                globalVars.screen.addstr(str(tweet.user.name), curses.color_pair(1))
                globalVars.screen.addstr(str(': ' + tweet.text + '\n'))
            globalVars.screen.refresh()  # Refresh screen now that strings added

    except curses.error:
        Cleanup(1)

    finally:
        globalVars.screen.addstr('\n Press q to exit program...')
        while True:
            key = globalVars.screen.getch()
            if key == ord('q'):
                Cleanup(0)
    return None


@initialAuth
def printMentions(number):
    # Print user's mentions
    """

    :param number:
    :return:
    """
    myMentions = globalVars.api.mentions_timeline(count=number)
    try:
        globalVars.screen.addstr('\n')
        if number == 0:
            return
        else:
            for mention in myMentions:
                globalVars.screen.addstr(str(mention.user.name), curses.color_pair(1))
                globalVars.screen.addstr(str(': ' + mention.text + '\n'))
            globalVars.screen.refresh()
    except curses.error:
        Cleanup(1)

    finally:
        globalVars.screen.addstr('\n Press q to exit program...')
        while True:
            key = globalVars.screen.getch()
            if key == ord('q'):
                Cleanup(0)
    return None


@initialAuth
def printRetweets(number):
    # Print user's tweets that others have retweeted
    """

    :param number:
    :return:
    """
    otherRetweets = globalVars.api.retweets_of_me(count=number, include_user_entities=False)
    try:
        globalVars.screen.addstr('\n')
        if number == 0:
            Cleanup(1)
            return
        else:
            for retweets in otherRetweets:
                # idName = globalVars.api.get_user(retweets.id_str)
                # globalVars.screen.addstr(str(idName.screen_name))
                globalVars.screen.addstr(str(retweets.id_str), curses.color_pair(1))
                globalVars.screen.addstr(str(': ' + retweets.text + '\n'))
            globalVars.screen.refresh()
    except curses.error:
        # import pdb; pdb.set_trace()
        Cleanup(1)

    finally:
        globalVars.screen.addstr('\n Press q to exit program...')
        while True:
            key = globalVars.screen.getch()
            if key == ord('q'):
                Cleanup(0)
    return None


@initialAuth
def printMyInfo():
    # Print information about me
    """

    :return:
    """
    myInfo = globalVars.api.me()
    try:
        # Format and print handle, username, and user ID
        globalVars.screen.addstr('\n')
        globalVars.screen.addstr(str('@'), curses.color_pair(1))
        globalVars.screen.addstr(str(myInfo.screen_name), curses.color_pair(1))
        globalVars.screen.addstr(str(' (') + str(myInfo.name), curses.color_pair(2))
        globalVars.screen.addstr(str('/') + str(myInfo.id_str), curses.color_pair(2))
        globalVars.screen.addstr(str(')'))

        # Format and print created date for user
        globalVars.screen.addstr(str('  User since: '), curses.color_pair(1))
        globalVars.screen.addstr(str(myInfo.created_at), curses.color_pair(2))

        # Format and print followers count
        globalVars.screen.addstr(str(' Followers: '), curses.color_pair(1))
        globalVars.screen.addstr(str(myInfo.followers_count), curses.color_pair(2))

        # Format and print number of tweets
        globalVars.screen.addstr(str(' Tweets: '), curses.color_pair(1))
        globalVars.screen.addstr(str(myInfo.statuses_count), curses.color_pair(2))

        # Format and print user's reported location
        globalVars.screen.addstr(str(' Location: '), curses.color_pair(1))
        globalVars.screen.addstr(str(myInfo.location), curses.color_pair(2))

        # Format and print description from user profile
        globalVars.screen.addstr('\n' + json.dumps(myInfo.description))
        globalVars.screen.addstr('\n')

        # Format and print user's URL, if present
        globalVars.screen.addstr(str('URL: '), curses.color_pair(1))
        globalVars.screen.addstr(str(myInfo.url))

        # Format and print link to profile picture
        globalVars.screen.addstr(str(' Profile Picture: '), curses.color_pair(1))
        globalVars.screen.addstr(str(myInfo.profile_image_url_https))
        globalVars.screen.addstr(str('\n'))

        # Add line space and clean up
        globalVars.screen.addstr('\n')
        globalVars.screen.refresh()

    except curses.error:
        Cleanup(1)

    finally:
        globalVars.screen.addstr('\n Press q to exit program...')
        while True:
            key = globalVars.screen.getch()
            if key == ord('q'):
                Cleanup(0)
    return None


@initialAuth
def printNotMe(data):
    # Print information on another user
    """

    :param data:
    :return:
    """
    notMe = globalVars.api.get_user(screen_name=data)
    try:

        # Format and print handle, username, and user ID
        globalVars.screen.addstr('\n')
        globalVars.screen.addstr(str('@'), curses.color_pair(1))
        globalVars.screen.addstr(str(notMe.screen_name), curses.color_pair(1))
        globalVars.screen.addstr(str(' (' + notMe.name + '/' + notMe.id_str
                                     + ')'))

        # Format and print created date for user
        globalVars.screen.addstr(str('  User since: '), curses.color_pair(1))
        globalVars.screen.addstr(str(notMe.created_at))

        # Format and print followers count
        globalVars.screen.addstr(str(' Followers: '), curses.color_pair(1))
        globalVars.screen.addstr(str(notMe.followers_count))

        # Format and print number of tweets
        globalVars.screen.addstr(str(' Tweets: '), curses.color_pair(1))
        globalVars.screen.addstr(str(notMe.statuses_count))

        # Format and print user's reported location
        globalVars.screen.addstr(str(' Location: '), curses.color_pair(1))
        globalVars.screen.addstr(str(notMe.location))

        # Format and print description from user profile
        globalVars.screen.addstr('\n' + json.dumps(notMe.description) + '\n')

        # Format and print user's URL, if present
        globalVars.screen.addstr(str('URL: '), curses.color_pair(1))
        globalVars.screen.addstr(str(notMe.url))

        # Format and print link to profile picture
        globalVars.screen.addstr(str(' Profile Picture: '), curses.color_pair(1))
        globalVars.screen.addstr(str(notMe.profile_image_url_https) + '\n')

        # Add line space and clean up
        globalVars.screen.addstr('\n')
        globalVars.screen.refresh()

    except curses.error:
        Cleanup(1)

    finally:
        globalVars.screen.addstr('\n Press q to exit program...')
        while True:
            key = globalVars.screen.getch()
            if key == ord('q'):
                Cleanup(0)
    return None


@initialAuth
def termSearch(term):
    """

    :param term:
    :return:
    """
    try:
        search = str(term[0])
        count = int(term[1])
        for tweet in tweepy.Cursor(globalVars.api.search, q=search).items(count):
            globalVars.screen.addstr(str(tweet.created_at) + ': ')
            globalVars.screen.addstr(str(tweet.user.name), curses.color_pair(1))
            globalVars.screen.addstr(str(': ' + tweet.text + '\n'))
            globalVars.screen.refresh()  # Refresh screen now that strings added

    except curses.error:
        Cleanup(1)
    finally:
        globalVars.screen.addstr('\n Press q to exit program...')
        while True:
            key = globalVars.screen.getch()
            if key == ord('q'):
                Cleanup(0)
    return None


def Cleanup(exitCode: object) -> object:
    """

    :param exitCode:
    """
    curses.echo()
    curses.nocbreak()
    curses.endwin()
    if exitCode == 1:
        print('Egads, it looks like we shit the bed...')
        sys.exit(exitCode)
    else:
        sys.exit(exitCode)


class Streamer(tweepy.StreamListener):
    def on_status(self, status):

        """

        :param status:
        """
        globalVars.screen.nodelay(1)
        c = globalVars.screen.getch()
        # TODO: Pull status.text into named str, regex for @handle and #hashtag
        #try:
        globalVars.screen.addstr(str(status.user.name), curses.color_pair(1))
        globalVars.screen.addstr(str(': ' + status.text + '\n'))
        globalVars.screen.refresh()  # Refresh screen now that strings added
        if c == ord('q'):
            Cleanup(0)
        """
        except curses.error:
            Cleanup(1)
        except BaseException as e:
            Cleanup(1)
            print('failed on_status, ', str(e))
            time.sleep(5)
        """


        """
    @staticmethod
    def on__error(status):


        :param status:

        Cleanup(1)
        print(status)
        """

    """
    # This is consuming everything
    # including the session opening friends list
    def on_data(self, data):
        #convert tweepy object to raw json/dictionary
        json_data = json.loads(data)

        tweetText = json_data['friends']
        print(tweetText)

        #Pretty print this to the screen
        print(json.dumps(json_data, indent=4, sort_keys=True))
    """


@initialAuth
def getStream():
    """

    """
    terenStream = tweepy.Stream(globalVars.auth, Streamer())
    terenStream.userstream()


@initialAuth
def getFollowStream(user):
    """

    :param user:
    """
    terenStream = tweepy.Stream(globalVars.auth, Streamer())
    userID = str(user)
    if userID != '17028130':
        terenStream.filter(follow=[userID])
    else:
        terenStream.userstream()


@initialAuth
def getStreamSearch(searchHash):
    """

    :param searchHash:
    """
    terenStream = tweepy.Stream(globalVars.auth, Streamer())
    str1 = ''.join(searchHash)
    try:
        terenStream.filter(track=[str1])
    except curses.error:
        Cleanup(1)
    #except BaseException as e:
    #    Cleanup(1)
    #    print('failed on_status, ', str(e))
    #    time.sleep(5)


@initialAuth
def directSend(user, msg):
    """

    :param user:
    :param msg:
    :return:
    """
    nameCheck = re.compile(r'(@)+')
    nameResult = nameCheck.search(user)

    if len(msg) >= 140:
        print('Tweets must be 140 characters or less')
    elif nameResult is None:
        print('Incorrect username format (must include @)')
    else:
        globalVars.api.send_direct_message(screen_name=user, text=msg)
        print('\nMessage "{}" sent to {} successfully\n'.format(msg, user))
        Cleanup(0)
    return None


@initialAuth
def statusUpdate(text):
    """

    :param text:
    :return:
    """
    if len(text) >= 140:
        print('Tweets must be 140 characters or less')
    else:
        globalVars.api.update_status(status=text)
        print('\nStatus "{}" updated successfully\n'.format(text))
        Cleanup(0)
    return None
