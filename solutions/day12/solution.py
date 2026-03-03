import re
from pathlib import Path


def solution(situation: str) -> int:
    sections = Path(situation).read_text().split("\n\n")
    shapes = [section.splitlines()[1:] for section in sections[:-1]]
    shape_areas = {
        i: sum(
            shapes[i][j][k] == "#"
            for j in range(len(shapes[i]))
            for k in range(len(shapes[i][0]))
        )
        for i in range(len(shapes))
    }
    return sum(
        sum(shape_areas[i] * int(q) for i, q in enumerate(str(sq).split()))
        <= int(width) * int(length)
        for width, length, sq in re.findall(r"(\d+)x(\d+): (.+)", sections[-1])
    )


def main() -> None:
    assert solution("input.txt") == 524
    print("All tests passed.")


if __name__ == "__main__":
    main()
