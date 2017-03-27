#!/usr/local/bin/python3


import click
import Packet_Tweet
import globalVars
import yaml

__author__ = 'SomeClown'

"""
Command Line Twitter Client
The goal of this project is to implement all functionality from the Twitter API via a traditional Unix interface.
"""

EPILOG = '... add search methods here. Need to overload class where Epilog is defined, to allow LF'

"""
    \n
    \b
SEARCH OPERATOR                         FINDS
-----------------------------------------------------------------------------------------------------------
watching now                            containing both “watching” and “now”. This is the default operator.
“happy hour”                            containing the exact phrase “happy hour”.
love OR hate                            containing either “love” or “hate” (or both).
beer -root                              containing “beer” but not “root”.
#haiku                                  containing the hashtag “haiku”.
from:interior                           sent from Twitter account “interior”.
list:NASA/astronauts-in-space-now       sent from a Twitter account in the NASA list astronauts-in-space-now
to:NASA                                 a Tweet authored in reply to Twitter account “NASA”.
@NASA                                   mentioning Twitter account “NASA”.
politics filter:safe                    containing “politics” with Tweets marked as potentially sensitive removed.
puppy filter:media                      containing “puppy” and an image or video.
puppy filter:native_video               containing “puppy” and an uploaded video, Amplify video, Periscope, or Vine.
puppy filter:periscope                  containing “puppy” and a Periscope video URL.
puppy filter:vine                       containing “puppy” and a Vine.
puppy filter:images                     containing “puppy” and links identified as photos, including third parties
                                        such as Instagram.
puppy filter:twimg                      containing “puppy” and a pic.twitter.comlink representing one or more photos.
hilarious filter:links                  containing “hilarious” and linking to URL.
superhero since:2015-12-21              containing “superhero” and sent since date “2015-12-21” (year-month-day).
puppy until:2015-12-21                  containing “puppy” and sent before the date “2015-12-21”.
movie -scary :)                         containing “movie”, but not “scary”, and with a positive attitude.
flight :(                               containing “flight” and with a negative attitude.
traffic ?                               containing “traffic” and asking a question.
\n
"""

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


def set_config():

    # Load and assign key variables from yaml configuration file
    my_config_file = open('config.yml')
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


@click.group(epilog=EPILOG, context_settings=CONTEXT_SETTINGS)
def cli():
    """
    Command line Twitter (and stuff) client - For questions contact @SomeClown
    """
    set_config()


@click.command(help='Get \'n\' list of friends')
@click.argument('number', default=10)
def init_friend_list(number):
    try:
        Packet_Tweet.init_curses()
        run_friends = Packet_Tweet.TweetArguments()
        run_friends.print_friends(number)
    except SystemExit:
        raise
    except KeyboardInterrupt:
        raise
    except BaseException as e:
        print(e)


@click.command(help='Get \'n\' number of recent tweets')
@click.argument('number', default=10)
def init_time_line(number):
    try:
        Packet_Tweet.init_curses()
        time_line = Packet_Tweet.TweetArguments()
        time_line.print_timeline(number)
    except SystemExit:
        raise
    except KeyboardInterrupt:
        raise
    except BaseException as e:
        print(e)


@click.command(help='Get \'n\' number of recent mentions')
@click.argument('number', default=10)
def init_mentions(number):
    try:
        Packet_Tweet.init_curses()
        mentions = Packet_Tweet.TweetArguments()
        mentions.print_mentions(number)
    except SystemExit:
        raise
    except KeyboardInterrupt:
        raise
    except BaseException as e:
        print(e)


@click.command(help='Get \'n\' number of recent retweets')
@click.argument('number', default=10)
def init_retweets(number):
    try:
        Packet_Tweet.init_curses()
        retweets = Packet_Tweet.TweetArguments()
        retweets.print_retweets(number)
    except SystemExit:
        raise
    except KeyboardInterrupt:
        raise
    except BaseException as e:
        print(e)


@click.command(help='Get \'n\' list of followers')
@click.argument('number', default=10)
def init_followers(number):
    try:
        Packet_Tweet.init_curses()
        followers = Packet_Tweet.TweetArguments()
        followers.show_followers(number)
    except SystemExit:
        raise
    except KeyboardInterrupt:
        raise
    except BaseException as e:
        print(e)


