class Dot:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class User:
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
            return Dot(x-1, y-1)

