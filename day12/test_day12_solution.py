import os

import pytest

from day12.day12_solution import (
    HeightMap,
    parse_data,
    find_shortest_path_length,
    find_shortest_path_from_any_point_with_elevation_a,
)
from read_data import read_raw_data_without_spaces


DATA_DIR = os.path.dirname(os.path.realpath(__file__)) + "/data/"


@pytest.fixture
def height_map(request) -> HeightMap:
    data = read_raw_data_without_spaces(DATA_DIR + request.param)
    return parse_data(data)


@pytest.mark.parametrize("height_map", ["test_data.txt"], indirect=True)
def test_find_shortest_path_length(height_map):
    assert find_shortest_path_length(height_map) == 31


@pytest.mark.parametrize("height_map", ["test_data.txt"], indirect=True)
def test_find_shortest_path_from_any_point_with_elevation_a(height_map):
    assert find_shortest_path_from_any_point_with_elevation_a(height_map) == 29
