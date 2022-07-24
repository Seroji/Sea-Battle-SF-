class BoardException(Exception):
    pass


class BoarUsedException(BoardException):
    def __str__(self):
        return "Вы уже стреляли в эту клетку!"


class BoardOutException(BoardException):
    def __str__(self):
        return "Эта клетка выходит за рамки поля!"


class BoardShipWrongException(BoardException):
    pass


class Dot:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return f"Dot({self.x}, {self.y})"


