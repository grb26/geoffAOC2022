#!python3

import inputFetcher

inputFile = inputFetcher.getInput('https://adventofcode.com/2022/day/9/input')

# Given a sequence of moves of a "head" around an arbitrary grid...
# Part 1: figure out how many squares the elastically-attached tail visits if the rope is of length 1
# Part 2: same, but longer rope

# Starting positions
visited = { '[0, 0]':1 }
knots = 10 					# Part 1: knots = 2; part 2: knots = 10
rope = [[0,0] for i in range(knots)]

# Input directions are U, D, L, R. Define a helper to convert into vectors
dir2vec = { 'U':[0,1], 'D':[0,-1], 'L':[-1,0], 'R':[1,0] }

# Weird that this isn't a built-in...
def sign(num):
	if num == 0: return 0
	elif num <0: return -1
	else: return 1

# Iterate over the input
for line in inputFile.iter_lines():

	# Read the input
	direction, stps = line.decode().split()
	steps = int(stps)

	# Model the movement
	for s in range(steps):

		# Move the head...
		rope[0] = [i+j for i,j in zip(rope[0], dir2vec[direction])]

		# ...and let each subsequent knot follow the preceding one
		for i in range(1,knots):
			if abs(rope[i][0]-rope[i-1][0])>1 or abs(rope[i][1]-rope[i-1][1])>1:
				rope[i][0] += sign(rope[i-1][0]-rope[i][0])
				rope[i][1] += sign(rope[i-1][1]-rope[i][1])

		visited[str(rope[knots-1])]=1
		
# How many squares have we visited?
print('Tail visited',len(visited),'positions')



