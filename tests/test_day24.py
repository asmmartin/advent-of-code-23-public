# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring

import pytest

import numpy as np

from advent_of_code_23.day24 import (
    Hailstone, find_future_xy_crosses_in_area_count, get_smashing_stone
)

@pytest.fixture(name='example_hailstones_text')
def example_hailstones_text_fixture():
    return (
        '19, 13, 30 @ -2,  1, -2\n'
        '18, 19, 22 @ -1, -1, -2\n'
        '20, 25, 34 @ -2, -2, -4\n'
        '12, 31, 28 @ -1, -2, -1\n'
        '20, 19, 15 @  1, -5, -3'
    )

def test_hailstone(example_hailstones_text):
    lines = example_hailstones_text.strip().splitlines()

    hailstones = [Hailstone.from_string(line) for line in lines]

    assert hailstones[0].velocity == (-2, 1, -2)
    assert hailstones[2].position == (20, 25, 34)

def test_hailstone_find_xy_path_cross_point_with(example_hailstones_text):

    lines = example_hailstones_text.strip().splitlines()
    hailstones = [Hailstone.from_string(line) for line in lines]

    cross_point = hailstones[0].find_xy_path_cross_point_with(hailstones[1])
    assert cross_point
    assert np.all(np.isclose(cross_point, (14.333, 15.333), atol=1e-3))

    cross_point = hailstones[0].find_xy_path_cross_point_with(hailstones[2])
    assert cross_point
    assert np.all(np.isclose(cross_point, (11.667, 16.667), atol=1e-3))

    cross_point = hailstones[1].find_xy_path_cross_point_with(hailstones[2])
    assert not cross_point

def test_hailstone_is_future_point(example_hailstones_text):

    lines = example_hailstones_text.strip().splitlines()
    hailstones = [Hailstone.from_string(line) for line in lines]

    cross_point = hailstones[0].find_xy_path_cross_point_with(hailstones[1])
    assert cross_point
    assert hailstones[0].is_future_point((*cross_point, 0))
    assert hailstones[1].is_future_point((*cross_point, 0))

    cross_point = hailstones[0].find_xy_path_cross_point_with(hailstones[4])
    assert cross_point
    assert not hailstones[0].is_future_point((*cross_point, 0))
    assert hailstones[4].is_future_point((*cross_point, 0))

    cross_point = hailstones[2].find_xy_path_cross_point_with(hailstones[4])
    assert cross_point
    assert hailstones[2].is_future_point((*cross_point, 0))
    assert not hailstones[4].is_future_point((*cross_point, 0))

    cross_point = hailstones[1].find_xy_path_cross_point_with(hailstones[4])
    assert cross_point
    assert not hailstones[1].is_future_point((*cross_point, 0))
    assert not hailstones[4].is_future_point((*cross_point, 0))

def test_find_future_xy_crosses_in_area_count(example_hailstones_text):

    lines = example_hailstones_text.strip().splitlines()
    hailstones = [Hailstone.from_string(line) for line in lines]

    cross_count = find_future_xy_crosses_in_area_count(
        hailstones, boundaries=(7, 27)
    )

    assert cross_count == 2

def test_get_smashing_stone(example_hailstones_text):


    lines = example_hailstones_text.strip().splitlines()
    hailstones = [Hailstone.from_string(line) for line in lines]

    stone = get_smashing_stone(hailstones)

    assert stone.position == (24, 13, 10)
    assert stone.velocity == (-3, 1, 2)
