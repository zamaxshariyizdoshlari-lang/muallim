# -*- coding: utf-8 -*-
from dsl import F, W, P, ORD

EXTRAS = {}

EXTRAS['m2a'] = dict(
    formulas=[F("Yig'indi kvadrati", "(a + b)² = a² + 2ab + b²", "101² = (100 + 1)² = 10 201"),
              F("Ayirma kvadrati", "(a − b)² = a² − 2ab + b²", ""),
              F("Kvadratlar ayirmasi", "a² − b² = (a − b)(a + b)", "99·101 = 100² − 1"),
              F("Kublar", "a³ ± b³ = (a ± b)(a² ∓ ab + b²)", "")],
    worked_examples=[
        W("Soddalashtiring: (x + 3)² − (x − 3)²", ["(x + 3)² = x² + 6x + 9", "(x − 3)² = x² − 6x + 9", "Ayiramiz: (x² + 6x + 9) − (x² − 6x + 9)", "= 12x"], "12x"),
        W("Qisqa ko'paytirish bilan hisoblang: 52²", ["52 = 50 + 2", "(50 + 2)² = 50² + 2·50·2 + 2²", "= 2500 + 200 + 4", "= 2704"], "2704")],
    problems=[
        P("99 · 101 ni qisqa ko'paytirish formulasi bilan hisoblang.", "9999", "(100 − 1)(100 + 1)", "100² − 1 = 9999"),
        P("a + b = 7 va ab = 10 bo'lsa, a² + b² nechaga teng?", "29", "(a+b)² = a² + 2ab + b²", "49 − 20 = 29"),
        P("x = 2 da 3x² − 5x + 1 ifodaning qiymatini toping.", "3", "", "3·4 − 10 + 1 = 3"),
        P("(2x + 1)² yoyilmasida x oldidagi koeffitsient nechaga teng?", "4", "2·(2x)·1", "4x² + 4x + 1 → 4"),
        P("a − b = 3 va ab = 4 bo'lsa, a² + b² nechaga teng?", "17", "(a−b)² = a² − 2ab + b²", "9 + 8 = 17"),
        P("(x − 5)² yoyilmasidagi ozod had nechaga teng?", "25", "", "x² − 10x + 25")],
    sentence_practice=[ORD("(x + 3)² − (x − 3)² ni soddalashtirish tartibi", ["(x + 3)² = x² + 6x + 9", "(x − 3)² = x² − 6x + 9", "(x² + 6x + 9) − (x² − 6x + 9)", "= 12x"])],
)

EXTRAS['m2b'] = dict(
    formulas=[F("Umumiy ko'paytuvchi", "ab + ac = a(b + c)", "6x² + 9x = 3x(2x + 3)"),
              F("Guruhlash", "ax + ay + bx + by = (a + b)(x + y)", ""),
              F("Kvadrat uchhad", "ax² + bx + c = a(x − x₁)(x − x₂)", "Viyet: x₁ + x₂ = −b/a, x₁x₂ = c/a"),
              F("Bezu teoremasi", "P(x) : (x − a) qoldig'i = P(a)", "P(a) = 0 ⇒ (x − a) ko'paytuvchi")],
    worked_examples=[
        W("x² − 5x + 6 ni ko'paytuvchilarga ajrating", ["Viyet: yig'indi 5, ko'paytma 6", "Sonlar 2 va 3 (2 + 3 = 5; 2·3 = 6)", "x² − 5x + 6 = (x − 2)(x − 3)", "Tekshirish: (x−2)(x−3) = x² − 5x + 6 ✓"], "(x − 2)(x − 3)"),
        W("x³ − 2x² + 3x − 6 ni guruhlab ajrating", ["(x³ − 2x²) + (3x − 6)", "x²(x − 2) + 3(x − 2)", "(x − 2)(x² + 3)"], "(x − 2)(x² + 3)")],
    problems=[
        P("x² − 7x + 10 = 0 tenglama ildizlarining yig'indisi nechaga teng?", "7", "Viyet teoremasi", "x₁ + x₂ = 7 (ildizlar 2 va 5)"),
        P("x² − 16 = (x − 4)(…) — ikkinchi qavs ichini yozing.", "x+4", "Kvadratlar ayirmasi.", "(x − 4)(x + 4)"),
        P("a = 2, b = 3, x = 1, y = 4 da ax + ay + bx + by ning qiymati?", "25", "(a + b)(x + y)", "5 · 5 = 25"),
        P("x³ − 6x² + 11x − 6 ning ildizlari ko'paytmasi nechaga teng?", "6", "Ildizlari 1, 2, 3.", "1·2·3 = 6"),
        P("x² + bx + 12 uchhadning ildizlari 3 va 4 bo'lsa, b nechaga teng?", "-7", "Ildizlar yig'indisi = −b", "3 + 4 = −b ⇒ b = −7"),
        P("P(x) = x³ − 2x² + x − 2 uchun P(3) ni toping.", "10", "", "27 − 18 + 3 − 2 = 10")],
    sentence_practice=[ORD("x² − 5x + 6 ni ajratish tartibi", ["Viyet: x₁ + x₂ = 5, x₁·x₂ = 6", "Ildizlar: 2 va 3", "x² − 5x + 6 = (x − 2)(x − 3)", "Qavslarni ochib tekshiramiz"])],
)

