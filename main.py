"""Пример генератора перестановок и полного перебора коммивояжёра.

Функцию generate_permutations нужно реализовать в permutation_generator.py.
Метод get_distance — в tsp_abs_solver.py.
Метод get_tsp_solution — в brute_force_tsp_solver.py.
"""

from brute_force_tsp_solver import BruteForceTspSolver
from permutation_generator import generate_permutations


def main():
    print(list(generate_permutations([1, 2, 3])))
    matrix = [[None, 1.0], [2.0, None]]
    solver = BruteForceTspSolver(matrix)
    print(solver.get_distance(matrix, [0, 1, 0]))
    print(solver.get_tsp_solution())


if __name__ == "__main__":
    main()
