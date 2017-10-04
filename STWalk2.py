
#############################
# Algorithm 2 of proposed method 
# learn spatial and temporal representation separately and add the vectors
#############################

import random
from gensim.models import Word2Vec
import networkx as nx
import sys
import time
from multiprocessing import cpu_count


# In[2]:

def createSpaceTimeGraph(G_list, time_window, start_node, time_step):
    """
     time step is necessary because we want representation only for last time step and
     we will create the spa-time graph for [time_step, time_step-1,time_step-2,...,time_step-time_window]
    """
    # G = nx.Graph()
    start = time.time()
    G = G_list[-1]

    for time1 in range(1, time_window+1):
        past_node = start_node.split("_")[0] + "_" + str(time_step - time1)
        if past_node not in G_list:
            continue
        else:
            G.add_edge(start_node, past_node)

            G_past = G_list[-time1-1]
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
        #from IPython.core.debugger import Tracer; Tracer()()
        cur = path[-1]
        if len(G[cur]) > 0:
            path.append(rand.choice(list(G[cur])))
        else:
            break
    #print("random walk="+str(len(path)))
    return path


# In[4]:

def create_vocab(G_list, num_restart, path_length, nodes, time_step, isTimeWalk, rand=random.Random(0),time_window=1):
    walks = []

    nodes = list(nodes)

    # number of path = num of restarts per node
    for cnt in range(num_restart):
        rand.shuffle(nodes)
        start = time.time()
        for node in list(nodes):
            if not isTimeWalk: # if it is space walk
                G = G_list[-1] # then consider only current time-step
            else:
                G = createSpaceTimeGraph(G_list, time_window, node, time_step)
            walks.append(random_walk(SpaceTimegraph=G,path_length=path_length, rand=rand, start=node))
        print(str(cnt)+" shuffle time="+str((time.time()-start)))
    #print("vocab created="+str(len(walks)))
    return walks


# In[5]:

# def combineEmbedding(spaceFilePath, timeFilePath, time_step,input_direc):
#     spaceDict = dict()
#     timeDict = dict()
#     finalEmb = dict()

#     print spaceFilePath, timeFilePath
#     with open(spaceFilePath,"r") as inFile:
#         inFile.readline()
#         for line in inFile:
#             token = line.strip().split(" ")
#             if "_"+str(time_step) in token[0]:
#                 spaceDict[token[0]] = [token[i] for i in range(1,len(token))]
#                 print spaceDict[token[0]]

#     with open(timeFilePath,"r") as inFile:
#         inFile.readline()
#         for line in inFile:
#             token = line.strip().split(" ")
#             if "_"+str(time_step) in token[0]:
#                 timeDict[token[0]] = [token[i] for i in range(1,len(token))]
#                 print timeDict[token[0]]


#     for spaceKey in spaceDict:
#         if spaceKey in timeDict:
#             finalEmb[spaceKey] = []
#             for i in range(len(spaceDict[spaceKey])):
#                     lst = finalEmb[spaceKey]
#                     spacelist = spaceDict[spaceKey]
#                     timelist = timeDict[spaceKey]
#                     lst.append((float(spacelist[i])+float(timelist[i])))
#                     finalEmb[spaceKey] = lst

#             print spaceKey, finalEmb[spaceKey]

#             # find out how is all nodes have time walk and is yes store each time file as separate
#     path = input_direc+"window_4/combineSpaceTime_files/final_spacetimecombined"+str(time_step)+".spacetimerep"
#     with open(path,"w") as inFile:
#         for key in finalEmb:
#             inFile.write(key+" ")
#             for val in finalEmb[key]:
#                 inFile.write(str(val)+" ")
#             inFile.write("\n")
#     print("Combined representation file saved: "+path)
#     return

def combineEmbedding(spaceFilePath, timeFilePath, time_step,input_direc):
    spaceDict = dict()
    timeDict = dict()
    finalEmb = dict()

    with open(spaceFilePath,"r") as inFile:
        for line in inFile:
            token = line.strip().split("|")
            if "_"+str(time_step) in token[0]:
                # spaceDict[token[0]] = token[1]
                rep = token[1].strip().split(" ")
                # print len(rep)
                spaceDict[token[0]] = [rep[i] for i in range(0,len(rep))]

    with open(timeFilePath,"r") as inFile:
        for line in inFile:
            token = line.strip().split("|")
            if "_"+str(time_step) in token[0]:
                # timeDict[token[0]] = token[1]
                rep = token[1].strip().split(" ")
                # print timeDict[token[0]]
                timeDict[token[0]] = [rep[i] for i in range(0,len(rep))]

    for spaceKey in spaceDict:
        if spaceKey in timeDict:
            finalEmb[spaceKey] = []
            for i in range(len(spaceDict[spaceKey])):
                    lst = finalEmb[spaceKey]
                    spacelist = spaceDict[spaceKey]
                    timelist = timeDict[spaceKey]
                    lst.append((float(spacelist[i])+float(timelist[i])))
                    finalEmb[spaceKey] = lst

            #find out how is all nodes have time walk and is yes store each time file as separate
    path = input_direc+"/window_6/combineSpaceTime_final/final_spacetimecombined"+str(time_step)+".spacetimerep"
    with open(path,"w") as inFile:
        for key in finalEmb:
            inFile.write(key+" ")
            for val in finalEmb[key]:
                inFile.write(str(val)+" ")
            inFile.write("\n")
    print("Combined representation file saved: "+path)
    return


