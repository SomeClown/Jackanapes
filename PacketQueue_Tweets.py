#!/usr/local/bin/python3
# Command line twitter client in the style of traditional unix shell commands
# Extensible so it can run as a bot, or be integrated into another application

import sys, tweepy, derp, webbrowser, os, time, json, argparse, re
import curses, curses.textpad
import traceback, logging
from derp import *

#TODO: Implement argparse[] and start building out functions. Also, clean up source here,
#TODO: and add obfuscation to user and app credentials somehow

def initialAuth():

	# Globals
	global auth	# Lazy, fix later
	global api	# Much drunk, so wow
	global user
	global color_black 
	global color_red
	global color_green
	global color_yellow
	global color_blue
	global color_purple
	global color_cyan
	global color_white

	# Set our color vars to the appropriate ansi escape codes
	#
	# Format: 	
	#		\033[ - Escape code, always the same
	# 		1 = style, 1 for normal
	# 		32 = text color
	#		40m = background color
	# Foreground Colors:
	#		30 = black
	#		31 = red
	#		32 = green
	#		33 = yellow
	#		34 = blue
	#		35 = purple
	#		36 = cyan
	#		37 = white
	# Text Style:
	#		0 = nothing
	#		1 = bold
	#		2 = underline
	#		3 = negative1
	#		4 = negative2
	# Background Colors:
	#		40 = black
	#		41 = red
	#		42 = green
	#		43 = yellow
	#		44 = blue
	#		45 = purple
	#		46 = cyan
	#		47 = white

	color_black = "\033[1;30m{0}\033[00m"
	color_red = "\033[01;31m{0}\033[00m"
	color_green = "\033[1;32m{0}\033[00m"
	color_yellow = "\033[1;33m{0}\033[00m"
	color_blue = "\033[1;34m{0}\033[00m"
	color_purple = "\033[1;35m{0}\033[00m"
	color_cyan = "\033[1;36m{0}\033[00m"
	color_white = "\033[1;37m{0}\033[00m"



	auth = derp.hokum()	
	api = tweepy.API(auth)	
	user = api.get_user('SomeClown')
	
	# Check to see if config file with credentials exists
	# if it does, load our keys from the file and pass them to the
	# auth.set_access_token() method
	try:
		home = os.path.expanduser("~")
		configFile = open(home + "/.packetqueue","r")
		accessToken = configFile.readline().strip()
		accessTokenSecret = configFile.readline().strip()
		configFile.close()
		auth.set_access_token(accessToken, accessTokenSecret)

	# If the file doesn't exist, notify user then move through granting access token process
	except IOError:
		print('File .packetqueue doesn\'t exist... \n')
		
		try:
			redirect_url = auth.get_authorization_url()
			webbrowser.open_new_tab(redirect_url)
			print('If a new browser window doesn\'t open, go to this URL:')
			print(redirect_url )
			print('and authorize this app. Return here with the pin code you receive in order to finish')
			print('authorizing this app to access your account as specified.')
			verifyPin = input('Pin Code: ')
			
			try:
				auth.get_access_token(verifyPin)
			except tweepy.TweepError:
				print('Error! Failed to get access token, or incorrect token was entered.')
				return(1)

			accessToken = auth.access_token
			accessTokenSecret = auth.access_token_secret
			# Write all of this good authentication stuff to a file
			# so we don't have to do it everytime we run the program
			configFile = open(home + "/.packetqueue","w")	# Change this to use the sheve()
			configFile.write(accessToken + '\n')		# function as a better way to store
			configFile.write(accessTokenSecret + '\n')	# the data
		
		# Something is so horribly borked we're just going to say fuck it
		except tweepy.TweepError:
			print('Error! Failed to get request token.')
			return(1)
	
	return None

