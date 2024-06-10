from scripts.graph_connector import query_executor
from scripts.neo4j_to_networkx import graph_from_cypher
from scripts.louvain_community_detection import louvain_community
from scripts.sample_queries import *


data = query_executor(query_all_data)
# print(data.keys)
# print("\n")
# print(data.records)
# print("\n")
# print(data.summary.plan)
# print("\n")

G = graph_from_cypher(data)
print(G.size)
community = louvain_community(G)
print(community)
print(len(community))
for communities in community:
        for node_id in communities:
                print(G.nodes[node_id])
                print('\n')