# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring

import pytest

from advent_of_code_23.day15 import hash_text, Box, Lens, BoxArray

@pytest.fixture(name='example_sequence')
def example_sequence_fixture():
    return 'rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7'

def test_hash_sequence(example_sequence):

    sequence = example_sequence.strip().replace('\n', '')

    hashes = [hash_text(step) for step in sequence.split(',')]

    assert hashes == [
        30, 253, 97, 47, 14, 180, 9, 197, 48, 214, 231
    ]

def test_box():

    box = Box(box_id=0, lenses=[Lens('rn', 1), Lens('cm', 2)])

    assert box.box_id == 0
    assert box.lenses[0].label == 'rn'
    assert box.lenses[0].focal_length == 1
    assert box.lenses[1].label == 'cm'
    assert box.lenses[1].focal_length == 2
    assert box.focusing_powers == (1, 4)

def test_box_array():

    array = BoxArray()

    assert len(array.boxes) == 256

def test_box_array_process_step(example_sequence):

    array = BoxArray()

    for step in example_sequence.split(','):
        array.process_step(step)

    assert array.boxes[0].focusing_powers == (1, 4)
    assert array.boxes[3].focusing_powers == (28, 40, 72)

    total_focusing_power = sum(
        sum(box.focusing_powers)
        for box in array.boxes.values()
    )

    assert total_focusing_power == 145
