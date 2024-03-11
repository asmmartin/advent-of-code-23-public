'''https://adventofcode.com/2023/day/9'''

# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring

import sys
from typing import Self

class History:

    def __init__(self, values: list[int]) -> None:
        self.values = values

    @classmethod
    def from_string(cls, text: str) -> Self:
        values = [
            int(value_text) for value_text in text.split() if value_text
        ]
        return cls(values=values)

    def calculate_next_value(self) -> int:
        if all(
            value == 0 for value in self.values
        ):
            return 0

        sub_history = self.generate_sub_history()
        return self.values[-1] + sub_history.calculate_next_value()

    def calculate_previous_value(self) -> int:

        if all(
            value == 0 for value in self.values
        ):
            return 0

        sub_history = self.generate_sub_history()
        return self.values[0] - sub_history.calculate_previous_value()

    def generate_sub_history(self) -> 'History':

        sub_history_values = [
            self.values[index + 1] - self.values[index]
            for index in range(len(self.values) - 1)
        ]
        return History(values=sub_history_values)


def main(input_text: str):
    histories = [
        History.from_string(line) for line in input_text.splitlines()
    ]
    next_values = [history.calculate_next_value() for history in histories]
    print(f'Solution part 1: {sum(next_values)=}')

    previous_values = [history.calculate_previous_value() for history in histories]
    print(f'Solution part 2: {sum(previous_values)=}')

if __name__ == "__main__":
    INPUT_TEXT = sys.stdin.read()
    main(INPUT_TEXT)
