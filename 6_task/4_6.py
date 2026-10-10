with open("in4.txt", "r") as f:
    c = float(f.readline())
    a = [float(x) for x in f.readline().split()]

k = 0
for x in a:
    if x < c:
        k += 1

idx = -1
for i in range(len(a)):
    if a[i] < 0:
        idx = i

s = 0
if idx != -1:
    for i in range(idx + 1, len(a)):
        s += int(a[i])

m = max(a)
b1 = []
b2 = []
for x in a:
    if abs(m - x) <= 0.2 * abs(m):
        b1.append(x)
    else:
        b2.append(x)

a = b1 + b2

with open("out4.txt", "w") as f:
    f.write(f"Меньше C: {k}\n")
    if idx != -1:
        f.write(f"Сумма: {s}\n")
    else:
        f.write("Нет отрицательных\n")
    f.write(f"Массив: {a}\n")