#!python3
import sys
import re
import math

resource = { 'ore':0, 'clay':1, 'obsidian':2, 'geode':3 }

# Read in the input
costs = {}
limits = {}
for l in sys.stdin:
	line = l.strip()
	if line == '': continue
	robot_cost = [ [0]*4 for _ in range(4) ]
	limit = [0]*4
	bpid = int(re.search(r'Blueprint (\d+)', line)[1])
	for spec in re.findall(r'Each [^.]+\.', line):
		g = re.search(r'Each (\w+) robot costs ([^\.]+)\.', spec)
		robot_type = g.group(1)
		ingredients = g.group(2)
		for cost in re.findall(r'(\d+) (\w+)', ingredients):
			robot_cost[resource[robot_type]][resource[cost[1]]] = int(cost[0])
		# Set limits on number of robots to build - no point in having rate of generation > max possible rate of consumption
		limit[0] = max([cost[0] for cost in robot_cost[1:3]])	# Everyone needs ore
		limit[1] = robot_cost[2][1]								# Only obsidianbots need clay
		limit[2] = robot_cost[3][2]								# Only geodebots need obsidian
		limit[3] = 50 											# Effectively unlimited requirement for geodebots

	costs[bpid] = robot_cost
	limits[bpid] = limit

# Function to run simulation
def sim(timelimit, results, maxbp):
	rob = 0
	res = 4
	points = 7
	time = 8 
	for bpid in range(1,maxbp+1):
		best = 0
		cost = costs[bpid]
		lim = limits[bpid]
		cache = {}

		evalq = [ [1,0,0,0, 0,0,0,0, 0, 'bpid'+str(bpid)+':'] ]		# State format: [ robot_count1,,4 resources_held1,,4 time ]
		for state in evalq:
			# Have we been here before? If so, don't bother
			fingerprint = str(state[:time])
			position = state[time]
			if fingerprint in cache:
				if cache[fingerprint]<=position:
					continue
			else:
				cache[fingerprint] = position

			# Absolute best case: every step from now creates a new geodebot. If this still isn't enough, prune this branch.
			timeleft = timelimit - state[time]
			wouldscore = state[points] + state[rob+3]*timeleft
			if wouldscore + (timeleft*(timeleft -1))//2 < best:
				continue

			# Generate next states to evaluate
			for nrt in [3,2,1,0]:		# Next robot type
				if state[rob+nrt] >= lim[nrt]: 	# Already got enough of these robots
					continue

				# Don't start building something if there isn't enough time to make use of whatever it produces
				if (nrt == 1 and timeleft <6) or (nrt == 0 and timeleft <8) or (nrt == 2 and timeleft <4) or (nrt == 3 and timeleft <2):
					continue

				# Can we actually build this robot type?
				unbuildable = False
				timereq = 0
				for i in range(4):
					if cost[nrt][i] == 0: 		# Robot type nrt doesn't use resource type i, so we're fine
						continue
					if state[rob+i] == 0: 		# Robot type needs resource i, but we don't have anyone producing it, so this will never work
						unbuildable = True
						break
					timereq = max(timereq, math.ceil((cost[nrt][i] - state[res+i])/state[rob+i]))
					if timereq > (timelimit - state[time] - (2 if nrt == 3 else 4)): # Geodebots need to be ready at least 2 cycles before the time limit in order to produce anything; other bots need to be ready 4 cycles before, in order to enable a geodebot to be built and deliver a geode
						unbuildable = True
						break
				if unbuildable: 
					continue
				timereq += 1
				
				# If we just let this run to the end now, what would we score?
				timewillbeleft = timeleft - timereq
				willscore = wouldscore
				if nrt == 3: willscore += timewillbeleft
				best = max(best,willscore)

				# Is there time to do anything else after this? If not, don't simulate further
				if timewillbeleft < 2:
					continue

				# Looks like this state might be viable, so add it to the queue to evaluate
				newstate = state.copy()
				for i in range(4):
					newstate[res+i] += (newstate[rob+i] * timereq) - cost[nrt][i]
				newstate[rob+nrt] += 1
				newstate[time] += timereq
				newstate[-1] += str(nrt)
				evalq.append(newstate)

		results.append([bpid, best])

# Pseudomain
res=[]
sim(24,res,len(costs))
score1 = 0
for b in res:
	score1 += b[0]*b[1]
print('Part 1:',score1)
res=[]
sim(32,res, 3)
score2 = 1
for b in res:
	score2 *= b[1]
print('Part 2:',score2)