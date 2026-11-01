from constants import PAIRS, Exceptions
from stack import Stack


def is_brackets_balanced(expression: str) -> bool:
    """Проверяет парность скобок с помощью Stack.

    Учитываются скобки (), [] и {}. Остальные символы пропускаются.
    Пустая строка и строка без скобок согласованы. Закрывающая скобка
    допустима только как пара к последней ещё не закрытой открывающей
    того же вида. В конце незакрытых скобок не остаётся.

    :param expression: проверяемая строка
    :raises TypeError: аргумент не строка
    :return: True, если скобки расставлены верно, False в ином случае
    """
    if not isinstance(expression, str):
        raise TypeError(Exceptions.INVALID_TYPE_BRACKETS)

    stack = Stack()

    for char in expression:
        if char in PAIRS.values():
            stack.push(char)

        elif char in PAIRS.keys():
            if stack.is_empty() or stack.peek() != PAIRS[char]:
                return False

            stack.pop()
    return stack.is_empty()


def main():
    stack = Stack()
    for value in (1, 2, 2):
        stack.push(value)
    print("Вершина:", stack.peek())
    print("Снято:", stack.pop())
    expression = "3 + 2 * (5 - [4 / {2 + 1}])"
    print(expression, is_brackets_balanced(expression))


if __name__ == "__main__":
    main()
