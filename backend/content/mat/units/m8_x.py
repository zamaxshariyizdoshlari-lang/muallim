# -*- coding: utf-8 -*-
from dsl import F, W, P, ORD

EXTRAS = {}

EXTRAS['m8a'] = dict(
    formulas=[F("Masofa", "d = √((x₂ − x₁)² + (y₂ − y₁)²)", ""),
              F("Kesma o'rtasi", "((x₁ + x₂)/2; (y₁ + y₂)/2)", ""),
              F("Simmetriya", "Ox: (x; −y); Oy: (−x; y); boshiga: (−x; −y)", ""),
              F("Parallelogramm", "A + C = B + D", "diagonal o'rtalari ustma-ust")],
    worked_examples=[
        W("A(1; 2) va B(4; 6) orasidagi masofani toping", ["Δx = 3, Δy = 4", "d = √(9 + 16)", "d = 5"], "5"),
        W("A(0;0), B(4;1), C(5;4) berilgan. ABCD parallelogramm bo'lsa, D ni toping", ["D = A + C − B", "x: 0 + 5 − 4 = 1", "y: 0 + 4 − 1 = 3", "D(1; 3)"], "D(1; 3)")],
    problems=[
        P("A(1; 2) va B(4; 6) orasidagi masofa?", "5", "", "√(9 + 16)"),
        P("A(2; 4) va B(8; 10) kesma o'rtasining abssissasi?", "5", "", "(2 + 8)/2"),
        P("A(0;0), B(3;0), C(0;4) uchburchakning BC tomoni?", "5", "", "√(9 + 16)"),
        P("A(0;0), B(4;1), C(5;4) bo'lsa, parallelogrammning D uchi abssissasi?", "1", "D = A + C − B", "0 + 5 − 4 = 1"),
        P("A(0;0), B(4;0), C(0;3) uchburchak yuzi?", "6", "", "4·3/2"),
        P("A(3; −2) nuqtaning koordinata boshiga nisbatan simmetrik nuqtasi ordinatasi?", "2", "(−x; −y)", "(−3; 2)")],
    sentence_practice=[ORD("Ikki nuqta orasidagi masofani topish tartibi", ["A(1; 2), B(4; 6)", "Δx = 3, Δy = 4", "d = √(3² + 4²)", "d = 5"])],
)

EXTRAS['m8b'] = dict(
    formulas=[F("To'g'ri chiziq", "y = kx + b; Ax + By + C = 0", ""),
              F("Parallel / perpendikulyar", "k₁ = k₂; k₁k₂ = −1", ""),
              F("Nuqtadan chiziqqacha", "d = |Ax₀ + By₀ + C|/√(A² + B²)", ""),
              F("Aylana", "(x − a)² + (y − b)² = R²", "")],
    worked_examples=[
        W("(0; 0) nuqtadan 3x + 4y − 10 = 0 chiziqqacha masofani toping", ["A = 3, B = 4, C = −10", "d = |3·0 + 4·0 − 10|/√(9 + 16)", "d = 10/5", "d = 2"], "2"),
        W("x² + y² − 4x + 6y − 12 = 0 aylana markazi va radiusini toping", ["To'liq kvadrat: (x − 2)² + (y + 3)² = 12 + 4 + 9", "(x − 2)² + (y + 3)² = 25", "Markaz (2; −3), R = 5"], "(2; −3), R = 5")],
    problems=[
        P("(1; 2) va (3; 6) nuqtalardan o'tuvchi chiziqning burchak koeffitsienti?", "2", "", "(6 − 2)/(3 − 1)"),
        P("(0; 0) nuqtadan 3x + 4y − 10 = 0 chiziqqacha masofa?", "2", "", "10/5"),
        P("x² + y² − 4x + 6y − 12 = 0 aylananing radiusi?", "5", "To'liq kvadrat", "25 ⇒ R = 5"),
        P("x² + y² − 4x + 6y − 12 = 0 aylana markazining abssissasi?", "2", "", "(2; −3)"),
        P("3x + 4y − 10 = 0 va 3x + 4y + 5 = 0 chiziqlar orasidagi masofa?", "3", "|C₁ − C₂|/√(A² + B²)", "15/5 = 3"),
        P("y = −x/2 + 1 ga perpendikulyar chiziqning burchak koeffitsienti?", "2", "k₁k₂ = −1", "2")],
    sentence_practice=[ORD("Nuqtadan chiziqqacha masofani topish", ["A = 3, B = 4, C = −10", "d = |3·0 + 4·0 − 10|/√(3² + 4²)", "d = 10/5", "d = 2"])],
)

