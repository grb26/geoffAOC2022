#!python3

import inputFetcher
import re

inputFile = inputFetcher.getInput('https://adventofcode.com/2022/day/4/input')

# Part 1 objective: 
# Given pairs of ranges ("2-4,6-12"), in how many pairs does one range fully contain the other?
# Part 2 objective:
# How many ranges overlap at all?


cumulativeScore1 = 0
cumulativeScore2 = 0

for line in inputFile.iter_lines():

	# Extract the four values as strings, map the results through the int function, and cast the map to a list
	vals = list(map(int, re.split('[,-]', line.decode())))

	# Identify fully contained ranges
	if (
	( vals[0] >= vals[2] and vals[1] <= vals[3] ) or 
	( vals[0] <= vals[2] and vals[1] >= vals[3] )
	):
		cumulativeScore1 += 1

	# Identify overlapping ranges
	if (
	( vals[0] >= vals[2] and vals[0] <= vals[3] ) or
	( vals[1] >= vals[2] and vals[1] <= vals[3] ) or 
	( vals[2] >= vals[0] and vals[2] <= vals[1] ) or 
	( vals[3] >= vals[0] and vals[3] <= vals[1] )
	):
		cumulativeScore2 += 1



print("Final score is",cumulativeScore1,"for part 1 and",cumulativeScore2,"for part 2.")
