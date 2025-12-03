from enum import StrEnum, auto
from pathlib import Path


class Method(StrEnum):
    PART1 = auto()
    PART2 = auto()


FACTORS = {
    2: [1],
    3: [1],
    4: [1, 2],
    5: [1],
    6: [1, 2, 3],
    7: [1],
    8: [1, 2, 4],
    9: [1, 3],
    10: [1, 2, 5],
}


def read_id_range(path: str) -> list[tuple[int, int]]:
    id_range = list[tuple[int, int]]()
    for range_ in Path(path).read_text().strip().split(","):
        a, b = range_.split("-")
        id_range.append((int(a), int(b)))
    return id_range


def id_invalid(id_: str) -> bool:
    if len(id_) % 2 == 1:
        return False
    left = 0
    right = len(id_) // 2
    for i in range(right, len(id_)):
        if id_[i] != id_[left]:
            return False
        left += 1
    return True


def id_invalid_by_size(id_: str, size: int) -> bool:
    previous = id_[:size]
    for i in range(size, len(id_), size):
        current = id_[i : i + size]
        if previous != current:
            return False
        previous = current
    return True


def id_invalid_part2(id_: str) -> bool:
    n = len(id_)
    if n == 1:
        return False
    for f in FACTORS[n]:
        if id_invalid_by_size(id_, f):
            return True
    return False


def sum_of_invalid_ids_in_range(a: int, b: int, method: Method) -> int:
    s = 0
    match method:
        case Method.PART1:
            id_invalid_method = id_invalid
        case Method.PART2:
            id_invalid_method = id_invalid_part2
    for id_ in range(a, b + 1):
        if id_invalid_method(str(id_)):
            s += id_
    return s


def sum_of_invalid_ids(id_ranges: list[tuple[int, int]], method: Method) -> int:
    s = 0
    for a, b in id_ranges:
        s += sum_of_invalid_ids_in_range(a, b, method)
    return s


def main() -> None:
    id_ranges = read_id_range("example.txt")
    assert sum_of_invalid_ids(id_ranges, Method.PART1) == 1227775554
    assert sum_of_invalid_ids(id_ranges, Method.PART2) == 4174379265
    id_ranges = read_id_range("input.txt")
    assert sum_of_invalid_ids(id_ranges, Method.PART1) == 23534117921
    assert sum_of_invalid_ids(id_ranges, Method.PART2) == 31755323497
    print("All tests passed.")


if __name__ == "__main__":
    main()
