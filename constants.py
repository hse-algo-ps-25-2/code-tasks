PAIRS: dict[str, str] = {")": "(", "]": "[", "}": "{"}


class Exceptions:
    CANNOT_EMPTY_STACK_POP = "Нельзя снять элемент с пустого стека"
    CANNOT_EMPTY_STACK_PEEK = "Нельзя посмотреть вершину пустого стека"
    INVALID_TYPE_BRACKETS = "Сравнение строк доступно только для строкового типа данных"
