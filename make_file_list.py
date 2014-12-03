import os
import json

sysPath = "/Users/rg/Projects/plotgen/ficgen/tropes_character/"

paths = []

for root, dirs, files in os.walk(sysPath):
    for f in files:
    	if f.endswith(".txt"):
    		fullPath = os.path.join(root, f)
    		shortPath = fullPath.split('/ficgen/')[-1]
        	paths.append(shortPath)

print paths
j = json.dumps(paths)

ff = open("/Users/rg/Projects/plotgen/ficgen/tropes_character.json", 'w')

print >> ff, j

ff.close()