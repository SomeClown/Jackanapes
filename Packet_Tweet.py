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
def printfriends(number: object) -> object:
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
        cleanup(1)

    finally:
        globalVars.screen.addstr('\n Press q to exit program...')
        while True:
            key = globalVars.screen.getch()
            if key == ord('q'):
                cleanup(0)

    return None


@initialAuth
def printtimeline(number: object) -> object:
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
        cleanup(1)

    finally:
        globalVars.screen.addstr('\n Press q to exit program...')
        while True:
            key = globalVars.screen.getch()
            if key == ord('q'):
                cleanup(0)
    return None


@initialAuth
def printmentions(number):
    # Print user's mentions
    """

    :param number:
    :return:
    """
    my_mentions = globalVars.api.mentions_timeline(count=number)
    try:
        globalVars.screen.addstr('\n')
        if number == 0:
            return
        else:
            for mention in my_mentions:
                globalVars.screen.addstr(str(mention.user.name), curses.color_pair(1))
                globalVars.screen.addstr(str(': ' + mention.text + '\n'))
            globalVars.screen.refresh()
    except curses.error:
        cleanup(1)

    finally:
        globalVars.screen.addstr('\n Press q to exit program...')
        while True:
            key = globalVars.screen.getch()
            if key == ord('q'):
                cleanup(0)
    return None


@initialAuth
def print_retweets(number: object) -> object:
    # Print user's tweets that others have retweeted
    """

    :return:
    :param number:
    :return:
    """
    other_retweets = globalVars.api.retweets_of_me(count=number, include_user_entities=False)
    try:
        globalVars.screen.addstr('\n')
        if number == 0:
            cleanup(1)
            return
        else:
            for retweets in other_retweets:
                globalVars.screen.addstr(str(retweets.id_str), curses.color_pair(1))
                globalVars.screen.addstr(str(': ' + retweets.text + '\n'))
            globalVars.screen.refresh()
    except curses.error:
        cleanup(1)

    finally:
        globalVars.screen.addstr('\n Press q to exit program...')
        while True:
            key = globalVars.screen.getch()
            if key == ord('q'):
                cleanup(0)
    return None


@initialAuth
def print_my_info() -> object:
    # Print information about me
    """

    :return:
    """
    my_info = globalVars.api.me()
    try:
        # Format and print handle, username, and user ID
        globalVars.screen.addstr('\n')
        globalVars.screen.addstr(str('@'), curses.color_pair(1))
        globalVars.screen.addstr(str(my_info.screen_name), curses.color_pair(1))
        globalVars.screen.addstr(str(' (') + str(my_info.name), curses.color_pair(2))
        globalVars.screen.addstr(str('/') + str(my_info.id_str), curses.color_pair(2))
        globalVars.screen.addstr(str(')'))

        # Format and print created date for user
        globalVars.screen.addstr(str('  User since: '), curses.color_pair(1))
        globalVars.screen.addstr(str(my_info.created_at), curses.color_pair(2))

        # Format and print followers count
        globalVars.screen.addstr(str(' Followers: '), curses.color_pair(1))
        globalVars.screen.addstr(str(my_info.followers_count), curses.color_pair(2))

        # Format and print number of tweets
        globalVars.screen.addstr(str(' Tweets: '), curses.color_pair(1))
        globalVars.screen.addstr(str(my_info.statuses_count), curses.color_pair(2))

        # Format and print user's reported location
        globalVars.screen.addstr(str(' Location: '), curses.color_pair(1))
        globalVars.screen.addstr(str(my_info.location), curses.color_pair(2))

        # Format and print description from user profile
        globalVars.screen.addstr('\n' + json.dumps(my_info.description))
        globalVars.screen.addstr('\n')

        # Format and print user's URL, if present
        globalVars.screen.addstr(str('URL: '), curses.color_pair(1))
        globalVars.screen.addstr(str(my_info.url))

        # Format and print link to profile picture
        globalVars.screen.addstr(str(' Profile Picture: '), curses.color_pair(1))
        globalVars.screen.addstr(str(my_info.profile_image_url_https))
        globalVars.screen.addstr(str('\n'))

        # Add line space and clean up
        globalVars.screen.addstr('\n')
        globalVars.screen.refresh()

    except curses.error:
        cleanup(1)

    finally:
        globalVars.screen.addstr('\n Press q to exit program...')
        while True:
            key = globalVars.screen.getch()
            if key == ord('q'):
                cleanup(0)
    return None


