

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
		
def lastPathSegment(str):
	str = str[1:-1]	#remove < >
	segments = str.split(".")		#split on .
	segments = segments[-1].split("/")	#take the last segment and split on /
	return "/".join(segments[1:])

# find map keys with values greater than 1 	
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
	
