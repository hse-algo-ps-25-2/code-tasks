import unittest

from directed_cycle_error import DirectedCycleError
from main import topological_sort

DIRECTED_CYCLE_ERROR_MESSAGE = "В орграфе есть ориентированный цикл"
TYPE_ERROR_MESSAGE = "Граф задают списком списков целых номеров вершин"
VALUE_ERROR_MESSAGE = "Номер вершины вне диапазона"


class TestTopologicalSort(unittest.TestCase):
    """Примеры топологической сортировки"""

    def assert_topological_order(self, graph, order):
        """Результат сортировки содержит каждую вершину ровно один раз, и начало
        каждой дуги стоит в списке раньше конца
        """
        self.assertEqual(len(order), len(graph))
        self.assertEqual(set(order), set(range(len(graph))))

        vertex_positions = {vertex: index for index, vertex in enumerate(order)}

        for source, neighbors in enumerate(graph):
            for target in neighbors:
                self.assertLess(vertex_positions[source], vertex_positions[target])

    def test_empty_graph(self):
        """Результат топологической сортировки пустого графа - пустой список"""
        self.assertEqual(topological_sort([]), [])

    def test_single_vertex(self):
        """Одна вершина без дуг уже стоит в топологическом порядке"""
        self.assertEqual(topological_sort([[]]), [0])

    def test_isolated_vertices(self):
        """Для нескольких изолированных вершин порядок сортировки произвольный"""
        graph = [[], []]
        self.assert_topological_order(graph, topological_sort(graph))

    def test_chain(self):
        """Дуга ведёт от более ранней вершины результата к более поздней"""
        self.assertEqual(topological_sort([[1], []]), [0, 1])

    def test_several_correct_orders(self):
        """Проверка сортировки графа, для которого допустимо
        несколько топологических порядков
        """
        graph = [[1, 2], [], []]
        self.assert_topological_order(graph, topological_sort(graph))

    def test_diamond(self):
        """Граф, в котором две дуги сходятся в одну вершину"""
        graph = [[1, 2], [3], [3], []]
        self.assert_topological_order(graph, topological_sort(graph))

    def test_several_components(self):
        """Граф из нескольких компонент связности"""
        graph = [[1], [], [3], []]
        self.assert_topological_order(graph, topological_sort(graph))

    def test_duplicate_edges(self):
        """Граф, содержащий кратные дуги"""
        graph = [
            [1, 1],
            [2, 2],
            [],
        ]
        self.assert_topological_order(graph, topological_sort(graph))

    def test_cycle(self):
        """Ориентированный цикл не допускает топологической сортировки"""
        with self.assertRaisesRegex(DirectedCycleError, DIRECTED_CYCLE_ERROR_MESSAGE):
            topological_sort([[1], [0]])

    def test_loop(self):
        """Наличие петли не допускает топологической сортировки"""
        with self.assertRaisesRegex(DirectedCycleError, DIRECTED_CYCLE_ERROR_MESSAGE):
            topological_sort([[1], [1, 2], []])

    def test_cycle_several_components(self):
        """Ориентированный цикл в одной из компонент связности
        не допускает топологической сортировки
        """
        with self.assertRaisesRegex(DirectedCycleError, DIRECTED_CYCLE_ERROR_MESSAGE):
            topological_sort([[1], [], [3], [2], [5], []])

    def test_not_a_list(self):
        """Орграф передают списком списков"""
        with self.assertRaisesRegex(TypeError, TYPE_ERROR_MESSAGE):
            topological_sort(None)

    def test_argument_is_list(self):
        """Аргумент topological_sort должен быть типа list"""
        for value in 0, "", False, (), {}:
            with self.subTest(value=value):
                with self.assertRaisesRegex(TypeError, TYPE_ERROR_MESSAGE):
                    topological_sort(value)

    def test_list_items_are_lists(self):
        """Элементы внешнего списка должны быть типа list"""
        for value in 0, "", False, (), {}, None:
            with self.subTest(value=value):
                with self.assertRaisesRegex(TypeError, TYPE_ERROR_MESSAGE):
                    topological_sort([[], value, []])

    def test_vertices_numbers_are_int(self):
        """Номера вершин должны быть типа int"""
        for value in 0.0, "", False, (), {}, None:
            with self.subTest(value=value):
                with self.assertRaisesRegex(TypeError, TYPE_ERROR_MESSAGE):
                    topological_sort([[], [value], []])

    def test_negative_vertices_numbers(self):
        """Номера вершин не могут быть отрицательными"""
        with self.assertRaisesRegex(ValueError, VALUE_ERROR_MESSAGE):
            topological_sort([[1], [2], [-1]])

    def test_vertices_numbers_out_of_range(self):
        """Номера вершин не могут быть больше, чем кол-во вершин минус один"""
        with self.assertRaisesRegex(ValueError, VALUE_ERROR_MESSAGE):
            topological_sort([[1], [2], [3]])


if __name__ == "__main__":
    unittest.main()
