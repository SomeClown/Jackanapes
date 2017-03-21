#!/usr/local/bin/python3


import click
import Packet_Tweet


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


@click.command(help='Get \'n\' number of friends')
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


cli.add_command(init_friend_list, 'friends')
cli.add_command(init_time_line, 'tweets')
cli.add_command(init_mentions, 'mentions')
cli.add_command(init_retweets, 'retweets')

cli()
