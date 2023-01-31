from day8.day8_solution import count_visible_trees, find_max_scenic_score


def test_count_visible_trees():
    assert (
        count_visible_trees(
            [
                [3, 0, 3, 7, 3],
                [2, 5, 5, 1, 2],
                [6, 5, 3, 3, 2],
                [3, 3, 5, 4, 9],
                [3, 5, 3, 9, 0],
            ]
        )
    ) == 21


def test_find_max_scenic_score():
    assert (
        find_max_scenic_score(
            [
                [3, 0, 3, 7, 3],
                [2, 5, 5, 1, 2],
                [6, 5, 3, 3, 2],
                [3, 3, 5, 4, 9],
                [3, 5, 3, 9, 0],
            ]
        )
        == 8
    )
