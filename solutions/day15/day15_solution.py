import re

from pydantic import BaseModel


class Point(BaseModel):
    x: int
    y: int


class Sensor(BaseModel):
    coordinates: Point
    nearest_beacon: Point
    distance_from_nearest_beacon: int = 0


def count_positions_where_beacon_can_not_be_present(
    sensors: list[Sensor], target_y: int
) -> int:
    positions_list: list[list[int]] = [
        get_reachable_points_x_coordinate(
            source_point=sensor.coordinates,
            target_y=target_y,
            max_distance=sensor.distance_from_nearest_beacon,
        )
        for sensor in sensors
    ]

    beacons_positions = [
        sensor.nearest_beacon.x
        for sensor in sensors
        if sensor.nearest_beacon.y == target_y
    ]

    return len(
        set(
            [
                position
                for positions in positions_list
                for position in positions
                if position not in beacons_positions
            ]
        )
    )


def get_reachable_points_x_coordinate(
    source_point: Point, target_y: int, max_distance: int
) -> list[int]:
    max_distance -= abs(target_y - source_point.y)
    if max_distance < 0:
        return []

    return [
        i
        for i in range(
            -max_distance + source_point.x, max_distance + source_point.x + 1
        )
    ]


def parse_data(data: list[str]) -> list[Sensor]:
    sensors = []
    for row in data:
        matched_coordinates = re.match(
            r"^Sensor at x=(.*?), y=(.*?): closest beacon is at x=(.*?), y=(.*?)$", row
        )

        sensor = Sensor(
            coordinates=Point(
                x=int(matched_coordinates.group(1)), y=int(matched_coordinates.group(2))
            ),
            nearest_beacon=Point(
                x=int(matched_coordinates.group(3)),
                y=int(matched_coordinates.group(4)),
            ),
        )
        sensor.distance_from_nearest_beacon = get_manhattan_distance(
            sensor.coordinates, sensor.nearest_beacon
        )
        sensors.append(sensor)

    return sensors


def get_manhattan_distance(point_a: Point, point_b: Point) -> int:
    return abs(point_a.x - point_b.x) + abs(point_a.y - point_b.y)
