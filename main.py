from enum import IntEnum


class VertexState(IntEnum):
    """Состояния вершины при обходе"""

    UNOPENED = 0
    OPEN = 1
    PROCESSED = 2


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
    pass


def main():
    print(topological_sort([[1], []]))


if __name__ == "__main__":
    main()
