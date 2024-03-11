'''https://adventofcode.com/2023/day/5'''

# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring

from collections import defaultdict
from dataclasses import dataclass
import sys
import re
from typing import Self

@dataclass(unsafe_hash=True)
class AlmanacMapRange:
    destination_start: int
    source_start: int
    length: int

    def __post_init__(self):
        self.source_end = self.source_start + self.length - 1

    def get_destination(self, source: int) -> int | None:
        if not self.source_start <= source <= self.source_end:
            return None
        offset = source - self.source_start
        return self.destination_start + offset

class Almanac:

    def __init__(
        self,
        seeds: tuple[int, ...],
        maps: dict[tuple[str, str], tuple[AlmanacMapRange, ...]]
    ):
        self.seeds = seeds
        self.maps = maps

    def convert_unit(
        self, source_value: int, source_type: str, destination_type: str
    ) -> int:
        conversion_map = self.maps.get((source_type, destination_type))
        if not conversion_map:
            raise ValueError(
                f'Cannot convert from {source_type=} to {destination_type=}'
            )
        for conversion_range in conversion_map:
            destination = conversion_range.get_destination(source_value)
            if destination is not None:
                return destination
        return source_value

    def convert_unit_range(
        self, source_range: range, source_type: str, destination_type: str
    ) -> tuple[range, ...]:

        if source_range.step != 1:
            raise ValueError('Only 1 step ranges allowed!')

        conversion_map = self.maps.get((source_type, destination_type))
        if conversion_map is None:
            raise ValueError(
                f'Cannot convert from {source_type=} to {destination_type=}'
            )

        split_points = set()
        for conversion_range in conversion_map:
            if (
                start := conversion_range.source_start
            ) in source_range:
                split_points.add(start)
            if (
                next_start := conversion_range.source_start + conversion_range.length
            ) in source_range:
                split_points.add(next_start)
        split_points.add(source_range.start)
        split_points.add(source_range.stop)

        result_ranges = []
        sorted_split_points = sorted(split_points)
        for index, _ in enumerate(sorted_split_points[:-1]):
            start = self.convert_unit(
                sorted_split_points[index], source_type, destination_type
            )
            end = self.convert_unit(
                sorted_split_points[index+1] - 1, source_type, destination_type
            ) + 1

            result_ranges.append(range(start, end))

        return tuple(result_ranges)

    def find_seed_location_ranges(
        self, seed_range: range
    ) -> tuple[range, ...]:

        conversions = (
            ('seed', 'soil'),
            ('soil', 'fertilizer'),
            ('fertilizer', 'water'),
            ('water', 'light'),
            ('light', 'temperature'),
            ('temperature', 'humidity'),
            ('humidity', 'location'),
        )

        ranges = [seed_range]
        for conversion in conversions:
            new_ranges = []
            for previous_range in ranges:
                new_ranges.extend(self.convert_unit_range(
                    previous_range, conversion[0], conversion[1]
                ))
            ranges = new_ranges

        return tuple(ranges)

    def find_seed_location(self, seed: int) -> int:

        soil = self.convert_unit(seed, 'seed', 'soil')
        fertilizer = self.convert_unit(soil, 'soil', 'fertilizer')
        water = self.convert_unit(fertilizer, 'fertilizer', 'water')
        light = self.convert_unit(water, 'water', 'light')
        temperature = self.convert_unit(light, 'light', 'temperature')
        humidity = self.convert_unit(temperature, 'temperature', 'humidity')
        location = self.convert_unit(humidity, 'humidity', 'location')
        return location

    @classmethod
    def from_string(cls, almanac_text: str) -> Self:
        text_parts = almanac_text.split('\n\n')
        seeds = tuple()
        maps = defaultdict(list)
        for part in text_parts:

            if 'seeds:' in part:
                seed_numbers = part.split(':')[1].strip()
                seeds = tuple(
                    int(number) for number in re.findall(r'\d+', seed_numbers)
                )
                continue

            part_lines = tuple(line.strip() for line in part.splitlines())
            title_match = re.match(r'(.+)-to-(.+) map:', part_lines[0])
            if not title_match:
                continue
            map_key = (title_match.group(1), title_match.group(2))

            for range_line in part_lines[1:]:
                range_numbers = (
                    int(number) for number in re.findall(r'\d+', range_line)
                )
                maps[map_key].append(AlmanacMapRange(*range_numbers))

        return cls(
            seeds=seeds,
            maps = {k: tuple(v) for k, v in maps.items()}
        )

def main(input_text: str):
    almanac = Almanac.from_string(input_text)
    locations = [almanac.find_seed_location(seed) for seed in almanac.seeds]
    print(f'Solution part 1: {min(locations)}')

    results = []
    seed_pairs = tuple(zip(*([iter(almanac.seeds)] * 2)))
    for seed_pair in seed_pairs:
        seed_range = range(seed_pair[0], seed_pair[0] + seed_pair[1])
        results.extend(almanac.find_seed_location_ranges(seed_range))
    second_locations_min = min(result.start for result in results)
    print(f'Solution part 2: {second_locations_min}')

if __name__ == "__main__":
    INPUT_TEXT = sys.stdin.read()
    main(INPUT_TEXT)
