"""Найкоротші шляхи в графі метро за алгоритмом Дейкстри."""

from __future__ import annotations

from typing import Dict, Iterable, Tuple

import networkx as nx

from task1 import build_kyiv_metro_graph

PathInfo = Dict[str, Tuple[float, list[str]]]
AllPairsPaths = Dict[str, PathInfo]


def dijkstra_all_pairs(
    graph: nx.Graph, weight: str = "duration_minutes"
) -> AllPairsPaths:
    """
    Обчислює найкоротші шляхи між усіма парами вершин.

    Використовує вбудовану реалізацію Дейкстри з NetworkX для кожної
    початкової вершини, повертаючи довжину маршруту та шлях.
    """
    all_paths: AllPairsPaths = {}
    for source in graph.nodes():
        distances, paths = nx.single_source_dijkstra(
            graph, source=source, weight=weight
        )
        all_paths[source] = {
            target: (distances[target], paths[target])
            for target in distances
        }
    return all_paths


def print_shortest_paths(
    all_paths: AllPairsPaths, max_targets: int | None = None
) -> None:
    """
    Друкує шляхи для кожної вершини. Параметр max_targets дозволяє
    обмежити кількість виведених цілей для читабельності.
    """
    for source in sorted(all_paths):
        print(f"\nВід {source}:")
        targets: Iterable[str] = sorted(all_paths[source])
        if max_targets:
            targets = list(targets)[:max_targets]
        for target in targets:
            distance, path = all_paths[source][target]
            path_str = " → ".join(path)
            print(f"- до {target}: {distance:.1f} хв | {path_str}")


def main() -> None:
    """Точка входу: будує граф і виводить усі найкоротші шляхи."""
    graph = build_kyiv_metro_graph()
    all_paths = dijkstra_all_pairs(graph)
    print_shortest_paths(all_paths)


if __name__ == "__main__":
    main()
