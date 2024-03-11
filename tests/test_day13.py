# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring

from advent_of_code_23.day13 import (
    Pattern, find_vertical_mirrors, find_horizontal_mirrors
)

def test_pattern():
    text = (
        '.#...#.\n'
        '..#.#..'
    )
    pattern = Pattern.from_string(text)

    assert pattern.rocks == {1, 5, 2+1j, 4+1j}
    assert pattern.rows == {
        0: (1, 5), 1: (2+1j, 4+1j)
    }
    assert pattern.columns == {
        1: (1,), 2: (2+1j,), 4: (4+1j,), 5: (5,)
    }
    assert pattern.width == 7
    assert pattern.height == 2

def test_find_vertical_mirrors_left():

    text = (
        '.#..#..\n'
        '..##..#'
    )
    pattern = Pattern.from_string(text)

    mirror = find_vertical_mirrors(pattern)

    assert mirror == 3

def test_find_vertical_mirrors_right():

    text = (
        '..#..#.\n'
        '#..##..'
    )
    pattern = Pattern.from_string(text)

    mirror = find_vertical_mirrors(pattern)

    assert mirror == 4

def test_find_vertical_mirrors_no_mirror():

    text = (
        '.#..##\n'
        '..##.#'
    )
    pattern = Pattern.from_string(text)

    mirror = find_vertical_mirrors(pattern)

    assert mirror is None

def test_find_vertical_mirrors_example():

    text = (
        '#.##..##.\n'
        '..#.##.#.\n'
        '##......#\n'
        '##......#\n'
        '..#.##.#.\n'
        '..##..##.\n'
        '#.#.##.#.'
    )
    pattern = Pattern.from_string(text)

    mirror = find_vertical_mirrors(pattern)

    assert mirror == 5

def test_find_horizontal_mirrors_example():

    text = (
        '#...##..#\n'
        '#....#..#\n'
        '..##..###\n'
        '#####.##.\n'
        '#####.##.\n'
        '..##..###\n'
        '#....#..#'
    )
    pattern = Pattern.from_string(text)

    mirror = find_horizontal_mirrors(pattern)

    assert mirror == 4

def test_pattern_score():

    patterns = [
        Pattern.from_string(
            '#.##..##.\n'
            '..#.##.#.\n'
            '##......#\n'
            '##......#\n'
            '..#.##.#.\n'
            '..##..##.\n'
            '#.#.##.#.'
        ),
        Pattern.from_string(
            '#...##..#\n'
            '#....#..#\n'
            '..##..###\n'
            '#####.##.\n'
            '#####.##.\n'
            '..##..###\n'
            '#....#..#'
        )
    ]

    scores = [pattern.calculate_score() for pattern in patterns]

    assert scores == [5, 400]

def test_find_horizontal_mirrors_with_smudges_example_one():

    text = (
        '#.##..##.\n'
        '..#.##.#.\n'
        '##......#\n'
        '##......#\n'
        '..#.##.#.\n'
        '..##..##.\n'
        '#.#.##.#.'
    )
    pattern = Pattern.from_string(text)

    mirror = find_horizontal_mirrors(pattern, 1)

    assert mirror == 3

def test_find_horizontal_mirrors_with_smudges_example_two():

    text = (
        '#...##..#\n'
        '#....#..#\n'
        '..##..###\n'
        '#####.##.\n'
        '#####.##.\n'
        '..##..###\n'
        '#....#..#'
    )
    pattern = Pattern.from_string(text)

    mirror = find_horizontal_mirrors(pattern, 1)

    assert mirror == 1

def test_pattern_score_with_smudges():

    patterns = [
        Pattern.from_string(
            '#.##..##.\n'
            '..#.##.#.\n'
            '##......#\n'
            '##......#\n'
            '..#.##.#.\n'
            '..##..##.\n'
            '#.#.##.#.'
        ),
        Pattern.from_string(
            '#...##..#\n'
            '#....#..#\n'
            '..##..###\n'
            '#####.##.\n'
            '#####.##.\n'
            '..##..###\n'
            '#....#..#'
        )
    ]

    scores = [pattern.calculate_score(1) for pattern in patterns]

    assert scores == [300, 100]
