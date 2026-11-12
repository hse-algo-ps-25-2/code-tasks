from doubly_list_node import DoublyListNode


class DoublyLinkedList:
    """
    Класс, реализующий двусвязный список.

    Атрибуты:
        head (DoublyListNode | None): ссылка на первый узел списка.
        tail (DoublyListNode | None): ссылка на последний узел списка.
        size (int): количество элементов в списке.

    Поддерживает базовые операции:
        - добавление элемента в конец (append),
        - вставка по индексу (insert),
        - удаление элемента по значению (remove),
        - поиск индекса элемента (index),
        - получение длины (__len__),
        - прямой обход (__iter__),
        - обратный обход (__reversed__),
        - строковое представление (__str__).
    """

    def __init__(self):
        """Создаёт пустой двусвязный список."""
        self.head = None
        self.tail = None
        self.size = 0

    def append(self, value):
        """
        Добавляет элемент в конец списка.

        Аргументы:
            value: значение нового элемента.
        """
        node = DoublyListNode(value)
        if self.head is None:
            self.head = node
            self.tail = node
        else:
            node.prev = self.tail
            self.tail.next = node
            self.tail = node
        self.size += 1

    def insert(self, index, value):
        """
        Вставляет элемент по указанному индексу.

        Аргументы:
            index (int): позиция вставки (0 ≤ index ≤ len).
            value: значение нового элемента.

        Исключения:
            IndexError — если индекс вне диапазона.
        """
        if index < 0 or index > self.size:
            raise IndexError("индекс вне диапазона")
        if index == self.size:
            self.append(value)
            return
        node = DoublyListNode(value)
        if index == 0:
            node.next = self.head
            self.head.prev = node
            self.head = node
        else:
            current = self.head
            for _ in range(index):
                current = current.next
            node.next = current
            node.prev = current.prev
            current.prev.next = node
            current.prev = node
        self.size += 1

    def remove(self, value):
        """
        Удаляет первый элемент с указанным значением.

        Аргументы:
            value: значение для удаления.

        Исключения:
            ValueError — если элемента с таким значением нет.
        """
        current = self.head
        while current is not None:
            if current.value == value:
                if current.prev is None:
                    self.head = current.next
                else:
                    current.prev.next = current.next
                if current.next is None:
                    self.tail = current.prev
                else:
                    current.next.prev = current.prev
                self.size -= 1
                return
            current = current.next
        raise ValueError("элемент не найден")

    def index(self, value):
        """
        Возвращает индекс первого элемента с указанным значением.

        Аргументы:
            value: искомое значение.

        Возвращает:
            int: индекс элемента, если найден.
            None: если элемент отсутствует.
        """
        current = self.head
        position = 0
        while current is not None:
            if current.value == value:
                return position
            current = current.next
            position += 1
        return None

    def __len__(self):
        """Возвращает количество элементов в списке."""
        return self.size

    def __iter__(self):
        """
        Позволяет итерироваться по значениям элементов списка в цикле for
        от головы к хвосту.

        Использование:
            for x in my_list:
                ...
        """
        current = self.head
        while current is not None:
            yield current.value
            current = current.next

    def __reversed__(self):
        """
        Позволяет итерироваться по значениям элементов списка
        от хвоста к голове.

        Использование:
            for x in reversed(my_list):
                ...
        """
        current = self.tail
        while current is not None:
            yield current.value
            current = current.prev

    def __str__(self):
        """
        Возвращает строковое представление списка.

        Формат:
            [elem1 <-> elem2 <-> elem3]

        Пустой список:
            []
        """
        values = [str(v) for v in self]
        return "[" + " <-> ".join(values) + "]"
