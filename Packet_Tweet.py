#!/usr/local/bin/python3
# Command line twitter client in the style of traditional unix shell commands
# Extensible so it can run as a bot, or be integrated into another application

import sys, tweepy, derp, webbrowser, os, time, json, argparse, re
import curses, curses.textpad
import traceback, logging
from derp import *

#TODO: Add obfuscation to user and app credentials somehow
#TODO: Move authentication to derp.py
#TODO: Move functions to doStuff.py

def initialAuth():
	
	global screen
	#screen = curses.initscr()
	#screen.nodelay(True)

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
		configFile = (home + '/.packetqueue/' + str(user.screen_name) + '/.packetqueue')
		#print(configFile)
		with open(configFile, 'r') as inFile:
			accessToken = inFile.readline().strip()
			accessTokenSecret = inFile.readline().strip()
			auth.set_access_token(accessToken, accessTokenSecret)
	
	# If the file doesn't exist, notify user then move through granting access token process
	except IOError:
		print('File .packetqueue doesn\'t exist... \n')
		
		try:
			redirect_url = auth.get_authorization_url()
			print('If a new browser window doesn\'t open, go to this URL: ')
			print(redirect_url)
			print('and authorize this app. Return here with the pin code you receive in order to finish')
			print('authorizing this app to access your account as specified.')
			webbrowser.open_new_tab(redirect_url)
			verifyPin = input('Pin Code: ')
			print(verifyPin)
			try:
				auth.get_access_token(verifyPin)
			except tweepy.TweepError:
				print('Error! Failed to get access token, or incorrect token was entered.')
				return(1)

			accessToken = auth.access_token
			accessTokenSecret = auth.access_token_secret
			
			# Write all of this good authentication stuff to a file
			# so we don't have to do it everytime we run the program
			ifconfigPath = os.path.join(home, '/.packetqueue/', str(user.screen_name))
			if not os.path.exists(home + '/.packetqueue/'):
				os.mkdir(home + '/.packetqueue/')
				if not os.path.exists(home + '/.packetqueue/' + str(user.screen_name)):
					os.mkdir(home + '/.packetqueue/' + str(user.screen_name))
			
			ifconfigFile = (home + '/.packetqueue/' + str(user.screen_name) + '/.packetqueue')
			print(ifconfigFile)
			with open(ifconfigFile, 'w+') as outFile:
				outFile.write(accessToken + '\n')	# function as a better way to store
				outFile.write(accessTokenSecret + '\n')	# the data

		
		# Something is so horribly borked we're just going to say fuck it
		except tweepy.TweepError:
			print('Error! Failed to get request token.')
			return(1)
	
	screen = curses.initscr()
	screen.nodelay(True)
	return None

def _mkdir_recursive(self, path):
	sub_path = os.path.dirname(path)
	if not os.path.exists(sub_path):
		self._mkdir_recursive(sub_path)
		if not os.path.exists(path):
			os.mkdir(path)

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
		screen.refresh() # Refresh screen now that strings added
	except curses.error:
		Cleanup(1)
	
	finally:
		screen.addstr('\n Press q to exit program...')
		while True:
			key = screen.getch()
			if key == ord('q'):
				Cleanup(0)
	
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
				screen.refresh() # Refresh screen now that strings added
		#Cleanup(0)

	except curses.error:
		Cleanup(1)
	
	finally:
		screen.addstr('\n Press q to exit program...')
		while True:
			key = screen.getch()
			if key == ord('q'):
				Cleanup(0)
	return None


def printMentions(number):
	# Print user's mentions
	myMentions = api.mentions_timeline(count=number)
	try:
		screen.addstr('\n')
		if number == 0:
			return
		else:
			for mention in myMentions:
				screen.addstr(str(mention.user.name),curses.color_pair(1))
				screen.addstr(str(': ' + mention.text + '\n'))
			screen.refresh()
		#Cleanup(0)
	except curses.error:
		Cleanup(1)

	finally:
		screen.addstr('\n Press q to exit program...')
		while True:
			key = screen.getch()
			if key == ord('q'):
				Cleanup(0)
	return None

def printRetweets(number):
	# Print user's tweets that others have retweeted
	otherRetweets = api.retweets_of_me(count=number, include_user_entities=False)
	try:
		screen.addstr('\n')
		if number == 0:
			return
		else:
			for retweets in otherRetweets:

				screen.addstr(str(retweets.user.name),curses.color_pair(1))
				screen.addstr(str(': ' + retweets.text + '\n'))
			screen.refresh()
			#Cleanup(0)
	except curses.error:
		Cleanup(1)

	finally:
		screen.addstr('\n Press q to exit program...')
		while True:
			key = screen.getch()
			if key == ord('q'):
				Cleanup(0)
	return None



