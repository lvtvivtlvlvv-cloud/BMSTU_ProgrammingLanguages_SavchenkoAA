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

a = []
with open("in5.txt", "r") as f:
    for s in f:
        if s.strip():
            a.append([int(x) for x in s.split()])

k = f1(a)
col, d = f2(a)

with open("out5.txt", "w") as f:
    f.write("Матрица:\n")
    for r in a:
        for x in r:
            f.write(f"{x:4}")
        f.write("\n")
    f.write(f"\nСтрок с нулями: {k}\n")
    f.write(f"Столбец: {col} длина серии: {d}\n")