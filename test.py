import unittest

from doubly_linked_list import DoublyLinkedList


class TestDoublyLinkedList(unittest.TestCase):
    """Набор тестов для класса DoublyLinkedList."""

    def test_empty_init(self):
        """Новый список пустой: длина 0, head и tail = None."""
        lst = DoublyLinkedList()
        self.assertEqual(len(lst), 0)
        self.assertIsNone(lst.head)
        self.assertIsNone(lst.tail)

    def test_append_one(self):
        """append добавляет один элемент в конец."""
        lst = DoublyLinkedList()
        lst.append(10)
        self.assertEqual(len(lst), 1)
        self.assertEqual(list(lst), [10])

    def test_append_many(self):
        """append несколько раз сохраняет порядок элементов."""
        lst = DoublyLinkedList()
        for val in [1, 2, 3]:
            lst.append(val)
        self.assertEqual(len(lst), 3)
        self.assertEqual(list(lst), [1, 2, 3])

    def test_insert_middle(self):
        """insert вставляет элемент в середину списка."""
        lst = DoublyLinkedList()
        for val in [1, 3]:
            lst.append(val)
        lst.insert(1, 2)
        self.assertEqual(list(lst), [1, 2, 3])

    def test_index_found(self):
        """index возвращает индекс первого найденного элемента."""
        lst = DoublyLinkedList()
        for val in ["a", "b", "c"]:
            lst.append(val)
        self.assertEqual(lst.index("b"), 1)

    def test_iteration(self):
        """Итерация по списку возвращает значения от головы к хвосту."""
        lst = DoublyLinkedList()
        for val in [1, 2, 3]:
            lst.append(val)
        self.assertEqual([x for x in lst], [1, 2, 3])

    def test_reversed(self):
        """Обратный обход возвращает значения от хвоста к голове."""
        lst = DoublyLinkedList()
        for val in [1, 2, 3]:
            lst.append(val)
        self.assertEqual([x for x in reversed(lst)], [3, 2, 1])


if __name__ == "__main__":
    unittest.main()
