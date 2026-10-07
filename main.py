LENGTH_NOT_INT = "Длина строки не является целым числом"
LENGTH_NOT_POS = "Длина строки меньше единицы"
NOT_LIST = "Набор строк не является списком"


def generate_strings_naive(length: int) -> list[str]:
    """Возвращает все строки длины length из 0 и 1 без двух нулей подряд.

    Набор строится наивно: перебираются все строки из 0 и 1 заданной длины,
    затем отбрасываются строки, в которых два нуля стоят рядом.
    Порядок строк не фиксируется.

    :param length: длина строки, целое число не меньше 1
    :raise TypeError: если length не целое
    :raise ValueError: если length меньше единицы
    :return: список строк
    """
    if type(length) is not int:
        raise TypeError(LENGTH_NOT_INT)
    if length < 1:
        raise ValueError(LENGTH_NOT_POS)

    return [s for s in recursive_gen(length) if '00' not in s]

def recursive_gen(length: int) -> list[str]:
    """Все строки длины length из '0' и '1'. Рекурсия по длине."""
    if length == 0:
        return [""]

    return [bit + el for bit in ("0", "1") for el in recursive_gen(length - 1)]

def check_zero_one_strings(length: int, strings: list[str]) -> bool:
    """Проверяет, что strings - полный набор всевозможных строк длины length
    из 0 и 1, в которых никакие два нуля не стоят рядом.

    Порядок строк не фиксируется. Повторы не допускаются.

    :param length: длина каждой строки, целое число не меньше 1
    :param strings: проверяемый набор строк
    :raise TypeError: если length не целое или strings не список
    :raise ValueError: если length меньше единицы
    :return: True, если набор полон и корректен, иначе False
    """
    if type(length) is not int:
        raise TypeError(LENGTH_NOT_INT)
    if length < 1:
        raise ValueError(LENGTH_NOT_POS)
    if not isinstance(strings, list):
        raise TypeError(NOT_LIST)

    if not all(isinstance(s, str) for s in strings):
        return False
    if not all(len(s) == length for s in strings):
        return False
    if not all(set(s) <= {"0", "1"} for s in strings):
        return False
    if any('00' in s for s in strings):
        return False
    if len(strings) != len(set(strings)):
        return False

    if len(strings) != calc_fib(length + 2):
        return False

    return True

def calc_fib(n: int) -> int:
    """n-е число фибоначчи при f(1) = f(2) = 1."""
    if n <= 2:
        return 1

    a, b = 1, 1
    for i in range(n - 2):
        a, b = b, a + b

    return b


def main():
    length = 3
    generated = generate_strings_naive(length)
    print("Наивная генерация строк из 0 и 1")
    print(f"Длина: {length}")
    print(f"Набор: {generated}")
    print(f"Результат проверки: {check_zero_one_strings(length, generated)}")


if __name__ == "__main__":
    main()
