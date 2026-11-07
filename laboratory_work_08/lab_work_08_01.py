from tkinter import *


def f(n, a, b, c):
    global cv, W, H

    p = []
    for i in range(n):
        p.append((b[i] - a[i]) / a[i] * 100)

    l = 80
    r = 40
    t = 70
    d = 170
    w = W - l - r
    h = H - t - d

    ma = max(p)
    ma = (int(ma) // 10 + 1) * 10

    for i in range(6):
        v = ma * i / 5
        y = H - d - v / ma * h
        cv.create_line(l, y, W - r, y, fill="#e0e0e0")
        cv.create_line(l - 6, y, l, y, fill="black")
        cv.create_text(l - 10, y, text=str(round(v, 1)), anchor="e",
                       font=("Liberation Sans", 10))

    cv.create_line(l, t, l, H - d, fill="black", width=2)
    cv.create_line(l, H - d, W - r, H - d, fill="black", width=2)

    k = w / n
    bw = k * 0.55
    mp = max(p)
    for i in range(n):
        x = l + (i + 0.5) * k
        hh = p[i] / ma * h
        if p[i] == mp:
            col = "red"
        else:
            col = "#4472c4"
        cv.create_rectangle(x - bw / 2, H - d - hh, x + bw / 2, H - d,
                            fill=col, outline="black")
        cv.create_text(x, H - d - hh - 12, text="{:.1f}".format(p[i]),
                       font=("Liberation Sans", 10))
        cv.create_text(x, H - d + 14, text=c[i], angle=90, anchor="w",
                       font=("Liberation Sans", 11))

    av = sum(p) / n
    y = H - d - av / ma * h
    cv.create_line(l, y, W - r, y, fill="green", dash=(6, 4), width=2)
    cv.create_text(W - r - 24, y - 10, text="средняя {:.1f}%".format(av),
                   anchor="e", fill="green", font=("Liberation Sans", 10))

    y = H - d - mp / ma * h
    cv.create_line(l, y, W - r, y, fill="red", dash=(2, 3), width=2)
    cv.create_text(W - r - 24, y - 10, text="максимальная {:.1f}%".format(mp),
                   anchor="e", fill="red", font=("Liberation Sans", 10))

    cv.create_text(W / 2, 25, text="Норма прибыли при реализации шоколада",
                   font=("Liberation Sans", 16, "bold"))
    cv.create_text(25, t + h / 2, text="Прибыль, %", angle=90,
                   font=("Liberation Sans", 12))
    cv.create_text(l + w / 2, H - 25, text="Сорт шоколада",
                   font=("Liberation Sans", 12))


def main():
    global cv, W, H

    root = Tk()
    root.title("Лабораторная работа № 8")
    root.resizable(False, False)

    W = int(root.winfo_screenwidth() * 0.7)
    H = int(root.winfo_screenheight() * 0.7)

    cv = Canvas(root, width=W, height=H, bg="white")
    cv.pack()

    a = []
    b = []
    c = []
    q = open("lab8_pb_in.txt", "r", encoding="utf-8")
    for s in q:
        z = s.split()
        if len(z) < 3:
            continue
        c.append(z[0])
        a.append(float(z[1]))
        b.append(float(z[2]))
    q.close()

    n = len(a)
    f(n, a, b, c)

    root.mainloop()


if __name__ == "__main__":
    main()
