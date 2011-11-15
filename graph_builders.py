
import networkx as nx
import util

#import graph_builders as gb
#g, tropes, works = gb.simpleBiPartiteNetwork(features)
def simpleBiPartiteNetwork(features):
	
	tropes = set()
	works = features.keys()
	edges = list()
	
	total_count = len(features)
	count = 0
	for work_name in features:
		count += 1
		if not (count % 100):
			print count, "of", total_count
		tropes = tropes.union(features[work_name])
		work_tropes = list(set(features[work_name]))
		edges.extend(zip([work_name for num in range(len(work_tropes))], work_tropes))
		
	print "building graph..."
	g = nx.Graph(edges)
	print "done"
	return g, tropes, works

# collapse the bipartite graph on the nodes passed in
#wg, feat_counts, edge_counts = gb.projectBipartite(g, tropes, works)
def projectBipartite(graph, collapse_nodes, persist_nodes):
	edge_counts = util.Counter()	#track num of tropes per edge
	feat_counts = util.Counter()	#track num of tropes per node
	
	print "counting tropes..."
	for n in persist_nodes:
		feat_counts[n] = len(graph.neighbors(n))
	print "trope counting done."
	
	total_count = len(collapse_nodes)
	count = 0
	for n in collapse_nodes:
		count += 1
		if not (count % 100):
			print count, "of", total_count, "collapsed"
		works = graph.neighbors(n)
		
		works.sort()
		for i in range(len(works)):
			for j in range(i+1, len(works)):
				edge_counts[(works[i],works[j])] += 1
	
	# create the graph
	print "building graph..."
	g = nx.Graph()
	g.add_nodes_from(persist_nodes)
	g.add_edges_from(edge_counts.keys())
	print "done"
	return g, feat_counts, edge_counts
