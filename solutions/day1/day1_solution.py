def get_calories_summed_up_by_elfs(data: list[str]) -> list[int]:
    calories_arr = [[]]
    for row in data:
        if not row.strip():
            calories_arr.append([])
        else:
            calories_arr[-1].append(int(row.strip()))

    return [sum(elfs_calories) for elfs_calories in calories_arr]


def get_top_n_calories_summed_up(calories_summed_up_by_elfs: list[int], n: int) -> int:
    return sum(sorted(calories_summed_up_by_elfs)[-n:])
