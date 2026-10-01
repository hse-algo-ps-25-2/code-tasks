"""Пример использования DoublyLinkedList.

Класс DoublyLinkedList нужно реализовать в doubly_linked_list.py
"""

from doubly_linked_list import DoublyLinkedList


def main():
    lst = DoublyLinkedList()
    print("Создан пустой список:", lst)

    lst.append(10)
    lst.append(20)
    lst.append(30)
    print("После добавления элементов:", lst)

    lst.insert(1, 15)
    print("После вставки 15 в позицию 1:", lst)

    lst.remove(20)
    print("После удаления элемента 20:", lst)

    idx = lst.index(30)
    print("Индекс элемента 30:", idx)
    print("Поиск отсутствующего элемента:", lst.index(99))

    print("Элементы в списке через цикл for:")
    for x in lst:
        print(x)

    print("Обратный обход:")
    for x in reversed(lst):
        print(x)

    print("Длина списка:", len(lst))


if __name__ == "__main__":
    main()
