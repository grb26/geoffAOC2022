#!python3

import inputFetcher
import operator

inputFile = inputFetcher.getInput('https://adventofcode.com/2022/day/2/input')

# Data input format
# Column 1: A=Rock, B=Paper, C=Scissors
# Column 2 (part1): X=Rock, Y=Paper, Z=Scissors. 
# Column 2 (part2): X=lose, Y=draw, Z=win

# Scoring system
# Score for the shape you selected (1 for Rock, 2 for Paper, and 3 for Scissors) 
# plus the score for the outcome (0 if you lost, 3 if the round was a draw, and 6 if you won).

scoreMatrix1 = { 'A X':1+3, 'A Y':2+6, 'A Z':3+0, 'B X':1+0, 'B Y':2+3, 'B Z':3+6, 'C X':1+6, 'C Y':2+0, 'C Z':3+3 }
scoreMatrix2 = { 'A X':3+0, 'A Y':1+3, 'A Z':2+6, 'B X':1+0, 'B Y':2+3, 'B Z':3+6, 'C X':2+0, 'C Y':3+3, 'C Z':1+6 }

cumulativeScore1 = 0
cumulativeScore2 = 0

for line in inputFile.iter_lines():
	play = line.decode()
	cumulativeScore1 += scoreMatrix1[play]
	cumulativeScore2 += scoreMatrix2[play]

print("Final score is",cumulativeScore1,"under part 1 assumptions, and",cumulativeScore2,"under part 2 assumptions.")
