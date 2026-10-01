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
    pass


def check_zero_one_strings(length: int, strings: list[str]) -> bool:
    """Проверяет, что strings — полный набор строк длины length из 0 и 1,
    в которых никакие два нуля не стоят рядом.

    Порядок строк не фиксируется. Повторы не допускаются.

    :param length: длина каждой строки, целое число не меньше 1
    :param strings: проверяемый набор строк
    :raise TypeError: если length не целое или strings не список
    :raise ValueError: если length меньше единицы
    :return: True, если набор полон и корректен, иначе False
    """
    pass


def main():
    length = 3
    generated = generate_strings_naive(length)
    print("Наивная генерация строк из 0 и 1")
    print(f"Длина: {length}")
    print(f"Набор: {generated}")
    print(f"Результат проверки: {check_zero_one_strings(length, generated)}")


if __name__ == "__main__":
    main()
