# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring

import pytest

from advent_of_code_23.day16 import Direction, next_directions, Contraption

@pytest.fixture(name='example_contraption_text')
def example_contraption_text_fixture():
    return (
        '.|...\\....\n'
        '|.-.\\.....\n'
        '.....|-...\n'
        '........|.\n'
        '..........\n'
        '.........\\\n'
        '..../.\\\\..\n'
        '.-.-/..|..\n'
        '.|....-|.\\\n'
        '..//.|....'
    )

def test_next_directions():

    assert next_directions(Direction.UP, '.') == (Direction.UP,)
    assert next_directions(Direction.DOWN, '.') == (Direction.DOWN,)
    assert next_directions(Direction.LEFT, '.') == (Direction.LEFT,)
    assert next_directions(Direction.RIGHT, '.') == (Direction.RIGHT,)

    assert next_directions(Direction.UP, '/') == (Direction.RIGHT,)
    assert next_directions(Direction.DOWN, '/') == (Direction.LEFT,)
    assert next_directions(Direction.LEFT, '/') == (Direction.DOWN,)
    assert next_directions(Direction.RIGHT, '/') == (Direction.UP,)

    assert next_directions(Direction.UP, '\\') == (Direction.LEFT,)
    assert next_directions(Direction.DOWN, '\\') == (Direction.RIGHT,)
    assert next_directions(Direction.LEFT, '\\') == (Direction.UP,)
    assert next_directions(Direction.RIGHT, '\\') == (Direction.DOWN,)

    assert next_directions(Direction.UP, '-') == (Direction.RIGHT, Direction.LEFT)
    assert next_directions(Direction.DOWN, '-') == (Direction.RIGHT, Direction.LEFT)
    assert next_directions(Direction.LEFT, '-') == (Direction.LEFT,)
    assert next_directions(Direction.RIGHT, '-') == (Direction.RIGHT,)

    assert next_directions(Direction.UP, '|') == (Direction.UP,)
    assert next_directions(Direction.DOWN, '|') == (Direction.DOWN,)
    assert next_directions(Direction.LEFT, '|') == (Direction.UP, Direction.DOWN)
    assert next_directions(Direction.RIGHT, '|') == (Direction.UP, Direction.DOWN)

def test_contraption(example_contraption_text):

    contraption = Contraption.from_string(example_contraption_text)

    assert len(contraption.mirrors) == 23
    assert contraption.width == 10
    assert contraption.height == 10
    assert contraption.energized_tiles == set()

def test_contraption_put_light(example_contraption_text):

    contraption = Contraption.from_string(example_contraption_text)

    contraption.put_light_beam(0, Direction.RIGHT)

    assert len(contraption.energized_tiles) == 46

def test_contraption_get_best_beam(example_contraption_text):

    contraption = Contraption.from_string(example_contraption_text)

    best_start, direction, most_energized_tiles = contraption.get_best_beam()

    assert best_start == 3
    assert direction == Direction.DOWN
    assert most_energized_tiles == 51
