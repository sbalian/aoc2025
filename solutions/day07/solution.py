from collections import defaultdict
from pathlib import Path

Point = tuple[int, int]


def read_grid(path: str) -> list[list[str]]:
    return [list(line) for line in Path(path).read_text().strip().splitlines()]


def find_start(grid: list[list[str]]) -> Point:
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == "S":
                return i, j
    raise ValueError("start not found")


def find_terminal_nodes_and_count_splits(
    grid: list[list[str]], start: Point
) -> tuple[list[Point], int]:
    beams = set[Point]()
    beams.add(start)
    splits = 0
    for _ in range(len(grid) - 1):
        new_beams = set[Point]()
        for i, j in beams:
            if grid[i + 1][j] == ".":
                new_beams.add((i + 1, j))
            else:
                splits += 1
                new_beams.add((i + 1, j + 1))
                new_beams.add((i + 1, j - 1))
        beams = new_beams
    return [(i + 1, j) for i, j in beams], splits


def find_non_terminal_nodes(grid: list[list[str]]) -> list[Point]:
    nodes = list[Point]()
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == "^" or grid[i][j] == "S":
                nodes.append((i, j))
    return nodes


def dfs_count_paths(
    neighbours: dict[Point, list[Point]], start: Point, end: Point
) -> int:
    stack = [(start, [start])]
    count = 0
    while stack:
        node, path = stack.pop()
        if node == end:
            count += 1
            continue
        for neighbour in neighbours[node]:
            if neighbour not in path:
                stack.append((neighbour, path + [neighbour]))
    return count


def count_paths(
    non_terminal_nodes: list[Point],
    terminal_nodes: list[Point],
    start: Point,
) -> int:
    all_nodes = non_terminal_nodes + terminal_nodes
    all_nodes_by_j = defaultdict[int, list[Point]](list)
    for i, j in all_nodes:
        all_nodes_by_j[j].append((i, j))
    for j in all_nodes_by_j.keys():
        all_nodes_by_j[j] = sorted(all_nodes_by_j[j], key=lambda x: x[0])
    neighbours = dict[Point, list[Point]]()
    left, right = None, None
    for i, j in non_terminal_nodes:
        if (i, j) == start:
            for node in all_nodes_by_j[j]:
                if node[0] > i:
                    neighbours[start] = [node]
                    break
            continue
        for node in all_nodes_by_j[j - 1]:
            if node[0] > i:
                left = node
                break
        for node in all_nodes_by_j[j + 1]:
            if node[0] > i:
                right = node
                break
        assert left is not None
        assert right is not None
        neighbours[(i, j)] = [left, right]
    for node in terminal_nodes:
        neighbours[node] = []
    count = 0
    for end in terminal_nodes:
        count += dfs_count_paths(neighbours, start, end)
    return count


def main() -> None:
    grid = read_grid("example.txt")
    start = find_start(grid)
    terminal_nodes, splits = find_terminal_nodes_and_count_splits(grid, start)
    assert splits == 21
    non_terminal_nodes = find_non_terminal_nodes(grid)
    assert count_paths(non_terminal_nodes, terminal_nodes, start) == 40

    grid = read_grid("input.txt")
    start = find_start(grid)
    terminal_nodes, splits = find_terminal_nodes_and_count_splits(grid, start)
    assert splits == 1566
    non_terminal_nodes = find_non_terminal_nodes(grid)
    count_paths(non_terminal_nodes, terminal_nodes, start)
    print("All tests passed.")


if __name__ == "__main__":
    main()
