import math
import re
from enum import Enum, auto
from math import prod
from pathlib import Path

Position = tuple[int, int, int]


class Part(Enum):
    ONE = auto()
    TWO = auto()


def read_junction_box_positions(path: str) -> list[Position]:
    return [
        (int(x), int(y), int(z))
        for x, y, z in re.compile(r"^(\d+),(\d+),(\d+)$", re.MULTILINE).findall(
            Path(path).read_text()
        )
    ]


def distance(a: Position, b: Position) -> float:
    return math.sqrt(sum([(a[i] - b[i]) ** 2 for i in range(3)]))


def find_circuit(
    circuits: list[frozenset[Position]], position: Position
) -> frozenset[Position]:
    for circuit in circuits:
        if position in circuit:
            return circuit
    raise ValueError("circuit not found")


def solve(
    junction_box_positions: list[Position],
    num_smallest: int,
    part: Part,
) -> int:
    pairs_and_distances = list[tuple[Position, Position, float]]()
    circuits = [frozenset([position]) for position in junction_box_positions]

    for i in range(len(junction_box_positions)):
        a = junction_box_positions[i]
        j = 0
        while j < i:
            b = junction_box_positions[j]
            pairs_and_distances.append((b, a, distance(a, b)))
            j += 1
    pairs_and_distances.sort(key=lambda x: x[2])

    for a, b, _ in pairs_and_distances[:num_smallest]:
        a_circuit = find_circuit(circuits, a)
        b_circuit = find_circuit(circuits, b)
        if a_circuit == b_circuit:
            continue
        else:
            new_circuit = a_circuit.union(b_circuit)
            circuits.remove(a_circuit)
            circuits.remove(b_circuit)
            circuits.append(new_circuit)
        if part is Part.TWO:
            if len(circuits) == 1:
                return a[0] * b[0]
    if part is Part.TWO:
        raise RuntimeError("increase num_smallest")
    circuits.sort(key=lambda x: len(x), reverse=True)
    return prod((len(c) for c in circuits[:3]))


def main() -> None:
    positions = read_junction_box_positions("example.txt")
    assert solve(positions, 10, Part.ONE) == 40
    assert solve(positions, 1000, Part.TWO) == 25272

    positions = read_junction_box_positions("input.txt")
    assert solve(positions, 1000, Part.ONE) == 330786
    assert solve(positions, 9000, Part.TWO) == 3276581616

    print("All tests passed.")


if __name__ == "__main__":
    main()
