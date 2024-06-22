'''
Script to test out the functionality of the NetworkX 
graph network algorithms for community detection
'''
import matplotlib
import matplotlib.pyplot as plt
import networkx as nx
from networkx import community
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


def 