EXTRAS['m8c'] = dict(
    formulas=[F("Ellips", "x²/a² + y²/b² = 1; c² = a² − b²", "e = c/a < 1; S = πab"),
              F("Giperbola", "x²/a² − y²/b² = 1; c² = a² + b²", "asimptota y = ±(b/a)x; e > 1"),
              F("Parabola", "y² = 2px; fokus (p/2; 0)", "e = 1"),
              F("Konik kesimlar", "doira, ellips, parabola, giperbola", "")],
    worked_examples=[
        W("x²/25 + y²/9 = 1 ellipsning fokus masofasi c va ekssentrisitetini toping", ["a² = 25, b² = 9", "c² = a² − b² = 16 ⇒ c = 4", "e = c/a = 4/5 = 0,8"], "c = 4; e = 0,8"),
        W("x²/9 − y²/16 = 1 giperbola asimptotalarini yozing", ["a = 3, b = 4", "y = ±(b/a)x", "y = ±(4/3)x"], "y = ±4x/3")],
    problems=[
        P("x²/25 + y²/9 = 1 ellipsda c nechaga teng?", "4", "c² = a² − b²", "16 ⇒ 4"),
        P("x²/25 + y²/9 = 1 ellipsning ekssentrisiteti?", "0,8", "e = c/a", "4/5"),
        P("x²/25 + y²/9 = 1 ellips yuzi π ning necha barobari?", "15", "S = πab", "5·3 = 15"),
        P("x²/9 − y²/16 = 1 giperbolada c nechaga teng?", "5", "c² = a² + b²", "9 + 16 = 25"),
        P("x²/9 − y²/16 = 1 asimptotasining burchak koeffitsienti (kasr)?", "4/3", "b/a", "4/3"),
        P("y = x² parabola fokusining ordinatasi (o'nli kasr)?", "0,25", "y = ax²: 1/(4a)", "1/4")],
    sentence_practice=[ORD("Ellipsning ekssentrisitetini topish", ["a² = 25, b² = 9", "c² = a² − b² = 16", "c = 4", "e = c/a = 0,8"])],
)

EXTRAS['m8d'] = dict(
    formulas=[F("Koordinatalar", "AB = (x₂ − x₁; y₂ − y₁); |a| = √(x² + y²)", ""),
              F("Amallar", "a + b = (x₁ + x₂; y₁ + y₂); λa = (λx; λy)", ""),
              F("Skalyar ko'paytma", "a·b = x₁x₂ + y₁y₂ = |a||b|cos φ", ""),
              F("Perpendikulyarlik", "a ⊥ b ⇔ a·b = 0", "")],
    worked_examples=[
        W("a = (2; 3), b = (1; −1). 3a − 2b ni toping", ["3a = (6; 9)", "2b = (2; −2)", "3a − 2b = (6 − 2; 9 + 2)", "(4; 11)"], "(4; 11)"),
        W("a = (1; 2), b = (2; −1) vektorlar perpendikulyarmi?", ["a·b = 1·2 + 2·(−1)", "= 2 − 2 = 0", "Skalyar ko'paytma 0 — perpendikulyar"], "Ha")],
    problems=[
        P("A(1; 2), B(4; 6) bo'lsa, |AB| nechaga teng?", "5", "AB = (3; 4)", "5"),
        P("a = (2; 3), b = (1; −1). a + b vektorning abssissasi?", "3", "", "2 + 1"),
        P("a = (2; 3), b = (1; −1). 3a − 2b vektorning ordinatasi?", "11", "", "9 + 2"),
        P("a = (1; 2), b = (2; −1) bo'lsa, a·b nechaga teng?", "0", "", "2 − 2"),
        P("a = (1; 0), b = (1; 1) vektorlar orasidagi burchak necha graduslik?", "45", "cos φ = a·b/(|a||b|)", "1/√2 ⇒ 45°", unit="°"),
        P("a = (1; 2; 2) vektorning uzunligi?", "3", "√(1 + 4 + 4)", "3")],
    sentence_practice=[ORD("3a − 2b ni hisoblash (a = (2; 3), b = (1; −1))", ["3a = (6; 9)", "2b = (2; −2)", "3a − 2b = (6 − 2; 9 − (−2))", "(4; 11)"])],
)
