from random import *

def show(a):
    for r in a:
        for x in r:
            print(f"{x:4}", end="")
        print()

def f1(a):
    k = 0
    for r in a:
        if 0 in r:
            k += 1
    return k

def f2(a):
    n = len(a)
    m = len(a[0])
    mx = 0
    ans = 0
    for j in range(m):
        cur = 1
        cur_mx = 1
        for i in range(1, n):
            if a[i][j] == a[i - 1][j]:
                cur += 1
                if cur > cur_mx:
                    cur_mx = cur
            else:
                cur = 1
        if cur_mx > mx:
            mx = cur_mx
            ans = j
    return ans + 1, mx

n = int(input("n: "))
m = int(input("m: "))

a = []
for i in range(n):
    r = []
    for j in range(m):
        r.append(randint(-10, 10))
    a.append(r)

print("Матрица:")
show(a)

k = f1(a)
col, d = f2(a)

print("Строк с нулями:", k)
print("Столбец:", col, "длина серии:", d)