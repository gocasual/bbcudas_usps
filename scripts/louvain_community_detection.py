'''
Script to test out the functionality of the NetworkX 
graph network algorithms for community detection
'''
import matplotlib.cm as cm
import matplotlib.pyplot as plt
import networkx as nx
from networkx import community as community_louvain
import os
from dotenv import load_dotenv
from neo4j import GraphDatabase

load_dotenv()


URI = os.getenv("NEO4J_URI")
USERNAME = os.getenv("NEO4J_USERNAME")
PASSWORD = os.getenv("NEO4J_PASSWORD")
AUTH = (USERNAME, PASSWORD)

with GraphDatabase.driver(URI, auth=AUTH) as driver:
    driver.verify_connectivity()


G = nx.karate_club_graph()

# first compute the best partition
partition = community_louvain.best_partition(G)

# draw the graph
pos = nx.spring_layout(G)

# color the nodes according to their partition
cmap = cm.get_cmap('viridis', max(partition.values()) + 1)
nx.draw_networkx_nodes(G, pos, partition.keys(), node_size=40, cmap=cmap, node_color=list(partition.values()))
nx.draw_networkx_edges(G, pos, alpha=0.5)
plt.show()
