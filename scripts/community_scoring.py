'''
Algorithm for scoring communities as a function of community 
significance factors, and potential fraud indicators. 

Goal of the algorithm is to return a prioritized list of 
the most influential communities that have the highest 
potential of fraudulent activity. 
'''
import math
import networkx as nx
import pandas as pd

def make_unfrozen_subgraph(G, community):
    sub_graph = G.subgraph(community)
    unfrozen_graph = nx.Graph(sub_graph)
    for node, data in list(unfrozen_graph.nodes(data=True)):
        if 'labels' in data and 'manifest' in data['labels']:
            unfrozen_graph.remove_node(node)
    for node1, node2, data in list(unfrozen_graph.edges(data=True)):
        if data['type_'] in ['attaches_to']:
            unfrozen_graph.remove_edge(node1, node2)
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
    return density,fraud_density,score

def graph_to_pandas(graph,debug=False):
  """
  Converts a NetworkX graph to Pandas DataFrames for nodes and edges.

  Args:
    graph: A NetworkX graph object.
    debug: If True, prints additional information about node and edge labels.

  Returns:
    A tuple of two Pandas DataFrames: (df_nodes, df_edges)
  """

  # Extract node data into a DataFrame
  nodes_dict = dict(graph.nodes(data=True))
  df_nodes = pd.DataFrame.from_dict(nodes_dict, orient='index')

  # Extract edge data into a DataFrame
  df_edges = nx.to_pandas_edgelist(graph)

  # Expand edge properties into separate columns
  weights = df_edges['properties'].apply(pd.Series)
  df_edges = pd.concat([df_edges.drop('properties', axis=1), weights], axis=1)

  if debug:
    print(f"Community has {graph.number_of_nodes()} nodes and {graph.number_of_edges()} edges.")  # Print graph summary
    print(f'Nodes:\n',df_nodes.labels.value_counts())  # Print node label counts
    print(f'Edges:\n',df_edges['type_'].value_counts())  # Print edge type counts

  return df_nodes, df_edges

def get_perc_fraud_indicators(df_edges, df_nodes):
    """
    This function analyzes a graph structure to identify potential fraud indicators based on edge types and weights.

    Args:
        df_edges (DataFrame): A DataFrame representing the edges in the graph, with columns:
            - 'type_' (str): The type of the edge.
            - 'weight' (numeric): The weight of the edge (higher indicates stronger connection).
        df_nodes (DataFrame): A DataFrame representing the nodes in the graph. Not directly used in this function 
                             but passed to 'get_indicator_type'.

    Returns:
        DataFrame: A summary DataFrame with the following columns:
            - 'type' (str): The type of edge.
            - 'count' (int): The total count of edges of that type.
            - 'weight_count' (int): The count of edges of that type with weight > 1.
            - 'pct' (float): The percentage of edges of that type with weight > 1.
    """

    # Count occurrences of each edge type
    df_type_counts = df_edges['type_'].value_counts().reset_index()
    df_type_counts.columns = ['type', 'count']  

    # Count occurrences of each edge type where weight > 1
    df_weights = (
        df_edges['type_'][df_edges['weight'] > 1]
        .value_counts()
        .reset_index()
        .fillna(0)
        .rename(columns={'type_': 'type', 'count': 'weight_count'})
    )

    # Special Handling for 'part_of' Edge Type
    if 'part_of' in df_weights['type'].values:  # Check if 'part_of' type exists
        print('Getting counts for the two indicator in the part of edge...')

        # Placeholder for get_indicator_type function
        df_part_of = get_indicator_type(df_nodes, df_edges)  

        # Remove the 'part_of' entry from the original weighted counts
        df_weights = df_weights[df_weights['type'] != 'part_of']

        # Combine the original weighted counts with the modified 'part_of' counts
        df_weights_mod = pd.concat([df_weights, df_part_of])

        # Merge the type counts with the potentially modified weight counts
        df_merged = pd.merge(df_type_counts, df_weights_mod, on='type', how='left')

        # Prioritize the 'new_type' column (from get_indicator_type) over the original 'type'
        df_merged['new_type'] = df_merged['new_type'].combine_first(df_merged['type'])
        df_merged = (df_merged.fillna({'weight_count': 0})  # Fill missing values with 0
                      .drop('type', axis=1)  # Drop the original 'type' column
                      .rename(columns={'new_type': 'type'}))  # Rename the new type column

    else:  # No 'part_of' edges, merge type counts with original weight counts directly
        df_merged = pd.merge(df_type_counts, df_weights, on='type', how='left')
        df_merged = df_merged.fillna(0)
    # Calculate percentage of weighted edges per type
    df_merged['pct'] = df_merged['weight_count'] / df_merged['count'] * 100

    return df_merged


