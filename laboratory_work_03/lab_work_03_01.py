from math import *

xb = float(input("Xнач: "))
xe = float(input("Xкон: "))
dx = float(input("dx: "))

r1 = 1
r2 = 2

print("\nТаблица значений функции")
print("+--------+----------+")
print("|   X    |    Y     |")
print("+--------+----------+")

x = xb
while x <= xe + dx / 2:
    if -3 <= x < -2:
        y = -x - 2
    elif -2 <= x < 0:
        val = max(0.0, r1**2 - (x + 1)**2)
        y = sqrt(val)
    elif 0 <= x < 4:
        val = max(0.0, r2**2 - (x - 2)**2)
        y = -sqrt(val)
    elif 4 <= x < 6:
        y = -0.5 * (x - 4)
    elif 6 <= x <= 7:
        y = -1.0
    else:
        y = None

    if y is not None:
        print(f"| {x:6.2f} | {y:8.4f} |")
    else:
        print(f"| {x:6.2f} |    нет   |")

    x += dx

print("+--------+----------+")