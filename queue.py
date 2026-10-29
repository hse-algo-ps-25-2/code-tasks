from doubly_linked_list import DoublyLinkedList

class Queue:
    """Структура данных Очередь"""

    def __init__(self):
        """Создаёт пустую очередь."""
        self.list = DoublyLinkedList()

    def is_empty(self) -> bool:
        """Возвращает True, если очередь пуста."""
        return self.__len__() == 0

    def __len__(self) -> int:
        """Возвращает число элементов."""
        return self.list.size

    def enqueue(self, value):
        """Ставит элемент в конец очереди.

        :param value: новое значение
        """
        self.list.append(value)

    def dequeue(self):
        """Удаляет и возвращает элемент из начала очереди.

        :raises IndexError: очередь пуста
        :return: удалённое значение
        """
        if self.is_empty():
            raise IndexError('очередь пуста')
        first = self.peek()
        self.list.remove(first)
        return first

    def peek(self):
        """Возвращает начало очереди, не удаляя его.

        :raises IndexError: очередь пуста
        :return: значение в начале
        """
        if self.is_empty():
            raise IndexError('очередь пуста')
        
        return self.list.head.value