def printFriends(number):


	try:
		
		screen.addstr('\n')
		screen.addstr('-------------------------------------------------------' + '\n')
		screen.addstr(str(user.screen_name) + '\n')
		screen.addstr('-------------------------------------------------------')
		screen.addstr('\n')
		screen.addstr('Friends Count: ' + str(user.followers_count) + '\n')
		if number == 0:
			return
		else:
			for friend in user.friends(count=number):
				screen.addstr('\t' + friend.screen_name + '\n')
		screen.addstr('\n')
		screen.addstr('-------------------------------------------------------')
		screen.addstr('\n')			
		screen.refresh() # Refresh screen now that strings addedi
	except curses.error:
		pass
	
	return None

	

def printTimeline(number):

	# Print user's public timeline
	public_tweets = api.home_timeline(count=number)
	#import pdb; pdb.set_trace()
	try:
		screen.addstr('\n')
		if number == 0:
			return
		else:
			for tweet in public_tweets:
				screen.addstr(str(tweet.user.name),curses.color_pair(1))
				screen.addstr(str(': ' + tweet.text + '\n'))
		screen.refresh() # Refresh screen now that strings addedi
	except curses.error:
		pass
	
	return None

def statusTest():
	for tweet in tweepy.Cursor(api.home_timeline(count=10)).items():
		print(tweet.text)
	return None


def badFollowers(cursor):	# I don't understand cursors yet
	while True:
		try:
			yield cursor.next()
		except tweepy.RateLimitError:
			time.sleep(15 * 60)

	return None

#TODO: Need to figure out how to parse this and store it in a database
#TODO: then pull out what we want for display

class DictStreamListener(tweepy.StreamListener):
	
	def on_status(self,status):
		
		#TODO: Pull status.text into named str, regex for @handle and #hashtag
		try:
			screen.addstr(str(status.user.name),curses.color_pair(1))
			screen.addstr(str(': ' + status.text + '\n'))
			screen.refresh() # Refresh screen now that strings added
		except curses.error:
			pass
	
	# This is consuming everything
	# including the session opening friends list
	#def on_data(self, data):
		# convert tweepy object to raw json/dictionary
		#json_data = json.loads(data)
		
		#tweetText = json_data['friends']
		#print(tweetText)
		
		#Pretty print this to the screen
		#print(json.dumps(json_data, indent=4, sort_keys=True))
	

def getStream():

	terenListener = DictStreamListener()
	terenStream = tweepy.Stream(auth, listener=terenListener)
	terenStream.userstream()

def getFollowStream(user):

	terenListener = DictStreamListener()
	terenStream = tweepy.Stream(auth, listener=terenListener)
	userID = str(user)
	if userID != '17028130':
		terenStream.filter(follow = [userID])	
	else: terenStream.userstream()

def getStreamSearch(searchHash):

	terenListener = DictStreamListener()
	terenStream = tweepy.Stream(auth, listener=terenListener)
	search = str(searchHash)
	terenStream.filter(track = [search])


def directSend(user, msg):

	nameCheck = re.compile(r'(@)+')
	nameResult = nameCheck.search(user)
	
	if len(msg) >= 140:
		print('Tweets must be 140 characters or less')
	elif nameResult == None:
		print('Incorrect username format (must include @)')
	else:
		directTweet = api.send_direct_message(screen_name=user, text=msg)
	return None


def statusUpdate(text):

	#import pdb; pdb.set_trace()
	if len(text) >= 140:
		print('Tweets must be 140 characters or less')
	else:
		status = api.update_status(status=text)
	return None


