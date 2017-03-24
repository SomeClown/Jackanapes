#!/usr/local/bin/python3
# Command line twitter client in the style of traditional unix shell commands
# Extensible so it can run as a bot, or be integrated into another application

import curses.textpad
import json
import os
import re
import globalVars
import sys
from authorization import initial_auth
from utilities import progress_bar_wrapper
import tweepy

__author__ = 'SomeClown'


class Streamer(tweepy.StreamListener):
    def on_status(self, status):
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


def init_curses():
    """
    Setup curses for use in which ever function requires it. Call this as needed
    """
    globalVars.screen = curses.initscr()
    try:
        globalVars.screen.scrollok(True)
        curses.noecho()  # Keeps key presses from echoing to screen
        curses.cbreak()  # Takes input away
        globalVars.screen.keypad(1)
        curses.start_color()
        curses.use_default_colors()
        curses.init_pair(1, curses.COLOR_RED, -1)       # Foreground Red/background transparent
        curses.init_pair(2, curses.COLOR_YELLOW, -1)    # Foreground Yellow/background transparent
    except SystemExit:
        curses.endwin()
        raise
    except KeyboardInterrupt:
        curses.endwin()
        raise


@initial_auth
class TweetArguments:

    def _mkdir_recursive(self, path):
        sub_path = os.path.dirname(path)
        if not os.path.exists(sub_path):
            self._mkdir_recursive(sub_path)
            if not os.path.exists(path):
                os.mkdir(path)

    @staticmethod
    def print_friends(number: int):
        """
        Print <number> of friends

        :param number:
        :return:

        print(globalVars.user)
        print('\n')
        print(globalVars.user_id)
        print('\n')
        print(globalVars.user_id.screen_name)
        print('\n')
        print(globalVars.user_id.followers_count)
        for friend in globalVars.user_id.friends(count=number):
            print('\t' + friend.screen_name + '\n')

        """
        try:
            globalVars.screen.nodelay(True)
            globalVars.screen.addstr('\n')
            globalVars.screen.addstr('-------------------------------------------------------' + '\n')
            globalVars.screen.addstr(str(globalVars.user) + ' friends count: '
                                     + str(globalVars.user_id.friends_count) + '\n')
            globalVars.screen.addstr('-------------------------------------------------------')
            globalVars.screen.addstr('\n')
            if number == 0:
                return
            else:
                for friend in globalVars.user_id.friends(count=number):
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

    @staticmethod
    def show_followers(number: int):
        """
        Print <number> of followers

        :param number:
        """
        try:
            globalVars.screen.nodelay(True)
            globalVars.screen.addstr('\n')
            globalVars.screen.addstr('-------------------------------------------------------' + '\n')
            globalVars.screen.addstr(str(globalVars.user) + ' followers count: '
                                     + str(globalVars.user_id.followers_count) + '\n')
            globalVars.screen.addstr('-------------------------------------------------------')
            globalVars.screen.addstr('\n')
            if number == 0:
                return
            else:
                for follower in globalVars.user_id.followers(count=number):
                    globalVars.screen.addstr('\t' + follower.screen_name + '\n')
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

    @staticmethod
    def save_followers(my_screen_name: str):
        """
        save followers list to a file for later use

        :param my_screen_name:
        """
        followers_count = globalVars.user.followers_count
        myfollowers = []
        try:
            cursor = tweepy.Cursor(globalVars.api.followers_ids, screen_name=my_screen_name, cursor=-1,
                                   wait_on_rate_limit=True, wait_on_rate_limit_notify=True, compression=True,
                                   skip_status=True, include_user_entities=False, count=5000)
            print('\n ', my_screen_name, 'has: ', followers_count, 'followers ')
            home = os.path.expanduser("~")
            config_file = (home + '/.packetqueue/' + str(globalVars.user.screen_name) + '/.followers')
            with open(config_file, 'w') as f:
                for page in cursor.pages():
                    for item in page:
                        myfollowers.append(item)
                f.write('\n'.join(map(str, myfollowers)))
        except tweepy.RateLimitError:
            print(tweepy.RateLimitError(reason='Exceeded Twitter Rate Limit'))
        except BaseException as e:
            print(e)
        return None

    @staticmethod
    def save_friends(my_screen_name: str):
        """
        save friends list to a file for later use

        :param my_screen_name:
        """
        friends_count = globalVars.user.friends_count
        my_friends = []
        try:
            cursor = tweepy.Cursor(globalVars.api.friends, screen_name=my_screen_name, cursor=-1,
                                   wait_on_rate_limit=True, wait_on_rate_limit_notify=True, compression=True,
                                   skip_status=True, include_user_entities=False, count=200)
            print('\n ', my_screen_name, 'has: ', friends_count, 'friends ')
            home = os.path.expanduser("~")
            config_file = (home + '/.packetqueue/' + str(globalVars.user.screen_name) + '/.friends')
            with open(config_file, 'w') as f:
                for page in cursor.pages():
                    for item in page:
                        my_friends.append(str(item.id) + ',' + item.screen_name)
                f.write('\n'.join(map(str, my_friends)))
        except tweepy.RateLimitError:
            print(tweepy.RateLimitError(reason='Exceeded Twitter Rate Limit'))
        except BaseException as e:
            print(e)

    @staticmethod
    def compare_followers():
        """
        compare followers and friends list to see which friends don't follow back

        """
        friends_list = []
        follower_list = []
        baddies_list = []
        index = 0

        try:
            home = os.path.expanduser("~")
            config_file = (home + '/.packetqueue/' + str(globalVars.user.screen_name) + '/.no_follow')
            friends_file = (home + '/.packetqueue/' + str(globalVars.user.screen_name) + '/.friends')
            followers_file = (home + '/.packetqueue/' + str(globalVars.user.screen_name) + '/.followers')
            with open(friends_file, 'r') as friends, open(followers_file, 'r') as followers:
                for i in followers:
                    follower_list.append(i)
                for j in friends:
                    friend_id = j.split(',')
                    friends_list.append(friend_id[0] + '\n')
            with open(config_file, 'w') as baddies:
                for item in friends_list:
                    if item not in follower_list:
                        baddies_list.append(item)
                        index += 1
                baddies.write(''.join(map(str, baddies_list)))
        except tweepy.RateLimitError:
            print(tweepy.RateLimitError(reason='Exceeded Twitter Rate Limit'))
        except BaseException as e:
            print(e)

    @staticmethod
    def print_timeline(number: int):
        """
        print user's timeline

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

    @staticmethod
    def print_mentions(number: int):
        """
        print user's mentions

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

    @staticmethod
    def print_retweets(number: int):
        # Print user's tweets that others have retweeted
        """

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
                    # idName = globalVars.api.get_user(retweets.id_str)
                    # globalVars.screen.addstr(str(idName.screen_name))
                    globalVars.screen.addstr(str(retweets.id_str), curses.color_pair(1))
                    globalVars.screen.addstr(str(': ' + retweets.text + '\n'))
                globalVars.screen.refresh()
        except curses.error:
            # import pdb; pdb.set_trace()
            cleanup(1)

        finally:
            globalVars.screen.addstr('\n Press q to exit program...')
            while True:
                key = globalVars.screen.getch()
                if key == ord('q'):
                    cleanup(0)

    @staticmethod
    def show_my_info():
        """

        Print information about me

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

    @staticmethod
    def show_not_me(data: str):
        """

        Print information on another user

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

    @staticmethod
    def term_search(term):
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

    @staticmethod
    def direct_send(user, msg):
        """

        DEPRECATED NOW: Use CreateUpdate.direct_update going forward

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
        return None

    @staticmethod
    def status_update(text):
        """

        DEPRECATED NOW: Use CreateUpdate.update_status going forward

        :param text:
        :return:
        """
        if len(text) >= 140:
            print('Tweets must be 140 characters or less')
        else:
            globalVars.api.update_status(status=text)
            print('\nStatus "{}" updated successfully\n'.format(text))
        return None

    @staticmethod
    def get_stream():
        """

        """
        teren_stream = tweepy.Stream(globalVars.auth, Streamer())
        teren_stream.userstream()

    @staticmethod
    def get_follow_stream(user):
        """

        :param user:
        """
        teren_stream = tweepy.Stream(globalVars.auth, Streamer())
        get_user = globalVars.api.get_user(user)
        user_id = get_user.id
        user_id = str(user_id)
        if user_id != '17028130':
            teren_stream.filter(follow=[user_id])
        else:
            teren_stream.userstream()

    @staticmethod
    def get_stream_search(search_hash):
        """

        :param search_hash:
        """
        teren_stream = tweepy.Stream(globalVars.auth, Streamer())
        str1 = ''.join(search_hash)
        try:
            teren_stream.filter(track=[str1])
        except curses.error:
            cleanup(1)


