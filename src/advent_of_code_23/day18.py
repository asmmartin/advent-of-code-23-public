'''https://adventofcode.com/2023/day/18'''

# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring

from functools import cached_property
import sys
from enum import Enum
from typing import Iterable

class Direction(complex, Enum):
    UP = -1j
    DOWN = 1j
    RIGHT = 1
    LEFT = -1

Instruction = tuple[Direction, int]

def parse_instruction(text: str) -> Instruction:
    direction_letters = {
        'R': Direction.RIGHT,
        'L': Direction.LEFT,
        'U': Direction.UP,
        'D': Direction.DOWN
    }
    direction, count, _ = text.strip().split()
    return direction_letters[direction], int(count)

def parse_rgb_instruction(text: str) -> Instruction:
    direction_digits = {
        '0': Direction.RIGHT,
        '1': Direction.DOWN,
        '2': Direction.LEFT,
        '3': Direction.UP
    }
    _, _, rgb = text.strip().split()

    rgb = rgb[1:-1].replace('#', '0x')

    count, direction = int(rgb[:-1], 0), rgb[-1]

    return direction_digits[direction], int(count)

class Trench:
    def __init__(self, vertices: tuple[complex, ...]) -> None:
        self.vertices = vertices
        self.edges = tuple(
            (vertices[index], vertices[(index+1)%len(vertices)])
            for index in range(len(vertices))
        )

    @classmethod
    def from_instructions(cls, instructions: Iterable[Instruction]):
        vertices = [0+0j]
        for instruction in instructions:
            new_vertex = vertices[-1] + instruction[0]*instruction[1]
            vertices.append(new_vertex)

        if vertices[0] != vertices[-1]:
            raise ValueError('Instructions do not form a closed trench!')

        return cls(vertices=tuple(vertices[:-1]))

    @cached_property
    def edge_cubes_count(self) -> int:
        return sum(
            int(abs(edge[1] - edge[0]))
            for edge in self.edges
        )

    @cached_property
    def interior_cubes_count(self) -> int:

        # Shoelace Formula
        total_area = sum(
            (
                self.vertices[index].real *
                (
                    self.vertices[(index+1) % len(self.vertices)].imag
                    -
                    self.vertices[(index-1) % len(self.vertices)].imag
                )
            )
            for index in range(len(self.vertices))
        ) // 2

        # Pick's Theorem
        interior = int(total_area) + 1 - self.edge_cubes_count//2

        return interior

    @cached_property
    def total_volume(self) -> int:
        return self.edge_cubes_count + self.interior_cubes_count

def main(input_text: str):
    instructions = [
        parse_instruction(instruction)
        for instruction in input_text.strip().splitlines()
    ]
    trench = Trench.from_instructions(instructions)
    print(f'Solution part 1: {trench.total_volume}')

    rgb_instructions = [
        parse_rgb_instruction(instruction)
        for instruction in input_text.strip().splitlines()
    ]
    rgb_trench = Trench.from_instructions(rgb_instructions)
    print(f'Solution part 2: {rgb_trench.total_volume}')

if __name__ == "__main__":
    INPUT_TEXT = sys.stdin.read()
    main(INPUT_TEXT)
