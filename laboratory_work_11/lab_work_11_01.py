import sys

KEY = {"программа", "если", "иначе", "пока", "печать", "возврат",
       "целое", "цел", "вещ", "вещественное", "строка"}
ONE = set("+-*/%=<>!&|")
SEP = set("(){}[],;.:")
TWO = {"==", "!=", "<=", ">=", "+=", "-=", "&&", "||", "++"}
TYP = ("целое", "цел", "вещ", "вещественное", "строка")


class E(Exception):
    def __init__(self, s, l, c):
        self.s = s
        self.l = l
        self.c = c

    def __str__(self):
        return "LexError [{}:{}]: {}".format(self.l, self.c, self.s)


class PE(Exception):
    def __init__(self, s, t):
        self.s = s
        self.t = t

    def __str__(self):
        return "ParseError [{}:{}]: {}".format(self.t.l, self.t.c, self.s)


class T:
    def __init__(self, t, v, l, c):
        self.t = t
        self.v = v
        self.l = l
        self.c = c


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
                while self.see() and self.see() != "\n":
                    self.go()
            elif c == "/" and self.see(1) == "*":
                l, c2 = self.l, self.c
                self.go()
                self.go()
                while self.see():
                    if self.see() == "*" and self.see(1) == "/":
                        self.go()
                        self.go()
                        break
                    self.go()
                else:
                    raise E("незакрытый комментарий", l, c2)
            elif c.isdigit() or (c == "." and self.see(1).isdigit()):
                a.append(self.num())
            elif c.isalpha() or c == "_":
                a.append(self.word())
            elif c == '"':
                a.append(self.string())
            elif c in ONE:
                l, c2 = self.l, self.c
                x = self.go()
                if self.see() and x + self.see() in TWO:
                    x += self.go()
                    a.append(T("OP", x, l, c2))
                else:
                    a.append(T("OP", x, l, c2))
            elif c in SEP:
                l, c2 = self.l, self.c
                a.append(T("SEP", self.go(), l, c2))
            else:
                raise E("недопустимый символ " + repr(c), self.l, self.c)
        a.append(T("EOF", "", self.l, self.c))
        return a

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


class N:
    def __init__(self, k, **a):
        self.k = k
        for x in a:
            setattr(self, x, a[x])


