import unittest
from main import ErrorMessages, recursive_quicksort
from datetime import date


class TestRecursiveSort(unittest.TestCase):
    """Набор тестов рекурсивной сортировки"""

    def test_empty(self):
        """Пустой список"""
        self.assertEqual(recursive_quicksort([]), [])

    def test_two(self):
        """Два элемента"""
        self.assertEqual(recursive_quicksort([2, 1]), [1, 2])

    def test_items_list_from_example(self):
        "items из примера"

        self.assertEqual(
            recursive_quicksort([5, 8, 1, 4, -7, 6, 12, 19, -6]),
            [-7, -6, 1, 4, 5, 6, 8, 12, 19],
        )

    def test_not_list(self):
        """Правильный TypeError если items не список"""

        with self.assertRaises(TypeError) as error:
            recursive_quicksort(1)
        self.assertEqual(str(error.exception), ErrorMessages.NOT_LIST_ERROR_MESSAGE)

    def test_sort_comparable_class(self):
        "Проверка что кастомный класс с оператором < корректно сортируется"
        class Human:
            "Человек"
            def __init__(self, name, birthdate):
                self.name = name
                self.birthdate = birthdate

            def __lt__(self, other):
                return self.birthdate < other.birthdate

        mathematicians = [
            Human("Ричард Бэллман", date(1920, 8, 26)),
            Human("Блез Паскаль", date(1623, 6, 19)),
            Human("Исаак Ньютон", date(1643, 1, 4)),
            Human("Андрей Николаевич Колмогоров", date(1903, 4, 25))
        ]

        print("Математики:")
        for mathematician in mathematicians:
            print(f"{mathematician.name} {mathematician.birthdate}")
        print()

        mathematician_sorted_by_age = recursive_quicksort(mathematicians)
        print("Математики по возрасту:")
        for mathematician in recursive_quicksort(mathematicians):
            print(f"{mathematician.name} {mathematician.birthdate}")

        for pair in [(mathematician_sorted_by_age[i].birthdate,
                     mathematician_sorted_by_age[i + 1].birthdate)\
                         for i in range(len(mathematician_sorted_by_age) - 1)]:
            current_birthdate, next_birthdate = pair
            self.assertTrue(current_birthdate <= next_birthdate)

    def test_error_not_comparable_class_in_list(self):
        "Правильный TypeError если cписок из кастомных\
            элементов не сравнимых оператором <"

        class NotComparabeHuman:
            "Человек которого не умеем сравнивать"
            def __init__(self, name, birthdate):
                self.name = name
                self.birthdate = birthdate

        mathematicians = [
            NotComparabeHuman("Ричард Бэллман", date(1920, 8, 26)),
            NotComparabeHuman("Блез Паскаль", date(1623, 6, 19)),
            NotComparabeHuman("Исаак Ньютон", date(1643, 1, 4)),
            NotComparabeHuman("Андрей Николаевич Колмогоров", date(1903, 4, 25))
        ]

        with self.assertRaises(TypeError) as error:
            recursive_quicksort(mathematicians)
            self.assertEqual(
                str(error.exception),
                ErrorMessages.LIST_CONTAINS_NOT_COMPARABLE_ITEMS
            )

    def test_not_comparable_items_in_list(self):
        """Правильный TypeError если cписок
        содержит не сравнимые оператором < элементы"""

        with self.assertRaises(TypeError) as error:
            recursive_quicksort(["1", 4, 3])
        self.assertEqual(
            str(error.exception), ErrorMessages.LIST_CONTAINS_NOT_COMPARABLE_ITEMS
        )


if __name__ == "__main__":
    unittest.main()
