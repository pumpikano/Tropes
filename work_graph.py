import networkx as nx
import graph_builders as gb
import cPickle


tropes = cPickle.load(open('tropes_clean','r'))
works = cPickle.load(open('works_clean','r'))
bigraph = cPickle.load(open('bigraph_clean','r'))

'''
tropes = cPickle.load(open('first','r'))
works = cPickle.load(open('second','r'))
bigraph = cPickle.load(open('rg','r'))
'''

wg, feat_counts, edge_counts = gb.projectBipartite(bigraph, tropes, works)

cPickle.dump(wg,open('work_graph','w'))
cPickle.dump(feat_counts,open('trope_counts','w'))
cPickle.dump(edge_counts,open('edge_counts','w'))
