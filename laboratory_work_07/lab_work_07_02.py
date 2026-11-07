from math import pi, cos, sin
from random import uniform
import turtle as tr


def f(x, y, r):
    return (((x - r) ** 2 + (y - r) ** 2 <= r ** 2 and y <= x) or
            ((x + r) ** 2 + (y + r) ** 2 <= r ** 2 and y >= x))


def g(x, y, a):
    tr.up()
    tr.goto(x, y)
    tr.begin_fill()
    if a == 0:
        tr.goto(x - 0.35, y + 0.14)
        tr.goto(x - 0.35, y - 0.14)
    else:
        tr.goto(x + 0.14, y - 0.35)
        tr.goto(x - 0.14, y - 0.35)
    tr.goto(x, y)
    tr.end_fill()


def h(x1, x2, y1, y2):
    tr.color("black")
    tr.width(2)
    tr.up()
    tr.goto(x1, 0)
    tr.down()
    tr.goto(x2 - 0.4, 0)
    g(x2 - 0.4, 0, 0)
    tr.up()
    tr.goto(0, y1)
    tr.down()
    tr.goto(0, y2 - 0.4)
    g(0, y2 - 0.4, 1)

    tr.up()
    for i in range(int(x1) + 1, int(x2)):
        tr.goto(i, -0.18)
        tr.down()
        tr.goto(i, 0.18)
        tr.up()
        tr.goto(i, -0.55)
        if i != 0:
            tr.write(str(i), align="center", font=("Arial", 18, "normal"))

    for i in range(int(y1) + 1, int(y2)):
        tr.goto(-0.18, i)
        tr.down()
        tr.goto(0.18, i)
        tr.up()
        tr.goto(-0.3, i - 0.1)
        if i != 0:
            tr.write(str(i), align="right", font=("Arial", 18, "normal"))

    tr.up()
    tr.goto(x2 - 0.3, -0.6)
    tr.write("X", font=("Arial", 24, "bold"))
    tr.goto(0.25, y2 - 0.45)
    tr.write("Y", font=("Arial", 24, "bold"))


def circle(x, y, r):
    tr.up()
    tr.goto(x + r, y)
    tr.down()
    tr.width(2)
    for i in range(1, 181):
        a = 2 * pi * i / 180
        tr.goto(x + r * cos(a), y + r * sin(a))


def main():
    r = float(input("R: "))
    x1 = -2 * r - 0.8
    x2 = 2 * r + 0.8
    y1 = -2 * r - 0.8
    y2 = 2 * r + 0.8

    dx = 850
    dy = int(dx * (y2 - y1) / (x2 - x1))
    tr.setup(dx, dy)
    tr.reset()
    tr.setworldcoordinates(x1, y1, x2, y2)
    tr.title("Лабораторная работа № 7, задание 2")
    tr.ht()
    tr.tracer(0, 0)

    n = 10000
    k = 0
    tr.up()
    for i in range(n):
        x = uniform(-2 * r, 2 * r)
        y = uniform(-2 * r, 2 * r)
        tr.goto(x, y)
        if f(x, y, r):
            tr.dot(4, "green")
            k += 1
        else:
            tr.dot(4, "#d9d9d9")

    tr.color("blue")
    circle(r, r, r)
    circle(-r, -r, r)
    tr.up()
    tr.goto(-2 * r - 0.4, -2 * r - 0.4)
    tr.down()
    tr.goto(2 * r + 0.4, 2 * r + 0.4)

    h(x1, x2, y1, y2)

    s1 = 16 * r * r * k / n
    s2 = pi * r * r
    e = abs(s1 - s2) / s2 * 100

    tr.up()
    tr.goto(x1 + 0.25, y2 - 0.45)
    tr.color("black")
    tr.write("N = %d\nNf = %d\nS = %.3f\nS точн. = %.3f\n"
             "Погрешность = %.2f %%" % (n, k, s1, s2, e),
             font=("Arial", 16, "bold"))

    tr.goto(2.1, y2 - 0.2)
    tr.write("Оценка площади методом Монте-Карло", align="center",
             font=("Arial", 13, "bold"))

    print("N =", n)
    print("Nf =", k)
    print("S =", round(s1, 4))
    print("S точн. =", round(s2, 4))
    print("Погрешность =", round(e, 2), "%")

    tr.mainloop()


if __name__ == "__main__":
    main()
