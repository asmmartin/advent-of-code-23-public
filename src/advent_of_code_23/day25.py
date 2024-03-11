'''https://adventofcode.com/2023/day/25'''

# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring

from math import prod
import sys
from collections import defaultdict
from copy import deepcopy

import networkx as nx

def generate_graph_from_string(text: str) -> dict[str, set[str]]:
    graph = defaultdict(set)
    lines = text.strip().splitlines()
    for line in lines:
        node, connections = line.split(': ')
        connections = connections.split()
        graph[node].update(connections)
        for connection in connections:
            graph[connection].add(node)
    return dict(graph)

def get_graph_groups(graph: dict[str, set[str]]) -> list[set[str]]:
    groups = []

    visited = set()
    for node in graph:
        if node in visited:
            continue
        visited.add(node)

        group = set()

        to_visit = [node]
        while to_visit:
            group_node = to_visit.pop()
            visited.add(group_node)
            group.add(group_node)
            for connection in graph[group_node]:
                if connection not in visited:
                    to_visit.append(connection)
        groups.append(group)

    return groups

def find_splitting_edges(graph: dict[str, set[str]]) -> set[tuple[str, str]]:

    # Using networkx. It's Christmas Day. I do not wan't to overthink...
    nx_graph = nx.Graph(graph)
    min_cuts = nx.minimum_edge_cut(nx_graph)
    return set(tuple(sorted(edge)) for edge in min_cuts) # type: ignore

def split_graph(
    graph: dict[str, set[str]], cuts: set[tuple[str, str]]
)-> dict[str, set[str]]:

    splitted_graph = deepcopy(graph)

    for edge in cuts:
        splitted_graph[edge[0]].remove(edge[1])
        splitted_graph[edge[1]].remove(edge[0])
    return splitted_graph

def main(input_text: str):
    graph = generate_graph_from_string(input_text)
    cuts = find_splitting_edges(graph)
    splitted_graph = split_graph(graph, cuts)
    groups = get_graph_groups(splitted_graph)
    result = prod(len(group) for group in groups)
    print(f'Solution day 25: {result}')

if __name__ == "__main__":
    INPUT_TEXT = sys.stdin.read().strip()
    main(INPUT_TEXT)
