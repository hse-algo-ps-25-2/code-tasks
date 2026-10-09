import unittest
from fractions import Fraction
from band_determinant import BandDeterminant
from bd_generator import BDGenerator


class TestBDGenerator(unittest.TestCase):
    """Набор тестов для класса BDGenerator"""

    def test_generate_result_types(self):
        """Тестирует корректность типов и диапазон возвращаемого результата"""
        generator = BDGenerator()
        low_bound = -10
        high_bound = 10
        result = generator.generate_brand_determinant(low_bound, high_bound)
        self.assertIsInstance(result, BandDeterminant)

        for root in result.roots:
            self.assertIsInstance(root, int)

        self.assertIsInstance(result.a, int)
        self.assertIsInstance(result.b, int)
        self.assertIsInstance(result.c, int)

        for coefficient in result.coefficients:
            self.assertIsInstance(coefficient, Fraction)

    def test_generate_forced_same_roots(self):
        """Тестирует корректную генерацию кратных корней для диапазона длины 1"""
        generator = BDGenerator()

        result = generator.generate_brand_determinant(1, 1)
        self.assertEqual(result.roots[0], result.roots[1])
        self.assertEqual(result.roots[0], 1)
        self.assertEqual(result.a, 2)
        self.assertEqual(result.b, 1)
        self.assertEqual(result.c, 1)
        self.assertEqual(result.coefficients[0], 1)
        self.assertEqual(result.coefficients[1], 1)

    def test_generate_result_valid(self):
        """
        Тестирует математическую корректность возвращаемого результата

        Проверяется, что задача не вырожденная
        Проверяется, что сгенерированные значения - небольшие числа
        (ограничение зависит от диапазона)

        Проверяется, что возвращаемые значения удовлетворяют условиям:
        a = root1 + root2
        b * c = root1 * root2

        Для кратных корней:
        (A + B)*root1 = a
        (2*A + B)*root1^2 = a^2 - b*c

        Для разных корней:
        A1*root1 + A2*root2 = a
        A1*root1^2 + A2*root2^2 = a^2 - b*c

        Так как генерация произвольная, тест выполняется в цикле
        с разными значениями границ диапазона
        """
        generator = BDGenerator()
        for offset in range(100):
            low_bound = -10 - offset
            high_bound = 10 + offset

            with self.subTest(low_bound=low_bound, high_bound=high_bound):
                result = generator.generate_brand_determinant(low_bound, high_bound)

                for root in result.roots:
                    self.assertGreaterEqual(root, low_bound)
                    self.assertLessEqual(root, high_bound)
                    self.assertNotEqual(root, 0)

                self.assertNotEqual(result.b, 0)
                self.assertNotEqual(result.c, 0)

                self.assertLessEqual(abs(result.a), 2 * high_bound)
                self.assertLessEqual(abs(result.b), high_bound)
                self.assertLessEqual(abs(result.c), high_bound)

                for coefficients in result.coefficients:
                    self.assertLessEqual(abs(coefficients), high_bound)

                self.assertEqual(result.a, result.roots[0] + result.roots[1])
                self.assertEqual(result.b * result.c, result.roots[0] * result.roots[1])

                if result.roots[0] == result.roots[1]:
                    self.assertEqual(
                        (result.coefficients[0] + result.coefficients[1])
                        * result.roots[0],
                        result.a,
                    )
                    self.assertEqual(
                        (2 * result.coefficients[0] + result.coefficients[1])
                        * result.roots[0] ** 2,
                        result.a**2 - result.b * result.c,
                    )
                else:
                    self.assertEqual(
                        result.coefficients[0] * result.roots[0]
                        + result.coefficients[1] * result.roots[1],
                        result.a,
                    )
                    self.assertEqual(
                        result.coefficients[0] * result.roots[0] ** 2
                        + result.coefficients[1] * result.roots[1] ** 2,
                        result.a**2 - result.b * result.c,
                    )

    def test_generate_invalid_bounds(self):
        """Тестирует ошибку при передаче некорректных границ диапазона"""
        generator = BDGenerator()
        low_bound = 5
        high_bound = 1

        self.assertRaises(
            ValueError, generator.generate_brand_determinant, low_bound, high_bound
        )
