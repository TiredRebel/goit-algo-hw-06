"""Побудова та аналіз графа київського метрополітену."""

from __future__ import annotations

import os
import pathlib
import subprocess
import sys

import matplotlib.pyplot as plt
import networkx as nx

# Базові кольори для відображення ліній метро
LINE_COLORS = {
    "Червона": "#d32f2f",
    "Синя": "#1976d2",
    "Зелена": "#388e3c",
}

# Зв'язки між станціями: (зв'язок A, зв'язок B, лінія, тривалість у хвилинах)
CONNECTIONS = [
    # Червона лінія
    ("Академмістечко", "Житомирська", "Червона", 2.5),
    ("Житомирська", "Святошин", "Червона", 2.0),
    ("Святошин", "Нивки", "Червона", 2.0),
    ("Нивки", "Берестейська", "Червона", 2.0),
    ("Берестейська", "Шулявська", "Червона", 2.0),
    ("Шулявська", "Політехнічний інститут", "Червона", 1.8),
    ("Політехнічний інститут", "Вокзальна", "Червона", 1.5),
    ("Вокзальна", "Університет", "Червона", 2.0),
    ("Університет", "Театральна", "Червона", 1.0),
    ("Театральна", "Хрещатик", "Червона", 1.0),
    ("Хрещатик", "Арсенальна", "Червона", 2.2),
    ("Арсенальна", "Дніпро", "Червона", 1.5),
    ("Дніпро", "Гідропарк", "Червона", 2.0),
    ("Гідропарк", "Лівобережна", "Червона", 2.1),
    ("Лівобережна", "Дарниця", "Червона", 2.0),
    ("Дарниця", "Чернігівська", "Червона", 2.4),
    ("Чернігівська", "Лісова", "Червона", 2.0),
    # Синя лінія
    ("Героїв Дніпра", "Мінська", "Синя", 2.0),
    ("Мінська", "Оболонь", "Синя", 1.8),
    ("Оболонь", "Почайна", "Синя", 2.0),
    ("Почайна", "Тараса Шевченка", "Синя", 2.1),
    ("Тараса Шевченка", "Поштова площа", "Синя", 1.5),
    ("Поштова площа", "Майдан Незалежності", "Синя", 1.2),
    ("Майдан Незалежності", "Площа Українських Героїв", "Синя", 1.0),
    ("Площа Українських Героїв", "Олімпійська", "Синя", 1.4),
    ("Олімпійська", "Палац Україна", "Синя", 1.5),
    ("Палац Україна", "Либідська", "Синя", 1.7),
    ("Либідська", "Деміївська", "Синя", 2.0),
    ("Деміївська", "Голосіївська", "Синя", 1.8),
    ("Голосіївська", "Васильківська", "Синя", 2.0),
    ("Васильківська", "Виставковий центр", "Синя", 1.6),
    ("Виставковий центр", "Іподром", "Синя", 1.5),
    ("Іподром", "Теремки", "Синя", 1.8),
    # Зелена лінія
    ("Сирець", "Дорогожичі", "Зелена", 2.0),
    ("Дорогожичі", "Лук'янівська", "Зелена", 2.0),
    ("Лук'янівська", "Золоті ворота", "Зелена", 2.1),
    ("Золоті ворота", "Палац спорту", "Зелена", 1.0),
    ("Палац спорту", "Кловська", "Зелена", 1.2),
    ("Кловська", "Печерська", "Зелена", 1.4),
    ("Печерська", "Дружби народів", "Зелена", 1.7),
    ("Дружби народів", "Видубичі", "Зелена", 2.1),
    ("Видубичі", "Славутич", "Зелена", 3.0),
    ("Славутич", "Осокорки", "Зелена", 2.0),
    ("Осокорки", "Позняки", "Зелена", 1.5),
    ("Позняки", "Харківська", "Зелена", 1.5),
    ("Харківська", "Вирлиця", "Зелена", 1.8),
    ("Вирлиця", "Бориспільська", "Зелена", 1.7),
    ("Бориспільська", "Червоний хутір", "Зелена", 2.0),
]


def build_kyiv_metro_graph() -> nx.Graph:
    """
    Створює неорієнтований граф на основі наближених даних київського метро.
    """
    graph = nx.Graph()
    for station_from, station_to, line_name, duration in CONNECTIONS:
        graph.add_edge(
            station_from,
            station_to,
            line=line_name,
            duration_minutes=duration,
        )
    return graph


def calculate_basic_metrics(graph: nx.Graph) -> dict[str, float]:
    """Розраховує базові характеристики графа для швидкої оцінки мережі."""
    num_nodes = graph.number_of_nodes()
    degrees = dict(graph.degree())
    average_degree = (
        sum(degrees.values()) / num_nodes if num_nodes else 0.0
    )
    return {
        "num_nodes": num_nodes,
        "num_edges": graph.number_of_edges(),
        "density": round(nx.density(graph), 4),
        "average_degree": round(average_degree, 2),
        "max_degree": max(degrees.values()) if degrees else 0,
    }


def visualize_graph(graph: nx.Graph, output_path: pathlib.Path) -> None:
    """Візуалізує граф та зберігає його у вигляді зображення."""
    pos = nx.spring_layout(graph, seed=42)
    lines = nx.get_edge_attributes(graph, "line")
    edge_colors = [
        LINE_COLORS.get(lines[(u, v)], "#9e9e9e")
        for u, v in graph.edges()
    ]

    plt.figure(figsize=(12, 9))
    nx.draw_networkx(
        graph,
        pos=pos,
        with_labels=True,
        node_color="#f5f5f5",
        edge_color=edge_colors,
        font_size=8,
        node_size=900,
        linewidths=1.0,
    )

    edge_labels = {
        (u, v): f'{lines[(u, v)]} ({graph[u][v]["duration_minutes"]} хв)'
        for u, v in graph.edges()
    }
    nx.draw_networkx_edge_labels(
        graph,
        pos=pos,
        edge_labels=edge_labels,
        font_size=7,
        label_pos=0.5,
    )

    plt.tight_layout()
    output_path = output_path.resolve()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_path, dpi=200)
    plt.close()
    print(f"Зображення графа збережено у файлі: {output_path}")


def open_image(output_path: pathlib.Path) -> None:
    """Відкриває створене зображення у стандартній програмі ОС."""
    try:
        if sys.platform.startswith("win"):
            os.startfile(output_path)  # type: ignore[attr-defined]
        elif sys.platform == "darwin":
            subprocess.run(["open", output_path], check=False)
        else:
            subprocess.run(["xdg-open", output_path], check=False)
    except Exception as error:  # noqa: BLE001
        print(f"Не вдалося автоматично відкрити зображення: {error}")


def print_metrics(metrics: dict[str, float]) -> None:
    """Друкує метрики у читабельному форматі."""
    print("Базові характеристики мережі:")
    for key, value in metrics.items():
        print(f"- {key}: {value}")


def main() -> None:
    """Точка входу для демонстрації створення та аналізу графа."""
    metro_graph = build_kyiv_metro_graph()
    metrics = calculate_basic_metrics(metro_graph)
    print_metrics(metrics)
    output_path = pathlib.Path("artifacts/kyiv_metro_graph.png")
    visualize_graph(metro_graph, output_path)
    open_image(output_path)


if __name__ == "__main__":
    main()
