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

    GRAPH_TYPE_ERROR = "Граф задают списком списков целых номеров вершин"
    GRAPH_EMPTY_ERROR = "Граф не должен быть пустым"
    VERTEX_VALUE_ERROR = "Номер вершины вне диапазона"
    VERTEX_TYPE_ERROR = "Номер вершины должен быть целым числом"


def _validate_graph(graph: list[list[int]], start: int, goal: int):
    if not isinstance(graph, list):
        raise TypeError(ErrorMessages.GRAPH_TYPE_ERROR)
    if len(graph) == 0:
        raise TypeError(ErrorMessages.GRAPH_EMPTY_ERROR)

    vertex_count = len(graph)

    for edge in graph:
        _validate_edge(edge, vertex_count)
    
    _validate_vertex(start, vertex_count, ErrorMessages.VERTEX_TYPE_ERROR)
    _validate_vertex(goal, vertex_count, ErrorMessages.VERTEX_TYPE_ERROR)

def _validate_edge(edge: list[int], vertex_count: int):
    if not isinstance(edge, list):
        raise TypeError(ErrorMessages.GRAPH_TYPE_ERROR)

    for vertex in edge:
        _validate_vertex(vertex, vertex_count, ErrorMessages.GRAPH_TYPE_ERROR)


def _validate_vertex(vertex: int, vertex_count: int, type_error_message: ErrorMessages):
    if not isinstance(vertex, int) or isinstance(vertex, bool):
        raise TypeError(type_error_message)
    if not (vertex >= 0 and vertex < vertex_count):
        raise ValueError(ErrorMessages.VERTEX_VALUE_ERROR)


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
    _validate_graph(graph, start, goal)
    vertex_count = len(graph)

    queue = Queue()
    queue.enqueue(start)

    parent: list[int | None] = [None] * vertex_count
    vertex_states = [VertexState.UNOPENED] * vertex_count
    vertex_states[start] = VertexState.OPEN

    while not queue.is_empty():
        vertex = queue.dequeue()

        if vertex == goal:
            break

        for sibling_vertex in graph[vertex]:
            if vertex_states[sibling_vertex] == VertexState.UNOPENED:
                vertex_states[sibling_vertex] = VertexState.OPEN
                parent[sibling_vertex] = vertex
                queue.enqueue(sibling_vertex)

        vertex_states[vertex] = VertexState.PROCESSED

    if vertex_states[goal] == VertexState.UNOPENED:
        raise UnreachableVertexError()

    result = []
    node = goal

    while node is not None:
        result.append(node)
        node = parent[node]

    result.reverse()

    return result


def main():
    print(shortest_path([[1], []], 0, 1))


if __name__ == "__main__":
    main()
