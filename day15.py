#!python3

# We're going to be using "Manhattan distance", which is pretty easy to calculate:
def dist(x1, y1, x2, y2):
	return (abs(x1-x2)+abs(y1-y2))

# Read in the input file, and store in a list-of-lists structure.
# Each item contains four values, representing the x & y coordinates of the sensor and nearest detected beacon
import re
import inputFetcher
inputFile = inputFetcher.getInput('https://adventofcode.com/2022/day/15/input')
inputs = []
for line in inputFile.iter_lines():
	thislist = []
	for numstr in re.findall(r'\-?\d+', line.decode()):
		thislist.append(int(numstr))
	thislist.append(dist(thislist[0], thislist[1], thislist[2], thislist[3]))
	inputs.append(thislist)

# Part 1: how many positions cannot contain a beacon in row 2e6?
y = 2000000		# y value of the row we're interested in
xnot = {}		# dictionary to store ruled-out x values
for [sx, sy, bx, by, sensordist] in inputs:
	# Check whether any point on the row is in range
	if abs(y-sy) < sensordist:
		# We're ruling out some points! How many in each direction?
		x = sensordist - abs(y-sy)
		for offset in range(x+1):
			xnot[sx+offset]=1
			xnot[sx-offset]=1

# Possible error to be corrected: if there are any sensors on the target row, that space can't contain a beacon; if there are any beacons, it can't NOT contain a beacon.
for [sx, sy, bx, by, sensordist] in inputs:
	if sy == y:
		xnot[sx]=1
	if by == y and bx in xnot:
		del(xnot[bx])

print("Part 1:",len(xnot))

# Part 2: in the space [x.y] := [0..4e6, 0..4e6], there is only one point that could contain an undetected beacon. 
# That means that the distance between the point and a sensor is greater than the distance between sensor and beacon for EVERY line in the input.
found = False
x = 0
y = 0
while x <= 4000000 and not found:
	print(x)	# Takes a minute or two to brute-force the search space, so this shows that progress is happening
	while y <= 4000000 and not found:
		found = True
		for [sx, sy, bx, by, sensordist] in inputs:
			if dist(x, y, sx, sy) <= sensordist:
				found = False
				y = sy + sensordist - abs(sx - x)		# Jump straight to the bottom of the coverage zone of the current sensor - skips a few hundred thousand evaluations
				break
		if not found:
			y += 1
	if not found:
		x += 1
		y = 0

print('Checking:')
for [sx, sy, bx, by, sensordist] in inputs:
	print(sx, sy, bx, by, sensordist, dist(sx, sy, x, y), 'so this sensor falls short by',dist(sx, sy, x, y) - sensordist)
print("Part 2: Coords are",x,y,"frequency is", int(x*4e6 + y))
 