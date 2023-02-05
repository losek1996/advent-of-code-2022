import functools

from pydantic import BaseModel


class Monkey(BaseModel):
    id: int
    items: list[int]
    operation_sign: str
    operation_value: str
    divisible_by: int
    true_division_condition_monkey: int
    false_division_condition_monkey: int
    inspected: int = 0


def count_inspections(
    monkeys: list[Monkey], iterations: int, worry_level_divisor: int
) -> list[int]:
    divisible_by_arr = get_all_divisible_by(monkeys)
    for it in range(iterations):
        for monkey in monkeys:
            for item in monkey.items:
                monkey_id, worry_level = get_monkey_to_throw_item(
                    monkey=monkey,
                    worry_level=item,
                    divisible_by_arr=divisible_by_arr,
                    worry_level_divisor=worry_level_divisor,
                )
                monkeys[monkey_id].items.append(worry_level)
            monkey.inspected += len(monkey.items)
            monkey.items = []

    return [monkey.inspected for monkey in monkeys]


def get_monkey_to_throw_item(
    monkey: Monkey,
    worry_level: int,
    divisible_by_arr: list[int],
    worry_level_divisor: int,
) -> tuple[int, int]:
    worry_level = get_updated_and_reduced_worry_level(
        so_far_worry_level=worry_level,
        operation_sign=monkey.operation_sign,
        operation_value=monkey.operation_value,
        divisible_by_arr=divisible_by_arr,
        worry_level_divisor=worry_level_divisor,
    )
    if worry_level % monkey.divisible_by == 0:
        return monkey.true_division_condition_monkey, worry_level

    return monkey.false_division_condition_monkey, worry_level


def get_updated_and_reduced_worry_level(
    so_far_worry_level: int,
    operation_sign: str,
    operation_value: str,
    divisible_by_arr: list[int],
    worry_level_divisor: int,
) -> int:
    operation_value = (
        so_far_worry_level if operation_value == "old" else int(operation_value)
    )

    match operation_sign:
        case "*":
            worry_level = (so_far_worry_level * operation_value) % functools.reduce(
                lambda x, y: x * y, divisible_by_arr
            )
        case "/":
            worry_level = so_far_worry_level // operation_value
        case "-":
            worry_level = so_far_worry_level - operation_value
        case "+":
            worry_level = so_far_worry_level + operation_value

    return worry_level // worry_level_divisor


def parse_monkey_record(data: list[str]) -> Monkey:
    return Monkey(
        id=int(data[0][7]),
        items=[int(number) for number in data[1][16:].split(",")],
        operation_sign=data[2][21],
        operation_value=data[2][23:],
        divisible_by=int(data[3][19:]),
        true_division_condition_monkey=int(data[4][25:]),
        false_division_condition_monkey=int(data[5][26:]),
    )


def get_all_divisible_by(monkeys: list[Monkey]) -> list[int]:
    return [monkey.divisible_by for monkey in monkeys]


def parse_data(data: list[str]) -> list[Monkey]:
    return [
        parse_monkey_record(data[i * 7 : i * 7 + 6])
        for i in range(len(data) // 7 + (len(data) % 7 > 0))
    ]
