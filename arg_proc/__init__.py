#!/usr/local/bin/python3

__author__ = 'SomeClown'

import curses
import tweepy

import globalVars
import Packet_Tweet



def arglebarg(command_args):
    """

    :return:
    :param command_args:
    :rtype: object

    """
    globalVars.screen = curses.initscr()

    # Get time line with 'n' number of tweets
    if command_args.tweetsNum:

        try:
            globalVars.screen.scrollok(True)
            curses.noecho()  # Keeps key presses from echoing to screen
            curses.cbreak()  # Takes input away
            globalVars.screen.keypad(1)
            curses.start_color()
            curses.use_default_colors()
            curses.init_pair(1, curses.COLOR_RED, -1)  # Foreground Red/background transparent
            Packet_Tweet.printTimeline(command_args.tweetsNum[0])
        except SystemExit:
            curses.endwin()
            raise
        except KeyboardInterrupt:
            curses.endwin()
            raise

    # Get mentions with 'n' number of tweets
    elif command_args.userMentions:

        try:
            globalVars.screen.scrollok(True)
            curses.noecho()  # Keeps key presses from echoing to screen
            curses.cbreak()  # Takes input away
            globalVars.screen.keypad(1)
            curses.start_color()
            curses.use_default_colors()
            curses.init_pair(1, curses.COLOR_RED, -1)  # Foreground Red/background transparent
            Packet_Tweet.printMentions(command_args.userMentions[0])
        except SystemExit:
            curses.endwin()
            raise
        except KeyboardInterrupt:
            curses.endwin()
            raise

    # Start stream on <@username>
    # If 'all' is put in place of username, stream user's home timeline
    elif command_args.streamUserSearch:

        try:
            globalVars.screen.scrollok(True)
            curses.noecho()  # Keeps key presses from echoing to screen
            curses.cbreak()  # Takes input away
            globalVars.screen.keypad(1)
            curses.start_color()
            curses.use_default_colors()
            curses.init_pair(1, curses.COLOR_RED, -1)  # Foreground Red/background transparent
            if 'all' in command_args.streamUserSearch:
                Packet_Tweet.getStream()
            else:
                screenName = command_args.streamUserSearch[0]
                getUser = globalVars.api.get_user(screenName)
                userID = getUser.id
                Packet_Tweet.getFollowStream(userID)
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

        try:
            globalVars.screen.scrollok(True)
            curses.noecho()  # Keeps key presses from echoing to screen
            curses.cbreak()  # Takes input away
            globalVars.screen.keypad(1)
            curses.start_color()
            curses.use_default_colors()
            curses.init_pair(1, curses.COLOR_RED, -1)  # Foreground Red/background transparent
            searchTerm = command_args.search
            Packet_Tweet.getStreamSearch(searchTerm)
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

        try:
            globalVars.screen.scrollok(True)
            curses.noecho()  # Keeps key presses from echoing to screen
            curses.cbreak()  # Takes input away
            globalVars.screen.keypad(1)
            curses.start_color()
            curses.use_default_colors()
            curses.init_pair(1, curses.COLOR_RED, -1)  # Foreground Red/background transparent
            Packet_Tweet.printFriends(command_args.numFriends[0])
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
        Packet_Tweet.directSend(userDirect, msgDirect)

    # update status
    elif command_args.statusUpdate:

        msgStatusUpdate = command_args.statusUpdate[0]
        Packet_Tweet.statusUpdate(msgStatusUpdate)

    elif command_args.myInfo:

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
            Packet_Tweet.printMyInfo()
        except SystemExit:
            curses.endwin()
            raise
        except KeyboardInterrupt:
            curses.endwin()
            raise

    elif command_args.notMe:
        try:
            globalVars.screen.scrollok(True)
            curses.noecho()
            curses.cbreak()
            globalVars.screen.keypad(1)
            curses.start_color()
            curses.use_default_colors()
            curses.init_pair(1, curses.COLOR_RED, -1)
            Packet_Tweet.printNotMe(command_args.notMe[0])
        except SystemExit:
            curses.endwin()
            raise
        except KeyboardInterrupt:
            curses.endwin()
            raise

    elif command_args.retweets:
        try:
            globalVars.screen.scrollok(True)
            curses.noecho()
            curses.cbreak()
            globalVars.screen.keypad(1)
            curses.start_color()
            curses.use_default_colors()
            curses.init_pair(1, curses.COLOR_RED, -1)
            Packet_Tweet.printRetweets(command_args.retweets[0])
        except SystemExit:
            curses.endwin()
            raise
        except KeyboardInterrupt:
            curses.endwin()
            raise

    elif command_args.term:
        try:
            globalVars.screen.scrollok(True)
            curses.noecho()
            curses.cbreak()
            globalVars.screen.keypad(1)
            curses.start_color()
            curses.use_default_colors()
            curses.init_pair(1, curses.COLOR_RED, -1)
            Packet_Tweet.termSearch(command_args.term)
        except SystemExit:
            curses.endwin()
            raise
        except KeyboardInterrupt:
            curses.endwin()
            raise

    else:
        return

    #return(command_args)

