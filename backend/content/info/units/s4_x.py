# -*- coding: utf-8 -*-
from dsl import P, ORD, TR, MT

EXTRAS = {}

EXTRAS['s4a'] = dict(
    matching=MT(("int", "Butun son: 5"), ("float", "Haqiqiy son: 3.14"), ("str", "Matn: \"salom\""), ("bool", "True yoki False"),
                ("input()", "Foydalanuvchi kiritgan matnni (str) qaytaradi"), ("//", "Butun bo'lish: 7 // 2 = 3")),
    problems=[
        P("17 % 5 nechaga teng?", "2", "", "17 = 5·3 + 2"),
        P("2 ** 10 nechaga teng?", "1024", "", "1024"),
        P("7 // 2 nechaga teng?", "3", "", "3"),
        P("type(3.14) qaysi turni qaytaradi? (float / int / str)", "float", "", "float")],
    code_trace=[
        TR("x = 7\ny = 2\nprint(x // y, x % y, x ** y)", "Dastur nimani chiqaradi?", "3 1 49", "7//2 = 3; 7%2 = 1; 7**2 = 49"),
        TR('print("ha" * 3)', "Dastur nimani chiqaradi?", "hahaha", ""),
        TR('a = "5"\nprint(a + a)', "Dastur nimani chiqaradi?", "55", "Satrlar birlashadi."),
        TR('print(int("5") + int("5"))', "Dastur nimani chiqaradi?", "10", "")],
    sentence_practice=[ORD("Ismni so'rab, yoshini 1 ga oshirib chiqaruvchi kodni tartiblang", ["ism = input('Ismingiz: ')", "yosh = int(input('Yoshingiz: '))", "yosh = yosh + 1", "print(ism, yosh)"], mono=True)],
)

EXTRAS['s4b'] = dict(
    matching=MT(("if", "Shart chin bo'lsa blokni bajaradi"), ("elif", "Qo'shimcha shart (else if)"), ("else", "Hech bir shart chin bo'lmaganda"),
                ("==", "Tenglikni tekshirish"), ("and", "Ikkala shart ham chin bo'lishi"), ("in", "A'zolikni tekshirish")),
    problems=[
        P("x = 5 da x > 3 and x < 10 ifodaning qiymati (True/False)?", "True", "", "True"),
        P("\"a\" in \"salom\" ifodaning qiymati (True/False)?", "True", "", "True"),
        P("0 shartda qanday hisoblanadi (True/False)?", "False", "", "False"),
        P("2000-yil kabisa yilmi? (ha/yo'q — 'ha' deb yozing)", "ha", "(y%4==0 and y%100!=0) or y%400==0", "Ha")],
    code_trace=[
        TR('x = 15\nif x % 3 == 0 and x % 5 == 0:\n    print("FizzBuzz")\nelif x % 3 == 0:\n    print("Fizz")', "Dastur nimani chiqaradi?", "FizzBuzz", "15 ham 3 ga, ham 5 ga bo'linadi."),
        TR("ball = 72\nif ball >= 86:\n    print(5)\nelif ball >= 71:\n    print(4)\nelse:\n    print(3)", "Dastur nimani chiqaradi?", "4", "86 dan kichik, 71 dan katta."),
        TR('print("juft" if 8 % 2 == 0 else "toq")', "Dastur nimani chiqaradi?", "juft", "Ternar ifoda.")],
    sentence_practice=[ORD("Sonning musbat/manfiy/nol ekanini aniqlash kodini tartiblang", ["x = int(input())", "if x > 0:", "print('musbat')", "elif x < 0:", "print('manfiy')", "else:", "print('nol')"], mono=True)],
)

EXTRAS['s4c'] = dict(
    matching=MT(("for", "Ketma-ketlik bo'ylab takrorlash"), ("while", "Shart chin bo'lguncha takrorlash"), ("break", "Siklni darhol to'xtatadi"),
                ("continue", "Joriy iteratsiyani o'tkazib yuboradi"), ("range(1, 5)", "1, 2, 3, 4"), ("List comprehension", "[i*i for i in range(4)]")),
    problems=[
        P("sum(range(1, 101)) nechaga teng?", "5050", "", "5050"),
        P("range(10, 0, -3) nechta son beradi?", "4", "10, 7, 4, 1", "4"),
        P("5 ning faktoriali sikl bilan hisoblansa natija?", "120", "", "120"),
        P("len(range(2, 11)) nechaga teng?", "9", "2..10", "9")],
    code_trace=[
        TR("for i in range(1, 4):\n    print(i * i)", "Dastur nimani chiqaradi?", "1\n4\n9", "", lines=3),
        TR("s = 0\nfor i in range(5):\n    if i % 2 == 0:\n        continue\n    s += i\nprint(s)", "Dastur nimani chiqaradi?", "4", "Faqat toq i: 1 + 3 = 4"),
        TR("n = 12345\ns = 0\nwhile n > 0:\n    s += n % 10\n    n //= 10\nprint(s)", "Dastur nimani chiqaradi?", "15", "Raqamlar yig'indisi 1+2+3+4+5"),
        TR("print([i * i for i in range(4)])", "Dastur nimani chiqaradi?", "[0, 1, 4, 9]", "")],
    sentence_practice=[ORD("1 dan 10 gacha juft sonlar yig'indisi kodini tartiblang", ["s = 0", "for i in range(1, 11):", "if i % 2 == 0:", "s += i", "print(s)"], mono=True)],
)

