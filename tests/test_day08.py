# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring

import pytest

from advent_of_code_23.day08 import (
    Node, Network, Loop, get_loop_end_nodes_coefficient
)

@pytest.fixture(name='example_text_1')
def example_text_1_fixture():
    return(
        'RL\n'
        '\n'
        'AAA = (BBB, CCC)\n'
        'BBB = (DDD, EEE)\n'
        'CCC = (ZZZ, GGG)\n'
        'DDD = (DDD, DDD)\n'
        'EEE = (EEE, EEE)\n'
        'GGG = (GGG, GGG)\n'
        'ZZZ = (ZZZ, ZZZ)'
    )

@pytest.fixture(name='example_text_2')
def example_text_2_fixture():
    return(
        'LLR\n'
        '\n'
        'AAA = (BBB, BBB)\n'
        'BBB = (AAA, ZZZ)\n'
        'ZZZ = (ZZZ, ZZZ)'
    )

@pytest.fixture(name='example_text_3')
def example_text_3_fixture():
    return(
        'LR\n'
        '\n'
        '11A = (11B, XXX)\n'
        '11B = (XXX, 11Z)\n'
        '11Z = (11B, XXX)\n'
        '22A = (22B, XXX)\n'
        '22B = (22C, 22C)\n'
        '22C = (22Z, 22Z)\n'
        '22Z = (22B, 22B)\n'
        'XXX = (XXX, XXX)'
    )

@pytest.fixture(name='example_text_4')
def example_text_4_fixture():
    return(
        'LR\n'
        '\n'
        '11A = (11B, XXX)\n'
        '11B = (XXX, 11Z)\n'
        '11Z = (11B, XXX)\n'
        '22A = (22B, XXX)\n'
        '22B = (22C, 22C)\n'
        '22C = (22Z, 22Z)\n'
        '22Z = (22B, 22B)\n'
        '33A = (33B, 2BB)\n'
        '33B = (33C, 33C)\n'
        '33C = (33D, 33D)\n'
        '33D = (33E, 33E)\n'
        '33E = (33Z, 33Z)\n'
        '33Z = (33F, 33F)\n'
        '33F = (33C, 33C)\n'
        'XXX = (XXX, XXX)'
    )

def test_node():
    node = Node(node_id='AAA', left='BBB', right='CCC')
    assert node.node_id == 'AAA'
    assert (node.left, node.right) == ('BBB', 'CCC')

def test_node_from_string():
    node = Node.from_string('AAA = (BBB, CCC)')

    assert node == Node('AAA', 'BBB', 'CCC')

def test_network(example_text_1):
    network = Network.from_string(example_text_1)

    assert network.instructions == 'RL'
    assert set(network.nodes.keys()) == {
        'AAA', 'BBB', 'CCC', 'DDD', 'EEE', 'GGG', 'ZZZ'
    }

def test_network_travel_1(example_text_1):

    network = Network.from_string(example_text_1)

    steps = network.travel(start_node_id='AAA', end_node_id='ZZZ')

    assert steps == 2

def test_network_travel_unreachable(example_text_1):

    network = Network.from_string(example_text_1)

    with pytest.raises(ValueError):
        network.travel(start_node_id='ZZZ', end_node_id='AAA')

def test_network_travel_2(example_text_2):

    network = Network.from_string(example_text_2)

    steps = network.travel(start_node_id='AAA', end_node_id='ZZZ')

    assert steps == 6

def test_network_ghost_travel(example_text_3):

    network = Network.from_string(example_text_3)

    steps = network.ghost_travel(start_nodes_tail='A', end_nodes_tail='Z')

    assert steps == 6

def test_network_ghost_travel_with_LCM(example_text_3): # pylint: disable=invalid-name

    network = Network.from_string(example_text_3)

    steps = network.ghost_travel_with_LCM(
        start_nodes_tail='A', end_nodes_tail='Z'
    )

    assert steps == 6

def test_network_get_loop(example_text_4):

    network = Network.from_string(example_text_4)
    loops = (
        network.get_loop('11A'),
        network.get_loop('22A'),
        network.get_loop('33A')
    )

    assert loops[0].start_index == 1
    assert loops[0].loop_length == 2
    assert loops[0].end_nodes_indexes == [2]

    assert loops[1].start_index == 1
    assert loops[1].loop_length == 6
    assert loops[1].end_nodes_indexes == [3, 6]

    assert loops[2].start_index == 2
    assert loops[2].loop_length == 10
    assert loops[2].end_nodes_indexes == [5, 10]

def test_get_loop_end_nodes_coefficient():

    loops = [
        Loop(1, 2, [2]), Loop(1, 6, [3, 6]), Loop(2, 10, [5, 10]),
        Loop(2, 10, [1, 5, 10])
    ]

    coefficients = [
        get_loop_end_nodes_coefficient(loop) for loop in loops
    ]

    assert coefficients == [2, 3, 5, None]
