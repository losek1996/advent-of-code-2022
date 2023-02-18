def read_raw_data(file_path: str) -> list[str]:
    with open(file_path, "r") as f:
        return f.readlines()


def read_raw_data_without_spaces(file_path: str) -> list[str]:
    return [raw.strip() for raw in read_raw_data(file_path)]
