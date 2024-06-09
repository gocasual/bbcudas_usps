from scripts.graph_connector import query_executor
from scripts.neo4j_to_networkx import graph_from_cypher
from scripts.louvain_community_detection import louvain_community

query = '''
        MATCH (m:mailPiece)-[r:`goes to`] -> (o:destination) 
        WHERE o.destaddress_STATENAME = "Florida"
        RETURN m, r, o
        '''

data = query_executor(query)
G = graph_from_cypher(data)
louvain_community(G)