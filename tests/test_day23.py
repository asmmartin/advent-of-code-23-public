# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring

import pytest

from advent_of_code_23.day23 import HikingMap

@pytest.fixture(name='example_hiking_map_text')
def example_hiking_map_text_fixture():
    return (
        '#.#####################\n'
        '#.......#########...###\n'
        '#######.#########.#.###\n'
        '###.....#.>.>.###.#.###\n'
        '###v#####.#v#.###.#.###\n'
        '###.>...#.#.#.....#...#\n'
        '###v###.#.#.#########.#\n'
        '###...#.#.#.......#...#\n'
        '#####.#.#.#######.#.###\n'
        '#.....#.#.#.......#...#\n'
        '#.#####.#.#.#########v#\n'
        '#.#...#...#...###...>.#\n'
        '#.#.#v#######v###.###v#\n'
        '#...#.>.#...>.>.#.###.#\n'
        '#####v#.#.###v#.#.###.#\n'
        '#.....#...#...#.#.#...#\n'
        '#.#########.###.#.#.###\n'
        '#...###...#...#...#.###\n'
        '###.###.#.###v#####v###\n'
        '#...#...#.#.>.>.#.>.###\n'
        '#.###.###.#.###.#.#v###\n'
        '#.....###...###...#...#\n'
        '#####################.#'
    )

def test_hiking_map(example_hiking_map_text):

    hiking_map = HikingMap.from_string(example_hiking_map_text)

    assert len(hiking_map.nodes) == 9
    assert hiking_map.nodes[1] == hiking_map.start
    assert hiking_map.nodes[21+22j] == hiking_map.end

def test_hiking_map_find_longest_path(example_hiking_map_text):

    hiking_map = HikingMap.from_string(example_hiking_map_text)

    _, distance = hiking_map.find_longest_path()

    assert distance == 94

def test_hiking_map_non_slippery_find_longest_path(example_hiking_map_text):


    hiking_map = HikingMap.from_string(example_hiking_map_text, slippery=False)

    _, distance = hiking_map.find_longest_path()

    assert distance == 154
