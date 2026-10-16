# -*- coding: utf-8 -*-
from dsl import F, W, P, ORD

EXTRAS = {}

EXTRAS['m1a'] = dict(
    formulas=[F("Qoldiqli bo'lish", "a = b·q + r, 0 ≤ r < b", "47 = 5·9 + 2"),
              F("Taqsimot qonuni", "a(b + c) = ab + ac", "25·12 = 25·10 + 25·2"),
              F("Amallar tartibi", "() → daraja → ·, : → +, −", "2 + 3·4 = 14"),
              F("Teskari amallar", "a + b = c ⇒ b = c − a", "x·k = n ⇒ x = n : k")],
    worked_examples=[
        W("Hisoblang: 3·(24 + 16) − 18 : 6", ["Avval qavs: 24 + 16 = 40", "Ko'paytirish: 3 · 40 = 120", "Bo'lish: 18 : 6 = 3", "Ayirish: 120 − 3 = 117"], "117"),
        W("4x − 7 = 25 tenglamani yeching", ["Ozod hadni o'tkazamiz: 4x = 25 + 7 = 32", "Ikkala tomonni 4 ga bo'lamiz: x = 32 : 4", "x = 8", "Tekshirish: 4·8 − 7 = 25 ✓"], "x = 8")],
    problems=[
        P("8 + 12 : 4 · 3 ifodasining qiymatini toping.", "17", "Avval bo'lish va ko'paytirish (chapdan o'ngga), keyin qo'shish.", "12 : 4 = 3; 3 · 3 = 9; 8 + 9 = 17"),
        P("47 ni 6 ga bo'lganda qoldiq nechaga teng?", "5", "6·7 = 42 ni oling.", "47 = 6·7 + 5"),
        P("5x + 3 = 38 tenglamaning ildizini toping.", "7", "Avval 3 ni o'ng tomonga o'tkazing.", "5x = 35; x = 7"),
        P("Taqsimot qonunidan foydalanib hisoblang: 25 · 36", "900", "36 = 30 + 6", "25·30 + 25·6 = 750 + 150 = 900"),
        P("(120 − 45) : 5 ni hisoblang.", "15", "", "75 : 5 = 15"),
        P("Eng katta uch xonali va eng kichik uch xonali son ayirmasini toping.", "899", "999 va 100.", "999 − 100 = 899")],
    sentence_practice=[ORD("3·(24 + 16) − 18 : 6 ni yechish tartibi", ["24 + 16 = 40", "3 · 40 = 120", "18 : 6 = 3", "120 − 3 = 117"])],
)

EXTRAS['m1b'] = dict(
    formulas=[F("3 va 9 ga bo'linish", "raqamlar yig'indisi 3 (9) ga bo'linadi", "729: 7+2+9 = 18 → 9 ga bo'linadi"),
              F("6 ga bo'linish", "2 ga ham, 3 ga ham bo'linadi", ""),
              F("EKUB va EKUK bog'lanishi", "EKUB(a, b) · EKUK(a, b) = a · b", "12 · 144 = 36 · 48"),
              F("Evklid algoritmi", "EKUB(a, b) = EKUB(b, a mod b)", "EKUB(48, 36) → (36, 12) → 12")],
    worked_examples=[
        W("84 va 126 ning EKUB va EKUK ini toping.", ["84 = 2²·3·7; 126 = 2·3²·7", "EKUB: umumiy ko'paytuvchilarning eng kichik darajalari: 2·3·7 = 42", "EKUK: barcha ko'paytuvchilarning eng katta darajalari: 2²·3²·7 = 252", "Tekshirish: 42·252 = 10 584 = 84·126 ✓"], "EKUB = 42, EKUK = 252"),
        W("Evklid algoritmi bilan EKUB(1071; 462) ni toping.", ["1071 = 2·462 + 147", "462 = 3·147 + 21", "147 = 7·21 + 0", "Oxirgi nolmas qoldiq — 21"], "21")],
    problems=[
        P("EKUB(36; 60) nechaga teng?", "12", "36 = 2²·3², 60 = 2²·3·5", "Umumiy: 2²·3 = 12"),
        P("EKUK(12; 18) nechaga teng?", "36", "EKUB(12,18) = 6; EKUK = 12·18 : 6", "216 : 6 = 36"),
        P("1 dan 20 gacha nechta tub son bor?", "8", "2, 3, 5, 7, ...", "2, 3, 5, 7, 11, 13, 17, 19 — 8 ta"),
        P("420 ni tub ko'paytuvchilarga yoyganda (takrorlari bilan) nechta ko'paytuvchi chiqadi?", "5", "420 = 2·210", "420 = 2²·3·5·7 → 2, 2, 3, 5, 7 — 5 ta"),
        P("EKUB(a; b) = 6, EKUK(a; b) = 72, a = 18 bo'lsa, b nechaga teng?", "24", "EKUB·EKUK = a·b", "6·72 = 432; b = 432 : 18 = 24"),
        P("Ikki avtobus 6 va 8 daqiqada qatnaydi. Birga chiqishgach, qancha daqiqadan keyin yana birga chiqadi?", "24", "EKUK(6, 8)", "EKUK(6; 8) = 24")],
    sentence_practice=[ORD("EKUB(1071; 462) ni Evklid algoritmi bilan topish tartibi", ["1071 = 2·462 + 147", "462 = 3·147 + 21", "147 = 7·21 + 0", "EKUB = 21"])],
)

