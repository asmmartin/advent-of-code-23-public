# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring

import pytest

from advent_of_code_23.day22 import Brick, Tower

@pytest.fixture(name='example_bricks_text')
def example_bricks_text_fixture():
    return (
        '1,0,1~1,2,1\n'
        '0,0,2~2,0,2\n'
        '0,2,3~2,2,3\n'
        '0,0,4~0,2,4\n'
        '2,0,5~2,2,5\n'
        '0,1,6~2,1,6\n'
        '1,1,8~1,1,9'
    )

@pytest.fixture(name='example_bricks')
def example_bricks_fixture(example_bricks_text):

    lines = example_bricks_text.strip().splitlines()
    bricks = [Brick.from_string(line) for line in lines]
    for letter, brick in zip('ABCDEFG', bricks):
        brick.brick_id = letter
    return bricks

def test_brick(example_bricks_text):

    lines = example_bricks_text.strip().splitlines()

    bricks = [Brick.from_string(line) for line in lines]

    assert [brick.brick_id for brick in bricks]
    for letter, brick in zip('ABCDEFG', bricks):
        brick.brick_id = letter

    assert bricks[0].coords == ([1, 0, 1], [1, 2, 1])
    assert bricks[1].coords == ([0, 0, 2], [2, 0, 2])

    assert bricks[0].footprint == {(1, 0), (1, 1),(1, 2)}
    assert bricks[1].footprint == {(0, 0), (1, 0), (2, 0)}
    assert bricks[2].footprint == {(0, 2), (1, 2), (2, 2)}
    assert bricks[-1].footprint == {(1, 1)}

    assert bricks[0].height == 1
    assert bricks[1].height == 1
    assert bricks[-1].height == 2

    for brick in bricks:
        assert brick.is_support_of == set()
        assert brick.is_supported_by == set()

def test_tower(example_bricks):

    tower = Tower(example_bricks)

    assert len(tower.bricks) == len(example_bricks)
    assert set(tower.bricks.keys()) == set('ABCDEFG')

def test_tower_drop_bricks(example_bricks):

    tower = Tower(example_bricks)

    tower.drop_bricks()

    assert tower.bricks['A'].base_height == 1
    assert tower.bricks['A'].is_supported_by == {'FLOOR'}
    assert tower.bricks['A'].is_support_of == {'B', 'C'}

    assert tower.bricks['B'].base_height == 2
    assert tower.bricks['B'].is_supported_by == {'A'}
    assert tower.bricks['B'].is_support_of == {'D', 'E'}

    assert tower.bricks['C'].base_height == 2
    assert tower.bricks['C'].is_supported_by == {'A'}
    assert tower.bricks['C'].is_support_of == {'D', 'E'}

    assert tower.bricks['D'].base_height == 3
    assert tower.bricks['D'].is_supported_by == {'B', 'C'}
    assert tower.bricks['D'].is_support_of == {'F'}

    assert tower.bricks['E'].base_height == 3
    assert tower.bricks['E'].is_supported_by == {'B', 'C'}
    assert tower.bricks['E'].is_support_of == {'F'}

    assert tower.bricks['F'].base_height == 4
    assert tower.bricks['F'].is_supported_by == {'D', 'E'}
    assert tower.bricks['F'].is_support_of == {'G'}

    assert tower.bricks['G'].base_height == 5
    assert tower.bricks['G'].is_supported_by == {'F'}
    assert tower.bricks['G'].is_support_of == set()

def test_tower_get_safely_desintegrable_brick_ids(example_bricks):

    tower = Tower(bricks=example_bricks)
    tower.drop_bricks()

    desintegrable = tower.get_safely_desintegrable_brick_ids()

    assert desintegrable == set('BCDEG')

def test_tower_get_dropping_bricks_if_desintegrate(example_bricks):

    tower = Tower(bricks=example_bricks)
    tower.drop_bricks()

    would_drop = tower.get_dropping_bricks_if_desintegrate('A')
    assert len(would_drop) == 6

    would_drop = tower.get_dropping_bricks_if_desintegrate('F')
    assert len(would_drop) == 1

    assert not tower.get_dropping_bricks_if_desintegrate('B')
    assert not tower.get_dropping_bricks_if_desintegrate('C')
    assert not tower.get_dropping_bricks_if_desintegrate('D')
    assert not tower.get_dropping_bricks_if_desintegrate('E')
    assert not tower.get_dropping_bricks_if_desintegrate('G')
