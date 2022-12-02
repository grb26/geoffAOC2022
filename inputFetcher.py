#!python3

# Helper function because it looks like we'll be reading input files a lot.
# AdventOfCode.com requires you to authenticate with GitHub (or other OAuth provider), so can't just directly pull the page. 
# Simple approach: steal the cookies from the browser, paste them into a config file, and away we go. 
# TO-DO when bored: do a proper OAuth redirect to get an authentication token

import requests
import config	# config.py just contains a line for each variable used: myGA=xxx, myGID=xxx, mySession=xxxxxxx

def getInput(url):
	jar = requests.cookies.RequestsCookieJar()
	jar.set('_ga', config.myGA, domain='.adventofcode.com', path='/')
	jar.set('_gid', config.myGID, domain='.adventofcode.com', path='/')
	jar.set('session', config.mySession, domain='.adventofcode.com', path='/')
	return requests.get(url, cookies=jar)