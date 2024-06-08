from scripts.graph_connector import query_executor
from scripts.neo4j_to_networkx import graph_from_cypher


query = '''
        MATCH (m:mailPiece)-[r:`goes to`] -> (o:destination) 
        WHERE o.destaddress_STATENAME = "Florida"
        RETURN m, r, o
        '''

data = query_executor(query)
G = graph_from_cypher(data)
print(list(G.nodes.data()))