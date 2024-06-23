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
import json

load_dotenv()


def louvain_community(G):
    print('Generating communities...')
    start = time.time()
    partition =community.louvain_communities(G)
    end = time.time()
    print(f'Community detection elapsed time: {end-start}')
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
    colors = {}
    counter = 0
    for community in communities:
        color = "#{:06x}".format(randint(0, 0xFFFFFF))
        counter += 1
        print(list(community))
        for node in list(community):  
            colors[node] = color
    pos = nx.spring_layout(G, iterations=15, seed=33)
    plt.figure(figsize=(15, 9))
    plt.axis("off")
    nx.draw_networkx(G, 
                     pos=pos, 
                     node_size=10, 
                     with_labels=False, 
                     width=0.15, 
                     node_color=[colors[node] for node in G.nodes()]
    )
    plt.savefig('community_graph.png')
    return counter


def evaluate_community(G, communities):
    print(communities)
    modularity_score = community.modularity(G, communities)
    print(modularity_score)
    # results = pd.DataFrame({"modularity": modularity_score})
    return modularity_score


def score_fraud():
    # in a given community, count the number of total fraud indicators
    # do some fraud indicators carry more weight?
    # normalize the total between 1-0
    # multiply that against the modularity score
    # rank the communities
    pass


def write_communities_json(communities):
    community_dict = {f'community_{index}':list(community) for index, community in enumerate(communities)}
    with open('result_community.json', 'w') as f:
        json.dump(community_dict, f, indent=2)