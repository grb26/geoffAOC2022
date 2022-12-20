#!python3

import inputFetcher
import operator
import re

inputFile = inputFetcher.getInput('https://adventofcode.com/2022/day/11/input')

# Given a description of monkey shennanigans...
# 1: Calculate the product of the inspections of the two most active monkeys
# 2: Same again, with different parameters (which make the numbers go ridiculous, so need to do something to keep them manageable)

# 2D array of items held by each monkey - first index is monkey ID, second index is object ID
# Make two copies, for parts 1 & 2
items1 = []
items2 = []

# 1D array to keep track of the number of inspections performed by each monkey
inspections = []

# What does each monkey do to the nervousness score?
rule_operator = []
rule_operand = []

# What divisibility test does each monkey apply?
test = []

# Monkey to throw to if true/false
iftrue = []
iffalse = []

### Part 0: parse the inputs

# Monkey index - initialise outside loop to set scope
m=0

# Read in the input
for l in inputFile.iter_lines():
	line = l.decode()

	if re.search(r'^Monkey',line):
		m = int(re.search(r'^Monkey (\d+):',line)[1])

	if re.search(r'Starting',line):
		items1.append([ int(x) for x in (re.findall(r'(\d+)', line))])
		items2.append([ int(x) for x in (re.findall(r'(\d+)', line))])

	if re.search(r'Operation: new = old \* old',line):
		rule_operator.append(operator.pow)
		rule_operand.append(2)
	elif re.search(r'Operation: new = old \+ \d+',line):
		rule_operator.append(operator.add)
		rule_operand.append(int(re.search(r'old \+ (\d+)',line)[1]))
	elif re.search(r'Operation: new = old \* \d+',line):
		rule_operator.append(operator.mul)
		rule_operand.append(int(re.search(r'old \* (\d+)',line)[1]))
	
	if re.search(r'Test:', line):
		test.append(int(re.search(r'divisible by (\d+)',line)[1]))

	if re.search('If true', line):
		iftrue.append(int(re.search(r'throw to monkey (\d+)',line)[1]))
	if re.search('If false', line):
		iffalse.append(int(re.search(r'throw to monkey (\d+)',line)[1]))

### Part 1
# Simulate the simian shennanigans
rounds = 20
inspections = [0]*len(items1)
for r in range(rounds):
	for m in range(len(items1)):
		while len(items1[m])>0:
			inspections[m] += 1
			x = items1[m][0]
			x = rule_operator[m](x, rule_operand[m])
			x = int(x/3)								# This is the only line that changes between parts 1 & 2
			if x % test[m] == 0:
				items1[iftrue[m]].append(x)
			else:
				items1[iffalse[m]].append(x)
			items1[m] = items1[m][1:]
			
top2 = sorted(inspections)[-2:]
score = top2[0] * top2[1]
print('Part 1',score) 

### Part 2
# Numbers get much larger, so we're going to need to use modulo arithmetic to prevent overflow errors
# All the tests are for divisibility by primes, so if we work modulo ${the product of all of the primes}, we shouldn't lose anything important
base = 1
for t in test:
	base *= t

rounds = 10000
inspections = [0]*len(items2)
for r in range(rounds):
	for m in range(len(items2)):
		while len(items2[m])>0:
			inspections[m] += 1
			x = items2[m][0]
			x = rule_operator[m](x, rule_operand[m])
			x = x % base								# In part 2, we don't divide by 3, but we do need to work modulo the base instead
			if x % test[m] == 0:
				items2[iftrue[m]].append(x)
			else:
				items2[iffalse[m]].append(x)
			items2[m] = items2[m][1:]
			
top2 = sorted(inspections)[-2:]
score = top2[0] * top2[1]
print('Part 2',score)
