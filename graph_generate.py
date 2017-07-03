#generate graphs for the yearly data
#if A and B have published a paper together, they will have an edge in the graph

import networkx as nx
import os 
import glob
import time



files = os.listdir("/media/sdg/himangi/DBLP/yearly_conf_labels")
#file = "./yearly_conf_labels/1969_labels.txt"

graph_dict = {}

if __name__=='__main__':

	
	h = -1
	txt_files = filter(lambda x: x[-4:] == '.txt', files)
	txt_files = glob.glob("yearly_conf_labels/*.txt")
	
	txt_files.sort()
	#for i in txt_files:
	#	print i[19:23]
	
	for file in txt_files:
		with open(file, 'r') as infile:
			for line in infile:
				token = line.strip().split("|")
				if token[1] not in graph_dict.keys():
					graph_dict[token[1]] = []
				graph_dict[token[1]].append(token[0])

		h += 1  
		G = nx.Graph()
		

		for k, v in graph_dict.iteritems():
			for i in range(len(v)):
				for j in range(i+1, len(v)):	
					G.add_edge(v[i], v[j])

		print "done" + file[19:23]
		name = "graph_" + str(h) + ".graphml"
		nx.write_graphml(G, name)
		
		
	
