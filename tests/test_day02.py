# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring

import pytest

from advent_of_code_23.day02 import Game

@pytest.fixture(name='example_games')
def example_games_fixture() -> tuple[Game, ...]:

    games_text = (
        'Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green',
        'Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue',
        'Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red',
        'Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red',
        'Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green',
    )

    return tuple(Game.from_string(text) for text in games_text)


def test_game():
    game = Game(id_number=1, sets=((4, 0, 3), (1, 2, 6), (0, 2, 0)))

    assert game.id_number == 1
    assert len(game.sets) == 3

def test_game_from_string():

    game = Game.from_string(
        'Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green'
    )

    assert game == Game(id_number=1, sets=((4, 0, 3), (1, 2, 6), (0, 2, 0)))

def test_game_check_possible_cubes(example_games):

    cubes_guess = (12, 13, 14)

    assert example_games[0].check_possible_cubes(cubes_guess)
    assert example_games[1].check_possible_cubes(cubes_guess)
    assert not example_games[2].check_possible_cubes(cubes_guess)
    assert not example_games[3].check_possible_cubes(cubes_guess)
    assert example_games[4].check_possible_cubes(cubes_guess)

def test_example_possible_games_ids_sum(example_games):

    cubes_guess = (12, 13, 14)

    total = sum(
        example_game.id_number
        for example_game in example_games
        if example_game.check_possible_cubes(cubes_guess)
    )

    assert total == 8

def test_example_games_power(example_games):
    powers = [example_game.power for example_game in example_games]

    assert powers == [48, 12, 1560, 630, 36]
    assert sum(powers) == 2286
