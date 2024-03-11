# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring

from advent_of_code_23.day01 import read_calibration_value

def test_read_calibration_value():
    assert read_calibration_value("1abc2") == 12
    assert read_calibration_value("pqr3stu8vwx") == 38
    assert read_calibration_value("a1b2c3d4e5f") == 15
    assert read_calibration_value("treb7uchet") == 77

def test_read_calibration_value_with_letters():
    assert read_calibration_value("two1nine") == 29
    assert read_calibration_value("eightwothree") == 83
    assert read_calibration_value("abcone2threexyz") == 13
    assert read_calibration_value("xtwone3four") == 24
    assert read_calibration_value("4nineeightseven2") == 42
    assert read_calibration_value("zoneight234") == 14
    assert read_calibration_value("7pqrstsixteen") == 76