@click.command(help='Stream user\'s twitter feed')
@click.argument('user', default='')
def init_stream(user):
    try:
        Packet_Tweet.init_curses()
        user_stream = Packet_Tweet.TweetArguments()
        user_stream.get_follow_stream(user)
    except SystemExit:
        raise
    except KeyboardInterrupt:
        raise
    except BaseException as e:
        print(e)
        Packet_Tweet.cleanup(1, e)


@click.command(help='information on yourself or others')
@click.option('-m', '--me', 'me', is_flag=True, help='me')
@click.option('-n', '--not', 'not_me', help='Not Me')
def init_info(me, not_me=''):
    if me:
        try:
            Packet_Tweet.init_curses()
            really_me = Packet_Tweet.TweetArguments()
            really_me.show_my_info()
        finally:
            pass
    if not_me:
        try:
            Packet_Tweet.init_curses()
            really_not_me = Packet_Tweet.TweetArguments()
            really_not_me.show_not_me(not_me)
        finally:
            pass


@click.command(help='send status update')
@click.argument('user')
@click.argument('status', default='...forgot status...')
@click.option('--direct', '-d', 'direct', is_flag=True, help='send direct message')
def init_status(direct, user, status):
    if direct is True:
        try:
            update = Packet_Tweet.CreateUpdate()
            update.direct_update(user, status)
        except BaseException as e:
            print(e)
    else:
        try:
            update = Packet_Tweet.CreateUpdate()
            update.status_update(status)
        except BaseException as e:
            print(e)


@click.command(options_metavar='[options]')
@click.argument('search_term', metavar='[search term]')
@click.argument('count', nargs=1, required=False, metavar='[number of items]')
@click.option('--static/--stream', default=True, help='Static or streaming search')
def init_search_global(static, search_term, count=10):
    """ \b
        This searches for a particular search term within the global
        twitter feed, and either displays [count] number of items, or
        streams in real-time.

        \n
        \b
SEARCH OPERATOR                         FINDS
-----------------------------------------------------------------------------------------------------------
watching now                            containing both “watching” and “now”. This is the default operator.
“happy hour”                            containing the exact phrase “happy hour”.
love OR hate                            containing either “love” or “hate” (or both).
beer -root                              containing “beer” but not “root”.
#haiku                                  containing the hashtag “haiku”.
from:interior                           sent from Twitter account “interior”.
list:NASA/astronauts-in-space-now       sent from a Twitter account in the NASA list astronauts-in-space-now
to:NASA                                 a Tweet authored in reply to Twitter account “NASA”.
@NASA                                   mentioning Twitter account “NASA”.
politics filter:safe                    containing “politics” with Tweets marked as potentially sensitive removed.
puppy filter:media                      containing “puppy” and an image or video.
puppy filter:native_video               containing “puppy” and an uploaded video, Amplify video, Periscope, or Vine.
puppy filter:periscope                  containing “puppy” and a Periscope video URL.
puppy filter:vine                       containing “puppy” and a Vine.
puppy filter:images                     containing “puppy” and links identified as photos, including third parties
                                        such as Instagram.
puppy filter:twimg                      containing “puppy” and a pic.twitter.comlink representing one or more photos.
hilarious filter:links                  containing “hilarious” and linking to URL.
superhero since:2015-12-21              containing “superhero” and sent since date “2015-12-21” (year-month-day).
puppy until:2015-12-21                  containing “puppy” and sent before the date “2015-12-21”.
movie -scary :)                         containing “movie”, but not “scary”, and with a positive attitude.
flight :(                               containing “flight” and with a negative attitude.
traffic ?                               containing “traffic” and asking a question.
\n
    """
    if static is True:
        try:
            Packet_Tweet.init_curses()
            this_search = Packet_Tweet.TweetArguments()
            this_search.term_search(search_term, count)
        finally:
            print(static)
            print(search_term)
            print(count)
    elif static is False:
        try:
            Packet_Tweet.init_curses()
            stream_search = Packet_Tweet.TweetArguments()
            stream_search.get_stream_search(search_term)
        finally:
            print(static)
            print(search_term)
            print(count)


