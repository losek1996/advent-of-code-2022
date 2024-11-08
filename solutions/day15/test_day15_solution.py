import os

import pytest

from solutions.day15 import day15_solution
from solutions.day15.day15_solution import (
    parse_data,
    Sensor,
    Point,
    count_positions_where_beacon_can_not_be_present,
    generate_beacon_candidate_positions,
    get_tuning_frequency_of_position_where_beacon_can_be_present,
    get_sensors_not_covered_by_another_sensors,
)
from solutions.read_data import read_raw_data_without_spaces


DATA_DIR = os.path.dirname(os.path.realpath(__file__)) + "/data/"


@pytest.fixture
def parsed_data(request) -> list[Sensor]:
    data = read_raw_data_without_spaces(DATA_DIR + request.param)
    return parse_data(data)


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


def test_parse_data():
    assert parse_data(
        ["Sensor at x=1458348, y=2739442: closest beacon is at x=1581951, y=2271709"]
    ) == [Sensor(coordinates=(1458348, 2739442), nearest_beacon=(1581951, 2271709))]


@pytest.mark.parametrize(
    "sensor, expected_positions",
    [
        (
            Sensor(coordinates=(1, 1), nearest_beacon=(2, 2)),
            {
                (0, 3),
                (1, 4),
                (2, 3),
                (3, 2),
                (4, 1),
                (3, 0),
            },
        )
    ],
)
def test_generate_beacon_candidate_positions(
    sensor: Sensor, expected_positions: list[Point]
):
    positions = generate_beacon_candidate_positions(sensor)
    assert set(positions) == expected_positions


@pytest.mark.parametrize(
    "parsed_data, expected_tuning_frequency",
    [("test_data.txt", 56000011)],
    indirect=["parsed_data"],
)
def test_get_tuning_frequency_of_position_where_beacon_can_be_present(
    parsed_data: list[Sensor], expected_tuning_frequency: int
):
    day15_solution.MAX_COORDINATE_VALUE = 20
    sensors = get_sensors_not_covered_by_another_sensors(parsed_data)
    tuning_frequency = get_tuning_frequency_of_position_where_beacon_can_be_present(
        sensors
    )
    assert tuning_frequency == expected_tuning_frequency
