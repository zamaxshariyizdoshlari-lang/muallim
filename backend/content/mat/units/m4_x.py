# -*- coding: utf-8 -*-
from dsl import F, W, P, ORD

EXTRAS = {}

EXTRAS['m4a'] = dict(
    formulas=[F("Qo'shni burchaklar", "α + β = 180°", "Vertikal burchaklar teng"),
              F("n-burchak ichki burchaklari", "(n − 2) · 180°", "Tashqi burchaklar yig'indisi 360°"),
              F("Muntazam n-burchak burchagi", "(n − 2) · 180° / n", "Oltiburchak: 120°"),
              F("Parallel chiziqlar", "ichki almashinuvchi va mos burchaklar teng", "Ichki bir tomonlilar yig'indisi 180°")],
    worked_examples=[
        W("Sakkizburchakning ichki burchaklari yig'indisini toping", ["n = 8", "(n − 2) · 180° = 6 · 180°", "= 1080°"], "1080°"),
        W("Qo'shni burchaklardan biri 65° bo'lsa, ikkinchisi?", ["Qo'shni burchaklar yig'indisi 180°", "180° − 65°", "= 115°"], "115°")],
    problems=[
        P("O'nburchak ichki burchaklarining yig'indisi necha graduslik?", "1440", "(n − 2)·180°", "8 · 180 = 1440", unit="°"),
        P("Muntazam o'n ikkiburchakning bitta ichki burchagi necha graduslik?", "150", "(12 − 2)·180/12", "1800/12 = 150", unit="°"),
        P("Qo'shni burchaklar 2 : 3 nisbatda. Kichigi necha graduslik?", "72", "5 qism = 180°", "180 : 5 = 36; 2·36 = 72", unit="°"),
        P("Parallel chiziqlarni kesuvchi kesganda ichki bir tomonli burchaklardan biri 70°. Ikkinchisi?", "110", "Yig'indi 180°", "180 − 70 = 110", unit="°"),
        P("Vertikal burchaklardan biri 48° bo'lsa, ikkinchisi necha graduslik?", "48", "Vertikal burchaklar teng.", "48", unit="°"),
        P("Uchburchak burchaklari 2 : 3 : 4 nisbatda. Eng kattasi necha graduslik?", "80", "9 qism = 180°", "20·4 = 80", unit="°")],
    sentence_practice=[ORD("Sakkizburchak burchaklari yig'indisini topish tartibi", ["n = 8", "(n − 2) · 180°", "6 · 180°", "= 1080°"])],
)

EXTRAS['m4b'] = dict(
    formulas=[F("Burchaklar yig'indisi", "A + B + C = 180°", ""),
              F("Tashqi burchak", "tashqi = qo'shni bo'lmagan ikki ichki yig'indisi", ""),
              F("Uchburchak tengsizligi", "|b − c| < a < b + c", ""),
              F("Mediana", "uchdan 2 : 1 nisbatda bo'linadi", "O'rta chiziq = asosning yarmi")],
    worked_examples=[
        W("Teng yonli uchburchak uchidagi burchak 40°. Asosidagi burchak?", ["Burchaklar yig'indisi 180°", "180° − 40° = 140°", "Asosdagi burchaklar teng: 140° : 2", "= 70°"], "70°"),
        W("Uchburchak tomonlari 5 va 7. Uchinchi tomon eng ko'pi bilan nechaga teng bo'lishi mumkin (butun)?", ["Uchburchak tengsizligi: c < 5 + 7 = 12", "c butun son", "Eng katta qiymat 11"], "11")],
    problems=[
        P("Uchburchakning ikki burchagi 50° va 65°. Uchinchisi necha graduslik?", "65", "", "180 − 115 = 65", unit="°"),
        P("Uchburchakning tashqi burchagi 120°, unga qo'shni bo'lmagan ichki burchaklardan biri 45°. Ikkinchisi?", "75", "Tashqi = ikki ichki yig'indisi", "120 − 45 = 75", unit="°"),
        P("Mediana 18 sm. Og'irlik markazi uchdan necha sm uzoqlikda?", "12", "2 : 1 nisbat", "18 · 2/3 = 12", unit="sm"),
        P("Uchburchak asosi 14 sm. O'rta chiziqning uzunligi?", "7", "", "14 : 2 = 7", unit="sm"),
        P("Teng yonli uchburchak perimetri 36, asosi 10. Yon tomoni?", "13", "", "(36 − 10) : 2 = 13", unit="sm"),
        P("Uchburchak tomonlari 5 va 7. Uchinchi tomon butun son bo'lsa, eng katta qiymati?", "11", "c < 12", "11")],
    sentence_practice=[ORD("Teng yonli uchburchak asos burchagini topish tartibi", ["Burchaklar yig'indisi 180°", "180° − 40° = 140°", "140° : 2", "Asos burchagi = 70°"])],
)

