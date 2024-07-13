'''
Algorithm for scoring communities as a function of community 
significance factors, and potential fraud indicators. 

Goal of the algorithm is to return a prioritized list of 
the most influential communities that have the highest 
potential of fraudulent activity. 
'''
import math
import networkx as nx


def make_unfrozen_subgraph(G, community):
    sub_graph = G.subgraph(community)
    unfrozen_graph = nx.Graph(sub_graph)
    return unfrozen_graph


def community_density(unfrozen_graph, weight=1):
    '''
    calculate and return the density of a given community. 
    '''
    density = nx.density(unfrozen_graph)
    weighted_density = density * weight
    return weighted_density


def potential_fraud_subgraph(unfrozen_graph):
    '''1. get nodes in community
       2. create a subgraph
       2a. drop all nodes with label 'destination'
       2b. remove all edges with label 'goes_to' and 'mails'
       3. filter the subgraph for nodes that could be potential fraud relationships
       '''
    for node, data in list(unfrozen_graph.nodes(data=True)):
        if 'labels' in data and 'destination' in data['labels']:
            unfrozen_graph.remove_node(node)
    
    for node1, node2, data in list(unfrozen_graph.edges(data=True)):
        if data['type_'] in ['goes_to', 'mails']:
            unfrozen_graph.remove_edge(node1, node2)

    return unfrozen_graph


def potential_fraud_score(graph, weight=1):
    ''' 4. calculate the total number of potential fraud count_fraud_indicators
        5. calculate total number of possible relationships
        6. return the community fraud score
        '''
    sum_fraud_edges = 0
    for node1, node2, data in list(graph.edges(data=True)):
        if data['properties']['weight'] <= 2:
            sum_fraud_edges += 1

    total_nodes = graph.number_of_nodes()
    fraud_density = (2 * sum_fraud_edges) / (total_nodes * (total_nodes - 1))
    weighted_density = fraud_density * weight
    return weighted_density


def log_transform(score1, score2):
    return score1 + math.log(score2, 10)


def community_score(G, community, d_weight=1, f_weight=1, type='weighted'):
    unfrozen_graph = make_unfrozen_subgraph(G, community)
    if type == 'weighted':
        density = community_density(unfrozen_graph, weight=d_weight)
        fraud_subgraph = potential_fraud_subgraph(unfrozen_graph)
        fraud_density = potential_fraud_score(fraud_subgraph, weight=f_weight)
        score = density + fraud_density
        print(f'density: {density} ' \
            f'fraud_density: {fraud_density} ' \
            f'score: {score}' ) 
    elif type == 'log':
        density = community_density(unfrozen_graph, weight=1)
        fraud_subgraph = potential_fraud_subgraph(unfrozen_graph)
        fraud_density = potential_fraud_score(fraud_subgraph, weight=1)
        plus_one = fraud_density + 1
        score = log_transform(density, plus_one)
        print(f'density: {density} ' \
            f'fraud_density: {fraud_density} ' \
            f'score: {score}' ) 
    else:
        print('type must be weighted or log')
    return score