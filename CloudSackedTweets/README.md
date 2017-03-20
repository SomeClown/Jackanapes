### Command Line Twitter Client #
The primary goal of this project is to implement what I like to call "utility" functionality. In other
words, that functionality usually missing from mainstream clients, relegated to the realm of web-based for profit
applications. Functionality like comparing followers to friends, or how may users follow me but have not posted in
some amount of time, bulk removal, add, etc. A secondary goal of this project is to implement all functionality
from the Twitter API via a traditional Unix interface, or at least to implement all useful mainstream functions,
where they make sense.

The to do list is growing by the day, as is the bugs list. I welcome all suggestions for features and/or improvements
to the program, as I want this to be as functional and stable as possible. One area where I could really use some
help is in developing tests and improving stability. I'd like to build a comprehensive test suite for each and every
class, function, etc. in the application. I'd also like robust logging and graceful crash recovery. I've come a long
way since my initial commit, but it's not even close to where I feel comfortable with where I am in the development
cycle.

While I personally use this application already, mostly for just streaming and searching my feed, I don't expect
anyone else to do the same. My only hope is that I get enough functionality built in that this application becomes
a useful utility for manipulating various aspects of an account in a way that is useful, free, and intuitive.

#### Command line Twitter (and stuff) client - For questions contact @SomeClown

usage: [program name] [options]

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
        -m              get mentions from logged in user's timeline <num>
        -M              Get information about me
        -n              Get information about someone other than me <@user>
        -r              Get retweets of me by others <num>
        -T              search logged in user's timeline for <phrase> <num>
            --version   show program's version number and exit
        -v, --verbose   verbose flag
```
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
```