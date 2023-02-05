def count_chars_in_front_of_first_marker(
    word: str, num_of_unique_chars_in_row: int
) -> int | None:
    for idx in range(len(word) - 3):
        if (
            len(set(word[idx : idx + num_of_unique_chars_in_row]))
            == num_of_unique_chars_in_row
        ):
            return idx + num_of_unique_chars_in_row