@initialAuth
def print_not_me(data: object) -> object:
    # Print information on another user
    """

    :param data:
    :return:
    """
    not_me = globalVars.api.get_user(screen_name=data)
    try:

        # Format and print handle, username, and user ID
        globalVars.screen.addstr('\n')
        globalVars.screen.addstr(str('@'), curses.color_pair(1))
        globalVars.screen.addstr(str(not_me.screen_name), curses.color_pair(1))
        globalVars.screen.addstr(str(' (' + not_me.name + '/' + not_me.id_str
                                     + ')'))

        # Format and print created date for user
        globalVars.screen.addstr(str('  User since: '), curses.color_pair(1))
        globalVars.screen.addstr(str(not_me.created_at))

        # Format and print followers count
        globalVars.screen.addstr(str(' Followers: '), curses.color_pair(1))
        globalVars.screen.addstr(str(not_me.followers_count))

        # Format and print number of tweets
        globalVars.screen.addstr(str(' Tweets: '), curses.color_pair(1))
        globalVars.screen.addstr(str(not_me.statuses_count))

        # Format and print user's reported location
        globalVars.screen.addstr(str(' Location: '), curses.color_pair(1))
        globalVars.screen.addstr(str(not_me.location))

        # Format and print description from user profile
        globalVars.screen.addstr('\n' + json.dumps(not_me.description) + '\n')

        # Format and print user's URL, if present
        globalVars.screen.addstr(str('URL: '), curses.color_pair(1))
        globalVars.screen.addstr(str(not_me.url))

        # Format and print link to profile picture
        globalVars.screen.addstr(str(' Profile Picture: '), curses.color_pair(1))
        globalVars.screen.addstr(str(not_me.profile_image_url_https) + '\n')

        # Add line space and clean up
        globalVars.screen.addstr('\n')
        globalVars.screen.refresh()

    except curses.error:
        cleanup(1)

    finally:
        globalVars.screen.addstr('\n Press q to exit program...')
        while True:
            key = globalVars.screen.getch()
            if key == ord('q'):
                cleanup(0)
    return None


@initialAuth
def term_search(term: object) -> object:
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
        cleanup(1)
    finally:
        globalVars.screen.addstr('\n Press q to exit program...')
        while True:
            key = globalVars.screen.getch()
            if key == ord('q'):
                cleanup(0)
    return None


def cleanup(exitCode: object) -> object:
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
    def on_status(self, status: object) -> object:

        """

        :param status:
        """
        globalVars.screen.nodelay(1)
        c = globalVars.screen.getch()
        # TODO: Pull status.text into named str, regex for @handle and #hashtag
        globalVars.screen.addstr(str(status.user.name), curses.color_pair(1))
        globalVars.screen.addstr(str(': ' + status.text + '\n'))
        globalVars.screen.refresh()  # Refresh screen now that strings added
        if c == ord('q'):
            cleanup(0)
        """
        except curses.error:
            cleanup(1)
        except BaseException as e:
            cleanup(1)
            print('failed on_status, ', str(e))
            time.sleep(5)
        """


        """
    @staticmethod
    def on__error(status):


        :param status:

        cleanup(1)
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
def get_stream() -> object:
    """

    """
    teren_stream = tweepy.Stream(globalVars.auth, Streamer())
    teren_stream.userstream()


@initialAuth
def get_follow_stream(user: object) -> object:
    """

    :param user:
    """
    teren_stream = tweepy.Stream(globalVars.auth, Streamer())
    user_ID = str(user)
    if user_ID != '17028130':
        teren_stream.filter(follow=[user_ID])
    else:
        teren_stream.userstream()


@initialAuth
def get_stream_search(searchHash: object) -> object:
    """

    :param searchHash:
    """
    teren_stream = tweepy.Stream(globalVars.auth, Streamer())
    str1 = ''.join(searchHash)
    try:
        teren_stream.filter(track=[str1])
    except curses.error:
        cleanup(1)
    #except BaseException as e:
    #    cleanup(1)
    #    print('failed on_status, ', str(e))
    #    time.sleep(5)


@initialAuth
def direct_send(user: object, msg: object) -> object:
    """

    :param user:
    :param msg:
    :return:
    """
    name_check = re.compile(r'(@)+')
    name_result = name_check.search(user)

    if len(msg) >= 140:
        print('Tweets must be 140 characters or less')
    elif name_result is None:
        print('Incorrect username format (must include @)')
    else:
        globalVars.api.send_direct_message(screen_name=user, text=msg)
        print('\nMessage "{}" sent to {} successfully\n'.format(msg, user))
        cleanup(0)
    return None


@initialAuth
def status_update(text: object) -> object:
    """

    :param text:
    :return:
    """
    if len(text) >= 140:
        print('Tweets must be 140 characters or less')
    else:
        globalVars.api.update_status(status=text)
        print('\nStatus "{}" updated successfully\n'.format(text))
        cleanup(0)
    return None
