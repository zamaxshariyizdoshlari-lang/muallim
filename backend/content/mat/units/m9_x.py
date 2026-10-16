# -*- coding: utf-8 -*-
from dsl import F, W, P, ORD

EXTRAS = {}

EXTRAS['m9a'] = dict(
    formulas=[F("Birinchi ajoyib limit", "lim(x→0) sin x / x = 1", ""),
              F("Ikkinchi ajoyib limit", "lim(x→∞) (1 + 1/x)ˣ = e", ""),
              F("Aniqmasliklar", "0/0, ∞/∞, ∞ − ∞, 0·∞, 1^∞", ""),
              F("Uzluksizlik", "lim f(x) = f(a)", "")],
    worked_examples=[
        W("lim(x→2) (x² − 4)/(x − 2) ni toping", ["Ifoda 0/0 aniqmaslik", "Surat: (x − 2)(x + 2)", "Qisqartiramiz: x + 2", "x → 2: 4"], "4"),
        W("lim(x→∞) (3x² + x)/(x² − 1) ni toping", ["∞/∞ aniqmaslik", "Surat va maxrajni x² ga bo'lamiz", "(3 + 1/x)/(1 − 1/x²)", "x → ∞: 3"], "3")],
    problems=[
        P("lim(n→∞) (2n + 1)/n nechaga teng?", "2", "", "2 + 1/n → 2"),
        P("lim(x→2) (x² − 4)/(x − 2) nechaga teng?", "4", "", "x + 2 → 4"),
        P("lim(x→∞) (3x² + x)/(x² − 1) nechaga teng?", "3", "", "3"),
        P("lim(x→0) sin 3x / x nechaga teng?", "3", "sin 3x / 3x ni ajrating.", "3 · 1 = 3"),
        P("lim(x→0) (eˣ − 1)/x nechaga teng?", "1", "", "1"),
        P("lim(x→0) (1 − cos x)/x² nechaga teng? (kasr)", "1/2", "", "1/2")],
    sentence_practice=[ORD("lim(x→2) (x² − 4)/(x − 2) ni hisoblash", ["Aniqmaslik 0/0", "x² − 4 = (x − 2)(x + 2)", "Qisqartirish: x + 2", "x → 2: limit = 4"])],
)

EXTRAS['m9b'] = dict(
    formulas=[F("Darajali", "(xⁿ)′ = n·xⁿ⁻¹", ""),
              F("Elementar", "(eˣ)′ = eˣ; (ln x)′ = 1/x; (sin x)′ = cos x; (cos x)′ = −sin x", ""),
              F("Ko'paytma va bo'linma", "(uv)′ = u′v + uv′; (u/v)′ = (u′v − uv′)/v²", ""),
              F("Zanjir qoidasi", "(f(g(x)))′ = f′(g(x))·g′(x)", "")],
    worked_examples=[
        W("f(x) = x² sin x ning hosilasini toping", ["u = x², v = sin x", "(uv)′ = u′v + uv′", "= 2x sin x + x² cos x"], "2x sin x + x² cos x"),
        W("f(x) = (3x + 1)⁵ ning hosilasini toping", ["Tashqi funksiya u⁵, ichki 3x + 1", "(u⁵)′ = 5u⁴; (3x + 1)′ = 3", "f′ = 5(3x + 1)⁴ · 3 = 15(3x + 1)⁴"], "15(3x + 1)⁴")],
    problems=[
        P("f(x) = x⁵ bo'lsa f′(1) nechaga teng?", "5", "", "5x⁴ ⇒ 5"),
        P("f(x) = 3x² − 4x + 7 bo'lsa f′(2) nechaga teng?", "8", "f′ = 6x − 4", "12 − 4 = 8"),
        P("f(x) = ln x bo'lsa f′(2) nechaga teng? (kasr)", "1/2", "", "1/x"),
        P("f(x) = sin 2x bo'lsa f′(0) nechaga teng?", "2", "2cos 2x", "2"),
        P("f(x) = x/(x + 1) bo'lsa f′(1) nechaga teng? (o'nli kasr)", "0,25", "(u′v − uv′)/v²", "1/(x+1)² = 1/4"),
        P("s(t) = t³ bo'lsa, t = 2 da oniy tezlik v nechaga teng?", "12", "v = s′", "3t² = 12")],
    sentence_practice=[ORD("(3x + 1)⁵ ning hosilasini topish", ["Tashqi funksiya u⁵, ichki u = 3x + 1", "(u⁵)′ = 5u⁴", "u′ = 3", "f′ = 15(3x + 1)⁴"])],
)

