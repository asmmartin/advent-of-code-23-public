# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring

import pytest

from advent_of_code_23.day17 import CityMap, Direction

@pytest.fixture(name='example_map_text')
def example_map_text_fixture():
    return (
        '2413432311323\n'
        '3215453535623\n'
        '3255245654254\n'
        '3446585845452\n'
        '4546657867536\n'
        '1438598798454\n'
        '4457876987766\n'
        '3637877979653\n'
        '4654967986887\n'
        '4564679986453\n'
        '1224686865563\n'
        '2546548887735\n'
        '4322674655533'
    )

def test_city_map(example_map_text):

    city_map = CityMap.from_string(example_map_text)

    assert city_map.height == 13
    assert city_map.width == 13
    assert city_map.blocks[7 + 6j] == 9

def test_directions():

    assert sum((
        Direction.UP, Direction.DOWN, Direction.LEFT, Direction.RIGHT
    )) == 0

def test_city_map_find_best_path_simple():

    city_map = CityMap.from_string(
        '241\n321'
    )

    heat_loss, path = city_map.find_best_path(0, 2)

    assert heat_loss == 5
    assert path == (Direction.RIGHT, Direction.RIGHT)

def test_city_map_find_best_path_simple_2():

    city_map = CityMap.from_string(
        '112999\n911111'
    )

    heat_loss, _ = city_map.find_best_path(0, 5+1j)

    assert heat_loss == 7

def test_city_map_find_best_path_simple_3():

    city_map = CityMap.from_string(
        '99999\n'
        '11111\n'
        '99119'
    )

    heat_loss, _ = city_map.find_best_path(1j, 4+1j)

    assert heat_loss == 6

def test_city_map_find_best_path_example(example_map_text):

    city_map = CityMap.from_string(example_map_text)

    heat_loss, path = city_map.find_best_path(0, 12+12j)

    assert heat_loss == 102
    assert sum(path) == 12 + 12j

def test_city_map_find_best_ultra_path_simple():

    text = (
        '111111111111\n'
        '999999999991\n'
        '999999999991\n'
        '999999999991\n'
        '999999999991'
    )
    city_map = CityMap.from_string(text)

    heat_loss, path = city_map.find_best_ultra_path(0, 11+4j)

    assert heat_loss == 71
    assert path == (
        (Direction.RIGHT,) * 7 + (Direction.DOWN,) * 4 + (Direction.RIGHT,) * 4
    )

def test_city_map_find_best_ultra_path_example(example_map_text):

    city_map = CityMap.from_string(example_map_text)

    heat_loss, path = city_map.find_best_ultra_path(0, 12+12j)

    assert heat_loss == 94
    assert path == (
        (Direction.RIGHT,) * 8 + (Direction.DOWN,) * 4 +
        (Direction.RIGHT,) * 4 + (Direction.DOWN,) * 8
    )
