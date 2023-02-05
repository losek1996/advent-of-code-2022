import pytest

from solutions.day2.day2_solution import (
    SECOND_STRATEGY_PUNCTUATION,
    FIRST_STRATEGY_PUNCTUATION,
    sum_punctuation,
)


@pytest.mark.parametrize(
    "strategy, expected_result",
    [(FIRST_STRATEGY_PUNCTUATION, 15), (SECOND_STRATEGY_PUNCTUATION, 12)],
)
def test_sum_punctuation(strategy: dict[str, int], expected_result: int):
    assert sum_punctuation(data=["A Y", "B X", "C Z"], punctuation_strategy=strategy)
