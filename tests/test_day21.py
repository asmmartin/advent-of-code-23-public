# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring

import pytest

from advent_of_code_23.day21 import Garden, InfiniteGarden

@pytest.fixture(name='example_garden_text')
def example_garden_text_fixture():
    return (
        '...........\n'
        '.....###.#.\n'
        '.###.##..#.\n'
        '..#.#...#..\n'
        '....#.#....\n'
        '.##..S####.\n'
        '.##..#...#.\n'
        '.......##..\n'
        '.##.#.####.\n'
        '.##..##.##.\n'
        '...........\n'
    )

@pytest.fixture(name='alternative_garden_text')
def alternative_garden_text_fixture():
    return (
		'...........\n'
		'......##.#.\n'
		'.###..#..#.\n'
		'..#.#...#..\n'
		'....#.#....\n'
		'.....S.....\n'
		'.##......#.\n'
		'.......##..\n'
		'.##.#.####.\n'
		'.##...#.##.\n'
		'...........'
    )

def test_garden(example_garden_text):

    garden = Garden.from_string(example_garden_text)

    assert garden.width == 11
    assert garden.heigth == 11
    assert garden.start == 5+5j
    assert len(garden.rocks) == 40

def test_garden_find_final_reachable_plots(example_garden_text):

    garden = Garden.from_string(example_garden_text)

    plots_three = garden.find_final_reachable_plots(steps=3)
    assert plots_three == {6+3j, 3+4j, 5+4j, 4+5j, 3+6j, 4+7j}

    plots_six = garden.find_final_reachable_plots(steps=6)
    assert len(plots_six) == 16

def test_infinite_garden_find_final_reachable_plots_small(example_garden_text):

    garden = InfiniteGarden.from_string(example_garden_text)

    plots = garden.find_final_reachable_plots(steps=6)
    assert len(plots) == 16
    plots = garden.find_final_reachable_plots(steps=10)
    assert len(plots) == 50
    plots = garden.find_final_reachable_plots(steps=50)
    assert len(plots) == 1594
    plots = garden.find_final_reachable_plots(steps=100)
    assert len(plots) == 6536

def test_infinite_garden_find_final_reachable_plots_big(example_garden_text):

    pytest.skip('This works, but it is too slow')

    garden = InfiniteGarden.from_string(example_garden_text)

    plots = garden.find_final_reachable_plots(steps=500)
    assert len(plots) == 167004
    plots = garden.find_final_reachable_plots(steps=1000)
    assert len(plots) == 668697
    plots = garden.find_final_reachable_plots(steps=5000)
    assert len(plots) == 16733044

def test_infinite_garden_find_final_reachable_plots_count_particular(
    alternative_garden_text
):

    garden = InfiniteGarden.from_string(alternative_garden_text)

    plot_count = garden.find_final_reachable_plots_count_particular(93)
    assert plot_count == len(garden.find_final_reachable_plots(93))

    plot_count = garden.find_final_reachable_plots_count_particular(101)
    assert plot_count == len(garden.find_final_reachable_plots(101))


def test_infinite_garden_find_final_reachable_plots_count_particular_simple():

    garden = InfiniteGarden([], 5, 5, 2+2j)

    plot_count = garden.find_final_reachable_plots_count_particular(11)
    assert plot_count == len(garden.find_final_reachable_plots(11))
    plot_count = garden.find_final_reachable_plots_count_particular(8)
    assert plot_count == len(garden.find_final_reachable_plots(8))
    plot_count = garden.find_final_reachable_plots_count_particular(12)
    assert plot_count == len(garden.find_final_reachable_plots(12))
    plot_count = garden.find_final_reachable_plots_count_particular(17)
    assert plot_count == len(garden.find_final_reachable_plots(17))
