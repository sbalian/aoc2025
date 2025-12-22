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


def num_paths_in_subgraph(graph: nx.DiGraph, source: str, target: str) -> int:
    return len(
        list(
            nx.all_simple_paths(
                graph.subgraph(
                    nx.descendants(graph, source)
                    .intersection(nx.ancestors(graph, target))
                    .union({source, target})
                ),
                source,
                target,
            )
        )
    )


def part2(graph: nx.DiGraph) -> int:
    a = num_paths_in_subgraph(graph, "svr", "fft")
    b = num_paths_in_subgraph(graph, "fft", "dac")
    assert num_paths_in_subgraph(graph, "dac", "fft") == 0
    c = num_paths_in_subgraph(graph, "dac", "out")
    return a * b * c


def main() -> None:
    graph = read_graph("example.txt")
    assert part1(graph) == 5
    graph = read_graph("input.txt")
    assert part1(graph) == 688
    assert part2(graph) == 293263494406608  # takes a minute
    print("All tests passed.")


if __name__ == "__main__":
    main()
