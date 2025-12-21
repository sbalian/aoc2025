from collections import defaultdict
from pathlib import Path

from ortools.sat.python import cp_model


class Machine:
    def __init__(self, manual_line: str):
        components = manual_line.split()
        self.lights = [1 if char == "#" else 0 for char in components.pop(0)[1:-1]]
        self.joltages = [int(x) for x in components.pop(-1)[1:-1].split(",")]
        self.num_buttons = len(components)
        light_to_buttons = defaultdict[int, list[int]](list)
        for b, button in enumerate(components):
            for light in [int(x) for x in button[1:-1].split(",")]:
                light_to_buttons[light].append(b)
        self.light_to_buttons = dict(
            sorted(light_to_buttons.items(), key=lambda x: x[0])
        )

    def part1(self) -> int:
        model = cp_model.CpModel()
        b = [model.new_int_var(0, 100, f"b{i}") for i in range(self.num_buttons)]
        for i, (light_value, buttons) in enumerate(
            zip(
                self.lights,
                [
                    map(
                        lambda x: b[x],
                        v,
                    )
                    for v in self.light_to_buttons.values()
                ],
            )
        ):
            model.add((ais := model.new_int_var(0, 100, f"a{i}_s")) == sum(buttons))
            model.add_modulo_equality(light_value, ais, 2)
        model.minimize(sum(b))
        if msg := model.validate():
            raise RuntimeError(msg)
        solver = cp_model.CpSolver()
        status = solver.solve(model)
        if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
            return int(solver.objective_value)
        else:
            raise RuntimeError("No solution found.")

    def part2(self) -> int:
        model = cp_model.CpModel()
        b = [model.new_int_var(0, 200, f"b{i}") for i in range(self.num_buttons)]
        for joltage, buttons in zip(
            self.joltages,
            [
                map(
                    lambda x: b[x],
                    v,
                )
                for v in self.light_to_buttons.values()
            ],
        ):
            model.add(sum(buttons) == joltage)
        model.minimize(sum(b))
        if msg := model.validate():
            raise RuntimeError(msg)
        solver = cp_model.CpSolver()
        status = solver.solve(model)
        if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
            return int(solver.objective_value)
        else:
            raise RuntimeError("No solution found.")


def read_machines(path: str) -> list[Machine]:
    return [Machine(line) for line in Path(path).read_text().strip().splitlines()]


def part1(machines: list[Machine]) -> int:
    return sum(machine.part1() for machine in machines)


def part2(machines: list[Machine]) -> int:
    return sum(machine.part2() for machine in machines)


def main() -> None:
    machines = read_machines("example.txt")
    assert part1(machines) == 7
    assert part2(machines) == 33
    machines = read_machines("input.txt")
    assert part1(machines) == 455
    assert part2(machines) == 16978
    print("All tests passed.")


if __name__ == "__main__":
    main()
