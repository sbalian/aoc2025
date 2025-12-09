from pathlib import Path


def read_banks(path) -> list[str]:
    return [bank for bank in Path(path).read_text().strip().splitlines()]

def max_from_left(bank: str, start: int, end: int) -> int:
    max_pos, max_ = start, int(bank[start])
    for i in range(start, end):
        if (current := int(bank[i])) > max_:
            max_pos, max_ = i, current
    return max_pos


def max_joltage(bank: str, num_digits: int) -> int:
    digits, start = "", 0
    for i in range(num_digits-1, -1, -1):
        start = max_from_left(bank, start, len(bank) - i)
        digits += bank[start]
        start += 1
    return int(digits)
        

def solve(banks: list[str], num_digits: int) -> int:
    return sum(
        max_joltage(bank, num_digits) for bank in banks
    )


def main() -> None:
    banks = read_banks("example.txt")
    assert solve(banks, 2) == 357
    assert solve(banks, 12) == 3121910778619

    banks = read_banks("input.txt")
    assert solve(banks, 2) == 17087
    assert solve(banks, 12) == 169019504359949
    print("All tests passed.")


if __name__ == "__main__":
    main()
