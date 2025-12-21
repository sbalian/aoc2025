import bisect
import random
import re
from functools import partial
from itertools import batched
from multiprocessing import Pool, cpu_count
from pathlib import Path

Position = tuple[int, int]

random.seed(42)


def read_red_tile_positions(path: str) -> list[Position]:
    pattern = re.compile(r"^(\d+),(\d+)$", re.MULTILINE)
    return [
        (int(x), int(y)) for x, y in pattern.findall(Path(path).read_text().strip())
    ]


def calculate_area(a: Position, b: Position) -> int:
    return abs(a[0] - b[0]) * abs(a[1] - b[1]) + abs(a[1] - b[1]) + abs(a[0] - b[0]) + 1


def part1(positions: list[Position]) -> int:
    return max(
        calculate_area(positions[i], positions[j])
        for i in range(len(positions))
        for j in range(i)
    )


def find_wall_tiles_and_horizontal_lines(
    positions: list[Position],
) -> tuple[set[Position], list[tuple[Position, Position]]]:
    wall_tiles = set[Position]()
    horizontal_lines = list[tuple[Position, Position]]()
    for start, end in zip(positions, positions[1:] + [positions[0]]):
        if start[0] == end[0]:
            if start[1] < end[1]:
                s, e = start[1], end[1]
            else:
                s, e = end[1], start[1]
            for i in range(s, e + 1):
                wall_tiles.add((start[0], i))
        elif start[1] == end[1]:
            horizontal_lines.append((start, end))
            if start[0] < end[0]:
                s, e = start[0], end[0]
            else:
                s, e = end[0], start[0]
            for i in range(s, e + 1):
                wall_tiles.add((i, start[1]))
        else:
            raise RuntimeError()
    horizontal_lines.sort(key=lambda x: x[0][1])
    return wall_tiles, horizontal_lines


def crosses_horizontal_line(
    point: Position, horizontal_line: tuple[Position, Position]
) -> bool:
    if horizontal_line[0][0] < horizontal_line[1][0]:
        left, right = horizontal_line[0][0], horizontal_line[1][0]
    else:
        left, right = horizontal_line[1][0], horizontal_line[0][0]
    return left < point[0] <= right


def is_tile_inside(
    tile: Position,
    horizontal_lines: list[tuple[Position, Position]],
) -> bool:
    return (
        sum(crosses_horizontal_line(tile, line) for line in horizontal_lines) % 2 != 0
    )


def find_rectangle_outline(a: Position, b: Position) -> list[Position]:
    tiles = list[Position]()

    if a[0] < b[0]:
        range_ = range(a[0], b[0] + 1)
    elif a[0] > b[0]:
        range_ = range(b[0], a[0] + 1)
    else:
        range_ = range(0, 0)
    for i in range_:
        tiles.append((i, a[1]))
        tiles.append((i, b[1]))

    if a[1] < b[1]:
        range_ = range(a[1], b[1] + 1)
    elif a[1] > b[1]:
        range_ = range(b[1], a[1] + 1)
    else:
        range_ = range(0, 0)
    for i in range_:
        tiles.append((a[0], i))
        tiles.append((b[0], i))

    random.shuffle(tiles)
    return tiles


def is_rectangle_inside(
    rectangle_outline: list[Position],
    wall_tiles: set[Position],
    horizontal_lines: list[tuple[Position, Position]],
) -> bool:
    for tile in rectangle_outline:
        if tile in wall_tiles:
            continue
        i = bisect.bisect_right(horizontal_lines, tile[1], key=lambda x: x[0][1])
        if not is_tile_inside(
            tile,
            horizontal_lines[i:],
        ):
            return False
    return True


def is_point_inside_rectangle(
    point: Position, rectangle: tuple[Position, Position]
) -> bool:
    a, b = rectangle
    if a[0] < b[0]:
        x_check = a[0] <= point[0] <= b[0]
    else:
        x_check = b[0] <= point[0] <= a[0]
    if b[1] < a[1]:
        y_check = b[1] <= point[1] <= a[1]
    else:
        y_check = a[1] <= point[1] <= b[1]
    return x_check and y_check


def rectangle_encloses(
    r1: tuple[Position, Position], r2: tuple[Position, Position]
) -> bool:
    return all(is_point_inside_rectangle(x, r1) for x in r2)


def part2_worker(
    pairs: list[tuple[Position, Position]],
    wall_tiles: set[Position],
    horizontal_lines: list[tuple[Position, Position]],
):
    max_area = 0
    rectangles_outside = list[tuple[Position, Position]]()
    for a, b in pairs:
        area_ = calculate_area(a, b)
        if area_ <= max_area:
            continue
        skip = False
        for r in rectangles_outside:
            if rectangle_encloses((a, b), r):
                rectangles_outside.append((a, b))
                skip = True
                break
        if skip:
            continue
        rectangle_outline = find_rectangle_outline(a, b)
        rectangle_inside = is_rectangle_inside(
            rectangle_outline, wall_tiles, horizontal_lines
        )
        if not rectangle_inside:
            rectangles_outside.append((a, b))
        if rectangle_inside and area_ > max_area:
            max_area = area_
    return max_area


def part2(positions: list[Position], serial: bool = False) -> int:
    wall_tiles, horizontal_lines = find_wall_tiles_and_horizontal_lines(positions)
    pairs = [
        (positions[i], positions[j]) for i in range(len(positions)) for j in range(i)
    ]
    if serial:
        return part2_worker(pairs, wall_tiles, horizontal_lines)
    else:
        random.shuffle(pairs)
        cpus = cpu_count()
        with Pool(processes=cpus) as p:
            areas = p.map(
                partial(
                    part2_worker,
                    wall_tiles=wall_tiles,
                    horizontal_lines=horizontal_lines,
                ),
                [list(c) for c in batched(pairs, len(pairs) // cpus)],
            )
        return max(areas)


def main() -> None:
    positions = read_red_tile_positions("example.txt")
    assert part1(positions) == 50
    assert part2(positions, serial=True) == 24
    positions = read_red_tile_positions("input.txt")
    assert part1(positions) == 4781377701
    assert part2(positions) == 1470616992  # takes 90 seconds on 12 cores (M4 Pro)
    print("All tests passed.")


if __name__ == "__main__":
    main()
