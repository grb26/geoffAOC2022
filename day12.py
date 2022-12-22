#!python3

import inputFetcher

inputFile = inputFetcher.getInput('https://adventofcode.com/2022/day/12/input')

######
# Read in the input, and create a terrain map with the altitude as an integer in the range 1-26
terrain = []		# Altitude of each coordinate, populated from the input file
start = (0,0)
end = (0,0)
for l in inputFile.iter_lines():

	line = [int(byte)-96 for byte in l]		# Convert array of bytes to array of ints. Ascii('a') == 97, so subtract 96 to bring the range to 1-26.
	
	# Convert 'S' and 'E' characters to their correct altitudes
	if b'S' in l:
		start = (len(terrain) , l.find(b'S'))
		line[l.find(b'S')] = 1
	if b'E' in l:
		end = (len(terrain) , l.find(b'E'))
		line[l.find(b'E')] = 26
	
	terrain.append(line)

######
# Function to test whether a square is a valid step from the current location
def isreachable(x, y, currenth, steps, terrain, dist):
	if x < 0: return False
	if y < 0: return False
	if x > len(terrain)-1: return False
	if y > len(terrain[0])-1: return False
	if dist[x][y] > -1: return False
	if terrain[x][y] > currenth + 1: return False
	return True

######
# Function to iteratively populate a map of distances (number of steps) from the start
def findpaths(startpoint, endpoint, terrain):
	# Initialise a clean distance array with dummy values
	dist = []
	for i in range(len(terrain)):
		dist.append([])
		for j in range(len(terrain[0])):
			dist[i].append(-1)
	dist[startpoint[0]][startpoint[1]] = 0

	# q is a list of pointers to FIFO queues of reachable points, one queue for each step taken
	step = 0
	q = []
	q.append([startpoint])															# Initialise with q[0] pointing to a list containing a single reachable point for step zero

	# For each reachable point, find subsequent reachable points, and keep going until we either win or run out of points
	for s in q:
		if len(s) == 0: break														# No steps added for this list, so we're stuck. Stop and return -1.
		q.append([])																# Create an empty list (index will be q[step+1]) to hold the points reachable in the next step
		for (i,j) in q[step]:
			if dist[i][j] == step:													# If we've already visited this point, dist[i][j] will be less than step, so skip it
				for (I, J) in [ (i+1,j), (i-1,j), (i,j+1), (i,j-1) ]:
					if isreachable(I, J, terrain[i][j], step+1, terrain, dist):
						if (I,J) == endpoint: return step + 1 						# Woohoo!
						dist[I][J] = step + 1
						q[step+1].append((I,J))
		step += 1
	return -1


######
# Do the work!
# Part 1: find the shortest route from the specified start point
best = findpaths(start,end, terrain)
print('Part 1:', best)

# Part 2: find the shortest route from any point with altitude 1
for i in range(len(terrain)):
	for j in range(len(terrain[i])):
		if terrain[i][j] == 1:
			thisn = findpaths((i,j),end, terrain)
			if thisn > 0 and thisn<best:
				best = thisn
print('Part 2:', best)