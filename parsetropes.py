import util

#type_map, feature_map, proc_cat1_map, proc_cat2_map, sameas_map, seealso_map, itemname_map = pt.parseTropes()
def parseTropes():
	file = open("../dbtropes/dbtropes-20111112.nt", "r")

	type_map = dict()
	feature_map = dict()
	proc_cat1_map = dict()
	proc_cat2_map = dict()
	sameas_map = dict()
	seealso_map = dict()
	itemname_map = dict()
	
	line_count = 0
	while file:
		line_count += 1
		if not (line_count % 1000):
			print line_count
		line = file.readline()
		if len(line) == 0:
			print line_count
			break
		parts = line.split(" ")
		
		name = lastPathSegment(parts[0])
		if parts[1] == "<http://www.w3.org/1999/02/22-rdf-syntax-ns#type>":
			if not name in type_map:
				type_map[name] = set()
			type_map[name].add(lastPathSegment(parts[2]))
		elif parts[1] == "<http://skipforward.net/skipforward/resource/seeder/skipinions/hasFeature>":
			if not name in feature_map:
				feature_map[name] = set()
			feature_map[name].add(lastPathSegment(parts[2]))
		elif parts[1] == "<http://dbtropes.org/ont/processingCategory1>":
			if not name in proc_cat1_map:
				proc_cat1_map[name] = set()
			proc_cat1_map[name].add(lastPathSegment(parts[2]))
		elif parts[1] == "<http://dbtropes.org/ont/processingCategory2>":
			if not name in proc_cat2_map:
				proc_cat2_map[name] = set()
			proc_cat2_map[name].add(lastPathSegment(parts[2]))
		elif parts[1] == "<http://www.w3.org/2002/07/owl#sameAs>":
			if not name in sameas_map:
				sameas_map[name] = set()
			sameas_map[name].add(lastPathSegment(parts[2]))
		elif parts[1] == "<http://www.w3.org/2000/01/rdf-schema#seeAlso>":
			if not name in seealso_map:
				seealso_map[name] = set()
			seealso_map[name].add(lastPathSegment(parts[2]))
		elif parts[1] == "<http://skipforward.net/skipforward/resource/seeder/skipinions/itemName>":
			if name.find("/int_name") > -1:
				name = name.replace("/int_name","")
			if not name in itemname_map:
				itemname_map[name] = set()
			itemname_map[name].add(lastPathSegment(parts[2]))
			
	return type_map, feature_map, proc_cat1_map, proc_cat2_map, sameas_map, seealso_map, itemname_map

#replace trope id's with trope types in feature_map and return a new map
#feat_lists = pt.resolveFeatures(feature_map, type_map)
def resolveFeatures(feature_map, type_map):
	total_count = len(feature_map.keys())
	
	count = 0
	feature_lists = dict()
	for name in feature_map:
		count += 1
		if not (count % 10):
			print count, "of", total_count
		feature_lists[name] = list()	
		feats = list()
		for feat_id in feature_map[name]:
			if not feat_id in type_map:
				print feat_id, "not in type map"
			else:
				feats.append(list(type_map[feat_id])[0])	# this works cuz there's supposed to be only one element in each set. verify with bigLenCount
		feature_lists[name] = list(set(feats))
	
	return feature_lists

# return a list of keys in feature_lists that have a sameas relation to any other key and whose feature set is smaller
def resolveSameAs(feature_lists, sameas_map):
	remove_keys = set()
	for k in sameas_map.keys():
		'''
		if not k in feature_lists:
			continue
		'''
		sameas_set = sameas_map[k]
		sameas_set.add(k)
		to_remove = set()
		for aka in sameas_set:
			if aka not in feature_lists:
				to_remove.add(aka)
		sameas_set = sameas_set.difference(to_remove)
		if not len(sameas_set) > 1:
			continue
		
		num_feats = util.Counter()
		for aka in sameas_set:
			num_feats[aka] = len(feature_lists[aka]) 
		to_keep = num_feats.argMax()
		sameas_set.remove(to_keep)
		remove_keys = remove_keys.union(sameas_set)
		
	return remove_keys

# delete all keys in key_set from map
def deleteKeys(key_set, map):
	for e in key_set:
		del map[e]

# count how many TVTItems have a sameas relation
def numTVTItem(type_map, sameas_map):
	count = 0
	for e in sameas_map:
		if e in type_map and list(type_map[e])[0] == "ont/TVTItem":
			count += 1
	print count, "TVTItems in sameas_map"

# turns out there is not anything other than ont/TVTItems in feature_map, as it should be
def nonTVTItemsInFeatMap(type_map, feature_map):
	nontvtitems = set()
	for e in feature_map:
		'''
		if e in type_map and list(type_map[e])[0] != "ont/TVTItem":
			nontvtitems.append(e)
		'''
		if e in type_map:
			nontvtitems = nontvtitems.union(type_map[e])
	return nontvtitems

# parse out and return the full path after the top-level domain
def lastPathSegment(str):
	str = str[1:-1]	#remove < >
	segments = str.split(".")		#split on .
	segments = segments[-1].split("/")	#take the last segment and split on /
	return "/".join(segments[1:])

# find map keys with len greater than 1 	
def bigLenCount(map):
	lens = [len(map[e]) for e in map]
	big = list()
	for e in range(len(lens)):
		if lens[e] > 1:
			big.append(map.keys()[e])
	return big

def emptyEntries(map):
	empt = list()
	for e in map.keys():
		if len(map[e]) == 0:
			empt.append(e)
	return empt
	
def find(f, seq):
  """Return first item in sequence where f(item) == True."""
  for ind in range(len(seq)):
    if f(seq[ind]): 
      return ind

# return set of tropes in common between work1 and work2
def commonTropes(feature_lists, work1, work2):
	return set(feature_lists[work1]).intersection(set(feature_lists[work2]))
	
def collectProcCatSet(proc_cat_map, type_map):
	combined_set = set()
	for e in proc_cat_map:
		if e in type_map and list(type_map[e])[0] == 'ont/TVTItem':
			combined_set = combined_set.union(proc_cat_map[e])
	return combined_set
			
def keysWithMoreThanOneType(type_map):
	key_list = list()
	for e in type_map:
		if len(type_map[e]) > 1:
			key_list.append(e)
	return key_list

def combineProcCats(proc_cat1_map, proc_cat2_map):
	new_map = dict()
	for e in proc_cat1_map:
		cat_set = proc_cat1_map[e]
		for c in proc_cat1_map[e]:
			if c in proc_cat2_map:
				cat_set = cat_set.union(proc_cat2_map[c])
		new_map[e] = cat_set
	return new_map
	
	
def subMapWorkInProcCat(feature_lists, proc_cat_map, proc_cat):
	new_map = dict()
	for e in feature_lists:
		if e in proc_cat_map and proc_cat in proc_cat_map[e]:
			new_map[e] = feature_lists[e]
	return new_map
			
			
			
			
			
			