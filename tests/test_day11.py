# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring

import pytest

from advent_of_code_23.day11 import Image, distance_between_galaxies

@pytest.fixture(name='image_text_example')
def image_text_example_fixture():
    return (
        '...#......\n'
        '.......#..\n'
        '#.........\n'
        '..........\n'
        '......#...\n'
        '.#........\n'
        '.........#\n'
        '..........\n'
        '.......#..\n'
        '#...#.....'
    )

@pytest.fixture(name='expanded_image_text_example')
def expanded_image_text_example_fixture():
    return (
        '....#........\n'
        '.........#...\n'
        '#............\n'
        '.............\n'
        '.............\n'
        '........#....\n'
        '.#...........\n'
        '............#\n'
        '.............\n'
        '.............\n'
        '.........#...\n'
        '#....#.......\n'
    )

def test_image(image_text_example):
    image = Image.from_string(image_text_example)

    assert image.galaxies == {3, 7+1j, 2j, 6+4j, 1+5j, 9+6j, 7+8j, 9j, 4+9j}

def test_image_expand_space(image_text_example, expanded_image_text_example):

    image = Image.from_string(image_text_example)

    expanded_image = image.expand_space()

    assert expanded_image == Image.from_string(expanded_image_text_example)

def test_distance_between_galaxies():

    galaxies_pairs = [
        (4, 9+10j), (2j, 12+7j), (11j, 5+11j)
    ]

    distances = [distance_between_galaxies(*pair) for pair in galaxies_pairs]

    assert distances == [15, 17, 5]

def test_image_calculate_galaxy_paths_lengths(expanded_image_text_example):
    image = Image.from_string(expanded_image_text_example)

    distances = image.calculate_galaxy_paths_lengths()

    assert sum(distances) == 374

def test_image_expansion_with_rate(image_text_example):
    image = Image.from_string(image_text_example)

    super_expanded = image.expand_space(rate=10)
    hyper_expanded = image.expand_space(rate=100)

    assert sum(super_expanded.calculate_galaxy_paths_lengths()) == 1030
    assert sum(hyper_expanded.calculate_galaxy_paths_lengths()) == 8410
