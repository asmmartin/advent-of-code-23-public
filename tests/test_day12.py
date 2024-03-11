# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring

from advent_of_code_23.day12 import find_arrangements, count_arrangements

def test_find_arrangements_plain():

    configuration = '#.#.###'
    damaged = (1, 1, 3)

    arrangements = find_arrangements(configuration, damaged)

    assert arrangements == set((configuration,))

def test_find_arrangements_plain_wrong():

    configuration = '#.#.##.'
    damaged = (1, 1, 3)

    arrangements = find_arrangements(configuration, damaged)

    assert arrangements == set()

def test_find_arrangements_plain_multiple():
    configurations = [
        "#.#.###" ,
        ".#...#....###.",
        ".#.###.#.######",
        "####.#...#...",
        "#....######..#####.",
        ".###.##....#"
    ]
    damaged_list = [
        (1, 1, 3),
        (1, 1, 3),
        (1, 3, 1, 6),
        (4, 1, 1),
        (1, 6, 5),
        (3, 2, 1),
    ]
    combinations = zip(configurations, damaged_list)

    for combination in combinations:
        arrangements = find_arrangements(*combination)
        assert arrangements == set((combination[0],))

def test_find_arrangements_with_unknowns_unique():

    configuration = '???.###'
    damaged = (1, 1, 3)

    arrangements = find_arrangements(configuration, damaged)

    assert arrangements == set(("#.#.###",))

def test_find_arrangements_with_unknowns_two_solutions():

    configuration = '.??..??...?##.'
    damaged = (1, 1, 3)

    arrangements = find_arrangements(configuration, damaged)

    assert arrangements == {
        '.#....#...###.',
        '.#...#....###.',
        '..#...#...###.',
        '..#..#....###.',
    }

def test_find_arrangements_example():
    text = (
        '???.### 1,1,3\n'
        '.??..??...?##. 1,1,3\n'
        '?#?#?#?#?#?#?#? 1,3,1,6\n'
        '????.#...#... 4,1,1\n'
        '????.######..#####. 1,6,5\n'
        '?###???????? 3,2,1'
    )

    all_arrangements = []
    for line in text.strip().splitlines():
        configuration, nums = line.split()
        damaged = tuple(int(num) for num in nums.split(','))
        all_arrangements.append(find_arrangements(configuration, damaged))

    assert [len(arrangements) for arrangements in all_arrangements] == [
        1, 4, 1, 1, 4, 10
    ]

def test_count_arrangements_example_unfolding():
    text = (
        '???.### 1,1,3\n'
        '.??..??...?##. 1,1,3\n'
        '?#?#?#?#?#?#?#? 1,3,1,6\n'
        '????.#...#... 4,1,1\n'
        '????.######..#####. 1,6,5\n'
        '?###???????? 3,2,1'
    )

    arrangements_counts = []
    for line in text.strip().splitlines():
        configuration, nums = line.split()
        configuration = '?'.join([configuration]*5)
        damaged = tuple(int(num) for num in nums.split(',')) * 5
        count = count_arrangements(configuration, damaged)
        assert count == len(find_arrangements(configuration, damaged))
        arrangements_counts.append(count)

    assert sum(arrangements_counts) == 525152
