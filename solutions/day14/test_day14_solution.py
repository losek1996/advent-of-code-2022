import os

import pytest

from solutions.day14.day14_solution import (
    parse_segments,
    Data,
    parse_data,
    produce_and_count_units_of_sand,
)
from solutions.read_data import read_raw_data_without_spaces


DATA_DIR = os.path.dirname(os.path.realpath(__file__)) + "/data/"


@pytest.fixture
def data(request) -> list[str]:
    return read_raw_data_without_spaces(DATA_DIR + request.param)


@pytest.fixture
def parsed_data(request) -> Data:
    data = read_raw_data_without_spaces(DATA_DIR + request.param)
    return parse_data(data)


@pytest.mark.parametrize(
    "data, expected_num_of_segments", [("test_data.txt", 5)], indirect=["data"]
)
def test_parse_segments(data: list[str], expected_num_of_segments: int):
    assert len(parse_segments(data)) == expected_num_of_segments


@pytest.mark.parametrize(
    "parsed_data, , floor_exists, expected_units_of_sand",
    [("test_data.txt", False, 24), ("test_data.txt", True, 93)],
    indirect=["parsed_data"],
)
def test_produce_and_count_units_of_sand(
    parsed_data: Data, floor_exists: bool, expected_units_of_sand: int
):
    assert (
        produce_and_count_units_of_sand(parsed_data, floor_exists)
        == expected_units_of_sand
    )
