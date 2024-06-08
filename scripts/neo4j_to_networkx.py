'''
Script that defines function to query data from Neo4J and
put it into a networkX graph to be able to run networkX algos
'''
from neo4j import GraphDatabase
from neo4j.graph import Node, Relationship
import networkx as nx


def graph_from_cypher(data):
    G = nx.MultiDiGraph()

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
        for entry in d:
            print(type(entry))
            for k, v in entry.items():
                if v:
                    add_node(v)
                elif #Record
                elif isinstance(v, Relationship):
                    add_edge(v)
                else:
                    pass
    return G


if __name__=='__main__':
    driver = GraphDatabase.driver('bolt://localhost:7687', auth=("neo4j", "hunter2"))
    query = """
    MATCH (p:Person)-[:ACTED_IN]->(m:Movie)
    WHERE toLower(m.title) CONTAINS "you"
    RETURN *
    """
    with driver.session() as session:
        result = session.run(query)
        G = graph_from_cypher(result.data())
