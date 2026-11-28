import lab_work_10_01 as m

a = [
    "x = 1_000_000;",
    "y = 0xFF_FF;",
    "z = 0b1010_0101;",
    "w = 3.14_15;",
    "q = 1e-1_0;",
    "r = 1_0.2_5e+2;",
    "_100 = 5;",
    "// 1_000\nx = 1;",
    's = "a\\nb";',
    "если (x <= 1_0) { x += 1; }",
    "1_;",
    "0x_1F;",
    "1__0;",
    'x = "abc;',
    "x = $;",
    "/* abc",
]

for i, s in enumerate(a, 1):
    print("---", i, repr(s))
    try:
        t = m.L(s).run()
        for x in t:
            print("{:<6} {:<20} {}:{}".format(x.t, repr(x.v), x.l, x.c))
    except m.E as e:
        print(e)