EXTRAS['m9c'] = dict(
    formulas=[F("Urinma", "y = f(x₀) + f′(x₀)(x − x₀)", ""),
              F("Monotonlik", "f′ > 0 — o'sadi; f′ < 0 — kamayadi", ""),
              F("Ekstremum", "f′ = 0, ishora +→− maksimum; −→+ minimum", ""),
              F("Eng katta/kichik qiymat", "kritik nuqtalar va kesma uchlari", "")],
    worked_examples=[
        W("f(x) = x³ − 3x ning ekstremumlarini toping", ["f′ = 3x² − 3 = 3(x − 1)(x + 1)", "Kritik nuqtalar: x = −1, x = 1", "x = −1 da f′: + → −: maksimum f(−1) = 2", "x = 1 da f′: − → +: minimum f(1) = −2"], "max 2 (x = −1); min −2 (x = 1)"),
        W("Perimetri 20 bo'lgan to'g'ri to'rtburchakning eng katta yuzini toping", ["Tomonlar x va 10 − x", "S = x(10 − x) = 10x − x²", "S′ = 10 − 2x = 0 ⇒ x = 5", "S = 25"], "25")],
    problems=[
        P("y = x² ga x = 1 nuqtadagi urinmaning burchak koeffitsienti?", "2", "f′(1)", "2"),
        P("y = x³ ga x = 1 da urinmaning Oy bilan kesishish ordinatasi?", "-2", "y = 1 + 3(x − 1)", "y(0) = −2"),
        P("f(x) = x² − 4x uchun f′(x) = 0 bo'ladigan x nechaga teng?", "2", "", "2x − 4 = 0"),
        P("f(x) = x³ − 3x ning [0; 2] kesmadagi eng katta qiymati?", "2", "f(0) = 0, f(1) = −2, f(2) = 2", "2"),
        P("S = x(10 − x) ning eng katta qiymati?", "25", "x = 5", "25"),
        P("f(x) = x² − 4x + 7 ning eng kichik qiymati?", "3", "x = 2 da", "4 − 8 + 7 = 3")],
    sentence_practice=[ORD("Eng katta yuzni topish (perimetr 20)", ["S = x(10 − x)", "S′ = 10 − 2x", "S′ = 0 ⇒ x = 5", "S_max = 25"])],
)

EXTRAS['m9d'] = dict(
    formulas=[F("Darajali", "∫xⁿ dx = xⁿ⁺¹/(n + 1) + C", "n ≠ −1"),
              F("Elementar", "∫eˣ dx = eˣ + C; ∫dx/x = ln|x| + C", ""),
              F("Trigonometrik", "∫sin x dx = −cos x + C; ∫cos x dx = sin x + C", ""),
              F("Bo'laklab", "∫u dv = uv − ∫v du", "")],
    worked_examples=[
        W("F′(x) = 2x va F(1) = 3 bo'lsa, F(x) ni toping", ["F(x) = x² + C", "F(1) = 1 + C = 3 ⇒ C = 2", "F(x) = x² + 2"], "x² + 2"),
        W("∫x eˣ dx ni toping", ["u = x, dv = eˣ dx ⇒ du = dx, v = eˣ", "= x eˣ − ∫eˣ dx", "= x eˣ − eˣ + C = (x − 1)eˣ + C"], "(x − 1)eˣ + C")],
    problems=[
        P("F′(x) = 2x, F(1) = 3 bo'lsa F(2) nechaga teng?", "6", "F = x² + 2", "4 + 2 = 6"),
        P("∫3x² dx = x^k + C bo'lsa, k nechaga teng?", "3", "", "x³"),
        P("∫cos x dx ning x = π/2 dagi qiymati (C = 0)?", "1", "sin x", "sin(π/2) = 1"),
        P("∫e^(3x) dx = k·e^(3x) + C bo'lsa k nechaga teng? (kasr)", "1/3", "", "1/3"),
        P("F′(x) = 6x − 4 va F(0) = 1 bo'lsa F(2) nechaga teng?", "5", "F = 3x² − 4x + 1", "12 − 8 + 1 = 5"),
        P("∫ 2x/(x² + 1) dx = ln(x² + k) + C bo'lsa, k nechaga teng?", "1", "", "ln(x² + 1)")],
    sentence_practice=[ORD("F′(x) = 2x, F(1) = 3 dan F ni topish", ["F(x) = x² + C", "F(1) = 1 + C = 3", "C = 2", "F(x) = x² + 2"])],
)

