from pathlib import Path

import networkx as nx


def read_graph(path: str) -> nx.DiGraph:
    graph = nx.DiGraph()
    for line in Path(path).read_text().strip().splitlines():
        node, right = line.split(": ")
        neighbors = right.split()
        for neighbor in neighbors:
            graph.add_edge(node, neighbor)
    return graph


def part1(graph: nx.DiGraph) -> int:
    return len(list(nx.all_simple_paths(graph, "you", "out")))


def main() -> None:
    graph = read_graph("example.txt")
    assert part1(graph) == 5
    graph = read_graph("input.txt")
    assert part1(graph) == 688
    print("All tests passed.")


if __name__ == "__main__":
    main()
