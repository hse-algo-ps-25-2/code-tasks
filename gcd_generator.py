import random

COMMON_FACTORS = 0
A_ONLY_FACTORS = 1
B_ONLY_FACTORS = 2


class GcdGenerator:
    """Генерирует пары чисел с известными НОД и НОК.

    Числа собираются из простых, возведённых в случайную степень:
    общие множители входят в оба числа, остальные не пересекаются.
    Метод generate_values заполняет внутреннее состояние,
    свойства gcd_value, a_value, b_value и lcm_value его только читают.
    """

    def __init__(self):
        """Набор простых чисел для генерации значений"""
        self.__primes: tuple[int, ...] = (
            2,
            3,
            5,
            7,
            11,
            13,
            17,
            19,
            23,
        )
        """Сгенерированные значения, общие множители (индекс COMMON_FACTORS),
        множители исключительно для a_value (индекс A_ONLY_FACTORS),
        множители исключительно для b_value (индекс B_ONLY_FACTORS)"""
        self.generate_values()

    @property
    def gcd_value(self) -> int:
        """Возвращает значение НОД для a_value и b_value"""
        return self.__values[COMMON_FACTORS]

    @property
    def a_value(self) -> int:
        """Возвращает число, полученное в результате перемножения простых чисел,
        возведенных в случайную степень. Число имеет как общие, так и различные
        множители с числом b_value"""
        return self.__values[COMMON_FACTORS] * self.__values[A_ONLY_FACTORS]

    @property
    def b_value(self) -> int:
        """Возвращает число, полученное в результате перемножения простых чисел,
        возведенных в случайную степень. Число имеет как общие, так и различные
        множители с числом a_value"""
        return self.__values[COMMON_FACTORS] * self.__values[B_ONLY_FACTORS]

    @property
    def lcm_value(self) -> int:
        """Возвращает значение НОК для a_value и b_value"""
        return (
            self.__values[COMMON_FACTORS]
            * self.__values[A_ONLY_FACTORS]
            * self.__values[B_ONLY_FACTORS]
        )

    @property
    def max_factor_cnt(self) -> int:
        """Возвращает количество простых множителей, которые можно использовать
        для генерации чисел"""
        return len(self.__primes)

    def generate_values(self, factor_cnt: int = 5, max_pow: int = 5) -> None:
        """Процедура генерирует значения a_value, b_value, gcd_value и lcm_value.
        :param factor_cnt: Количество простых чисел, используемых для генерации,
        не должно превышать значение max_factor_cnt. Значение по умолчанию 5.
        :param max_pow: Верхняя граница для случайной степени. Значение по
        умолчанию 5.
        :return: None
        """
        if factor_cnt < 0:
            raise ValueError("factor_cnt не может быть меньше или равен 0")
        if factor_cnt > self.max_factor_cnt:
            raise ValueError(f"factor_cnt не может быть больше {self.max_factor_cnt}")
        self.__values = [1, 1, 1]
        # Выбираем случайные простые числа из доступных
        # Распределяем их в произвольную группу с произвольной степенью
        selected_primes = random.sample(self.__primes, factor_cnt)
        for index, prime in enumerate(selected_primes):
            group = index % 3
            pow = random.randint(1, max_pow)
            self.__values[group] *= prime**pow


if __name__ == "__main__":
    print("Генерация чисел для проверки НОД/НОК")
    generator = GcdGenerator()
    generator.generate_values(8, 5)
    print("Число a = %d" % generator.a_value)
    print("Число b = %d" % generator.b_value)
    print("НОД(a, b) = %d" % generator.gcd_value)
    print("НОК(a, b) = %d" % generator.lcm_value)
