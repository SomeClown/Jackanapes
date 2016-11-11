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

