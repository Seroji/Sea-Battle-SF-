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
    def __init__(self, hid=True):
        self.field = [["0" for i in range(6)] for i in range(6)]
        self.hid = hid
        self.busy = []
        self.ships = []
        self.size = 6
        self.count = 0
        self.busy_dot = []

    def add_ship(self, ship):
        for dot in ship.dots:
            if dot in self.busy or self.out(dot):
                raise BoardShipWrongException
        for dot in ship.dots:
            cur_x = dot.x
            cur_y = dot.y
            self.field[cur_x][cur_y] = "■"
        self.ships.append(ship)
        self.contour(ship)

    def contour(self, ship, hiding_status = True):
        exodus = [
            Dot(-1, 1), Dot(0, 1), Dot(1, 1),
            Dot(-1, 0), Dot(0, 0), Dot(1, 0),
            Dot(-1, -1), Dot(0, -1), Dot(1, -1)
        ]
        cont = []
        for dot in ship.dots:
            for contour_dot in exodus:
                mod_x = dot.x + contour_dot.x
                mod_y = dot.y + contour_dot.y
                d = Dot(mod_x, mod_y)
                if d not in self.busy_dot and not self.out(d):
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
        return not ((0 <= dot.x < self.size) and (0 <= dot.y < self.size))

    def shot(self, dot):
        if self.out(dot):
            raise BoardOutException
        if dot in self.busy_dot:
            raise BoardUsedException
        self.busy_dot.append(dot)
        for ship in self.ships:
            if dot in ship.dots:
                ship.lives -= 1
                self.count += 1
                if ship.lives == 0:
                    print('Корабль уничтожен!')
                    print("-" * 20)
                    self.contour(ship,hiding_status = False)
                    self.field[dot.x][dot.y] = "X"
                    return True
                else:
                    print('Корабль ранен!')
                    print("-" * 20)
                    self.field[dot.x][dot.y] = "X"
                    return True
        print('Промах!')
        print("-" * 20)
        self.field[dot.x][dot.y] = "."
        return False


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
        print(f"Выбранная компьютером точка: {dot.x},{dot.y}")
        return dot


class User(Player):
    def ask(self):
        while True:
            coordinates = input('Введите координаты в формате X, Y: ')
            if len(coordinates) != 3:
                print("Введите координаты в указанном формате!")
                continue
            if coordinates[1] != ',':
                print('Введите корректные координаты!')
                continue
            x, y = coordinates.split(",")
            if not ((x.isnumeric()) and (y.isnumeric())):
                print('Введите координаты в форме целых чисел!')
                continue
            x, y = int(x), int(y)
            dot = Dot(y - 1, x - 1)
            return dot


class Game:
    def __init__(self):
        us_board = self.random_board()
        ai_board = self.random_board()
        self.us = User(us_board, ai_board)
        self.ai = AI(ai_board, us_board)
        ai_board.hid = True

    @staticmethod
    def random_place():
        vehicles = [3,2,2,1,1,1,1]
        board = Board(hid=False)
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
        return board

    def random_board(self):
        board = None
        while board is None:
            board = self.random_place()
        return board

    @staticmethod
    def greet():
        print('Добро пожаловать в игру')
        print('Морской бой')
        print('-' * 20)

    def loop(self):
        turn = 0
        while True:
            print("Ваша доска:")
            print(self.us.board)
            print("-" * 20)
            print("Доска компьютера:")
            print(self.ai.board)
            print("-" * 20)
            if turn == 0:
                print('Ваш ход!')
                self.us.move()
                turn += 1
                if self.ai.board.count == 11:
                    print('Победа пользователя!')
                    break

            if turn == 1:
                print('Ход компьютера!')
                self.ai.move()
                turn -= 1
                if self.us.board.count == 11:
                    print('Победа компьютера!')
                    break

    def start(self):
        self.greet()
        self.loop()


g = Game()
g.start()



