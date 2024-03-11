# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring

import pytest

from advent_of_code_23.day03 import (
    find_schematic_numbers, find_schematic_part_numbers, is_part_number,
    find_gears
)

@pytest.fixture(name='example_schematic_text')
def example_schematic_text_fixture():
    return (
        "467..114..\n"
        "...*......\n"
        "..35..633.\n"
        "......#...\n"
        "617*......\n"
        ".....+.58.\n"
        "..592.....\n"
        "......755.\n"
        "...$.*....\n"
        ".664.598.."
    )

@pytest.fixture(name='example_schematic_numbers_and_coords')
def example_schematic_numbers_and_coords_fixture():
    return (
        (467, 0, 0),
        (114, 0, 5),
        (35, 2, 2),
        (633, 2, 6),
        (617, 4, 0),
        (58, 5, 7),
        (592, 6, 2),
        (755, 7, 6),
        (664, 9, 1),
        (598, 9, 5)
    )

def test_find_schematic_numbers(example_schematic_text):

    numbers_and_coords = find_schematic_numbers(example_schematic_text)

    numbers = tuple(zip(*numbers_and_coords))[0]
    assert numbers == (
        467, 114, 35, 633, 617, 58, 592, 755, 664, 598
    )

def test_is_part_number(
    example_schematic_text, example_schematic_numbers_and_coords
):

    for number_and_coords in example_schematic_numbers_and_coords:
        if number_and_coords[0] in (114, 58):
            assert not is_part_number(example_schematic_text, *number_and_coords)
        else:
            assert is_part_number(example_schematic_text, *number_and_coords)


def test_find_schematic_part_numbers(example_schematic_text):

    part_numbers = find_schematic_part_numbers(example_schematic_text)

    assert part_numbers == (
        467, 35, 633, 617, 592, 755, 664, 598
    )
    assert sum(part_numbers) == 4361

def test_find_gears(example_schematic_text):

    gears = find_gears(example_schematic_text)

    assert gears == (
        ((1, 3), 467, 35),
        ((8, 5), 755, 598)
    )

    assert sum(gear[1] * gear[2] for gear in gears)
