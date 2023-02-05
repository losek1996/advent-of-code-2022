from solutions.read_data import read_raw_data

TreesHeightsMap = list[list[int]]


def count_visible_trees(trees_heights: TreesHeightsMap) -> int:
    counter = len(trees_heights[0]) * 2 + len(trees_heights) * 2 - 4

    for x in range(1, len(trees_heights) - 1):
        for y in range(1, len(trees_heights[x]) - 1):
            counter += is_tree_visible(x, y, trees_heights)

    return counter


def find_max_scenic_score(trees_heights: TreesHeightsMap) -> int:
    max_scenic_score = 0
    for x in range(1, len(trees_heights) - 1):
        for y in range(1, len(trees_heights[x]) - 1):
            max_scenic_score = max(
                establish_scenic_score(x, y, trees_heights), max_scenic_score
            )

    return max_scenic_score


def is_tree_visible(x: int, y: int, trees_heights: TreesHeightsMap) -> bool:
    tree_height = trees_heights[x][y]

    return (
        max(trees_heights[x][y + 1 :]) < tree_height
        or max(trees_heights[x][:y]) < tree_height
        or max(row[y] for row in trees_heights[:x]) < tree_height
        or max(row[y] for row in trees_heights[x + 1 :]) < tree_height
    )


def establish_scenic_score(x: int, y: int, trees_heights: TreesHeightsMap) -> int:
    tree_height = trees_heights[x][y]
    right_visible_neighbors = count_visible_neighbors(
        tree_height, neighbors_heights=trees_heights[x][y + 1 :]
    )
    left_visible_neighbors = count_visible_neighbors(
        tree_height, neighbors_heights=trees_heights[x][:y][::-1]
    )
    top_visible_neighbors = count_visible_neighbors(
        tree_height, neighbors_heights=[row[y] for row in trees_heights[:x]][::-1]
    )
    bottom_visible_neighbors = count_visible_neighbors(
        tree_height, neighbors_heights=[row[y] for row in trees_heights[x + 1 :]]
    )

    return (
        left_visible_neighbors
        * right_visible_neighbors
        * top_visible_neighbors
        * bottom_visible_neighbors
    )


def count_visible_neighbors(tree_height: int, neighbors_heights: list[int]) -> int:
    for idx, neighbor_height in enumerate(neighbors_heights):
        if neighbor_height >= tree_height:
            return idx + 1

    return len(neighbors_heights)


def read_and_parse_data(filename: str) -> TreesHeightsMap:
    data = read_raw_data(filename)
    return [[int(digit) for digit in raw.strip()] for raw in data]
