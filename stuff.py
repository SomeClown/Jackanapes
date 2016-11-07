#!/usr/local/bin/python3

def writeFile(fileName):
	try:
		home = os.path.expanduser("~")
		configFile = (home + '/.packetqueue/' + str(globalVars.user.screen_name) + fileName)
		with open(configFile, 'r') as inFile:
			return
	
	except IOError:
		print('File ' + filename + ' does not exist... \n')

