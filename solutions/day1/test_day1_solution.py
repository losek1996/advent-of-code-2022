import os

import pytest

from solutions.day1.day1_solution import (
    get_calories_summed_up_by_elfs,
    get_top_n_calories_summed_up,
)
from solutions.read_data import read_raw_data

DATA_DIR = os.path.dirname(os.path.realpath(__file__)) + "/data/"


GET_TOP_N_CALORIES_SUMMED_UP_TEST_DATA = [
    pytest.param([1000, 2000, 500], 1, 2000, id="top 1"),
    pytest.param([1000, 2000, 500], 2, 3000, id="top 2"),
]


@pytest.fixture
def data(request):
    return read_raw_data(DATA_DIR + request.param)


@pytest.mark.parametrize("data", ["test_data.txt"], indirect=True)
def test_get_calories_summed_up_by_elfs(data: list[str]):
    assert get_calories_summed_up_by_elfs(data) == [6000, 4000, 11000, 24000, 10000]


@pytest.mark.parametrize(
    "calories_summed_up_by_elfs, top_n, expected_top_n_calories_summed_up",
    GET_TOP_N_CALORIES_SUMMED_UP_TEST_DATA,
)
def test_get_top_n_calories_summed_up(
    calories_summed_up_by_elfs: list[int],
    top_n: int,
    expected_top_n_calories_summed_up: int,
):
    assert (
        get_top_n_calories_summed_up(calories_summed_up_by_elfs, n=top_n)
        == expected_top_n_calories_summed_up
    )
