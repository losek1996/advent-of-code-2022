import re


type ValveWithFlowRate = dict[str, int]
type ValveWithNeighbors = dict[str, list[str]]


def parse_data(data: list[str]) -> tuple[ValveWithFlowRate, ValveWithNeighbors]:
    valve_with_flow_rate: ValveWithFlowRate = {}
    valve_with_neighbors: ValveWithNeighbors = {}
    for row in data:
        matched_coordinates = re.match(
            r"^Valve (.*?) has flow rate=(.*?); tunnels lead to valves (.*?)$", row
        )

        valve_id = matched_coordinates.group(1)
        flow_rate = int(matched_coordinates.group(2))
        valve_neighbors = [
            neighbor.strip() for neighbor in matched_coordinates.group(3).split(",")
        ]

        valve_with_flow_rate[valve_id] = flow_rate
        valve_with_neighbors[valve_id] = valve_neighbors

    return valve_with_flow_rate, valve_with_neighbors
