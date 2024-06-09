'''
Script to test out the functionality of the NetworkX 
graph network algorithms for community detection
'''
import matplotlib.cm as cm
import matplotlib.pyplot as plt
import networkx as nx
from networkx import community
from dotenv import load_dotenv

load_dotenv()

def louvain_community(G):

    # first compute the best partition
    partition =community.louvain_communities(G)

    # draw the graph
    pos = nx.spring_layout(G)

    # color the nodes according to their partition
    cmap = cm.get_cmap('viridis', max(partition.values()) + 1)
    nx.draw_networkx_nodes(G, pos, partition.keys(), node_size=40, cmap=cmap, node_color=list(partition.values()))
    nx.draw_networkx_edges(G, pos, alpha=0.5)
    plt.show()