@click.command(options_metavar='[options]')
@click.argument('search_term', metavar='[search term]')
@click.argument('count', nargs=1, required=False, metavar='[number of items]')
@click.option('--static/--stream', default=True, help='Static or streaming search')
def init_search_local(static, search_term, count=10):
    """ \b
            This searches for a particular search term within the user's
            twitter feed, and either displays [count] number of items, or
            streams in real-time.

        \n
        \b
SEARCH OPERATOR                         FINDS
-----------------------------------------------------------------------------------------------------------
watching now                            containing both “watching” and “now”. This is the default operator.
“happy hour”                            containing the exact phrase “happy hour”.
love OR hate                            containing either “love” or “hate” (or both).
beer -root                              containing “beer” but not “root”.
#haiku                                  containing the hashtag “haiku”.
from:interior                           sent from Twitter account “interior”.
list:NASA/astronauts-in-space-now       sent from a Twitter account in the NASA list astronauts-in-space-now
to:NASA                                 a Tweet authored in reply to Twitter account “NASA”.
@NASA                                   mentioning Twitter account “NASA”.
politics filter:safe                    containing “politics” with Tweets marked as potentially sensitive removed.
puppy filter:media                      containing “puppy” and an image or video.
puppy filter:native_video               containing “puppy” and an uploaded video, Amplify video, Periscope, or Vine.
puppy filter:periscope                  containing “puppy” and a Periscope video URL.
puppy filter:vine                       containing “puppy” and a Vine.
puppy filter:images                     containing “puppy” and links identified as photos, including third parties
                                        such as Instagram.
puppy filter:twimg                      containing “puppy” and a pic.twitter.comlink representing one or more photos.
hilarious filter:links                  containing “hilarious” and linking to URL.
superhero since:2015-12-21              containing “superhero” and sent since date “2015-12-21” (year-month-day).
puppy until:2015-12-21                  containing “puppy” and sent before the date “2015-12-21”.
movie -scary :)                         containing “movie”, but not “scary”, and with a positive attitude.
flight :(                               containing “flight” and with a negative attitude.
traffic ?                               containing “traffic” and asking a question.
\n
        """
    pass


@click.command(options_metavar='[options]', short_help='save all friends to disk')
@click.argument('user_username', metavar='[twitter user name]')
def init_friends(user_username):
    """ \b
        This will download all of your friends (the people you follow) and
        store the results by user_id in a file, by default called .friends
        and located in the application directory for the user.
    """
    friends = Packet_Tweet.TweetArguments()
    friends.save_friends(user_username)


@click.command(options_metavar='[options]', short_help='save all followers to disk')
@click.argument('user_username', metavar='[twitter user name]')
def init_followers(user_username):
    """ \b
       This will download all of your followers (the people following you) and
       store the results by user_id in a file, by default called .followers
       and located in the application directory for the user.
    """
    followers = Packet_Tweet.TweetArguments()
    followers.save_followers(user_username)


@click.command(options_metavar='[options]', short_help='various comparisons')
@click.option('-m', '--me', 'me', is_flag=True, help='add some help here')
@click.option('-u', '--user', 'user', help='add some help here')
@click.option('-f', '--file', 'file', is_flag=True, help='add some help here')
def init_compare(me, user, file=''):
    """ \b
        This method makes various comparisons, based on input, between the local user
        and the various followers and friends they have; comparisons such as whether or
        not the people they follow follow them back. This is useful for account pruning.
    """
    compare = Packet_Tweet.TweetArguments()
    if me is True:
        compare.compare_users('someclown')
    elif user:
        compare.compare_users(user)
    elif file:
        compare.compare_followers()


@click.command(options_metavar='[options]', short_help='save full user objects to file')
def init_save_objects():
    save_objects = Packet_Tweet.TweetArguments()
    save_objects.grab_user_object('/Users/brysont/.packetqueue/SomeClown/.followers')

cli.add_command(init_friend_list, 'friend')
cli.add_command(init_time_line, 'tweets')
cli.add_command(init_mentions, 'mentions')
cli.add_command(init_retweets, 'retweets')
cli.add_command(init_followers, 'followers')
cli.add_command(init_stream, 'stream')
cli.add_command(init_status, 'status')
cli.add_command(init_info, 'info')
cli.add_command(init_search_global, 'sg')
cli.add_command(init_search_local, 'sl')
cli.add_command(init_friends, 'friends')
cli.add_command(init_followers, 'followers')
cli.add_command(init_compare, 'compare')
cli.add_command(init_save_objects, 'save')

cli()
