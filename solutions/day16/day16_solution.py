import re
from collections import deque
from itertools import permutations
from random import shuffle

type ValveWithFlowRate = dict[str, int]
type ValveWithNeighbors = dict[str, list[str]]
type Path = str  # if we have nodes A and B, path between A and B will be `A_B`
type Node = str  # e.g. if we have node A, it will be A

TIME_TO_OPEN_VALVE = 1
TIME_TO_VOLCANO_ERUPTION = 30
MAX_NUMBER_OF_CONSIDERED_PATHS = 5 * 10**6
PATH_LENGTH = 6  # how many nodes will be included in path
START_NODE = "AA"


def parse_data(data: list[str]) -> tuple[ValveWithFlowRate, ValveWithNeighbors]:
    valve_with_flow_rate: ValveWithFlowRate = {}
    valve_with_neighbors: ValveWithNeighbors = {}
    for row in data:
        matched_input_data = re.match(
            r"^Valve (.*?) has flow rate=(.*?); tunnels? leads? to valves? (.*?)$", row
        )

        valve_id = matched_input_data.group(1)
        flow_rate = int(matched_input_data.group(2))
        valve_neighbors = [
            neighbor.strip() for neighbor in matched_input_data.group(3).split(",")
        ]

        valve_with_flow_rate[valve_id] = flow_rate
        valve_with_neighbors[valve_id] = valve_neighbors

    return valve_with_flow_rate, valve_with_neighbors


def get_most_pressure_possible_to_release(
    start_node: Node,
    valve_with_neighbors: ValveWithNeighbors,
    valve_with_flow_rate: ValveWithFlowRate,
    path_length: int,
    max_number_of_considered_paths: int,
):
    nodes_to_include_in_output = [start_node] + get_all_nodes_with_non_zero_flow_rate(
        valve_with_flow_rate
    )
    shortest_paths = get_shortest_paths_between_all_nodes(
        valve_with_neighbors, nodes_to_include_in_output
    )
    valves_paths_permutations = generate_all_valves_paths_permutations(
        nodes_to_visit=nodes_to_include_in_output, path_length=path_length
    )

    max_released_pressure = 0
    shuffle(valves_paths_permutations)
    for path in valves_paths_permutations[
        :max_number_of_considered_paths
    ]:  # probabilistic approach if search space is too big
        released_pressure = get_released_pressure_for_path(
            path,
            shortest_paths,
            valve_with_flow_rate,
            TIME_TO_VOLCANO_ERUPTION,
            TIME_TO_OPEN_VALVE,
        )
        if released_pressure > max_released_pressure:
            max_released_pressure = released_pressure
    return max_released_pressure


def get_released_pressure_for_path(
    full_path: list[Node],
    shortest_paths_between_nodes: dict[Path, int],
    valve_with_flow_rate: ValveWithFlowRate,
    time_to_volcano_eruption: int,
    time_to_open_valve: int,
) -> int:
    """I assume start node has no pressure to release."""
    released_pressure = 0
    previous_node = full_path[0]

    for current_node in full_path[1:]:
        if valve_with_flow_rate == 0:
            return released_pressure
        path = generate_path(previous_node, current_node)
        time_to_reach_next_node = shortest_paths_between_nodes[path]
        if is_enough_time_to_release_pressure_from_valve(
            time_to_volcano_eruption, time_to_reach_next_node, time_to_open_valve
        ):
            time_to_volcano_eruption -= time_to_reach_next_node + time_to_open_valve
            released_pressure += (
                valve_with_flow_rate[current_node] * time_to_volcano_eruption
            )
            previous_node = current_node

    return released_pressure


def get_shortest_paths_between_all_nodes(
    valve_with_neighbors: ValveWithNeighbors, nodes_to_include_in_output: list[Node]
) -> dict[Path, int]:
    """Only nodes with non-zero flow rate are must-visit nodes as in those nodes we can release pressure."""
    shortest_paths: dict[Path, int] = {}
    for node_to_visit in nodes_to_include_in_output:
        shortest_paths_for_node = get_shortest_distance_to_all_nodes(
            start_node=node_to_visit,
            valve_with_neighbors=valve_with_neighbors,
            nodes_to_include_in_output=nodes_to_include_in_output,
        )
        shortest_paths.update(shortest_paths_for_node)

    return shortest_paths


def get_shortest_distance_to_all_nodes(
    start_node: Node,
    valve_with_neighbors: ValveWithNeighbors,
    nodes_to_include_in_output: list[str],
) -> dict[Node, int]:
    shortest_paths: dict[Path, int] = {}
    visited_nodes: set[Node] = set()
    nodes_to_visit: deque[tuple[Node, int]] = deque([(start_node, 0)])

    while nodes_to_visit:
        current_node, distance = nodes_to_visit.popleft()
        visited_nodes.add(current_node)
        distance += 1

        for neighbor in valve_with_neighbors[current_node]:
            if neighbor in visited_nodes:
                continue
            if neighbor in nodes_to_include_in_output:
                path = generate_path(start_node, neighbor)
                shortest_paths[path] = distance
            nodes_to_visit.append((neighbor, distance))

    return shortest_paths


def get_all_nodes_with_non_zero_flow_rate(
    valve_with_flow_rate: ValveWithFlowRate,
) -> list[Node]:
    nodes_with_non_zero_flow_rate: list[Node] = []
    for valve_id, flow_rate in valve_with_flow_rate.items():
        if flow_rate > 0:
            nodes_with_non_zero_flow_rate.append(valve_id)

    return nodes_with_non_zero_flow_rate


def generate_all_valves_paths_permutations(
    nodes_to_visit: list[Node], path_length: int
) -> list[list[Node]]:
    start_node = nodes_to_visit[0]
    return [
        [start_node] + list(path)
        for path in permutations(nodes_to_visit[1:], path_length)
    ]


def generate_path(node_a: Node, node_b: Node) -> Path:
    return f"{node_a}_{node_b}"


def is_enough_time_to_release_pressure_from_valve(
    time_to_volcano_eruption: int, time_to_reach_next_node: int, time_to_open_valve: int
):
    return (time_to_volcano_eruption - time_to_reach_next_node - time_to_open_valve) > 0
