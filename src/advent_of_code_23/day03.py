'''https://adventofcode.com/2023/day/3'''

# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring

from collections import defaultdict
import sys

def is_digit(character: str) -> bool:
    return character in '1234567890'

def is_symbol(character: str) -> bool:
    return not is_digit(character) and character != '.'


def find_schematic_numbers(
    schematic_text: str
) -> tuple[tuple[int, int, int], ...]:
    """Scan the schematic text and return all the numbers, with their coords

    The structure for each number is (number, row, starting_column)
    """

    numbers: list[tuple[int, int, int]] = []

    for row, line in enumerate(schematic_text.splitlines()):
        current_number_digits = ''
        current_number_starting_col = None

        for col, character in enumerate(line):
            if is_digit(character):
                if current_number_starting_col is None:
                    current_number_starting_col = col
                current_number_digits += character

            elif current_number_digits and current_number_starting_col is not None:
                numbers.append((
                    int(current_number_digits),
                    row, current_number_starting_col)
                )
                current_number_digits = ''
                current_number_starting_col = None

        if current_number_digits and current_number_starting_col is not None:
            numbers.append((
                int(current_number_digits),
                row, current_number_starting_col)
            )

    return tuple(numbers)

def is_part_number(
    schematic_text: str, number: int, number_row: int, number_starting_col: int
) -> bool:

    schematic_lines = schematic_text.splitlines()

    number_length = len(str(number))

    start_row = max(0, number_row - 1)
    start_col = max(0, number_starting_col - 1)
    end_row = min(len(schematic_lines) - 1, number_row + 1)
    end_col = min(len(schematic_lines[0]) - 1 , number_starting_col + number_length)

    for row in range(start_row, end_row + 1):
        for col in range(start_col, end_col + 1):
            if is_symbol(schematic_lines[row][col]):
                return True
    return False

def find_schematic_part_numbers(schematic_text: str) -> tuple[int, ...]:

    numbers_and_coords = find_schematic_numbers(schematic_text)
    return tuple(
        number_and_coords[0]
        for number_and_coords in numbers_and_coords
        if is_part_number(schematic_text, *number_and_coords)
    )

def find_possible_gears(
    schematic_text: str, number: int, number_row: int, number_starting_col: int
) -> tuple[tuple[int, int], ...]:
    possible_gears = []

    schematic_lines = schematic_text.splitlines()

    number_length = len(str(number))

    start_row = max(0, number_row - 1)
    start_col = max(0, number_starting_col - 1)
    end_row = min(len(schematic_lines) - 1, number_row + 1)
    end_col = min(len(schematic_lines[0]) - 1 , number_starting_col + number_length)

    for row in range(start_row, end_row + 1):
        for col in range(start_col, end_col + 1):
            if schematic_lines[row][col] == '*':
                possible_gears.append((row, col))
    return tuple(possible_gears)

def find_gears(
    schematic_text: str
) -> tuple[tuple[tuple[int, int], int, int], ...]:

    possible_gears = defaultdict(list)
    numbers_and_coords = find_schematic_numbers(schematic_text)
    for number_and_coords in numbers_and_coords:
        number_possible_gears = find_possible_gears(schematic_text, *number_and_coords)
        for possible_gear in number_possible_gears:
            possible_gears[possible_gear].append(number_and_coords[0])

    return tuple(
        (gear, numbers[0], numbers[1])
        for gear, numbers in possible_gears.items()
        if len(numbers) == 2
    )

def main(input_text: str):
    part_numbers = find_schematic_part_numbers(input_text)
    part_numbers_sum = sum(part_numbers)
    print(f'Solution part 1: {part_numbers_sum}')

    gears = find_gears(input_text)
    gear_ratio_sum = sum(gear[1] * gear[2] for gear in gears)
    print(f'Solution part 2: {gear_ratio_sum}')

if __name__ == "__main__":
    INPUT_TEXT = sys.stdin.read()
    main(INPUT_TEXT)
