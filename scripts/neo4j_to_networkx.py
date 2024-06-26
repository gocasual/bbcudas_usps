'''
Script that defines function to query data from Neo4J and
put it into a networkX graph to be able to run networkX algos
'''
from neo4j.graph import Node, Relationship
from neo4j.data import Record
import networkx as nx


def graph_from_cypher(data):
    G = nx.MultiGraph()

    def add_node(node):
        u = node.id
        if G.has_node(u):
            return
        G.add_node(u, labels=node._labels, properties=dict(node))

    def add_edge(relation):
        for node in (relation.start_node, relation.end_node):
            add_node(node)
        u = relation.start_node.id
        v = relation.end_node.id
        eid = relation.id
        if G.has_edge(u, v, key=eid):
            return
        G.add_edge(u, v, key=eid, type_=relation.type, properties=dict(relation))

    for d in data:
        try:
            for entry in d:
                for k, v in entry.items():
                    if isinstance(v, Node):
                        add_node(v)  
                    elif isinstance(v, Relationship):
                        add_edge(v)
                    else:
                        pass
        except (TypeError, AttributeError):
            if TypeError:
                print('Node or Edge import error - Type error - continuing')
            if AttributeError:
                print('Node or Edge import error - Attribute error - continuing')
            pass
    
    num_nodes = G.number_of_nodes()
    num_edges = G.number_of_edges()
    print(f"total nodes: {num_nodes}, total edges: {num_edges}")
    
    return G


def dataframe_of_edges(G):
    pass