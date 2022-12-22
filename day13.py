#!python3

# Read in the input file, and store in a list. Even indicies will be "left" values, odd will be "right".
import inputFetcher
inputFile = inputFetcher.getInput('https://adventofcode.com/2022/day/13/input')
inputs = []
for line in inputFile.iter_lines():
	if not line == b'':
		inputs.append(line.decode())

# Function to parse a string like '[1,[2,3],4]' into an actual list [1, [2, 3], 4]
def parse(txt):
	result = parserecursively(txt[1:-1])	# Strip the outer []s because we initialise result with an empty array
	return result
import re
def parserecursively(txt, pos=0):
	result = []
	while pos < len(txt):
		if txt[pos] == '[':
			pos, item = parserecursively(txt,pos+1)
			result.append(item)
		elif txt[pos] == ']':
			return pos+1, result
		elif txt[pos] == ',':
			pos += 1
		else:
			match = re.search(r'^(\d+)',txt[pos:])
			if match:
				result.append(int(match[1]))
				pos += len(match[1])
	return result

# Function to compare two lists using some weird rules
# Implicit rule 0: the first unambiguously true or false test determines the outcome; if they're equal, keep comparing more values.
# So to do this recursively, we will need three possible return values (true, false, continue)
false = 0
true = 1
cont = 2
def rightorder(left, right):
	i = 0

	# Rule 1: if both items are ints, left should be smaller
	if isinstance(left, int) and isinstance(right, int):
		if left > right: 
			return false
		elif left == right:
			return cont
		else:
			return true

	# Rule 2: if both items are lists, compare the contents in order - do this by recursing for each item
	if isinstance(left, list) and isinstance(right, list):
		while i<len(left) and i<len(right):
			check = rightorder(left[i], right[i]) 
			if check == false:
				return false
			elif check == true:
				return true
			i += 1
		# Reached the end of one of the lists, so apply the second half of rule 2: the left list should run out of items first
		if len(left) > len(right): 
			return false
		elif len(left) < len(right):
			return true
		else:
			return cont

	# Rule 3: if one side is an int and the other is a list, pretend the int is a list of length 1
	if isinstance(left, int) and isinstance(right, list): 
		check = rightorder([left], right)
		return check
	if isinstance(left, list) and isinstance(right, int): 
		check = rightorder(left, [right])
		return check

	# One of the conditions above must be true (unless the inputs are corrupt), so it should be impossible to get here 
	print('Surely unreachable?')
	return True
	# End of rightorder() function


# Part 1: Walk through the list and add up the indicies of all matching pairs
score1 = 0
for i in range(0, len(inputs), 2):
	j = int(i/2) + 1
	if rightorder(parse(inputs[i]), parse(inputs[i+1])) == true:
		score1 += j
print("Part 1:",score1)

# Part 2: Now we need to sort the list. It's a ridiculous comparison function, so we'll brute force it with a manual insertion sort
srtd = ['[[2]]', '[[6]]']
for i in range(len(inputs)):
	for j in range(len(srtd)):
		if rightorder(parse(inputs[i]), parse(srtd[j])) == true:
			srtd.insert(j, inputs[i])
			break
print("Part 2:",(srtd.index('[[2]]')+1) * (srtd.index('[[6]]')+1))