from linked_list import LinkedList


class Stack:
    """Стек на готовом односвязном списке.

    Элементы хранятся в объекте LinkedList. Вершина стека — голова списка.
    """

    def __init__(self):
        """Создаёт пустой стек."""
        self._items = LinkedList()

    def is_empty(self) -> bool:
        """Возвращает True, если стек пуст."""
        return len(self._items) == 0

    def __len__(self) -> int:
        """Возвращает число элементов."""
        return len(self._items)

    def push(self, value):
        """Кладёт элемент на вершину.

        :param value: новое значение вершины
        """
        self._items.insert(0, value)

    def pop(self):
        """Снимает и возвращает вершину.

        :raises IndexError: стек пуст
        :return: снятое значение
        """
        if self._items.head is None:
            raise IndexError("стек пуст")
        value = self._items.head.value
        self._items.remove(value)
        return value

    def peek(self):
        """Возвращает вершину, не снимая её.

        :raises IndexError: стек пуст
        :return: значение вершины
        """
        if self._items.head is None:
            raise IndexError("стек пуст")
        return self._items.head.value
