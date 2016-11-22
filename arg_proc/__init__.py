#!/usr/local/bin/python3

__author__ = 'SomeClown'

import curses
import tweepy
import globalVars
import Packet_Tweet

"""

All of the logic for the program goes here. pq.py calls pq_args which is where we set up
the parser. The parser then passes back to this file the options selected, where the appropriate
stanza is executed. The execution logic takes place in Packet_Tweet, where each function is also
wrapped with the authorization function.

"""


def arglebarg(command_args):
    """

    :type command_args: object
    :type command_args: object
    :return:
    :param command_args:
    :rtype: object

    """
    if command_args.followers:
        #user = '@someclown'
        try:
            Packet_Tweet.savefollowers(command_args.followers[0])
        except SystemExit:
            raise
        except KeyboardInterrupt:
            raise


    if command_args.friends:
        try:
            Packet_Tweet.savefriends(command_args.friends[0])
        except SystemExit:
            raise
        except KeyboardInterrupt:
            raise

    if command_args.baddies:
        try:
            Packet_Tweet.comparefollowers(command_args.baddies[0])
        except SystemExit:
            raise
        except KeyboardInterrupt:
            raise

    # Get time line with 'n' number of tweets
    elif command_args.tweets_num:
        globalVars.screen = curses.initscr()
        try:
            globalVars.screen.scrollok(True)
            curses.noecho()  # Keeps key presses from echoing to screen
            curses.cbreak()  # Takes input away
            globalVars.screen.keypad(1)
            curses.start_color()
            curses.use_default_colors()
            curses.init_pair(1, curses.COLOR_RED, -1)  # Foreground Red/background transparent
            Packet_Tweet.printtimeline(command_args.tweets_num[0])
        except SystemExit:
            curses.endwin()
            raise
        except KeyboardInterrupt:
            curses.endwin()
            raise

    # Get mentions with 'n' number of tweets
    elif command_args.userMentions:
        globalVars.screen = curses.initscr()
        try:
            globalVars.screen.scrollok(True)
            curses.noecho()  # Keeps key presses from echoing to screen
            curses.cbreak()  # Takes input away
            globalVars.screen.keypad(1)
            curses.start_color()
            curses.use_default_colors()
            curses.init_pair(1, curses.COLOR_RED, -1)  # Foreground Red/background transparent
            Packet_Tweet.printmentions(command_args.userMentions[0])
        except SystemExit:
            curses.endwin()
            raise
        except KeyboardInterrupt:
            curses.endwin()
            raise

    # Start stream on <@username>
    # If 'all' is put in place of username, stream user's home timeline
    elif command_args.streamUserSearch:
        globalVars.screen = curses.initscr()
        try:
            globalVars.screen.scrollok(True)
            curses.noecho()  # Keeps key presses from echoing to screen
            curses.cbreak()  # Takes input away
            globalVars.screen.keypad(1)
            curses.start_color()
            curses.use_default_colors()
            curses.init_pair(1, curses.COLOR_RED, -1)  # Foreground Red/background transparent
            if 'all' in command_args.streamUserSearch:
                Packet_Tweet.get_stream()
            else:
                screen_name = command_args.streamUserSearch[0]
                get_user = globalVars.api.get_user(screen_name)
                user_id = get_user.id
                Packet_Tweet.get_follow_stream(user_id)
        except tweepy.TweepError as e:
            curses.endwin()
            print(e.response)  # This works
        except SystemExit:
            curses.endwin()
            raise
        except KeyboardInterrupt:
            curses.endwin()
            raise

    # Start stream using <search term>
    elif command_args.search:
        globalVars.screen = curses.initscr()
        try:
            globalVars.screen.scrollok(True)
            curses.noecho()  # Keeps key presses from echoing to screen
            curses.cbreak()  # Takes input away
            globalVars.screen.keypad(1)
            curses.start_color()
            curses.use_default_colors()
            curses.init_pair(1, curses.COLOR_RED, -1)  # Foreground Red/background transparent
            searchTerm = command_args.search
            Packet_Tweet.get_stream_search(searchTerm)
        except tweepy.TweepError:
            curses.endwin()
            print(tweepy.TweepError)
        except SystemExit:
            curses.endwin()
            raise
        except KeyboardInterrupt:
            curses.endwin()
            raise

    # Print <n> number of friends to screen, where <n> is less than Titter max limit
    elif command_args.numFriends:
        globalVars.screen = curses.initscr()
        try:
            globalVars.screen.scrollok(True)
            curses.noecho()  # Keeps key presses from echoing to screen
            curses.cbreak()  # Takes input away
            globalVars.screen.keypad(1)
            curses.start_color()
            curses.use_default_colors()
            curses.init_pair(1, curses.COLOR_RED, -1)  # Foreground Red/background transparent
            Packet_Tweet.printfriends(command_args.numFriends[0])
        except SystemExit:
            curses.endwin()
            raise
        except KeyboardInterrupt:
            curses.endwin()
            raise

    # send a direct message
    elif command_args.directMessage:

        userDirect = command_args.directMessage[0]
        msgDirect = command_args.directMessage[1]
        Packet_Tweet.direct_send(userDirect, msgDirect)

    # update status
    elif command_args.status_update:

        msg_status_update = command_args.status_update[0]
        Packet_Tweet.status_update(msg_status_update)

    elif command_args.myInfo:
        globalVars.screen = curses.initscr()
        try:
            globalVars.screen.scrollok(True)
            curses.noecho()  # Keeps key presses from echoing to screen
            curses.cbreak()  # Takes input away
            globalVars.screen.keypad(1)
            curses.start_color()
            curses.use_default_colors()
            curses.init_pair(1, curses.COLOR_RED, -1)  # Foreground Red/background transparent
            curses.init_pair(2, curses.COLOR_YELLOW, -1)
            curses.init_pair(3, curses.COLOR_BLUE, -1)
            curses.init_pair(5, curses.COLOR_MAGENTA, -1)
            Packet_Tweet.print_my_info()
        except SystemExit:
            curses.endwin()
            raise
        except KeyboardInterrupt:
            curses.endwin()
            raise

    elif command_args.notMe:
        globalVars.screen = curses.initscr()
        try:
            globalVars.screen.scrollok(True)
            curses.noecho()
            curses.cbreak()
            globalVars.screen.keypad(1)
            curses.start_color()
            curses.use_default_colors()
            curses.init_pair(1, curses.COLOR_RED, -1)
            Packet_Tweet.print_not_me(command_args.notMe[0])
        except SystemExit:
            curses.endwin()
            raise
        except KeyboardInterrupt:
            curses.endwin()
            raise

    elif command_args.retweets:
        globalVars.screen = curses.initscr()
        try:
            globalVars.screen.scrollok(True)
            curses.noecho()
            curses.cbreak()
            globalVars.screen.keypad(1)
            curses.start_color()
            curses.use_default_colors()
            curses.init_pair(1, curses.COLOR_RED, -1)
            Packet_Tweet.print_retweets(command_args.retweets[0])
        except SystemExit:
            curses.endwin()
            raise
        except KeyboardInterrupt:
            curses.endwin()
            raise

    elif command_args.term:
        globalVars.screen = curses.initscr()
        try:
            globalVars.screen.scrollok(True)
            curses.noecho()
            curses.cbreak()
            globalVars.screen.keypad(1)
            curses.start_color()
            curses.use_default_colors()
            curses.init_pair(1, curses.COLOR_RED, -1)
            Packet_Tweet.term_search(command_args.term)
        except SystemExit:
            curses.endwin()
            raise
        except KeyboardInterrupt:
            curses.endwin()
            raise


    else:
        return

        # return(command_args)
