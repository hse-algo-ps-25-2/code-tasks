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
        self.assertEqual(lst.head.value, 10)
        self.assertIs(lst.head, lst.tail)
        self.assertIsNone(lst.head.prev)
        self.assertIsNone(lst.head.next)

    def test_append_many(self):
        """append несколько раз сохраняет порядок элементов."""
        lst = DoublyLinkedList()
        for val in [1, 2, 3]:
            lst.append(val)

        self.assertIsNone(lst.head.prev)
        self.assertIsNone(lst.tail.next)
        self.assertIs(lst.head.next.prev, lst.head)
        self.assertIs(lst.head.next.next, lst.tail)
        self.assertIs(lst.tail.prev.next, lst.tail)
        self.assertEqual(len(lst), 3)
        self.assertEqual(list(lst), [1, 2, 3])

    def test_insert_middle(self):
        """insert вставляет элемент в середину списка."""
        lst = DoublyLinkedList()
        for val in [1, 3]:
            lst.append(val)
        lst.insert(1, 2)
        self.assertIs(lst.head.next.prev, lst.head)
        self.assertIs(lst.tail.prev.next, lst.tail)
        self.assertEqual(list(lst), [1, 2, 3])

    def test_insert_in_empty_list(self):
        """insert вставляет элемент в пустой список."""
        lst = DoublyLinkedList()
        lst.insert(0, 31)
        self.assertEqual(list(lst), [31])
        self.assertIs(lst.head, lst.tail)
        self.assertIsNone(lst.head.prev)
        self.assertIsNone(lst.head.next)

    def test_insert_zero_index(self):
        """insert вставляет элемент в начало списка."""
        lst = DoublyLinkedList()
        for val in [1, 3]:
            lst.append(val)
        lst.insert(0, 0)
        self.assertEqual(list(lst), [0, 1, 3])

    def test_insert_last_index(self):
        """insert вставляет элемент в конец списка."""
        lst = DoublyLinkedList()
        for val in [1, 3]:
            lst.append(val)
        lst.insert(2, 4)
        self.assertEqual(lst.tail.value, 4)
        self.assertIsNone(lst.tail.next)
        self.assertEqual(lst.tail.prev.value, 3)
        self.assertEqual(len(lst), 3)
        self.assertEqual(list(lst), [1, 3, 4])

    def test_insert_after_last_index(self):
        """проверяем исключение при вызове insert с некорректным индексом"""
        lst = DoublyLinkedList()

        for val in [1, 2, 3]:
            lst.append(val)

        self.assertRaises(IndexError, lst.insert, 4, 5)

    def test_str(self):
        """проверяем трансформацию списка в строку"""
        lst = DoublyLinkedList()

        for val in [1, 2, 3]:
            lst.append(val)

        self.assertEqual(str(lst), "[1 <-> 2 <-> 3]")

    def test_str_empty(self):
        """проверяем трансформацию пустого списка в строку"""
        lst = DoublyLinkedList()

        self.assertEqual(str(lst), "[]")

    def test_remove(self):
        """проверяем удаление элемента из списка"""
        lst = DoublyLinkedList()
        for val in [1, 2, 3]:
            lst.append(val)
        lst.remove(2)
        self.assertEqual(list(lst), [1, 3])
        self.assertEqual(lst.head.value, 1)
        self.assertEqual(lst.tail.value, 3)
        self.assertIs(lst.head.next, lst.tail)
        self.assertIs(lst.tail.prev, lst.head)
        self.assertIsNone(lst.head.prev)
        self.assertIsNone(lst.tail.next)

    def test_insert_append(self):
        """insert -> append"""
        lst = DoublyLinkedList()
        lst.insert(0, 1)
        lst.append(2)
        self.assertEqual(list(lst), [1, 2])

    def test_insert_negative_index(self):
        """бросает исключение при insert с негативным индексом"""
        lst = DoublyLinkedList()
        self.assertRaises(IndexError, lst.insert, -1, 1)

    def test_remove_last(self):
        """проверяем удаление элемента из списка (последний)"""
        lst = DoublyLinkedList()
        for val in [1, 2, 3]:
            lst.append(val)
        lst.remove(3)
        self.assertEqual(list(lst), [1, 2])
        self.assertEqual(lst.tail.value, 2)
        self.assertIsNone(lst.tail.next)
        self.assertIs(lst.tail.prev, lst.head)
        self.assertIs(lst.head.next, lst.tail)

    def test_remove_first(self):
        """проверяем удаление элемента из списка (первый)"""
        lst = DoublyLinkedList()
        for val in [1, 2, 3]:
            lst.append(val)
        lst.remove(1)
        self.assertEqual(list(lst), [2, 3])
        self.assertEqual(lst.head.value, 2)
        self.assertIsNone(lst.head.prev)
        self.assertIs(lst.head.next, lst.tail)
        self.assertIs(lst.tail.prev, lst.head)

    def test_remove_wrong_value(self):
        """удаление несуществующего элемента бросает исключение"""
        lst = DoublyLinkedList()
        for val in [1, 2, 3]:
            lst.append(val)
        self.assertRaises(ValueError, lst.remove, 5)

    def test_remove_only_first_value(self):
        """удаляет только первое вхождение"""
        lst = DoublyLinkedList()
        for val in [1, 1, 1]:
            lst.append(val)
        lst.remove(1)
        self.assertEqual(len(lst), 2)
        self.assertEqual(list(lst), [1, 1])

    def test_remove_only_element(self):
        """проверяем удаление единственного элемента"""
        lst = DoublyLinkedList()
        lst.append(10)

        lst.remove(10)

        self.assertEqual(len(lst), 0)
        self.assertIsNone(lst.head)
        self.assertIsNone(lst.tail)
        self.assertEqual(list(lst), [])

    def test_remove_from_empty_list(self):
        """проверяем удаление из пустого"""
        lst = DoublyLinkedList()

        self.assertRaises(ValueError, lst.remove, 10)

    def test_clear_list(self):
        """проверяем очистку списка"""
        lst = DoublyLinkedList()
        for val in [1, 2]:
            lst.append(val)
        lst.remove(1)
        lst.remove(2)
        self.assertEqual(len(lst), 0)
        self.assertEqual(list(lst), [])
        self.assertIsNone(lst.head)
        self.assertIsNone(lst.tail)

    def test_index_found(self):
        """index возвращает индекс первого найденного элемента."""
        lst = DoublyLinkedList()
        for val in ["a", "b", "c"]:
            lst.append(val)
        self.assertEqual(lst.index("b"), 1)

    def test_first_index_found(self):
        """index возвращает индекс первого найденного элемента. (первый)"""
        lst = DoublyLinkedList()
        for val in ["a", "b", "c"]:
            lst.append(val)
        self.assertEqual(lst.index("a"), 0)

    def test_last_index_found(self):
        """index возвращает индекс первого найденного элемента. (последний)"""
        lst = DoublyLinkedList()
        for val in ["a", "b", "c"]:
            lst.append(val)
        self.assertEqual(lst.index("c"), 2)

    def test_index_not_found(self):
        """index возвращает None если элемента нет в списке."""
        lst = DoublyLinkedList()
        for val in ["a", "b", "c"]:
            lst.append(val)
        self.assertIsNone(lst.index("hello world"))

    def test_insert_out_of_range(self):
        """index вне диапазона бросает исключение IndexError"""
        lst = DoublyLinkedList()
        for val in ["a", "b", "c"]:
            lst.append(val)
        self.assertRaises(IndexError, lst.insert, 10, "d")

    def test_index_returns_first_occurrence(self):
        """проверяем что index возвращает первое вхождение"""
        lst = DoublyLinkedList()

        for val in [1, 2, 1, 3]:
            lst.append(val)

        self.assertEqual(lst.index(1), 0)

    def test_index_empty_list(self):
        """index пустого списка возвращает None"""
        lst = DoublyLinkedList()

        self.assertIsNone(lst.index(10))

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

    def test_reversed_after_remove(self):
        """Обратный обход возвращает значения от хвоста к голове."""
        lst = DoublyLinkedList()

        for val in [1, 2, 3]:
            lst.append(val)

        lst.remove(2)

        self.assertEqual([x for x in reversed(lst)], [3, 1])


if __name__ == "__main__":
    unittest.main()
