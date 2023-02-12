def sum_indices_of_packets_in_right_order(data: list[list]) -> int:
    return sum(
        [
            idx + 1
            for idx in range(len(data) // 2)
            if compare(data[idx * 2], data[idx * 2 + 1])
        ]
    )


def count_packets_in_front(packet: list, data: list[list]) -> int:
    return sum([compare(left, packet) for left in data])


def compare(left: list, right: list) -> bool:
    if isinstance(left, int) and isinstance(right, int):
        return left < right
    elif isinstance(left, int):
        return compare([left], right)
    elif isinstance(right, int):
        return compare(left, [right])

    for a, b in zip(left, right):
        if not is_same(a, b):
            return compare(a, b)

    return len(left) <= len(right)


def get_first_int(data: list) -> int | None:
    if len(data) == 0:
        return None
    while isinstance(data, list) and len(data) > 0:
        data = data[0]

    return data if isinstance(data, int) else None


def is_same(left: list | int, right: list | int) -> bool:
    if type(left) == type(right):
        return left == right

    if isinstance(left, int):
        return len(right) == 1 and left == get_first_int(right)

    return False
