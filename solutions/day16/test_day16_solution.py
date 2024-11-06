from solutions.day16.day16_solution import parse_data


def test_parse_data():
    assert parse_data(["Valve FR has flow rate=0; tunnels lead to valves JQ, GS"]) == (
        {"FR": 0},
        {"FR": ["JQ", "GS"]},
    )
