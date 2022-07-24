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