def main(**kwargs):

	progVersion = str('Alpha 0.1')

	parser = argparse.ArgumentParser(description='Command line Twitter client', 
			formatter_class=argparse.RawTextHelpFormatter, epilog='For questions contact @SomeClown')
	
	parser.add_argument('--tweets', '-t', action="store", type=int, nargs='+', default=0, required=False, dest="tweetsNum", 
			help="Get 'n' number of recent tweets from main feed")
	
	parser.add_argument('--stream', '-s', action='store', type=str, nargs='+', dest='streamUserSearch', 
			help='Stream full user feed, or feed mentioning <user>')
	
	parser.add_argument('--search', '-e', action='store', type=str, nargs='+', required=False, dest='search', 
			help='stream the global twitter feed by search term')
	
	parser.add_argument('--friends', '-f', action="store", type=int, nargs='+', default=0, required=False, dest='numFriends', 
			help='print list of friends')
	
	parser.add_argument('--direct', '-d', nargs=2, action="store", type=str, 
			dest='directMessage', help='send a direct message')
	
	parser.add_argument('--status', '-S', nargs='*', action="store", type=str, 
			dest='statusUpdate', help='update twitter status')

	parser.add_argument('--version', action='version', version=progVersion)

	parser.add_argument('--verbose', '-v', action='store_true', help='verbose flag')

	# Use vars() to create dictionary of command line switches and text.
	
	command_args = parser.parse_args()
	argsDict = vars(command_args)

	# Get timeline with 'n' number of tweets	
	if command_args.tweetsNum:
	
		try:
			initialAuth()
			screen.scrollok(True)
			curses.noecho()	# Keeps key presses from echoing to screen
			curses.cbreak() # Takes input away
			screen.keypad(1)
			curses.start_color()
			curses.use_default_colors()
			curses.init_pair(1, curses.COLOR_RED, -1) # Foreground Red/background transparent
			printTimeline(command_args.tweetsNum[0])
		except (SystemExit):
			raise
		except (KeyboardInterrupt):
			logging.exception
		#import pdb; pdb.set_trace()
	
	# Start stream on <@username>
	# If 'all' is put in place of username, stream user's home timeline
	elif command_args.streamUserSearch:
		
		try:
			initialAuth()
			screen.scrollok(True)
			curses.noecho()	# Keeps key presses from echoing to screen
			curses.cbreak() # Takes input away
			screen.keypad(1)
			curses.start_color()
			curses.use_default_colors()
			curses.init_pair(1, curses.COLOR_RED, -1) # Foreground Red/background transparent
			#getUser = api.get_user(screen_name=argsDict['streamUserSearch'])
			if 'all' in argsDict['streamUserSearch']:
				getStream()
			else:
				screenName = command_args.streamUserSearch[0]
				getUser = api.get_user(screenName)
				userID = getUser.id
				getFollowStream(userID)
		except tweepy.TweepError as e:
			curses.endwin()
			print(e.response) 		#This works
			#print(e.message[0]['code'])	#This does not work
		except (SystemExit):
			curses.endwin()
			raise
		except (KeyboardInterrupt):
			curses.endwin()
			logging.exception

	# Start stream using <searchterm>
	elif command_args.search:
		
		try:
			initialAuth()
			screen.scrollok(True)
			curses.noecho()	# Keeps key presses from echoing to screen
			curses.cbreak() # Takes input away
			screen.keypad(1)
			curses.start_color()
			curses.use_default_colors()
			curses.init_pair(1, curses.COLOR_RED, -1) # Foreground Red/background transparent
			searchTerm = command_args.search[0]
			getStreamSearch(searchTerm)
		except (tweepy.TweepError):
			curses.endwin()
			print(TweepError.message[0]['code'])
		except (SystemExit):
			curses.endwin()
			raise
		except (KeyboardInterrupt):
			curses.endwin()
	
	# Print <n> number of friends to screen, where <n> is less than Titter max limit
	elif command_args.numFriends:

		try:
			initialAuth()
			screen.scrollok(True)
			curses.noecho()	# Keeps key presses from echoing to screen
			curses.cbreak() # Takes input away
			screen.keypad(1)
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
	
		initialAuth()
		userDirect = command_args.directMessage[0]
		msgDirect = command_args.directMessage[1]
		directSend(userDirect, msgDirect)

	# update status
	elif command_args.statusUpdate:
		
		initialAuth()
		msgStatusUpdate = command_args.statusUpdate[0]
		statusUpdate(msgStatusUpdate)


	#else: print(sys.argv)

	return None

if __name__ == '__main__':
	main()

else:
	print("loaded as module or bot...")
