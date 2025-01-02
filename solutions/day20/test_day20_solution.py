import os

import pytest

from solutions.day20.day20_solution import (
    get_mixed_encrypted_file,
    sum_1000th_2000th_3000th_number,
)
from solutions.read_data import read_raw_data_without_spaces

DATA_DIR = os.path.dirname(os.path.realpath(__file__)) + "/data/"


@pytest.fixture
def parsed_data(request) -> list[int]:
    data = read_raw_data_without_spaces(DATA_DIR + request.param)
    data = [int(number) for number in data]
    return data


@pytest.mark.parametrize(
    "parsed_data, num_of_iterations, multiplier, expected_mixed_encrypted_file, expected_result",
    [
        pytest.param("test_data.txt", 1, 1, [1, 2, -3, 4, 0, 3, -2], 3),
        pytest.param(
            "test_data.txt",
            10,
            811589153,
            [
                0,
                -2434767459,
                1623178306,
                3246356612,
                -1623178306,
                2434767459,
                811589153,
            ],
            1623178306,
        ),
    ],
    indirect=["parsed_data"],
)
def test_sum_1000th_2000th_3000th_number(
    parsed_data: list[int],
    num_of_iterations: int,
    multiplier: int,
    expected_mixed_encrypted_file: list[int],
    expected_result: int,
):
    mixed_encrypted_file = get_mixed_encrypted_file(
        parsed_data, num_of_iterations=num_of_iterations, multiplier=multiplier
    )
    assert mixed_encrypted_file == expected_mixed_encrypted_file
    assert sum_1000th_2000th_3000th_number(mixed_encrypted_file) == expected_result
