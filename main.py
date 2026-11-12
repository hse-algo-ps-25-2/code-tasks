from enum import IntEnum


class VertexState(IntEnum):
    """Состояния вершины при обходе"""

    UNOPENED = 0
    OPEN = 1
    PROCESSED = 2


def shortest_path(graph: list[list[int]], start: int, goal: int) -> list[int]:
    """Возвращает кратчайший по числу рёбер путь из start в goal.

    graph — список списков. Вершины — индексы 0, 1, ..., n - 1.
    graph[i] — концы дуг, выходящих из i. Путь содержит start и goal.
    При start == goal путь состоит из одной вершины. Списки смежности
    при этом всё равно проверяются.

    :param graph: списки смежности орграфа
    :param start: номер начальной вершины
    :param goal: номер конечной вершины
    :raises TypeError: Граф задают списком списков целых номеров вершин
    :raises TypeError: Номер вершины должен быть целым числом
    :raises ValueError: Номер вершины вне диапазона
    :raises UnreachableVertexError: Вершина недостижима
    :return: вершины кратчайшего пути
    """
    pass


def main():
    print(shortest_path([[1], []], 0, 1))


if __name__ == "__main__":
    main()
