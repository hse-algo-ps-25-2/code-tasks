from enum import IntEnum

from directed_cycle_error import DirectedCycleError
from stack import Stack


class VertexState(IntEnum):
    """Состояния вершины при обходе"""

    UNOPENED = 0
    OPEN = 1
    PROCESSED = 2


def validate_graph(graph: list[list[int]]):
    pass


def visit_depth_first(
    graph: list[list[int]],
    vertex_states: list[VertexState],
    result: list[int],
    start: int,
):
    """
    Обходит компонент связности в глубину

    graph — список списков. Вершины — индексы 0, 1, ..., n - 1.
    vertex_states - состояния вершин графа
    result - формируемый порядок обхода
    start - вершина, с которой начинается обход
    """
    vertex_states[start] = VertexState.OPEN
    vertex_to_process = Stack()
    vertex_to_process.push((start, 0))

    while not vertex_to_process.is_empty():
        vertex, child_num = vertex_to_process.pop()

        if child_num == len(graph[vertex]):
            vertex_states[vertex] = VertexState.PROCESSED
            result.append(vertex)
            continue

        vertex_to_process.push((vertex, child_num + 1))

        child_vertex = graph[vertex][child_num]
        if vertex_states[child_vertex] == VertexState.OPEN:
            raise DirectedCycleError()

        if vertex_states[child_vertex] == VertexState.UNOPENED:
            vertex_states[child_vertex] = VertexState.OPEN
            vertex_to_process.push((child_vertex, 0))


def topological_sort(graph: list[list[int]]) -> list[int]:
    """Возвращает вершины орграфа в топологическом порядке.

    graph — список списков. Вершины — индексы 0, 1, ..., n - 1.
    graph[i] — концы дуг, выходящих из i. Результат содержит каждую вершину
    один раз, и начало каждой дуги стоит в нём раньше конца.

    :param graph: списки смежности орграфа
    :raises TypeError: Граф задают списком списков целых номеров вершин
    :raises ValueError: Номер вершины вне диапазона
    :return: номера вершин в топологическом порядке
    """
    validate_graph(graph)
    vertex_states = [VertexState.UNOPENED for i in range(len(graph))]
    reversed_order = []

    for vertex in range(len(graph)):
        if vertex_states[vertex] == VertexState.UNOPENED:
            visit_depth_first(graph, vertex_states, reversed_order, vertex)

    return reversed_order[::-1]


def main():
    print(topological_sort([[1], []]))


if __name__ == "__main__":
    main()
