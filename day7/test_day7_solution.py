import os

import pytest

from day7.day7_solution import (
    establish_current_dir,
    establish_dirs_size,
    parse_data,
    get_sum_of_dirs_with_size_below_100k,
    get_smallest_dir_size_to_freeze_memory_to_40000k,
)
from read_data import read_raw_data_without_spaces

DATA_DIR = os.path.dirname(os.path.realpath(__file__)) + "/"


@pytest.fixture
def parsed_data(request):
    data = read_raw_data_without_spaces(DATA_DIR + request.param)
    return parse_data(data)


def test_establish_current_dir__returns_current_dir():
    assert establish_current_dir("/", "a") == "/a"
    assert establish_current_dir("/a/b", "c") == "/a/b/c"
    assert establish_current_dir("/a/b", "..") == "/a"
    assert establish_current_dir("/a", "b") == "/a/b"


@pytest.mark.parametrize("parsed_data", ["data.txt"], indirect=True)
def test_get_sum_of_dirs_with_size_below_100k(parsed_data):
    dirs_with_size = establish_dirs_size(parsed_data)
    assert get_sum_of_dirs_with_size_below_100k(dirs_with_size) == 1611443


@pytest.mark.parametrize("parsed_data", ["data.txt"], indirect=True)
def test_get_smallest_dir_size_to_freeze_memory_to_40000k(parsed_data):
    dirs_with_size = establish_dirs_size(parsed_data)
    assert get_smallest_dir_size_to_freeze_memory_to_40000k(dirs_with_size) == 2086088
