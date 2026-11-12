import unittest

from main import shortest_path


class TestShortestPath(unittest.TestCase):
    """Примеры кратчайшего пути"""

    def test_same_vertex(self):
        """Путь из вершины в неё саму не содержит рёбер"""
        self.assertEqual(shortest_path([[0]], 0, 0), [0])

    def test_one_edge(self):
        """Единственная дуга и есть кратчайший путь"""
        self.assertEqual(shortest_path([[1], []], 0, 1), [0, 1])

    def test_not_a_list(self):
        """Орграф передают списком списков"""
        with self.assertRaisesRegex(
            TypeError, "Граф задают списком списков целых номеров вершин"
        ):
            shortest_path(None, 0, 0)


if __name__ == "__main__":
    unittest.main()
