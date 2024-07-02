'''
Script to test out the functionality of the NetworkX 
graph network algorithms for community detection
'''
from random import randint
import matplotlib
import matplotlib.pyplot as plt
import networkx as nx
from networkx import community
import pandas as pd
import matplotlib
from dotenv import load_dotenv
import time
import json

matplotlib.use('Agg')
load_dotenv()


def louvain_community(G, weight='weight', seed=33):
    print('Generating communities...')
    start = time.time()
    partition =community.louvain_communities(G, weight=weight, seed=seed)
    end = time.time()
    print(f'Community detection elapsed time: {end-start}')
    communities = remove_singletons(partition)
    print(f'total communities with more than one node: {len(communities)}')
    return communities


def remove_singletons(communities):
    # get rid of communities of 1
    return [s for s in communities if len(s) > 1]


def select_communities(communities, n=3):
    sorted_communities = sorted(communities, key=len, reverse=True)
    top_communities = sorted_communities[:n]
    return top_communities


def make_subgraph(G, communities):
    # make a subgraph made up of the 3 biggest communities
    top_nodes = [node for community in communities for node in community]
    subgraph = G.subgraph(top_nodes)
    return subgraph


def community_colors(communities):
    colors = {}
    counter = 0
    print('begin coloring')
    for community in communities:
        color = "#{:06x}".format(randint(0, 0xFFFFFF))
        counter += 1
        for node in community: 
            colors[node] = color
    print('done with coloring')
    return colors


def draw_communities(G, colors, communities):
    pos = nx.spring_layout(G, iterations=15, seed=33)
    new_pos = {}
    offset = 0
    for community in communities:
        community_pos = {node: pos[node] for node in community}
        center = [sum(coord)/len(community_pos) for coord in zip(*community_pos.values())]
        for node in community:
            new_pos[node] = (pos[node][0] - center[0] + offset, pos[node][1] - center[1])
        offset +=2
    print("pos complete")
    plt.figure(figsize=(15, 9))
    plt.axis("off")
    print("drawing network")
    nx.draw_networkx(G, 
                     pos=new_pos, 
                     node_size=10, 
                     with_labels=False, 
                     width=0.15, 
                     node_color=[colors[node] for node in G.nodes()]
    )
    plt.savefig('community_graph.png')
    return plt


def community_node_count(G, communities):
    '''
    function to count the nodes in a community
    '''
    pass


def community_density():
    '''
    function to calculate the density of each community
    '''
    pass


def write_communities_json(communities):
    community_dict = {f'{index}':list(community) for index, community in enumerate(communities)}
    with open('result_community.json', 'w') as f:
        json.dump(community_dict, f, indent=2)