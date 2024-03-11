# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring

import pytest

from advent_of_code_23.day10 import (
    Direction, get_pipe_connections, Board, find_enclosed_tiles
)

@pytest.fixture(name='example_board_text_one')
def example_board_text_one_fixture():
    return (
        '.....\n'
        '.S-7.\n'
        '.|.|.\n'
        '.L-J.\n'
        '.....'
    )

@pytest.fixture(name='example_board_text_one_with_extras')
def example_board_text_one_with_extras_fixture():
    return (
        '-L|F7\n'
        '7S-7|\n'
        'L|7||\n'
        '-L-J|\n'
        'L|-JF'
    )

@pytest.fixture(name='example_board_text_two_with_extras')
def example_board_text_two_with_extras_fixture():
    return (
        '7-F7-\n'
        '.FJ|7\n'
        'SJLL7\n'
        '|F--J\n'
        'LJ.LJ'
    )

@pytest.fixture(name='example_board_text_three')
def example_board_text_three_fixture():
    return (
        '..........\n'
        '.S------7.\n'
        '.|F----7|.\n'
        '.||....||.\n'
        '.||....||.\n'
        '.|L-7F-J|.\n'
        '.|..||..|.\n'
        '.L--JL--J.\n'
        '..........'
    )

@pytest.fixture(name='example_board_text_four')
def example_board_text_four_fixture():
    return (
        '.F----7F7F7F7F-7....\n'
        '.|F--7||||||||FJ....\n'
        '.||.FJ||||||||L7....\n'
        'FJL7L7LJLJ||LJ.L-7..\n'
        'L--J.L7...LJS7F-7L7.\n'
        '....F-J..F7FJ|L7L7L7\n'
        '....L7.F7||L7|.L7L7|\n'
        '.....|FJLJ|FJ|F7|.LJ\n'
        '....FJL-7.||.||||...\n'
        '....L---J.LJ.LJLJ...'
    )


@pytest.fixture(name='example_board_text_five')
def example_board_text_five_fixture():
    return (
        'FF7FSF7F7F7F7F7F---7\n'
        'L|LJ||||||||||||F--J\n'
        'FL-7LJLJ||||||LJL-77\n'
        'F--JF--7||LJLJ7F7FJ-\n'
        'L---JF-JLJ.||-FJLJJ7\n'
        '|F|F-JF---7F7-L7L|7|\n'
        '|FFJF7L7F-JF7|JL---7\n'
        '7-L-JL7||F7|L7F-7F7|\n'
        'L.L7LFJ|||||FJL7||LJ\n'
        'L7JLJL-JLJLJL--JLJ.L'
    )

def test_directions():

    assert Direction.UP.complementary == Direction.DOWN
    assert Direction.DOWN.complementary == Direction.UP
    assert Direction.LEFT.complementary == Direction.RIGHT
    assert Direction.RIGHT.complementary == Direction.LEFT

def test_pipe_connections():

    assert get_pipe_connections('|') == {Direction.UP, Direction.DOWN}
    assert get_pipe_connections('-') == {Direction.LEFT, Direction.RIGHT}
    assert get_pipe_connections('L') == {Direction.UP, Direction.RIGHT}
    assert get_pipe_connections('J') == {Direction.UP, Direction.LEFT}
    assert get_pipe_connections('7') == {Direction.LEFT, Direction.DOWN}
    assert get_pipe_connections('F') == {Direction.RIGHT, Direction.DOWN}
    assert get_pipe_connections('.') == set()
    assert get_pipe_connections('S') == {
        Direction.UP, Direction.DOWN, Direction.RIGHT, Direction.LEFT
    }

def test_board(example_board_text_one):
    board = Board.from_string(example_board_text_one)

    assert (board.width, board.height) == (5, 5)

    assert board.get_at(1 + 1j) == 'S'
    assert board.get_at(3 + 3j) == 'J'
    assert board.get_at(1 + 3j) == 'L'
    assert board.get_at(3 + 1j) == '7'

    assert board.get_at(999 + 999j) == '.'
    assert board.get_at(-1 + -1j) == '.'

    assert board.get_start() == 1 + 1j

def test_board_get_farthest_point_simple(example_board_text_one_with_extras):
    board = Board.from_string(example_board_text_one_with_extras)

    farthest_point = board.get_farthest_point()

    assert farthest_point == (3 + 3j, 4)

def test_board_get_farthest_point_complex(example_board_text_two_with_extras):
    board = Board.from_string(example_board_text_two_with_extras)
    farthest_point = board.get_farthest_point()

    assert farthest_point == (4+2j, 8)

def test_board_generate_clean_version(
    example_board_text_one, example_board_text_one_with_extras
):
    board = Board.from_string(example_board_text_one_with_extras)

    cleaned = board.generate_clean_version()

    assert cleaned.tiles == Board.from_string(example_board_text_one).tiles

def test_find_enclosed_tiles_simple(example_board_text_three):
    board = Board.from_string(example_board_text_three)

    enclosed_tiles = find_enclosed_tiles(board)

    assert enclosed_tiles == {
        2+6j, 3+6j, 6+6j, 7+6j
    }

def test_find_enclosed_tiles_complex(
    example_board_text_four, example_board_text_five
):
    boards = [
        Board.from_string(example_board_text_four),
        Board.from_string(example_board_text_five)
    ]

    enclosed_tiles = [find_enclosed_tiles(board) for board in boards]

    assert len(enclosed_tiles[0]) == 8
    assert len(enclosed_tiles[1]) == 10
