from pathlib import Path


def max_from_left(bank: str) -> int:
    max_pos, max_ = 0, int(bank[0])
    for i in range(len(bank) - 1):
        if (current := int(bank[i])) > max_:
            max_pos, max_ = i, current
    return max_pos


def max_from_right(bank: str, end: int) -> int:
    n = len(bank)
    max_pos, max_ = n - 1, int(bank[n - 1])
    for i in range(n - 1, end, -1):
        if (current := int(bank[i])) > max_:
            max_pos, max_ = i, current
    return max_pos


def max_joltage(bank: str) -> int:
    left = max_from_left(bank)
    right = max_from_right(bank, left)
    return int(f"{bank[left]}{bank[right]}")


def part1(path: str) -> int:
    return sum(
        max_joltage(bank) for bank in Path(path).read_text().strip().splitlines()
    )


def main() -> None:
    assert part1("example.txt") == 357
    assert part1("input.txt") == 17087
    print("All tests passed.")


if __name__ == "__main__":
    main()
