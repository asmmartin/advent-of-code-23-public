'''https://adventofcode.com/2023/day/7'''

# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring

import sys
from collections import Counter
from enum import Enum
from functools import partial, cmp_to_key
from typing import Callable

CARD_VALUES = dict(zip('AKQJT98765432', range(14, 1, -1)))

class HandType(Enum):
    FIVE_OF_A_KIND = 7
    FOUR_OF_A_KIND = 6
    FULL_HOUSE = 5
    THREE_OF_A_KIND = 4
    TWO_PAIRS = 3
    PAIR = 2
    HIGH_CARD = 1

def get_card_value(card: str, j_is_lowest: bool = False) -> int:
    value = CARD_VALUES.get(card, 0)
    if j_is_lowest and card == 'J':
        value = 1
    return value

def hand_cmp_by_first_difference(
    first: str,
    second: str,
    j_is_lowest: bool = False
) -> int:
    for cards in zip(first, second):
        values = (
            get_card_value(cards[0], j_is_lowest),
            get_card_value(cards[1], j_is_lowest)
        )
        if values[0] < values[1]:
            return -1
        if values[0] > values[1]:
            return 1
    return 0

def evaluated_hand_cmp(
    first: tuple[tuple[HandType, str | tuple[str, str]], str, int],
    second: tuple[tuple[HandType, str | tuple[str, str]], str, int],
    untie_func: Callable[[str, str], int]
) -> int:

    if first[0][0].value < second[0][0].value:
        return -1
    if first[0][0].value > second[0][0].value:
        return 1

    return untie_func(first[1], second[1])

def parse_hands_list(text: str) -> list[tuple[str, int]]:
    lines = text.splitlines()
    hands = []
    for line in lines:
        hand, bid = line.split(maxsplit=1)
        hands.append((hand, int(bid)))
    return hands

class HandClassifier:

    @staticmethod
    def find_five_of_a_kind(hand: str, j_is_joker: bool = False) -> str | None:
        counter = Counter(hand)

        if j_is_joker and (j_count := counter.get('J', 0)):
            counter = {card: count+j_count for card, count in counter.items()}
            counter['J'] = j_count

        for label, count in counter.items():
            if count == 5:
                return label
        return None

    @staticmethod
    def find_four_of_a_kind(hand: str, j_is_joker: bool = False) -> str | None:
        counter = Counter(hand)

        if j_is_joker and (j_count := counter.get('J', 0)):
            counter = {card: count+j_count for card, count in counter.items()}
            counter['J'] = j_count

        for label, count in counter.items():
            if count == 4:
                return label
        return None

    @staticmethod
    def find_three_of_a_kind(hand: str, j_is_joker: bool = False) -> str | None:
        counter = Counter(hand)

        if j_is_joker and (j_count := counter.get('J', 0)):
            counter = {card: count+j_count for card, count in counter.items()}
            counter['J'] = j_count

        for label, count in counter.items():
            if count == 3:
                return label
        return None

    @staticmethod
    def find_pair(hand: str, j_is_joker: bool = False) -> str | None:
        counter = Counter(hand)

        if j_is_joker and (j_count := counter.get('J', 0)):
            counter = {card: count+j_count for card, count in counter.items()}
            counter['J'] = j_count

        for label, count in counter.items():
            if count == 2:
                return label
        return None

    @staticmethod
    def find_full_house(
        hand: str, j_is_joker: bool = False
    ) -> tuple[str, str] | None:

        three_of_a_kind = HandClassifier.find_three_of_a_kind(hand, j_is_joker)
        if not three_of_a_kind:
            return None

        hand = hand.replace(three_of_a_kind, '')

        if j_is_joker:
            hand = hand.replace('J', '')

        pair = HandClassifier.find_pair(hand, j_is_joker)

        if three_of_a_kind and pair:
            return (three_of_a_kind, pair)
        return None


    @staticmethod
    def find_two_pairs(
        hand: str, j_is_joker: bool = False
    ) -> tuple[str, str] | None:
        pairs = []

        counter = Counter(hand)

        if j_is_joker and (j_count := counter.get('J', 0)):
            counter = {card: count+j_count for card, count in counter.items()}
            counter['J'] = j_count

        for label, count in counter.items():
            if count == 2:
                pairs.append(label)

        if len(pairs) == 2:
            return tuple(sorted(pairs, key=get_card_value, reverse=True)) # type: ignore
        return None

    @staticmethod
    def find_high_card(hand: str, j_is_joker: bool = False) -> str | None:
        if len(hand) == len(set(hand)):
            sorted_cards = sorted(
                hand,
                key=partial(get_card_value, j_is_lowest=j_is_joker),
                reverse=True
            )
            return sorted_cards[0]
        return None

    @staticmethod
    def classify(
        hand: str,
        j_is_joker: bool = False
    ) -> tuple[HandType, str | tuple[str, str]]:

        finders = {
            HandClassifier.find_five_of_a_kind: HandType.FIVE_OF_A_KIND,
            HandClassifier.find_four_of_a_kind: HandType.FOUR_OF_A_KIND,
            HandClassifier.find_full_house: HandType.FULL_HOUSE,
            HandClassifier.find_three_of_a_kind: HandType.THREE_OF_A_KIND,
            HandClassifier.find_two_pairs: HandType.TWO_PAIRS,
            HandClassifier.find_pair: HandType.PAIR,
            HandClassifier.find_high_card: HandType.HIGH_CARD
        }

        for finder, hand_type in finders.items():
            found = finder(hand, j_is_joker)
            if found is not None:
                return hand_type, found

        raise ValueError(f'{hand=} does not match with any of the types!')
class HandsSorter:

    def __init__(
        self, hands: list[tuple[str, int]], j_is_joker: bool = False
    ) -> None:
        self.evaluated_hands = []
        for hand in hands:
            classification = HandClassifier.classify(hand[0], j_is_joker=j_is_joker)
            self.evaluated_hands.append(
                (classification, hand[0], hand[1])
            )

    def sort(
        self, untie_func: Callable[[str, str], int], reverse: bool = False
    ) -> list[tuple[str, int]]:

        cmp_func = partial(evaluated_hand_cmp, untie_func=untie_func)
        key_func = cmp_to_key(cmp_func)

        sorted_hands = sorted(
            self.evaluated_hands, key=key_func, reverse=reverse
        )
        return [(hand[1], hand[2]) for hand in sorted_hands]

def main(input_text: str):
    hands = parse_hands_list(input_text)
    sorter = HandsSorter(hands)
    sorted_hands = sorter.sort(hand_cmp_by_first_difference)
    winnings = sum((i + 1) * hand[1] for i, hand in enumerate(sorted_hands))
    print(f'Solution part 1: {winnings}')

    sorter_jokers = HandsSorter(hands, j_is_joker=True)
    sorted_hands_jokers = sorter_jokers.sort(
        partial(hand_cmp_by_first_difference, j_is_lowest=True)
    )
    winnings_jokers = sum(
        (i + 1) * hand[1] for i, hand in enumerate(sorted_hands_jokers)
    )
    print(f'Solution part 2: {winnings_jokers}')

if __name__ == "__main__":
    INPUT_TEXT = sys.stdin.read()
    main(INPUT_TEXT)
