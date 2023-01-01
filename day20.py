#!python3
import sys
from collections import deque

lst1 = []
lst2 = []
magic_number=811589153

# Read in the input
n=0
for l in sys.stdin:
	line = l.strip()
	if line == '': continue
	lst1.append([n, int(line)])
	lst2.append([n, int(line)*magic_number])
	n += 1

def dump():
	print([ _[1] for _ in d ])

def mix(d):
	# Run through the items in their original order
	for i in range(n):

		# Find item i
		for j in range(n):
			if d[j][0] == i:
				break

		shift = d[j][1]

		d.rotate(-j)	# Bring the item to the front of the queue
		item = d.popleft()
		d.rotate(-shift)	# Move to the new position
		d.appendleft(item)
	
		#dump()

def score(d):
	retval = 0
	# Find the zero
	for j in range(n): 
		if d[j][1] ==0: 
			break
	d.rotate(-j)
	# Extract the required values
	for p in [1000, 2000, 3000]:
		retval += d[p%n][1]
	return retval

# Part 1
d = deque(lst1, maxlen=n)
mix(d)
print("Part 1:",score(d))

# Part 2
d = deque(lst2, maxlen=n)
for i in range(10): 
	mix(d)
print("Part 2:",score(d))


