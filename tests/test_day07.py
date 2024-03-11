# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring

from functools import partial

import pytest

from advent_of_code_23.day07 import (
    HandClassifier, HandType, hand_cmp_by_first_difference, parse_hands_list,
    HandsSorter
)

@pytest.fixture(name='example_hands_list_text')
def example_hands_list_text_fixture():
    return (
        "32T3K 765\n"
        "T55J5 684\n"
        "KK677 28\n"
        "KTJJT 220\n"
        "QQQJA 483"
    )

@pytest.fixture(name='example_hands_list_text_reddit')
def example_hands_list_text_reddit_fixture():
    # Credit: https://www.reddit.com/r/adventofcode/comments/
    # 18cr4xr/2023_day_7_better_example_input_not_a_spoiler/
    return (
        "2345A 1\n"
        "Q2KJJ 13\n"
        "Q2Q2Q 19\n"
        "T3T3J 17\n"
        "T3Q33 11\n"
        "2345J 3\n"
        "J345A 2\n"
        "32T3K 5\n"
        "T55J5 29\n"
        "KK677 7\n"
        "KTJJT 34\n"
        "QQQJA 31\n"
        "JJJJJ 37\n"
        "JAAAA 43\n"
        "AAAAJ 59\n"
        "AAAAA 61\n"
        "2AAAA 23\n"
        "2JJJJ 53\n"
        "JJJJ2 41\n"
    )

def test_parse_hands_list(example_hands_list_text):
    parsed = parse_hands_list(example_hands_list_text)
    assert parsed == [
        ("32T3K", 765),
        ("T55J5", 684),
        ("KK677", 28),
        ("KTJJT", 220),
        ("QQQJA", 483)
    ]

def test_hand_classifier_find_five_of_a_kind():

    assert HandClassifier.find_five_of_a_kind('AAAAA') == 'A'
    assert HandClassifier.find_five_of_a_kind('77777') == '7'
    assert HandClassifier.find_five_of_a_kind('AAAA7') is None


def test_hand_classifier_find_four_of_a_kind():

    assert HandClassifier.find_four_of_a_kind('AAAA7') == 'A'
    assert HandClassifier.find_four_of_a_kind('77K77') == '7'
    assert HandClassifier.find_four_of_a_kind('AAAAA') is None
    assert HandClassifier.find_four_of_a_kind('77777') is None

def test_hand_classifier_find_three_of_a_kind():

    assert HandClassifier.find_three_of_a_kind('AAAK7') == 'A'
    assert HandClassifier.find_three_of_a_kind('77KQ7') == '7'
    assert HandClassifier.find_three_of_a_kind('AAAAA') is None
    assert HandClassifier.find_three_of_a_kind('77777') is None

def test_hand_classifier_find_pair():

    assert HandClassifier.find_pair('AAQK7') == 'A'
    assert HandClassifier.find_pair('79KQ7') == '7'
    assert HandClassifier.find_pair('AAAAA') is None
    assert HandClassifier.find_pair('77777') is None

def test_hand_classifier_find_full_house():

    assert HandClassifier.find_full_house('AAA77') == ('A', '7')
    assert HandClassifier.find_full_house('7AA77') == ('7', 'A')
    assert HandClassifier.find_full_house('AAAAA') is None
    assert HandClassifier.find_full_house('7AAAA') is None
    assert HandClassifier.find_full_house('77A77') is None

def test_hand_classifier_find_full_house_joker():

    assert HandClassifier.find_full_house('AAJ77', True) == ('A', '7')
    assert HandClassifier.find_full_house('AJJ77', True) == ('A', '7')
    assert HandClassifier.find_full_house('7AA77', True) == ('7', 'A')
    assert HandClassifier.find_full_house('AAAAJ', True) is None

def test_hand_classifier_find_two_pairs():

    assert HandClassifier.find_two_pairs('AAK77') == ('A', '7')
    assert HandClassifier.find_two_pairs('KAKA8') == ('A', 'K')
    assert HandClassifier.find_two_pairs('7AAAA') is None
    assert HandClassifier.find_two_pairs('77A77') is None

