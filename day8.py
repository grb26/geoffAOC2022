#!python3

import inputFetcher
import re

inputFile = inputFetcher.getInput('https://adventofcode.com/2022/day/8/input')

# Given a grid of tree heights...
# Part 1: figure out which are visible from the edges
# Part 2: identify the tree that can see most other trees ("scenic score" = PRODUCT of trees seen in each direction)

# Read in the grid - decode bytes to string, cast string to list to split into characters, then map through int() to get a list of numbers
trees = []
for line in inputFile.iter_lines():
	trees.append(list(map(int, list(line.decode()))))
# Readability note: the resulting coordinate system has (0,0) at the TOP left, and the y coordinate is the first index.
# So trees[3][1] is the fourth row DOWN, and the second column across. (Because both start at zero.)

# Assume that the grid is rectangular (i.e. no missing bits), but how big is it?
w = len(trees[0])
h = len(trees)

# PART 1
# Create an array to hold the visible trees, and initialize with zeroes
visible = []
for i in range(h):
	visible.append([0]*w)

# Scan for visibility from the left
for i in range(h):
	tallest = -1
	for j in range(w):
		if trees[i][j] > tallest:
			visible[i][j] = 1
			tallest = trees[i][j]

# Scan from the right
for i in range(h):
	tallest = -1
	for j in range(w-1, -1, -1):
		if trees[i][j] > tallest:
			visible[i][j] = 1
			tallest = trees[i][j]

# Scan from the top
for j in range(w):
	tallest = -1
	for i in range(h):
		if trees[i][j] > tallest:
			visible[i][j] = 1
			tallest = trees[i][j]

# Scan from the right
for j in range(w):
	tallest = -1
	for i in range(h-1, -1, -1):
		if trees[i][j] > tallest:
			visible[i][j] = 1
			tallest = trees[i][j]

print('Total visible trees from outside the plantation:',sum(map(sum,visible)))

# PART 2
# Create an array to hold the scores trees, and initialize with zeroes
bestscore = 0

# For each tree (excluding the edges, which are guaranteed a zero score)...
for y in range(1,h-1):
	for x in range(1,w-1):

		left, right, up, down = 0, 0, 0, 0
		myheight = trees[y][x]

		# Look left
		for j in range(x-1,-1,-1):
			left += 1
			if trees[y][j]>=myheight: break

		# Look right
		for j in range(x+1,w,1):
			right += 1
			if trees[y][j]>=myheight: break

		# Look up
		for i in range(y-1,-1,-1):
			up += 1
			if trees[i][x]>=myheight: break

		# Look down
		for i in range(y+1,h,1):
			down += 1
			if trees[i][x]>=myheight: break

		myscore = left * right * up * down
		bestscore = max(myscore, bestscore)

print('Maximum scenic score:',bestscore)
