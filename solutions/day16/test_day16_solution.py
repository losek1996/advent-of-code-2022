import os

import pytest

from solutions.day16.day16_solution import (
    parse_data,
    ValveWithFlowRate,
    ValveWithNeighbors,
    Path,
    get_shortest_paths_between_all_nodes,
    Node,
    get_most_pressure_possible_to_release,
    MAX_NUMBER_OF_CONSIDERED_PATHS,
    PATH_LENGTH,
    START_NODE,
)
from solutions.read_data import read_raw_data_without_spaces


DATA_DIR = os.path.dirname(os.path.realpath(__file__)) + "/data/"


@pytest.fixture
def parsed_data(request) -> tuple[ValveWithFlowRate, ValveWithNeighbors]:
    data = read_raw_data_without_spaces(DATA_DIR + request.param)
    return parse_data(data)


def test_parse_data():
    assert parse_data(["Valve FR has flow rate=0; tunnels lead to valves JQ, GS"]) == (
        {"FR": 0},
        {"FR": ["JQ", "GS"]},
    )


@pytest.mark.parametrize(
    "parsed_data, nodes_to_include_in_output, expected_shortest_paths_length, expected_shortest_paths_for_start_node",
    [
        (
            "test_data.txt",
            ["AA", "BB", "CC", "DD", "EE", "HH", "JJ"],
            42,
            {
                "AA_BB": 1,
                "AA_CC": 2,
                "AA_DD": 1,
                "AA_EE": 2,
                "AA_HH": 5,
                "AA_JJ": 2,
            },
        )
    ],
    indirect=["parsed_data"],
)
def test_get_shortest_paths_between_all_nodes__returns_shortest_paths_between_all_nodes(
    parsed_data: tuple[ValveWithFlowRate, ValveWithNeighbors],
    nodes_to_include_in_output: list[Node],
    expected_shortest_paths_length: int,
    expected_shortest_paths_for_start_node: dict[Path, int],
):
    _, valve_with_neighbors = parsed_data
    shortest_paths = get_shortest_paths_between_all_nodes(
        valve_with_neighbors, nodes_to_include_in_output
    )
    assert len(shortest_paths) == expected_shortest_paths_length
    for (
        path,
        expected_shortest_path_length,
    ) in expected_shortest_paths_for_start_node.items():
        assert shortest_paths[path] == expected_shortest_path_length


@pytest.mark.parametrize(
    "parsed_data, start_node, path_length, max_number_of_considered_paths, expected_released_pressure",
    [("test_data.txt", START_NODE, PATH_LENGTH - 1, MAX_NUMBER_OF_CONSIDERED_PATHS, 1651)],
    indirect=["parsed_data"],
)
def test_get_most_pressure_possible_to_release_releases_max_possible_pressure(
    parsed_data: tuple[ValveWithFlowRate, ValveWithNeighbors],
    start_node: Node,
    path_length: int,
    max_number_of_considered_paths: int,
    expected_released_pressure: int,
):
    valve_with_flow_rate, valve_with_neighbors = parsed_data
    assert (
        get_most_pressure_possible_to_release(
            start_node,
            valve_with_neighbors,
            valve_with_flow_rate,
            path_length=path_length,
            max_number_of_considered_paths=max_number_of_considered_paths,
        )
        == expected_released_pressure
    )
