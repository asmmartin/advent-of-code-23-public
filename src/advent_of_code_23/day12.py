'''https://adventofcode.com/2023/day/12'''

# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring

import sys
from functools import cache

OPERATIONAL = '.'
DAMAGED = '#'
UNKNOWN = '?'

def find_arrangements(
    configuration: str,
    damaged_to_find: tuple[int, ...],
    cursor: int = 0,
    damaged_cursor: int = 0
) -> set[str]:

    arrangements = set()

    while cursor < len(configuration) and damaged_cursor < len(damaged_to_find):

        if configuration[cursor] == OPERATIONAL:
            cursor += 1
            continue

        if configuration[cursor] == UNKNOWN:
            arrangements.update(find_arrangements(
                configuration[:cursor] + '.' + configuration[cursor + 1:],
                damaged_to_find,
                cursor=cursor+1,
                damaged_cursor=damaged_cursor
            ))

        end = cursor + damaged_to_find[damaged_cursor]
        if end > len(configuration):
            break
        if end < len(configuration) and configuration[end] == DAMAGED:
            break
        if OPERATIONAL in configuration[cursor:end]:
            break

        configuration = (
            configuration[:cursor] +
            DAMAGED * (end - cursor) +
            (OPERATIONAL if end < len(configuration) else '') +
            configuration[end + 1:]
        )

        damaged_cursor += 1
        cursor = end + 1
    else:
        if (
            damaged_cursor == len(damaged_to_find) and
            DAMAGED not in configuration[cursor:]
        ):
            configuration = (
                configuration[:cursor] +
                configuration[cursor:].replace(UNKNOWN, OPERATIONAL)
            )
            arrangements.add(configuration)

    return arrangements

@cache
def count_arrangements(
    configuration: str, damaged_to_find: tuple[int, ...]
) -> int:
    """Recursively count how many possible configurations are there in"""

    count = 0

    if damaged_to_find:
        if not configuration:
            return 0
    else:
        if not configuration:
            return 1
        return DAMAGED not in configuration

    if configuration[0] in (OPERATIONAL, UNKNOWN):
        count += count_arrangements(configuration[1:], damaged_to_find)

    if configuration[0] in (DAMAGED, UNKNOWN):
        block_length = damaged_to_find[0]
        if block_length > len(configuration):
            pass
        elif OPERATIONAL in configuration[:block_length]:
            pass
        elif configuration[block_length:][:1] != DAMAGED:
            count += count_arrangements(
                configuration[block_length + 1:], damaged_to_find[1:]
            )

    return count

def main(input_text: str):

    all_arrangements = []
    for line in input_text.strip().splitlines():
        configuration, nums = line.split()
        damaged = tuple(int(num) for num in nums.split(','))
        arrangements = find_arrangements(configuration, damaged)
        all_arrangements.append(arrangements)
    total_arrangements_count = sum(
        len(arrangements) for arrangements in all_arrangements
    )
    print(f'Solution part 1: {total_arrangements_count}')

    arrangements_counts = []
    for line in input_text.strip().splitlines():
        configuration, nums = line.split()
        configuration = '?'.join([configuration]*5)
        damaged = tuple(int(num) for num in nums.split(',')) * 5
        arrangements_count = count_arrangements(configuration, damaged)
        arrangements_counts.append(arrangements_count)
    total_count = sum(arrangements_counts)
    print(f'Solution part 2: {total_count}')

if __name__ == "__main__":
    INPUT_TEXT = sys.stdin.read()
    main(INPUT_TEXT)
