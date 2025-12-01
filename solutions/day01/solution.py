import re
from enum import StrEnum
from pathlib import Path
from typing import NamedTuple


class Orientation(StrEnum):
    LEFT = "L"
    RIGHT = "R"


PATTERN = re.compile(r"^(R|L)(\d+)$", re.MULTILINE)


class Rotation(NamedTuple):
    orientation: Orientation
    distance: int


def read_rotations(path: str) -> list[Rotation]:
    return [
        Rotation(orientation=Orientation(orientation), distance=int(distance))
        for orientation, distance in PATTERN.findall(Path(path).read_text().strip())
    ]


def actual_password(rotations: list[Rotation]) -> int:
    password = 0
    value = 50
    for rotation in rotations:
        if value == 0:
            password += 1
        diff = (
            rotation.distance
            if rotation.orientation is Orientation.RIGHT
            else -rotation.distance
        )
        value = (value + diff) % 100
    return password


def method_0x434C49434B(rotations: list[Rotation]) -> int:
    password = 0
    start = 50
    for rotation in rotations:
        match rotation.orientation:
            case Orientation.RIGHT:
                end = (start + rotation.distance) % 100
                password += (start + rotation.distance) // 100
            case Orientation.LEFT:
                end = (start - rotation.distance) % 100
                password += abs((start - rotation.distance) // 100)
                if start == 0:
                    password -= 1
                if end == 0:
                    password += 1
        start = end
    return password


def main() -> None:
    rotations = read_rotations("example.txt")
    assert actual_password(rotations) == 3
    assert method_0x434C49434B(rotations) == 6

    rotations = read_rotations("input.txt")
    assert actual_password(rotations) == 1064
    assert method_0x434C49434B(rotations) == 6122
    print("All tests passed.")


if __name__ == "__main__":
    main()
