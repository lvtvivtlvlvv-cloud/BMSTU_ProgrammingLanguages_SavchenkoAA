r = float(input("R: "))
x = float(input("X: "))
y = float(input("Y: "))

if ((x - r)**2 + (y - r)**2 <= r**2 and y <= x) or ((x + r)**2 + (y + r)**2 <= r**2 and y >= x):
    print("Попадает")
else:
    print("Не попадает")