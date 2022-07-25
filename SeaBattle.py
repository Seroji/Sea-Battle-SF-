from random import randint


class BoardException(Exception):
    pass


class BoardUsedException(BoardException):
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
        self.count = 0

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
                    if not hiding_status:
                        self.field[d.x][d.y] = "."

    def __str__(self):
        conclusion = ""
        conclusion += "  | 1 | 2 | 3 | 4 | 5 | 6 |"
        for index, value in enumerate(self.field):
            conclusion += f"\n{index + 1} | " + " | ".join(map(str, value)) + " |"
        if self.hid:
            conclusion = conclusion.replace("■", "0")
        return conclusion

    def out(self, dot):
        return not ((0 <= dot.x <= self.size) and (0 <= dot.y <= self.size))

    def shot(self, dot):
        self.busy = []
        if self.out(dot):
            raise BoardOutException
        if dot in self.busy:
            raise BoardUsedException
        for ship in self.ships:
            if dot in ship.dots:
                ship.lives -= 1
                if not ship.lives:
                    self.count += 1
                    print('Корабль ранен!')
                else:
                    print('Корабль уничтожен!') # Возможно требуются дополнения
                self.field[dot.x][dot.y] = "X"
            else:
                print('Промах!')
                self.field[dot.x][dot.y] = "."


class Player:
    def __init__(self, board, enemy):
        self.board = board
        self.enemy = enemy

    def ask(self):
        pass

    def move(self):
        while True:
            try:
                obj = self.ask()
                repeat = self.enemy.shot(obj)
                return repeat
            except BoardException as e:
                print(e)


class AI(Player):
    def ask(self):
        dot = Dot(randint(0,5), randint(0,5))
        return dot


class User(Player):
    def ask(self):
        while True:
            coordinates = input('Введите координаты в формате X, Y: ')
            if len(coordinates) != 3:
                print("Введите координаты в указанном формате!")
                continue
            x, y = coordinates.split(",")
            if not ((x.isnumeric()) and (y.isnumeric())):
                print('Введите координаты в форме целых чисел!')
                continue
            x, y = int(x), int(y)
            dot = Dot(x - 1, y - 1)
            return dot


class Game:
    def __init__(self):
        self.us_board = Board()
        self.ai_board = Board()
        self.us = User(self.us_board, self.ai_board)
        self.ai = AI(self.ai_board, self.us_board)

    @staticmethod
    def random_place():
        vehicles = [3, 2, 2, 1, 1, 1, 1]
        board = Board()
        attempts = 0
        for sh in vehicles:
            while True:
                attempts += 1
                if attempts > 2000:
                    return None
                ship = Ship(Dot(randint(0, 5), randint(0, 5)), sh, randint(0, 1))
                try:
                    board.add_ship(ship)
                    break
                except BoardShipWrongException:
                    pass
                except IndexError:
                    pass
        return board

    def random_board(self):
        board = None
        while board is None:
            board = self.random_place()
        return board

    def greet(self):
        print('Добро пожаловать в игру')
        print('Морской бой')
        print('-' * 20)


g = Game()
print(g.random_board())







