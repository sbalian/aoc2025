from pathlib import Path


def read_ranges_and_ids(path: str) -> tuple[list[tuple[int, int]], list[int]]:
    top, bottom = Path(path).read_text().strip().split("\n\n")
    ranges = list[tuple[int, int]]()
    for range_ in top.splitlines():
        left, right = range_.split("-")
        ranges.append((int(left), int(right)))
    return ranges, [int(id_) for id_ in bottom.splitlines()]


def part1(ids: list[int], ranges: list[tuple[int, int]]) -> int:
    answer = 0
    for id_ in ids:
        for start, end in ranges:
            if start <= id_ <= end:
                answer += 1
                break
    return answer


def part2(ranges: list[tuple[int, int]]) -> int:
    ranges = sorted(ranges, key=lambda x: x[0])
    answer = ranges[0][1] - ranges[0][0] + 1
    previous = ranges[0]
    for i in range(1, len(ranges)):
        current = ranges[i]
        if current[0] >= previous[0] and current[1] <= previous[1]:
            continue
        elif current[0] <= previous[1] and current[1] > previous[1]:
            answer += current[1] - previous[1]
            previous = (previous[0], current[1])
        else:
            answer += current[1] - current[0] + 1
            previous = current
    return answer


def main() -> None:
    ranges, ids = read_ranges_and_ids("example.txt")
    assert part1(ids, ranges) == 3
    assert part2(ranges) == 14
    ranges, ids = read_ranges_and_ids("input.txt")
    assert part1(ids, ranges) == 613
    assert part2(ranges) == 336495597913098
    print("All tests passed.")


if __name__ == "__main__":
    main()
