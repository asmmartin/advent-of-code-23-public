# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring

import pytest

from advent_of_code_23.day09 import History

@pytest.fixture(name='example_text')
def example_text_fixture():
    return (
        '0 3 6 9 12 15\n'
        '1 3 6 10 15 21\n'
        '10 13 16 21 30 45\n'
    )

def test_history(example_text):

    histories = [
        History.from_string(line) for line in example_text.splitlines()
    ]

    assert [history.values for history in histories] == [
        [0, 3, 6, 9, 12, 15],
        [1, 3, 6, 10, 15, 21],
        [10, 13, 16, 21, 30, 45],
    ]

def test_history_calculate_next_value(example_text):

    histories = [
        History.from_string(line) for line in example_text.splitlines()
    ]

    next_values = [history.calculate_next_value() for history in histories]

    assert next_values == [18, 28, 68]

def test_history_calculate_previous_value(example_text):

    histories = [
        History.from_string(line) for line in example_text.splitlines()
    ]

    next_values = [history.calculate_previous_value() for history in histories]

    assert next_values == [-3, 0, 5]
