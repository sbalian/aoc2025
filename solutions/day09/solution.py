import re
from pathlib import Path

Position = tuple[int, int]


def read_positions(path: str) -> list[Position]:
    pattern = re.compile(r"^(\d+),(\d+)$", re.MULTILINE)
    return [
        (int(x), int(y)) for x, y in pattern.findall(Path(path).read_text().strip())
    ]


def area(a: Position, b: Position) -> int:
    return abs(a[0] - b[0]) * abs(a[1] - b[1]) + abs(a[1] - b[1]) + abs(a[0] - b[0]) + 1


def largest_area(positions: list[Position]) -> int:
    areas = list[int]()
    for i in range(len(positions)):
        j = 0
        while j < i:
            areas.append(area(positions[i], positions[j]))
            j += 1
    return max(areas)


def main() -> None:
    positions = read_positions("example.txt")
    assert largest_area(positions) == 50
    positions = read_positions("input.txt")
    assert largest_area(positions) == 4781377701
    print("All tests passed.")


if __name__ == "__main__":
    main()
