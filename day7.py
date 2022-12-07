#!python3

import inputFetcher
import re

inputFile = inputFetcher.getInput('https://adventofcode.com/2022/day/7/input')

# Given a log of commands traversing a directory tree, reconstruct the sizes of directories

sizes = {}

# Bit of a hack: requests.response.iter_lines() doesn't reliably work if called from multiple places
# so read the entire input file into memory, and manually maintain a 'file' pointer
inputLines = []
for line in inputFile.iter_lines():
	inputLines.append(line.decode())
pointer = 0

# Recursive function to add up the size of files in a directory
def getSize(ptr, inp, nom, sizes):
	mysize = 0
	while True:

		ptr += 1
		if ptr >= len(inp):			# Reached EOF
			break;
		line = inp[ptr]

		if line == '$ cd ..':		# Finished this directory, so pop up a level in the recursion
			break
		else:
			srch = re.search(r'(\d+) \w+.?\w*', line)		# Is it a line with a file size? If so, add it to the running total
			if srch:
				filesize = int(srch.group(1))
				mysize += filesize
			else:
				srch2 = re.search(r'\$ cd (\w+)', line)		# Or is it changing to a new directory? If so, recurse!
				if srch2:
					subdir = nom + '/' + srch2.group(1)
					sizes[subdir], ptr, sizes = getSize(ptr, inp, subdir, sizes)
					mysize += sizes[subdir]
					
	return mysize, ptr, sizes

# Assume first line is $ cd /, and start the recursive parse
sizes['/'], pointer, sizes = getSize(pointer, inputLines, '', sizes)

# The sizes dict should now be populated. Scan through, and figure out the answers
total1 = 0
small2 = 30000000000
freedisk = 70000000 - sizes['/']
spaceneeded = 30000000 - freedisk
smallname = 'dummystartvalue'
for clef in sizes.keys():
	if sizes[clef] <= 100000:
		total1 += sizes[clef]
	if sizes[clef] > spaceneeded and sizes[clef] < small2:
		small2 = sizes[clef]
		smallname = clef

print("Total for part 1:",total1)
print("Smallest folder >300k is",smallname,"at",small2)

