from collections import OrderedDict


def get_mixed_encrypted_file(
    data: list[int], num_of_iterations: int, multiplier: int
) -> list[int]:
    num_of_values = len(data)
    original_to_current_index_map = OrderedDict()
    current_to_original_index_map = OrderedDict()
    for idx in range(num_of_values):
        original_to_current_index_map[idx] = idx
        current_to_original_index_map[idx] = idx

    _last_index = num_of_values - 1
    for _ in range(num_of_iterations):
        for original_index in range(len(data)):
            current_index = original_to_current_index_map[original_index]
            value = data[original_index]

            """
            (a + b) % c = (a % c + b % c) % c
            (a * b) % c = (a % c * b % c) % c
            (a + d * e) % c = (a % c + (d * e) % c) % c = (a % c + (d % c * e % c) % c) %c
            _last_index = len(data) - 1  # Why? because allowed indices are 0..(len(data) - 1)   
            """
            destination_index = (
                current_index % _last_index
                + (value % _last_index * multiplier % _last_index) % _last_index
            ) % _last_index
            indices_diff = abs(current_index - destination_index)
            if destination_index == 0 and indices_diff > 0:
                destination_index = _last_index
            elif destination_index == _last_index and indices_diff > 0:
                destination_index = 0

            current_order = list(current_to_original_index_map.values())

            """We operate on original indices in new_order list"""
            if destination_index >= current_index:
                """
                Assume we move some value from index A to index B.
                X1 A X2 B X3 -> X1 X2 B A X3
                """
                new_order = (
                    current_order[:current_index]
                    + current_order[current_index + 1 : destination_index + 1]
                    + [original_index]
                    + current_order[destination_index + 1 :]
                )
            else:
                """
                Assume we move some value from index A to index B.
                X1 B X2 A X3 -> X1 A B X2 X3
                """
                new_order = (
                    current_order[:destination_index]
                    + [original_index]
                    + current_order[destination_index:current_index]
                    + current_order[current_index + 1 :]
                )

            for current_idx, original_idx in enumerate(new_order):
                original_to_current_index_map[original_idx] = current_idx
                current_to_original_index_map[current_idx] = original_idx

    final_order = list(current_to_original_index_map.values())
    mixed_encrypted_file = [
        data[original_idx] * multiplier for original_idx in final_order
    ]
    return mixed_encrypted_file


def sum_1000th_2000th_3000th_number(mixed_encrypted_file: list[int]) -> int:
    value_0_idx = mixed_encrypted_file.index(0)
    number_after = [1000, 2000, 3000]
    sum_of_numbers = 0
    for number in number_after:
        sum_of_numbers += mixed_encrypted_file[
            (value_0_idx + number)
            % (len(mixed_encrypted_file))  # we assume first number after 0 has index 1
        ]
    return sum_of_numbers
