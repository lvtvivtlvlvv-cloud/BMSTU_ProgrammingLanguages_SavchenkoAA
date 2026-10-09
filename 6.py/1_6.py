from math import *

with open("in1.txt", "r") as f1, open("out1.txt", "w") as f2:
    f2.write("   a         z1         z2\n")
    for s in f1:
        s = s.strip()
        if not s:
            continue
        a = float(s)
        if a <= 0 or a == 2:
            f2.write(f"{a:6.2f}   ошибка\n")
        else:
            z1 = ((a + 2) / sqrt(2 * a) - a / (sqrt(2 * a) + 2) + 2 / (a - sqrt(2 * a))) * (sqrt(a) - sqrt(2)) / (a + 2)
            z2 = 1 / (sqrt(a) + sqrt(2))
            f2.write(f"{a:6.2f} {z1:10.4f} {z2:10.4f}\n")