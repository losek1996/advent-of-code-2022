from enum import Enum

from pydantic import BaseModel

COORDINATES_SEPARATOR = ","
POINTS_SEPARATOR = " -> "
START_X = 500
START_Y = 0
BUFFER = 150


class Coordinate(BaseModel):
    x: int
    y: int


class Segment(BaseModel):
    start: Coordinate
    end: Coordinate


class PointType(int, Enum):
    ROCK = 2
    SAND = 1


Map = dict[str, int]
Key = str
Data = tuple[Map, list[Segment]]


def produce_and_count_units_of_sand(data: Data, floor_exists=False) -> int:
    map_of_area, segments = data
    min_x, max_x, max_y = (
        find_min_x(segments),
        find_max_x(segments),
        find_max_y(segments),
    )
    if floor_exists:
        max_y = max_y + 2
        map_of_area = add_floor(map_of_area, min_x, max_x, max_y)

        min_x = float("-inf")
        max_x = float("inf")

    map_of_area = produce_units_of_sand(map_of_area, min_x, max_x, max_y)

    return count_units_of_sand(map_of_area)


def count_units_of_sand(map_of_area: Map) -> int:
    return [*map_of_area.values()].count(PointType.SAND.value)


def produce_units_of_sand(
    map_of_area: Map, min_x: int | float, max_x: int | float, max_y: int
) -> Map:
    while True:
        next_move = generate_next_move(
            map_of_area, x=START_X, y=START_Y, min_x=min_x, max_x=max_x, max_y=max_y
        )
        if next_move and not next_move in map_of_area:
            map_of_area[next_move] = PointType.SAND.value
        else:
            return map_of_area


def generate_next_move(
    map_of_area, x: int, y: int, min_x: int | float, max_x: int | float, max_y: int
) -> Key | None:
    bottom_left = map_of_area.get(generate_key(x - 1, y + 1))
    bottom_down = map_of_area.get(generate_key(x, y + 1))
    bottom_right = map_of_area.get(generate_key(x + 1, y + 1))

    if bottom_left and bottom_down and bottom_right:
        return generate_key(x=x, y=y)

    if not bottom_down:
        return (
            generate_next_move(map_of_area, x, y + 1, min_x, max_x, max_y)
            if y < max_y and min_x < x < max_x
            else None
        )

    if not bottom_left:
        return (
            generate_next_move(map_of_area, x - 1, y + 1, min_x, max_x, max_y)
            if y < max_y and min_x < x - 1 < max_x
            else None
        )

    if not bottom_right:
        return (
            generate_next_move(map_of_area, x + 1, y + 1, min_x, max_x, max_y)
            if y < max_y and min_x < x + 1 < max_x
            else None
        )


def parse_data(data: list[str]) -> Data:
    map_of_area = {}
    segments = parse_segments(data)
    for segment in segments:
        fill_map(segment, map_of_area)

    return map_of_area, segments


def fill_map(segment: Segment, map_of_area: Map) -> None:
    if segment.start.x == segment.end.x:
        min_y, max_y = min(segment.start.y, segment.end.y), max(
            segment.start.y, segment.end.y
        )
        for y in range(min_y, max_y + 1):
            map_of_area[generate_key(x=segment.start.x, y=y)] = PointType.ROCK.value
    elif segment.start.y == segment.end.y:
        min_x, max_x = min(segment.start.x, segment.end.x), max(
            segment.start.x, segment.end.x
        )
        for x in range(min_x, max_x + 1):
            map_of_area[generate_key(x=x, y=segment.start.y)] = PointType.ROCK.value


def parse_segments(data: list[str]) -> list[Segment]:
    segments: list[Segment] = []
    for row in data:
        coordinates = row.split(POINTS_SEPARATOR)
        for start, end in zip(coordinates[1:], coordinates[:-1]):
            segments.append(
                Segment(start=parse_coordinate(start), end=parse_coordinate(end))
            )
    return segments


def parse_coordinate(coordinate: str) -> Coordinate:
    x, y = coordinate.split(COORDINATES_SEPARATOR)

    return Coordinate(x=int(x), y=int(y))


def find_min_x(segments: list[Segment]) -> int:
    return min([min(segment.start.x, segment.end.x) for segment in segments])


def find_max_x(segments: list[Segment]) -> int:
    return max([max(segment.start.x, segment.end.x) for segment in segments])


def find_max_y(segments: list[Segment]) -> int:
    return max([max(segment.start.y, segment.end.y) for segment in segments])


def generate_key(x: int, y: int) -> Key:
    return f"{x} {y}"


def add_floor(map_of_area: Map, min_x: int, max_x: int, max_y: int) -> Map:
    for x in range(min_x - BUFFER, max_x + 1 + BUFFER):
        map_of_area[generate_key(x=x, y=max_y)] = PointType.ROCK.value

    return map_of_area