EXTRAS['m4c'] = dict(
    formulas=[F("Pifagor teoremasi", "c² = a² + b²", "c — gipotenuza"),
              F("Pifagor uchliklari", "(3;4;5), (5;12;13), (8;15;17), (7;24;25)", ""),
              F("Maxsus uchburchaklar", "45°: a, a, a√2; 30°-60°: a, a√3, 2a", ""),
              F("Masofa", "d = √((x₂ − x₁)² + (y₂ − y₁)²)", "")],
    worked_examples=[
        W("Katetlari 6 va 8 bo'lgan uchburchakning gipotenuzasini toping", ["c² = 6² + 8²", "c² = 36 + 64 = 100", "c = 10"], "10"),
        W("Narvon 13 m, devordan 5 m masofada turibdi. Devorga qanday balandlikda tegadi?", ["Narvon — gipotenuza: 13", "h² = 13² − 5² = 169 − 25", "h² = 144", "h = 12 m"], "12 m")],
    problems=[
        P("Katetlari 9 va 12 bo'lgan uchburchakning gipotenuzasi?", "15", "9² + 12² = 225", "√225 = 15"),
        P("Gipotenuza 17, kateti 8. Ikkinchi kateti?", "15", "17² − 8²", "289 − 64 = 225 ⇒ 15"),
        P("Tomoni 7 bo'lgan kvadrat diagonalining kvadrati nechaga teng?", "98", "d² = 7² + 7²", "49 + 49 = 98"),
        P("Tomonlari 8 va 15 bo'lgan to'g'ri to'rtburchakning diagonali?", "17", "", "√(64 + 225) = 17"),
        P("Romb diagonallari 10 va 24. Tomoni?", "13", "Yarim diagonallar 5 va 12.", "√(25 + 144) = 13"),
        P("Teng yonli uchburchak yon tomoni 10, asosi 12. Balandligi?", "8", "Asosning yarmi 6.", "√(100 − 36) = 8")],
    sentence_practice=[ORD("Narvon masalasini yechish tartibi", ["Gipotenuza 13, kateti 5", "h² = 13² − 5²", "h² = 169 − 25 = 144", "h = 12 m"])],
)

EXTRAS['m4d'] = dict(
    formulas=[F("Parallelogramm", "S = a · h", "P = 2(a + b)"),
              F("Romb", "S = d₁d₂ / 2", "Tomoni = √((d₁/2)² + (d₂/2)²)"),
              F("Trapesiya", "S = (a + b)/2 · h = m · h", "m — o'rta chiziq"),
              F("Diagonallar soni", "n(n − 3)/2", "")],
    worked_examples=[
        W("Asoslari 6 va 10, balandligi 4 bo'lgan trapesiya yuzini toping", ["O'rta chiziq: (6 + 10)/2 = 8", "S = m · h = 8 · 4", "S = 32"], "32"),
        W("Diagonallari 6 va 8 bo'lgan rombning yuzi va tomonini toping", ["S = 6·8/2 = 24", "Yarim diagonallar 3 va 4", "Tomon = √(9 + 16) = 5"], "S = 24, tomon 5")],
    problems=[
        P("Asosi 12, balandligi 5 bo'lgan parallelogramm yuzi?", "60", "", "12 · 5 = 60"),
        P("Trapesiyaning o'rta chizig'i 9, balandligi 4. Yuzi?", "36", "S = m·h", "36"),
        P("Diagonallari 10 va 24 bo'lgan romb yuzi?", "120", "d₁d₂/2", "10·24/2 = 120"),
        P("Kvadrat diagonali 8√2 bo'lsa, tomoni nechaga teng?", "8", "d = a√2", "8√2/√2 = 8"),
        P("Sakkizburchakning nechta diagonali bor?", "20", "n(n − 3)/2", "8·5/2 = 20"),
        P("To'g'ri to'rtburchak perimetri 30, bir tomoni 9. Yuzi?", "54", "Ikkinchi tomon: 15 − 9 = 6", "9 · 6 = 54")],
    sentence_practice=[ORD("Trapesiya yuzini topish tartibi", ["Asoslar: 6 va 10, h = 4", "O'rta chiziq m = (6 + 10)/2 = 8", "S = m · h", "S = 32"])],
)