EXTRAS['m2c'] = dict(
    formulas=[F("Chiziqli tenglama", "ax + b = 0 ⇒ x = −b/a", "a ≠ 0"),
              F("Modulli tenglama", "|f| = a ⇒ f = a yoki f = −a", "a > 0"),
              F("Harakat", "s = v · t", "v = s/t; t = s/v"),
              F("Birga ishlash", "t = 1 / (1/t₁ + 1/t₂)", "6 va 3 kun → 2 kun")],
    worked_examples=[
        W("2(x − 3) + 4 = 3x − 1 ni yeching", ["Qavsni ochamiz: 2x − 6 + 4 = 3x − 1", "Ixchamlaymiz: 2x − 2 = 3x − 1", "Noma'lumlarni chapga: 2x − 3x = −1 + 2", "−x = 1 ⇒ x = −1"], "x = −1"),
        W("Ikki son yig'indisi 50, biri ikkinchisidan 8 ta ko'p. Sonlarni toping.", ["Kichigi x, kattasi x + 8", "x + (x + 8) = 50", "2x = 42 ⇒ x = 21", "Katta son: 29"], "21 va 29")],
    problems=[
        P("3x − 5 = 7 tenglamani yeching.", "4", "", "3x = 12; x = 4"),
        P("(x + 2)/3 + (x − 2)/2 = 3 tenglamani yeching.", "4", "6 ga ko'paytiring.", "2(x+2) + 3(x−2) = 18 → 5x = 20 → x = 4"),
        P("|2x − 1| = 5 ning ildizlarini yozing (; bilan ajrating).", "3; -2", "2x − 1 = 5 yoki 2x − 1 = −5", "x = 3 yoki x = −2", fmt="3; -2"),
        P("Avtomobil 60 km/soat tezlikda 270 km yo'lni necha soatda bosib o'tadi?", "4,5", "t = s/v", "270 : 60 = 4,5", unit="soat"),
        P("Ota o'g'lidan 30 yosh katta. 5 yildan keyin otasi o'g'lidan 3 marta katta bo'ladi. O'g'li hozir necha yoshda?", "10", "x + 35 = 3(x + 5)", "x + 35 = 3x + 15 → x = 10", unit="yosh"),
        P("Bir ishchi ishni 6 kunda, ikkinchisi 3 kunda bajaradi. Birga necha kunda bajaradi?", "2", "1/6 + 1/3", "1/6 + 2/6 = 1/2 kunlik ish → 2 kun", unit="kun")],
    sentence_practice=[ORD("2(x − 3) + 4 = 3x − 1 ni yechish tartibi", ["2x − 6 + 4 = 3x − 1", "2x − 2 = 3x − 1", "2x − 3x = −1 + 2", "−x = 1 ⇒ x = −1"])],
)

EXTRAS['m2d'] = dict(
    formulas=[F("Belgi qoidasi", "manfiy songa ko'paytirsak: < ↔ >", "−2x > 6 ⇒ x < −3"),
              F("Modul < a", "|x| < a ⇔ −a < x < a", ""),
              F("Modul > a", "|x| > a ⇔ x < −a yoki x > a", ""),
              F("Oraliqlar", "(a; b) interval, [a; b] kesma", "∞ ga doim yumaloq qavs")],
    worked_examples=[
        W("2 − 3x ≥ 8 ni yeching", ["−3x ≥ 8 − 2 = 6", "Manfiy songa bo'lamiz — belgi o'zgaradi", "x ≤ −2", "Javob: (−∞; −2]"], "x ≤ −2"),
        W("|x − 3| < 2 ni yeching", ["−2 < x − 3 < 2", "Hamma qismga 3 ni qo'shamiz", "1 < x < 5", "Javob: (1; 5)"], "(1; 5)")],
    problems=[
        P("2x + 1 ≥ 5 tengsizlikning eng kichik butun yechimi nechaga teng?", "2", "2x ≥ 4", "x ≥ 2 ⇒ eng kichik butun: 2"),
        P("−2x > 6 tengsizlikni yeching: x < ? (sonni yozing)", "-3", "Manfiy songa bo'lganda belgi o'zgaradi.", "x < −3"),
        P("1 < x ≤ 5 oraliqdagi butun sonlar nechta?", "4", "", "2, 3, 4, 5 — 4 ta"),
        P("|x| < 3 tengsizlikning butun yechimlari nechta?", "5", "−3 < x < 3", "−2, −1, 0, 1, 2 — 5 ta"),
        P("3x − 1 < 8 tengsizlikning eng katta butun yechimi nechaga teng?", "2", "3x < 9", "x < 3 ⇒ eng katta butun: 2"),
        P("(1; 5) ∩ [3; 8] kesishmasidagi eng kichik butun son nechaga teng?", "3", "Kesishma [3; 5).", "[3; 5) ⇒ 3")],
    sentence_practice=[ORD("|x − 3| < 2 ni yechish tartibi", ["|x − 3| < 2", "−2 < x − 3 < 2", "−2 + 3 < x < 2 + 3", "1 < x < 5"])],
)

