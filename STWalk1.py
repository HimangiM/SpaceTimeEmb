#####################
# Algorithm 1 of porposed method
# learn spatio-temporal embedding together
#####################

# In[1]:

import random
from gensim.models import Word2Vec
import networkx as nx
import sys
from multiprocessing import cpu_count
import time


# In[2]:
# from sympy.core.basic import preorder_traversal


def createSpaceTimeGraph(G_list, time_window, start_node, time_step):
    """
     time step is necessary because we want representation only for last time step and
     we will create the spa-time graph for [time_step, time_step-1,time_step-2,...,time_step-time_window]
    """
    start = time.time()
    G = G_list[-1]
    for time1 in range(1, time_window+1):
        past_node = start_node.split("_")[0] + "_" + str(time_step-time1)
        #print(past_node)
        if past_node not in G_list:
            continue
        else: 
            G.add_edge(start_node, past_node)

            G_past = G_list[-time1-1]
            #from IPython.core.debugger import Tracer; Tracer()()
            # considering first level neighbors
            past_neighbors = list(G_past.neighbors(past_node))
            temp=[]
            # considering second level neighbors
            for elt in past_neighbors:
                temp = temp+list(G_past.neighbors(elt))
            # merging list of level-1 and level-2 neighbors
            past_neighbors=past_neighbors+temp
            past_neighbors.append(past_node)
            # finding the subgraph
            past_subgraph = G_past.subgraph(past_neighbors)

            G = nx.compose(G, past_subgraph)  # merge current graph with past subgraphs
            #print("space time graph created")
            #print("space-time graph"+str((time.time()-start)))
            start_node = past_node
    return G


# In[3]:

def random_walk(SpaceTimegraph, path_length, rand=random.Random(0), start=None):  # alpha = prob of restart
    """ Returns a truncated random walk.
        path_length: Length of the random walk.
        removed = alpha: probability of restarts.
        start: the start node of the random walk.
    """
    G = SpaceTimegraph
    if start:
        path = [start]
    else:
        # Sampling is uniform w.r.t V, and not w.r.t E
        # path = [rand.choice(G.keys())]
        sys.exit("ERROR: Start node not mentioned for random_walk")

    while len(path) < path_length:
        cur = path[-1]
        if len(G[cur]) > 0:
            path.append(rand.choice(list(G[cur])))
        else:
            break
    #print("random walk="+str(len(path)))
    return path


# In[4]:

def create_vocab(G_list, num_restart, path_length, nodes, time_step, rand=random.Random(0), time_window=1):
    walks = []

    nodes = list(nodes)

    # number of path = num of restarts per node
    for cnt in range(num_restart):
        rand.shuffle(nodes)
        start = time.time()
        for node in list(nodes):
            G = createSpaceTimeGraph(G_list, time_window, node, time_step)
            walks.append(random_walk(SpaceTimegraph=G,path_length=path_length, rand=rand, start=node))
        print(str(cnt)+" shuffle time="+str((time.time()-start)))
    print("vocab created="+str(len(walks)))
    return walks


# In[ ]:

# this function will generate representation for all nodes in space-time-graph of all nodes of graph at t=time_step
# however we will consider only representations of nodes present in graph at t = time_step
def spatioTemporalRep(input_direc, output_file, number_restart, walk_length, representation_size, time_step,
                      time_window_size, workers,vocab_window_size):
    if time_window_size>time_step:
        sys.exit("ERROR: time_window_size(="+str(time_window_size)+") cannot be more than time_step(="+str(time_step)+"):")


    G_list = [nx.read_graphml(input_direc + "graph_" + str(i) + ".graphml") for i in range(time_step-time_window_size, time_step+1)]

    #from IPython.core.debugger import Tracer; Tracer()()
    # get list of nodes
    nodes = G_list[-1].nodes()
    print("Creating vocabulary")
    walks = create_vocab(G_list, num_restart=number_restart, path_length=walk_length, nodes=nodes,
                         rand=random.Random(0), time_step=time_step,time_window=time_window_size)


    # time-step is decremented by 1, because, time steps are from 0 to time_step-1=total time_step length
    print("Generating representation")
    model = Word2Vec(walks, size=representation_size, window=vocab_window_size, min_count=0, workers=workers)

    model.wv.save_word2vec_format("/home/himangi/Internship/Work/DBLP/restarts_dblp_64_10/"+ output_file)
    print("Representation File saved: "+"/home/himangi/Internship/Work/DBLP/restarts_dblp_64_10/"+ output_file)
    return


# In[ ]:

number_restart = 40
walk_length = 10
representation_size = 64
#time_step = 4
#time_window_size = 3
vocab_window_size = 5
workers = cpu_count()
#print(workers)
#direc = "/home/cs15mtech11016/spacetime/"
#direc = "D:/IIT Hyd Sem-4/Research/algo output files/synDataFiles/newLabel/"
direc = "/home/himangi/Internship/Work/DBLP/graphs_order/"
seq=[]

for t in range(0, 46):
	if(t+1)%10==0:
		seq.append(t)


for t in seq:
    print("\n***Generating "+str(representation_size)+" dimension embeddings for nodes")
    time_step = t
    time_window_size = 9 # including current time step total window size is of 5 time-step
    start = time.time()
    spatioTemporalRep(direc, "space_time_" + str(time_step)+".spacetimerep", number_restart=number_restart,
                      walk_length=walk_length, vocab_window_size=vocab_window_size,
                      representation_size=representation_size, time_step=time_step, time_window_size=time_window_size,
                      workers=workers)

    print "representation for " + str(t) + "generated in " + str(time.time() - start)
