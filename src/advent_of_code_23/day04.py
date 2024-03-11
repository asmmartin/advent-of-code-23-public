'''https://adventofcode.com/2023/day/4'''

# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring

import re
import sys
from dataclasses import dataclass
from functools import cached_property
from typing import Iterable, Self

@dataclass
class Card:
    card_id: int
    winning_numbers: set[int]
    numbers: tuple[int, ...]

    @classmethod
    def from_string(cls, string: str) -> Self:
        card_info, all_numbers = string.split(':')
        winning_numbers_text, numbers_text = all_numbers.split('|')

        card_id = int(re.findall(r'\d+', card_info)[0])
        winning_numbers = {
            int(number) for number in re.findall(r'\d+', winning_numbers_text)
        }
        numbers = tuple(
            int(number) for number in re.findall(r'\d+', numbers_text)
        )

        return cls(
            card_id=card_id, winning_numbers=winning_numbers, numbers=numbers
        )

    @cached_property
    def wins(self) -> int:
        return sum(
            1 if number in self.winning_numbers else 0
            for number in self.numbers
        )

    @cached_property
    def score(self) -> int:
        return 2**(self.wins-1) if self.wins else 0

def play_all_cards(cards: Iterable[Card]) -> int:
    cards = list(cards)
    card_amounts = [1 for _ in cards]

    for card_index, card in enumerate(cards):
        for win_index in range(card_index + 1, card_index + card.wins + 1):
            card_amounts[win_index] += card_amounts[card_index]
    return sum(card_amounts)

def main(input_text: str):
    input_lines = input_text.splitlines()
    cards = [Card.from_string(line) for line in input_lines]
    total_points = sum(card.score for card in cards)
    print(f'Solution part 1: {total_points}')

    total_cards = play_all_cards(cards)
    print(f'Solution part 2: {total_cards}')

if __name__ == "__main__":
    INPUT_TEXT = sys.stdin.read()
    main(INPUT_TEXT)
