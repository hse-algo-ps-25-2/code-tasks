"""Тесты трёх функций из main.py. Запуск: python test.py."""

import math
import unittest
from itertools import product

import main

INVALID_TYPES = (
    None,
    True,
    False,
    1.0,
    1.5,
    0.0,
    -2.5,
    float("nan"),
    float("inf"),
    float("-inf"),
    "abc",
    "",
    "5",
    "null",
    "nil",
    "nill",
    "true",
    b"5",
    [],
    [1],
    {},
    {"n": 1},
    (),
    (1,),
    {1},
    complex(1, 0),
)

BINOMIAL_FUNCTION_NAMES = (
    "binomial_coefficient_iter",
    "binomial_coefficient_rec",
)


def brute_force_triangle_count(length):
    count = 0

    for middle in product("ABC", repeat=length - 1):
        route = ("A",) + middle + ("A",)

        if all(left != right for left, right in zip(route, route[1:])):
            count += 1

    return count


class TrianglePathTests(unittest.TestCase):
    def test_invalid_types_raise_type_error(self):
        for value in INVALID_TYPES:
            with self.subTest(value=repr(value)):
                with self.assertRaises(TypeError):
                    main.get_triangle_path_count(value)

    def test_nonpositive_lengths_raise_value_error(self):
        for length in (0, -1, -5, -100):
            with self.subTest(length=length):
                with self.assertRaises(ValueError):
                    main.get_triangle_path_count(length)

    def test_known_results(self):
        cases = (
            (1, 0),
            (2, 2),
            (3, 2),
            (4, 6),
            (5, 10),
            (6, 22),
            (7, 42),
            (8, 86),
            (10, 342),
            (12, 1366),
        )

        for length, expected in cases:
            with self.subTest(length=length):
                actual = main.get_triangle_path_count(length)
                self.assertIs(type(actual), int)
                self.assertEqual(actual, expected)

    def test_results_match_direct_enumeration(self):
        for length in range(1, 10):
            with self.subTest(length=length):
                actual = main.get_triangle_path_count(length)
                self.assertIs(type(actual), int)
                self.assertEqual(actual, brute_force_triangle_count(length))


class BinomialCoefficientTests(unittest.TestCase):
    def test_invalid_n_types_raise_type_error(self):
        for name in BINOMIAL_FUNCTION_NAMES:
            function = getattr(main, name)

            for value in INVALID_TYPES:
                with self.subTest(function=name, n=repr(value), k=0):
                    with self.assertRaises(TypeError):
                        function(value, 0)

    def test_invalid_k_types_raise_type_error(self):
        for name in BINOMIAL_FUNCTION_NAMES:
            function = getattr(main, name)

            for value in INVALID_TYPES:
                with self.subTest(function=name, n=5, k=repr(value)):
                    with self.assertRaises(TypeError):
                        function(5, value)

    def test_invalid_integer_values_raise_value_error(self):
        cases = ((-1, 0), (0, -1), (-1, -1), (5, -1), (-5, 2),
                 (1, 2), (0, 1), (5, 6))

        for name in BINOMIAL_FUNCTION_NAMES:
            function = getattr(main, name)

            for n, k in cases:
                with self.subTest(function=name, n=n, k=k):
                    with self.assertRaises(ValueError):
                        function(n, k)

    def test_known_results_including_boundaries(self):
        cases = (
            (0, 0, 1),
            (1, 0, 1),
            (1, 1, 1),
            (5, 0, 1),
            (5, 5, 1),
            (5, 2, 10),
            (5, 3, 10),
            (6, 2, 15),
            (10, 5, 252),
            (30, 20, 30045015),
        )

        for name in BINOMIAL_FUNCTION_NAMES:
            function = getattr(main, name)

            for n, k, expected in cases:
                with self.subTest(function=name, n=n, k=k):
                    actual = function(n, k)
                    self.assertIs(type(actual), int)
                    self.assertEqual(actual, expected)

    def test_results_match_math_comb(self):
        for name in BINOMIAL_FUNCTION_NAMES:
            function = getattr(main, name)

            for n in range(31):
                for k in range(n + 1):
                    with self.subTest(function=name, n=n, k=k):
                        actual = function(n, k)
                        self.assertIs(type(actual), int)
                        self.assertEqual(actual, math.comb(n, k))

    def test_large_results_remain_exact_integers(self):
        cases = ((60, 30), (100, 50), (10**30, 1), (10**30, 2))

        for name in BINOMIAL_FUNCTION_NAMES:
            function = getattr(main, name)

            for n, k in cases:
                with self.subTest(function=name, n=n, k=k):
                    actual = function(n, k)
                    self.assertIs(type(actual), int)
                    self.assertEqual(actual, math.comb(n, k))


if __name__ == "__main__":
    unittest.main(verbosity=2)
