'''https://adventofcode.com/2023/day/11'''

# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring

import itertools
import sys
from dataclasses import dataclass
from typing import Self

GALAXY = '#'
VOID = '.'

@dataclass
class Image:
    galaxies: set[complex]
    height: int
    width: int

    @classmethod
    def from_string(cls, text: str) -> Self:
        text_lines = text.strip().splitlines()
        height = len(text_lines)
        width = len(text_lines[0])

        galaxies = set()

        for row, line in enumerate(text_lines):
            for col, tile in enumerate(line):
                if tile == GALAXY:
                    galaxies.add(col + row*1j)

        return cls(galaxies=galaxies, height=height, width=width)

    def expand_space(self, rate: int = 2) -> Self:
        height = self.height
        width = self.width
        galaxies_movements = {galaxy: galaxy for galaxy in self.galaxies}

        # Rows expansion
        for row in range(self.height):
            if any(
                (col + 1j*row) in self.galaxies
                for col in range(self.height)
            ):
                continue
            height += (rate - 1)
            for galaxy in galaxies_movements:
                if galaxy.imag > row:
                    galaxies_movements[galaxy] += (rate - 1)*1j
        # Columns expansion
        for col in range(self.width):
            if any(
                (col + 1j*row) in self.galaxies
                for row in range(self.width)
            ):
                continue
            width += rate - 1
            for galaxy in galaxies_movements:
                if galaxy.real > col:
                    galaxies_movements[galaxy] += (rate - 1)

        return Image(
            galaxies=set(galaxies_movements.values()),
            height=height,
            width=width
        )

    def calculate_galaxy_paths_lengths(self) -> list[int]:
        galaxy_pairs = itertools.combinations(self.galaxies, 2)

        return [
            distance_between_galaxies(*galaxy_pair)
            for galaxy_pair in galaxy_pairs
        ]

def distance_between_galaxies(galaxy_a: complex, galaxy_b: complex) -> int:
    return int(
        abs(galaxy_a.imag - galaxy_b.imag) + abs(galaxy_a.real - galaxy_b.real)
    )

def main(input_text: str):
    image = Image.from_string(input_text)
    expanded_image = image.expand_space()
    sum_paths = sum(expanded_image.calculate_galaxy_paths_lengths())
    print(f'Solution part 1: {sum_paths}')

    super_expanded_image = image.expand_space(1_000_000)
    sum_super_paths = sum(super_expanded_image.calculate_galaxy_paths_lengths())
    print(f'Solution part 2: {sum_super_paths}')

if __name__ == "__main__":
    INPUT_TEXT = sys.stdin.read()
    main(INPUT_TEXT)
