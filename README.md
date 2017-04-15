### Jackanapes - Another Command Line Twitter Utility # 
The primary goal of this project is to implement what I like to call "utility" functionality. In other
words, that functionality usually missing from mainstream clients, relegated to the realm of web-based for profit
applications. Functionality like comparing followers to friends, or how may users follow me but have not posted in
some amount of time, bulk removal, add, etc. A secondary goal of this project is to implement all functionality
from the Twitter API via a traditional Unix interface, or at least to implement all useful mainstream functions,
where they make sense.

While I personally use this application already, mostly for just streaming and searching my feed, I don't expect
anyone else to do the same. My only hope is that I get enough functionality built in that this application becomes
a useful utility for manipulating various aspects of an account in a way that is useful, free, and intuitive. Note
that this is a moving target, as I continue to find things to refactor, add, remove, or just add random comments
to.

Also, for more fully featured command-line clients, or at least ones with different approaches, take a look at:

* Python Twitter Tools: https://github.com/sixohsix/twitter/tree/master
* Rainbow Stream: https://github.com/DTVD/rainbowstream and the website at: http://www.rainbowstream.org/
* Turses: https://github.com/dialelo/turses

I'm sure there are more great examples out there, but those are the three I found when I was initially looking for
something like what I'm writing. All came close, and all are great in their own ways, but I wanted what I wanted, 
and it's been a fun exercise writing my own client.

Lastly, I welcome any and all contributions, pull requests, forks, comments, and suggestions.



#### Command line Twitter (and stuff) client - For questions contact @SomeClown


```
Usage: jackanapes [OPTIONS] COMMAND [ARGS]...
 
Options:
  -h, --help  Show this message and exit.
 
Commands:
  blocks      block/unblock users
  compare     various comparisons
  followers   save all followers to disk
  friend      Get 'n' list of friends
  friends     save all friends to disk
  friendship  follow/un-follow users
  info        information on yourself or others
  mentions    Get 'n' number of recent mentions
  retweets    Get 'n' number of recent retweets
  save        save full user objects to file
  sg          This searches for a particular search term...
  sl          This searches for a particular search term...
  spam        report and block user for spam
  status      send status update
  stream      Stream user's twitter feed
  testing     testing
  tweets      Get 'n' number of recent tweets

 
 

Operator                                Finds tweets…
----------------------------------------------------------------------------------------------------------------------- 
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
```
