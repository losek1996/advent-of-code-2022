from dataclasses import dataclass


@dataclass
class Assignment:
    first_section_idx: int
    last_section_idx: int


def parse_row(row: str) -> tuple[Assignment, Assignment]:
    assignment_a, assignment_b = row.split(sep=",")
    return (
        Assignment(*(int(section) for section in assignment_a.split(sep="-"))),
        Assignment(*(int(section) for section in assignment_b.split(sep="-"))),
    )


def fully_contains_other(
    first_assignment: Assignment, second_assignment: Assignment
) -> bool:
    return (
        second_assignment.first_section_idx >= first_assignment.first_section_idx
        and second_assignment.last_section_idx <= first_assignment.last_section_idx
    ) or (
        second_assignment.first_section_idx <= first_assignment.first_section_idx
        and second_assignment.last_section_idx >= first_assignment.last_section_idx
    )


def overlaps_other(first_assignment: Assignment, second_assignment: Assignment) -> bool:
    return (
        (
            first_assignment.last_section_idx
            >= second_assignment.first_section_idx
            >= first_assignment.first_section_idx
            or first_assignment.last_section_idx
            >= second_assignment.last_section_idx
            >= first_assignment.first_section_idx
        )
        or second_assignment.last_section_idx
        >= first_assignment.first_section_idx
        >= second_assignment.first_section_idx
        or second_assignment.last_section_idx
        >= first_assignment.last_section_idx
        >= second_assignment.first_section_idx
    )


def count_fully_contains_other(data: list[str]) -> int:
    return sum(fully_contains_other(*parse_row(row)) for row in data)


def count_overlaps_other(data: list[str]) -> int:
    return sum(overlaps_other(*parse_row(row)) for row in data)


if __name__ == "__main__":
    assert fully_contains_other(
        Assignment(first_section_idx=1, last_section_idx=2),
        Assignment(first_section_idx=1, last_section_idx=4),
    )
    assert fully_contains_other(
        Assignment(first_section_idx=1, last_section_idx=4),
        Assignment(first_section_idx=2, last_section_idx=3),
    )
    assert not fully_contains_other(
        Assignment(first_section_idx=1, last_section_idx=4),
        Assignment(first_section_idx=2, last_section_idx=5),
    )
    assert parse_row(row="39-57,39-57") == (
        Assignment(first_section_idx=39, last_section_idx=57),
        Assignment(first_section_idx=39, last_section_idx=57),
    )
    assert overlaps_other(
        Assignment(first_section_idx=1, last_section_idx=2),
        Assignment(first_section_idx=2, last_section_idx=5),
    )
    assert overlaps_other(
        Assignment(first_section_idx=1, last_section_idx=4),
        Assignment(first_section_idx=2, last_section_idx=5),
    )
    assert overlaps_other(
        Assignment(first_section_idx=2, last_section_idx=5),
        Assignment(first_section_idx=1, last_section_idx=5),
    )
    assert overlaps_other(
        Assignment(first_section_idx=2, last_section_idx=5),
        Assignment(first_section_idx=1, last_section_idx=3),
    )
    assert overlaps_other(
        Assignment(first_section_idx=5, last_section_idx=7),
        Assignment(first_section_idx=7, last_section_idx=9),
    )
    assert overlaps_other(
        Assignment(first_section_idx=2, last_section_idx=8),
        Assignment(first_section_idx=3, last_section_idx=7),
    )
    assert overlaps_other(
        Assignment(first_section_idx=6, last_section_idx=6),
        Assignment(first_section_idx=4, last_section_idx=6),
    )
    assert overlaps_other(
        Assignment(first_section_idx=2, last_section_idx=6),
        Assignment(first_section_idx=4, last_section_idx=8),
    )
    assert overlaps_other(
        Assignment(first_section_idx=32, last_section_idx=32),
        Assignment(first_section_idx=31, last_section_idx=77),
    )
    assert not overlaps_other(
        Assignment(first_section_idx=2, last_section_idx=5),
        Assignment(first_section_idx=8, last_section_idx=9),
    )
    assert overlaps_other(
        Assignment(first_section_idx=2, last_section_idx=10),
        Assignment(first_section_idx=9, last_section_idx=9),
    )
    assert not overlaps_other(
        Assignment(first_section_idx=8, last_section_idx=9),
        Assignment(first_section_idx=2, last_section_idx=5),
    )
