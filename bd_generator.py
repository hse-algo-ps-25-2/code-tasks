import math
import random
from fractions import Fraction

from band_determinant import BandDeterminant


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
        """
        self.small_value_limit = small_value_limit

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
        if low_bound > high_bound:
            raise ValueError("Нижняя граница не может быть больше верхней.")

        lambda1, lambda2 = self._generate_roots(low_bound, high_bound)
        matrix = self._calculate_matrix(lambda1, lambda2, low_bound, high_bound)
        if matrix is None:
            return None
        a, b, c = matrix
        coefficients = self._calculate_coefficients(lambda1, lambda2, a, b * c)
        return BandDeterminant(a, b, c, [lambda1, lambda2], coefficients)

    def _generate_roots(self, low_bound, high_bound):
        lambda1 = 0
        lambda2 = 0

        while lambda1 == 0 or lambda2 == 0:
            lambda1 = random.randint(low_bound, high_bound)
            lambda2 = random.randint(low_bound, high_bound)

        return [lambda1, lambda2]

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

    def _calculate_coefficients(self, lambda1, lambda2, a, bc):
        """
        Характеристическое уравнение:
        lambda ** 2 - a * lambda + bc = 0

        Начальные условия:
        detA1 = a
        detA2 = a  ** 2 - bc

        Случай 1: корень кратности 2
            Решение:
            detAn = (lambda ** n) * (A * n + B)

            Система уравнений:
            (A * 1 + B) * lambda = a
            (A * 2 + B) * lambda ** 2 = a ** 2 - bc

            Нахождение коэффициентов:
            A = (a ** 2 - bc - a * lambda) / (lambda ** 2)

        Случай 2: разные корни
            Решение:
            detAn = A1 * (lambda1 ** n) + A2 * (lambda2 ** n)

            По теореме Виета:
            a = lambda1 + lambda2
            bc = lambda1 * lambda2

            Система уравнений:
            A1 * lambda1 + A2 * lambda2 = a
            A1 * (lambda1 ** 2) + A2 * (lambda2 ** 2) = a ** 2 - bc

            Нахождение коэффициентов:
            A1 = lambda1 / (lambda1 - lambda2)
            A2 = -lambda2 / (lambda1 - lambda2)
        """
        coefficients = []
        if lambda1 == lambda2:
            A = Fraction(a**2 - bc - a * lambda1, lambda1**2)
            B = Fraction(a, lambda1) - A
            coefficients.append(A)
            coefficients.append(B)
            return coefficients
        else:
            A1 = Fraction(lambda1, lambda1 - lambda2)
            A2 = Fraction(-lambda2, lambda1 - lambda2)
            coefficients.append(A1)
            coefficients.append(A2)
            return coefficients
