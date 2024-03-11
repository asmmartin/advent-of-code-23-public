# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring

import pytest

from advent_of_code_23.day04 import Card, play_all_cards

@pytest.fixture(name='example_cards_texts')
def example_cards_texts_fixture():
    return (
        "Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53",
        "Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19",
        "Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1",
        "Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83",
        "Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36",
        "Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11",
    )

def test_card_from_string(example_cards_texts):

    card_1 = Card.from_string(example_cards_texts[0])

    assert card_1.card_id == 1
    assert card_1.winning_numbers == {41, 48, 83, 86, 17}
    assert card_1.numbers == (83, 86, 6, 31, 17, 9, 48, 53)

def test_example_card_scores(example_cards_texts):

    cards = [Card.from_string(text) for text in example_cards_texts]
    scores = [card.score for card in cards]

    assert scores == [8, 2, 2, 1, 0, 0]

def test_play_all_cards(example_cards_texts):

    cards = (Card.from_string(text) for text in example_cards_texts)
    all_cards_amount = play_all_cards(cards)
    assert all_cards_amount == 30
