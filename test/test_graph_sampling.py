#!/usr/bin/env python3

import graph_tools

import graph_sampling

def test_subgraph_from_nodes():
    g = graph_tools.Graph(directed=False)
    g.add_edge(1, 2)
    g.add_edge(1, 3)
    g.add_edge(2, 3)
    g.add_edge(3, 4)
    sampler = graph_sampling.NodeSampler(g)

    gg = sampler.subgraph_from_nodes([1])
    assert set(gg.vertices()) == {1}
    assert set(gg.edges()) == set()    

    gg = sampler.subgraph_from_nodes([1, 2])
    assert set(gg.vertices()) == {1, 2}
    assert set(gg.edges()) == {(1, 2)}

    gg = sampler.subgraph_from_nodes([1, 2, 3])
    assert set(gg.vertices()) == {1, 2, 3}
    assert set(gg.edges()) == {(1, 2), (1, 3), (2, 3)}

    gg = sampler.subgraph_from_nodes([1, 4])
    assert set(gg.vertices()) == {1, 4}
    assert set(gg.edges()) == set()

