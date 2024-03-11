'''https://adventofcode.com/2023/day/6'''

# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring

import math
import re
import sys

def parse_sheet(sheet_text: str) -> tuple[tuple[int, int], ...]:
    time_line, distance_line = sheet_text.splitlines()[:2]
    times = [int(number) for number in re.findall(r'\d+', time_line)]
    distances = [int(number) for number in re.findall(r'\d+', distance_line)]

    return tuple(zip(times, distances))

def parse_sheet_singular(sheet_text: str) -> tuple[int, int]:

    time_line, distance_line = sheet_text.splitlines()[:2]
    time = int(''.join(re.findall(r'\d+', time_line)))
    distance = int(''.join(re.findall(r'\d+', distance_line)))

    return time, distance

def find_winners(time: int, distance: int) -> range:

    # T := race time; h := time holding; D := record distance
    # Formula: (T - h) * h > D

    low = (time - math.sqrt(time**2 - 4 * distance)) / 2
    up = (time + math.sqrt(time**2 - 4 * distance)) / 2

    return range(math.floor(low) + 1, math.ceil(up))

def main(input_text: str):
    sheet = parse_sheet(input_text)
    winners = (len(find_winners(time, distance)) for time, distance in sheet)
    winners_prod = math.prod(winners)
    print(f'Solution part 1: {winners_prod}')

    singular_sheet = parse_sheet_singular(input_text)
    winners = find_winners(*singular_sheet)
    print(f'Solution part 1: {len(winners)}')

if __name__ == "__main__":
    INPUT_TEXT = sys.stdin.read()
    main(INPUT_TEXT)
