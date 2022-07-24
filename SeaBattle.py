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


class Ship:
    def __init__(self, init_pos, length, direction):
        self.init_pos = init_pos
        self.length = length
        self.lives = length
        self.direction = direction

    @property
    def dots(self):
        ship_dots = []
        for i in range(self.length):
            cur_x = self.init_pos.x
            cur_y = self.init_pos.y
            if self.direction:
                cur_x += i
            else:
                cur_y += i
            ship_dots.append(Dot(cur_x, cur_y))
        return ship_dots


class Board:
    def __init__(self, hid=True, size=6):
        self.field = [["0" for i in range(6)] for i in range(6)]
        self.hid = hid
        self.busy = []
        self.lives = []
        self.ships = []
        self.size = size
        count = 0

    def add_ship(self, ship):
        for dot in ship.dots:
            if dot in self.busy or self.out(dot):
                raise BoardShipWrongException
        for dot in ship.dots:
            cur_x = dot.x
            cur_y = dot.y
            self.field[cur_x][cur_y] = "■"
            self.busy.append(dot)
        self.ships.append(ship)
        self.contour(ship)
        return self.field

    def contour(self, ship, hiding_status=True):
        exodus = [
            Dot(-1, 1), Dot(0, 1), Dot(1, 1),
            Dot(-1, 0), Dot(0, 0), Dot(1, 0),
            Dot(-1, -1), Dot(0, -1), Dot(1, -1)
        ]
        for dot in ship.dots:
            for contour_dot in exodus:
                mod_x = dot.x + contour_dot.x
                mod_y = dot.y + contour_dot.y
                d = Dot(mod_x, mod_y)
                if d not in self.busy and not self.out(d):
                    self.busy.append(d)
                    self.field[d.x][d.y] = '.'

    def __str__(self):
        conclusion = ""
        conclusion += "  | 1 | 2 | 3 | 4 | 5 | 6 |"
        for index, value in enumerate(self.field):
            conclusion += f"\n{index + 1} | " + " | ".join(map(str, value)) + " |"
        return conclusion

    def out(self, dot):
        return not ((0 <= dot.x <= self.size) and (0 <= dot.y <= self.size))

    


ship_1 = Ship(Dot(2, 2), 1, 0)
print(ship_1.dots)
b = Board()
b.add_ship(ship_1)
print(b)
