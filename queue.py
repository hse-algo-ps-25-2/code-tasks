from doubly_linked_list import DoublyLinkedList


class Queue:
    """Очередь на готовом двусвязном списке.

    Начало очереди — голова списка, конец — хвост.
    """

    def __init__(self):
        """Создаёт пустую очередь."""
        self._items = DoublyLinkedList()

    def is_empty(self) -> bool:
        """Возвращает True, если очередь пуста."""
        return len(self._items) == 0

    def __len__(self) -> int:
        """Возвращает число элементов."""
        return len(self._items)

    def enqueue(self, value):
        """Ставит элемент в конец очереди.

        :param value: новое значение
        """
        self._items.append(value)

    def dequeue(self):
        """Удаляет и возвращает элемент из начала очереди.

        :raises IndexError: очередь пуста
        :return: удалённое значение
        """
        if self._items.head is None:
            raise IndexError("очередь пуста")
        value = self._items.head.value
        self._items.remove(value)
        return value

    def peek(self):
        """Возвращает начало очереди, не удаляя его.

        :raises IndexError: очередь пуста
        :return: значение в начале
        """
        if self._items.head is None:
            raise IndexError("очередь пуста")
        return self._items.head.value
