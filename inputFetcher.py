#!python3

import requests
import config

def getInput(url):
	jar = requests.cookies.RequestsCookieJar()
	jar.set('_ga', config.myGA, domain='.adventofcode.com', path='/')
	jar.set('_gid', config.myGID, domain='.adventofcode.com', path='/')
	jar.set('session', config.mySession, domain='.adventofcode.com', path='/')
	return requests.get(url, cookies=jar)