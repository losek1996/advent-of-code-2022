import re

from pydantic import BaseModel

MIN_COORDINATE_VALUE = 0
MAX_COORDINATE_VALUE = 4 * 10**6

Point = tuple[int, int]


class NoSinglePositionWhereBeaconCanBePresentError(Exception):
    pass


class Sensor(BaseModel):
    coordinates: Point
    nearest_beacon: Point

    @property
    def distance_from_nearest_beacon(self) -> int:
        return get_manhattan_distance(
            self.nearest_beacon,
            self.coordinates,
        )


def count_positions_where_beacon_can_not_be_present(
    sensors: list[Sensor], target_y: int
) -> int:
    """
    Beacon can not be present on positions which distance is smaller or equal to the distance
    between sensor and its closest beacon.
    """

    def _get_x_coordinate_of_beacons(sensors_list: list[Sensor], y: int) -> set[int]:
        """
        We can't count positions where beacon already is.
        """
        beacons_x_coordinate = set()
        for sensor in sensors_list:
            nearest_beacon_x, nearest_beacon_y = sensor.nearest_beacon
            if nearest_beacon_y == y:
                beacons_x_coordinate.add(nearest_beacon_x)
        return beacons_x_coordinate

    x_coordinates_where_beacon_can_not_be_present: set[int] = set()
    x_coordinate_of_beacons = _get_x_coordinate_of_beacons(sensors, target_y)
    for sensor in sensors:
        positions = get_sensor_x_coordinates_where_beacon_can_not_be_present(
            sensor=sensor, target_y=target_y
        )
        x_coordinates_where_beacon_can_not_be_present.update(positions)

    return len(x_coordinates_where_beacon_can_not_be_present - x_coordinate_of_beacons)


def get_tuning_frequency_of_position_where_beacon_can_be_present(
    sensors: list[Sensor],
) -> int:
    beacon_position = find_position_where_additional_beacon_can_be_present(sensors)
    return get_tuning_frequency(beacon_position)


def parse_data(data: list[str]) -> list[Sensor]:
    sensors = []
    for row in data:
        matched_coordinates = re.match(
            r"^Sensor at x=(.*?), y=(.*?): closest beacon is at x=(.*?), y=(.*?)$", row
        )

        coordinates = (
            int(matched_coordinates.group(1)),
            int(matched_coordinates.group(2)),
        )
        nearest_beacon = (
            int(matched_coordinates.group(3)),
            int(matched_coordinates.group(4)),
        )

        sensor = Sensor(coordinates=coordinates, nearest_beacon=nearest_beacon)
        sensors.append(sensor)

    return sensors


def find_position_where_additional_beacon_can_be_present(
    sensors: list[Sensor],
) -> Point:
    """
    There is only a single position where additional beacon can be present.
    Distance of sensor to additional beacon must be equal to distance of that sensor to the closest beacon + 1.
    In other case there would exist multiple additional beacons.
    """
    for sensor in sensors:
        candidate_positions: set[Point] = generate_beacon_candidate_positions(sensor)
        for beacon_candidate in candidate_positions:
            if all(
                can_be_additional_beacon_position(beacon_candidate, sensor)
                for sensor in sensors
            ):
                return beacon_candidate

    raise NoSinglePositionWhereBeaconCanBePresentError


def get_manhattan_distance(point_a: Point, point_b: Point) -> int:
    point_a_x, point_a_y = point_a
    point_b_x, point_b_y = point_b
    return abs(point_a_x - point_b_x) + abs(point_a_y - point_b_y)


def get_sensor_x_coordinates_where_beacon_can_not_be_present(
    sensor: Sensor, target_y: int
) -> list[int]:
    source_point_x, source_point_y = sensor.coordinates
    max_distance = sensor.distance_from_nearest_beacon

    max_distance -= abs(target_y - source_point_y)
    if max_distance < 0:
        return []

    return [
        x
        for x in range(
            -max_distance + source_point_x, max_distance + source_point_x + 1
        )
    ]


def can_be_additional_beacon_position(beacon_candidate: Point, sensor: Sensor) -> bool:
    """
    Beacon candidate can't have smaller Manhattan distance to sensor than the sensor closest beacon.
    """
    distance_to_sensor = get_manhattan_distance(beacon_candidate, sensor.coordinates)
    return distance_to_sensor > sensor.distance_from_nearest_beacon


def generate_beacon_candidate_positions(sensor: Sensor) -> set[Point]:
    """
    Beacon candidate positions will have Manhattan distance equal to
    distance from sensor to the closest beacon + 1.
    In other case more than one beacon candidate could be additional beacon.
    """
    beacon_candidate_from_sensor_distance = sensor.distance_from_nearest_beacon + 1
    if beacon_candidate_from_sensor_distance > MAX_COORDINATE_VALUE:
        return set()

    beacon_candidate_positions: set[Point] = set()
    for x in range(beacon_candidate_from_sensor_distance + 1):
        y = beacon_candidate_from_sensor_distance - x
        coordinate_shifts = {(x, y), (-x, y), (-x, -y), (x, -y)}
        for x_shift, y_shift in coordinate_shifts:
            sensor_x_coordinate, sensor_y_coordinate = sensor.coordinates
            x_coordinate = sensor_x_coordinate + x_shift
            y_coordinate = sensor_y_coordinate + y_shift
            if (
                MIN_COORDINATE_VALUE <= x_coordinate <= MAX_COORDINATE_VALUE
                and MIN_COORDINATE_VALUE <= y_coordinate <= MAX_COORDINATE_VALUE
            ):
                beacon_candidate = (x_coordinate, y_coordinate)
                beacon_candidate_positions.add(beacon_candidate)
    return beacon_candidate_positions


def get_tuning_frequency(point: Point) -> int:
    x, y = point
    return 4 * 10**6 * x + y


def is_sensor_covered_by_another_sensor(
    parent_sensor: Sensor, child_sensor: Sensor
) -> bool:
    return (
        get_manhattan_distance(parent_sensor.coordinates, child_sensor.coordinates)
        + child_sensor.distance_from_nearest_beacon
        <= parent_sensor.distance_from_nearest_beacon
    )


def get_sensors_not_covered_by_another_sensors(sensors: list[Sensor]) -> list[Sensor]:
    """
    If area where beacons can not be located is covered by another sensor, we can exclude those sensors.
    """
    sensors_not_covered_by_another_sensors = []
    for idx, child_sensor in enumerate(sensors):
        if any(
            is_sensor_covered_by_another_sensor(parent_sensor, child_sensor)
            for parent_sensor in sensors
            if child_sensor is not parent_sensor
        ):
            continue
        sensors_not_covered_by_another_sensors.append(child_sensor)
    return sensors_not_covered_by_another_sensors
