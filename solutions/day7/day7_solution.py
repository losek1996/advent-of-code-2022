from dataclasses import dataclass, field


MEMORY_LIMIT_TO_USE = 4 * 10**7


@dataclass
class LsTerminalCommand:
    current_dir: str
    output: list[str] = field(default_factory=list)


@dataclass
class TerminalCommand:
    command: str
    output: list[str] = field(default_factory=list)


def get_sum_of_dirs_with_size_below_100k(dirs_with_size: dict[str, int]) -> int:
    return sum(dir_size for dir_size in dirs_with_size.values() if dir_size < 10**5)


def get_smallest_dir_size_to_freeze_memory_to_40000k(
    dirs_with_size: dict[str, int]
) -> int:
    total_size_of_dirs = max(dirs_with_size.values())
    if total_size_of_dirs > MEMORY_LIMIT_TO_USE:
        return min(
            [
                dir_size
                for dir_size in dirs_with_size.values()
                if dir_size > (total_size_of_dirs - MEMORY_LIMIT_TO_USE)
            ]
        )
    return 0


def establish_dirs_size(terminal_records: list[LsTerminalCommand]) -> dict[str, int]:
    dirs_with_size = {}
    for record in terminal_records[::-1]:
        dirs_with_size[record.current_dir] = establish_dir_size(record, dirs_with_size)

    return dirs_with_size


def parse_data(data: list[str]) -> list[LsTerminalCommand]:
    ls_command_records = []
    current_dir = ""
    split_data = split_by_command(data)
    for terminal_record in split_data:
        if terminal_record.command.startswith("$ ls"):
            ls_command_records.append(
                create_ls_command_record(terminal_record, current_dir)
            )
        elif terminal_record.command.startswith("$ cd"):
            current_dir = establish_current_dir(
                so_far_current_dir=current_dir, cd_argument=terminal_record.command[5:]
            )

    return ls_command_records


def establish_dir_size(
    record: LsTerminalCommand, dirs_with_size: dict[str, int]
) -> int:
    return sum(
        (
            dirs_with_size[
                establish_current_dir(record.current_dir, cd_argument=raw[4:])
            ]
            if raw.startswith("dir")
            else int(raw.split()[0])
        )
        for raw in record.output
    )


def establish_current_dir(so_far_current_dir: str, cd_argument: str) -> str:
    match cd_argument:
        case "/":
            return f"{so_far_current_dir}/"
        case "..":
            return f"/{'/'.join((dir_name for dir_name in so_far_current_dir.split('/')[:-1] if dir_name))}"
        case _:
            return f"{so_far_current_dir if so_far_current_dir != '/' else ''}/{cd_argument}"


def split_by_command(data: list[str]) -> list[TerminalCommand]:
    split_data = []
    for row in data:
        if row.startswith("$"):
            split_data.append(TerminalCommand(command=row))
        else:
            split_data[-1].output.append(row)

    return split_data


def create_ls_command_record(
    terminal_record: TerminalCommand, current_dir: str
) -> LsTerminalCommand:
    return LsTerminalCommand(current_dir=current_dir, output=terminal_record.output)
