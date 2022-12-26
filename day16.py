#!python3

# Read in the input file, and store in a list-of-lists structure.
# Each item contains four values, representing the x & y coordinates of the sensor and nearest detected beacon
import re
import sys
flows = {}
nodes = []
edges = {}
nonzeronodes = []	# Some (most) of the valves have zero flow, so they won't be worth considering in the optimisation 
for line in sys.stdin:
	# Format: Valve AC has flow rate=4; tunnels lead to valves KC, RN, QA, QZ, UB
	valve = re.search(r'Valve (..) has', line)[1]
	nodes.append(valve)
	flow = int(re.search(r'rate=(\d+);', line)[1])
	tunnels = re.findall(r'([A-Z][A-Z])', line)[1:]		# [1:] to skip the first match, "Valve XX has flow rate..."
	if flow > 0:
		nonzeronodes.append(valve)
	flows[valve] = flow
	edges[valve] = tunnels

# Generate a lookup table of distances between each valve, using the Floyd–Warshall algorithm
dist = {}
for u in nodes:
	# Initialise this row of the array
	dist[u] = {}
	for v in nodes:
		dist[u][v] = 1000								# Initialise to a distance larger than we can possibly care about
	# Initialise the easy values: self, and immediate neighbours (i.e. the edges connected to node u)
	dist[u][u] = 0
	for v in edges[u]:
		dist[u][v] = 1
for k in nodes:
    for i in nodes:
        for j in nodes:
            if dist[i][j] > dist[i][k] + dist[k][j]:
                dist[i][j] = dist[i][k] + dist[k][j]

# Function to calculate the flow rate that results from a particular path
flowcache = {}
def pathflow(path, maxtime):			# Optimising assumptions: only visit rooms with nonzero rates, never visit the same room twice
	global flowcache
	pathkey = '-'.join(path)
	if pathkey in flowcache: 
		return flowcache[pathkey]
	flow = 0
	openvalves = []
	time = 0

	for i in range(1,len(path)):
		timespent = dist[path[i-1]][path[i]] + 1
		bust = False
		if timespent > maxtime - time: 
			bust = True
			timespent = maxtime - time			
		for valve in openvalves:
			flow += flows[valve] * timespent	
		if bust: break
		openvalves.append(path[i])
		time += timespent

	if time < maxtime:
		for valve in openvalves:
			flow += flows[valve] * (maxtime - time)

	flowcache[pathkey] = flow 	# Cache the value for next time
	return flow

# Recursive function to generate all possible paths, and keep track of the best flows
def createpath(path, length, availablenodes, maxtime, bestflow=0):
	global dist
	score = pathflow(path, maxtime)
	bestflow = max(bestflow, score)
	
	# Calculate next steps
	lastnode = path[-1]
	for nextnode in availablenodes:
		extralength = dist[lastnode][nextnode]
		if length + extralength + 1 <= maxtime:
			score = createpath(path+[nextnode], length+extralength+1, list(set(availablenodes)-set([nextnode])), maxtime, bestflow)
			bestflow = max(bestflow, score)
	return bestflow

# Part 1: What's the best achievable flow for a single person working for 30s?
# Kick off the recursion with our starting node, zero distance travelled, and a limit of 30 minutes
p1best = createpath(['AA'], 0, nonzeronodes, 30)
print('Part 1:',p1best)

# Part 2: What if we had two agents working for 26s?
# Approach: full recursion across both paths is computationally heavy, so split the problem in two: generate all possible single
#  paths, then for each one, generate all possible paths from the remaining available nodes.
#  Prune by only considering valves with non-zero flow, and removing visited nodes from subsequent calculations.
#  In theory, all paths have already been evaluated, so it's just a case of generating the paths - the scoring should always be a cache hit.
# Max time drops to 26, so previous calculations aren't useful - need to recalculate flow cache
flowcache = {}
singlebest = createpath(['AA'], 0, nonzeronodes, 26)	# Initialise the cache, and keep track of the best single score
nznodes = set(nonzeronodes)
p2best = 0
for humanpath in flowcache.keys():
	hpath = humanpath.split('-')
	othernodes = list(nznodes - set(hpath))
	if flowcache[humanpath] + singlebest < p2best: continue					# No point if even the best available path wouldn't combine with this one to beat our running highscore
	score = flowcache[humanpath] + createpath(['AA'], 0, othernodes, 26)
	p2best = max(score, p2best)

print('Part 2:',p2best)