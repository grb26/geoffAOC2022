#!python3

# Read in the input, which specifies a sequence of wind gusts
import sys
cubes = []
maxextent = None
minextent = None
for line in sys.stdin:
	if line.strip() == '': continue
	cube = list(map(int,line.strip().split(',')))
	cubes.append(cube)
	if not maxextent:
		maxextent = cube.copy()
		minextent = cube.copy()
	for i in [0,1,2]:
		if cube[i] > maxextent[i]: maxextent[i] = cube[i]
		if cube[i] < minextent[i]: minextent[i] = cube[i]

# Iterate through each cube, and check whether each neighbour is part of the droplet
neighbours = [ [0,0,1], [0,0,-1], [0,1,0], [0,-1,0], [1,0,0], [-1,0,0] ]
surf = 0
candidates = []		# Void cubes that could potentially be bubbles
for c in cubes:
	for n in neighbours:
		check = [ i+j for i,j in zip(c,n) ]
		if not check in cubes:
			surf += 1
			if not check in candidates: candidates.append(check)

# Now check each candidate and see if we can identify a bubble
bubble = []
outside = []

# A void is a bubble if all neighbours are either bubble or rock; not if it touches empty space. 
#    Use a floodfill algorithm to populate a list of connected points. As soon as* any point is 
#    out of bounds, we know it's exposed; if we run out of void spaces without going out of bounds
#    then it could be a bubble. Return boolean couldBeBubble, modify the supplied list in place
#    to add connected points as we recurse.
#
#    * note that returing  "as soon as" means we don't necessarily fill to the boundaries, so 
#      we need to call this check for all points, to be sure we don't miss any.


# Iteratively scan all potential bubble cells, and in doing so populate the bubble[] list
for cand in sorted(candidates):
	if not (cand in bubble or cand in cubes or cand in outside):
		connections = [cand]
		for c in connections:		# This isn't a pointless loop - connections will get more elements dynamically added
			exposed = False
			checks = [ [ i+j for i,j in zip(c,n) ] for n in neighbours]
			
			# Do these basic checks first, before recursing further, to prune the search tree
			for check in checks:
				# Do we already know that this check-cube is outside?
				if check in outside: 
					exposed = True
					break
				# Is the check-cube out of bounds?
				for i in [0,1,2]:
					if check[i] > maxextent[i] or check[i] < minextent[i]: 
						exposed = True
						break

			if not exposed:
				for check in checks:
					# If we don't know anything about the check-cube...
					if not (check in connections or check in bubble or check in cubes or check in outside):
						# ...then add it to the list for investigation
						connections.append(check)

			if exposed: break

		if exposed:
			outside += connections
		else:
			bubble += connections


# Now rerun the surface area calculation
surf2 = 0
for c in cubes:
	for n in neighbours:
		check = [ i+j for i,j in zip(c,n) ]
		if not check in cubes and not check in bubble:
			surf2 += 1

print("Part 1: total surface area is ",surf)
print('Part 2: outward-facing surface area is',surf2)

exit()

# Visualise
clr_cube='\033[92m'
clr_bubble='\033[91m'
clr_space='\033[94m'
clr_clear='\033[0m'
for i in range(minextent[0]-1,maxextent[0]+2,1):
	print(f'------------{i:2}------------')
	print('    ', end='')
	for j in range(minextent[1]-1,maxextent[1]+2,4):
		print(f'{j:<4}', end='')
	print()
	print('    ', end='')
	for j in range(minextent[1]-1,maxextent[1]+2,4):
		print('v   ', end='')
	print()
	for j in range(minextent[1]-1,maxextent[1]+2,1):
		print(f'{j:2}: ',end='')
		for k in range(minextent[2]-1,maxextent[2]+2,1):
			if [i,j,k] in cubes:
				print(f'{clr_cube}#{clr_clear}', end='')
			elif [i,j,k] in bubble:
				print(f'{clr_bubble}x{clr_clear}', end='')
			elif [i,j,k] in outside:
				print(f'{clr_space}.{clr_clear}', end='')
			else:
				print(f' ', end='')
		print()
