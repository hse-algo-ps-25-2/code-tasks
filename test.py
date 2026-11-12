import unittest

from directed_cycle_error import DirectedCycleError
from main import topological_sort


class TestTopologicalSort(unittest.TestCase):
    """Примеры топологической сортировки"""

    def test_single_vertex(self):
        """Одна вершина без дуг уже стоит в топологическом порядке"""
        self.assertEqual(topological_sort([[]]), [0])

    def test_chain(self):
        """Дуга ведёт от более ранней вершины результата к более поздней"""
        self.assertEqual(topological_sort([[1], []]), [0, 1])

    def test_cycle(self):
        """Ориентированный цикл не допускает топологической сортировки"""
        with self.assertRaisesRegex(
            DirectedCycleError, "В орграфе есть ориентированный цикл"
        ):
            topological_sort([[1], [0]])

    def test_not_a_list(self):
        """Орграф передают списком списков"""
        with self.assertRaisesRegex(
            TypeError, "Граф задают списком списков целых номеров вершин"
        ):
            topological_sort(None)


if __name__ == "__main__":
    unittest.main()
