'''https://adventofcode.com/2023/day/16'''

# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring

import sys
from enum import Enum
from typing import Self

class Direction(complex, Enum):
    UP = -1j
    DOWN = 1j
    LEFT = -1
    RIGHT = 1

def next_directions(
    current: Direction, tile_type: str
) -> tuple[Direction] | tuple[Direction, Direction] :

    match (current, tile_type):
        case Direction.RIGHT, ('/'):
            return (Direction.UP,)
        case Direction.LEFT, ('/'):
            return (Direction.DOWN,)
        case Direction.UP, ('/'):
            return (Direction.RIGHT,)
        case Direction.DOWN, ('/'):
            return (Direction.LEFT,)

        case Direction.RIGHT, ('\\'):
            return (Direction.DOWN,)
        case Direction.LEFT, ('\\'):
            return (Direction.UP,)
        case Direction.UP, ('\\'):
            return (Direction.LEFT,)
        case Direction.DOWN, ('\\'):
            return (Direction.RIGHT,)

        case Direction.RIGHT | Direction.LEFT, ('|'):
            return (Direction.UP, Direction.DOWN)
        case Direction.UP | Direction.DOWN, ('-'):
            return (Direction.RIGHT, Direction.LEFT)

        case _:
            return (current,)

class Contraption:

    def __init__(
        self, mirrors: dict[complex, str], height: int, width: int
    ) -> None:

        self.mirrors = mirrors
        self.height = height
        self.width = width

        self.energized_tiles: set[complex] = set()

    @classmethod
    def from_string(cls, text: str) -> Self:

        lines = text.strip().splitlines()

        height = len(lines)
        width = len(lines[0])

        mirrors = {}

        for row, line in enumerate(lines):
            for col, tile in enumerate(line):
                if tile != '.':
                    mirrors[col + row * 1j] = tile

        return cls(mirrors=mirrors, width=width, height=height)

    def put_light_beam(
        self, coords: complex,
        direction: Direction,
        already_processed: set[tuple[complex, Direction]] | None = None
    ) -> None:

        if already_processed is None:
            already_processed = set()

        if (coords, direction) in already_processed:
            return

        already_processed.add((coords, direction))

        if not 0 <= coords.real < self.width:
            return
        if not 0 <= coords.imag < self.height:
            return

        self.energized_tiles.add(coords)

        tile_type = self.mirrors.get(coords, '.')

        for next_direction in next_directions(direction, tile_type):
            next_coords = coords + next_direction
            self.put_light_beam(next_coords, next_direction, already_processed)

    def get_best_beam(self) -> tuple[complex, Direction, int]:

        cached_energized = self.energized_tiles

        current_best_start_tile = 0
        current_best_start_direction = Direction.RIGHT
        current_max = 0

        for col in range(self.width):
            self.energized_tiles = set()
            tile = col
            self.put_light_beam(tile, Direction.DOWN)
            if len(self.energized_tiles) > current_max:
                current_best_start_tile = tile
                current_best_start_direction = Direction.DOWN
                current_max = len(self.energized_tiles)

        for col in range(self.width):
            self.energized_tiles = set()
            tile = col + (self.height - 1)*1j
            self.put_light_beam(tile, Direction.UP)
            if len(self.energized_tiles) > current_max:
                current_best_start_tile = tile
                current_best_start_direction = Direction.UP
                current_max = len(self.energized_tiles)

        for row in range(self.height):
            self.energized_tiles = set()
            tile = row * 1j
            self.put_light_beam(tile, Direction.RIGHT)
            if len(self.energized_tiles) > current_max:
                current_best_start_tile = tile
                current_best_start_direction = Direction.RIGHT
                current_max = len(self.energized_tiles)

        for row in range(self.height):
            self.energized_tiles = set()
            tile = (self.width - 1) + row * 1j
            self.put_light_beam(tile, Direction.LEFT)
            if len(self.energized_tiles) > current_max:
                current_best_start_tile = tile
                current_best_start_direction = Direction.LEFT
                current_max = len(self.energized_tiles)

        self.energized_tiles = cached_energized
        return (
            current_best_start_tile, current_best_start_direction, current_max
        )

    @property
    def energized_drawing(self) -> str:
        text = ''
        for row in range(self.height):
            for col in range(self.width):
                if col + row*1j in self.energized_tiles:
                    text += '#'
                else:
                    text += '.'
            text += '\n'
        return text

def main(input_text: str):
    contraption = Contraption.from_string(input_text)
    sys.setrecursionlimit((contraption.width + 2) * (contraption.height + 2))
    contraption.put_light_beam(0, Direction.RIGHT)
    print(f'Solution part 1: {len(contraption.energized_tiles)}')

    *_, best = contraption.get_best_beam()
    print(f'Solution part 2: {best}')

if __name__ == "__main__":
    INPUT_TEXT = sys.stdin.read()
    main(INPUT_TEXT)