EXTRAS['m9e'] = dict(
    formulas=[F("Nyuton–Leybnits", "∫ₐᵇ f dx = F(b) − F(a)", ""),
              F("Yuza", "S = ∫ₐᵇ (f − g) dx", "f ≥ g"),
              F("Aylanish jismi hajmi", "V = π∫ₐᵇ f² dx", ""),
              F("Yo'l", "s = ∫ v dt", "")],
    worked_examples=[
        W("∫₀² x² dx ni hisoblang", ["Boshlang'ich funksiya: x³/3", "F(2) − F(0) = 8/3 − 0", "= 8/3"], "8/3"),
        W("y = x va y = x² orasidagi yuzani toping", ["Kesishish: x = x² ⇒ x = 0, x = 1", "S = ∫₀¹ (x − x²) dx", "= 1/2 − 1/3", "= 1/6"], "1/6")],
    problems=[
        P("∫₀² x² dx nechaga teng? (kasr)", "8/3", "", "8/3"),
        P("∫₀^π sin x dx nechaga teng?", "2", "−cos x", "1 + 1 = 2"),
        P("∫₁^e dx/x nechaga teng?", "1", "ln x", "1 − 0"),
        P("y = x va y = x² orasidagi shakl yuzi (kasr)?", "1/6", "", "1/2 − 1/3"),
        P("v = 3t² (m/s) bo'lsa, 0 dan 2 sekundgacha o'tilgan yo'l?", "8", "∫v dt", "t³ |₀² = 8", unit="m"),
        P("∫₋₁¹ x³ dx nechaga teng?", "0", "Toq funksiya", "0")],
    sentence_practice=[ORD("y = x va y = x² orasidagi yuzani topish", ["Kesishish: x = 0 va x = 1", "S = ∫₀¹ (x − x²) dx", "S = [x²/2 − x³/3]₀¹", "S = 1/6"])],
)

EXTRAS['m9f'] = dict(
    formulas=[F("Xususiy hosila", "∂f/∂x — y o'zgarmas", ""),
              F("Gradiyent", "∇f = (f_x; f_y)", "eng tez o'sish yo'nalishi"),
              F("Qator yaqinlashishi", "lim aₙ = 0 — zaruriy shart", ""),
              F("Makloren", "eˣ = Σxⁿ/n!; sin x = x − x³/3! + ...", "")],
    worked_examples=[
        W("f = x²y + y³ ning (1; 2) nuqtadagi xususiy hosilalarini toping", ["f_x = 2xy ⇒ f_x(1; 2) = 4", "f_y = x² + 3y² ⇒ f_y(1; 2) = 1 + 12 = 13"], "f_x = 4; f_y = 13"),
        W("Σ (1/3)ⁿ (n = 0, 1, 2, ...) qator yig'indisini toping", ["Geometrik qator: b₁ = 1, q = 1/3", "|q| < 1", "S = 1/(1 − 1/3) = 3/2"], "3/2")],
    problems=[
        P("f = x²y + y³ uchun f_x(1; 2) nechaga teng?", "4", "2xy", "2·1·2"),
        P("f = x²y + y³ uchun f_y(1; 2) nechaga teng?", "13", "x² + 3y²", "1 + 12"),
        P("f = x² + y² funksiya gradiyentining (3; 4) nuqtadagi uzunligi?", "10", "∇f = (2x; 2y)", "|(6; 8)| = 10"),
        P("Σ (1/2)ⁿ (n = 1, 2, 3, ...) qator yig'indisi?", "1", "b₁ = ½, q = ½", "1"),
        P("Σ (1/3)ⁿ (n = 0, 1, 2, ...) qator yig'indisi (kasr)?", "3/2", "", "1/(1 − 1/3)"),
        P("eˣ ning Makloren qatorida x³ oldidagi koeffitsientning maxraji (1/k)?", "6", "1/3!", "1/6")],
    sentence_practice=[ORD("Gradiyent uzunligini topish (f = x² + y², nuqta (3; 4))", ["f_x = 2x, f_y = 2y", "∇f(3; 4) = (6; 8)", "|∇f| = √(36 + 64)", "|∇f| = 10"])],
)
