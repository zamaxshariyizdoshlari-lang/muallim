# -*- coding: utf-8 -*-
from dsl import P, ORD, TR, MT

EXTRAS = {}

EXTRAS['s3a'] = dict(
    matching=MT(("AND (∧)", "Ikkalasi chin bo'lsagina chin"), ("OR (∨)", "Kamida bittasi chin bo'lsa chin"),
                ("NOT (¬)", "Qiymatni teskarisiga o'zgartiradi"), ("XOR", "Qiymatlar farq qilsa chin"),
                ("De Morgan", "¬(A∧B) = ¬A ∨ ¬B"), ("Chinlik jadvali", "Barcha kirishlar uchun natijalar jadvali")),
    problems=[
        P("(1 AND 0) OR 1 ifodaning qiymati?", "1", "Avval AND.", "0 OR 1 = 1"),
        P("NOT (1 OR 0) ifodaning qiymati?", "0", "Avval qavs.", "NOT 1 = 0"),
        P("4 ta o'zgaruvchili chinlik jadvalida nechta satr bor?", "16", "2ⁿ", "2⁴ = 16", unit="satr"),
        P("1 XOR 1 nechaga teng?", "0", "", "0"),
        P("A = 1, B = 0 da (A OR B) AND NOT B ning qiymati?", "1", "", "(1) AND 1 = 1")],
    code_trace=[
        TR("print(True and False or True)", "Dastur nimani chiqaradi?", "True", "and or dan ustun: (True and False) or True = True."),
        TR("print(not (1 > 2))", "Dastur nimani chiqaradi?", "True", "1 > 2 — False; not False = True."),
        TR("print(5 > 3 and 2 > 4)", "Dastur nimani chiqaradi?", "False", "Ikkinchi shart yolg'on.")],
    sentence_practice=[ORD("¬(A ∧ B) ning chinlik jadvalini tuzish tartibi", ["A va B ning barcha kombinatsiyalarini yozing (4 satr)", "A ∧ B ustunini hisoblang", "Uning inkorini oling", "De Morgan bilan ¬A ∨ ¬B ga tenglashtiring"])],
)

EXTRAS['s3b'] = dict(
    matching=MT(("Diskretlik", "Jarayon alohida qadamlarga bo'linadi"), ("Aniqlik", "Har bir qadam ravshan va bir ma'noli"),
                ("Chekliklik", "Chekli qadamdan so'ng natija beradi"), ("Ommaviylik", "Bir turdagi barcha masalalar uchun yaroqli"),
                ("Ijrochi", "Algoritm buyruqlarini bajaruvchi"), ("Blok-sxema", "Algoritmning grafik tasviri")),
    problems=[
        P("Algoritm so'zi qaysi buyuk olim nomidan kelib chiqqan? (familiyasi)", ["xorazmiy", "al-xorazmiy", "al xorazmiy"], "", "Al-Xorazmiy"),
        P("Algoritmning nechta asosiy xossasi sanaladi (diskretlik, aniqlik, chekliklik, ommaviylik, tushunarlilik)?", "5", "", "5 ta"),
        P("Qaysi xossa bo'yicha algoritm chekli qadamdan keyin to'xtashi kerak? (bir so'z)", "chekliklik", "", "Chekliklik")],
    code_trace=[
        TR("for i in range(3):\n    print(i * 2)", "Dastur nimani chiqaradi?", "0\n2\n4", "i = 0, 1, 2", lines=3),
        TR("s = 0\nfor i in range(1, 5):\n    s += i\nprint(s)", "Dastur nimani chiqaradi?", "10", "1 + 2 + 3 + 4 = 10")],
    sentence_practice=[ORD("Choy damlash algoritmi (to'g'ri tartib)", ["Suvni qaynating", "Choynakka quruq choy soling", "Qaynoq suv quying", "5 daqiqa damlang", "Piyolaga quying"])],
)

EXTRAS['s3c'] = dict(
    matching=MT(("Oval", "Boshlanish/tugash bloki"), ("Parallelogramm", "Kiritish/chiqarish bloki"), ("To'g'ri to'rtburchak", "Hisoblash bloki"),
                ("Romb", "Shart tekshirish bloki"), ("while", "Shart chin bo'lguncha takrorlash"), ("for", "Takrorlar soni ma'lum sikl")),
    problems=[
        P("1 dan 10 gacha sonlar yig'indisini hisoblovchi siklda natija?", "55", "", "55"),
        P("EKUB(48; 36) ni Evklid algoritmi bilan toping.", "12", "48 mod 36 = 12", "(48,36)→(36,12)→(12,0): 12"),
        P("5! (faktorial) nechaga teng?", "120", "", "120"),
        P("Fibonachchi ketma-ketligi: 1, 1, 2, 3, 5, 8, ... 7-hadi?", "13", "8 + 5", "13")],
    code_trace=[
        TR('n = 7\nif n % 2 == 0:\n    print("juft")\nelse:\n    print("toq")', "Dastur nimani chiqaradi?", "toq", "7 % 2 = 1 ≠ 0", lines=1),
        TR("i = 1\nwhile i < 20:\n    i *= 2\nprint(i)", "Dastur nimani chiqaradi?", "32", "1→2→4→8→16→32; 32 < 20 yolg'on."),
        TR("a, b = 0, 1\nfor _ in range(5):\n    a, b = b, a + b\nprint(a)", "Dastur nimani chiqaradi?", "5", "a: 0→1→1→2→3→5")],
    sentence_practice=[ORD("Ikki sonning kattasini topish (blok-sxema tartibi)", ["Boshlash", "a va b ni kiritish", "a > b shartini tekshirish", "Kattasini chiqarish", "Tugatish"]),
                       ORD("Yig'indini hisoblash kodini tartiblang", ["s = 0", "for i in range(1, 11):", "s += i", "print(s)"], mono=True)],
)

