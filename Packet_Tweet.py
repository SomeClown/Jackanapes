#!/usr/local/bin/python3
# Command line twitter client in the style of traditional unix shell commands
# Extensible so it can run as a bot, or be integrated into another application

import sys, tweepy, derp, webbrowser, os, time, json, argparse, re
import curses, curses.textpad, arguments, globalVars
import traceback, logging
import stuff
from derp import *
from helpText import *
from authorization import initialAuth

def _mkdir_recursive(self, path):
	sub_path = os.path.dirname(path)
	if not os.path.exists(sub_path):
		self._mkdir_recursive(sub_path)
		if not os.path.exists(path):
			os.mkdir(path)

@initialAuth
def printFriends(number):

	try:
		globalVars.screen.addstr('\n')
		globalVars.screen.addstr('-------------------------------------------------------' + '\n')
		globalVars.screen.addstr(str(globalVars.user.screen_name) + '\n')
		globalVars.screen.addstr('-------------------------------------------------------')
		globalVars.screen.addstr('\n')
		globalVars.screen.addstr('Friends Count: ' + str(globalVars.user.followers_count) + '\n')
		if number == 0:
			return
		else:
			for friend in globalVars.user.friends(count=number):
				globalVars.screen.addstr('\t' + friend.screen_name + '\n')
		globalVars.screen.addstr('\n')
		globalVars.screen.addstr('-------------------------------------------------------')
		globalVars.screen.addstr('\n')			
		globalVars.screen.refresh() # Refresh screen now that strings added
	except curses.error:
		Cleanup(1)
	
	finally:
		globalVars.screen.addstr('\n Press q to exit program...')
		while True:
			key = globalVars.screen.getch()
			if key == ord('q'):
				Cleanup(0)
	
	return None

@initialAuth
def printTimeline(number):

	# Print user's public timeline
	public_tweets = globalVars.api.home_timeline(count=number)
	try:
		globalVars.screen.addstr('\n')
		if number == 0:
			return
		else:
			for tweet in public_tweets:
				globalVars.screen.addstr(str(tweet.user.name),curses.color_pair(1))
				globalVars.screen.addstr(str(': ' + tweet.text + '\n'))
			globalVars.screen.refresh() # Refresh screen now that strings added

	except curses.error:
		Cleanup(1)
	
	finally:
		globalVars.screen.addstr('\n Press q to exit program...')
		while True:
			key = globalVars.screen.getch()
			if key == ord('q'):
				Cleanup(0)
	return None

@initialAuth
def printMentions(number):
	# Print user's mentions
	myMentions = globalVars.api.mentions_timeline(count=number)
	try:
		globalVars.screen.addstr('\n')
		if number == 0:
			return
		else:
			for mention in myMentions:
				globalVars.screen.addstr(str(mention.user.name),curses.color_pair(1))
				globalVars.screen.addstr(str(': ' + mention.text + '\n'))
			globalVars.screen.refresh()
	except curses.error:
		Cleanup(1)

	finally:
		globalVars.screen.addstr('\n Press q to exit program...')
		while True:
			key = globalVars.screen.getch()
			if key == ord('q'):
				Cleanup(0)
	return None

@initialAuth
def printRetweets(number):
	# Print user's tweets that others have retweeted
	otherRetweets = globalVars.api.retweets_of_me(count=number, include_user_entities=False)
	try:
		globalVars.screen.addstr('\n')
		if number == 0:
			Cleanup(1)
			return
		else:
			for retweets in otherRetweets:
				#idName = globalVars.api.get_user(retweets.id_str)
				#globalVars.screen.addstr(str(idName.screen_name))
				globalVars.screen.addstr(str(retweets.id_str),curses.color_pair(1))
				globalVars.screen.addstr(str(': ' + retweets.text + '\n'))
			globalVars.screen.refresh()
	except curses.error:
		import pdb; pdb.set_trace()
		Cleanup(1)

	finally:
		globalVars.screen.addstr('\n Press q to exit program...')
		while True:
			key = globalVars.screen.getch()
			if key == ord('q'):
				Cleanup(0)
	return None

