import pytest

from day6.day6_solution import count_chars_in_front_of_first_marker

COUNT_CHARS_IN_FRONT_OF_FIRST_MARKER_TEST_DATA = [
    pytest.param("bvwbjplbgvbhsrlpgdmjqwftvncz", 4, 5),
    pytest.param("zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw", 4, 11),
    pytest.param("mjqjpqmgbljsphdztnvjfqwrcgsmlb", 14, 19),
    pytest.param("zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw", 14, 26),
]


@pytest.mark.parametrize(
    "word, num_of_unique_chars_in_row, expected_result",
    COUNT_CHARS_IN_FRONT_OF_FIRST_MARKER_TEST_DATA,
)
def test_count_chars_in_front_of_first_marker(
    word, num_of_unique_chars_in_row, expected_result
):
    assert (
        count_chars_in_front_of_first_marker(word, num_of_unique_chars_in_row)
        == expected_result
    )
