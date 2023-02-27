import os

import pytest

from solutions.day15.day15_solution import (
    parse_data,
    Sensor,
    Point,
    count_positions_where_beacon_can_not_be_present,
)
from solutions.read_data import read_raw_data_without_spaces


DATA_DIR = os.path.dirname(os.path.realpath(__file__)) + "/data/"


@pytest.fixture
def parsed_data(request) -> list[Sensor]:
    data = read_raw_data_without_spaces(DATA_DIR + request.param)
    return parse_data(data)


def test_parse_data():
    assert parse_data(
        ["Sensor at x=1458348, y=2739442: closest beacon is at x=1581951, y=2271709"]
    ) == [
        Sensor(
            coordinates=Point(x=1458348, y=2739442),
            nearest_beacon=Point(
                x=1581951,
                y=2271709,
            ),
            distance_from_nearest_beacon=591336,
        )
    ]


@pytest.mark.parametrize(
    "parsed_data, target_y, expected_result",
    [("test_data.txt", 10, 26)],
    indirect=["parsed_data"],
)
def test_count_positions_where_beacon_can_not_be_present(
    parsed_data: list[Sensor], target_y: int, expected_result: int
):
    assert (
        count_positions_where_beacon_can_not_be_present(
            sensors=parsed_data, target_y=target_y
        )
        == expected_result
    )