EXTRAS['m1c'] = dict(
    formulas=[F("Qo'shish/ayirish", "a/b ± c/d = (ad ± bc)/(bd)", "Umumiy maxraj EKUK orqali"),
              F("Ko'paytirish", "a/b · c/d = ac/(bd)", "Avval qisqartiring"),
              F("Bo'lish", "a/b : c/d = a/b · d/c", "Teskarisiga ko'paytirish"),
              F("Aralash son", "n a/b = (nb + a)/b", "2 3/7 = 17/7")],
    worked_examples=[
        W("Hisoblang: 2/3 + 3/4", ["Umumiy maxraj: EKUK(3, 4) = 12", "2/3 = 8/12; 3/4 = 9/12", "8/12 + 9/12 = 17/12", "Butun ajratamiz: 17/12 = 1 5/12"], "1 5/12"),
        W("Hisoblang: 5/6 : 10/9", ["Teskarisiga ko'paytiramiz: 5/6 · 9/10", "Surat va maxraj: (5·9)/(6·10) = 45/60", "45/60 ni 15 ga qisqartiramiz", "= 3/4"], "3/4")],
    problems=[
        P("1/2 + 1/3 ni hisoblang (kasr ko'rinishida).", "5/6", "Umumiy maxraj 6.", "3/6 + 2/6 = 5/6"),
        P("3/4 · 8/9 ni hisoblang.", "2/3", "Avval qisqartiring.", "(3·8)/(4·9) = 24/36 = 2/3"),
        P("2 1/2 − 1 1/3 ni hisoblang (noto'g'ri kasr shaklida).", "7/6", "5/2 − 4/3", "15/6 − 8/6 = 7/6"),
        P("3/5 : 3/10 ni hisoblang.", "2", "3/5 · 10/3", "30/15 = 2"),
        P("x ning 2/5 qismi 18 ga teng. x ni toping.", "45", "x · 2/5 = 18", "x = 18 : 2/5 = 18 · 5/2 = 45"),
        P("7/12 − 1/4 ni hisoblang (qisqargan kasr).", "1/3", "1/4 = 3/12", "7/12 − 3/12 = 4/12 = 1/3")],
    sentence_practice=[ORD("2/3 + 3/4 ni hisoblash tartibi", ["Umumiy maxraj topiladi: EKUK(3, 4) = 12", "8/12 + 9/12", "17/12", "1 5/12"])],
)

EXTRAS['m1d'] = dict(
    formulas=[F("Qo'shish/ayirish", "vergul vergul tagida", "3,45 + 2,7 = 6,15"),
              F("Ko'paytirish", "kasr xonalar yig'indisi", "0,3 · 0,4 = 0,12"),
              F("10ⁿ ga ko'paytirish", "vergul n xona o'ngga", "3,45 · 100 = 345"),
              F("Oddiy ↔ o'nli", "1/2 = 0,5; 1/4 = 0,25; 1/8 = 0,125", "1/3 = 0,(3)")],
    worked_examples=[
        W("12,5 − 4,75 ni hisoblang", ["12,50 − 4,75 deb yozamiz", "Vergullarni tekislab ustunda ayiramiz", "12,50 − 4,75 = 7,75"], "7,75"),
        W("3,6 : 0,12 ni hisoblang", ["Bo'luvchida vergulni 2 xona o'ngga suramiz: 0,12 → 12", "Bo'linuvchida ham 2 xona: 3,6 → 360", "360 : 12 = 30"], "30")],
    problems=[
        P("0,3 + 0,45 nechaga teng?", "0,75", "0,30 + 0,45", "0,75"),
        P("2,4 · 0,5 nechaga teng?", "1,2", "24·5 = 120, 2 ta kasr xona", "120 → 1,20 = 1,2"),
        P("7,2 : 0,9 nechaga teng?", "8", "72 : 9", "72 : 9 = 8"),
        P("1/8 ni o'nli kasr ko'rinishida yozing.", "0,125", "1 : 8", "1 : 8 = 0,125"),
        P("0,6 ni qisqargan oddiy kasr ko'rinishida yozing.", "3/5", "6/10", "6/10 = 3/5"),
        P("100 · 0,075 nechaga teng?", "7,5", "Vergul 2 xona o'ngga.", "0,075 · 100 = 7,5")],
    sentence_practice=[ORD("3,6 : 0,12 ni hisoblash tartibi", ["Bo'luvchini butun qilamiz: 0,12 → 12 (2 xona)", "Bo'linuvchini ham 2 xona suramiz: 3,6 → 360", "360 : 12", "= 30"])],
)

