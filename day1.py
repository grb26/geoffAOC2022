#!python3

import inputFetcher
import operator

inputFile = inputFetcher.getInput('https://adventofcode.com/2022/day/1/input')

scores = {}	# Record scores in a dictionary, structure { elf_ID:score }
			# Is a calorie count really a "score"? Yeah, that's certainly my relationship with food.
thisElf = 1
thisScore = 0

# Read the input from the adventofcode website
for line in inputFile.iter_lines():

	# Lines come back as byte arrays. If it's an empty byte array (b'') then record this elf's score and move on to the next
	if line == b'':
		scores[thisElf] = thisScore
		thisScore = 0
		thisElf += 1

	else:
		# Another row for the same elf, so just add it to the total and continue
		thisScore += int(line.decode())

# Edge case: we don't get a blank line at the end of the input, so need to record the score of the last elf
scores[thisElf] = thisScore

# Now sort the scores by value and take the top N elves
topElves = sorted(scores.items(), key=operator.itemgetter(1), reverse=True)
combinedCalories = 0
topN = 3
for i in range(0,topN):
	print("Elf",topElves[i][0],"scored",topElves[i][1])
	combinedCalories += topElves[i][1]
print("The combined calories carried by the top",topN,"elves is",combinedCalories)