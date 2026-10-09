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
