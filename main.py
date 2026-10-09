"""Пример использования BruteForceSolver.

Класс BruteForceSolver нужно реализовать в brute_force_solver.py.
Методы get_weight, get_cost и _validate_params — в knapsack_abs_solver.py.
"""

from brute_force_solver import BruteForceSolver


def main():
    weights = [11, 4, 8, 6, 3, 5, 5]
    costs = [17, 6, 11, 10, 5, 8, 6]
    weight_limit = 30
    print("Пример решения задачи о рюкзаке полным перебором")
    print(f"Веса предметов: {weights}")
    print(f"Стоимости предметов: {costs}")
    print(f"Ограничение вместимости: {weight_limit}")
    solver = BruteForceSolver(weights, costs, weight_limit)
    result = solver.get_knapsack()
    print(f"Максимальная стоимость: {result.cost}, индексы предметов: {result.items}")


if __name__ == "__main__":
    main()
