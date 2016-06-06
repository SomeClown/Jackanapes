#!/usr/local/bin/python3
# Command line twitter client in the style of traditional unix shell commands
# Extensible so it can run as a bot, or be integrated into another application

import sys, tweepy, derp, webbrowser, os, time, json, argparse, re
import curses, curses.textpad

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
	
	return(0)

def printFriends(number):

	print('\n')
	print('-------------------------------------------------------')
	print(user.screen_name)
	print('-------------------------------------------------------')
	print('Friends Count: ' + str(user.followers_count))
	for friend in user.friends(count=number):
		print('\t' + friend.screen_name)

	print('\n')
	print('-------------------------------------------------------')
	print('\n')
	return(0)

def printTimeline(number):

	# Print user's public timeline
	public_tweets = api.home_timeline(count=number)

	print('\n')
	for tweet in public_tweets:
		print(color_red.format(str(tweet.user.name)) + ': ' + tweet.text)

	return(0)

def statusTest():
	for tweet in tweepy.Cursor(api.home_timeline(count=10)).items():
		print(tweet.text)

def badFollowers(cursor):	# I don't understand cursors yet
	while True:
		try:
			yield cursor.next()
		except tweepy.RateLimitError:
			time.sleep(15 * 60)

#TODO: Need to take the best practices from Twitter and apply them here. Specifically
#TODO: the ones around consuming the feed and storing it in one process, and 
#TODO: printing it (or whatever) in another process.

class MyStreamListener(tweepy.StreamListener):
	''' Deprecated at this point in favor of DictStreamListener class below '''
	
	# This is just consuming and printing status
	def on_status(self, status):
		print(status.text)
		return True

#TODO: Need to figure out how to parse this and store it in a database
#TODO: then pull out what we want for display

class DictStreamListener(tweepy.StreamListener):
	
	def on_status(self,status):
		print(color_red.format(str(status.user.name)) + ': ' + status.text)
	
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
	#return(0)

def directSend(user, text):
	'''
	nameCheck = re.compile(r'(@)+')
	nameResult = nameCheck.search(user)
	
	if len(text) >= 140:
		print('Tweets must be 140 characters or less')
	elif nameResult == None:
		print('Incorrect username format (must include @)')
	else:
		directTweet = api.send_direct_message(screen_name=user, text=text)
	return(0)
'''

def statusUpdate(text):

	if len(text) >= 140:
		print('Tweets must be 140 characters or less')
	else:
		status = api.update_status(status=text)
	return(0)


def cursesTest():
	
	screen = curses.initscr()
	curses.noecho()
	curses.curs_set(0)
	screen.keypad(1)
	while True:
		event = screen.getch()
		if event == ord("q"): break
		addstr(getStream())
	curses.endwin()

	return(0)


def main():

	parser = argparse.ArgumentParser(description='Command line Twitter client', 
			epilog='For questions contact @SomeClown')
	
	parser.add_argument('--tweets', '-t', action="store", type=int, dest="tweetsNum", 
			help="Get 'n' number of recent tweets from main feed")
	
	parser.add_argument('--stream', '-s', action='store_true', 
			help='start client in streaming mode')
	
	parser.add_argument('--friends', '-f', action="store", type=int, dest='numFriends', 
			help='print list of friends')
	
	parser.add_argument('--direct', '-d', nargs=2, action="store", type=str, 
			dest='directMessage', help='send a direct message')
	
	parser.add_argument('--status', '-S', nargs='*', action="store", type=str, 
			dest='statusUpdate', help='update twitter status')
	
	parser.add_argument('--verbose', action='store_true', help='verbose flag')

	parser.add_argument('--cursesTest', '-c', action='store_true',
			help='ncurses testing...')

	# Use vars() to create dictionary of command line switches and text.
	command_args = parser.parse_args()
	argsDict = vars(command_args)
	#print(argsDict)

	initialAuth()
	#cursesTest()

	# Get timeline with 'n' number of tweets
	if command_args.tweetsNum:
		printTimeline(command_args.tweetsNum)
		
	# Start client in streaming mode
	elif command_args.stream:
		getStream()
		
	# Print friends list
	elif command_args.numFriends:
		printFriends(command_args.numFriends)
		
	# send a direct message
	elif command_args.directMessage:
		userDirect = command_args.directMessage[0]
		msgDirect = command_args.directMessage[1]
		directSend(userDirect, msgDirect)

	# update status
	elif command_args.statusUpdate:
		msgStatusUpdate = command_args.statusUpdate[0]
		statusUpdate(command_args.statusUpdate[0])

	elif command_args.cursesTest:
		cursesTest()

	else: print(sys.argv)

if __name__ == '__main__':
	main()

else:
	print("loaded as module...")
