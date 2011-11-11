import BackwardsReader as br

def cleanRDF():
	outfile = open("./dbtropes/stripped_tropes.nt", "w")
	infile = open("./dbtropes/dbtropes-20111003.nt", "r")
	
	line_count = 0
	while infile:
		line_count += 1
		if not (line_count % 1000):
			print line_count
		line = infile.readline()
		if len(line) == 0:
			print line_count
			break
		elif line.find("<http://www.w3.org/1999/02/22-rdf-syntax-ns#type>") > 0 or line.find("<http://skipforward.net/skipforward/resource/seeder/skipinions/hasFeature>") > 0:
			outfile.write(line)
	outfile.close()
	infile.close()
	
def parseTropes():
	file = open("./dbtropes/stripped_tropes.nt", "r")
	#b = br.BackwardsReader("./dbtropes/stripped_tropes.nt")

	type_map = dict()
	feature_map = dict()
	
	line_count = 0
	while file:
		line_count += 1
		line = file.readline()
		if len(line) == 0:
			print line_count
			break
		parts = line.split(" ")
		
		name = lastPathSegment(parts[0])
		if parts[1] == "<http://www.w3.org/1999/02/22-rdf-syntax-ns#type>" and not name in type_map:
			type_map[name] = lastPathSegment(parts[2])
			
	file.close()
	
	# second pass
	file = open("./dbtropes/stripped_tropes.nt", "r")
	line_count = 0
	while file:
		line_count += 1
		line = file.readline()
		if len(line) == 0:
			print line_count
			break
		parts = line.split(" ")
		
		name = lastPathSegment(parts[0])
		if parts[1] == "<http://skipforward.net/skipforward/resource/seeder/skipinions/hasFeature>":
			if not name in feature_map:
				feature_map[name] = list()
			feature_map[name].append(type_map[lastPathSegment(parts[2])])
	file.close()
	
	'''
	file.close()
	feature_lists = dict()
	for name in feature_map:
		feature_lists[name] = list()	
		for feat_id in feature_map[name]:
			feature_lists[name].append(type_map[feat_id])
	'''
	return feature_map
	
	
def lastPathSegment(str):
	# remove < >
	str = str[1:-1]
	segments = str.split("/")
	return "/".join(segments[-2:])