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
import tweepy
import click
import pickle
import json

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
        followers_count = globalVars.user_id.followers_count
        save_followers = []
        try:
            cursor = tweepy.Cursor(globalVars.api.followers_ids, screen_name=my_screen_name, cursor=-1,
                                   wait_on_rate_limit=True, wait_on_rate_limit_notify=True, compression=True,
                                   skip_status=True, include_user_entities=False, count=5000)
            print('\n ', my_screen_name, 'has: ', followers_count, 'followers ')
            config_file = (globalVars.complete_dir_path + '/.followers')
            with open(config_file, 'w') as f:
                for page in cursor.pages():
                    for item in page:
                        save_followers.append(item)
                f.write('\n'.join(map(str, save_followers)))
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
        friends_count = globalVars.user_id.friends_count
        my_friends = []
        try:
            cursor = tweepy.Cursor(globalVars.api.friends, screen_name=my_screen_name, cursor=-1,
                                   wait_on_rate_limit=True, wait_on_rate_limit_notify=True, compression=True,
                                   skip_status=True, include_user_entities=False, count=200)
            print('\n ', my_screen_name, 'has: ', friends_count, 'friends ')
            config_file = (globalVars.complete_dir_path + '/.friends')
            with open(config_file, 'w') as f:
                for page in cursor.pages():
                    with click.progressbar(page, label='downloading friends list') as outer_items:
                        for item in outer_items:
                            my_friends.append(str(item.id))
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
        # TODO: Change this entire block to use a "set" comparison for better readability and efficiency
        try:
            config_file = (globalVars.complete_dir_path + '/.no_follow')
            friends_file = (globalVars.complete_dir_path + '/.friends')
            followers_file = (globalVars.complete_dir_path + '/.followers')
            print(followers_file)
            with open(friends_file, 'r') as friends, open(followers_file, 'r') as followers:
                for i in followers:
                    follower_list.append(i)
                for j in friends:
                    friends_list.append(j)
            with open(config_file, 'w') as baddies:
                with click.progressbar(friends_list, label='comparing friends/followers') as outer_items:
                        for item in outer_items:
                            if item not in follower_list:
                                baddies_list.append(item)
                                index += 1
                baddies.write(''.join(map(str, baddies_list)))
        except tweepy.RateLimitError:
            print(tweepy.RateLimitError(reason='Exceeded Twitter Rate Limit'))
        except BaseException as e:
            print(e)

    @staticmethod
    def grab_user_object(file_name):
        """
        
        takes a file of twitter user_ids as input, retrieves the complete user objects
        of each one, then stores the resulting objects as a list in binary form on disk.
        The resulting file is named after the original file, but with '_blob' at the end.
        
        :param file_name: 
        :return: 
        """
        raw_ids = []
        complete_file = os.path.join(globalVars.complete_dir_path, file_name)
        out_file = complete_file + '_blob'
        try:
            with open(complete_file, 'r') as f:
                for line in f:
                    raw_ids.append(line.strip('\n'))
            composite_ids = [raw_ids[x:x+99] for x in range(0, len(raw_ids), 99)]
            full_user_objects = []
            with click.progressbar(composite_ids, label='grabbing user objects') as outer_list_item:
                for item in outer_list_item:
                    full_user_objects.append(globalVars.api.lookup_users(user_ids=item))
            with open(out_file, 'wb') as g:
                pickle.dump(full_user_objects, g)
        except BaseException as e:
            print(e)

    @staticmethod
    def print_time_line(number: int):
        """
        print user's time_line

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
        """
        
        print user's tweets which have been re_tweeted by others

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
                for thing in other_retweets:
                    foo = globalVars.api.retweets(thing.id_str)
                    bar = foo[0]
                    globalVars.screen.addstr(bar._json['user']['name'], curses.color_pair(1))
                    globalVars.screen.addstr(': ' + bar._json['text'] + '\n')
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
    def compare_users(user, compare_date=0, num=0):
        """

        Comparison method. This is where we'll take in user arguments to return
        data such as: how long since a given user tweeted, or how many followers
        do they have, etc.

        :param user:
        :param compare_date:
        :param num:
        :return:
        """
        user_info = globalVars.api.get_user(user)
        print(user_info.followers_count)
        print(user_info.statuses_count)
        print(user_info.created_at)

    @staticmethod
    def term_search(term, tweet_count):
        """

        :param term:
        :param tweet_count:
        :return:
        """
        # cursor = tweepy.Cursor(globalVars.api.search, q=term).items(count)
        try:
            item = globalVars.api.search(q=term, count=tweet_count)
            for tweet in item:
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
    def status_update(user, msg):
        """

        DEPRECATED NOW: Use CreateUpdate.update_status going forward

        :param user: not used here, included for consistency
        :param msg:
        :return:
        """
        if len(msg) >= 140:
            print('Tweets must be 140 characters or less')
        else:
            globalVars.api.update_status(status=msg)
            print('\nStatus "{}" updated successfully\n'.format(msg))
        return None

    @staticmethod
    def friendship_follow(screen_name=''):
        """
        
        Follow a user
        
        :param screen_name:
        :return: 
        """
        try:
            new_name = ('@' + globalVars.user)
            print(new_name)
            globalVars.api.create_friendship(screen_name)
            friend_tuple = globalVars.api.show_friendship(target_screen_name=new_name,
                                                          source_screen_name=screen_name)
            if friend_tuple[1].following is True:
                print('Successfully followed ' + screen_name)
            elif friend_tuple[1].following is False:
                print('WTF? SHIT THE BED!')
        except tweepy.TweepError as e:
            print('Something went wrong...')
            print(e)
        except BaseException as e:
            print(e)

    @staticmethod
    def friendship_un_follow(screen_name=''):
        """
        
        Un-follow a user
        
        :param screen_name: 
        :return: 
        """
        try:
            new_name = ('@' + globalVars.user)
            globalVars.api.destroy_friendship(screen_name)
            friend_tuple = globalVars.api.show_friendship(target_screen_name=new_name,
                                                 source_screen_name=screen_name)
            if friend_tuple[1].following is False:
                print('Successfully un-followed ' + screen_name)
            elif friend_tuple[1].following is True:
                print('WTF? SHIT THE BED!')
        except tweepy.TweepError as e:
            print('Something went wrong...')
            print(e)
        except BaseException as e:
            print(e)

    @staticmethod
    def user_block(screen_name=''):
        """
        
        Block a user
        
        :param screen_name: 
        :return: 
        """
        try:
            globalVars.api.create_block(screen_name)
        except tweepy.TweepError as e:
            print('Something went wrong')
            print(e)
        except BaseException as e:
            print(e)

    @staticmethod
    def user_unblock(screen_name=''):
        """
        
        Unblock a user
        
        :param screen_name: 
        :return: 
        """
        try:
            globalVars.api.destroy_block(screen_name)
        except tweepy.TweepError as e:
            print('Something went wrong')
            print(e)
        except BaseException as e:
            print(e)

    @staticmethod
    def show_blocks():
        """
        Show all users currently being blocked
        
        :param screen_name: 
        :return: 
        """
        try:
            blocks = globalVars.api.blocks()
            length = len(blocks)
            n = 0
            print('\n')
            while n <= length - 1:
                print(blocks[n].screen_name + ' (' + blocks[n].name + ')')
                n = n + 1
            print('\n' + str(n) + ' blocked users\n')

        except tweepy.TweepError as e:
            print('Something went wrong')
            print(e)
        except BaseException as e:
            print(e)

    @staticmethod
    def set_spam(screen_name):
        """
        
        Report user for spam, and block
        
        :param screen_name: 
        :return: 
        """
        try:
            globalVars.api.report_spam(screen_name)
        except tweepy.TweepError as e:
            print('Something went wrong. This usually means the specified user doesn\'t exist')
            print(e)

        except BaseException as e:
            print(e)

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

    @staticmethod
    def set_testing():
        test_pull = globalVars.api.retweets_of_me(counts=1)
        try:
            for thing in test_pull:
                foo = globalVars.api.retweets(thing.id_str)
                bar = foo[0]
                print(bar._json['user']['name'] + ': ' + bar._json['text'])
                #print(json.dumps(bar._json, indent=5))

        except tweepy.TweepError as e:
            print(e)


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
            print('Tweets must be 140 characters or less. Your tweet is ' + str(len(tweet_text)))
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
