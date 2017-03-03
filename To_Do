## To do list for the command line client

- [ ] Use tweet_id (or something) to restructure tweet stream to incorporate the history with the tweet (replied to, etc.)
        In other words, show replies inline with the stream. Make this a selectable option at invokation
- [ ] Rewrite code for config file using ConfigParser module from standard library
	- [ ] Add current functionality to pull oauth keys
	- [ ] Add additional functionality for colors, curses-based vs. standard text, etc.
- [ ] Add database functionality (or flat file, as appropriate)
	- [X] Store friends list (use ID)
	- [ ] Store cursor for later recall of where we were in the stream when last ran
	- [ ] Look into something like tinydb to see if appropriate as longer term storage vs. flat files
- [ ] Add progress bar for oauth authentication, as well as for large data pulls (friends lists, etc.)
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

# Known bugs list

- [ ] Some functions seem to hit the error condition on exit, despite what should be a clean exit. No obvious errors
- [ ] comparefollowers method requires argument which is not used. Suspect this is coming from argparse configuration
- [ ] Not all search term combinations work (OR, AND) with multiple keywords
