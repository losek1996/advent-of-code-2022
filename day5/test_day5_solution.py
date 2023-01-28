import os

import pytest

from day5.day5_solution import (
    apply_moves_and_get_result,
    parse,
    Move,
    Queue,
    find_num_of_stacks,
    find_empty_raw_idx,
    parse_initial_state,
    parse_moves,
)
from read_data import read_raw_data

DATA_DIR = os.path.dirname(os.path.realpath(__file__)) + "/data/"


@pytest.fixture
def data(request):
    return read_raw_data(DATA_DIR + request.param)


APPLY_MOVES_AND_GET_RESULT_TEST_DATA = [
    pytest.param(
        [["Z", "N"], ["M", "C", "D"], ["P"]],
        [
            Move(crates_number=1, from_queue=2, to_queue=1),
            Move(crates_number=3, from_queue=1, to_queue=3),
            Move(crates_number=2, from_queue=2, to_queue=1),
            Move(crates_number=1, from_queue=1, to_queue=2),
        ],
        False,
        "CMZ",
        id="with not retained order",
    ),
    pytest.param(
        [["Z", "N"], ["M", "C", "D"], ["P"]],
        [
            Move(crates_number=1, from_queue=2, to_queue=1),
            Move(crates_number=3, from_queue=1, to_queue=3),
            Move(crates_number=2, from_queue=2, to_queue=1),
            Move(crates_number=1, from_queue=1, to_queue=2),
        ],
        True,
        "MCD",
    ),
]


@pytest.mark.parametrize(
    "initial_state, moves, retain_crates_order, expected_result",
    APPLY_MOVES_AND_GET_RESULT_TEST_DATA,
)
def test_apply_moves_and_get_result__returns_result_(
    initial_state: list[list[str]],
    moves: list[Move],
    retain_crates_order: bool,
    expected_result: str,
):
    assert (
        apply_moves_and_get_result(initial_state, moves, retain_crates_order)
        == expected_result
    )


@pytest.mark.parametrize("data", ["test_data.txt"], indirect=True)
def test_parse__parses_initial_state_and_moves(data: list[str]):
    assert parse(data) == (
        [
            Queue(crates=["Z", "N"]),
            Queue(crates=["M", "C", "D"]),
            Queue(crates=["P"]),
        ],
        [
            Move(crates_number=1, from_queue=2, to_queue=1),
            Move(crates_number=3, from_queue=1, to_queue=3),
            Move(crates_number=2, from_queue=2, to_queue=1),
            Move(crates_number=1, from_queue=1, to_queue=2),
        ],
    )


def test_find_num_of_stacks():
    assert find_num_of_stacks(raw=" 1   2   3 ") == 3


@pytest.mark.parametrize("data", ["test_data.txt"], indirect=True)
def test_find_empty_raw_idx(data):
    assert find_empty_raw_idx(data) == 4
