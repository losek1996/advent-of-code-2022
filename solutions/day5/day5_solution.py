import re
from dataclasses import dataclass, field


@dataclass
class Move:
    from_queue: int
    to_queue: int
    crates_number: int


@dataclass
class Queue:
    crates: list[str] = field(default_factory=list)


def parse(data: list[str]) -> tuple[list[Queue], list[Move]]:
    empty_raw_idx = find_empty_raw_idx(data)
    num_of_stacks = find_num_of_stacks(raw=data[empty_raw_idx - 1])
    return parse_initial_state(
        data, end_line=empty_raw_idx - 1, num_of_stacks=num_of_stacks
    ), parse_moves(data, start_line=empty_raw_idx + 1)


def apply_moves_and_get_result(
    state: list[list[str]], moves: list[Move], retain_crates_order
) -> str:
    for move in moves:
        state[move.to_queue - 1].extend(
            state[move.from_queue - 1][-move.crates_number :][
                :: 1 if retain_crates_order else -1
            ]
        )
        state[move.from_queue - 1] = state[move.from_queue - 1][: -move.crates_number]

    return "".join((queue[-1] for queue in state))


def parse_initial_state(
    data: list[str], end_line: int, num_of_stacks: int
) -> list[Queue]:
    initial_state = [Queue() for _ in range(num_of_stacks)]
    for raw in data[:end_line][::-1]:
        for idx in range(1, len(raw), 4):
            if raw[idx] != " ":
                initial_state[(idx - 1) // 4].crates.append(raw[idx])

    return initial_state


def parse_moves(data: list[str], start_line: int) -> list[Move]:
    moves_matches = (
        re.search(r"^move (.+?) from (.+?) to (.+?)$", raw) for raw in data[start_line:]
    )
    return [
        Move(
            crates_number=int(match.group(1)),
            from_queue=int(match.group(2)),
            to_queue=int(match.group(3)),
        )
        for match in moves_matches
    ]


def find_empty_raw_idx(data: list[str]) -> int:
    for idx, raw in enumerate(data):
        if not raw.strip():
            return idx


def find_num_of_stacks(raw: str) -> int:
    return int(raw.strip().split()[-1])
