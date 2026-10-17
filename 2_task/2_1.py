from math import *

x = float(input("x: "))

r1 = 1
r2 = 2

if -3 <= x < -2:
    y = -x - 2
elif -2 <= x < 0:
    y = sqrt(r1**2 - (x + 1)**2)
elif 0 <= x < 4:
    y = -sqrt(r2**2 - (x - 2)**2)
elif 4 <= x < 6:
    y = -0.5 * (x - 4)
elif 6 <= x <= 7:
    y = -1.0
else:
    print("x вне диапазона графика")
    exit()

print("y =", y)
