import unittest

from stack import Stack


class TestStack(unittest.TestCase):
    """Публичные примеры стека."""

    def test_lifo(self):
        """Последний положенный элемент снимается первым."""
        stack = Stack()
        self.assertTrue(stack.is_empty())
        self.assertEqual(len(stack), 0)
        stack.push(1)
        stack.push(2)
        self.assertFalse(stack.is_empty())
        self.assertEqual(len(stack), 2)
        self.assertEqual(stack.peek(), 2)
        self.assertEqual(len(stack), 2)
        self.assertEqual(stack.pop(), 2)
        self.assertEqual(stack.peek(), 1)
        self.assertEqual(stack.pop(), 1)
        self.assertTrue(stack.is_empty())

    def test_empty_stack(self):
        """У пустого стека нет вершины."""
        stack = Stack()
        with self.assertRaises(IndexError):
            stack.pop()
        with self.assertRaises(IndexError):
            stack.peek()

    def test_push_pop_many(self):
        """Несколько push и pop сохраняют порядок LIFO."""
        stack = Stack()
        for value in [1, 2, 3]:
            stack.push(value)
        self.assertEqual([stack.pop() for _ in range(3)], [3, 2, 1])

    def test_peek_does_not_remove(self):
        """peek не меняет вершину и длину."""
        stack = Stack()
        stack.push("a")
        stack.push("b")
        self.assertEqual(stack.peek(), "b")
        self.assertEqual(stack.peek(), "b")
        self.assertEqual(len(stack), 2)

    def test_duplicates(self):
        """Повторяющиеся значения снимаются по одному."""
        stack = Stack()
        for value in [1, 1, 2]:
            stack.push(value)
        self.assertEqual([stack.pop() for _ in range(3)], [2, 1, 1])

    def test_pop_until_empty(self):
        """После снятия всех элементов стек снова пуст."""
        stack = Stack()
        stack.push(1)
        stack.pop()
        self.assertTrue(stack.is_empty())
        self.assertEqual(len(stack), 0)

    def test_is_empty_after_push(self):
        """После push стек перестаёт быть пустым."""
        stack = Stack()
        self.assertTrue(stack.is_empty())
        stack.push(42)
        self.assertFalse(stack.is_empty())

    def test_len_after_operations(self):
        """len отражает число элементов после push и pop."""
        stack = Stack()
        stack.push(1)
        stack.push(2)
        stack.push(3)
        self.assertEqual(len(stack), 3)
        stack.pop()
        self.assertEqual(len(stack), 2)
        stack.pop()
        self.assertEqual(len(stack), 1)
        stack.pop()
        self.assertEqual(len(stack), 0)

    def test_different_types(self):
        """Стек не ограничивает тип значений."""
        stack = Stack()
        values = [1, "two", None, False, 3.5]
        for value in values:
            stack.push(value)
        popped = [stack.pop() for _ in range(len(values))]
        self.assertEqual(popped, list(reversed(values)))

    def test_false_and_zero(self):
        """False и 0 — допустимые значения, а не признак пустоты."""
        stack = Stack()
        stack.push(False)
        stack.push(0)
        self.assertFalse(stack.is_empty())
        self.assertEqual(stack.pop(), 0)
        self.assertEqual(stack.pop(), False)
        self.assertTrue(stack.is_empty())

    def test_pop_after_empty_raises_again(self):
        """После опустошения pop и peek снова дают IndexError."""
        stack = Stack()
        stack.push(1)
        stack.pop()
        with self.assertRaises(IndexError):
            stack.pop()
        with self.assertRaises(IndexError):
            stack.peek()


if __name__ == "__main__":
    unittest.main()
