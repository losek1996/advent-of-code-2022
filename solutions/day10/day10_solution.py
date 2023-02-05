from enum import Enum


class Instruction(str, Enum):
    NOOP = "noop"
    ADDX = "addx"


def count_combined_signal_strength(register: dict[int, int]) -> int:
    return sum(cycle * register[cycle - 1] for cycle in range(20, 260, 40))


def produce_visualization(register: dict[int, int]) -> str:
    pixels = []
    for idx in range(6):
        for cycle in range(40):
            if register[cycle + idx * 40] - 1 <= cycle < register[cycle + idx * 40] + 2:
                pixels.append("#")
            else:
                pixels.append(".")

    return "\n".join("".join(pixels[40 * idx : 40 * (idx + 1)]) for idx in range(6))


def process_data(data: list[str]) -> dict[int, int]:
    register = {}
    cycle, value = 0, 1
    for record in data:
        if record[:4] == Instruction.NOOP.value:
            register[cycle] = value
            cycle += 1
        elif record[:4] == Instruction.ADDX.value:
            register[cycle] = value
            register[cycle + 1] = value
            cycle += 2
            value += int(record[5:])

    return register
