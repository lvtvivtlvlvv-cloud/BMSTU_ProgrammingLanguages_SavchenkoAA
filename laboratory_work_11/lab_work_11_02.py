import lab_work_11_01 as m

a = 0
b = 0


def run(s):
    try:
        return m.P(m.L(s).run()).run(), None
    except (m.E, m.PE) as e:
        return None, str(e)


def chk(i, x, s):
    global a, b
    if x:
        a += 1
        print("OK  ", i, s)
    else:
        b += 1
        print("FAIL", i, s)


def prg(s):
    return "программа T {\n" + s + "\n} конец"


t, e = run(prg("x : целое = 2;"))
chk(1, t and t.name == "T" and t.body[0].name == "x", "имя программы и объявление")

t, e = run(prg("x : вещ;"))
chk(2, t and t.body[0].type == "вещ" and t.body[0].e is None, "тип без значения")

t, e = run(prg("x : целое = 3;"))
chk(3, t and t.body[0].e.k == "C" and t.body[0].e.v == 3, "целое 3")

t, e = run(prg("x : целое = 0x1F;"))
chk(4, t and t.body[0].e.v == 31, "0x1F -> 31")

t, e = run(prg("x : целое = 0b1010;"))
chk(5, t and t.body[0].e.v == 10, "0b1010 -> 10")

t, e = run(prg("x : вещ = 1e-5;"))
chk(6, t and abs(t.body[0].e.v - 1e-5) < 1e-12, "1e-5")

t, e = run(prg("x = 2 + 3 * 4;"))
chk(7, t and t.body[0].e.op == "+" and t.body[0].e.r.op == "*", "приоритет * над +")

t, e = run(prg("x = 1 - 2 - 3;"))
chk(8, t and t.body[0].e.op == "-" and t.body[0].e.l.op == "-", "левая ассоциативность")

t, e = run(prg("x = (1 + 2) * 3;"))
chk(9, t and t.body[0].e.op == "*" and t.body[0].e.l.op == "+", "скобки")

t, e = run(prg("x = -y;"))
chk(10, t and t.body[0].e.k == "U" and t.body[0].e.op == "-", "унарный минус")

t, e = run(prg("x = a || b && c;"))
chk(11, t and t.body[0].e.op == "||" and t.body[0].e.r.op == "&&", "уровни или/и")

t, e = run(prg('если (x < 1) { печать("a"); } иначе { печать("b"); }'))
chk(12, t and t.body[0].k == "I" and len(t.body[0].b) == 1, "если/иначе")

t, e = run(prg("пока (x < 5) { x += 1; }"))
chk(13, t and t.body[0].k == "W" and t.body[0].a[0].op == "+=", "пока и +=")

t, e = run(prg("печать;"))
chk(14, t and t.body[0].k == "O" and t.body[0].a == [], "печать без аргументов")

t, e = run(prg("печать(x, 1);"))
chk(15, t and len(t.body[0].a) == 2, "печать с аргументами")

t, e = run(prg("возврат;"))
chk(16, t and t.body[0].k == "R" and t.body[0].e is None, "возврат без значения")

t, e = run(prg("x = 1"))
chk(17, e is not None and e.startswith("ParseError") and "ожидалось ;" in e, "нет ; -> ParseError")

t, e = run("программа T {\n  x = $;\n} конец")
chk(18, e is not None and e.startswith("LexError") and "[2:7]" in e, "$ -> LexError [2:7]")

print("итог: {}/{}".format(a, a + b))
