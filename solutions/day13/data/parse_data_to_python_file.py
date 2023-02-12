from solutions.read_data import read_raw_data_without_spaces


def create_python_file_with_list_data(source_filename: str):
    data = read_raw_data_without_spaces(source_filename)

    with open("data.py", "w") as f:
        f.write("data = [\n")
        for row in data:
            if row:
                f.write(f"    {row},\n")
        f.write("]\n")
