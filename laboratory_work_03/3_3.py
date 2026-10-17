xb = float(input("Xнач: "))
xe = float(input("Xкон: "))
dx = float(input("dx: "))
eps = float(input("eps: "))

print("+--------+----------+-----+")
print("|   X    |    Y     |  N  |")
print("+--------+----------+-----+")

x = xb
while x <= xe + dx / 2:
    an = x - 1
    s = an
    n = 0

    while abs(an) >= eps:
        k = -(x - 1) * (n + 1) / (n + 2)
        an = an * k
        s += an
        n += 1

    print(f"| {x:6.2f} | {s:8.4f} | {n + 1:3d} |")
    x += dx

print("+--------+----------+-----+")