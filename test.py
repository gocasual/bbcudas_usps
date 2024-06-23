from scripts.graph_connector import query_executor
from scripts.neo4j_to_networkx import graph_from_cypher
from scripts.louvain_community_detection import *
from scripts.sample_queries import *


data = query_executor(query_all_data)

G = graph_from_cypher(data)

communities = louvain_community(G)
draw_communities(G, communities)
results = evaluate_community(G, communities)
print(results)
write_communities_json(communities)