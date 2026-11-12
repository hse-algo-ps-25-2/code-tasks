from list_node import ListNode


class LinkedList:
    """
    Класс, реализующий односвязный список.

    Атрибуты:
        head (ListNode | None): ссылка на первый узел списка.
        size (int): количество элементов в списке.

    Поддерживает базовые операции:
        - добавление элемента в конец (append),
        - вставка по индексу (insert),
        - удаление элемента по значению (remove),
        - поиск индекса элемента (index),
        - получение длины (__len__),
        - итерация (__iter__),
        - строковое представление (__str__).
    """

    def __init__(self):
        """Создаёт пустой связный список."""
        self.head = None
        self.size = 0

    def append(self, value):
        """
        Добавляет элемент в конец списка.

        Аргументы:
            value: значение нового элемента.
        """
        node = ListNode(value)
        if self.head is None:
            self.head = node
        else:
            current = self.head
            while current.next is not None:
                current = current.next
            current.next = node
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
        node = ListNode(value)
        if index == 0:
            node.next = self.head
            self.head = node
        else:
            current = self.head
            for _ in range(index - 1):
                current = current.next
            node.next = current.next
            current.next = node
        self.size += 1

    def remove(self, value):
        """
        Удаляет первый элемент с указанным значением.

        Аргументы:
            value: значение для удаления.

        Исключения:
            ValueError — если элемента с таким значением нет.
        """
        if self.head is None:
            raise ValueError("элемент не найден")
        if self.head.value == value:
            self.head = self.head.next
            self.size -= 1
            return
        previous = self.head
        current = self.head.next
        while current is not None:
            if current.value == value:
                previous.next = current.next
                self.size -= 1
                return
            previous = current
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
        Позволяет итерироваться по значениям элементов списка в цикле for.

        Использование:
            for x in my_list:
                ...
        """
        current = self.head
        while current is not None:
            yield current.value
            current = current.next

    def __str__(self):
        """
        Возвращает строковое представление списка.

        Формат:
            [elem1 -> elem2 -> elem3]

        Пустой список:
            []
        """
        values = [str(v) for v in self]
        return "[" + " -> ".join(values) + "]"
