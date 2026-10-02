from list_node import ListNode


class LinkedListIterator:
    """
    Класс, реализующий итератор по односвязному списку.

    Атрибуты:
        current (ListNode | None): ссылка на текущий узел списка.

    Поддерживает базовые операции:
        - итерация (__iter__),
        - переход к следующему элементу (__next__).
    """

    def __init__(self, head: ListNode):
        """
        Создаёт итератор с указанного начального узла.

        Аргументы:
            head (ListNode | None): ссылка на начальный узел.
        """
        self.current = head

    def __iter__(self):
        """
        Возвращает итератор. Текущий класс уже является итератором.
        """
        return self

    def __next__(self):
        """
        Возвращает следующий элемент итератора.

        Исключения:
            StopIteration — если достигнут конец списка.
        """
        if self.current is None:
            raise StopIteration

        result = self.current.value
        self.current = self.current.next
        return result
