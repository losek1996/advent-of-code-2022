import pytest

from day4.day4_solution import (
    fully_contains_other,
    overlaps_other,
    parse_row,
    Assignment,
)

FULLY_CONTAINS_OTHER_TEST_DATA = [
    pytest.param(
        Assignment(first_section_idx=1, last_section_idx=5),
        Assignment(first_section_idx=2, last_section_idx=3),
        True,
        id="True, 1st contains 2nd",
    ),
    pytest.param(
        Assignment(first_section_idx=2, last_section_idx=3),
        Assignment(first_section_idx=1, last_section_idx=5),
        True,
        id="True, 2nd contains 1st",
    ),
    pytest.param(
        Assignment(first_section_idx=2, last_section_idx=3),
        Assignment(first_section_idx=4, last_section_idx=5),
        False,
        id="False",
    ),
]


OVERLAPS_OTHER_TEST_DATA = [
    pytest.param(
        Assignment(first_section_idx=2, last_section_idx=3),
        Assignment(first_section_idx=3, last_section_idx=4),
        True,
        id="True (1)",
    ),
    pytest.param(
        Assignment(first_section_idx=2, last_section_idx=3),
        Assignment(first_section_idx=1, last_section_idx=2),
        True,
        id="True (2)",
    ),
    pytest.param(
        Assignment(first_section_idx=1, last_section_idx=2),
        Assignment(first_section_idx=3, last_section_idx=4),
        False,
        id="False (1)",
    ),
    pytest.param(
        Assignment(first_section_idx=3, last_section_idx=4),
        Assignment(first_section_idx=2, last_section_idx=3),
        True,
        id="True (3)",
    ),
    pytest.param(
        Assignment(first_section_idx=1, last_section_idx=2),
        Assignment(first_section_idx=2, last_section_idx=3),
        True,
        id="True (4)",
    ),
    pytest.param(
        Assignment(first_section_idx=3, last_section_idx=4),
        Assignment(first_section_idx=1, last_section_idx=2),
        False,
        id="False (2)",
    ),
]


@pytest.mark.parametrize(
    "first_assignment, second_assignment, expected_result",
    FULLY_CONTAINS_OTHER_TEST_DATA,
)
def test_fully_contains_other(
    first_assignment: Assignment, second_assignment: Assignment, expected_result: bool
):
    assert fully_contains_other(first_assignment, second_assignment) is expected_result


@pytest.mark.parametrize(
    "first_assignment, second_assignment, expected_result", OVERLAPS_OTHER_TEST_DATA
)
def test_overlaps_other(
    first_assignment: Assignment, second_assignment: Assignment, expected_result: bool
):
    assert overlaps_other(first_assignment, second_assignment) is expected_result


def test_parse_row():
    assert parse_row(row="39-57,39-57") == (
        Assignment(first_section_idx=39, last_section_idx=57),
        Assignment(first_section_idx=39, last_section_idx=57),
    )
