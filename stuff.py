#!/usr/local/bin/python3

__author__ = 'SomeClown'


class myFile(object):

    def __init__(self, myfilename: object, myflag: object, mycontents: object) -> object:
        self.myfilename = myfilename
        self.myflag = myflag
        self.mycontents = mycontents
    
    # Write a file
    def writeFile(self, myfilename, myflag, mycontents):
        try:
            with open(myfilename, myflag, mycontents) as outfile:
                return self.myfilename
        except IOError:
            print('File ' + filename + ' does not exist... \n')

    # Read a file
    def readFile(self, myfilename, myflag, mycontents):
        try:
            with open(myfilename, myflag, mycontents) as infile:
                return self.myfilename
        except IOError:
            print('File ' + myfilename, ' does not exist, or something went wrong. \n')
    
    # Modify an input file        
    def modFile(self, myfilename, myflag, mycontents):
        try:
            with open(myfilename, myflag, mycontents) as modfile:
                return self.myfilename
        except IOError:
            print('Something went wrong with operation on ' + myfilename + '\n')
