from linked_list import LinkedList

CANNOT_EMPTY_STACK_POP = "Нельзя снять элемент с пустого стека"
CANNOT_EMPTY_STACK_PEEK = "Нельзя посмотреть вершину пустого стека"


class Stack:
    """Стек на готовом односвязном списке.

    Элементы хранятся в объекте LinkedList. Вершина стека — голова списка.
    """

    def __init__(self):
        """Создаёт пустой стек."""
        self._items = LinkedList()

    def is_empty(self) -> bool:
        """Возвращает True, если стек пуст."""
        return self._items.head is None

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
        if self.is_empty():
            raise IndexError(CANNOT_EMPTY_STACK_POP)
        value = self._items.head.value
        self._items.remove(value)
        return value

    def peek(self):
        """Возвращает вершину, не снимая её.

        :raises IndexError: стек пуст
        :return: значение вершины
        """
        if self.is_empty():
            raise IndexError(CANNOT_EMPTY_STACK_PEEK)
        return self._items.head.value
