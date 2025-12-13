from collections import defaultdict
from functools import cache
from pathlib import Path

Point = tuple[int, int]


class Grid:
    def __init__(self, path: str):
        self.values = [
            list(line) for line in Path(path).read_text().strip().splitlines()
        ]
        self.height = len(self.values)
        self.width = len(self.values[0])
        self.start = self.find_start()
        self.splitters = self.find_splitters()
        self.sources = self.find_sources()
        self.final_splitters = self.find_final_splitters()

    def find_start(self) -> Point:
        for i in range(self.height):
            for j in range(self.width):
                if self.values[i][j] == "S":
                    return i, j
        raise ValueError("start not found")

    def find_splitters(self) -> list[Point]:
        return [
            (i, j)
            for i in range(self.height)
            for j in range(self.width)
            if self.values[i][j] == "^"
        ]

    def find_sources(self) -> dict[Point, list[Point]]:
        sources = defaultdict[Point, list[Point]](list)
        for splitter in self.splitters:
            i, j = splitter
            k = i - 1
            right_under_source = False
            while k >= 0:
                if self.values[k][j] == ".":
                    k -= 1
                elif self.values[k][j] == "^":
                    break
                else:  # S
                    sources[(i, j)].append((k, j))
                    right_under_source = True
                    break
            if right_under_source:
                continue
            for p in range(i - 1, k, -1):
                if self.values[p][j + 1] == "^":
                    sources[(i, j)].append((p, j + 1))
                if self.values[p][j - 1] == "^":
                    sources[(i, j)].append((p, j - 1))
        return dict(sources)

    @cache
    def splits(self, splitter: Point) -> bool:
        if splitter not in self.sources:
            return False
        if self.sources[splitter] == [self.start]:
            return True
        return any(self.splits(splitter) for splitter in self.sources[splitter])

    def find_final_splitters(self) -> list[Point]:
        final_splitters = list[Point]()
        for splitter in self.splitters:
            final = True
            i, j = splitter
            for k in range(i + 1, self.height):
                if self.values[k][j + 1] == "^" or self.values[k][j - 1] == "^":
                    final = False
                    break
            if final:
                final_splitters.append(splitter)
        return final_splitters


def part1(grid: Grid) -> int:
    return sum(grid.splits(splitter) for splitter in grid.splitters)


def main() -> None:
    grid = Grid("example.txt")
    assert part1(grid) == 21

    grid = Grid("input.txt")
    assert part1(grid) == 1566

    print("All tests passed.")


if __name__ == "__main__":
    main()
