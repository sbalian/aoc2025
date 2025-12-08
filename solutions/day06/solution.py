import re
from math import prod
from pathlib import Path


def part1(path: str) -> int:
    lines = Path(path).read_text().strip().splitlines()
    numbers, operations = (
        [
            [int(entry) for entry in re.findall(r"\d+", lines[i])]
            for i in range(len(lines) - 1)
        ],
        [str(entry) for entry in re.findall(r"[+*]", lines[-1])],
    )
    transposed_numbers = [
        [numbers[j][i] for j in range(len(numbers))] for i in range(len(numbers[0]))
    ]
    return sum(
        sum(row) if operation == "+" else prod(row)
        for row, operation in zip(transposed_numbers, operations, strict=True)
    )


def part2(path: str) -> int:
    answer = 0
    grid = [list(row) for row in Path(path).read_text().splitlines()]
    current = list[int]([])
    for row in reversed(
        ["".join([grid[j][i] for j in range(len(grid))]) for i in range(len(grid[0]))]
    ):
        if row.strip():
            if (add := row.endswith("+")) or row.endswith("*"):
                current.append(int(row[:-1]))
                answer += sum(current) if add else prod(current)
                current = list[int]([])
            else:
                current.append(int(row))
    return answer


def main() -> None:
    assert part1("example.txt") == 4277556
    assert part1("input.txt") == 4648618073226
    assert part2("example.txt") == 3263827
    assert part2("input.txt") == 7329921182115
    print("All tests passed.")


if __name__ == "__main__":
    main()