EXTRAS['m1e'] = dict(
    formulas=[F("Sonning p% i", "N · p / 100", "240 ning 15% i = 36"),
              F("Foiz oshirish/kamaytirish", "×(1 ± p/100)", "20% oshish: ×1,2"),
              F("Murakkab foiz", "S = P(1 + r)ⁿ", "1000, 10%, 2 yil → 1210"),
              F("Proporsiya", "a : b = c : d ⇒ ad = bc", "x : 4 = 15 : 12")],
    worked_examples=[
        W("Narxi 800 so'm bo'lgan tovar 15% arzonlashdi. Yangi narx?", ["15% = 0,15", "Chegirma: 800 · 0,15 = 120", "Yangi narx: 800 − 120 = 680", "Yoki bir amalda: 800 · 0,85 = 680"], "680 so'm"),
        W("3 ishchi ishni 12 kunda bajaradi. 6 ishchi necha kunda bajaradi?", ["Ishchi soni 2 marta oshdi", "Ish teskari proporsional: kun 2 marta kamayadi", "12 : 2 = 6"], "6 kun")],
    problems=[
        P("240 ning 15% i nechaga teng?", "36", "240 · 0,15", "36"),
        P("Biror sonning 30% i 45 ga teng. Shu sonni toping.", "150", "45 : 0,3", "45 : 0,3 = 150"),
        P("8 kg olma 640 so'm tursa, 5 kg necha so'm?", "400", "1 kg narxini toping.", "640 : 8 = 80; 80 · 5 = 400"),
        P("2000 so'm narx 10% ga oshdi. Yangi narx?", "2200", "×1,1", "2000 · 1,1 = 2200"),
        P("1000 so'm yiliga 20% murakkab foizda 2 yildan keyin necha so'm bo'ladi?", "1440", "1000·1,2·1,2", "1000 · 1,44 = 1440"),
        P("x : 4 = 15 : 12 proporsiyadan x ni toping.", "5", "ad = bc", "12x = 60; x = 5")],
    sentence_practice=[ORD("Narxni 15% arzonlashtirish (800 so'm) tartibi", ["15% = 0,15", "Chegirma: 800 · 0,15 = 120", "Yangi narx: 800 − 120", "= 680 so'm"])],
)

EXTRAS['m1f'] = dict(
    formulas=[F("Modul", "|a| = a (a ≥ 0); |a| = −a (a < 0)", "|−5| = 5"),
              F("Daraja xossalari", "aᵐ·aⁿ = aᵐ⁺ⁿ; aᵐ/aⁿ = aᵐ⁻ⁿ; (aᵐ)ⁿ = aᵐⁿ", ""),
              F("Nol va manfiy daraja", "a⁰ = 1; a⁻ⁿ = 1/aⁿ", "2⁻³ = 1/8"),
              F("Standart ko'rinish", "a·10ⁿ, 1 ≤ a < 10", "5 400 000 = 5,4·10⁶")],
    worked_examples=[
        W("Hisoblang: (−3)² + 2³ − |−5|", ["(−3)² = 9", "2³ = 8", "|−5| = 5", "9 + 8 − 5 = 12"], "12"),
        W("Soddalashtiring: 2⁵ · 2⁻²", ["Asoslar bir xil — ko'rsatkichlar qo'shiladi", "5 + (−2) = 3", "2³ = 8"], "8")],
    problems=[
        P("|−7| + |3| nechaga teng?", "10", "", "7 + 3 = 10"),
        P("(−2)³ nechaga teng?", "-8", "Manfiy sonning toq darajasi manfiy.", "(−2)(−2)(−2) = −8"),
        P("5⁰ + 3⁻¹ ni kasr ko'rinishida yozing.", "4/3", "5⁰ = 1; 3⁻¹ = 1/3", "1 + 1/3 = 4/3"),
        P("2⁴ · 2³ : 2⁵ nechaga teng?", "4", "Ko'rsatkichlar: 4 + 3 − 5", "2² = 4"),
        P("√169 nechaga teng?", "13", "13 ning kvadratini tekshiring.", "13² = 169"),
        P("3 500 000 = 3,5 · 10ⁿ bo'lsa, n nechaga teng?", "6", "Vergulni nechta xona surdingiz?", "3 500 000 → 3,5 : 6 xona; n = 6")],
    sentence_practice=[ORD("(−3)² + 2³ − |−5| ni hisoblash tartibi", ["(−3)² = 9", "2³ = 8", "|−5| = 5", "9 + 8 − 5 = 12"])],
)
