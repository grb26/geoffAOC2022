#!python3
import sys
import re
import operator
import json

formulae = {}
origknown = {}
deps = {}
ops = { '+':operator.add, '-':operator.sub, '*':operator.mul, '/':operator.floordiv }

for l in sys.stdin:
	line = l.strip()
	renum = re.match(r'(\w+): (\d+)', line)
	refor = re.match(r'(\w+): (\w+) (.) (\w+)', line)
	if renum:
		origknown[renum.group(1)] = int(renum.group(2))
	elif refor:
		formulae[refor.group(1)] = [refor.group(2), refor.group(3), refor.group(4)]
		if not refor.group(2) in deps:
			deps[refor.group(2)] = []
		deps[refor.group(2)] += [refor.group(1)]
		if not refor.group(4) in deps:
			deps[refor.group(4)] = []
		deps[refor.group(4)] += [refor.group(1)]

def solve1():
	known = origknown.copy()		# Going to need this list intact for part 2, so take a copy to work with
	while not 'root' in known:
		for k in list(known.keys()):
			for d in deps[k]:
				if formulae[d][0] in known and formulae[d][2] in known:
					known[d] = ops[formulae[d][1]](known[formulae[d][0]],known[formulae[d][2]])
	return known['root']

# Fix the value of anything not dependent on 'humn', to make part 2 solvable
def fixnondeps(known):
	cont = True 
	while cont:
		cont = False
		for k in list(known.keys()):
			if not k in deps: continue
			for d in deps[k]:
				if d == 'humn' or d in known: continue
				if formulae[d][0] in known and formulae[d][2] in known:
					known[d] = ops[formulae[d][1]](known[formulae[d][0]],known[formulae[d][2]])
					cont = True

# Walk down the tree, propagating a constraint to the child nodes based on the target value of the parent node
def solve2():
	# Assumption: there's just one path to humn - if this is true, we're cooking on gas
	n1 = formulae['root'][0]
	n2 = formulae['root'][2]
	if n1 in origknown:
		n = n2
		t = origknown[n1]
	elif n2 in origknown:
		n = n1
		t = origknown[n2]
	else:
		print("Broken")
		exit()
	while n != 'humn':
		(n,t) = solvefor(n,t)
	return t

# Function to effectively rearrange the equation for a child node
def solvefor(node,target):
	if formulae[node][0] in origknown:
		unknown = formulae[node][2]
		known = origknown[formulae[node][0]]
		knownname = formulae[node][0]
		# t = k ? u so   t=k/u -> u=k/t  t=k*u -> u=t/k   t=k+u -> u=t-k   t=k-u -> u=k-t
		if formulae[node][1] == '+':
			nexttarget = target-known
		elif formulae[node][1] == '-':
			nexttarget = known-target
		elif formulae[node][1] == '*':
			nexttarget = target//known
		elif formulae[node][1] == '/':
			nexttarget = known//target
		else:
			print("Broken")
			exit()

	elif formulae[node][2] in origknown:
		unknown = formulae[node][0]
		known = origknown[formulae[node][2]]
		knownname = formulae[node][2]
		# t = u ? k    so    t=u/k -> u=kt    t=u*k -> u=t/k     t=u+k -> u=t-k     t=u-k -> u=t+k
		if formulae[node][1] == '+':
			nexttarget = target-known
		elif formulae[node][1] == '-':
			nexttarget = target+known
		elif formulae[node][1] == '*':
			nexttarget = target//known
		elif formulae[node][1] == '/':
			nexttarget = known*target
		else:
			print("Broken")
			exit()
	
	else:
		print('Sorry, unknowns on both sides')
		exit()
	
	#print('converted',node,target,'into',unknown,nexttarget,'due to formula',formulae[node],'and node',knownname,'=',origknown[knownname])
	return (unknown, nexttarget)


# Part 1: just solve the formulae given
print('Part 1:',solve1())

# Part 2: discard the value of 'humn' and find an alternative that makes root's two terms equal
del(origknown['humn'])
fixnondeps(origknown)
print('Part 2:',solve2())


