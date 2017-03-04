## To do list for the command line client

- [ ] Use tweet_id (or something) to restructure tweet stream to incorporate the history with the tweet (replied to, etc.)
        In other words, show replies inline with the stream. Make this a selectable option at invocation
- [ ] Rewrite code for config file using ConfigParser module from standard library
	- [ ] Add current functionality to pull oauth keys
	- [ ] Add additional functionality for colors, curses-based vs. standard text, etc.
- [ ] Add database functionality (or flat file, as appropriate)
	- [X] Store friends list (use ID)
	- [ ] Store cursor for later recall of where we were in the stream when last ran
	- [ ] Look into something like tinydb to see if appropriate as longer term storage vs. flat files
- [ ] Fix progress bar for oauth authentication, as well as for large data pulls (friends lists, etc.)
- [ ] Rewrite portions of code to allow for threading (use standard library's threading module)
	- [ ] At least separate keyboard controls into separate thread to allow for mid-stream manipulation of searches, etc.
- [ ] Add colorization to hashtags both in streams and in static data pulls
- [ ] Add ability to search and add/remove followers based on different criteria such as: number of tweets, followers, etc.
- [ ] Add pause feature to streaming, or long, outputs
- [ ] Add scrollbar functionality (ability to scroll backward in curses.) Use pad.
- [ ] Move logging file(s) to file directory, not current working directory
- [ ] Add setup function to do initial checks of configs, and setup if not ran before (oauth tokens, create logging
        directory, read configuration from file, etc.)
- [ ] Add functionality to allow streaming in background, wait for keystrokes, and exit or change stream conditions
- [ ] Follow user
- [ ] Un-follow user
- [ ] Find user in friends list (direct search, and regex)
- [ ] Find user in followers list (direct search, and regex)
- [ ] Mute user
- [ ] Un-mute user
- [ ] Add threading to time line search, streaming APIs, etc.
- [ ] Show direct messages to authenticated user
- [ ] User manipulation based on metrics
    - [ ] Function to create list of users who I follow but who don't follow me back
    - [ ] Function to create list of users who I follow but who have less than <n> followers themselves
    - [ ] Function to create list of users ranked based on activity (last time posted, "dead" users, etc.)
    - [ ] Function to remove/manipulate users in bulk based on lists/criteria above
    - [ ] Create logging function to track all activity above, along with "roll-back" option of some sort
- [ ] Abstract all areas where username and path are hardcoded
    - [ ] Remove '@someclown' from code, replace with function to select user
    - [ ] Cleanup path objects, abstract for any user
    - [ ] Allow user selection at startup
- [ ] Change/add/fix argparse functionality to allow for multiple arguments/flags for same command (in other words,
        maybe I'd like to use "--follow" and allow file storage with a switch, or printout with another switch.
        There are several places in the code where I'd like to have this... allows better reuse of code.
        Example: "pq.py --follow <username> -print <filename> -sort <sort_method>"
- [ ] Write output class and methods with regular print, curses print, file storage as input methods to class

## Known bugs list

- [ ] Some functions seem to hit the error condition on exit, despite what should be a clean exit. No obvious errors
- [ ] comparefollowers method requires argument which is not used. Suspect this is coming from argparse configuration
