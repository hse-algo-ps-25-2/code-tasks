from linked_list import LinkedList

CANNOT_EMPTY_STACK_POP = "Нельзя снять элемент с пустого стека"
CANNOT_EMPTY_STACK_PEEK = "Нельзя посмотреть вершину пустого стека"


class Stack:
    """Стек на готовом односвязном списке.

    Элементы хранятся в объекте LinkedList. Вершина стека — голова списка.
    """

    def __init__(self):
        """Создаёт пустой стек."""
        self.stack = LinkedList()

    def is_empty(self) -> bool:
        """Возвращает True, если стек пуст."""
        return self.__len__() == 0

    def __len__(self) -> int:
        """Возвращает число элементов."""
        return self.stack.size

    def push(self, value):
        """Кладёт элемент на вершину.

        :param value: новое значение вершины
        """
        self.stack.insert(0, value)

    def pop(self):
        """Снимает и возвращает вершину.

        :raises IndexError: стек пуст
        :return: снятое значение
        """
        if self.is_empty():
            raise IndexError(CANNOT_EMPTY_STACK_POP)
        value = self.stack.head.value
        self.stack.remove(value)
        return value

    def peek(self):
        """Возвращает вершину, не снимая её.

        :raises IndexError: стек пуст
        :return: значение вершины
        """
        if self.is_empty():
            raise IndexError(CANNOT_EMPTY_STACK_PEEK)
        return self.stack.head.value