@initialAuth
def printMyInfo():
	# Print information about me
	myInfo = globalVars.api.me()
	try:
		# Format and print handle, username, and user ID
		globalVars.screen.addstr('\n')
		globalVars.screen.addstr(str('@'),curses.color_pair(1))
		globalVars.screen.addstr(str(myInfo.screen_name),curses.color_pair(1))
		globalVars.screen.addstr(str(' (') + str(myInfo.name),curses.color_pair(2))
		globalVars.screen.addstr(str('/') + str(myInfo.id_str),curses.color_pair(2))
		globalVars.screen.addstr(str(')'))
		
		# Format and print created date for user
		globalVars.screen.addstr(str('  User since: '),curses.color_pair(1))
		globalVars.screen.addstr(str(myInfo.created_at),curses.color_pair(2))
		
		# Format and print followers count
		globalVars.screen.addstr(str(' Followers: '),curses.color_pair(1))
		globalVars.screen.addstr(str(myInfo.followers_count),curses.color_pair(2))

		# Format and print number of tweets
		globalVars.screen.addstr(str(' Tweets: '),curses.color_pair(1))
		globalVars.screen.addstr(str(myInfo.statuses_count),curses.color_pair(2))
		
		# Format and print user's reported location
		globalVars.screen.addstr(str(' Location: '),curses.color_pair(1))
		globalVars.screen.addstr(str(myInfo.location),curses.color_pair(2))
		
		# Format and print description from user profile
		globalVars.screen.addstr('\n' + json.dumps(myInfo.description))
		globalVars.screen.addstr('\n')
		
		# Format and print user's URL, if present
		globalVars.screen.addstr(str('URL: '),curses.color_pair(1))
		globalVars.screen.addstr(str(myInfo.url))

		# Format and print link to profile picture
		globalVars.screen.addstr(str(' Profile Picture: '),curses.color_pair(1))
		globalVars.screen.addstr(str(myInfo.profile_image_url_https))
		globalVars.screen.addstr(str('\n'))
		
		# Add line space and clean up
		globalVars.screen.addstr('\n')
		globalVars.screen.refresh()

	except curses.error:
		Cleanup(1)
	
	finally:
		globalVars.screen.addstr('\n Press q to exit program...')
		while True:
			key = globalVars.screen.getch()
			if key == ord('q'):
				Cleanup(0)
	return None

@initialAuth
def printNotMe(data):
	# Print information on another user
	notMe = globalVars.api.get_user(screen_name=data)
	try:

		# Format and print handle, username, and user ID
		globalVars.screen.addstr('\n')
		globalVars.screen.addstr(str('@'),curses.color_pair(1))
		globalVars.screen.addstr(str(notMe.screen_name),curses.color_pair(1))
		globalVars.screen.addstr(str(' (' + notMe.name + '/' + notMe.id_str 
			+ ')'))
		
		# Format and print created date for user
		globalVars.screen.addstr(str('  User since: '),curses.color_pair(1))
		globalVars.screen.addstr(str(notMe.created_at))
		
		# Format and print followers count
		globalVars.screen.addstr(str(' Followers: '),curses.color_pair(1))
		globalVars.screen.addstr(str(notMe.followers_count))

		# Format and print number of tweets
		globalVars.screen.addstr(str(' Tweets: '),curses.color_pair(1))
		globalVars.screen.addstr(str(notMe.statuses_count))
		
		# Format and print user's reported location
		globalVars.screen.addstr(str(' Location: '),curses.color_pair(1))
		globalVars.screen.addstr(str(notMe.location))

		# Format and print description from user profile
		globalVars.screen.addstr('\n' + json.dumps(notMe.description) + '\n')
		
		# Format and print user's URL, if present
		globalVars.screen.addstr(str('URL: '),curses.color_pair(1))
		globalVars.screen.addstr(str(notMe.url))
		
		# Format and print link to profile picture
		globalVars.screen.addstr(str(' Profile Picture: '),curses.color_pair(1))
		globalVars.screen.addstr(str(notMe.profile_image_url_https) + '\n')

		# Add line space and clean up
		globalVars.screen.addstr('\n')
		globalVars.screen.refresh()
	
	except curses.error:
		Cleanup(1)

	finally:
		globalVars.screen.addstr('\n Press q to exit program...')
		while True:
			key = globalVars.screen.getch()
			if key == ord('q'):
				Cleanup(0)
	return None
	
@initialAuth
def termSearch(term):

	try:
		search = str(term[0])
		count = int(term[1])
		for tweet in tweepy.Cursor(globalVars.api.search, q=search).items(count):	
			globalVars.screen.addstr(str(tweet.created_at) + ': ')
			globalVars.screen.addstr(str(tweet.user.name),curses.color_pair(1))
			globalVars.screen.addstr(str(': ' + tweet.text + '\n'))
			globalVars.screen.refresh() # Refresh screen now that strings added
			
	except curses.error:
		Cleanup(1)
	finally:
		globalVars.screen.addstr('\n Press q to exit program...')
		while True:
			key = globalVars.screen.getch()
			if key == ord('q'):
				Cleanup(0)
	return None

