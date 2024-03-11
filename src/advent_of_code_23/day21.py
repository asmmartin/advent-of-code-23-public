'''https://adventofcode.com/2023/day/21'''

# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring

from functools import cached_property
import sys
from collections import deque
from typing import Iterable, Self

class Garden:

    def __init__(
        self,
        rocks: Iterable[complex],
        width: int,
        heigth: int,
        start: complex
    ):
        self.rocks = set(rocks)
        self.width = width
        self.heigth = heigth
        self.start = start

    @classmethod
    def from_string(cls, text: str) -> Self:
        lines = text.strip().splitlines()

        heigth = len(lines)
        width = len(lines[0])
        rocks = []
        start = None

        for row, line in enumerate(lines):
            for col, plot in enumerate(line):
                if plot == 'S':
                    start = col + row*1j
                elif plot == '#':
                    rocks.append(col + row*1j)

        if start is None:
            raise ValueError('Unknown starting plot!')

        return cls(
            rocks=rocks, width=width, heigth=heigth, start=start
        )

    def find_final_reachable_plots(self, steps: int) -> set[complex]:

        final_plots = set()

        if steps < 0:
            return final_plots

        # BFS
        to_visit = deque()
        to_visit.append((steps, self.start))
        visited = set()

        while to_visit:
            remaining_steps, plot = to_visit.popleft()

            if plot in visited:
                continue
            visited.add(plot)

            if remaining_steps % 2 == 0:
                final_plots.add(plot)

            if not remaining_steps:
                continue

            for direction in (1, -1, 1j, -1j):
                neighbour = plot + direction
                if neighbour in visited:
                    continue
                if not 0 <= neighbour.real < self.width:
                    continue
                if not 0 <= neighbour.imag < self.heigth:
                    continue
                if neighbour in self.rocks:
                    continue
                to_visit.append((remaining_steps-1, neighbour))

        return final_plots

    @cached_property
    def even_plots_count(self) -> int:
        return len(self.find_final_reachable_plots(4*self.width))

    @cached_property
    def odd_plots_count(self) -> int:
        return len(self.find_final_reachable_plots(4*self.width+1))

class InfiniteGarden(Garden):

    @cached_property
    def even_plots_count(self) -> int:
        return len(super().find_final_reachable_plots(4*self.width))

    @cached_property
    def odd_plots_count(self) -> int:
        return len(super().find_final_reachable_plots(4*self.width+1))

    def find_final_reachable_plots(self, steps: int) -> set[complex]:

        final_plots = set()

        # BFS
        to_visit = deque()
        to_visit.append((steps, self.start))
        visited: set[complex] = set()

        while to_visit:
            remaining_steps, plot = to_visit.popleft()

            if plot in visited:
                continue
            visited.add(plot)

            if remaining_steps % 2 == 0:
                final_plots.add(plot)

            if not remaining_steps:
                continue

            for direction in (1, -1, 1j, -1j):
                neighbour = plot + direction
                if (remaining_steps-1, neighbour) in visited:
                    continue
                normalized_neighbour = (
                    (neighbour.real % self.width) +
                    (neighbour.imag % self.heigth) * 1j
                )
                if normalized_neighbour in self.rocks:
                    continue
                to_visit.append((remaining_steps-1, neighbour))

        return final_plots

    def find_final_reachable_plots_count_particular(self, steps: int) -> int:

        # This solution makes some assumptions:
        #   - The garden is a square
        #   - The garden side has odd length
        #   - The starting plot is the central one
        #   - There are no rocks in the starting plot row and column

        assert self.width == self.heigth
        assert self.width % 2
        assert int(self.start.real) == int(self.start.imag) == self.width // 2
        assert all(rock.real != self.start.real for rock in self.rocks)
        assert all(rock.imag != self.start.imag for rock in self.rocks)
        assert steps > self.width//2
        # assert steps % 2


        # For every int m where
        #       m * garden.width <= steps < (m+1) * garden.width
        #
        #   - The amount of 'half empty diagonal gardens' = m (per diag)
        #   - The amount of 'half full diagonal gardens' = m - 1 (per diag)

        g = (steps - self.width//2 - 1) // self.width
        m = steps // self.width

        central_parity = steps % 2

        same_parity_gardens = (g//2*2 + 1) ** 2
        different_parity_gardens = ((g-1)//2 * 2 + 2) ** 2
        half_empty_diagonal_gardens = m
        half_full_diagonal_gardens = max(0, m-1)

        # Internal gardens
        if central_parity == 1:
            internal_plots = (
                self.odd_plots_count * same_parity_gardens
                +
                self.even_plots_count * different_parity_gardens
            )
        else:
            internal_plots = (
                self.even_plots_count * same_parity_gardens
                +
                self.odd_plots_count * different_parity_gardens
            )

        # Diagonal gardens
        diagonal_reminder = steps % self.width - 1
        diagonal_gardens = {
            "top_right": Garden(
                self.rocks, self.width, self.heigth,
                start=(self.heigth-1) * 1j
            ),
            "top_left": Garden(
                self.rocks, self.width, self.heigth,
                start=(self.width-1) + (self.heigth-1) * 1j
            ),
            "bottom_right": Garden(
                self.rocks, self.width, self.heigth,
                start=0
            ),
            "bottom_left": Garden(
                self.rocks, self.width, self.heigth,
                start=self.width-1
            )
        }
        half_empty_garden_plot_counts = {
            key: len(garden.find_final_reachable_plots(diagonal_reminder))
            for key, garden in diagonal_gardens.items()
        }
        half_full_garden_plot_counts = {
            key: len(garden.find_final_reachable_plots(self.width+diagonal_reminder))
            for key, garden in diagonal_gardens.items()
        }
        diagonal_gardens_plots = (
            sum(
                half_empty_diagonal_gardens*count
                for count in half_empty_garden_plot_counts.values()
            )
            +
            sum(
                half_full_diagonal_gardens*count
                for count in half_full_garden_plot_counts.values()
            )
        )

        # Tip gardens
        tip_remainder = (steps - self.width//2 - 1) % self.width
        tip_gardens = {
            "top": Garden(
                self.rocks, self.width, self.heigth,
                start=self.width//2 + (self.heigth-1)*1j
            ),
            "left": Garden(
                self.rocks, self.width, self.heigth,
                start=(self.width-1) + (self.heigth//2)*1j
            ),
            "bottom": Garden(
                self.rocks, self.width, self.heigth,
                start=(self.width//2)
            ),
            "rigth": Garden(
                self.rocks, self.width, self.heigth,
                start=(self.heigth//2)*1j
            )
        }
        tip_gardens_plot_counts = {
            key: len(garden.find_final_reachable_plots(tip_remainder))
            for key, garden in tip_gardens.items()
        }
        tip_gardens_plots = sum(
            count for count in tip_gardens_plot_counts.values()
        )

        return internal_plots + diagonal_gardens_plots + tip_gardens_plots


def main(input_text: str):
    garden = Garden.from_string(input_text)
    plots = garden.find_final_reachable_plots(steps=64)
    print(f'Solution part 1: {len(plots)}')

    infinite_garden = InfiniteGarden.from_string(input_text)
    infinite_plots = infinite_garden.find_final_reachable_plots_count_particular(
        26501365
    )
    print(f'Solution part 2: {infinite_plots}')


if __name__ == "__main__":
    INPUT_TEXT = sys.stdin.read()
    main(INPUT_TEXT)