class P:
    def __init__(self, a):
        self.a = a
        self.i = 0

    def look(self, n=0):
        j = self.i + n
        if j < len(self.a):
            return self.a[j]
        return self.a[-1]

    def next(self):
        t = self.a[self.i]
        if t.t != "EOF":
            self.i += 1
        return t

    def is_(self, t, v=None):
        x = self.a[self.i]
        if x.t != t:
            return False
        if v is not None and x.v != v:
            return False
        return True

    def ok(self, t, v=None):
        if self.is_(t, v):
            return self.next()
        return None

    def need(self, t, v=None):
        if not self.is_(t, v):
            raise PE("ожидалось " + (v if v else t), self.a[self.i])
        return self.next()

    def run(self):
        self.need("KW", "программа")
        a = self.need("ID").v
        self.need("SEP", "{")
        b = []
        while not self.is_("SEP", "}") and not self.is_("EOF"):
            b.append(self.stmt())
        self.need("SEP", "}")
        x = self.a[self.i]
        if x.v != "конец":
            raise PE("ожидалось конец", x)
        self.next()
        return N("P", name=a, body=b)

    def stmt(self):
        t = self.a[self.i]
        if t.t == "KW":
            if t.v == "если":
                return self.if_()
            if t.v == "пока":
                return self.while_()
            if t.v == "печать":
                return self.print_()
            if t.v == "возврат":
                return self.ret()
        if t.t == "SEP" and t.v == "{":
            return self.block()
        if t.t == "ID":
            if self.look(1).v == ":":
                return self.decl()
            return self.assign()
        raise PE("ожидался оператор", t)

    def decl(self):
        a = self.need("ID").v
        self.need("SEP", ":")
        t = self.a[self.i]
        if t.t != "KW" or t.v not in TYP:
            raise PE("ожидался тип", t)
        self.next()
        e = None
        if self.ok("OP", "="):
            e = self.expr()
        self.need("SEP", ";")
        return N("D", name=a, type=t.v, e=e)

    def assign(self):
        a = self.need("ID").v
        o = self.a[self.i]
        if o.t != "OP" or o.v not in ("=", "+=", "-="):
            raise PE("ожидался =, += или -=", o)
        self.next()
        e = self.expr()
        self.need("SEP", ";")
        return N("A", name=a, op=o.v, e=e)

    def if_(self):
        self.need("KW", "если")
        c = self.expr()
        self.need("SEP", "{")
        a = []
        while not self.is_("SEP", "}") and not self.is_("EOF"):
            a.append(self.stmt())
        self.need("SEP", "}")
        b = []
        if self.ok("KW", "иначе"):
            self.need("SEP", "{")
            while not self.is_("SEP", "}") and not self.is_("EOF"):
                b.append(self.stmt())
            self.need("SEP", "}")
        return N("I", c=c, a=a, b=b)

    def while_(self):
        self.need("KW", "пока")
        c = self.expr()
        self.need("SEP", "{")
        a = []
        while not self.is_("SEP", "}") and not self.is_("EOF"):
            a.append(self.stmt())
        self.need("SEP", "}")
        return N("W", c=c, a=a)

    def print_(self):
        self.need("KW", "печать")
        a = []
        if self.ok("SEP", "("):
            a.append(self.expr())
            while self.ok("SEP", ","):
                a.append(self.expr())
            self.need("SEP", ")")
        self.need("SEP", ";")
        return N("O", a=a)

    def ret(self):
        self.need("KW", "возврат")
        e = None
        if not self.is_("SEP", ";"):
            e = self.expr()
        self.need("SEP", ";")
        return N("R", e=e)

    def block(self):
        self.need("SEP", "{")
        a = []
        while not self.is_("SEP", "}") and not self.is_("EOF"):
            a.append(self.stmt())
        self.need("SEP", "}")
        return N("B", a=a)

    def expr(self):
        return self.or_()

    def or_(self):
        a = self.and_()
        while self.ok("OP", "||"):
            a = N("E", op="||", l=a, r=self.and_())
        return a

    def and_(self):
        a = self.cmp_()
        while self.ok("OP", "&&"):
            a = N("E", op="&&", l=a, r=self.cmp_())
        return a

    def cmp_(self):
        a = self.add()
        while (self.a[self.i].t == "OP"
               and self.a[self.i].v in ("==", "!=", "<", ">", "<=", ">=")):
            o = self.next().v
            a = N("E", op=o, l=a, r=self.add())
        return a

    def add(self):
        a = self.mul()
        while self.a[self.i].t == "OP" and self.a[self.i].v in ("+", "-"):
            o = self.next().v
            a = N("E", op=o, l=a, r=self.mul())
        return a

    def mul(self):
        a = self.un()
        while self.a[self.i].t == "OP" and self.a[self.i].v in ("*", "/", "%"):
            o = self.next().v
            a = N("E", op=o, l=a, r=self.un())
        return a

    def un(self):
        t = self.a[self.i]
        if t.t == "OP" and t.v in ("!", "-", "+"):
            self.next()
            return N("U", op=t.v, x=self.un())
        return self.prim()

    def prim(self):
        t = self.a[self.i]
        if t.t == "INT":
            self.next()
            v = t.v.replace("_", "")
            if v.lower().startswith("0x"):
                return N("C", v=int(v, 16))
            if v.lower().startswith("0b"):
                return N("C", v=int(v, 2))
            return N("C", v=int(v, 10))
        if t.t == "FLOAT":
            self.next()
            return N("C", v=float(t.v.replace("_", "")))
        if t.t == "STR":
            self.next()
            return N("S", v=t.v)
        if t.t == "ID":
            self.next()
            return N("V", name=t.v)
        if t.t == "SEP" and t.v == "(":
            self.next()
            a = self.expr()
            self.need("SEP", ")")
            return a
        raise PE("ожидалось выражение", t)


def dump(n, d=0):
    p = "   " * d
    k = n.k
    if k == "C":
        print(p + "C[" + str(n.v) + "]")
    elif k == "S":
        print(p + "S[" + n.v + "]")
    elif k == "V":
        print(p + "V[" + n.name + "]")
    elif k == "E":
        print(p + "E[" + n.op + "]")
        dump(n.l, d + 1)
        dump(n.r, d + 1)
    elif k == "U":
        print(p + "U[" + n.op + "]")
        dump(n.x, d + 1)
    elif k == "P":
        print(p + "P[" + n.name + "]")
        for x in n.body:
            dump(x, d + 1)
    elif k == "D":
        print(p + "D[" + n.name + ":" + n.type + "]")
        if n.e:
            dump(n.e, d + 1)
    elif k == "A":
        print(p + "A[" + n.name + n.op + "]")
        dump(n.e, d + 1)
    elif k == "I":
        print(p + "I")
        dump(n.c, d + 1)
        for x in n.a:
            dump(x, d + 1)
        for x in n.b:
            dump(x, d + 1)
    elif k == "W":
        print(p + "W")
        dump(n.c, d + 1)
        for x in n.a:
            dump(x, d + 1)
    elif k == "O":
        print(p + "O")
        for x in n.a:
            dump(x, d + 1)
    elif k == "R":
        print(p + "R")
        if n.e:
            dump(n.e, d + 1)
    elif k == "B":
        print(p + "B")
        for x in n.a:
            dump(x, d + 1)


def main():
    p = sys.argv[1] if len(sys.argv) > 1 else "example.src"
    try:
        s = open(p, encoding="utf-8").read()
        a = L(s).run()
        n = P(a).run()
    except (E, PE) as e:
        print(e)
        return 1
    dump(n)
    return 0


if __name__ == "__main__":
    sys.exit(main())
