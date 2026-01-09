"""Порівняння шляхів DFS та BFS на графі київського метро."""

from __future__ import annotations

from collections import deque
from typing import Iterable

import networkx as nx

from task1 import build_kyiv_metro_graph


def dfs_path(graph: nx.Graph, start: str, goal: str) -> list[str] | None:
    """
    Пошук шляху за допомогою DFS.

    Використовує стек, відвідані вершини та сортування сусідів для
    детермінованого порядку обходу.
    """
    stack: list[tuple[str, list[str]]] = [(start, [start])]
    visited: set[str] = set()

    while stack:
        node, path = stack.pop()
        if node == goal:
            return path

        if node in visited:
            continue
        visited.add(node)

        neighbors: Iterable[str] = sorted(graph.neighbors(node))
        # Додаємо у зворотному порядку, щоб перший сусід ішов у глибину.
        for neighbor in reversed(list(neighbors)):
            if neighbor not in visited:
                stack.append((neighbor, path + [neighbor]))
    return None


def bfs_path(graph: nx.Graph, start: str, goal: str) -> list[str] | None:
    """
    Пошук шляху за допомогою BFS.

    Використовує чергу та гарантує мінімальну кількість ребер між точками.
    """
    queue: deque[tuple[str, list[str]]] = deque([(start, [start])])
    visited: set[str] = {start}

    while queue:
        node, path = queue.popleft()
        if node == goal:
            return path

        neighbors: Iterable[str] = sorted(graph.neighbors(node))
        for neighbor in neighbors:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, path + [neighbor]))
    return None


def compare_algorithms(graph: nx.Graph, start: str, goal: str) -> None:
    """
    Друкує результати DFS і BFS та пояснює відмінності.
    """
    dfs_result = dfs_path(graph, start, goal)
    bfs_result = bfs_path(graph, start, goal)

    print(f"Початок: {start}")
    print(f"Фініш:  {goal}")
    print("DFS шлях:", " → ".join(dfs_result) if dfs_result else "немає")
    print("BFS шлях:", " → ".join(bfs_result) if bfs_result else "немає")

    if bfs_result and dfs_result:
        print(f"Довжина DFS: {len(dfs_result) - 1} ребер")
        print(f"Довжина BFS: {len(bfs_result) - 1} ребер")
        print(
            "\nBFS мінімізує кількість ребер, тому знаходить найкоротший за "
            "кількістю переходів маршрут. DFS заглиблюється згідно з "
            "порядком сусідів (відсортовані назви станцій), тож шлях може "
            "бути довшим або іншим, навіть коли існують коротші маршрути."
        )


def main() -> None:
    """Точка входу: будує граф і порівнює шляхи DFS/BFS."""
    graph = build_kyiv_metro_graph()
    start = "Сирець"
    goal = "Червоний хутір"
    compare_algorithms(graph, start, goal)


if __name__ == "__main__":
    main()
