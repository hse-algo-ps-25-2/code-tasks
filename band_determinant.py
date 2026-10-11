class BandDeterminant:
    """
    Класс, описывающий задачу о ленточном определителе

    Атрибуты:
        a (int): значение главной диагонали
        b (int): значение верхней диагонали
        c (int): значение нижней диагонали
        roots (list): корни характеристического уравнения
        coefficients (list): коэффициенты рекуррентного уравнения
    """

    def __init__(self, a, b, c, roots, coefficients):
        self.a = a
        self.b = b
        self.c = c
        self.roots = roots
        self.coefficients = coefficients

    def __str__(self):
        coef_str = (
            f"A1 = {self.coefficients[0]}, A2 = {self.coefficients[1]}"
            if self.roots[0] != self.roots[1]
            else f"A = {self.coefficients[0]}, B = {self.coefficients[1]}"
        )
        return (
            f"Элементы на диагонали матрицы: a = {self.a}, b = {self.b}, c = {self.c}."
            + "\n"
            + f"Корни характеристического уравнения: {self.roots[0]}, {self.roots[1]}."
            + "\n"
            + f"Коэффициенты для общей формулы: {coef_str}"
        )
