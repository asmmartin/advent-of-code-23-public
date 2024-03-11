# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring

import pytest

from advent_of_code_23.day14 import Platform

@pytest.fixture(name='starting_platform_text')
def starting_platform_text_fixture():
    return (
        'O....#....\n'
        'O.OO#....#\n'
        '.....##...\n'
        'OO.#O....O\n'
        '.O.....O#.\n'
        'O.#..O.#.#\n'
        '..O..#O..O\n'
        '.......O..\n'
        '#....###..\n'
        '#OO..#....'
    )

@pytest.fixture(name='tilted_north_platform_text')
def tilted_north_platform_text_fixture():
    return (
        'OOOO.#.O..\n'
        'OO..#....#\n'
        'OO..O##..O\n'
        'O..#.OO...\n'
        '........#.\n'
        '..#....#.#\n'
        '..O..#.O.O\n'
        '..O.......\n'
        '#....###..\n'
        '#....#....'
    )

@pytest.fixture(name='platform_texts_after_cycles')
def platform_texts_after_cycles_fixture():
    return (
        '.....#....\n'
        '....#...O#\n'
        '...OO##...\n'
        '.OO#......\n'
        '.....OOO#.\n'
        '.O#...O#.#\n'
        '....O#....\n'
        '......OOOO\n'
        '#...O###..\n'
        '#..OO#....\n'
        '\n'
        '.....#....\n'
        '....#...O#\n'
        '.....##...\n'
        '..O#......\n'
        '.....OOO#.\n'
        '.O#...O#.#\n'
        '....O#...O\n'
        '.......OOO\n'
        '#..OO###..\n'
        '#.OOO#...O\n'
        '\n'
        '.....#....\n'
        '....#...O#\n'
        '.....##...\n'
        '..O#......\n'
        '.....OOO#.\n'
        '.O#...O#.#\n'
        '....O#...O\n'
        '.......OOO\n'
        '#...O###.O\n'
        '#.OOO#...O'
    ).split('\n\n')

def test_platform():
    text = (
        '..#..\n'
        'O..OO\n'
        '..OO.\n'
    )
    platform = Platform.from_string(text)

    assert platform.cube_rocks == {2}
    assert platform.round_rocks == {1j, 3+1j, 4+1j, 2+2j, 3+2j}
    assert platform.height == 3
    assert platform.width == 5

def test_platform_tilt_north():

    text = (
        '..#..\n'
        'O..OO\n'
        '..OO.\n'
    )
    platform = Platform.from_string(text)

    platform.tilt_north()

    assert platform.cube_rocks == {2}
    assert platform.round_rocks == {0, 3, 4, 2+1j, 3+1j}

def test_platform_tilt_north_example(
    starting_platform_text, tilted_north_platform_text
):
    platform = Platform.from_string(starting_platform_text)

    platform.tilt_north()

    assert platform == Platform.from_string(tilted_north_platform_text)

def test_platform_north_load(tilted_north_platform_text):

    platform = Platform.from_string(tilted_north_platform_text)

    assert platform.north_load == 136

def test_platform_cycles(
    starting_platform_text, platform_texts_after_cycles
):

    platform = Platform.from_string(starting_platform_text)

    platform.tilt_cycle()
    assert platform == Platform.from_string(platform_texts_after_cycles[0])
    platform.tilt_cycle()
    assert platform == Platform.from_string(platform_texts_after_cycles[1])
    platform.tilt_cycle()
    assert platform == Platform.from_string(platform_texts_after_cycles[2])

def test_platform_multiples_cycles(starting_platform_text):

    platform = Platform.from_string(starting_platform_text)

    platform.tilt_multiple_cycles(1_000_000_000)

    assert platform.north_load == 64
