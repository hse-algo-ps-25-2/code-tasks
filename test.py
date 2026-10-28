import unittest

from linked_list import LinkedList


class TestLinkedList(unittest.TestCase):
    """Набор тестов для класса LinkedList."""

    def test_empty_init(self):
        """Новый список пустой: длина 0, head = None."""
        lst = LinkedList()
        self.assertEqual(len(lst), 0)
        self.assertIsNone(lst.head)

    def test_append_one(self):
        """append добавляет один элемент в конец."""
        lst = LinkedList()
        lst.append(10)
        self.assertEqual(len(lst), 1)
        self.assertEqual(list(lst), [10])

    def test_append_many(self):
        """append несколько раз сохраняет порядок элементов."""
        lst = LinkedList()
        for val in [1, 2, 3]:
            lst.append(val)
        self.assertEqual(len(lst), 3)
        self.assertEqual(list(lst), [1, 2, 3])

    def test_insert_empty(self):
        """insert вставляет элемент в пустой список."""
        lst = LinkedList()
        lst.insert(0, "some value")

        self.assertEqual(len(lst), 1)
        self.assertEqual(list(lst), ["some value"])
        self.assertEqual(lst.head.value, "some value")

    def test_insert_head(self):
        """insert вставляет элемент в начало непустого списка."""
        lst = LinkedList()
        for val in [1, 2, 3]:
            lst.append(val)
        lst.insert(0, 0)

        self.assertEqual(len(lst), 4)
        self.assertEqual(list(lst), [0, 1, 2, 3])
        self.assertEqual(lst.head.value, 0)

    def test_insert_middle(self):
        """insert вставляет элемент в середину списка."""
        lst = LinkedList()
        for val in [1, 3]:
            lst.append(val)
        lst.insert(1, 2)
        self.assertEqual(list(lst), [1, 2, 3])

    def test_insert_end(self):
        """insert вставляет элемент в конец списка."""
        lst = LinkedList()
        for val in [1, 2, 3]:
            lst.append(val)
        lst.insert(len(lst), 4)

        self.assertEqual(len(lst), 4)
        self.assertEqual(list(lst), [1, 2, 3, 4])

    def test_insert_out_of_range(self):
        """insert выбрасывает IndexError при попытке вставить элемент по индексу,
        превышающему длину списка."""
        lst = LinkedList()
        for val in [1, 2, 3]:
            lst.append(val)

        self.assertRaises(IndexError, lst.insert, len(lst) + 1, 4)

    def test_insert_negative_index(self):
        """insert выбрасывает IndexError при попытке вставить элемент
        по отрицательному индексу."""
        lst = LinkedList()
        for val in [1, 2, 3]:
            lst.append(val)

        self.assertRaises(IndexError, lst.insert, -1, 0)

    def test_insert_invalid_index(self):
        """insert выбрасывает IndexError при попытке вставить элемент
        по индексу некорректного типа."""
        lst = LinkedList()
        for val in [1, 2, 3]:
            lst.append(val)

        self.assertRaises(IndexError, lst.insert, 1.5, 0)

    def test_remove_empty(self):
        """remove выбрасывает ValueError при попытке удалить элемент
        из пустого списка."""
        lst = LinkedList()

        self.assertRaises(ValueError, lst.remove, "some value")

    def test_remove_head(self):
        """remove корректно удаляет первый узел списка."""
        lst = LinkedList()
        for val in [1, 2, 3]:
            lst.append(val)
        lst.remove(1)

        self.assertEqual(len(lst), 2)
        self.assertEqual(list(lst), [2, 3])
        self.assertEqual(lst.head.value, 2)

    def test_remove_middle(self):
        """remove удаляет элемент из списка."""
        lst = LinkedList()
        for val in [1, 2, 3]:
            lst.append(val)
        lst.remove(2)

        self.assertEqual(len(lst), 2)
        self.assertEqual(list(lst), [1, 3])

    def test_remove_not_found(self):
        """remove выбрасывает ValueError, если элемент не был найден."""
        lst = LinkedList()
        for val in [1, 2, 3]:
            lst.append(val)

        self.assertRaises(ValueError, lst.remove, 4)

    def test_remove_only_first(self):
        """remove удаляет только первое вхождение элемента."""
        lst = LinkedList()
        for val in [1, 2, 3, 1, 2, 3]:
            lst.append(val)
        lst.remove(2)

        self.assertEqual(len(lst), 5)
        self.assertEqual(list(lst), [1, 3, 1, 2, 3])

    def test_index_found(self):
        """index возвращает индекс первого найденного элемента."""
        lst = LinkedList()
        for val in ["a", "b", "c"]:
            lst.append(val)
        self.assertEqual(lst.index("b"), 1)

    def test_index_not_found(self):
        """index возвращает None, если элемент не был найден."""
        lst = LinkedList()
        for val in [1, 2, 3]:
            lst.append(val)

        self.assertEqual(lst.index(45), None)

    def test_index_empty(self):
        """index возвращает None при поиске в пустом списке."""
        lst = LinkedList()

        self.assertEqual(lst.index(123), None)

    def test_index_duplicates(self):
        """index возвращает индекс первого вхождения элемента."""
        lst = LinkedList()
        for val in [1, 2, 3, 1, 2, 3]:
            lst.append(val)

        self.assertEqual(lst.index(3), 2)

    def test_iteration(self):
        """Итерация по списку возвращает значения в порядке следования."""
        lst = LinkedList()
        for val in [1, 2, 3]:
            lst.append(val)
        self.assertEqual([x for x in lst], [1, 2, 3])

    def test_iteration_empty(self):
        """Пустой список является итерируемым."""
        lst = LinkedList()

        self.assertEqual(list(lst), [])

    def test_size_insert(self):
        """size изменяется при добавлении элементов."""
        lst = LinkedList()
        for val in [1, 2, 3]:
            lst.append(val)

        self.assertEqual(lst.size, 3)

        lst.append(4)
        self.assertEqual(lst.size, 4)

        lst.insert(0, 0)
        self.assertEqual(lst.size, 5)

    def test_size_remove(self):
        """size изменяется при удалении элементов."""
        lst = LinkedList()
        for val in [1, 2, 3]:
            lst.append(val)

        self.assertEqual(lst.size, 3)

        lst.remove(3)
        self.assertEqual(lst.size, 2)

    def test_str(self):
        """Строковое представление списка."""
        lst = LinkedList()
        for val in [1, 2, 3]:
            lst.append(val)

        self.assertEqual(str(lst), "[1 -> 2 -> 3]")

    def test_str_empty(self):
        """Строковое представление пустого списка."""
        lst = LinkedList()

        self.assertEqual(str(lst), "[]")

    def test_str_single(self):
        """Строковое представление списка из одного элемента."""
        lst = LinkedList()
        lst.append(123)

        self.assertEqual(str(lst), "[123]")


if __name__ == "__main__":
    unittest.main()
