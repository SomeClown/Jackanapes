# Command Line Twitter Client #
## The goal of this project is to implement all functionality from the Twitter API via a traditional Unix interface. ##

Command line Twitter (and stuff) client
For questions contact @SomeClown

usage: [program name] [options]

optional arguments:

	-h, --help      show this help message and exit
	-t, --tweets    Get 'n' number of recent tweets from main feed
	-s, --stream    Stream full user feed, or feed mentioning <user>
	-e, --search    stream the global twitter feed by search term
	-f, --friends   print list of friends
	-d, --direct	send a direct message
	-S, --status    update twitter status
	-m, --mentions  get mentions from logged in user's timeline
	-M, --me        Get information about me
	-n, --notme     Get information about someone other than me
	-r, --retweets  Get retweets of me by others
	-V, --version   show program's version number and exit
	-v, --verbose   verbose flag

Operator                                Finds tweets…

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