def Cleanup(exitCode):
	curses.echo()
	curses.nocbreak()
	curses.endwin()
	if exitCode == 1:
		print('Egads, it looks like we shit the bed...')
		sys.exit(exitCode)
	else:
		sys.exit(exitCode)

class Streamer(tweepy.StreamListener):
	
	def on_status(self,status):
		
		globalVars.screen.nodelay(1)
		c = globalVars.screen.getch()
		#TODO: Pull status.text into named str, regex for @handle and #hashtag
		try:
			globalVars.screen.addstr(str(status.user.name),curses.color_pair(1))
			globalVars.screen.addstr(str(': ' + status.text + '\n'))
			globalVars.screen.refresh() # Refresh screen now that strings added
			if c == ord('q'):
				Cleanup(0)
			else:
				pass
		
		except curses.error:
			Cleanup(1)
		except BaseException as e:
			Cleanup(1)
			print('failed on_status, ', str(e))
			time.sleep(5)


	def on__error(self, status):
		Cleanup(1)
		print(status)
'''
	# This is consuming everything
	# including the session opening friends list
	def on_data(self, data):
		#convert tweepy object to raw json/dictionary
		json_data = json.loads(data)
		
		tweetText = json_data['friends']
		print(tweetText)
		
		#Pretty print this to the screen
		print(json.dumps(json_data, indent=4, sort_keys=True))
'''	

@initialAuth
def getStream():

	terenStream = tweepy.Stream(globalVars.auth, Streamer())
	terenStream.userstream()

@initialAuth
def getFollowStream(user):

	terenStream = tweepy.Stream(globalVars.auth, Streamer())
	userID = str(user)
	if userID != '17028130':
		terenStream.filter(follow = [userID])	
	else: terenStream.userstream()

@initialAuth
def getStreamSearch(searchHash):

	terenStream = tweepy.Stream(globalVars.auth, Streamer())
	i = len(searchHash)
	str1 = ''.join(searchHash)
	terenStream.filter(track = [str1])

@initialAuth
def directSend(user, msg):

	nameCheck = re.compile(r'(@)+')
	nameResult = nameCheck.search(user)
	
	if len(msg) >= 140:
		print('Tweets must be 140 characters or less')
	elif nameResult == None:
		print('Incorrect username format (must include @)')
	else:
		directTweet = globalVars.api.send_direct_message(screen_name=user, text=msg)
	return None

@initialAuth
def statusUpdate(text):

	if len(text) >= 140:
		print('Tweets must be 140 characters or less')
	else:
		status = globalVars.api.update_status(status=text)
	return None


