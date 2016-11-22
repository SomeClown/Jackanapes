#!/usr/local/bin/python3

__author__ = 'SomeClown'

import argparse
import helpText
import sys


def argumentsParsing():
    """

    :return:
    """
    prog_version = str('Alpha 0.1')

    ''' Suppressing help messages on all options below in favor of our own custom message contained
    in a different module that we import (help_text()) '''

    parser = argparse.ArgumentParser(description='Command line Twitter (and stuff) client',
                                     epilog='For questions contact @SomeClown',
                                     usage=helpText.help_text())

    parser.add_argument('-t', '--tweets', type=int, action='store', nargs=1, dest="tweets_num", metavar='',
                        help=argparse.SUPPRESS)

    parser.add_argument('-s', action='store', type=str, nargs=1, dest='streamUserSearch', metavar='',
                        help=argparse.SUPPRESS)

    parser.add_argument('-e', action='store', type=str, nargs='*', dest='search', metavar='',
                        help=argparse.SUPPRESS)

    parser.add_argument('-f', action="store", type=int, nargs=1, dest='numFriends', metavar='',
                        help=argparse.SUPPRESS)

    parser.add_argument('-d', nargs=2, action="store", type=str, metavar='', dest='directMessage',
                        help=argparse.SUPPRESS)

    parser.add_argument('-S', nargs=1, action="store", type=str, metavar='', dest='status_update',
                        help=argparse.SUPPRESS)

    parser.add_argument('-m', type=int, nargs=1, action='store', metavar='', dest='userMentions',
                        help=argparse.SUPPRESS)

    parser.add_argument('-M', action='store_true', dest='myInfo', help=argparse.SUPPRESS)

    parser.add_argument('-n', metavar='', action='store', dest='notMe', nargs=1, type=str,
                        help=argparse.SUPPRESS)

    parser.add_argument('-r', metavar='', action='store', dest='retweets', nargs=1, type=int,
                        help=argparse.SUPPRESS)

    parser.add_argument('-T', action='store', type=str, nargs=2, dest='term', metavar='',
                        help=argparse.SUPPRESS)

    parser.add_argument('--version', action='version', version=prog_version, help=argparse.SUPPRESS)

    parser.add_argument('--followers', metavar='', action='store', nargs=1, type=str, dest='followers',
                        help=argparse.SUPPRESS)

    parser.add_argument('--friends', metavar='', action='store', nargs=1, type=str, dest='friends',
                        help=argparse.SUPPRESS)

    parser.add_argument('--compare', action='store', nargs=1, metavar='', dest='baddies',
                        help=argparse.SUPPRESS)

    parser.add_argument('-v', '--verbose', action='store_true', help=argparse.SUPPRESS)

    if len(sys.argv) == 1:
        print(helpText.help_text())
        #parser.print_help()
        sys.exit(0)

    else:
        my_command_args = parser.parse_args()

    assert isinstance(my_command_args, object)
    return my_command_args
