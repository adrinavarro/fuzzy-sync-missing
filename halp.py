# HELP! I deleted a bunch of files from a destination, and my backup is unstructured!

# Imagine: you copy some camera recordings to a structured folder and rename the files.
# You still keep a snapshot of the SD Cards you've processed over time.
# One day, you accidentally remove some files from the structured folder.
# How to figure out which ones went missing? Use this script.

# WHAT IT DOES
# 1. Lists all files (recursively) in the origin folder
# 2. Lists all files (recursively) in the destination folder
# 3. Examines which ones are missing from the destination based on name+size, or size alone

import glob, os, pprint


def build_index(folder):
	index = []

	for f in glob.glob(folder + '/**', recursive=True):
		if not os.path.isfile(f):
			continue

		index.append({'location': f, 'name': os.path.basename(f), \
					  'size': os.path.getsize(f), 'sum': None})
	
	return index


def find_by_size_name(size, name, index):
	for i in index:
		if i['size'] == size and i['name'] == name:
			return i['location']
	return None


def find_by_size(size, index):
	results = []

	for i in index:
		if i['size'] == size:
			results.append(i['location'])

	return results

def execute(orig, dest):
	o_index = build_index(orig)
	d_index = build_index(dest)

	found_sure = []
	found_maybe = []
	not_found = []

	for o in o_index:
		print("Looking at %s..." % o['name'])
		comprehensive = find_by_size_name(o['size'], o['name'], d_index)

		if comprehensive:
			found_sure.append((o, comprehensive))
		else:
			fuzzy = find_by_size(o['size'], d_index)

			if fuzzy:
				found_maybe.append((o, fuzzy))
			else:
				not_found.append(o)

	return found_sure, found_maybe, not_found


orig = '/Users/adrian/SD_Cards'
dest = '/Users/adrian/Recordings'

found, maybe, notfound = execute(orig, dest)

print("Maybe found, please check:")
pprint.pprint(maybe)
print("\n\n")

print("NOT found, need to be copied:")
pprint.pprint(notfound)
print("\n\n")
