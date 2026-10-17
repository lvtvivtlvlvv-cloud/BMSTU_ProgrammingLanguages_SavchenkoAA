from random import *

r = float(input("R: "))

for i in range(1, 11):
    x = uniform(-2 * r, 2 * r)
    y = uniform(-2 * r, 2 * r)

    if ((x - r)**2 + (y - r)**2 <= r**2 and y <= x) or ((x + r)**2 + (y + r)**2 <= r**2 and y >= x):
        print(f"Выстрел {i}: ({x:.2f}, {y:.2f}) — Попадает")
    else:
        print(f"Выстрел {i}: ({x:.2f}, {y:.2f}) — Не попадает")