EXTRAS['s4d'] = dict(
    matching=MT(("def", "Funksiya e'lon qilish"), ("return", "Qiymat qaytarib funksiyani tugatadi"), ("Parametr", "Funksiya e'londagi nom"),
                ("Argument", "Chaqiruvdagi qiymat"), ("Rekursiya", "Funksiyaning o'zini chaqirishi"), ("import", "Modulni ulash")),
    problems=[
        P("def f(a, b=2): return a + b bo'lsa, f(3) nechaga teng?", "5", "", "3 + 2"),
        P("abs(-7) nechaga teng?", "7", "", "7"),
        P("fakt(5) (fakt(n) = n·fakt(n−1)) nechaga teng?", "120", "", "120"),
        P("round(3.6) nechaga teng?", "4", "", "4")],
    code_trace=[
        TR("def f(x, y=2):\n    return x * y\nprint(f(3), f(3, 4))", "Dastur nimani chiqaradi?", "6 12", ""),
        TR("def fakt(n):\n    return 1 if n <= 1 else n * fakt(n - 1)\nprint(fakt(5))", "Dastur nimani chiqaradi?", "120", ""),
        TR("x = 10\ndef g():\n    x = 5\n    return x\ng()\nprint(x)", "Dastur nimani chiqaradi?", "10", "Funksiya ichidagi x — lokal o'zgaruvchi."),
        TR("import math\nprint(math.sqrt(16))", "Dastur nimani chiqaradi?", "4.0", "sqrt float qaytaradi.")],
    sentence_practice=[ORD("kvadrat funksiyasini e'lon qilib chaqirish kodini tartiblang", ["def kvadrat(x):", "return x * x", "print(kvadrat(5))"], mono=True)],
)

EXTRAS['s4e'] = dict(
    matching=MT(("list", "O'zgaruvchan tartiblangan ro'yxat"), ("tuple", "O'zgarmas ketma-ketlik"), ("dict", "Kalit:qiymat juftliklari"),
                ("set", "Takrorlanmaydigan elementlar"), ("a[::-1]", "Ro'yxatni teskari qiladi"), ("split()", "Satrni ro'yxatga ajratadi")),
    problems=[
        P("len([5, 6, 7]) nechaga teng?", "3", "", "3"),
        P("\"salom\"[1:3] nima beradi? (2 harf)", "al", "", "al"),
        P("[1, 2] + [3] ro'yxatida nechta element bor?", "3", "", "3"),
        P("{\"a\": 1, \"b\": 2} lug'atida nechta kalit bor?", "2", "", "2")],
    code_trace=[
        TR("a = [1, 2, 3]\na.append(4)\nprint(a[-1], len(a))", "Dastur nimani chiqaradi?", "4 4", ""),
        TR('s = "salom"\nprint(s.upper()[1:3])', "Dastur nimani chiqaradi?", "AL", "upper() → SALOM; [1:3] → AL"),
        TR('d = {"a": 1, "b": 2}\nprint(sum(d.values()))', "Dastur nimani chiqaradi?", "3", ""),
        TR("t = (1, 2, 3)\nprint(t[::-1])", "Dastur nimani chiqaradi?", "(3, 2, 1)", "")],
    sentence_practice=[ORD("Ro'yxatdagi sonlar o'rtachasini topuvchi kodni tartiblang", ["sonlar = [4, 8, 6]", "yigindi = sum(sonlar)", "o_rta = yigindi / len(sonlar)", "print(o_rta)"], mono=True)],
)

EXTRAS['s4f'] = dict(
    matching=MT(("with open(...)", "Faylni avtomatik yopadi"), ("try / except", "Xatoni ushlash"), ("finally", "Har doim bajariladi"),
                ("class", "Obyektlar shabloni"), ("__init__", "Konstruktor"), ("Meros", "Sinf boshqasidan xususiyat oladi")),
    problems=[
        P("1 / 0 qanday xatoni beradi? (xato nomi)", "ZeroDivisionError", "", "ZeroDivisionError"),
        P("int('abc') qanday xatoni beradi?", "ValueError", "", "ValueError"),
        P("Faylga oxiridan qo'shish rejimi harfi?", "a", "", "\"a\" (append)"),
        P("OYD ning 4 asosiy tamoyilidan biri: ... (inkapsulyatsiya, meros, polimorfizm, abstraksiya) — nechta tamoyil?", "4", "", "4")],
    code_trace=[
        TR('try:\n    print(10 / 0)\nexcept ZeroDivisionError:\n    print("xato")', "Dastur nimani chiqaradi?", "xato", ""),
        TR('try:\n    int("abc")\nexcept ValueError:\n    print("ValueError")\nfinally:\n    print("tamom")', "Dastur nimani chiqaradi?", "ValueError\ntamom", "finally har doim ishlaydi.", lines=2),
        TR("class A:\n    def __init__(self, n):\n        self.n = n\na = A(3)\nprint(a.n * 2)", "Dastur nimani chiqaradi?", "6", "")],
    sentence_practice=[ORD("Faylga yozish kodini tartiblang", ["with open('a.txt', 'w') as f:", "f.write('salom')", "print('tayyor')"], mono=True)],
)