EXTRAS['s3d'] = dict(
    matching=MT(("Chiziqli qidiruv", "O(n), massiv tartiblangan bo'lishi shart emas"), ("Ikkilik qidiruv", "O(log n), tartiblangan massivda"),
                ("Pufakchali saralash", "Qo'shnilarni taqqoslab almashtiradi, O(n²)"), ("Tezkor saralash", "Pivot orqali bo'ladi, o'rtacha O(n log n)"),
                ("Merge sort", "Bo'lib, saralab birlashtiradi, doim O(n log n)"), ("O-notatsiya", "Amallar sonining o'sish tartibi")),
    problems=[
        P("1000 elementli tartiblangan massivda ikkilik qidiruv ko'pi bilan nechta taqqoslash talab qiladi?", "10", "2¹⁰ = 1024", "10"),
        P("16 elementli tartiblangan massivda ikkilik qidiruv ko'pi bilan nechta qadam talab qiladi?", "4", "log₂ 16", "4"),
        P("[3, 1, 2] da pufakchali saralashning birinchi o'tishidan keyin oxirgi element?", "3", "Eng katta oxiriga suriladi.", "3"),
        P("n = 100 da O(n²) algoritm taxminan necha amal bajaradi?", "10000", "", "100² = 10 000", unit="amal")],
    code_trace=[
        TR("a = [5, 2, 9]\na.sort()\nprint(a)", "Dastur nimani chiqaradi?", "[2, 5, 9]", ""),
        TR("print(sorted([3, 1, 2], reverse=True))", "Dastur nimani chiqaradi?", "[3, 2, 1]", "reverse=True — kamayish tartibi."),
        TR("a = [1, 3, 5, 7, 9]\nlo, hi = 0, 4\nmid = (lo + hi) // 2\nprint(a[mid])", "Dastur nimani chiqaradi?", "5", "mid = 2 → a[2] = 5")],
    sentence_practice=[ORD("Ikkilik qidiruv kodini tartiblang", ["lo, hi = 0, len(a) - 1", "while lo <= hi:", "mid = (lo + hi) // 2", "if a[mid] == x: return mid", "elif a[mid] < x: lo = mid + 1", "else: hi = mid - 1"], mono=True)],
)

EXTRAS['s3e'] = dict(
    matching=MT(("Stek", "LIFO: oxirgi kirgan birinchi chiqadi"), ("Navbat", "FIFO: birinchi kirgan birinchi chiqadi"),
                ("Daraxt", "Ildiz va shoxlardan iborat ierarxiya"), ("Graf", "Tugunlar va qirralar to'plami"),
                ("Lug'at (dict)", "Kalit–qiymat juftliklari"), ("Hash jadval", "Kalitni indeksga aylantirib tez qidiradi")),
    problems=[
        P("Stekka 1, 2, 3 ketma-ket qo'shildi (push). Bitta pop() nimani qaytaradi?", "3", "LIFO", "3"),
        P("Navbatga 1, 2, 3 ketma-ket qo'shildi. Bitta dequeue() nimani qaytaradi?", "1", "FIFO", "1"),
        P("Hash jadvalda o'rtacha qidiruv murakkabligi O(?). Sonni yozing: O(1)", ["1", "o(1)"], "", "O(1)"),
        P("Daraxtning eng yuqori tuguni nima deyiladi? (bir so'z)", "ildiz", "", "Ildiz (root)")],
    code_trace=[
        TR("s = []\ns.append(1)\ns.append(2)\nprint(s.pop())", "Dastur nimani chiqaradi?", "2", "Stek: oxirgi element chiqadi."),
        TR('d = {"a": 1}\nprint(d.get("b", 0))', "Dastur nimani chiqaradi?", "0", "Kalit yo'q — standart qiymat 0."),
        TR("print(len({1, 2, 2, 3}))", "Dastur nimani chiqaradi?", "3", "To'plamda takror elementlar bo'lmaydi.")],
    sentence_practice=[ORD("Stek bilan ishlash kodini tartiblang", ["stek = []", "stek.append(10)", "stek.append(20)", "print(stek.pop())"], mono=True)],
)