def test_hand_classifier_find_high_card():

    assert HandClassifier.find_high_card('TAK47') == 'A'
    assert HandClassifier.find_high_card('TQK47') == 'K'
    assert HandClassifier.find_high_card('7AAAA') is None
    assert HandClassifier.find_high_card('77A77') is None

def test_hand_classifier_classify():

    hands = ['AAAAA', 'AAAAK', 'AKAKA', 'AK7KK', 'AKAK7', 'AK47A', 'AK74T']

    classifications = [HandClassifier.classify(hand) for hand in hands]

    assert classifications == [
        (HandType.FIVE_OF_A_KIND, 'A'),
        (HandType.FOUR_OF_A_KIND, 'A'),
        (HandType.FULL_HOUSE, ('A', 'K')),
        (HandType.THREE_OF_A_KIND, 'K'),
        (HandType.TWO_PAIRS, ('A', 'K')),
        (HandType.PAIR, 'A'),
        (HandType.HIGH_CARD, 'A'),
    ]

def test_hand_cmp_by_first_difference():

    ties = [('33332', '2AAAA'), ('77888', '77788')]
    assert hand_cmp_by_first_difference(*ties[0]) == 1
    assert hand_cmp_by_first_difference(*ties[0][::-1]) == -1
    assert hand_cmp_by_first_difference(*ties[1]) == 1
    assert hand_cmp_by_first_difference(*ties[1][::-1]) == -1


def test_hands_sorter_sort(example_hands_list_text):
    hands = parse_hands_list(example_hands_list_text)

    sorter = HandsSorter(hands)
    sorted_hands = sorter.sort(
        untie_func=hand_cmp_by_first_difference, reverse=True
    )
    sorted_hands_strings = [hand[0] for hand in sorted_hands]

    winnings = 0
    for i, hand in enumerate(sorted_hands[::-1]):
        winnings += (i + 1) * hand[1]

    assert sorted_hands_strings == [
        "QQQJA",
        "T55J5",
        "KK677",
        "KTJJT",
        "32T3K",
    ]
    assert winnings == 6440

def test_hands_sorter_sort_with_jokers(example_hands_list_text):
    hands = parse_hands_list(example_hands_list_text)

    sorter = HandsSorter(hands, j_is_joker=True)
    sorted_hands = sorter.sort(
        untie_func=hand_cmp_by_first_difference, reverse=True
    )
    sorted_hands_strings = [hand[0] for hand in sorted_hands]

    winnings = 0
    for i, hand in enumerate(sorted_hands[::-1]):
        winnings += (i + 1) * hand[1]

    assert sorted_hands_strings == [
        "KTJJT",
        "QQQJA",
        "T55J5",
        "KK677",
        "32T3K",
    ]
    assert winnings == 5905

def test_hands_sorter_sort_with_jokers_reddit(example_hands_list_text_reddit):
    hands = parse_hands_list(example_hands_list_text_reddit)

    sorter = HandsSorter(hands, j_is_joker=True)
    sorted_hands = sorter.sort(
        untie_func=partial(hand_cmp_by_first_difference, j_is_lowest=True)
    )
    sorted_hands_strings = [hand[0] for hand in sorted_hands]

    winnings = 0
    for i, hand in enumerate(sorted_hands):
        winnings += (i + 1) * hand[1]

    assert sorted_hands_strings == [
        "2345A",
        "J345A",
        "2345J",
        "32T3K",
        "KK677",
        "T3Q33",
        "Q2KJJ",
        "T3T3J",
        "Q2Q2Q",
        "2AAAA",
        "T55J5",
        "QQQJA",
        "KTJJT",
        "JJJJJ",
        "JJJJ2",
        "JAAAA",
        "2JJJJ",
        "AAAAJ",
        "AAAAA"
    ]
    assert winnings == 6839
