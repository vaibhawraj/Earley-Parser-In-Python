import re

def isDecimal(s):
	mobj = re.match("^[0-9]*\.[0-9]+$",s)
	if mobj:
		return True
	else:
		return False

def isString(s):
	mobj = re.match("^[a-zA-Z]+(-[a-zA-Z]+)?$",s)
	if mobj:
		return True
	else:
		return False

def isInt(s):
	mobj = re.match("^[0-9]+$",s)    #Matches Int
	if mobj:
		return True
	else:
		return False