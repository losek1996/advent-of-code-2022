import pytest

from solutions.day13.data.data import input_data
from solutions.day13.day13_solution import (
    compare,
    sum_indices_of_packets_in_right_order,
    get_first_int,
    count_packets_in_front,
)


COMPARE_TEST_DATA = [
    pytest.param([1, 1, 3, 1, 1], [1, 1, 5, 1, 1], True, id="5 is greater than 3"),
    pytest.param([[1], [2, 3, 4]], [[1], 4], True, id="4 is greater than 2"),
    pytest.param([9], [[8, 7, 6]], False, id="8 is not greater than 9"),
    pytest.param(
        [[4, 4], 4, 4],
        [[4, 4], 4, 4, 4],
        True,
        id="left list first run out of elements",
    ),
    pytest.param(
        [7, 7, 7, 7], [7, 7, 7], False, id="right list first run out of elements"
    ),
    pytest.param([], [3], True, id="left list first run out of elements (1)"),
    pytest.param([[[]]], [[]], False, id="right list first run out of elements (1)"),
    pytest.param(
        [1, [2, [3, [4, [5, 6, 7]]]], 8, 9],
        [1, [2, [3, [4, [5, 6, 0]]]], 8, 9],
        False,
        id="0 is not greater than 7",
    ),
]


@pytest.mark.parametrize("left, right, expected_result", COMPARE_TEST_DATA)
def test_compare(left: list | int, right: list | int, expected_result: bool):
    assert compare(left, right) is expected_result


@pytest.mark.parametrize("data, expected_result", [([[[]]], None), ([[[2, 3]]], 2)])
def test_get_first_int(data, expected_result):
    assert get_first_int(data) == expected_result


def test_sum_indices_of_packets_in_right_order():
    assert sum_indices_of_packets_in_right_order(input_data) == 5588


def test_count_packets_in_front():
    data = [
        [],
        [[]],
        [[[]]],
        [1, 1, 3, 1, 1],
        [1, 1, 5, 1, 1],
        [[1], [2, 3, 4]],
        [1, [2, [3, [4, [5, 6, 0]]]], 8, 9],
        [1, [2, [3, [4, [5, 6, 7]]]], 8, 9],
        [[1], 4],
        [3],
        [[4, 4], 4, 4],
        [[4, 4], 4, 4, 4],
        [7, 7, 7],
        [7, 7, 7, 7],
        [[8, 7, 6]],
        [9],
    ]

    assert count_packets_in_front(packet=[[2]], data=data) == 9
    assert count_packets_in_front(packet=[[6]], data=[[[2]], *data]) == 13
