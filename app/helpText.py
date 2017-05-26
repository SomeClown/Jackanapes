#!/usr/bin/env python3
# coding=utf-8

__author__ = 'SomeClown'
__license__ = "MIT"
__maintainer__ = "Teren Bryson"
__email__ = "teren@packetqueue.net"


def help_text() -> object:

    """

    :return:
    """
    h = """\n usage: [program name] [options]

    optional arguments:

        -h, --help      show this help message and exit
            --friends   Get a list of all friends of specified user and dump to file
            --followers Get a list of all followers of specified user and dump to file
            --compare   Compare friends and followers to see who you follow and are not followed back
        -t              Get 'n' number of recent tweets from main feed <num>
        -s              Stream full user feed, or feed mentioning <user>
        -e              stream the global twitter feed by search term <search term>
        -f              print list of friends <num>
        -d              send a direct message <@user> <text>
        -S              update twitter status <text>
        -m              get mentions from logged in user's time line <num>
        -M              Get information about me
        -n              Get information about someone other than me <@user>
        -r              Get retweets of me by others <num>
        -T              search logged in user's time line for <phrase> <num>
            --version   show program's version number and exit
        -v, --verbose   verbose flag

    Operator								Finds tweets…
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
    puppy filter:images                     containing “puppy” and links identified as photos, including third parties such as Instagram.
    puppy filter:twimg                      containing “puppy” and a pic.twitter.comlink representing one or more photos.
    hilarious filter:links                  containing “hilarious” and linking to URL.
    superhero since:2015-12-21              containing “superhero” and sent since date “2015-12-21” (year-month-day).
    puppy until:2015-12-21                  containing “puppy” and sent before the date “2015-12-21”.
    movie -scary :)                         containing “movie”, but not “scary”, and with a positive attitude.
    flight :(                               containing “flight” and with a negative attitude.
    traffic ?                               containing “traffic” and asking a question.

    """
    return h