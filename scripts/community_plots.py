'''
Script for plotting differect visualizations. 
For plotting one community use draw_single_community
For plotting multiple communities use draw_multiple_communities
For par graphs use standard_plot
'''
import matplotlib.pyplot as plt
import pandas as pd
from random import randint
import networkx as nx
import matplotlib.patches as mpatches


def community_colors(communities):
    colors = {}
    counter = 0
    print('begin coloring')
    for community in communities:
        color = "#{:06x}".format(randint(0, 0xFFFFFF))
        counter += 1
        for node in community: 
            colors[node] = color
    print('done with coloring')
    return colors


def draw_multiple_communities(G, colors, communities):
    pos = nx.spring_layout(G, iterations=15, seed=33)
    new_pos = {}
    offset = 0
    for community in communities:
        community_pos = {node: pos[node] for node in community}
        center = [sum(coord)/len(community_pos) for coord in zip(*community_pos.values())]
        for node in community:
            new_pos[node] = (pos[node][0] - center[0] + offset, pos[node][1] - center[1])
        offset +=2
    plt.figure(figsize=(15, 9))
    plt.axis("off")
    nx.draw_networkx(G, 
                     pos=new_pos, 
                     node_size=50, 
                     with_labels=False, 
                     width=0.15, 
                     node_color=[colors[node] for node in G.nodes()]
    )
    plt.savefig('community_graph.png')
    return plt


def node_type_colors(sub_graph, color_map):
    node_color = [color_map[list(data['labels'])[0]] for node, data in sub_graph.nodes(data=True)]
    return node_color


def node_type_labels(sub_graph):
    return {node: list(data['labels'])[0] for node, data in sub_graph.nodes(data=True)}


def edge_weights(sub_graph):
    edge_map = {1: 0.5,
                2: 2.0,
                4: 4.0
                }
    edge_weight_list = [edge_map[data['properties']['weight']] for u, v, data in sub_graph.edges(data=True)]
    return edge_weight_list


def draw_single_community(sub_graph, one_community, id):
    color_map = {'mailPiece': 'red',
                'owner': 'tan',
                'label': 'orange',
                'mailer': 'green',
                'origin': 'purple',
                'destination': 'grey'}
    node_color = node_type_colors(sub_graph, color_map)
    node_labs = node_type_labels(sub_graph)
    edge_weight_list = edge_weights(sub_graph)
    pos = nx.kamada_kawai_layout(sub_graph)

    new_pos = {}
    offset = 0
    for community in one_community:
        community_pos = {node: pos[node] for node in community}
        center = [sum(coord)/len(community_pos) for coord in zip(*community_pos.values())]
    for node in community:
        new_pos[node] = (pos[node][0] - center[0] + offset, pos[node][1] - center[1])
        offset +=2
    node_size = 500 - 0.8*(len(list(sub_graph.nodes())))
    plt.figure(figsize=(10, 8))
    plt.axis("off")
    nx.draw_networkx(sub_graph, 
                        pos=new_pos, 
                        node_size=node_size,  
                        width=edge_weight_list, 
                        node_color=node_color,
                        with_labels=False
    )
    patchList = []
    for key in color_map:
        data_key = mpatches.Patch(color=color_map[key], label=key)
        patchList.append(data_key)
    plt.legend(handles=patchList)
    plt.title(f'Community Structure for Community #{id}')
    plt.show()


def node_type_count_bar_plot(df_sorted, rows):
    # Select percentage columns and first 10 rows (sroted by score)
    df_to_plot = df_sorted.iloc[rows, df_sorted.columns.str.endswith('_nodes')]

    # Transpose DataFrame for plotting
    df_to_plot = df_to_plot.transpose()

    # Create bar plot
    df_to_plot.plot(kind='bar', figsize=(10, 6), colormap="Set3")
    plt.xlabel('Label')
    plt.ylabel('Count')
    plt.title('Count of Node Labels for Top 10 Communities')
    plt.xticks(rotation=45)
    plt.legend(title='Community ID')
    plt.tight_layout()
    plt.show()


def standard_plot(df, type='barh', rows=None, cols='_nodes_perc', title='SAMPLE', x_label='SAMPLE', y_label='SAMPLE'):
    if rows:
        df_to_plot = df.iloc[rows, df.columns.str.endswith(f'{cols}')]
    else: 
        df_to_plot = df.iloc[:, df.columns.str.endswith(f'{cols}')].sort_index(ascending=False)

    df_to_plot.plot(kind=type, figsize=(12, 8))
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title)
    plt.xticks(rotation=45)
    plt.show()