EXTRAS['m2e'] = dict(
    formulas=[F("O'rniga qo'yish", "y = f(x) ni ikkinchi tenglamaga qo'yamiz", ""),
              F("Qo'shish usuli", "tenglamalarni qo'shib bir noma'lumni yo'qotamiz", ""),
              F("Yechimlar soni", "kesishadi — 1; parallel — 0; ustma-ust — ∞", ""),
              F("Simmetrik sistema", "x + y = s, xy = p ⇒ t² − st + p = 0", "")],
    worked_examples=[
        W("{x + y = 5; 2x − y = 1} ni yeching", ["Tenglamalarni qo'shamiz: 3x = 6", "x = 2", "y = 5 − 2 = 3", "Tekshirish: 2·2 − 3 = 1 ✓"], "(2; 3)"),
        W("{x + y = 7; xy = 12} ni yeching", ["Viyet: t² − 7t + 12 = 0", "t = 3 va t = 4", "Juftliklar: (3; 4) va (4; 3)"], "(3; 4) va (4; 3)")],
    problems=[
        P("{x + y = 10; x − y = 2} sistemada x nechaga teng?", "6", "Qo'shing.", "2x = 12 ⇒ x = 6"),
        P("{y = 2x; x + y = 9} sistemada y nechaga teng?", "6", "y ni qo'ying.", "3x = 9; x = 3; y = 6"),
        P("{x + y = 7; xy = 12} sistemaning ikkala x qiymatini yozing (; bilan).", "3; 4", "t² − 7t + 12 = 0", "x = 3 yoki 4", fmt="3; 4"),
        P("1 daftar va 1 qalam 11 ming so'm; 3 daftar va 2 qalam 27 ming so'm. Daftar necha ming so'm?", "5", "d + q = 11; 3d + 2q = 27", "2d + 2q = 22 ayiring: d = 5"),
        P("Ikki son yig'indisi 20, ayirmasi 4. Katta son?", "12", "", "(20 + 4) : 2 = 12"),
        P("{3x + 2y = 12; y = 3} sistemada x nechaga teng?", "2", "", "3x + 6 = 12 ⇒ x = 2")],
    sentence_practice=[ORD("{x + y = 5; 2x − y = 1} ni yechish tartibi", ["Tenglamalarni qo'shamiz: 3x = 6", "x = 2", "y = 5 − x = 3", "Javob: (2; 3)"])],
)

EXTRAS['m2f'] = dict(
    formulas=[F("RQS", "maxraj ≠ 0; ildiz ostida ≥ 0", ""),
              F("Ildiz xossalari", "√(ab) = √a·√b; √(a²) = |a|", ""),
              F("Qo'shma ifoda", "(√a − √b)(√a + √b) = a − b", "1/(√3 − 1) = (√3 + 1)/2"),
              F("Kasr daraja", "a^(m/n) = ⁿ√(aᵐ)", "8^(2/3) = 4")],
    worked_examples=[
        W("(x² − 4)/(x − 2) ni soddalashtiring (x ≠ 2)", ["Suratni ajratamiz: x² − 4 = (x − 2)(x + 2)", "(x − 2) ni qisqartiramiz", "Natija: x + 2"], "x + 2"),
        W("√50 ni soddalashtiring", ["50 = 25 · 2", "√50 = √25 · √2", "= 5√2"], "5√2")],
    problems=[
        P("x = 3 da (x² − 9)/(x − 3) ifodaning qiymatini (soddalashtirib) toping.", "6", "x + 3", "(x−3)(x+3)/(x−3) = x + 3 = 6"),
        P("√72 = k·√2 bo'lsa, k nechaga teng?", "6", "72 = 36·2", "√72 = 6√2"),
        P("(√5 − 2)(√5 + 2) nechaga teng?", "1", "a² − b²", "5 − 4 = 1"),
        P("8^(2/3) nechaga teng?", "4", "∛8 = 2", "2² = 4"),
        P("√12 · √3 nechaga teng?", "6", "√(12·3)", "√36 = 6"),
        P("x = 2 da (x + 1)/(x − 1) ning qiymati nechaga teng?", "3", "", "3/1 = 3")],
    sentence_practice=[ORD("(x² − 4)/(x − 2) ni soddalashtirish tartibi", ["x² − 4 = (x − 2)(x + 2)", "(x − 2)(x + 2)/(x − 2)", "(x − 2) ni qisqartiramiz", "Natija: x + 2"])],
)
