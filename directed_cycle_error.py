class DirectedCycleError(Exception):
    """Ориентированный цикл в орграфе"""

    def __init__(self):
        super().__init__("В орграфе есть ориентированный цикл")
