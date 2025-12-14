from collections import defaultdict
from functools import cache
from pathlib import Path
from typing import Literal, NamedTuple

Point = tuple[int, int]


class FinalSplitter(NamedTuple):
    splitter: Point
    multiplier: Literal[1, 2]


class Manifold:
    def __init__(self, path: str):
        self.values = [
            list(line) for line in Path(path).read_text().strip().splitlines()
        ]
        self.height, self.width = len(self.values), len(self.values[0])
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

    def splits(self, splitter: Point) -> bool:
        return splitter in self.sources

    def find_final_splitters(self) -> list[FinalSplitter]:
        final_splitters = list[FinalSplitter]()
        for i, j in self.splitters:
            from_right, from_left = True, True
            for k in range(i + 1, self.height):
                if self.values[k][j + 1] == "^":
                    from_right = False
                if self.values[k][j - 1] == "^":
                    from_left = False
                if not from_right and not from_left:
                    break
            if from_right or from_left:
                multiplier = 1
                if from_right and from_left:
                    multiplier = 2
                final_splitters.append(
                    FinalSplitter(splitter=(i, j), multiplier=multiplier)
                )
        return final_splitters

    @cache
    def paths(self, splitter: Point) -> int:
        sources = self.sources.get(splitter, [])
        if sources == [self.start]:
            return 1
        else:
            return sum(self.paths(source) for source in sources)

    @property
    def num_splits(self) -> int:
        return sum(self.splits(splitter) for splitter in self.splitters)

    @property
    def num_timelines(self) -> int:
        return sum(
            multiplier * self.paths(splitter)
            for splitter, multiplier in self.final_splitters
        )


def main() -> None:
    manifold = Manifold("example.txt")
    assert manifold.num_splits == 21
    assert manifold.num_timelines == 40

    manifold = Manifold("input.txt")
    assert manifold.num_splits == 1566
    assert manifold.num_timelines == 5921061943075

    print("All tests passed.")


if __name__ == "__main__":
    main()
