'''https://adventofcode.com/2023/day/14'''

# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring

import sys
from dataclasses import dataclass
from typing import Self

ROUND_ROCK = 'O'
CUBE_ROCK = '#'

@dataclass
class Platform:
    cube_rocks: set[complex]
    round_rocks: set[complex]
    height: int
    width: int

    @classmethod
    def from_string(cls, text: str) -> Self:
        lines = text.strip().splitlines()
        height = len(lines)
        width = len(lines[0])

        cube_rocks, round_rocks = set(), set()
        for row, line in enumerate(lines):
            for col, tile in enumerate(line):
                if tile == CUBE_ROCK:
                    cube_rocks.add(col + row * 1j)
                if tile == ROUND_ROCK:
                    round_rocks.add(col + row * 1j)

        return cls(
            cube_rocks=cube_rocks,
            round_rocks=round_rocks,
            height=height,
            width=width
        )

    def tilt_north(self) -> None:
        new_round_rocks = set()
        for col in range(self.width):
            base = -1
            for row in range(self.height):
                if col + row*1j in self.cube_rocks:
                    base = row
                elif col + row*1j in self.round_rocks:
                    base += 1
                    new_round_rocks.add(col + base*1j)
        self.round_rocks = new_round_rocks

    def tilt_south(self) -> None:
        new_round_rocks = set()
        for col in range(self.width):
            base = self.height
            for row in range(self.height - 1, -1, -1):
                if col + row*1j in self.cube_rocks:
                    base = row
                elif col + row*1j in self.round_rocks:
                    base -= 1
                    new_round_rocks.add(col + base*1j)
        self.round_rocks = new_round_rocks

    def tilt_west(self) -> None:
        new_round_rocks = set()
        for row in range(self.height):
            base = -1
            for col in range(self.width):
                if col + row*1j in self.cube_rocks:
                    base = col
                elif col + row*1j in self.round_rocks:
                    base += 1
                    new_round_rocks.add(base + row*1j)
        self.round_rocks = new_round_rocks

    def tilt_east(self) -> None:
        new_round_rocks = set()
        for row in range(self.height):
            base = self.width
            for col in range(self.width - 1, -1, -1):
                if col + row*1j in self.cube_rocks:
                    base = col
                elif col + row*1j in self.round_rocks:
                    base -= 1
                    new_round_rocks.add(base + row*1j)
        self.round_rocks = new_round_rocks

    def tilt_cycle(self) -> None:
        self.tilt_north()
        self.tilt_west()
        self.tilt_south()
        self.tilt_east()

    def tilt_multiple_cycles(self, cycles: int) -> None:
        cache = {self._calculate_cache_key(): 0}

        for iteration in range(1, cycles+1):
            self.tilt_cycle()
            current_key = self._calculate_cache_key()

            if current_key in cache:
                loop_start = cache[current_key]
                loop_length = iteration - loop_start
                offset = (cycles - loop_start) % loop_length

                for rocks, cached_iteration in cache.items():
                    if cached_iteration == loop_start + offset:
                        self.round_rocks = set(rocks)
                        return
                raise ValueError(
                    f'Cache error: Iteration {loop_start + offset} not found.'
                )

            cache[current_key] = iteration

    def _calculate_cache_key(self) -> tuple[complex, ...]:
        return tuple(sorted(
            self.round_rocks,
            key=lambda rock: (rock.imag, rock.real)
        ))

    @property
    def north_load(self) -> int:
        return sum(
            int(self.height - rock.imag)
            for rock in self.round_rocks
        )

def main(input_text: str):
    platform = Platform.from_string(input_text)
    platform.tilt_north()
    print(f'Solution part 1: {platform.north_load}')

    second_platform = Platform.from_string(input_text)
    second_platform.tilt_multiple_cycles(1_000_000_000)
    print(f'Solution part 2: {second_platform.north_load}')

if __name__ == "__main__":
    INPUT_TEXT = sys.stdin.read()
    main(INPUT_TEXT)
