'''https://adventofcode.com/2023/day/10'''

# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring

import sys
from collections import deque
from enum import Enum
from typing import Self

class Direction(Enum):
    UP = -1j
    DOWN = 1j
    LEFT = -1
    RIGHT = 1

    @property
    def complementary(self) -> Self:
        match self.name:
            case 'UP':
                return self.__class__.DOWN
            case 'DOWN':
                return self.__class__.UP
            case 'LEFT':
                return self.__class__.RIGHT
            case 'RIGHT':
                return self.__class__.LEFT
            case _:
                raise ValueError('Unknown direction')

def get_pipe_connections(pipe: str) -> set[Direction]:

    match pipe:
        case '|':
            return {Direction.UP, Direction.DOWN}
        case '-':
            return {Direction.LEFT, Direction.RIGHT}
        case 'L':
            return {Direction.UP, Direction.RIGHT}
        case 'J':
            return {Direction.UP, Direction.LEFT}
        case '7':
            return {Direction.LEFT, Direction.DOWN}
        case 'F':
            return {Direction.RIGHT, Direction.DOWN}
        case '.':
            return set()
        case 'S':
            return {
                Direction.UP, Direction.DOWN, Direction.RIGHT, Direction.LEFT
            }
        case _:
            raise ValueError(f'Unknown pipe: {pipe}')

def get_pipe_by_connections(directions: set[Direction]) -> str:

    if directions == {Direction.UP, Direction.DOWN}:
        return '|'
    if directions == {Direction.LEFT, Direction.RIGHT}:
        return '-'
    if directions == {Direction.UP, Direction.RIGHT}:
        return 'L'
    if directions == {Direction.UP, Direction.LEFT}:
        return 'J'
    if directions == {Direction.LEFT, Direction.DOWN}:
        return '7'
    if directions == {Direction.RIGHT, Direction.DOWN}:
        return 'F'
    if directions == set():
        return '.'

    raise ValueError(f'Unknown pipe: {directions=}')

class Board:
    def __init__(
        self, tiles: list[list[str]], start: complex | None = None
    ) -> None:
        self.tiles = tiles
        self.height = len(tiles)
        self.width = len(tiles[0])
        self.start = start if start is not None else self.get_start()

    @classmethod
    def from_string(cls, text: str) -> Self:
        tiles = [list(line) for line in text.strip().splitlines()]
        return cls(tiles=tiles)

    def get_at(self, position: complex) -> str:
        if not 0 <= position.real < self.width:
            return '.'
        if not 0 <= position.imag < self.height:
            return '.'

        return self.tiles[int(position.imag)][int(position.real)]

    def get_start(self) -> complex:
        for r, line in enumerate(self.tiles):
            for c, tile in enumerate(line):
                if tile == 'S':
                    return c + r*1j

        raise ValueError('This board has no start!')

    def traverse_loop(self) -> dict[complex, int]:

        # BFS (with a dict, to store the steps)
        visited: dict[complex, int] = {}
        to_visit = deque()
        to_visit.append((self.start, 0))

        while to_visit:
            current_coords, current_steps = to_visit.popleft()
            visited[current_coords] = current_steps

            for direction in get_pipe_connections(self.get_at(current_coords)):
                coords = current_coords + direction.value
                if coords in visited:
                    continue
                neighbour_connections = get_pipe_connections(self.get_at(coords))
                if direction.complementary in neighbour_connections:
                    to_visit.append((coords, current_steps + 1))

        return visited

    def get_farthest_point(self) -> tuple[complex, int]:

        loop = self.traverse_loop()
        end = max(loop.items(), key=lambda x: x[1])
        return end

    def generate_clean_version(self) -> Self:

        loop = self.traverse_loop()

        clean_tiles = []
        for row in range(self.height):
            line = []
            for column in range(self.width):
                if column + row * 1j in loop:
                    line.append(self.tiles[row][column])
                else:
                    line.append('.')
            clean_tiles.append(line)

        return Board(tiles=clean_tiles, start=self.start)

def find_enclosed_tiles(board: Board) -> set[complex]:
    clean_board = board.generate_clean_version()

    # Determine start's type of pipe
    start_directions = set()
    for direction in Direction:
        neighbour = clean_board.get_at(clean_board.start + direction.value)
        if direction.complementary in get_pipe_connections(neighbour):
            start_directions.add(direction)
    start_coords = int(clean_board.start.imag), int(clean_board.start.real)
    clean_board.tiles[start_coords[0]][start_coords[1]] = (
        get_pipe_by_connections(start_directions)
    )

    possible_enclosed_tiles = [set(), set()]

    # Horizontal scan
    for row in range(clean_board.height):
        inside = False
        squeezing = None
        for col in range(clean_board.width):
            match (squeezing, clean_board.tiles[row][col]):
                case _, '.':
                    if inside:
                        possible_enclosed_tiles[0].add(col + row * 1j)
                case _, '|':
                    inside = not inside
                case _, '-':
                    pass
                case ('L', 'J') | ('F', '7'):
                    squeezing = None
                case ('L', '7') | ('F', 'J'):
                    squeezing = None
                    inside = not inside
                case (None, tile) if tile in 'FL':
                    squeezing = tile
                case _, _:
                    raise ValueError('Unknown error: Loop not valid!')

    # Vertical scan
    for col in range(clean_board.width):
        inside = False
        squeezing = None
        for row in range(clean_board.height):
            match (squeezing, clean_board.tiles[row][col]):
                case _, '.':
                    if inside:
                        possible_enclosed_tiles[1].add(col + row * 1j)
                case _, '-':
                    inside = not inside
                case _, '|':
                    pass
                case ('F', 'L') | ('7', 'J'):
                    squeezing = None
                case ('F', 'J') | ('7', 'L'):
                    squeezing = None
                    inside = not inside
                case (None, tile) if tile in 'F7':
                    squeezing = tile
                case _, _:
                    raise ValueError('Unknown error: Loop not valid!')

    return possible_enclosed_tiles[0] & possible_enclosed_tiles[1]

def main(input_text: str):
    board = Board.from_string(input_text)
    farthest = board.get_farthest_point()
    print(f'Solution part 1: {farthest}')

    enclosed_tiles = find_enclosed_tiles(board)
    print(f'Solution part 2: {len(enclosed_tiles)}')

if __name__ == "__main__":
    INPUT_TEXT = sys.stdin.read()
    main(INPUT_TEXT)
