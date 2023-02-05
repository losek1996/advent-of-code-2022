import copy
from collections import deque
from enum import Enum

from pydantic import BaseModel


class PointType(str, Enum):
    ORIGIN = "S"
    DESTINATION = "E"


class HeightType(str, Enum):
    ORIGIN = "a"
    DESTINATION = "z"


class Point(BaseModel):
    x: int
    y: int


class GridPoint(BaseModel):
    elevation: str
    distance_from_origin: int = 0


HeightMap = dict[str, GridPoint]


def find_shortest_path_length(height_map: HeightMap, origin: str = None) -> int | None:
    if not origin:
        origin = find_point_by_type(point_type=PointType.ORIGIN, height_map=height_map)
    destination: str = find_point_by_type(
        point_type=PointType.DESTINATION, height_map=height_map
    )
    to_visit: deque[str] = deque([origin])
    visited: set = set()

    while to_visit:
        current_point = to_visit.popleft()
        visited.add(current_point)

        if current_point == destination:
            return height_map[current_point].distance_from_origin

        next_points = generate_all_next_valid_points(current_point, height_map, visited)
        height_map = set_distance_from_origin(
            points=next_points,
            height_map=height_map,
            distance=height_map[current_point].distance_from_origin + 1,
        )
        to_visit.extend(*[next_points])


def find_shortest_path_from_any_point_with_elevation_a(
    height_map: HeightMap,
) -> int | None:
    start_points = find_all_points_by_elevation_height(HeightType.ORIGIN, height_map)
    distances = [
        find_shortest_path_length(copy.deepcopy(height_map), origin=start_point)
        for start_point in start_points
    ]
    distances = [distance for distance in distances if distance is not None]

    if not distances:
        return None

    return min(distances)


def generate_all_next_valid_points(
    curr_point_str: str, height_map: HeightMap, visited: set
) -> list[str]:
    curr_point = str_to_point(curr_point_str)
    next_possible_points = [
        f"{curr_point.x} {curr_point.y + 1}",
        f"{curr_point.x} {curr_point.y - 1}",
        f"{curr_point.x + 1} {curr_point.y}",
        f"{curr_point.x - 1} {curr_point.y}",
    ]

    return [
        point
        for point in next_possible_points
        if is_next_point_valid(
            curr_point_str, next_point_str=point, height_map=height_map, visited=visited
        )
    ]


def is_next_point_valid(
    curr_point_str: str, next_point_str: str, height_map: HeightMap, visited: set
) -> bool:
    if (
        next_point_str in height_map
        and next_point_str not in visited
        and not is_next_point_already_on_to_visit_queue(height_map[next_point_str])
    ):
        curr_point_elevation_height = get_elevation_height(
            elevation=height_map[curr_point_str].elevation
        )
        next_point_elevation_height = get_elevation_height(
            elevation=height_map[next_point_str].elevation
        )
        return next_point_elevation_height <= curr_point_elevation_height + 1

    return False


def parse_data(data: list[str]) -> HeightMap:
    height_map = {}
    for row_idx, row in enumerate(data):
        for column_idx, elevation in enumerate(row):
            height_map[f"{row_idx} {column_idx}"] = GridPoint(elevation=elevation)

    return height_map


def find_point_by_type(point_type: PointType, height_map: HeightMap) -> str | None:
    for cooridnates, grid_point in height_map.items():
        if point_type.value == grid_point.elevation:
            return cooridnates


def find_all_points_by_elevation_height(
    height: HeightType, height_map: HeightMap
) -> list[str]:
    return [
        cooridnates
        for cooridnates, grid_point in height_map.items()
        if get_elevation_height(height.value)
        == get_elevation_height(grid_point.elevation)
    ]


def set_distance_from_origin(
    points: list[str], height_map: HeightMap, distance: int
) -> HeightMap:
    for point in points:
        height_map[point].distance_from_origin = distance

    return height_map


def str_to_point(coordinates: str) -> Point:
    x, y = [int(coordinate) for coordinate in coordinates.split()]
    return Point(x=x, y=y)


def get_elevation_height(elevation: str) -> int:
    match elevation:
        case PointType.ORIGIN.value:
            return ord("a")
        case PointType.DESTINATION.value:
            return ord("z")
        case _:
            return ord(elevation)


def is_next_point_already_on_to_visit_queue(point: GridPoint) -> bool:
    """
    Points that have distance_from_origin different from 0, are already added to to_visit.
    distance_from_origin gets updated once point is added to to_visit queue and distance_from_origin can no longer be 0.
    """
    return point.distance_from_origin != 0
