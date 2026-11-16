from enum import IntEnum, StrEnum
from queue import Queue

from unreachable_vertex_error import UnreachableVertexError


class VertexState(IntEnum):
    """Состояния вершины при обходе"""

    UNOPENED = 0
    OPEN = 1
    PROCESSED = 2

class ErrorMessages(StrEnum):
    """Перечисление сообщений об ошибках"""
    TYPE_ERROR = "Граф задают списком списков целых номеров вершин"
    VALUE_ERROR = "Номер вершины вне диапазона"
    EMPTY_ERROR = "Граф не должен быть пустым"


def validate_graph(graph: list[list[int]]):
    if not isinstance(graph, list):
        raise TypeError(ErrorMessages.TYPE_ERROR)
    if len(graph) == 0:
        raise TypeError(ErrorMessages.EMPTY_ERROR)

    if (
        not isinstance(graph, list)
        or not all(isinstance(sublist, list) for sublist in graph)
        or not all(
            (isinstance(item_of_sublist, int) or isinstance(item_of_sublist, float))
            and not isinstance(item_of_sublist, bool)
            for sublist in graph
            for item_of_sublist in sublist
        )
    ):
        raise TypeError(ErrorMessages.TYPE_ERROR)
    if not all(
        (item_of_sublist >= 0 and item_of_sublist < len(graph))
        for sublist in graph
        for item_of_sublist in sublist
    ):
        raise ValueError(ErrorMessages.VALUE_ERROR)


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
    validate_graph(graph)
    queue = Queue()
    queue.enqueue(start)
    path = []

    if len(path) == 0:
        raise UnreachableVertexError("Вершина недостижима")

    return path


def main():
    print(shortest_path([[1], []], 0, 1))


if __name__ == "__main__":
    main()
