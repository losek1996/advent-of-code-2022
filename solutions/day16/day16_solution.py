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
MAX_NUMBER_OF_CONSIDERED_PATHS = 33 * 10**6
PATH_LENGTH = 7  # how many nodes will be included in path
START_NODE = "AA"
MAX_NUMBER_OF_CONSIDERED_NODES = 16
MINIMUM_PRESSURE_RELEASED_FOR_FIRST_PATH = 500  # when we have 2 parallel paths first path is included when releases pressure above threshold


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
    max_number_of_considered_nodes: int,
    time_to_volcano_eruption: int,
    two_parallel_paths_allowed: bool,
    second_path_length: int | None,
):
    """
    I implemented brute force where it's possible to reduce search space using multiple parameters like:
    max_number_of_considered_nodes -> to limit search to only most profitable nodes
    max_number_of_considered_paths -> probabilistic approach where not all paths are considered
    path_length -> it searches only paths with given length
    """
    nodes_to_include_in_output = [start_node] + get_top_n_nodes_with_highest_flow_rate(
        valve_with_flow_rate,
        max_number_of_considered_nodes,
        start_node_to_exclude=start_node,
    )
    shortest_paths = get_shortest_paths_between_all_nodes(
        valve_with_neighbors, nodes_to_include_in_output
    )

    if two_parallel_paths_allowed:
        valves_paths_permutations = generate_2_parallel_valves_paths_permutations(
            nodes_to_visit=nodes_to_include_in_output,
            first_path_length=path_length,
            second_path_length=second_path_length,
            shortest_paths_between_nodes=shortest_paths,
            valve_with_flow_rate=valve_with_flow_rate,
            minimum_pressure_released_for_first_path=MINIMUM_PRESSURE_RELEASED_FOR_FIRST_PATH,
        )
        return _get_max_released_pressure_for_2_parallel_paths(
            max_number_of_considered_paths,
            shortest_paths,
            valve_with_flow_rate,
            valves_paths_permutations,
            time_to_volcano_eruption,
        )

    valves_paths_permutations = generate_valves_paths_permutations(
        nodes_to_visit=nodes_to_include_in_output, path_length=path_length
    )

    return _get_max_released_pressure(
        max_number_of_considered_paths,
        shortest_paths,
        valve_with_flow_rate,
        valves_paths_permutations,
        time_to_volcano_eruption,
    )


def _get_max_released_pressure(
    max_number_of_considered_paths: int,
    shortest_paths: dict[Path, int],
    valve_with_flow_rate: dict[Node, int],
    valves_paths_permutations: list[list[Node]],
    time_to_volcano_eruption: int,
) -> int:
    max_released_pressure = 0
    shuffle(valves_paths_permutations)
    for path in valves_paths_permutations[
        :max_number_of_considered_paths
    ]:  # probabilistic approach if search space is too big
        released_pressure = get_released_pressure_for_path(
            path,
            shortest_paths,
            valve_with_flow_rate,
            time_to_volcano_eruption,
            TIME_TO_OPEN_VALVE,
        )
        if released_pressure > max_released_pressure:
            max_released_pressure = released_pressure
    return max_released_pressure


def _get_max_released_pressure_for_2_parallel_paths(
    max_number_of_considered_paths: int,
    shortest_paths: dict[Path, int],
    valve_with_flow_rate: dict[Node, int],
    valves_paths_permutations: list[tuple[list[Node], list[Node]]],
    time_to_volcano_eruption: int,
):
    max_released_pressure = 0
    shuffle(valves_paths_permutations)
    for first_path, second_path in valves_paths_permutations[
        :max_number_of_considered_paths
    ]:  # probabilistic approach if search space is too big
        released_pressure = 0
        for path in [first_path, second_path]:
            released_pressure += get_released_pressure_for_path(
                path,
                shortest_paths,
                valve_with_flow_rate,
                time_to_volcano_eruption,
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


def get_top_n_nodes_with_highest_flow_rate(
    valve_with_flow_rate: ValveWithFlowRate,
    max_number_of_nodes: int,
    start_node_to_exclude: Node,
) -> list[Node]:
    """We exclude node AA as it's start node and it's obligatory."""
    valve_with_flow_rate.pop(start_node_to_exclude)
    valve_with_flow_rate = sorted(
        valve_with_flow_rate.items(), key=lambda item: item[1], reverse=True
    )
    return [valve_id for valve_id, _ in valve_with_flow_rate[:max_number_of_nodes]]


def generate_valves_paths_permutations(
    nodes_to_visit: list[Node], path_length: int
) -> list[list[Node]]:
    start_node = nodes_to_visit[0]
    return [
        [start_node] + list(path)
        for path in permutations(nodes_to_visit[1:], path_length)
    ]


def generate_2_parallel_valves_paths_permutations(
    nodes_to_visit: list[Node],
    first_path_length: int,
    second_path_length: int,
    shortest_paths_between_nodes: dict[Path, int],
    valve_with_flow_rate: ValveWithFlowRate,
    minimum_pressure_released_for_first_path: int,
) -> list[tuple[list[Node], list[Node]]]:
    output_permutations = []
    first_path_permutations = generate_valves_paths_permutations(
        nodes_to_visit, first_path_length
    )

    for first_path in first_path_permutations:
        released_pressure = get_released_pressure_for_path(
            first_path, shortest_paths_between_nodes, valve_with_flow_rate, 26, 1
        )
        if (
            released_pressure < minimum_pressure_released_for_first_path
        ):  # we reduce search space as we assume both paths will reduce pressure by amount higher than minimum_pressure_released_for_first_path
            continue
        nodes_for_second_path = [
            node for node in nodes_to_visit if node not in first_path[1:]
        ]
        second_path_permutations = generate_valves_paths_permutations(
            nodes_for_second_path, second_path_length
        )
        for second_path in second_path_permutations:
            output_permutations.append((first_path, second_path))

    return output_permutations


def generate_path(node_a: Node, node_b: Node) -> Path:
    return f"{node_a}_{node_b}"


def is_enough_time_to_release_pressure_from_valve(
    time_to_volcano_eruption: int, time_to_reach_next_node: int, time_to_open_valve: int
):
    return (time_to_volcano_eruption - time_to_reach_next_node - time_to_open_valve) > 0
