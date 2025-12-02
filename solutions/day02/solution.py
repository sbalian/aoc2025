from pathlib import Path


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


def sum_of_invalid_ids_in_range(a: int, b: int) -> int:
    s = 0
    for id_ in range(a, b + 1):
        if id_invalid(str(id_)):
            s += id_
    return s


def sum_of_invalid_ids(id_ranges: list[tuple[int, int]]) -> int:
    s = 0
    for a, b in id_ranges:
        s += sum_of_invalid_ids_in_range(a, b)
    return s


def main() -> None:
    id_ranges = read_id_range("example.txt")
    assert sum_of_invalid_ids(id_ranges) == 1227775554
    id_ranges = read_id_range("input.txt")
    assert sum_of_invalid_ids(id_ranges) == 23534117921
    print("All tests passed.")


if __name__ == "__main__":
    main()
