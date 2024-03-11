'''https://adventofcode.com/2023/day/24'''

# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring

import sys
from dataclasses import dataclass
from itertools import combinations
from typing import Self

import numpy as np
import sympy

@dataclass
class Hailstone:
    position: tuple[int, int, int]
    velocity: tuple[int, int, int]

    @classmethod
    def from_string(cls, text: str) -> Self:
        position, velocity = text.split('@')
        return cls(
            position=tuple(int(p) for p in position.split(',')), # type: ignore
            velocity=tuple(int(v) for v in velocity.split(',')) # type: ignore
        )

    def find_xy_path_cross_point_with(
        self, other: Self
    ) -> tuple[float, float] | None:

        a = [
            [self.velocity[0], -other.velocity[0]],
            [self.velocity[1], -other.velocity[1]],
        ]
        b = [
            other.position[0] - self.position[0],
            other.position[1] - self.position[1],
        ]

        x, _, rank, _ = np.linalg.lstsq(a, b, rcond=None)

        if int(rank) < 2:
            return None

        cross_point = (
            self.position[0] + x[0] * self.velocity[0],
            self.position[1] + x[0] * self.velocity[1],
        )

        return cross_point

    def is_future_point(
        self, point: tuple[float, float, float], ignore_z: bool = True
    ) -> bool:

        k = (
            (point[0] - self.position[0]) // self.velocity[0],
            (point[1] - self.position[1]) // self.velocity[1],
            (point[2] - self.position[2]) // self.velocity[2]
        )

        if ignore_z:
            return k[0] >= 0 and k[1] >= 0
        return k[0] >= 0 and k[1] >= 0 and k[2] >= 0

def find_future_xy_crosses_in_area_count(
    hailstones: list[Hailstone], boundaries: tuple[int, int]
) -> int:

    hailstones_combinations = combinations(hailstones, 2)

    cross_count = 0
    for hailstone_pair in hailstones_combinations:
        cross_point = hailstone_pair[0].find_xy_path_cross_point_with(
            hailstone_pair[1]
        )
        if cross_point is None:
            continue
        if not hailstone_pair[0].is_future_point((*cross_point, 0)):
            continue
        if not hailstone_pair[1].is_future_point((*cross_point, 0)):
            continue
        if not boundaries[0] <= cross_point[0] <= boundaries[1]:
            continue
        if not boundaries[0] <= cross_point[1] <= boundaries[1]:
            continue
        cross_count += 1

    return cross_count

def get_smashing_stone(hailstones: list[Hailstone]) -> Hailstone:

    prx, pry, prz, vrx, vry, vrz = sympy.symbols((
        'prx', 'pry', 'prz', 'vrx', 'vry', 'vrz'
    ))

    system = []
    # Only 3 collisions needed
    for hailstone in hailstones[:3]:
        phx, phy, phz = hailstone.position
        vhx, vhy, vhz = hailstone.velocity

        system.append(sympy.Eq((prx-phx)*(vhy-vry), (vhx-vrx)*(pry-phy)))
        system.append(sympy.Eq((pry-phy)*(vhz-vrz), (vhy-vry)*(prz-phz)))
        system.append(sympy.Eq((prx-phx)*(vhz-vrz), (vhx-vrx)*(prz-phz)))

    try:
        solution = sympy.solve(system)[0]
    except IndexError as error:
        raise ValueError('There is no solution!!') from error

    return Hailstone(
        position=(solution[prx], solution[pry], solution[prz]),
        velocity=(solution[vrx], solution[vry], solution[vrz]),
    )

def main(input_text: str):
    lines = input_text.splitlines()
    hailstones = [Hailstone.from_string(line) for line in lines]
    boundaries = (200000000000000, 400000000000000)
    cross_count = find_future_xy_crosses_in_area_count(hailstones, boundaries)
    print(f'Solution part 1: {cross_count}')

    stone = get_smashing_stone(hailstones)
    print(f'Solution part 2: {sum(stone.position)}')

if __name__ == "__main__":
    INPUT_TEXT = sys.stdin.read().strip()
    main(INPUT_TEXT)