def cleanup(exit_code: object, error=''):
    """

    :param exit_code:
    :param error:
    """
    curses.echo()
    curses.nocbreak()
    curses.endwin()
    if exit_code == 1:
        print('Egads, it looks like we shit the bed...')
        print(error)
        sys.exit(exit_code)
    else:
        sys.exit(exit_code)


class DisplayTweet(object):
    """

    prototype for an output class which would take in a tweet
    and output it in a certain format. Goal is to eliminate
    redundant code

        item_type = what type of display should this be: standard text, or curses
        tweet_text = text of whatever is to be displayed
    """

    def __init__(self, item_type, tweet_text):
        self.item_type = item_type
        self.tweet_text = tweet_text

    def regular_text(self):
        pass

    def curses_text(self):
        pass


class SaveTweet(object):
    """

    prototype for a save class to store various aspects of tweets
    in a variety of different files depending on type and need

        filename = file to save object data into
        file_contents = whatever text or data we're storing to file
    """

    def __init__(self, file_name, file_contents):
        self.file_name = file_name
        self.file_contents = file_contents


@initial_auth
class CreateUpdate:
    """

    class holder for various update methods

    """
    @staticmethod
    def direct_update(user: str, tweet_text: str):
        """

        :param user:
        :param tweet_text:

        """
        name_check = re.compile(r'(@)+')
        name_result = name_check.search(user)

        if len(tweet_text) >= 140:
            print('Tweets must be 140 characters or less')
        elif name_result is None:
            print('Incorrect username format (must include @)')
        else:
            globalVars.api.send_direct_message(screen_name=user, text=tweet_text)
            print('\nMessage "{}" sent to {} successfully\n'.format(tweet_text, user))
        return None

    @staticmethod
    def status_update(tweet_text: str):
        """

        :param tweet_text:

        """
        if len(tweet_text) >= 140:
            print('Tweets must be 140 characters or less')
        else:
            globalVars.api.update_status(status=tweet_text)
            print('\nStatus "{}" updated successfully\n'.format(tweet_text))

    def reply(self):
        pass


def main():
    pass
if __name__ == '__main__':
    main()
else:
    pass