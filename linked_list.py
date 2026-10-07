from linked_list_iterator import LinkedListIterator
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
            self.size = 1
            return

        cur = self.head
        while cur.next is not None:
            cur = cur.next

        cur.next = node
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
        if index > self.size or index < 0:
            raise IndexError("Индекс вне диапазона")

        node = ListNode(value)

        if index == 0:
            node.next = self.head
            self.head = node
            self.size += 1
            return

        prev = None
        cur = self.head
        i = 0

        while i < index:
            prev = cur
            cur = cur.next
            i += 1

        node.next = cur
        prev.next = node
        self.size += 1

    def remove(self, value):
        """
        Удаляет первый элемент с указанным значением.

        Аргументы:
            value: значение для удаления.

        Исключения:
            ValueError — если элемента с таким значением нет.
        """
        if self.head is not None and self.head.value == value:
            self.head = self.head.next
            self.size -= 1
            return

        prev = None
        cur = self.head

        while cur is not None and cur.value != value:
            prev = cur
            cur = cur.next

        if cur is None:
            raise ValueError(f"Элемент со значением {value} не найден")

        prev.next = cur.next
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
        cur = self.head
        index = 0

        while cur is not None:
            if cur.value == value:
                return index
            index += 1
            cur = cur.next
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
        return LinkedListIterator(self.head)

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
