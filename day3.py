#!python3

import inputFetcher

inputFile = inputFetcher.getInput('https://adventofcode.com/2022/day/3/input')

# Part 1 objective: 
# 1. Split each input in half
# 2. Identify the ONE common letter between each half
# 3. Calculate the total score across all rows (a-z:1-26, A-Z:27-52)

def getScore(letter):
	asciival = ord(letter)
	# ASCII codes have lowercase in the range 97-122 and uppercase 65-90
	if asciival>95:
		return asciival - 97 + 1
	else:
		return asciival - 65 + 27

cumulativeScore1 = 0
cumulativeScore2 = 0
linebuffer = []

for line in inputFile.iter_lines():

	# Split the line into two halves
	both = line.decode()
	half1 = both[:int(len(both)/2)]
	half2 = both[int(len(both)/2):]

	# Step through one half, to find the character that also appears in the other half
	for c in half1:
		if c in half2:
			cumulativeScore1 += getScore(c)
			break

	# For part 2, analyse groups of 3
	linebuffer.append(both)
	if len(linebuffer)==3:
		for c in linebuffer[0]:
			if c in linebuffer[1] and c in linebuffer[2]:
				# Found a match across all three, so record the score and reset the buffer
				cumulativeScore2 += getScore(c)
				linebuffer=[]
				break;



print("Final score is",cumulativeScore1,"for part 1 and",cumulativeScore2,"for part 2.")
