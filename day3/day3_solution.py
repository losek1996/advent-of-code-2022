def sum_priorities_1st_strategy(words: list[str]) -> int:
    return sum(
        sum_same_letters_cost(words=[word[: len(word) // 2], word[len(word) // 2 :]])
        for word in words
    )


def sum_priorities_2nd_strategy(words: list[str]) -> int:
    return sum(
        sum_same_letters_cost(words=words[i : i + 3]) for i in range(0, len(words), 3)
    )


def sum_same_letters_cost(words: list[str]) -> int:
    counters = [count_letters(word) for word in words]
    return sum(
        get_letter_cost(key)
        for key in counters[0].keys()
        if all(key in counter for counter in counters[1:])
    )


def get_letter_cost(letter: str) -> int:
    if letter.isupper():
        return 26 + ord(letter) - ord("A") + 1

    return ord(letter) - ord("a") + 1


def count_letters(word: str) -> dict[str, int]:
    counter = {}
    for letter in word:
        counter[letter] = counter.get(letter, 0) + 1

    return counter
