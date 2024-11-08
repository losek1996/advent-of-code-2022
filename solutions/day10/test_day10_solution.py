import os

import pytest

from solutions.day10.day10_solution import (
    process_data,
    count_combined_signal_strength,
    produce_visualization,
)
from solutions.read_data import read_raw_data_without_spaces

DATA_DIR = os.path.dirname(os.path.realpath(__file__)) + "/data/"


@pytest.fixture
def register(request) -> dict[int, int]:
    data = read_raw_data_without_spaces(DATA_DIR + request.param)
    return process_data(data)


@pytest.mark.parametrize("register", ["test_data.txt"], indirect=True)
def test_count_combined_signal_strength(register: dict[int, int]):
    assert count_combined_signal_strength(register) == 13140


@pytest.mark.parametrize("register", ["test_data.txt"], indirect=True)
def test_produce_visualization(register: dict[int, int]):
    expected_visualization = [
        "##..##..##..##..##..##..##..##..##..##..",
        "###...###...###...###...###...###...###.",
        "####....####....####....####....####....",
        "#####.....#####.....#####.....#####.....",
        "######......######......######......####",
        "#######.......#######.......#######.....",
    ]
    assert produce_visualization(register) == "\n".join(expected_visualization)
