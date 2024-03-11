# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring

from math import prod
import pytest

from advent_of_code_23.day25 import (
    generate_graph_from_string, get_graph_groups, find_splitting_edges,
    split_graph
)

@pytest.fixture(name='example_text')
def example_text_fixture():
    return (
        'jqt: rhn xhk nvd\n'
        'rsh: frs pzl lsr\n'
        'xhk: hfx\n'
        'cmg: qnr nvd lhk bvb\n'
        'rhn: xhk bvb hfx\n'
        'bvb: xhk hfx\n'
        'pzl: lsr hfx nvd\n'
        'qnr: nvd\n'
        'ntq: jqt hfx bvb xhk\n'
        'nvd: lhk\n'
        'lsr: lhk\n'
        'rzs: qnr cmg lsr rsh\n'
        'frs: qnr lhk lsr'
    )

@pytest.fixture(name='example_graph')
def example_graph_fixture(example_text):
    return generate_graph_from_string(example_text)

@pytest.fixture(name='example_splitted_graph')
def example_splitted_graph_fixture():
    return generate_graph_from_string(
        'jqt: rhn xhk\n'
        'rsh: frs pzl lsr\n'
        'xhk: hfx\n'
        'cmg: qnr nvd lhk\n'
        'rhn: xhk bvb hfx\n'
        'bvb: xhk hfx\n'
        'pzl: lsr nvd\n'
        'qnr: nvd\n'
        'ntq: jqt hfx bvb xhk\n'
        'nvd: lhk\n'
        'lsr: lhk\n'
        'rzs: qnr cmg lsr rsh\n'
        'frs: qnr lhk lsr'
    )

def test_generate_graph_from_string(example_text):

    graph = generate_graph_from_string(example_text)

    assert 'rhn' in graph['jqt']
    assert 'jqt' in graph['rhn']

def test_get_graph_groups(example_graph, example_splitted_graph):

    groups = get_graph_groups(example_graph)
    splitted_groups = get_graph_groups(example_splitted_graph)

    assert len(groups) == 1
    assert len(splitted_groups) == 2

    assert prod(len(group) for group in splitted_groups) == 54

def test_find_splitting_edges(example_graph):

    edges = find_splitting_edges(example_graph)

    assert edges == {('hfx', 'pzl'), ('bvb', 'cmg'), ('jqt', 'nvd')}

def test_split_graph(example_graph, example_splitted_graph):

    splitted = split_graph(
        example_graph,
        cuts={('hfx', 'pzl'), ('bvb', 'cmg'), ('jqt', 'nvd')}
    )

    assert splitted == example_splitted_graph
