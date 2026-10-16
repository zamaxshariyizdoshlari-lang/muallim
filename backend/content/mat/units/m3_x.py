# -*- coding: utf-8 -*-
from dsl import F, W, P, ORD

EXTRAS = {}

EXTRAS['m3a'] = dict(
    formulas=[F("Diskriminant", "D = b² − 4ac", "D > 0: 2 ildiz; D = 0: 1; D < 0: yo'q"),
              F("Ildizlar", "x₁,₂ = (−b ± √D)/(2a)", ""),
              F("Viyet teoremasi", "x₁ + x₂ = −b/a; x₁x₂ = c/a", ""),
              F("Bikvadrat", "ax⁴ + bx² + c = 0, t = x²", "t ≥ 0")],
    worked_examples=[
        W("2x² − 3x − 2 = 0 ni yeching", ["a = 2, b = −3, c = −2", "D = 9 + 16 = 25", "x = (3 ± 5)/4", "x₁ = 2; x₂ = −1/2"], "2; −1/2"),
        W("x⁴ − 5x² + 4 = 0 ni yeching", ["t = x² deymiz: t² − 5t + 4 = 0", "t = 1 yoki t = 4", "x² = 1 ⇒ x = ±1; x² = 4 ⇒ x = ±2", "To'rtta ildiz: ±1, ±2"], "±1; ±2")],
    problems=[
        P("2x² + 5x − 3 = 0 tenglamaning diskriminanti nechaga teng?", "49", "b² − 4ac", "25 + 24 = 49"),
        P("x² − 4x − 5 = 0 tenglama ildizlarining ko'paytmasi nechaga teng?", "-5", "Viyet: c/a", "−5"),
        P("Ildizlari 2 va −5 bo'lgan x² + px + q = 0 tenglamada p nechaga teng?", "3", "p = −(x₁ + x₂)", "x₁ + x₂ = −3 ⇒ p = 3"),
        P("x⁴ − 5x² + 4 = 0 tenglama nechta haqiqiy ildizga ega?", "4", "t = x²", "±1 va ±2 — 4 ta"),
        P("x² − 6x + 9 = 0 tenglamaning ildizini toping.", "3", "D = 0", "(x − 3)² = 0 ⇒ x = 3"),
        P("x² − 5x + 3 = 0 ning ildizlari uchun x₁² + x₂² ni toping.", "19", "(x₁ + x₂)² − 2x₁x₂", "25 − 6 = 19")],
    sentence_practice=[ORD("x² − 5x + 6 = 0 ni diskriminant bilan yechish tartibi", ["a = 1, b = −5, c = 6", "D = 25 − 24 = 1", "x = (5 ± 1)/2", "x₁ = 3, x₂ = 2"])],
)

EXTRAS['m3b'] = dict(
    formulas=[F("Chiziqli funksiya", "y = kx + b", "k — qiyalik, b — Oy dagi kesishish"),
              F("Ikki nuqtadan", "k = (y₂ − y₁)/(x₂ − x₁)", ""),
              F("Parallel / perpendikulyar", "k₁ = k₂; k₁·k₂ = −1", ""),
              F("Juft va toq", "f(−x) = f(x); f(−x) = −f(x)", "")],
    worked_examples=[
        W("(1; 2) va (3; 6) nuqtalardan o'tuvchi chiziq tenglamasini yozing", ["k = (6 − 2)/(3 − 1) = 2", "y − 2 = 2(x − 1)", "y = 2x − 2 + 2", "y = 2x"], "y = 2x"),
        W("f(x) = 2x + 3 da f(x) = 5 bo'ladigan x ni toping", ["2x + 3 = 5", "2x = 2", "x = 1"], "x = 1")],
    problems=[
        P("f(x) = 3x − 2 bo'lsa, f(5) nechaga teng?", "13", "", "15 − 2 = 13"),
        P("(0; 4) va (2; 0) nuqtalardan o'tuvchi to'g'ri chiziqning burchak koeffitsienti?", "-2", "k = Δy/Δx", "(0 − 4)/(2 − 0) = −2"),
        P("y = 2x − 4 chiziq Ox o'qini qaysi x da kesadi?", "2", "y = 0 deng.", "2x − 4 = 0 ⇒ x = 2"),
        P("y = −x/2 + 1 ga perpendikulyar chiziqning burchak koeffitsienti nechaga teng?", "2", "k₁k₂ = −1", "(−1/2)·k = −1 ⇒ k = 2"),
        P("f(x) = √(x − 3) ning aniqlanish sohasidagi eng kichik butun x nechaga teng?", "3", "x − 3 ≥ 0", "x ≥ 3"),
        P("f(x) = 1/(x² − 4) funksiya nechta nuqtada aniqlanmagan?", "2", "x² − 4 = 0", "x = 2 va x = −2")],
    sentence_practice=[ORD("(1; 2) va (3; 6) dan o'tuvchi chiziqni topish tartibi", ["k = (6 − 2)/(3 − 1) = 2", "y − 2 = 2(x − 1)", "y = 2x − 2 + 2", "y = 2x"])],
)

