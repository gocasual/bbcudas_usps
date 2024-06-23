import json
import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from random import randint
from scripts.graph_connector import query_executor
from scripts.neo4j_to_networkx import graph_from_cypher
from scripts.louvain_community_detection import louvain_community
from scripts.sample_queries import *


data = query_executor(query_company_delinked_mid)


G = graph_from_cypher(data)
communities = louvain_community(G)

community_dict = {f'community_{index}':list(community) for index, community in enumerate(communities)}

with open('result_community.json', 'w') as f:
    json.dump(community_dict, f, indent=2)