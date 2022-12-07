#!python3

import inputFetcher
import re

inputFile = inputFetcher.getInput('https://adventofcode.com/2022/day/6/input')

# Given a long random-looking string...
# Part 1: Find the first group of four unique characters (return the position of the end of the group)
# Part 2: Same, but 14 unique chars

def firstUnique(n, s):
	i = n
	while (len(dict(zip(s[i-n:i],s[i-n:i]))) < n):		# Clear code documents itself, no need for explanatory comments
		i += 1
	return i

for linebytes in inputFile.iter_lines():
	line = linebytes.decode()
	print("Part 1:", firstUnique(4,line))
	print("Part 2:", firstUnique(14,line))