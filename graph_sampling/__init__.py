#!/usr/bin/env python3

import collections
import graph_tools
import random
import randwalk

from typing import Any

class Sampler():
    def __init__(self, g: graph_tools.Graph):
        self.g = g

class NodeSampler(Sampler):
    def sample_nodes(self,
                     p: float,
                     weight_dict: dict[Any, float]) -> set[Any]:
        vertices = set(self.g.vertices())
        V: set[Any] = set()
        for _ in range(int(self.g.nvertices() * p)):
            v = self.sample_node(vertices, weight_dict)
            V.add(v)
            vertices.remove(v)
            del weight_dict[v]
        return V

    def sample_node(self,
                    nodes: set[Any],
                    weight_dict: dict[Any, float]) -> Any:
        V = list(nodes)
        weights = [weight_dict[v] for v in V]
        return random.choices(V, weights=weights, k=1)[0]

    def subgraph_from_nodes(self, V: set[Any]) -> graph_tools.Graph:
        g = graph_tools.Graph(directed=self.g.directed())
        g.add_vertices(*V)
        for u in V:
            for v in V:
                if self.g.has_edge(u, v) and not g.has_edge(u, v):
                    g.add_edge(u, v)
        return g

class RandomNodeSampler(NodeSampler):
    def sample(self, p: float) -> graph_tools.Graph:
        weight_dict = {v: 1. for v in self.g.vertices()}
        V = self.sample_nodes(p, weight_dict)
        return self.subgraph_from_nodes(V)

class RandomDegreeNodeSampler(NodeSampler):
    def sample(self, p: float) -> graph_tools.Graph:
        weight_dict = {v: self.g.degree(v) for v in self.g.vertices()}
        V = self.sample_nodes(p, weight_dict)
        return self.subgraph_from_nodes(V)

class Crawler(NodeSampler):
    def __init__(self, g: graph_tools.Graph):
        super().__init__(g)
        self._explored: list[Any] = []

    def sample(self, p: float) -> graph_tools.Graph:
        components = self.g.components()
        random.shuffle(components)
        for c in components:
            self.sample_by_component(c)
        V = set(self._explored[:int(self.g.nvertices() * p)])
        return self.subgraph_from_nodes(V)

    def sample_by_component(self, component: set[Any]):
        pass

    def is_component_explored(self, component: set[Any]) -> bool:
        return component - set(self._explored) == set()

class BFSCrawler(Crawler):
    def sample_by_component(self, component: set[Any]):
        q = collections.deque()
        q.append(random.choice(list(component)))
        while not self.is_component_explored(component):
            v = q.popleft()
            if not v in self._explored:
                self._explored.append(v)
                N = list(self.g.neighbors(v))
                random.shuffle(N)
                for w in N:
                    q.append(w)        

class DFSCrawler(Crawler):
    def sample_by_component(self, component: set[Any]):    
        q = collections.deque()
        q.append(random.choice(list(component)))
        while not self.is_component_explored(component):
            v = q.pop()
            if not v in self._explored:
                self._explored.append(v)
                N = list(self.g.neighbors(v))
                random.shuffle(N)
                for w in N:
                    q.append(w)

class RWCrawler(Crawler):
    def sample_by_component(self, component: set[Any], c: float = 0.15):
        s = random.choice(list(component))
        agent = randwalk.SRW(self.g, current=s)
        while not self.is_component_explored(component):
            if not agent.current in self._explored:
                self._explored.append(agent.current)
            if random.uniform(0, 1) <= c:
                agent.current = s
            agent.advance()

class RJCrawler(Crawler):
    def sample_by_component(self, component: set[Any], c: float = 0.15):
        s = random.choice(list(component))
        agent = randwalk.SRW(self.g, current=s)
        while not self.is_component_explored(component):
            if not agent.current in self._explored:
                self._explored.append(agent.current)
            if random.uniform(0, 1) <= c:
                agent.current = random.choice(list(component))
            agent.advance()            
