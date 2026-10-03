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
        if len(self) == 0:
            self.tail = node
            self.head = node
        elif isinstance(self.tail, DoublyListNode):
            self.tail.next = node
            node.prev = self.tail
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
        if index > len(self):
            raise IndexError("индекс вне диапазона")

        new_node = DoublyListNode(value)

        if index == len(self):
            node = self.tail
            if isinstance(node, DoublyListNode):
                node.next = new_node
                new_node.prev = node
                self.tail = new_node

        node = None
        for i in range(0, index + 1):
            if i == 0:
                node = self.head
            else:
                if (isinstance(node, DoublyListNode)):
                    node = node.next
                else:
                    raise TypeError("элемент листа не является DoublyListNode")
        prev = None

        if (isinstance(node, DoublyListNode)):
            prev = node.prev
            node.prev = new_node
        if (isinstance(prev, DoublyListNode)):
            prev.next = new_node
        new_node.prev = prev
        new_node.next = node
        if index == 0:
            self.head = new_node
        self.size += 1

    def remove(self, value):
        """
        Удаляет первый элемент с указанным значением.

        Аргументы:
            value: значение для удаления.

        Исключения:
            ValueError — если элемента с таким значением нет.
        """
        node = None
        for index in range(len(self)):
            if index == 0:
                node = self.head
            else:
                if (isinstance(node, DoublyListNode)):
                    node = node.next
                else: 
                    raise TypeError("элемент листа не является DoublyListNode")
            if isinstance(node, DoublyListNode):
                if node.value == value:
                    if index == 0 and self.size > 0 and isinstance(self.head, DoublyListNode):
                        self.head = self.head.next
                    elif index == len(self) - 1 and isinstance(self.tail, DoublyListNode):
                        self.tail = self.tail.prev
                    elif isinstance(node.prev, DoublyListNode) and isinstance(node.next, DoublyListNode):
                        next = node.next
                        prev = node.prev
                        prev.next = next
                        next.prev = prev
                    self.size -= 1

    def index(self, value):
        """
        Возвращает индекс первого элемента с указанным значением.

        Аргументы:
            value: искомое значение.

        Возвращает:
            int: индекс элемента, если найден.
            None: если элемент отсутствует.
        """
        for i, val in enumerate(self):
            if val == value:
                return i
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
        node = None
        for index in range(len(self)):
            if index == 0:
                node = self.head
                if (isinstance(node, DoublyListNode)):
                    yield node.value
            else:
                if (isinstance(node, DoublyListNode)):
                    node = node.next
                    if (isinstance(node, DoublyListNode)):
                        yield node.value
                else: 
                    raise TypeError("элемент листа не является DoublyListNode")

    def __reversed__(self):
        """
        Позволяет итерироваться по значениям элементов списка
        от хвоста к голове.

        Использование:
            for x in reversed(my_list):
                ...
        """
        node = None
        for index in range(len(self), 0, -1):
            if index == len(self):
                node = self.tail
                if (isinstance(node, DoublyListNode)):
                    yield node.value
            else:
                if (isinstance(node, DoublyListNode)):
                    node = node.prev
                    if (isinstance(node, DoublyListNode)):
                        yield node.value
                else: 
                    raise TypeError("элемент листа не является DoublyListNode")

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