def get_indicator_type(df_nodes, df_edges):
    """
    Analyzes 'part_of' edges with weight > 1 to identify potential fraud indicators.

    Args:
        df_nodes (DataFrame): DataFrame with node information, including a 'properties' column 
                             containing a dictionary with properties like 'manifest' and 'labels'.
        df_edges (DataFrame): DataFrame with edge information, including columns 'source', 'target', 
                             'type_', and 'weight'.

    Returns:
        DataFrame: A DataFrame with the following columns:
            - 'type': Always 'part_of'.
            - 'new_type': Either 'part_of_mismatch' or 'part_of_manifest'.
            - 'weight_count': The count of edges falling into the new_type category.
    """

    # Filter for high-weight 'part_of' edges
    high_weight_part_of = df_edges[(df_edges['type_'] == 'part_of') & (df_edges['weight'] > 1)]
    print('here')
    # Get node properties for target nodes of high-weight 'part_of' edges
    target_nodes_ids = high_weight_part_of['target'].tolist()
    target_nodes = df_nodes[df_nodes.index.isin(target_nodes_ids)].copy()
    target_nodes_props = target_nodes['properties'].apply(pd.Series)
    target_nodes = pd.concat([target_nodes.drop('properties', axis=1), target_nodes_props], axis=1)
    target_nodes = target_nodes.merge(high_weight_part_of[['target', 'weight']], left_index=True, right_on='target')
    target_nodes = target_nodes.set_index('target')
    print(target_nodes.shape)
    # Get node properties for source nodes of high-weight 'part_of' edges
    source_nodes_ids = high_weight_part_of['source'].tolist()
    source_nodes = df_nodes[df_nodes.index.isin(source_nodes_ids)].copy()
    source_nodes_props = source_nodes['properties'].apply(pd.Series)
    source_nodes = pd.concat([source_nodes.drop('properties', axis=1), source_nodes_props], axis=1)
    source_nodes = source_nodes.merge(high_weight_part_of[['source', 'weight']], left_index=True, right_on='source')
    source_nodes = source_nodes.set_index('source')
    print(source_nodes.shape)

    # Combine target and source nodes
    source_target_nodes = pd.concat([target_nodes, source_nodes])

    # Filter for nodes where the 'labels' property is equal to a frozenset containing 'label'
    source_target_nodes = source_target_nodes[source_target_nodes['labels'] == frozenset({'label'})].drop_duplicates()

    # Create a DataFrame for calculations
    df = source_target_nodes.copy()[['manifest', 'weight']]

    # Create 'part_of_mismatch' indicator
    df.loc[:,'part_of_mismatch'] = (
    ((df['manifest'] == False) & (df['weight'] == 4)) | 
    ((df['manifest'] == True) & (df['weight'] == 2))
      ).astype(int)
    df.loc[:,'part_of_manifest'] = (df['manifest'] == False).astype(int)

    # Calculate sums for each indicator type
    df_sums = (
        df[['part_of_mismatch', 'part_of_manifest']].sum().reset_index().rename(columns={'index': 'new_type', 0: 'weight_count'})
    )
    df_sums['type'] = 'part_of'  # Add the original 'part_of' type

    return df_sums
