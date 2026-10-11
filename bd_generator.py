import random
from fractions import Fraction
from math import gcd

from band_determinant import BandDeterminant

INVALID_BOUNDS = (
    "Для диапазона [{0}; {1}] и параметров генератора "
    + "невозможно создать задачу, удовлетворяющую условиям"
)


class BDGenerator:
    """Генерирует условия для задачи о ленточном определителе
    методом неопределенных коэффициентов

    Корни характеристического уравнения выбираются из указанного диапазона,
    на основании подобранных корней по теореме Виета вычисляются значения
    для диагоналей матрицы и коэффициенты рекуррентного уравнения.
    Для того, чтобы получить удобное решение корни подбираются так,
    чтобы коэффициенты рекуррентного уравнения были целыми числами
    или простыми дробями.
    """

    def __init__(self, small_value_limit=15, max_denominator=5):
        """
        Инициализирует генератор

        Args:
            small_value_limit (int): ограничение "небольшого" значения
            для генерируемых значений
            max_denominator (int): ограничение знаменателя дробей
        """
        if not isinstance(small_value_limit, int):
            raise ValueError("small_value_limit должен быть целым числом")
        if small_value_limit <= 0:
            raise ValueError("small_value_limit должен быть больше нуля")
        if not isinstance(max_denominator, int):
            raise ValueError("max_denominator должен быть целым числом")
        if max_denominator <= 0:
            raise ValueError("max_denominator должен быть больше нуля")
        self.small_value_limit = small_value_limit
        self.max_denominator = max_denominator

    def generate_band_determinant(
        self, low_bound: int, high_bound: int
    ) -> BandDeterminant:
        """
        Генерирует условия для задачи о ленточном определителе методом
        неопределенных коэффициентов

        Args:
            low_bound (int): нижняя граница диапазона для выбора корней
                характеристического уравнения
            high_bound (int): верхняя граница диапазона для выбора корней
                характеристического уравнения
        """
        if not isinstance(low_bound, int):
            raise ValueError("low_bound должен быть целым числом")
        if not isinstance(high_bound, int):
            raise ValueError("high_bound должен быть целым числом")
        if low_bound > high_bound:
            raise ValueError("Нижняя граница не может быть больше верхней.")

        generation_result = self._generate_roots(low_bound, high_bound)
        if not generation_result:
            raise ValueError(str.format(INVALID_BOUNDS, low_bound, high_bound))
        lambda1, lambda2, a, b, c = generation_result
        coefficients = self._calculate_coefficients(lambda1, lambda2)
        return BandDeterminant(a, b, c, [lambda1, lambda2], coefficients)

    def _generate_roots(self, low_bound, high_bound):
        """
        Подбирает корни и коэффициенты матрицы.

        Перебирает пары целых корней из заданного диапазона,
        проверяет их удобство и подбирает диагонали матрицы.

        Args:
            low_bound (int): нижняя граница диапазона для выбора корней
            high_bound (int): верхняя граница диапазона для выбора корней

        Returns:
            tuple[int, int, int, int, int] | None:
                (lambda1, lambda2, a, b, c) или None
        """
        candidates = []

        for lambda1 in range(low_bound, high_bound + 1):
            for lambda2 in range(lambda1, high_bound + 1):

                if not self._check_roots(
                    lambda1,
                    lambda2,
                    low_bound,
                    high_bound,
                ):
                    continue

                diagonals = self._calculate_matrix(lambda1, lambda2)

                if diagonals is None:
                    continue

                a, b, c = diagonals
                candidates.append((lambda1, lambda2, a, b, c))

        if not candidates:
            return None

        return random.choice(candidates)

    def _check_roots(self, lambda1, lambda2, low_bound, high_bound):
        """
        Проверяет соответствие корней условиям:
        - Ячейки матрицы должны быть меньше лимита значений
        - Числители коэффициентов должны быть меньше лимита значений
        - Знаменатель коэффициентов должен быть небольшим числом
        """
        if lambda1 == 0 or lambda2 == 0:
            return False

        if (
            lambda1 < low_bound
            or lambda1 > high_bound
            or lambda2 < low_bound
            or lambda2 > high_bound
        ):
            return False

        if abs(lambda1 + lambda2) > self.small_value_limit:
            return False

        if lambda1 == lambda2:
            return True

        g = gcd(abs(lambda1), abs(lambda2))

        denominator = abs(lambda1 - lambda2) // g
        numerator1 = abs(lambda1) // g
        numerator2 = abs(lambda2) // g

        return (
            denominator <= self.max_denominator
            and numerator1 <= self.small_value_limit
            and numerator2 <= self.small_value_limit
        )

    def _calculate_matrix(self, lambda1, lambda2):
        """
        Подбирает ненулевые целые a, b, c по корням.

        Returns:
            tuple[int, int, int] | None: (a, b, c) или None
        """
        bc = lambda1 * lambda2
        if bc == 0:
            return None
        a = lambda1 + lambda2
        results = []
        limit = self.small_value_limit
        for b in range(-limit, limit + 1):
            if b == 0:
                continue
            if bc % b == 0:
                c = bc // b
                if c == 0:
                    continue
                if abs(c) > limit:
                    continue
                results.append((a, b, c))
                if b != c:
                    results.append((a, c, b))

        if not results:
            return None
        return random.choice(results)

    def _calculate_coefficients(self, lambda1, lambda2):
        """
        Вычисляет коэффициенты рекурсивного уравнения

        Случай 1: корень кратности 2
            Уравнение вида:
            detAn = (lambda ** n) * (A * n + B)

            Система уравнений:
            (A * 1 + B) * lambda = a = 2 * lambda
            (A * 2 + B) * lambda ** 2 = a ** 2 - bc = 3 * lambda ** 2

            Система всегда сводится к решению
            A = B = 1

        Случай 2: разные корни
            Уравнение вида:
            detAn = A1 * (lambda1 ** n) + A2 * (lambda2 ** n)

            Система уравнений:
            A1 * lambda1 + A2 * lambda2 = a
            A1 * (lambda1 ** 2) + A2 * (lambda2 ** 2) = a ** 2 - bc

            Сводится к формуле:
            A1 = lambda1 / (lambda1 - lambda2)
            A2 = -lambda2 / (lambda1 - lambda2)
        """
        if lambda1 == lambda2:
            return [1, 1]

        return [
            Fraction(lambda1, lambda1 - lambda2),
            Fraction(-lambda2, lambda1 - lambda2),
        ]