# In[6]:

def combineSpaceaTimeWalk(input_direc, output_file, number_restart, walk_length_time,walk_length_space, representation_size, time_step,
                      time_window_size, workers,vocab_window_size):
    if time_window_size>time_step:
        sys.exit("ERROR: time_window_size(="+str(time_window_size)+") cannot be more than time_step(="+str(time_step)+"):")

    if walk_length_space<vocab_window_size:
        print("WARNING: space_walk length cannot be less than window size. Setting space_walk_length=window_size")
        walk_length_space = vocab_window_size
    if walk_length_time<vocab_window_size:
        print("WARNING: time_walk length cannot be less than window size. Setting time_walk_length=window_size")
        walk_length_time = vocab_window_size

    G_list = [nx.read_graphml(input_direc + "graphs_order/graph_" + str(i) + ".graphml") for i in range(time_step-time_window_size, time_step+1)]

    ################
    #  spaceWalk  ##
    ###############
    # get list of nodes
    nodes = G_list[-1].nodes()
    print("Creating vocabulary")
    spacewalks = create_vocab(G_list, num_restart=number_restart, path_length=walk_length_space, nodes=nodes,
                         rand=random.Random(0), time_step=time_step, isTimeWalk=False, time_window=0)

    # time-step is decremented by 1, because, time steps are from 0 to time_step-1=total time_step length
    print("Generating representation from spaceWalk")
    model = Word2Vec(spacewalks, size=representation_size, window=vocab_window_size, min_count=0, workers=workers)
    space_output_file = "space_"+output_file
    model.wv.save_word2vec_format(input_direc +"window_6/combineSpaceTime_files/"+ space_output_file)
    print("Space Representation File saved: "+input_direc +"window_6/combineSpaceTime_files/"+ space_output_file)

    ################
    #  timeWalk  ##
    ###############
    # get list of nodes
    nodes = G_list[-1].nodes()
    print("Creating vocabulary")
    timewalks = create_vocab(G_list, num_restart=number_restart, path_length=walk_length_space, nodes=nodes,
                         rand=random.Random(0), time_step=time_step, isTimeWalk=True, time_window=time_window_size)

    # time-step is decremented by 1, because, time steps are from 0 to time_step-1=total time_step length
    print("Generating representation from spaceWalk")
    model = Word2Vec(timewalks, size=representation_size, window=vocab_window_size, min_count=0, workers=workers)
    time_output_file = "time_"+output_file
    model.wv.save_word2vec_format(input_direc +"window_6/combineSpaceTime_files/"+ time_output_file)
    print("Time Representation File saved: "+input_direc +"window_6/combineSpaceTime_files/"+ time_output_file)

    #################################
    # combining two representation ##
    #################################
    combineEmbedding(input_direc +"window_6/combineSpaceTime_final/"+ space_output_file,
                     input_direc +"window_6/combineSpaceTime_final/"+ time_output_file,
                     time_step,input_direc)

    return


# In[7]:


number_restart = 40
walk_length_time = 30
walk_length_space = 30
representation_size = 128
#time_step = 3
#time_window_size = 3
vocab_window_size = 5
workers = cpu_count()
print(workers)


#direc = "/home/cs15mtech11016/spacetimeCombined/"
direc = "/home/himangi/Internship/Work/DBLP/"
seq=[]
for i in range(36,46):
    if (i+1)%6==0:
        seq.append(i)

for t in seq:
    print("\n***Generating "+str(representation_size)+" dimension embeddings for nodes at t="+str(t))
    time_step = t
    time_window_size = 5 # including current time step total window size is of 5 time-step
    start = time.time()
    combineSpaceaTimeWalk(direc, "space_time_" + str(time_step)+".spacetimerep", number_restart=number_restart,
                      walk_length_time=walk_length_time,walk_length_space=walk_length_space, vocab_window_size=vocab_window_size,
                      representation_size=representation_size, time_step=time_step, time_window_size=time_window_size,
                      workers=workers)

    print("TIME:"+str(t)+" file generation time="+str((time.time()-start)))

