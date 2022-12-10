#!python3

import inputFetcher

inputFile = inputFetcher.getInput('https://adventofcode.com/2022/day/10/input')

# Given a sequence of CPU instructions, calculate the x register, then render the output of a CRT controlled by x

# Array to keep track of the history of x values
xhist = [1]

# Read the input file and calculate the value of x at each clock cycle
for line in inputFile.iter_lines():

	if line == b'noop':
		xhist.append(xhist[-1])		# No change to x, so copy the last value

	if line[0:4] == b'addx':
		xhist.append(xhist[-1])
		xhist.append(xhist[-1] + int(line[5:]))

# Part 1: calculate the sum.product of x*cycle at certain cycle numbers
interesting_values = [20, 60, 100, 140, 180, 220]
part1score = sum([ c * xhist[c-1] for c in interesting_values])
print("Part 1:", part1score)

# Part 2: render the screen given by x
for row in range(6):
	for col in range(40):
		
		cycle = col + 40*row
		x = xhist[cycle]

		if col > x-2 and col < x+2:
			print('#', end='')
		else:
			print(' ', end='')

	print()
