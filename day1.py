#!python3

import inputFetcher
import operator

inputFile = inputFetcher.getInput('https://adventofcode.com/2022/day/1/input')

scores = {}
thisElf = 1
thisScore = 0

for line in inputFile.iter_lines():
	if line == b'':
		scores[thisElf] = thisScore
		#print("Elf",thisElf,"scores",thisScore)
		thisScore = 0
		thisElf += 1

	else:
		thisScore += int(line.decode())

# Edge case: we don't get a blank line at the end, so need to check if the last elf was the winner
scores[thisElf] = thisScore
#print("Elf",thisElf,"scores",thisScore)

topElves = sorted(scores.items(), key=operator.itemgetter(1), reverse=True)
combinedCalories = 0
topN = 3
for i in range(0,topN):
	print("Elf",topElves[i][0],"scored",topElves[i][1])
	combinedCalories += topElves[i][1]
print("The combined calories carried by the top",topN,"elves is",combinedCalories)