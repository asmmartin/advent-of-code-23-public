'''https://adventofcode.com/2023/day/22'''

# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring

from collections import defaultdict
from typing import Iterable, Self
from uuid import uuid4
import sys
from dataclasses import dataclass, field

@dataclass
class Brick:
    coords: tuple[list[int], list[int]]
    brick_id: str = field(default_factory=lambda: str(uuid4()))
    is_support_of: set[str] = field(default_factory=set)
    is_supported_by: set[str] = field(default_factory=set)

    @property
    def footprint(self) -> set[tuple[int, int]]:
        footprint = set()
        for x in range(self.coords[0][0], self.coords[1][0]+1):
            for y in range(self.coords[0][1], self.coords[1][1]+1):
                footprint.add((x, y))
        return footprint

    @property
    def height(self) -> int:
        return self.coords[1][2] - self.coords[0][2] + 1

    @property
    def base_height(self) -> int:
        return self.coords[0][2]

    @classmethod
    def from_string(cls, text: str) -> Self:
        coords_strings = text.strip().split('~')
        coords = (
            [int(c) for c in coords_strings[0].split(',')],
            [int(c) for c in coords_strings[1].split(',')],
        )
        return cls(coords=coords)

class Tower:

    def __init__(self, bricks: Iterable[Brick]) -> None:
        self.bricks = {brick.brick_id: brick for brick in bricks}

    def drop_bricks(self) -> None:
        column_heights: dict[tuple[int, int], tuple[int, str]] = defaultdict(
            lambda: (1, 'FLOOR')
        )
        bricks = sorted(
            self.bricks.values(), key=lambda brick: brick.base_height
        )

        for brick in bricks:
            support_height = 1
            supports = set()
            for tile in brick.footprint:
                column_height, support_brick_id = column_heights[tile]
                if column_height > support_height:
                    support_height = column_height
                    supports = set()

                if column_height == support_height:
                    supports.add(support_brick_id)

            brick_height = brick.height
            brick.coords[0][2] = support_height
            brick.coords[1][2] = support_height + brick_height - 1

            brick.is_supported_by = supports
            for support_brick_id in supports:
                if support_brick_id == 'FLOOR':
                    continue
                self.bricks[support_brick_id].is_support_of.add(brick.brick_id)

            for tile in brick.footprint:
                column_heights[tile] = brick.coords[1][2] + 1, brick.brick_id

    def get_safely_desintegrable_brick_ids(self) -> set[str]:
        desintegrable = set()
        for brick in self.bricks.values():
            for supported_brick_id in brick.is_support_of:
                supported_brick = self.bricks[supported_brick_id]
                if len(supported_brick.is_supported_by) < 2:
                    break
            else:
                desintegrable.add(brick.brick_id)

        return desintegrable

    def get_dropping_bricks_if_desintegrate(self, brick_id: str) -> set[str]:
        would_drop = set((brick_id,))

        bricks = sorted(
            self.bricks.values(), key=lambda brick: brick.base_height
        )

        for brick in bricks:
            if brick.brick_id in would_drop:
                for support_brick_id in brick.is_support_of:
                    supported_brick = self.bricks[support_brick_id]
                    if all(
                        support in would_drop
                        for support in supported_brick.is_supported_by
                    ):
                        would_drop.add(supported_brick.brick_id)

        would_drop.remove(brick_id)
        return would_drop

def main(input_text: str):
    lines = input_text.strip().splitlines()
    bricks = [Brick.from_string(line) for line in lines]
    tower = Tower(bricks=bricks)
    tower.drop_bricks()
    desintegrable = tower.get_safely_desintegrable_brick_ids()
    print(f'Solution part 1: {len(desintegrable)}')

    potential_brick_falling = sum(
        len(tower.get_dropping_bricks_if_desintegrate(brick_id))
        for brick_id in tower.bricks.keys()
    )
    print(f'Solution part 2: {potential_brick_falling}')

if __name__ == "__main__":
    INPUT_TEXT = sys.stdin.read()
    main(INPUT_TEXT)