EXTRAS['m3c'] = dict(
    formulas=[F("Uchi", "x₀ = −b/(2a); y₀ = f(x₀)", ""),
              F("Yo'nalish", "a > 0 — yuqoriga; a < 0 — pastga", ""),
              F("Standart ko'rinish", "y = a(x − m)² + n", "uchi (m; n)"),
              F("Kvadrat tengsizlik", "a > 0, D > 0: f < 0 ildizlar orasida", "")],
    worked_examples=[
        W("y = x² − 4x + 7 ning eng kichik qiymatini toping", ["a = 1 > 0 — minimum bor", "x₀ = 4/2 = 2", "y₀ = 4 − 8 + 7 = 3", "Eng kichik qiymat 3"], "3"),
        W("x² − 5x + 4 < 0 ni yeching", ["Ildizlar: x₁ = 1, x₂ = 4", "a > 0 — parabola ildizlar orasida manfiy", "1 < x < 4"], "(1; 4)")],
    problems=[
        P("y = x² − 6x + 5 parabola uchining abssissasi nechaga teng?", "3", "−b/(2a)", "6/2 = 3"),
        P("y = x² − 6x + 5 parabola uchining ordinatasi nechaga teng?", "-4", "x₀ = 3 ni qo'ying.", "9 − 18 + 5 = −4"),
        P("y = −2x² + 8x funksiyaning eng katta qiymatini toping.", "8", "x₀ = 2", "−8 + 16 = 8"),
        P("x² − 5x + 4 < 0 tengsizlikning butun yechimlari nechta?", "2", "1 < x < 4", "2 va 3"),
        P("Perimetri 24 bo'lgan to'g'ri to'rtburchakning eng katta yuzi nechaga teng?", "36", "S = x(12 − x)", "x = 6: S = 36"),
        P("y = x² + bx + c parabola uchining abssissasi −2 bo'lsa, b nechaga teng?", "4", "−b/2 = −2", "b = 4")],
    sentence_practice=[ORD("y = x² − 4x + 7 ning minimumini topish tartibi", ["a = 1 > 0 — minimum bor", "x₀ = −b/(2a) = 2", "y₀ = 4 − 8 + 7", "y_min = 3"])],
)

EXTRAS['m3d'] = dict(
    formulas=[F("Ko'rsatkichli funksiya", "y = aˣ, a > 0, a ≠ 1", "E = (0; +∞)"),
              F("Bir xil asos", "aᶠ = aᵍ ⇒ f = g", ""),
              F("O'sish", "N = N₀ · aᵗ", ""),
              F("Tengsizlik", "a > 1: belgi saqlanadi; 0 < a < 1: o'zgaradi", "")],
    worked_examples=[
        W("4ˣ − 3·2ˣ + 2 = 0 ni yeching", ["t = 2ˣ (t > 0): t² − 3t + 2 = 0", "t = 1 yoki t = 2", "2ˣ = 1 ⇒ x = 0; 2ˣ = 2 ⇒ x = 1", "Ildizlar: 0 va 1"], "0; 1"),
        W("(1/2)ˣ > 4 ni yeching", ["4 = (1/2)⁻²", "Asos 0 < 1/2 < 1 — belgi teskari bo'ladi", "x < −2"], "x < −2")],
    problems=[
        P("3^(x+1) = 27 tenglamaning ildizini toping.", "2", "27 = 3³", "x + 1 = 3 ⇒ x = 2"),
        P("(1/2)ˣ = 8 tenglamaning ildizini toping.", "-3", "8 = 2³ = (1/2)⁻³", "x = −3"),
        P("2ˣ > 16 tengsizlik x > ? shaklida yechiladi. Sonni yozing.", "4", "16 = 2⁴", "x > 4"),
        P("9ˣ − 4·3ˣ + 3 = 0 ning ildizlarini yozing (; bilan).", "0; 1", "t = 3ˣ", "t = 1, 3 ⇒ x = 0; 1", fmt="0; 1"),
        P("Bakteriyalar har soatda 2 barobar ko'payadi. Boshida 100 ta bo'lsa, 4 soatdan keyin nechta?", "1600", "100·2⁴", "100 · 16 = 1600"),
        P("5^(2x − 1) = 125 tenglamaning ildizini toping.", "2", "125 = 5³", "2x − 1 = 3 ⇒ x = 2")],
    sentence_practice=[ORD("2ˣ = 8 ni yechish tartibi", ["8 ni 2 ning darajasi qilamiz: 8 = 2³", "2ˣ = 2³", "Asoslar teng — ko'rsatkichlar teng", "x = 3"])],
)

