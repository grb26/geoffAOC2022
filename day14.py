#!python3

# Read in the input file, and store each coordinate in a list-of-lists structure.
import re
import inputFetcher
inputFile = inputFetcher.getInput('https://adventofcode.com/2022/day/14/input')
inputs = []
maxx = 0
minx = 1000000
maxy = 0
for line in inputFile.iter_lines():
	thislist = []
	for coord in re.findall(r'\d+,\d+', line.decode()):
		[x,y] = map(int, coord.split(','))
		thislist.append([x,y])
		if x > maxx: maxx = x
		if x < minx: minx = x
		if y > maxy: maxy = y
	inputs.append(thislist)


# Create a map of the cave, going just a few squares wider than we need
leftxmargin = 100 									# Magic numbers tuned to allow visualisation. Could just use the coords as given, with width 0-10k, but it won't fit on my screen without preposterous zooming.
rightxmargin = 200
xoffset = minx - leftxmargin						# Correction to map xcoords to the visualisable range
width = leftxmargin + rightxmargin + maxx - minx	# Resulting width of the slice of cave to be modelled
ymargin = 2 										# Gap specified in part 2
height = ymargin + maxy								# Height of the modelled cave
cave = [ ['.']*width for _ in range(height) ]		# Initialise the cave with .'s to represent empty space
cave.append(['#']*width)							# Add the floor for part 2

# Helper function to get the sign of a number
def sign(num):
	if num == 0: return 0
	elif num <0: return -1
	else: return 1

# Helper function to print the cave map
def dump():
	for row in cave:
		print(''.join(row))

# Parse the inputs into rock drawn on the cave map
for path in inputs:
	for i in range(len(path)-1):
		stepx = sign(path[i+1][0] - path[i][0])
		stepy = sign(path[i+1][1] - path[i][1])
		cursor = path[i].copy()
		cave[cursor[1]][cursor[0]-xoffset] = '#'
		while cursor != path[i+1]:
			cursor[0] += stepx
			cursor[1] += stepy
			cave[cursor[1]][cursor[0]-xoffset] = '#'

dump()

# Simulate some sand
startpoint = [500-xoffset, 0]
abyss = False					# Flag to mark the first grain to fall into the abyss (or, as it turns out, on to the floor)
grain = 0 						# Counter to keep track of the number of grains of sand
while True:
	grain += 1
	cursor = startpoint.copy()			# Take a copy because otherwise updating cursor would overwrite startpoint
	run = True
	while run:
		if cave[cursor[1]+1][cursor[0]] == '.':				# Sand falls vertically by preference...
			cursor[1] += 1
		elif cave[cursor[1]+1][cursor[0]-1] == '.':			# ...or diagonally left...
			cursor[1] += 1
			cursor[0] -= 1
		elif cave[cursor[1]+1][cursor[0]+1] == '.':			# ...or diagonally right if it can't go left...
			cursor[1] += 1
			cursor[0] += 1
		else:												# ...or comes to rest if it can't go down at all.
			run = False

		if cursor[1] == height-1 and not abyss:				# Detect part 1 finish condition
			abyss = True
			print('Part 1: the structure was able to accommodate',grain-1,'grains of sand before hitting the floor')
		
	cave[cursor[1]][cursor[0]] = 'o'						# Grain has now stopped falling, so draw it on the map

	if cursor[1] == 0:										# Detect part 2 finish condition
		print('Part 2: total of',grain,'grains required to reach and plug the source')
		break;

dump()
