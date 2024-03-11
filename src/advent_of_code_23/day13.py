'''https://adventofcode.com/2023/day/13'''

# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring

from collections import defaultdict
import sys
from typing import Self

ROCK = '#'
ASH = '.'


class Pattern:

    def __init__(self, rocks: set[complex], height: int, width: int) -> None:
        self.rocks = rocks
        self.height = height
        self.width = width
        rows = defaultdict(list)
        columns = defaultdict(list)

        for rock in rocks:
            rows[int(rock.imag)].append(rock)
            columns[int(rock.real)].append(rock)

        self.rows = {k: tuple(v) for k, v in rows.items()}
        self.columns = {k: tuple(v) for k, v in columns.items()}


    @classmethod
    def from_string(cls, text: str) -> Self:
        rocks = set()
        lines = text.strip().splitlines()
        for row, line in enumerate(lines):
            for col, tile in enumerate(line):
                if tile != ROCK:
                    continue
                rock = col + row*1j
                rocks.add(rock)
        return cls(
            rocks=rocks,
            height=len(lines),
            width=len(lines[0])
        )

    def calculate_score(self, smudges: int = 0) -> int:
        score = 0

        if (
            vertical_mirror := find_vertical_mirrors(self, smudges)
        ) is not None:
            score += vertical_mirror
        if (
            horizontal_mirror := find_horizontal_mirrors(self, smudges)
        ) is not None:
            score += horizontal_mirror*100

        return score


def find_vertical_mirrors(pattern: Pattern, smudges: int = 0) -> int | None:

    middle = pattern.width // 2

    # Left half
    for column in range(1, middle+1):
        left_reflection, right = set(), set()
        for delta in range(0, column):
            for rock in pattern.columns.get(column-delta-1, ()):
                left_reflection.add(rock + 2*delta+1)
            for rock in pattern.columns.get(column+delta, ()):
                right.add(rock)
        if len(right.symmetric_difference(left_reflection)) == smudges:
            return column

    # Right half
    for column in range(middle+1, pattern.width):
        left_reflection, right = set(), set()
        for delta in range(0, pattern.width - column):
            for rock in pattern.columns.get(column-delta-1, ()):
                left_reflection.add(rock + 2*delta+1)
            for rock in pattern.columns.get(column+delta, ()):
                right.add(rock)
        if len(right.symmetric_difference(left_reflection)) == smudges:
            return column

def find_horizontal_mirrors(pattern: Pattern, smudges: int = 0) -> int | None:

    middle = pattern.height // 2

    # Top half
    for row in range(1, middle+1):
        top_reflection, bottom = set(), set()
        for delta in range(0, row):
            for rock in pattern.rows.get(row-delta-1, ()):
                top_reflection.add(rock + (2*delta+1)*1j)
            for rock in pattern.rows.get(row+delta, ()):
                bottom.add(rock)
        if len(bottom.symmetric_difference(top_reflection)) == smudges:
            return row

    # Bottom half
    for row in range(middle+1, pattern.height):
        top_reflection, bottom = set(), set()
        for delta in range(0, pattern.height - row):
            for rock in pattern.rows.get(row-delta-1, ()):
                top_reflection.add(rock + (2*delta+1)*1j)
            for rock in pattern.rows.get(row+delta, ()):
                bottom.add(rock)
        if len(bottom.symmetric_difference(top_reflection)) == smudges:
            return row

def main(input_text: str):
    pattern_texts = input_text.strip().split('\n\n')
    patterns = tuple(Pattern.from_string(text) for text in pattern_texts)
    scores = tuple(pattern.calculate_score() for pattern in patterns)
    print(f'Solution part 1: {sum(scores)}')

    scores_with_smudges = tuple(
        pattern.calculate_score(1) for pattern in patterns
    )
    print(f'Solution part 2: {sum(scores_with_smudges)}')

if __name__ == "__main__":
    INPUT_TEXT = sys.stdin.read()
    main(INPUT_TEXT)
