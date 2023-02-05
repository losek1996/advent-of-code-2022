import copy
import os

import pytest

from solutions.day11.day11_solution import parse_data, Monkey, count_inspections
from solutions.read_data import read_raw_data_without_spaces

DATA_DIR = os.path.dirname(os.path.realpath(__file__)) + "/data/"


@pytest.fixture
def parsed_data(request) -> list[Monkey]:
    data = read_raw_data_without_spaces(DATA_DIR + request.param)
    return parse_data(data)


@pytest.mark.parametrize("parsed_data", ["test_data.txt"], indirect=True)
def test_count_inspections(parsed_data):
    assert count_inspections(
        monkeys=copy.deepcopy(parsed_data), iterations=20, worry_level_divisor=3
    ) == [101, 95, 7, 105]
    assert count_inspections(
        monkeys=copy.deepcopy(parsed_data), iterations=10000, worry_level_divisor=1
    ) == [
        52166,
        47830,
        1938,
        52013,
    ]