EXTRAS['m3e'] = dict(
    formulas=[F("Ta'rif", "log_a b = c ⇔ aᶜ = b", "b > 0, a > 0, a ≠ 1"),
              F("Ko'paytma/bo'linma", "log(xy) = log x + log y; log(x/y) = log x − log y", ""),
              F("Daraja", "log xᵖ = p · log x", ""),
              F("Asos almashtirish", "log_a b = log_c b / log_c a", "")],
    worked_examples=[
        W("log₂ x + log₂ (x − 2) = 3 ni yeching", ["RQS: x > 2", "log₂ [x(x − 2)] = 3 ⇒ x(x − 2) = 8", "x² − 2x − 8 = 0 ⇒ x = 4 yoki x = −2", "x = −2 RQS ga kirmaydi"], "x = 4"),
        W("log₃ 81 − log₃ 3 ni hisoblang", ["log₃ 81 = 4 (3⁴ = 81)", "log₃ 3 = 1", "4 − 1 = 3"], "3")],
    problems=[
        P("log₂ 32 nechaga teng?", "5", "2^? = 32", "2⁵ = 32"),
        P("log₅ (1/25) nechaga teng?", "-2", "1/25 = 5⁻²", "−2"),
        P("log₂ 12 − log₂ 3 nechaga teng?", "2", "log₂ (12/3)", "log₂ 4 = 2"),
        P("lg 0,001 nechaga teng?", "-3", "10^? = 0,001", "10⁻³ ⇒ −3"),
        P("log₃ (x − 1) = 2 tenglamaning ildizini toping.", "10", "x − 1 = 3²", "x = 10"),
        P("2^(log₂ 7) nechaga teng?", "7", "Asosiy logarifmik ayniyat", "a^(log_a b) = b ⇒ 7")],
    sentence_practice=[ORD("log₃ (x − 1) = 2 ni yechish tartibi", ["RQS: x − 1 > 0", "Ta'rifdan: x − 1 = 3²", "x − 1 = 9", "x = 10"])],
)

EXTRAS['m3f'] = dict(
    formulas=[F("Modul", "|f| = a ⇒ f = ±a", "a > 0"),
              F("Modulli tengsizlik", "|f| < a ⇔ −a < f < a", ""),
              F("Irratsional", "√f = g ⇔ g ≥ 0 va f = g²", "ildizlarni tekshiring"),
              F("Kasr nolga teng", "P/Q = 0 ⇔ P = 0 va Q ≠ 0", "")],
    worked_examples=[
        W("√(x + 6) = x ni yeching", ["Shart: x ≥ 0", "Kvadratga ko'taramiz: x + 6 = x²", "x² − x − 6 = 0 ⇒ x = 3 yoki x = −2", "x = −2 shartga zid (chet ildiz)"], "x = 3"),
        W("(x² − 4)/(x − 2) = 0 ni yeching", ["Surat nolga teng: x² − 4 = 0 ⇒ x = ±2", "Maxraj ≠ 0: x ≠ 2", "Faqat x = −2"], "x = −2")],
    problems=[
        P("|x − 2| = 3 tenglamaning ildizlarini yozing (; bilan).", "5; -1", "", "x − 2 = ±3", fmt="5; -1"),
        P("√(2x + 1) = 3 tenglamaning ildizini toping.", "4", "Kvadratga ko'taring.", "2x + 1 = 9 ⇒ x = 4"),
        P("(x² − 4)/(x − 2) = 0 tenglamaning ildizini toping.", "-2", "x ≠ 2 ni unutmang.", "x = −2"),
        P("|x| < 2 tengsizlikning butun yechimlari nechta?", "3", "−2 < x < 2", "−1, 0, 1 — 3 ta"),
        P("(x − 1)/(x + 2) > 0 tengsizlikning eng kichik butun musbat yechimi nechaga teng?", "2", "x < −2 yoki x > 1", "x > 1 ⇒ 2"),
        P("1/x = 2 tenglamaning ildizini (o'nli kasrda) toping.", "0,5", "", "x = 1/2")],
    sentence_practice=[ORD("√(x + 6) = x ni yechish tartibi", ["Shart: x ≥ 0", "x + 6 = x²", "x² − x − 6 = 0 ⇒ x = 3 yoki x = −2", "x = −2 chet ildiz — javob x = 3"])],
)