#TODO: Wrap this in loop to test for verbose flag, if yes, dump entire JSON object to screen
def printMyInfo():
	# Print information about me
	myInfo = api.me()
	try:
		# Format and print handle, username, and user ID
		screen.addstr('\n')
		screen.addstr(str('@'),curses.color_pair(1))
		screen.addstr(str(myInfo.screen_name),curses.color_pair(1))
		screen.addstr(str(' (') + str(myInfo.name),curses.color_pair(2))
		screen.addstr(str('/') + str(myInfo.id_str),curses.color_pair(2))
		screen.addstr(str(')'))
		
		# Format and print created date for user
		screen.addstr(str('  User since: '),curses.color_pair(1))
		screen.addstr(str(myInfo.created_at),curses.color_pair(2))
		
		# Format and print followers count
		screen.addstr(str(' Followers: '),curses.color_pair(1))
		screen.addstr(str(myInfo.followers_count),curses.color_pair(2))

		# Format and print number of tweets
		screen.addstr(str(' Tweets: '),curses.color_pair(1))
		screen.addstr(str(myInfo.statuses_count),curses.color_pair(2))
		
		# Format and print user's reported location
		screen.addstr(str(' Location: '),curses.color_pair(1))
		screen.addstr(str(myInfo.location),curses.color_pair(2))
		
		# Format and print description from user profile
		screen.addstr('\n' + json.dumps(myInfo.description))
		screen.addstr('\n')
		
		# Format and print user's URL, if present
		screen.addstr(str('URL: '),curses.color_pair(1))
		screen.addstr(str(myInfo.url))

		# Format and print link to profile picture
		screen.addstr(str(' Profile Picture: '),curses.color_pair(1))
		screen.addstr(str(myInfo.profile_image_url_https))
		screen.addstr(str('\n'))
		
		# Add line space and clean up
		screen.addstr('\n')
		screen.refresh()
		#Cleanup(0)

	except curses.error:
		Cleanup(1)
	
	finally:
		screen.addstr('\n Press q to exit program...')
		while True:
			key = screen.getch()
			if key == ord('q'):
				Cleanup(0)
	return None

#TODO: Wrap this in loop to test for verbose flag, if yes, dump entire JSON object to screen
def printNotMe(data):
	# Print information on another user
	notMe = api.get_user(screen_name=data)
	try:
		
		#screen.addstr('\n')
		#screen.addstr(json.dumps(notMe.description) + '\n')
		#screen.addstr('\n')
		#screen.refresh()

		# Format and print handle, username, and user ID
		screen.addstr('\n')
		screen.addstr(str('@'),curses.color_pair(1))
		screen.addstr(str(notMe.screen_name),curses.color_pair(1))
		screen.addstr(str(' (' + notMe.name + '/' + notMe.id_str 
			+ ')'))
		
		# Format and print created date for user
		screen.addstr(str('  User since: '),curses.color_pair(1))
		screen.addstr(str(notMe.created_at))
		
		# Format and print followers count
		screen.addstr(str(' Followers: '),curses.color_pair(1))
		screen.addstr(str(notMe.followers_count))

		# Format and print number of tweets
		screen.addstr(str(' Tweets: '),curses.color_pair(1))
		screen.addstr(str(notMe.statuses_count))
		
		# Format and print user's reported location
		screen.addstr(str(' Location: '),curses.color_pair(1))
		screen.addstr(str(notMe.location))

		# Format and print description from user profile
		screen.addstr('\n' + json.dumps(notMe.description) + '\n')
		
		# Format and print user's URL, if present
		screen.addstr(str('URL: '),curses.color_pair(1))
		screen.addstr(str(notMe.url))
		
		# Format and print link to profile picture
		screen.addstr(str(' Profile Picture: '),curses.color_pair(1))
		screen.addstr(str(notMe.profile_image_url_https) + '\n')

		# Add line space and clean up
		screen.addstr('\n')
		screen.refresh()
		#Cleanup(0)
	
	except curses.error:
		Cleanup(1)

	finally:
		screen.addstr('\n Press q to exit program...')
		while True:
			key = screen.getch()
			if key == ord('q'):
				Cleanup(0)
	return None
	

