'''https://adventofcode.com/2023/day/2'''

# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring

import sys
import re

from dataclasses import dataclass
from typing import Self

@dataclass
class Game:
    id_number: int
    sets: tuple[tuple[int, int, int], ...]

    @classmethod
    def from_string(cls, text: str) -> Self:
        id_text, sets_text = text.split(':')

        id_number_match = re.search(r'Game (\d+)', id_text)
        if not id_number_match:
            raise ValueError('Game has no ID')
        id_number = int(id_number_match.group(1))

        sets = []
        for set_text in sets_text.split(';'):
            red_match = re.search(r'(\d+) red', set_text)
            green_match = re.search(r'(\d+) green', set_text)
            blue_match = re.search(r'(\d+) blue', set_text)

            red = int(red_match.group(1)) if red_match else 0
            green = int(green_match.group(1)) if green_match else 0
            blue = int(blue_match.group(1)) if blue_match else 0

            sets.append((red, green, blue))

        return cls(id_number=id_number, sets=tuple(sets))

    @property
    def max_colours(self) -> tuple[int, int, int]:

        return tuple(
            max(colours) for colours in zip(*self.sets)
        ) # type: ignore

    @property
    def power(self) -> int:
        red, green, blue = self.max_colours
        return red * green * blue

    def check_possible_cubes(self, cubes: tuple[int, int, int]) -> bool:

        return all(
            cube >= max_colour
            for max_colour, cube in zip(self.max_colours, cubes)
        )

def main(input_text: str):

    games = [Game.from_string(line) for line in input_text.splitlines()]
    cubes_guess = (12, 13, 14)
    total = sum(
        game.id_number for game in games
        if game.check_possible_cubes(cubes_guess)
    )
    print(f'Solution part 1: {total}')

    total_power = sum(game.power for game in games)
    print(f'Solution part 2: {total_power}')


if __name__ == "__main__":
    INPUT_TEXT = sys.stdin.read()
    main(INPUT_TEXT)
