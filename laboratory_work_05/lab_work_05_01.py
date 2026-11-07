from random import *

def make_matrix(rows, cols):
    a = []
    for i in range(rows):
        row = []
        for j in range(cols):
            row.append(randint(-100, 100))
        a.append(row)
    return a

def print_matrix(a):
    for row in a:
        for x in row:
            print(f"{x:4}", end="")
        print()

def count_zero_rows(a):
    count = 0
    for row in a:
        if 0 in row:
            count += 1
    return count

def find_longest_series_col(a):
    rows = len(a)
    cols = len(a[0])
    max_len = 0
    best_col = 0

    for j in range(cols):
        cur_len = 1
        max_col_len = 1
        for i in range(1, rows):
            if a[i][j] == a[i - 1][j]:
                cur_len += 1
                if cur_len > max_col_len:
                    max_col_len = cur_len
            else:
                cur_len = 1
        
        if max_col_len > max_len:
            max_len = max_col_len
            best_col = j

    return best_col, max_len

n = int(input("Количество строк: "))
m = int(input("Количество столбцов: "))

matrix = make_matrix(n, m)

print("\nМатрица:")
print_matrix(matrix)

zero_rows = count_zero_rows(matrix)
col_idx, series_len = find_longest_series_col(matrix)

print("\nСтрок с нулями:", zero_rows)
print(f"Столбец с самой длинной серией: {col_idx + 1} (длина серии: {series_len})")