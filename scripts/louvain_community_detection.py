'''
Script to test out the functionality of the NetworkX 
graph network algorithms for community detection
'''
from random import randint
import matplotlib.pyplot as plt
import networkx as nx
from networkx import community
import pandas as pd
from dotenv import load_dotenv
import time

load_dotenv()


def louvain_community(G):
    print('generating communities')
    start = time.time()
    partition =community.louvain_communities(G)
    pos = nx.spring_layout(G)
    end = time.time()
    print(f'elapsed time: {end-start}')
    return partition


def neo4j_louvain_community(graph_name):
    query = f'''CALL gds.louvain.stream(
               graphName: {graph_name},
               configuration: Map
               )
              YIELD
              nodeId: Integer,
              communityId: Integer,
              intermediateCommunityIds: List of Integer'''
    return query


def draw_communities(G, communities):
    colors = ["" for x in range(G.number_of_nodes())] 
    counter = 0
    for community in communities:
        color = "#%06X" % randint(0, 0xFFFFFF)  
        counter += 1
        for node in list(community):  
            colors[node] = color
    counter
    pos = nx.spring_layout(G, iterations=15, seed=33)
    plt.figure(figsize=(15, 9))
    plt.axis("off")
    nx.draw_networkx(G, 
                     pos=pos, 
                     node_size=10, 
                     with_labels=False, 
                     width=0.15, 
                     node_color=colors
    )
    plt.savefig('community_graph.png')
    return counter


def evaluate_community(G, communities):
    modularity_score = communities.modularity(G, communities)
    results = pd.DataFrame(modularity_score)
    return results


def score_fraud():
    # in a given community, count the number of total fraud indicators
    # do some fraud indicators carry more weight?
    # normalize the total between 1-0
    # multiply that against the modularity score
    # rank the communities
    pass