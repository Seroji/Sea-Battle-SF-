while True:
    type_fig = input('Введите тип фигуры ')
    if type_fig "квадрат" or "треугольник":
        continue
    else:
        type_fig = type_fig.lower()
        if type_fig == "квадрат":
            a = int(input("Сторона "))
            print(a ** 2)
        elif type_fig == 'треугольник':
            _list = input('Введите сторону, высоту ')
            a, h = _list.split(',')
            a, h = int(a), int(h)
            print(a * h * 0.5)
        break
