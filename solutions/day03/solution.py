from pathlib import Path


def batteries_for_max_joltage(bank: str) -> int:
    n = len(bank)
    max_ = 1
    for i in range(n):
        j = 0
        while j < i:
            current = int(f"{bank[j]}{bank[i]}")
            if current > max_:
                max_ = current
            j += 1
    return max_


def part1(path: str) -> int:
    j = 0
    for bank in Path(path).read_text().strip().splitlines():
        m = batteries_for_max_joltage(bank)
        j += m
    return j


def main() -> None:
    assert part1("example.txt") == 357
    assert part1("input.txt") == 17087
    print("All tests passed.")


if __name__ == "__main__":
    main()
