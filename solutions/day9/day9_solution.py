from dataclasses import dataclass
from enum import Enum


@dataclass
class Position:
    x: int
    y: int

    def __str__(self):
        return f"{self.x} {self.y}"


class Direction(str, Enum):
    UP = "U"
    DOWN = "D"
    LEFT = "L"
    RIGHT = "R"


def count_tail_positions(lines: list[str], rope_length: int) -> int:
    curr_rope_pos = [Position(0, 0)] * rope_length

    tail_positions = set()
    tail_positions.add(str(curr_rope_pos[0]))

    for line in lines:
        for move in range(int(line[2:])):
            curr_rope_pos = set_curr_rope_position(
                so_far_rope_pos=curr_rope_pos, direction=line[0]
            )
            tail_positions.add(str(curr_rope_pos[-1]))

    return len(tail_positions)


def set_curr_rope_position(
    so_far_rope_pos: list[Position], direction: str
) -> list[Position]:
    curr_head_pos = set_curr_head_position(
        curr_position=so_far_rope_pos[0], direction=direction
    )
    curr_rope_pos = [curr_head_pos]
    for position in so_far_rope_pos[1:]:
        curr_rope_pos.append(
            set_curr_tail_position(head_pos=curr_rope_pos[-1], tail_pos=position)
        )

    return curr_rope_pos


def set_curr_head_position(curr_position: Position, direction: str) -> Position:
    match direction:
        case Direction.UP.value:
            return Position(x=curr_position.x, y=curr_position.y + 1)
        case Direction.DOWN.value:
            return Position(x=curr_position.x, y=curr_position.y - 1)
        case Direction.LEFT.value:
            return Position(x=curr_position.x - 1, y=curr_position.y)
        case Direction.RIGHT.value:
            return Position(x=curr_position.x + 1, y=curr_position.y)


def set_curr_tail_position(head_pos: Position, tail_pos: Position) -> Position:
    if tail_touches_head(tail_pos, head_pos):
        return tail_pos

    if is_same_row(head_pos, tail_pos):
        x = tail_pos.x + 1 if head_pos.x > tail_pos.x else tail_pos.x - 1
        return Position(x=x, y=tail_pos.y)
    elif is_same_column(head_pos, tail_pos):
        y = tail_pos.y + 1 if head_pos.y > tail_pos.y else tail_pos.y - 1
        return Position(x=tail_pos.x, y=y)

    x = tail_pos.x + 1 if head_pos.x > tail_pos.x else tail_pos.x - 1
    y = tail_pos.y + 1 if head_pos.y > tail_pos.y else tail_pos.y - 1
    return Position(x=x, y=y)


def is_same_row(head_pos: Position, tail_pos: Position) -> bool:
    return tail_pos.y == head_pos.y


def is_same_column(head_pos: Position, tail_pos: Position) -> bool:
    return tail_pos.x == head_pos.x


def tail_touches_head(tail_pos: Position, head_pos: Position) -> bool:
    return abs(tail_pos.x - head_pos.x) < 2 and abs(tail_pos.y - head_pos.y) < 2
