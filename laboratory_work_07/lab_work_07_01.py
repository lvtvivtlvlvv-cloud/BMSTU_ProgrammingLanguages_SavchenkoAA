from math import sqrt
import turtle as tr


def f(x):
    if x < -3 or x > 7:
        return None
    if x < -2:
        return -x - 2
    if x < 0:
        return sqrt(max(0.0, 1.0 - (x + 1.0) ** 2))
    if x < 4:
        return -sqrt(max(0.0, 4.0 - (x - 2.0) ** 2))
    if x < 6:
        return -0.5 * (x - 4.0)
    return -1.0


def g(x, y, a):
    tr.up()
    tr.goto(x, y)
    tr.begin_fill()
    if a == 0:
        tr.goto(x - 0.3, y + 0.12)
        tr.goto(x - 0.3, y - 0.12)
    else:
        tr.goto(x + 0.12, y - 0.3)
        tr.goto(x - 0.12, y - 0.3)
    tr.goto(x, y)
    tr.end_fill()


def h(x1, x2, y1, y2):
    tr.width(2)
    tr.color("black")
    tr.up()
    tr.goto(x1, 0)
    tr.down()
    tr.goto(x2 - 0.3, 0)
    g(x2 - 0.3, 0, 0)
    tr.up()
    tr.goto(0, y1)
    tr.down()
    tr.goto(0, y2 - 0.3)
    g(0, y2 - 0.3, 1)

    tr.up()
    for i in range(-4, 8):
        tr.goto(i, -0.1)
        tr.down()
        tr.goto(i, 0.1)
        tr.up()
        tr.goto(i, -0.45)
        if i != 0:
            tr.write(str(i), align="center", font=("Arial", 22, "normal"))

    for i in range(-2, 2):
        tr.goto(-0.1, i)
        tr.down()
        tr.goto(0.1, i)
        tr.up()
        tr.goto(-0.2, i - 0.08)
        if i != 0:
            tr.write(str(i), align="right", font=("Arial", 22, "normal"))

    tr.up()
    tr.goto(x2 - 0.3, -0.45)
    tr.write("X", font=("Arial", 26, "bold"))
    tr.goto(0.18, y2 - 0.3)
    tr.write("Y", font=("Arial", 26, "bold"))


def grafik(x1, x2):
    tr.color("green")
    tr.width(3)
    n = 1500
    dx = (x2 - x1) / n
    x = x1
    y = f(x)
    tr.up()
    tr.goto(x, y)
    tr.down()
    while x <= x2:
        x += dx
        y = f(x)
        if y is None:
            break
        tr.goto(x, y)


def main():
    a = (-4.5, 7.8)
    b = (-2.8, 2.2)
    dx = 1200
    dy = int(dx / ((a[1] - a[0]) / (b[1] - b[0])))
    tr.setup(dx, dy)
    tr.reset()
    tr.setworldcoordinates(a[0], b[0], a[1], b[1])
    tr.title("Лабораторная работа № 7, задание 1")
    tr.ht()
    tr.tracer(0, 0)
    h(a[0], a[1], b[0], b[1])
    grafik(-3.0, 7.0)
    tr.up()
    tr.goto(4.2, b[1] - 0.3)
    tr.write("График функции y = f(x)", align="center",
             font=("Arial", 28, "bold"))
    tr.mainloop()


if __name__ == "__main__":
    main()
