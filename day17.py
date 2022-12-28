#!python3

# Read in the input, which specifies a sequence of wind gusts
import sys
wind = []
for line in sys.stdin:
	wind += line.strip()
# Convert the <> symbols to 1D vectors (positive or negative x increments)
for i in range(len(wind)):
	if wind[i] == '>': 
		wind[i] = 1
	else:
		wind[i] = -1
		

# Define rock types
rocks = [ 	[[True,True,True,True]], 
			[[False,True,False],[True,True,True],[False,True,False]], 
			[[True,True,True],[False,False,True],[False,False,True]], 
			[[True],[True],[True],[True]], 
			[[True,True],[True,True]]
		]
rockwidth = [4,3,3,1,2]
rockheight = [1,3,3,4,2]
numrocktypes = 5

# Keep track of the contents of the cave, and dynamically extend it upward when things land. Start with just the floor.
cave = [ [True,True,True,True,True,True,True] ]
cavewidth = len(cave[0])

def pr(c, r=False):
	if r: print('@', end='')
	elif c: print('#', end='')
	else: print(' ', end='')

def dump(rockid=None, x=2, h=0, showtop=None):
	caveheight = len(cave)-1
	maxh = caveheight
	if rockid: 
		rockw = rockwidth[rockid]
		rocktop = h+rockheight[rockid]-1
		maxh = max(caveheight, rocktop)
	if showtop:
		minh = maxh - showtop
	else:
		minh = 0
	for r in range(maxh,minh,-1):
		print('|', end='')
		if r<=caveheight: 
			caverow = cave[r]
		else:
			caverow = [False for _ in range(cavewidth)]
		if rockid and r >= h and r <= rocktop:
			rr = r-h	# Rock row, i.e. which row of rock are we rendering
			for j in range(cavewidth):
				if j < x or j > x+rockw - 1: pr(caverow[j])
				else: pr(caverow[j],rocks[rockid][rr][j-x])
		else:
			for c in caverow:
				pr(c)
		if r == maxh and r == caveheight:
			print('| <<o h is',caveheight)
		elif r == maxh:
			print('| <')
		elif r == caveheight:
			print('|  <o h is',caveheight)
		else:
			print('|')
	print('+-------+')
	print('/// h=',caveheight, flush=True)

def checkcollisions(rockid, xoffset, hoffset):
	#print('Checking with xoffset hoffset',xoffset,hoffset,'and rock',rock)
	if hoffset < 0 or xoffset < 0:
		#print("Fail1")
		return False						# Below the cave floor, or out of bounds to the left
	if xoffset + rockwidth[rockid] > cavewidth:
		#print("Fail2")
		return False
	caveheight = len(cave)
	for i in range(rockheight[rockid]):
		h = i+hoffset
		#print('i,h',i,h)
		if h < caveheight:
			for j in range(rockwidth[rockid]):
				x = j+xoffset
				#print('i,h,j,x',i,h,j,x)
				if x >= cavewidth:
					return False			# out of bounds to the right
				if cave[h][x] and rocks[rockid][i][j]:
					return False			# Overlap between falling rock and existing cave structures
	#print('No collision')
	return True


# Part 1: Simulate 2022 rocks falling
# Part 2: Simulate 1,000,000,000,000 rocks falling... except that would take about 130 days to run. 
#   Can we find any repeating pattern? The wind pattern doesn't repeat, so any pattern will be a multiple of len(wind).
#   So, let's keep track of the final position of each rock and compare it with n*len(wind) positions ago.
#   If we get a certain number of matches in a row, it might be a good candidate.
numrocks = 1000000000000			# Let it run as long as it takes to find a repeating pattern. In practice, we will only need a couple of million rocks.
p1numrocks = 2022					# Target for part 1
windcounter = 0
patternthreshold = 30				# Want to be really sure it's a genuine repeating pattern. If you just check (say) 5 entries, there are some coincidental repeats before the true pattern emerges.
minpattern = 1500 					# Magic number for performance tuning. I don't understand how this can be less than len(wind) though, as the wind pattern doesn't repeat within the input file.
record = []
for r in range(numrocks):
	#print('~~~~~ NEXT ROCK ~~~~~')
	h = len(cave)+3			# Start height of the base of the falling block is 3 units above the current highest bit of rock
	x = 2					# Start position is 2 units from the left edge
	rockid = r % numrocktypes
	falling = True
	#dump(rock,x,h)
	while falling:
		# Blown by wind
		winddir = wind[windcounter % len(wind)]
		if checkcollisions(rockid, x+winddir, h):
			x += winddir
		windcounter += 1

		# Pulled by gravity
		if checkcollisions(rockid, x, h-1):
			h -= 1
		else:
			falling = False

	# Rock has finished falling, so solidify its final position in the cave structure
	cave += [ [0,0,0,0,0,0,0] for _ in range(0,h+rockheight[rockid]-len(cave)) ]		# Extend the cave array to hold the new rock (if necessary)
	for i in range(rockheight[rockid]):
		for j in range(rockwidth[rockid]):
			cave[h+i][x+j] = cave[h+i][x+j] or rocks[rockid][i][j]

	if r == p1numrocks:
		dump(rockid,2,len(cave)+3,showtop=30)
		print('Part 1:',len(cave)-1)

	# Attempt to detect repeating patterns
	record.append([x,len(cave)-1])						# Store a record containing the x position of the rock, and the height of the tower
	if r <= minpattern+patternthreshold: continue		# Need to have enough rocks for at least one full cycle and <patternthreshold> steps of the second cycle
	r1 = r % minpattern									# r1 is the rock where the pattern started (actually it's not, r1-patternthreshold is, but it's now a repeating pattern so it doesn't really matter where we claim it starts)
	if r1 < patternthreshold: continue					# Don't look if we would have to go beyond the base of the tower
	patternlength = r - r1
	match = True
	for p in range(patternthreshold):					# Check for a match in the x-coords across the previous entries
		if record[r1-p][0] != record[r-p][0]:
			match = False
			break
	if match:
		#print('Pattern identified at rock',r)
		#for k in range(patternthreshold):
		#	print("Rock",r1-k,": x",record[r1-k][0],"h",record[r1-k][1],"| Rock",r-k,"x",record[r-k][0],"h",record[r-k][1],"| Height difference is",record[r-k][1]-record[r1-k][1])
		hdiff = record[r][1]-record[r1][1]
		#print('Pattern length is',patternlength)
		#print('Height difference is',hdiff)
		patterns = int((numrocks-r1)/patternlength)
		fullreplength = patterns*patternlength					# length of the sequence made up of full repetitions of the pattern
		repheight = patterns*hdiff								# height that will be contributed by the full repetitions
		remainder = numrocks - fullreplength - r1 - 1			# number of rocks remaining after the full repetitions have happened. (-1 because there was a rock zero)
		extraheight = record[r1+remainder][1] - record[r1][1]	# height that will be gained by those extra rocks
		finalheight = record[r1][1] + repheight + extraheight
		print('Part 2:',finalheight)
		exit()

print('Sorry, no pattern found. Brute force solution to part 2 was:',len(cave)-1)


