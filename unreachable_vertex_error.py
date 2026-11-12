class UnreachableVertexError(Exception):
    """Недостижимая вершина орграфа.

    Из начальной вершины нет пути в конечную.
    """

    def __init__(self):
        super().__init__("Вершина недостижима")