def statusTest():
	for tweet in tweepy.Cursor(api.home_timeline(count=10)).items():
		print(tweet.text)
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
		
		screen.nodelay(1)
		c = screen.getch()
		#TODO: Pull status.text into named str, regex for @handle and #hashtag
		try:
			screen.addstr(str(status.user.name),curses.color_pair(1))
			screen.addstr(str(': ' + status.text + '\n'))
			screen.refresh() # Refresh screen now that strings added
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

def getStream():

	#terenListener = Streamer()
	#terenStream = tweepy.Stream(auth, listener=terenListener)
	terenStream = tweepy.Stream(auth, Streamer())
	terenStream.userstream()

def getFollowStream(user):

	#terenListener = Streamer()
	terenStream = tweepy.Stream(auth, Streamer())
	userID = str(user)
	if userID != '17028130':
		terenStream.filter(follow = [userID])	
	else: terenStream.userstream()

def getStreamSearch(searchHash):

	#terenListener = Streamer()
	terenStream = tweepy.Stream(auth, Streamer())
	i = len(searchHash)
	#search = str(searchHash)
	str1 = ''.join(searchHash)
	terenStream.filter(track = [str1])


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

def argumentProcess(command_args):
	
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
			curses.endwin()
			raise
		except (KeyboardInterrupt):
			curses.endwin()
			logging.exception
			sys.exit(1)
		#import pdb; pdb.set_trace()
		#curses.endwin()			#TODO: Need to exit curses cleanly, not working now.
	# Get mentions with 'n' number of tweets
	elif command_args.userMentions:
	
		try:
			initialAuth()
			screen.scrollok(True)
			curses.noecho()	# Keeps key presses from echoing to screen
			curses.cbreak() # Takes input away
			screen.keypad(1)
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
			if 'all' in command_args.streamUserSearch:
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

	
	elif command_args.myInfo:
	
		try:
			initialAuth()
			screen.scrollok(True)
			curses.noecho()	# Keeps key presses from echoing to screen
			curses.cbreak() # Takes input away
			screen.keypad(1)
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
			initialAuth()
			screen.scrollok(True)
			curses.noecho()
			curses.cbreak()
			screen.keypad(1)
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
			initialAuth()
			screen.scrollok(True)
			curses.noecho()
			curses.cbreak()
			screen.keypad(1)
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

	else: print(sys.argv)

def main():


	progVersion = str('Alpha 0.1')

	parser = argparse.ArgumentParser(description='Command line Twitter (and stuff) client', 
			epilog='For questions contact @SomeClown', usage='%(prog)s [options]')
	
	parser.add_argument('-t', '--tweets', type=int, action='store', nargs=1, dest="tweetsNum", 
			metavar='', help="Get 'n' number of recent tweets from main feed")

	parser.add_argument('-s', '--stream', action='store', type=str, nargs=1, dest='streamUserSearch', 
			metavar='', help='Stream full user feed, or feed mentioning <user>')
	
	parser.add_argument('-e', '--search', action='store', type=str, nargs='*', dest='search', 
			metavar='', help='stream the global twitter feed by search term')
	
	parser.add_argument('-f', '--friends', action="store", type=int, nargs=1, dest='numFriends', 
			metavar='', help='print list of friends')
	
	parser.add_argument('-d', '--direct', nargs=2, action="store", type=str, 
			metavar='', dest='directMessage', help='send a direct message')
	
	parser.add_argument('-S', '--status', nargs=1, action="store", type=str, 
			metavar='', dest='statusUpdate', help='update twitter status')

	parser.add_argument('-m', '--mentions', type=int, nargs=1, action='store',
			metavar='', dest='userMentions', help='get mentions from logged in user\'s timeline')

	parser.add_argument('-M', '--me', action='store_true', dest='myInfo', help='Get information about me')

	parser.add_argument('-n', '--notme', metavar='', dest='notMe', nargs=1, type=str,
			help='Get information about someone other than me')

	parser.add_argument('-r', '--retweets', metavar='', dest='retweets', nargs=1, type=str,
			help='Get retweets of me by others')
	
	parser.add_argument('-V', '--version', action='version', version=progVersion)

	parser.add_argument('-v', '--verbose', action='store_true', help='verbose flag')
	
	if len(sys.argv)==1:
		parser.print_help()
		sys.exit(1)
	
	command_args = parser.parse_args()
	argumentProcess(command_args)

	return None

if __name__ == '__main__':
	main()

else: print("loaded as module, api, or Skynet...")
