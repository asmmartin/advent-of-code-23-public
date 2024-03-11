'''https://adventofcode.com/2023/day/17'''

# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring

import heapq
import sys
from enum import Enum
from typing import Self

class Direction(complex, Enum):
    UP = -1j
    DOWN = 1j
    RIGHT = 1
    LEFT = -1

class CityMap:

    def __init__(
        self, blocks: dict[complex, int], width: int, height: int
    ) -> None:
        self.blocks = blocks
        self.width = width
        self.height = height

    @classmethod
    def from_string(cls, text: str) -> Self:
        lines = text.strip().splitlines()

        height = len(lines)
        width = len(lines[0])

        blocks = {}
        for row, line in enumerate(lines):
            for col, block in enumerate(line):
                blocks[col + row*1j] = int(block)

        return cls(blocks=blocks, width=width, height=height)

    def find_best_path(
        self, start: complex, end: complex
    ) -> tuple[int, list[Direction]]:

        # Dijkstra's Algorithm
        done: dict[
            tuple[complex, tuple[Direction, ...]],
            tuple[int, list[Direction]]
        ] = {}
        min_heap = []
        insertion_order = 0 # To sort equal heat elements in heap

        heapq.heappush(min_heap, (0, insertion_order, start, tuple()))
        while min_heap:
            lost_heat, _, coords, previous_directions = heapq.heappop(min_heap)

            if (coords, previous_directions[-3:]) in done:
                continue

            done[coords, previous_directions[-3:]] = lost_heat, previous_directions

            if coords == end:
                break

            for direction in self.find_allowed_directions(
                coords, previous_directions
            ):
                neighbour_previous_directions = (*previous_directions, direction)
                neighbour = coords + direction
                if (neighbour, neighbour_previous_directions[-3:]) in done:
                    continue
                insertion_order += 1
                neighbour_heat = lost_heat + self.blocks[neighbour]
                heapq.heappush(
                    min_heap,
                    (
                        neighbour_heat,
                        insertion_order,
                        neighbour,
                        neighbour_previous_directions
                    )
                )

        for (block, _), (heat_loss, path) in done.items():
            if block == end:
                return heat_loss, path
        raise ValueError('Path not found!')

    def find_allowed_directions(
        self,
        coords: complex,
        previous_directions: tuple[Direction, ...]
    ) -> tuple[Direction, ...]:

        allowed = []
        for direction in Direction:
            if (
                len(previous_directions) >= 3 and
                previous_directions[-3:] == (direction, direction, direction)
            ):
                continue

            if (previous_directions and previous_directions[-1] == -direction):
                continue

            new_block = coords + direction
            if new_block in self.blocks:
                allowed.append(direction)
        return tuple(allowed)

    def find_best_ultra_path(
        self, start: complex, end: complex
    ) -> tuple[int, list[Direction]]:

        # Dijkstra's Algorithm
        done: dict[
            tuple[complex, tuple[Direction, ...]],
            tuple[int, list[Direction]]
        ] = {}
        min_heap = []
        insertion_order = 0 # To sort equal heat elements in heap

        heapq.heappush(min_heap, (0, insertion_order, start, tuple()))
        while min_heap:
            lost_heat, _, coords, previous_directions = heapq.heappop(min_heap)

            if (coords, previous_directions[-10:]) in done:
                continue

            done[coords, previous_directions[-10:]] = lost_heat, previous_directions

            if coords == end and len(set(previous_directions[-4:])) == 1:
                break

            for direction in self.find_allowed_ultra_directions(
                coords, previous_directions
            ):
                neighbour_previous_directions = (*previous_directions, direction)
                neighbour = coords + direction
                if (neighbour, neighbour_previous_directions[-10:]) in done:
                    continue
                insertion_order += 1
                neighbour_heat = lost_heat + self.blocks[neighbour]
                heapq.heappush(
                    min_heap,
                    (
                        neighbour_heat,
                        insertion_order,
                        neighbour,
                        neighbour_previous_directions
                    )
                )

        for (block, _), (heat_loss, path) in done.items():
            if block == end and len(set(path[-4:])) == 1:
                return heat_loss, path
        raise ValueError('Path not found!')

    def find_allowed_ultra_directions(
        self,
        coords: complex,
        previous_directions: tuple[Direction, ...]
    ) -> tuple[Direction, ...]:

        allowed = []

        if previous_directions and (
            previous_directions[-4:] != (previous_directions[-1],) * 4
        ):
            if coords + previous_directions[-1] in self.blocks:
                return (previous_directions[-1],)
            return tuple()

        for direction in Direction:

            if (
                len(previous_directions) >= 10 and
                previous_directions[-10:] == (direction,) * 10
            ):
                continue

            if (
                previous_directions and
                previous_directions[-1] == -direction
            ):
                continue

            new_block = coords + direction
            if new_block in self.blocks:
                allowed.append(direction)
        return tuple(allowed)

def main(input_text: str):
    city_map = CityMap.from_string(input_text)
    end = (city_map.width - 1) + (city_map.height - 1) * 1j
    heat_loss, _ = city_map.find_best_path(0, end)
    print(f'Solution part 1: {heat_loss}')

    # This takes a lot of RAM and time. For less resource consuming solution
    # consider creating a version that did not return the path, so
    # it would need to track only the last 10 elements of each path.
    heat_loss_ultra, _ = city_map.find_best_ultra_path(0, end)
    print(f'Solution part 2: {heat_loss_ultra}')

if __name__ == "__main__":
    INPUT_TEXT = sys.stdin.read()
    main(INPUT_TEXT)
