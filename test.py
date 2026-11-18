import unittest

from main import shortest_path
from unreachable_vertex_error import UnreachableVertexError


class TestShortestPath(unittest.TestCase):
    """Примеры кратчайшего пути"""

    def test_same_vertex(self):
        """Путь из вершины в неё саму не содержит рёбер."""
        self.assertEqual(shortest_path([[0]], 0, 0), [0])

    def test_one_edge(self):
        """Единственная дуга и есть кратчайший путь."""
        self.assertEqual(shortest_path([[1], []], 0, 1), [0, 1])

    def test_shortest_path(self):
        """Выбирается путь с наименьшим количеством рёбер."""
        graph = [[1, 2], [3], [4], [5], [5], []]
        self.assertEqual(shortest_path(graph, 0, 5), [0, 1, 3, 5])

    def test_direct_path(self):
        """Прямая дуга предпочтительнее пути через другие вершины."""
        graph = [[1, 2], [2], []]
        self.assertEqual(shortest_path(graph, 0, 2), [0, 2])

    def test_multiple_shortest_paths(self):
        """Допускается любой из нескольких кратчайших путей."""
        graph = [[1, 2], [3], [3], []]
        result = shortest_path(graph, 0, 3)

        self.assertIn(result, [[0, 1, 3], [0, 2, 3]])

    def test_cycle(self):
        """Наличие цикла не мешает поиску пути."""
        graph = [[1], [2], [0, 3], []]
        self.assertEqual(shortest_path(graph, 0, 3), [0, 1, 2, 3])

    def test_self_loop(self):
        """Петля не мешает поиску кратчайшего пути."""
        graph = [[0, 1], []]
        self.assertEqual(shortest_path(graph, 0, 1), [0, 1])

    def test_directed_graph(self):
        """Дуги учитываются только в заданном направлении."""
        graph = [[1], [], [0]]

        with self.assertRaisesRegex(UnreachableVertexError, "Вершина недостижима"):
            shortest_path(graph, 1, 0)

    def test_unreachable_vertex(self):
        """Недостижимая вершина вызывает исключение."""
        graph = [[1], [0], []]

        with self.assertRaisesRegex(UnreachableVertexError, "Вершина недостижима"):
            shortest_path(graph, 0, 2)

    def test_empty_adjacency_lists(self):
        """Пустые списки смежности допустимы."""
        self.assertEqual(shortest_path([[], [2], []], 1, 2), [1, 2])

    def test_not_a_list(self):
        """Граф должен быть списком."""
        with self.assertRaisesRegex(
            TypeError, "Граф задают списком списков целых номеров вершин"
        ):
            shortest_path(None, 0, 0)

    def test_empty_list(self):
        """Граф не должен быть пустым."""
        with self.assertRaisesRegex(TypeError, "Граф не должен быть пустым"):
            shortest_path([], 0, 0)

    def test_edge_not_a_list(self):
        """Список смежности должен быть списком."""
        with self.assertRaisesRegex(
            TypeError, "Граф задают списком списков целых номеров вершин"
        ):
            shortest_path([None], 0, 0)

    def test_invalid_vertex_type(self):
        """Номер вершины в списке смежности должен быть целым числом."""
        with self.assertRaisesRegex(
            TypeError, "Граф задают списком списков целых номеров вершин"
        ):
            shortest_path([[1.5], []], 0, 0)

    def test_boolean_vertex(self):
        """Bool не считается допустимым номером вершины."""
        with self.assertRaisesRegex(
            TypeError, "Граф задают списком списков целых номеров вершин"
        ):
            shortest_path([[True]], 0, 0)

    def test_invalid_value_vertex(self):
        """Номер вершины в списке смежности должен быть в диапазоне."""
        with self.assertRaisesRegex(ValueError, "Номер вершины вне диапазона"):
            shortest_path([[2]], 0, 0)

    def test_negative_vertex(self):
        """Отрицательный номер вершины недопустим."""
        with self.assertRaisesRegex(ValueError, "Номер вершины вне диапазона"):
            shortest_path([[-1]], 0, 0)

    def test_invalid_start_type(self):
        """Start должен быть целым числом."""
        with self.assertRaisesRegex(
            TypeError, "Номер вершины должен быть целым числом"
        ):
            shortest_path([[0]], 0.5, 0)

    def test_invalid_goal_type(self):
        """Goal должен быть целым числом."""
        with self.assertRaisesRegex(
            TypeError, "Номер вершины должен быть целым числом"
        ):
            shortest_path([[0]], 0, "0")

    def test_boolean_start(self):
        """Bool не считается допустимым номером start."""
        with self.assertRaisesRegex(
            TypeError, "Номер вершины должен быть целым числом"
        ):
            shortest_path([[0]], True, 0)

    def test_boolean_goal(self):
        """Bool не считается допустимым номером goal."""
        with self.assertRaisesRegex(
            TypeError, "Номер вершины должен быть целым числом"
        ):
            shortest_path([[0]], 0, False)

    def test_start_out_of_range(self):
        """Start должен находиться в диапазоне вершин графа."""
        with self.assertRaisesRegex(ValueError, "Номер вершины вне диапазона"):
            shortest_path([[0]], -1, 0)

    def test_goal_out_of_range(self):
        """Goal должен находиться в диапазоне вершин графа."""
        with self.assertRaisesRegex(ValueError, "Номер вершины вне диапазона"):
            shortest_path([[0]], 0, 1)

    def test_graph_validation_when_start_equals_goal(self):
        """При совпадении start и goal граф всё равно проверяется."""
        with self.assertRaisesRegex(
            TypeError, "Граф задают списком списков целых номеров вершин"
        ):
            shortest_path([[0], [True]], 0, 0)


if __name__ == "__main__":
    unittest.main()
