
import networkx as nx
import pytest
from scripts.community_scoring import *


G = nx.Graph()
labels = ['owner', 'mailer', 'mailPiece', 'label', 'origin', 'destination']
for i in range(1, 7):
    G.add_node(i, label=labels[i-1])
edges = [(1, 2, {'type_': 'owns', 'properties': {'weight': 2}}), 
         (2, 3, {'type_': 'mails', 'properties': {'weight': 1}}), 
         (4, 3, {'type_': 'attaches_to', 'properties': {'weight': 2}}), 
         (3, 5, {'type_': 'originates_at', 'properties': {'weight': 2}}), 
         (3, 6, {'type_': 'goes_to', 'properties': {'weight': 1}})]
G.add_edges_from(edges)

communities = [{1, 2, 3}, {4, 5, 6}]
community1 = {1, 2, 3}
community2 = {4, 5, 6}
community3 = {1, 2, 3, 4, 5, 6}


def test_make_unfrozen_subgraph():
    graph = make_unfrozen_subgraph(G, community1)
    assert len(graph.nodes()) == 3
    assert len(graph.edges()) == 2
    assert 1 in graph.nodes() 
    assert 2 in graph.nodes()
    assert 3 in graph.nodes()
    assert 5 not in graph.nodes()


def test_community_density():
    graph = make_unfrozen_subgraph(G, community1)
<<<<<<< HEAD
    density1 = community_density(graph)
    density2 = community_density(graph)
    assert density1 >= 0
    assert density2 >= 0
    assert density2 / density1 == 1
=======
    density1 = community_density(graph, weight = 1)
    density2 = community_density(graph, weight = 2)
    assert density1 >= 0
    assert density2 >= 0
    assert density2 / density1 == 2
>>>>>>> main
    assert density1 <= 1


def test_potential_fraud_subgraph():
    unfrozen = make_unfrozen_subgraph(G, community3)
    graph = potential_fraud_subgraph(unfrozen)
    for node, data in list(graph.nodes(data=True)):
        assert 'destination' not in data['label']
    for node1, node2, data in list(graph.edges(data=True)):
        assert 'goes_to' not in data['type_']
        assert 'mails' not in data['type_']
    assert len(list(graph.nodes())) == 5
    assert len(list(graph.edges)) == 3


def test_potential_fraud_score():
    unfrozen = make_unfrozen_subgraph(G, community1)
    sub = potential_fraud_subgraph(unfrozen)
<<<<<<< HEAD
    score1 = potential_fraud_score(sub)
    assert score1 == (1/3)


def test_geo_mean():
    output_high = geo_mean(0.5, 0.005)
    output_middle = geo_mean(0.4, 0.001)
    output_low = geo_mean(0.05, 0.0005)
    assert output_high > output_middle
    assert output_middle > output_low
    assert output_high > output_low


def test_community_score():
    score1 = community_score(G, community1)
    assert score1 == math.sqrt((2/3)*(1/3))
=======
    score1 = potential_fraud_score(sub, weight=1)
    score2 = potential_fraud_score(sub, weight=2)
    assert score1 == (1/3)
    assert score2 == (2/3) 
    assert score1 >= 0
    assert score2 >= 0  


def test_log_transform():
    output1 = log_transform(1, 10)
    assert output1 == 2


def test_community_score():
    score1 = community_score(G, community1, type='log')
    score2 = community_score(G, community1, d_weight=1, f_weight=1, type='weighted')
    score3 = community_score(G, community1, d_weight=0.0, f_weight=0.0, type='weighted')
    assert score1 == 
    assert score2 == 1.0 
    assert score3 == 0
>>>>>>> main



