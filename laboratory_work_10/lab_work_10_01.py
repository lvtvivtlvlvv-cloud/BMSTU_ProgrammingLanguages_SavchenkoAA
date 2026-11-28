import sys

KEY = {"если", "иначе", "пока", "возврат", "функция", "истина", "ложь", "программа"}
ONE = set("+-*/%=<>!&|")
SEP = set("(){}[],;.:")
TWO = {"==", "!=", "<=", ">=", "+=", "-=", "&&", "||", "++"}


class E(Exception):
    def __init__(self, s, l, c):
        self.s = s
        self.l = l
        self.c = c

    def __str__(self):
        return "LexError [{}:{}]: {}".format(self.l, self.c, self.s)


class T:
    def __init__(self, t, v, l, c):
        self.t = t
        self.v = v
        self.l = l
        self.c = c

    def __repr__(self):
        return "{}:{}@{}:{}".format(self.t, self.v, self.l, self.c)


class L:
    def __init__(self, s):
        self.s = s
        self.i = 0
        self.l = 1
        self.c = 1

    def go(self):
        a = self.s[self.i]
        self.i += 1
        if a == "\n":
            self.l += 1
            self.c = 1
        else:
            self.c += 1
        return a

    def see(self, n=0):
        a = self.i + n
        if a < len(self.s):
            return self.s[a]
        return ""

    def run(self):
        a = []
        while self.i < len(self.s):
            c = self.see()
            if c in " \t\r\n":
                self.go()
            elif c == "/" and self.see(1) == "/":
                self.com()
            elif c == "/" and self.see(1) == "*":
                self.com2()
            elif c.isdigit() or (c == "." and self.see(1).isdigit()):
                a.append(self.num())
            elif c.isalpha() or c == "_":
                a.append(self.word())
            elif c == '"':
                a.append(self.string())
            elif c in ONE:
                a.append(self.op())
            elif c in SEP:
                a.append(T("SEP", self.go(), self.l, self.c - 1))
            else:
                raise E("недопустимый символ " + repr(c), self.l, self.c)
        a.append(T("EOF", "", self.l, self.c))
        return a

    def com(self):
        while self.see() and self.see() != "\n":
            self.go()

    def com2(self):
        l, c = self.l, self.c
        self.go()
        self.go()
        while self.see():
            if self.see() == "*" and self.see(1) == "/":
                self.go()
                self.go()
                return
            self.go()
        raise E("незакрытый комментарий", l, c)

    def op(self):
        l, c = self.l, self.c
        a = self.go()
        if self.see() and a + self.see() in TWO:
            self.go()
            return T("OP", a + self.s[self.i - 1], l, c)
        return T("OP", a, l, c)

    def word(self):
        l, c, a = self.l, self.c, self.i
        while self.see() and (self.see().isalnum() or self.see() == "_"):
            self.go()
        v = self.s[a:self.i]
        if v in KEY:
            return T("KW", v, l, c)
        return T("ID", v, l, c)

    def dig(self, d):
        k = 0
        while True:
            c = self.see()
            if c and c in d:
                self.go()
                k += 1
            elif c == "_":
                l, c2 = self.l, self.c
                if k == 0:
                    raise E("разделитель в начале числа", l, c2)
                if not self.see(1) or self.see(1) not in d:
                    raise E("после _ нужна цифра", l, c2)
                self.go()
                k = 0
            else:
                break

    def num(self):
        l, c, a = self.l, self.c, self.i
        if self.see() == "0" and self.see(1) and self.see(1) in "xXbB":
            p = self.go() + self.go()
            d = "0123456789abcdefABCDEF" if p.lower() == "0x" else "01"
            if not self.see() or self.see() not in d:
                raise E("после " + p + " нужна цифра", self.l, self.c)
            self.dig(d)
        else:
            self.dig("0123456789")
            if self.see() == "." and self.see(1).isdigit():
                self.go()
                self.dig("0123456789")
            if self.see() and self.see() in "eE":
                self.go()
                if self.see() and self.see() in "+-":
                    self.go()
                if not self.see().isdigit():
                    raise E("в экспоненте нужна цифра", self.l, self.c)
                self.dig("0123456789")
        v = self.s[a:self.i]
        if any(x in ".eE" for x in v):
            return T("FLOAT", v, l, c)
        return T("INT", v, l, c)

    def string(self):
        l, c = self.l, self.c
        self.go()
        a = []
        e = {"n": "\n", "t": "\t", '"': '"', "\\": "\\"}
        while True:
            x = self.see()
            if not x:
                raise E("строка не закрыта", l, c)
            if x == "\n":
                raise E("перевод строки в строке", self.l, self.c)
            if x == '"':
                self.go()
                return T("STR", "".join(a), l, c)
            if x == "\\":
                self.go()
                x = self.see()
                if x not in e:
                    raise E("неверная escape-последовательность", self.l, self.c)
                a.append(e[x])
                self.go()
            else:
                a.append(self.go())


def show(a):
    f = "{:>4}  {:<6}  {:<28}  {:>6}  {:>7}"
    print(f.format("N", "Тип", "Значение", "Строка", "Столбец"))
    print("-" * 62)
    for i, t in enumerate(a, 1):
        print(f.format(i, t.t, repr(t.v), t.l, t.c))


def main():
    p = sys.argv[1] if len(sys.argv) > 1 else "programm.bmstu"
    try:
        s = open(p, encoding="utf-8").read()
        a = L(s).run()
    except E as e:
        print(e)
        return 1
    show(a)
    return 0


if __name__ == "__main__":
    sys.exit(main())
