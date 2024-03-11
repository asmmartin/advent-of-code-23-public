# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring

import pytest

from advent_of_code_23.day06 import (
    parse_sheet, find_winners, parse_sheet_singular
)

@pytest.fixture(name='example_sheet_text')
def example_sheet_text_fixture():
    return (
        "Time:      7  15   30\n"
        "Distance:  9  40  200\n"
    )

def test_parse_sheet(example_sheet_text):
    sheet = parse_sheet(example_sheet_text)

    assert sheet == ((7, 9), (15, 40), (30, 200))

def test_parse_sheet_singular(example_sheet_text):
    sheet = parse_sheet_singular(example_sheet_text)

    assert sheet == (71530, 940200)

def test_find_winners(example_sheet_text):

    sheet = parse_sheet(example_sheet_text)
    winners = [find_winners(time, distance) for time, distance in sheet]

    assert [len(winner) for winner in winners] == [4, 8, 9]

def test_find_winners_big():

    winners = find_winners(71530, 940200)

    assert len(winners) == 71503
