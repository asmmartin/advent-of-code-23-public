# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring

import pytest

from advent_of_code_23.day18 import (
    parse_instruction, Direction, Trench, parse_rgb_instruction
)

@pytest.fixture(name='example_instructions_text')
def example_instructions_text_fixture():
    return (
        'R 6 (#70c710)\n'
        'D 5 (#0dc571)\n'
        'L 2 (#5713f0)\n'
        'D 2 (#d2c081)\n'
        'R 2 (#59c680)\n'
        'D 2 (#411b91)\n'
        'L 5 (#8ceee2)\n'
        'U 2 (#caa173)\n'
        'L 1 (#1b58a2)\n'
        'U 2 (#caa171)\n'
        'R 2 (#7807d2)\n'
        'U 3 (#a77fa3)\n'
        'L 2 (#015232)\n'
        'U 2 (#7a21e3)'
    )

@pytest.fixture(name='example_instructions')
def example_instructions_fixture(example_instructions_text):
    return tuple(
        parse_instruction(instruction)
        for instruction in example_instructions_text.splitlines()
    )

def test_parse_instruction(example_instructions_text):

    instructions = [
        parse_instruction(instruction)
        for instruction in example_instructions_text.splitlines()
    ]

    assert instructions[0:5] == [
        (Direction.RIGHT, 6), (Direction.DOWN, 5), (Direction.LEFT, 2),
        (Direction.DOWN, 2), (Direction.RIGHT, 2)
    ]
    assert instructions[7] == (Direction.UP, 2)

def test_trench(example_instructions):

    trench = Trench.from_instructions(example_instructions)

    assert trench.vertices == (
        0, 6, 6+5j, 4+5j, 4+7j, 6+7j, 6+9j, 1+9j, 1+7j, 7j, 5j, 2+5j, 2+2j, 2j
    )

def test_trench_edge_cubes_count(example_instructions):

    trench = Trench.from_instructions(example_instructions)

    assert trench.edge_cubes_count == 38

def test_trench_interior_cubes_count(example_instructions):

    trench = Trench.from_instructions(example_instructions)

    assert trench.interior_cubes_count == 24

def test_trench_total_volume(example_instructions):

    trench = Trench.from_instructions(example_instructions)

    assert trench.total_volume == 62

def test_parse_rgb_instruction(example_instructions_text):

    instructions = [
        parse_rgb_instruction(instruction)
        for instruction in example_instructions_text.splitlines()
    ]

    assert instructions[0] == (Direction.RIGHT, 461937)
    assert instructions[1] == (Direction.DOWN, 56407)
    assert instructions[6] == (Direction.LEFT, 577262)
    assert instructions[7] == (Direction.UP, 829975)

def test_rgb_trench_total_volume(example_instructions_text):

    instructions = [
        parse_rgb_instruction(instruction)
        for instruction in example_instructions_text.splitlines()
    ]
    trench = Trench.from_instructions(instructions)

    assert trench.total_volume == 952408144115
