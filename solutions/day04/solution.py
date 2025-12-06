from functools import cache
from pathlib import Path

Coord = tuple[int, int]


class Grid:
    def __init__(self, path: str):
        self.values = [
            list(line) for line in Path(path).read_text().strip().splitlines()
        ]

    @property
    def width(self) -> int:
        return len(self.values[0])

    @property
    def height(self) -> int:
        return len(self.values)

    @cache
    def neighbours(self, coord: Coord) -> list[Coord]:
        i, j = coord
        return [
            (p, q)
            for p, q in [
                (i, j + 1),
                (i, j - 1),
                (i + 1, j),
                (i - 1, j),
                (i + 1, j + 1),
                (i - 1, j - 1),
                (i + 1, j - 1),
                (i - 1, j + 1),
            ]
            if (0 <= p < self.height) and (0 <= q < self.width)
        ]

    def accessible(self) -> set[Coord]:
        output = set[Coord]()
        for i in range(self.height):
            for j in range(self.width):
                if self.values[i][j] == "@":
                    rolls, to_add = 0, True
                    for p, q in self.neighbours((i, j)):
                        if self.values[p][q] == "@":
                            rolls += 1
                        if rolls == 4:
                            to_add = False
                            break
                    if to_add:
                        output.add((i, j))
        return output

    def remove(self, to_remove: set[Coord]) -> None:
        for i in range(self.height):
            for j in range(self.width):
                if (i, j) in to_remove:
                    self.values[i][j] = "."


def total_removed(grid: Grid) -> int:
    total = 0
    while (num_removed := len(accessible := grid.accessible())) != 0:
        total += num_removed
        grid.remove(accessible)
    return total


def main() -> None:
    grid = Grid("example.txt")
    assert len(grid.accessible()) == 13
    assert total_removed(grid) == 43
    grid = Grid("input.txt")
    assert len(grid.accessible()) == 1464
    assert total_removed(grid) == 8409
    print("All tests passed.")


if __name__ == "__main__":
    main()
