
import networkx as nx

def simpleBiPartiteNetwork(features):
	
	tropes = set()
	all_works = features.keys()
	edges = list()
	
	for work_name in features:
		tropes = tropes.union(features[work_name])
		work_tropes = list(set(features[work_name]))
		edges.extend(zip([work_name for num in range(len(work_tropes))], work_tropes))
		
	g = nx.Graph(edges)
	return g