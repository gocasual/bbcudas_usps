'''
Algorithm for scoring communities as a function of community 
significance factors, and potential fraud indicators. 

Goal of the algorithm is to return a prioritized list of 
the most influential communities that have the highest 
potential of fraudulent activity. 
'''
import networkx as nx

def potential_fraud_subgraph(G, community):
    '''1. get nodes in community
       2. create a subgraph
       2a. drop all nodes with label 'destination'
       2b. remove all edges with label 'goes_to' and 'mails'
       3. filter the subgraph for nodes that could be potential fraud relationships
       '''
    sub_graph = G.subgraph(community)
    unfrozen_graph = nx.Graph(sub_graph)
    for node, data in list(unfrozen_graph.nodes(data=True)):
        if 'labels' in data and 'destination' in data['labels']:
            unfrozen_graph.remove_node(node)
    
    for node1, node2, data in list(unfrozen_graph.edges(data=True)):
        if data['type_'] in ['goes_to', 'mails']:
            unfrozen_graph.remove_edge(node1, node2)

    return unfrozen_graph


def potential_fraud_score(graph):
    ''' 4. calculate the total number of potential fraud count_fraud_indicators
        5. calculate total number of possible relationships
        6. return the community fraud score
        '''
    sum_fraud_edges = 0
    for node1, node2, data in list(graph.edges(data=True)):
        if data['properties']['weight'] == 2:
            sum_fraud_edges += 1

    total_nodes = graph.number_of_nodes()
    fraud_density = (2 * sum_fraud_edges) / (total_nodes * (total_nodes - 1))

    return fraud_density