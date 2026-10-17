from random import *

n = int(input("n: "))
c = float(input("C: "))

a = []
for i in range(n):
    a.append(round(uniform(-20, 20), 2))

print("Исходный:", a)

k = 0
for x in a:
    if x < c:
        k += 1


idx = -1
for i in range(n):
    if a[i] < 0:
        idx = i

s = 0
if idx != -1:
    for i in range(idx + 1, n):
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

print("Кол-во меньше C:", k)
if idx != -1:
    print("Сумма:", s)
else:
    print("Нет отрицательных")
print("Итог:", a)