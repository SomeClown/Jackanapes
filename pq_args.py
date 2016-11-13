#!/usr/local/bin/python3

import argparse
import helpText
import sys


def argumentsParsing(formatter_class=argparse.HelpFormatter):
    """

    :return:
    """
    progVersion = str('Alpha 0.1')

    ''' Suppressing help messages on all options below in favor of our own custom message contained
    in a different module that we import (helpText()) '''

    parser = argparse.ArgumentParser(description='Command line Twitter (and stuff) client',
                                     epilog='For questions contact @SomeClown',
                                     usage=helpText.helpText())

    parser.add_argument('-t', '--tweets', type=int, action='store', nargs=1, dest="tweetsNum", metavar='',
                        help=argparse.SUPPRESS)

    parser.add_argument('-s', '--stream', action='store', type=str, nargs=1, dest='streamUserSearch', metavar='',
                        help=argparse.SUPPRESS)

    parser.add_argument('-e', '--search', action='store', type=str, nargs='*', dest='search', metavar='',
                        help=argparse.SUPPRESS)

    parser.add_argument('-f', '--friends', action="store", type=int, nargs=1, dest='numFriends', metavar='',
                        help=argparse.SUPPRESS)

    parser.add_argument('-d', '--direct', nargs=2, action="store", type=str, metavar='', dest='directMessage',
                        help=argparse.SUPPRESS)

    parser.add_argument('-S', '--status', nargs=1, action="store", type=str, metavar='', dest='statusUpdate',
                        help=argparse.SUPPRESS)

    parser.add_argument('-m', '--mentions', type=int, nargs=1, action='store', metavar='', dest='userMentions',
                        help=argparse.SUPPRESS)

    parser.add_argument('-M', '--me', action='store_true', dest='myInfo', help=argparse.SUPPRESS)

    parser.add_argument('-n', '--notme', metavar='', action='store', dest='notMe', nargs=1, type=str,
                        help=argparse.SUPPRESS)

    parser.add_argument('-r', '--retweets', metavar='', action='store', dest='retweets', nargs=1, type=int,
                        help=argparse.SUPPRESS)

    parser.add_argument('-T', '--term', action='store', type=str, nargs=2, dest='term', metavar='',
                        help=argparse.SUPPRESS)

    parser.add_argument('-V', '--version', action='version', version=progVersion, help=argparse.SUPPRESS)

    parser.add_argument('-v', '--verbose', action='store_true', help=argparse.SUPPRESS)

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    else:
        my_command_args = parser.parse_args()

    assert isinstance(my_command_args, object)
    return my_command_args
