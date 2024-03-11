# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring

import pytest

from advent_of_code_23.day05 import (
    AlmanacMapRange, Almanac
)

@pytest.fixture(name='almanac_text_example')
def almanac_text_example_fixture():
    return (
        "seeds: 79 14 55 13\n"
        "\n"
        "seed-to-soil map:\n"
        "50 98 2\n"
        "52 50 48\n"
        "\n"
        "soil-to-fertilizer map:\n"
        "0 15 37\n"
        "37 52 2\n"
        "39 0 15\n"
        "\n"
        "fertilizer-to-water map:\n"
        "49 53 8\n"
        "0 11 42\n"
        "42 0 7\n"
        "57 7 4\n"
        "\n"
        "water-to-light map:\n"
        "88 18 7\n"
        "18 25 70\n"
        "\n"
        "light-to-temperature map:\n"
        "45 77 23\n"
        "81 45 19\n"
        "68 64 13\n"
        "\n"
        "temperature-to-humidity map:\n"
        "0 69 1\n"
        "1 0 69\n"
        "\n"
        "humidity-to-location map:\n"
        "60 56 37\n"
        "56 93 4"
    )

def test_almanac_map_range():
    map_range_1 = AlmanacMapRange(
        destination_start=50, source_start=98, length=2
    )
    assert map_range_1.get_destination(98) == 50
    assert map_range_1.get_destination(99) == 51
    assert map_range_1.get_destination(100) is None


    map_range_2 = AlmanacMapRange(
        destination_start=52, source_start=50, length=48
    )
    assert map_range_2.get_destination(50) == 52
    assert map_range_2.get_destination(51) == 53
    assert map_range_2.get_destination(98) is None

def test_almanac_and_convert_unit():
    almanac = Almanac(
        seeds=(79, 14, 55, 13),
        maps={
            ('seed', 'soil'): (
                AlmanacMapRange(50, 98, 2),
                AlmanacMapRange(52, 50, 48)
            )
        }
    )

    soils = [
        almanac.convert_unit(
            source_value=almanac.seeds[i],
            source_type='seed',
            destination_type='soil'
        ) for i in range(4)
    ]

    assert soils == [81, 14, 57, 13]

def test_almanac_convert_unit_error():
    almanac = Almanac(
        seeds=(79, 14, 55, 13),
        maps={
            ('seed', 'soil'): (
                AlmanacMapRange(50, 98, 2),
                AlmanacMapRange(52, 50, 48)
            )
        }
    )
    with pytest.raises(ValueError):
        almanac.convert_unit(1, 'seed', 'location')

def test_almanac_from_string(almanac_text_example):
    almanac = Almanac.from_string(almanac_text_example)

    assert len(almanac.maps[('seed', 'soil')]) == 2
    assert len(almanac.maps[('soil', 'fertilizer')]) == 3
    assert len(almanac.maps[('fertilizer', 'water')]) == 4
    assert len(almanac.maps[('water', 'light')]) == 2
    assert len(almanac.maps[('light', 'temperature')]) == 3
    assert len(almanac.maps[('temperature', 'humidity')]) == 2
    assert len(almanac.maps[('humidity', 'location')]) == 2

def test_almanac_find_seed_location(almanac_text_example):

    almanac = Almanac.from_string(almanac_text_example)

    locations = [
        almanac.find_seed_location(seed=seed) for seed in almanac.seeds
    ]

    assert locations == [82, 43, 86, 35]

def test_almanac_convert_range_unit():

    almanac = Almanac(
        seeds=(0, 101),
        maps={
            ('seeds', 'soil'): (
                AlmanacMapRange(125, 25, 25),
                AlmanacMapRange(160, 60, 15),
            )
        }
    )
    seed_range = range(almanac.seeds[0], almanac.seeds[0] + almanac.seeds[1])

    soil_ranges = almanac.convert_unit_range(seed_range, 'seeds', 'soil')

    assert set(soil_ranges) == {
        range(0, 25), range(50, 60), range(75, 101), range(125, 150), range(160, 175)
    }

def test_almanac_find_seed_location_ranges(almanac_text_example):
    almanac = Almanac.from_string(almanac_text_example)
    seed_pairs = tuple(zip(*([iter(almanac.seeds)] * 2)))

    results = []
    for pair in seed_pairs:
        seed_range = range(pair[0], pair[0] + pair[1])
        results.extend(almanac.find_seed_location_ranges(seed_range))

    assert min(result_range.start for result_range in results) == 46
