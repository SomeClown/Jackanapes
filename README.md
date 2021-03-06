### Jackanapes - Another Command Line Twitter Utility # 
The primary goal of this project is to implement what I like to call "utility" functionality. In other
words, that functionality usually missing from mainstream clients, relegated to the realm of web-based for profit
applications. Functionality such as: comparing followers to friends, finding out how many users follow me but have 
not posted in some amount of time, pushing automatic updates from existing text files, bulk removal, add, etc. 
A secondary, and less important, goal of this project is to implement all functionality from the Twitter API via 
a traditional Unix interface, or at least to implement all useful mainstream functions, where they make sense.

While I personally use this application already, mostly for just streaming and searching my feed, I don't expect
anyone else to do the same. My only hope is that I get enough functionality built in that this application becomes
a useful utility for manipulating various aspects of an account in a way that is useful, free, and intuitive. Note
that this is a moving target, as I continue to find things to refactor, add, remove, or just add random comments
to.

Also, for more fully featured command-line clients, or at least ones with different approaches, take a look at:

* Python Twitter Tools: https://github.com/sixohsix/twitter/tree/master
* Rainbow Stream: https://github.com/DTVD/rainbowstream and the website at: http://www.rainbowstream.org/
* Turses: https://github.com/dialelo/turses
* Tweepy: https://github.com/tweepy/tweepy without which, this project would have been much more challenging to write

I'm sure there are more great examples out there, but those are the three I found when I was initially looking for
something like what I'm writing. All came close, and all are great in their own ways, but I wanted what I wanted, 
and it's been a fun exercise writing my own client. You are free to use this utility and code however you see fit,
but when you register it to Twitter in order to get your consumer/application keys/secrets, it would be lovely if
you kept the "jackanapes" name and point to the github repo at: https://github.com/SomeClown/Jackanapes. However, 
that is your choice.

Lastly, I welcome any and all contributions, pull requests, forks, comments, and suggestions.


NOTE: _Since rewriting the authentication methods, putting everything into a YAML file, the entire authorization module
is redundant and doing nothing except logging every call made to it, which of course is on every run since we're
wrapping all functions with that module/method. The only reason this is all still happening is because I want to
still utilize this method to generate the initial config.yml file, and to get user credentials in a more automatic
way. That said, since the user needs to register the application with their twitter dev account anyhow, I'm not
sure at this point if it's necessary. The bottom line is that I'm at a crossroads with this portion of the program,
and don't have a clear direction in my head just yet. Ideally, I'd have all of the inital credentials baked right
into the application, but as this is Python and I can't figure out how to hide those keys, it may not be something
that can be done as is. I'll likely end up rewriting this entire section of the program in pure C, which should
offer more flexibility and speed._


Installation:
1. CLone or download repo
2. Register application with Twitter and generate consumer/app tokens/keys
3. Copy example.yml to config.yml and edit as appropriate
4. In base directory, run "pip install -e ." to install the jackanapes binary into your (hopefully) virtualenv
5. "jackanapes" will start you off with a help message as below
6. Enjoy

I have also added a Dockerfile to the project. Example usage below:
1. docker build -t jackanapes .
2. docker run -t jackanapes --help

#### Command line Twitter (and stuff) client - For questions contact @SomeClown


```
Usage: jack [OPTIONS] COMMAND [ARGS]...
 
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
  long_status Long (greater than 140 characters) status update
  mentions    Get 'n' number of recent mentions
  retweets    Get 'n' number of recent retweets
  save        save full user objects to file
  sg          This searches for a particular search term...
  sl          This searches for a particular search term...
  spam        report and block user for spam
  status      send status update
  stream      Stream user's twitter feed
  tweets      Get 'n' number of recent tweets
 
NOTE: Help for all commands which have sub-commands can be seen by appending '--help' on the end of the command. For
example, you could say 'jack blocks --help' which would return the following:
        
        Options:
          -b, --block TEXT    block selected user
          -u, --unblock TEXT  unblock selected user
          -s, --show          show users being blocked
          -h, --help          Show this message and exit.

Search methods for all of the functions which allow search may be found in the table below.

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
