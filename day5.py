#!python3

import inputFetcher
import re

inputFile = inputFetcher.getInput('https://adventofcode.com/2022/day/5/input')

# Given a graphical description of some towers (stacks of crates), plus some moves, what is the resulting arrangement?
# Part 1: Tower of Hannoy style moves
# Part 2: Move multiple crates in one move

debug = False
def dump(ts):
	if debug:
		total=0
		for t in ts:
			total += len(t)
			print(t)
		print("Size:",total)

state = 0			# Starting state
towers = []			# Array of towers
n = 0				# Number of towers - will be detected in state 0

mode = 2			# Answer part 1 or part 2?

for linebytes in inputFile.iter_lines():

	line = linebytes.decode()

	# We receive a diagram, then the labels for the diagram, then a blank line, then the moves.
	# Use a simple state machine to keep track of which section we're in.
	
	# State 0: Figure out the number of towers
	# The diagram is space-padded, so all lines are the same width. Can therefore calculate
	# the number of towers from the length of the first line.
	if state == 0:
		n = int((len(line)+1)/4)	# Each column takes up 3 chars, plus a space between each
		for i in range(n):
			towers.append([])
		state = 1

	# Ignore the labels and the blank line - state 2 does nothing
	if line == '' or re.search(r'^[ \d]+$', line):
		state = 2

	if re.search('move', line):
		state = 3

	# State 1: populate the starting arrangement
	if state == 1:
		for i in range(n):
			pos = 4*i + 1
			if line[pos] != ' ':
				towers[i]= [ line[pos] ] + towers[i]

	# State 3: process move instructions
	if state == 3:
		print(line)
		[num, frm, to] = [int(x) for x in re.findall(r'\d+', line)]	# Format: "move 6 from 4 to 6"
		if mode == 1:	# Iteratively move one crate at a time (hence order reversed)
			for i in range(num):
				towers[to-1].append(towers[frm-1].pop())
		if mode == 2:	# Move all crates in one batch (hence order preserved)
			towers[to-1] += towers[frm-1][-num:]
			towers[frm-1] = towers[frm-1][:len(towers[frm-1])-num]
		dump(towers)

ans = ''
for t in towers:
	ans += t[-1]
print("Part",mode,"result:",ans)
