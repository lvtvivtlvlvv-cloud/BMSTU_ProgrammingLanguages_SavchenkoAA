from math import log
import turtle as tr

eps = 0.001


def f(x):
    a = x - 1.0
    s = a
    n = 0
    while abs(a) >= eps:
        a = a * (-(x - 1.0) * (n + 1) / (n + 2))
        s += a
        n += 1
    return s


def g(x, y, a):
    tr.up()
    tr.goto(x, y)
    tr.begin_fill()
    if a == 0:
        tr.goto(x - 0.08, y + 0.03)
        tr.goto(x - 0.08, y - 0.03)
    else:
        tr.goto(x + 0.03, y - 0.08)
        tr.goto(x - 0.03, y - 0.08)
    tr.goto(x, y)
    tr.end_fill()


def h(x1, x2, y1, y2):
    tr.color("black")
    tr.width(2)
    tr.up()
    tr.goto(x1, 0)
    tr.down()
    tr.goto(x2 - 0.05, 0)
    g(x2 - 0.05, 0, 0)
    tr.up()
    tr.goto(0, y1)
    tr.down()
    tr.goto(0, y2 - 0.06)
    g(0, y2 - 0.06, 1)

    tr.up()
    x = 0.2
    while x <= 2.0001:
        tr.goto(x, -0.07)
        tr.down()
        tr.goto(x, 0.07)
        tr.up()
        tr.goto(x, -0.2)
        tr.write("%.1f" % x, align="center", font=("Arial", 16, "normal"))
        x += 0.2

    y = -2.0
    while y <= 0.5001:
        tr.goto(-0.04, y)
        tr.down()
        tr.goto(0.04, y)
        tr.up()
        tr.goto(-0.07, y - 0.04)
        tr.write("%.1f" % y, align="right", font=("Arial", 16, "normal"))
        y += 0.5

    tr.up()
    tr.goto(x2 - 0.1, -0.28)
    tr.write("X", font=("Arial", 20, "bold"))
    tr.goto(0.05, y2 - 0.1)
    tr.write("Y", font=("Arial", 20, "bold"))


def grafik(x1, x2):
    tr.color("green")
    tr.width(3)
    n = 800
    dx = (x2 - x1) / n
    x = x1
    tr.up()
    tr.goto(x, f(x))
    tr.down()
    while x <= x2:
        x += dx
        tr.goto(x, f(x))


def e(x1, x2):
    tr.color("red")
    n = 800
    dx = (x2 - x1) / n
    tr.up()
    for i in range(n + 1):
        x = x1 + i * dx
        tr.goto(x, log(x))
        if i % 8 == 0:
            tr.dot(4, "red")


def main():
    x1 = -0.38
    x2 = 2.15
    y1 = -2.55
    y2 = 0.9

    dx = 800
    dy = int(dx / ((x2 - x1) / (y2 - y1)))
    tr.setup(dx, dy)
    tr.reset()
    tr.setworldcoordinates(x1, y1, x2, y2)
    tr.title("Лабораторная работа № 7, задание 3")
    tr.ht()
    tr.tracer(0, 0)

    h(x1, x2, y1, y2)
    grafik(0.1, 2.0)
    e(0.1, 2.0)

    tr.up()
    tr.color("green")
    tr.width(4)
    tr.goto(1.05, 0.72)
    tr.down()
    tr.goto(1.25, 0.72)
    tr.up()
    tr.color("black")
    tr.goto(1.3, 0.68)
    tr.write("ряд (eps = 0.001)", font=("Arial", 16, "normal"))

    tr.color("red")
    tr.goto(1.15, 0.55)
    tr.dot(6, "red")
    tr.up()
    tr.color("black")
    tr.goto(1.3, 0.51)
    tr.write("ln(x)", font=("Arial", 16, "normal"))

    tr.up()
    tr.goto((x1 + x2) / 2, y2 - 0.12)
    tr.write("y = ln(x), вычисленный через ряд", align="center",
             font=("Arial", 22, "bold"))

    tr.mainloop()


if __name__ == "__main__":
    main()