def argumentProcess(command_args):
	
	# Get timeline with 'n' number of tweets
	if command_args.tweetsNum:
	
		try:
			globalVars.screen.scrollok(True)
			curses.noecho()	# Keeps key presses from echoing to screen
			curses.cbreak() # Takes input away
			globalVars.screen.keypad(1)
			curses.start_color()
			curses.use_default_colors()
			curses.init_pair(1, curses.COLOR_RED, -1) # Foreground Red/background transparent
			printTimeline(command_args.tweetsNum[0])
		except (SystemExit):
			curses.endwin()
			raise
		except (KeyboardInterrupt):
			curses.endwin()
			logging.exception
			sys.exit(1)
	
	# Get mentions with 'n' number of tweets
	elif command_args.userMentions:
	
		try:
			globalVars.screen.scrollok(True)
			curses.noecho()	# Keeps key presses from echoing to screen
			curses.cbreak() # Takes input away
			globalVars.screen.keypad(1)
			curses.start_color()
			curses.use_default_colors()
			curses.init_pair(1, curses.COLOR_RED, -1) # Foreground Red/background transparent
			printMentions(command_args.userMentions[0])
		except (SystemExit):
			curses.endwin()
			raise
		except (KeyboardInterrupt):
			curses.endwin()
			logging.exception
			
	# Start stream on <@username>
	# If 'all' is put in place of username, stream user's home timeline
	elif command_args.streamUserSearch:
		
		try:
			globalVars.screen.scrollok(True)
			curses.noecho()	# Keeps key presses from echoing to screen
			curses.cbreak() # Takes input away
			globalVars.screen.keypad(1)
			curses.start_color()
			curses.use_default_colors()
			curses.init_pair(1, curses.COLOR_RED, -1) # Foreground Red/background transparent
			if 'all' in command_args.streamUserSearch:
				getStream()
			else:
				screenName = command_args.streamUserSearch[0]
				getUser = globalVars.api.get_user(screenName)
				userID = getUser.id
				getFollowStream(userID)
		except tweepy.TweepError as e:
			curses.endwin()
			print(e.response) 		#This works
		except (SystemExit):
			curses.endwin()
			raise
		except (KeyboardInterrupt):
			curses.endwin()
			logging.exception

	# Start stream using <searchterm>
	elif command_args.search:
		
		try:
			globalVars.screen.scrollok(True)
			curses.noecho()	# Keeps key presses from echoing to screen
			curses.cbreak() # Takes input away
			globalVars.screen.keypad(1)
			curses.start_color()
			curses.use_default_colors()
			curses.init_pair(1, curses.COLOR_RED, -1) # Foreground Red/background transparent
			searchTerm = command_args.search
			getStreamSearch(searchTerm)
		except (tweepy.TweepError):
			curses.endwin()
			print(TweepError.message[0]['code'])
		except (SystemExit):
			curses.endwin()
			raise
		except (KeyboardInterrupt):
			curses.endwin()
			logging.exception
	
	# Print <n> number of friends to screen, where <n> is less than Titter max limit
	elif command_args.numFriends:

		try:
			globalVars.screen.scrollok(True)
			curses.noecho()	# Keeps key presses from echoing to screen
			curses.cbreak() # Takes input away
			globalVars.screen.keypad(1)
			curses.start_color()
			curses.use_default_colors()
			curses.init_pair(1, curses.COLOR_RED, -1) # Foreground Red/background transparent
			printFriends(command_args.numFriends[0])
		except (SystemExit):
			raise
		except (KeyboardInterrupt):
			logging.exception
			curses.endwin()
	
	# send a direct message
	elif command_args.directMessage:
	
		userDirect = command_args.directMessage[0]
		msgDirect = command_args.directMessage[1]
		directSend(userDirect, msgDirect)

	# update status
	elif command_args.statusUpdate:
		
		msgStatusUpdate = command_args.statusUpdate[0]
		statusUpdate(msgStatusUpdate)

	elif command_args.myInfo:
	
		try:
			globalVars.screen.scrollok(True)
			curses.noecho()	# Keeps key presses from echoing to screen
			curses.cbreak() # Takes input away
			globalVars.screen.keypad(1)
			curses.start_color()
			curses.use_default_colors()
			curses.init_pair(1, curses.COLOR_RED, -1) # Foreground Red/background transparent
			curses.init_pair(2, curses.COLOR_YELLOW, -1)
			curses.init_pair(3, curses.COLOR_BLUE, -1)
			curses.init_pair(5, curses.COLOR_MAGENTA, -1)
			printMyInfo()
		except (SystemExit):
			curses.endwin()
			raise
		except (KeyboardInterrupt):
			curses.endwin()
			logging.exception

	elif command_args.notMe:
		try:
			globalVars.screen.scrollok(True)
			curses.noecho()
			curses.cbreak()
			globalVars.screen.keypad(1)
			curses.start_color()
			curses.use_default_colors()
			curses.init_pair(1, curses.COLOR_RED, -1)
			printNotMe(command_args.notMe[0])
		except (SystemExit):
			curses.endwin()
			raise
		except (KeyboardInterrupt):
			curses.endwin()
			logging.exception

	elif command_args.retweets:
		try:
			globalVars.screen.scrollok(True)
			curses.noecho()
			curses.cbreak()
			globalVars.screen.keypad(1)
			curses.start_color()
			curses.use_default_colors()
			curses.init_pair(1, curses.COLOR_RED, -1)
			printRetweets(command_args.retweets[0])
		except (SystemExit):
			curses.endwin()
			raise
		except (KeyboardInterrupt):
			curses.endwin()
			logging.exception

	elif command_args.term:
		try:
			globalVars.screen.scrollok(True)
			curses.noecho()
			curses.cbreak()
			globalVars.screen.keypad(1)
			curses.start_color()
			curses.use_default_colors()
			curses.init_pair(1, curses.COLOR_RED, -1)
			termSearch(command_args.term)
		except (SystemExit):
			curses.endwin()
			raise
		except (KeyboardInterrupt):
			curses.endwin()
			logging.exception
	
	else: print(sys.argv)
	
def main():

	my_command_args = arguments.argumentsParsing()
	argumentProcess(my_command_args)	
	return None

if __name__ == '__main__':
	main()

else: print("loaded as module, api, or Skynet...")
