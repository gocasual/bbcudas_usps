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
import os

matplotlib.use('Agg')
load_dotenv()


def louvain_community(G, weight='weight', seed=33):
    # runs the Louvain Algorithm with added features
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
    # from a list of communities, selects the N largest communities by node size
    sorted_communities = sorted(communities, key=len, reverse=True)
    top_communities = sorted_communities[:n]
    return top_communities


def make_subgraph(G, communities):
    # make a subgraph made up of the 3 biggest communities
    top_nodes = [node for community in communities for node in community]
    subgraph = G.subgraph(top_nodes)
    return subgraph


def write_communities_json(communities):
    result_path = os.path.join('.', 'data', 'result_community.json')
    community_dict = {f'{index}':list(community) for index, community in enumerate(communities)}
    with open(result_path, 'w') as f:
        json.dump(community_dict, f, indent=2)