EXTRAS['m4e'] = dict(
    formulas=[F("Aylana uzunligi", "C = 2πr", ""),
              F("Doira yuzi", "S = πr²", ""),
              F("Burchaklar", "ichki chizilgan = yoyning yarmi; diametrga tiralgani 90°", ""),
              F("Yoy va sektor", "l = πrα/180°; S = πr²α/360°", "")],
    worked_examples=[
        W("r = 5 bo'lgan aylana uzunligi va doira yuzini toping", ["C = 2πr = 2π · 5 = 10π", "S = πr² = π · 25 = 25π"], "C = 10π; S = 25π"),
        W("Markaziy burchak 80° bo'lsa, shu yoyga tiralgan ichki burchak?", ["Ichki chizilgan burchak yoyning yarmiga teng", "Markaziy burchak yoyga teng: 80°", "80° : 2 = 40°"], "40°")],
    problems=[
        P("Aylana uzunligi 20π bo'lsa, radiusi nechaga teng?", "10", "C = 2πr", "r = 10"),
        P("Radiusi 6 bo'lgan doira yuzi π ning necha barobari?", "36", "πr²", "36π"),
        P("Markaziy burchak 80° bo'lsa, shu yoyga tiralgan ichki burchak necha graduslik?", "40", "", "80 : 2 = 40", unit="°"),
        P("Radiusi 4 bo'lgan aylananing 90° li yoyi uzunligi π ning necha barobari?", "2", "l = πrα/180", "π·4·90/180 = 2π"),
        P("Katetlari 6 va 8 bo'lgan uchburchakka tashqi chizilgan aylana radiusi?", "5", "R = c/2", "10/2 = 5"),
        P("Aylana vatari 8, markazdan masofa 3. Radius?", "5", "Yarim vatar 4.", "√(16 + 9) = 5")],
    sentence_practice=[ORD("Radiusi 5 bo'lgan doira yuzini topish", ["S = πr²", "r = 5", "S = π · 25", "S = 25π"])],
)

EXTRAS['m4f'] = dict(
    formulas=[F("Gerone", "S = √(p(p − a)(p − b)(p − c))", "p = (a + b + c)/2"),
              F("Sinus orqali", "S = ½ab·sin C", ""),
              F("O'xshashlik", "perimetr k; yuza k²; hajm k³", ""),
              F("Koordinatalarda", "(x; y) → Ox ga simmetrik (x; −y)", "")],
    worked_examples=[
        W("Tomonlari 13, 14, 15 bo'lgan uchburchak yuzini toping", ["p = (13 + 14 + 15)/2 = 21", "p − a = 8; p − b = 7; p − c = 6", "S = √(21 · 8 · 7 · 6) = √7056", "S = 84"], "84"),
        W("O'xshashlik koeffitsienti 3 bo'lsa, yuzalar nisbati qancha?", ["Yuzalar k² nisbatda", "3² = 9"], "9")],
    problems=[
        P("13, 14, 15 tomonli uchburchakning 15 tomoniga tushirilgan balandligi (o'nli kasr)?", "11,2", "h = 2S/a, S = 84", "168 : 15 = 11,2"),
        P("O'xshash uchburchaklar yuzalari 1 : 9 nisbatda. O'xshashlik koeffitsienti?", "1/3", "k² = 1/9", "k = 1/3"),
        P("O'xshash uchburchaklar perimetrlari 12 va 30. Kattasining yuzi 100 bo'lsa, kichigining yuzi?", "16", "k = 12/30 = 2/5", "100 · 4/25 = 16"),
        P("A(0;0), B(4;0), C(0;3) uchburchak yuzi?", "6", "To'g'ri burchakli", "4·3/2 = 6"),
        P("A(1; 1) nuqtaning Ox ga nisbatan simmetrik nuqtasi ordinatasi?", "-1", "", "(1; −1)"),
        P("Tomonlari 10 va 10, ular orasidagi burchak 30° bo'lgan uchburchak yuzi?", "25", "½ab·sin30°", "½ · 100 · ½ = 25")],
    sentence_practice=[ORD("Gerone formulasi bilan yuza topish", ["p = (a + b + c)/2 = 21", "p − a = 8, p − b = 7, p − c = 6", "S = √(21 · 8 · 7 · 6)", "S = 84"])],
)
