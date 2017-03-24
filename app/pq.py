#!/usr/local/bin/python3


import click
import Packet_Tweet
import globalVars


__author__ = 'SomeClown'

"""
Command Line Twitter Client
The goal of this project is to implement all functionality from the Twitter API via a traditional Unix interface.
"""

EPILOG = '... add search methods here. Need to overload class where Epilog is defined, to allow LF'


@click.group(chain=True, epilog=EPILOG)
def cli():
    """
    Command line Twitter (and stuff) client - For questions contact @SomeClown
    """


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

cli.add_command(init_friend_list, 'friends')
cli.add_command(init_time_line, 'tweets')
cli.add_command(init_mentions, 'mentions')
cli.add_command(init_retweets, 'retweets')
cli.add_command(init_followers, 'followers')
cli.add_command(init_stream, 'stream')
cli.add_command(init_status, 'status')
cli.add_command(init_info, 'info')

cli()
