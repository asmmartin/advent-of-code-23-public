'''https://adventofcode.com/2023/day/1'''

# pylint: disable=missing-function-docstring

import sys
import re

DIGITS = {
    'one': '1',
    'two': '2',
    'three': '3',
    'four': '4',
    'five': '5',
    'six': '6',
    'seven': '7',
    'eight': '8',
    'nine': '9'
}

def read_calibration_value(text: str) -> int:

    pattern = re.compile(
        r'(?=(\d|one|two|three|four|five|six|seven|eight|nine))'
    )

    numbers = pattern.findall(text)
    if not numbers:
        raise ValueError(f'{text!r} does not include numbers!')

    first, last = numbers[0], numbers[-1]

    first = DIGITS.get(first, first)
    last = DIGITS.get(last, last)

    return int(first + last)

def main(input_text: str):
    total = sum(
        read_calibration_value(calibration_line)
        for calibration_line in input_text.splitlines()
    )
    print(f'Solution: {total}')

if __name__ == "__main__":
    INPUT_TEXT = sys.stdin.read()
    main(INPUT_TEXT)
