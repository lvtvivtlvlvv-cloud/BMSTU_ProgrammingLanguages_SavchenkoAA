from math import *

a = float(input())

z1 = ((a + 2) / sqrt(2 * a) - a / (sqrt(2 * a) + 2) + 2 / (a - sqrt(2 * a))) * (sqrt(a) - sqrt(2)) / (a + 2)
z2 = 1 / (sqrt(a) + sqrt(2))

print(f"решение - {z1}")
print(f"решение - {z2}")