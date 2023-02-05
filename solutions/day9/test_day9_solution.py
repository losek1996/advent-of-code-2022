import os

import pytest

from solutions.day9.day9_solution import count_tail_positions
from solutions.read_data import read_raw_data

DATA_DIR = os.path.dirname(os.path.realpath(__file__)) + "/data/"


@pytest.fixture
def data(request):
    return read_raw_data(DATA_DIR + request.param)


COUNT_TAIL_POSITIONS_TEST_DATA = [
    pytest.param("test_data.txt", 2, 13),
    pytest.param("test_data.txt", 10, 1, id="tail doesn't move at all"),
    pytest.param("additional_test_data.txt", 10, 36),
]


@pytest.mark.parametrize(
    "data, rope_length, expected_result",
    COUNT_TAIL_POSITIONS_TEST_DATA,
    indirect=["data"],
)
def test_count_tail_positions(data: list[str], rope_length: int, expected_result: int):
    assert count_tail_positions(data, rope_length) == expected_result
