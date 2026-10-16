# -*- coding: utf-8 -*-
from dsl import F, W, P, ORD

EXTRAS = {}

EXTRAS['m6a'] = dict(
    formulas=[F("Nisbatlar", "sin = qarshisidagi/gipotenuza; cos = yopishgan/gipotenuza; tg = sin/cos", ""),
              F("Asosiy ayniyat", "sin²α + cos²α = 1", ""),
              F("Radian", "180° = π rad", "1 rad ≈ 57,3°"),
              F("Maxsus qiymatlar", "30°: ½, √3/2; 45°: √2/2; 60°: √3/2, ½", "")],
    worked_examples=[
        W("Gipotenuza 10, o'tkir burchak 30°. Qarshisidagi kateti?", ["sin 30° = qarshisidagi kateti / gipotenuza", "kateti = 10 · sin 30°", "= 10 · ½", "= 5"], "5"),
        W("3-4-5 uchburchakda 3 qarshisidagi burchak sinus, kosinus, tangensini toping", ["sin α = 3/5", "cos α = 4/5", "tg α = 3/4"], "3/5; 4/5; 3/4")],
    problems=[
        P("sin 30° nechaga teng? (kasr)", "1/2", "", "½"),
        P("cos 60° nechaga teng? (kasr)", "1/2", "", "½"),
        P("150° necha π/6 ga teng? (sonni yozing)", "5", "150° = 5·30°", "30° = π/6 ⇒ 150° = 5π/6"),
        P("tg 45° nechaga teng?", "1", "", "sin 45° / cos 45° = 1"),
        P("O'tkir α uchun sin α = 3/5 bo'lsa, cos α nechaga teng? (kasr)", "4/5", "sin² + cos² = 1", "√(1 − 9/25) = 4/5"),
        P("π/3 radian necha graduslik?", "60", "", "180° : 3 = 60", unit="°")],
    sentence_practice=[ORD("Qarshisidagi katetni topish tartibi (gipotenuza 10, α = 30°)", ["sin α = qarshisidagi kateti / gipotenuza", "kateti = 10 · sin 30°", "kateti = 10 · ½", "kateti = 5"])],
)

EXTRAS['m6b'] = dict(
    formulas=[F("Choraklar", "I: hammasi +; II: sin +; III: tg +; IV: cos +", ""),
              F("Juft-toqlik", "cos(−α) = cos α; sin(−α) = −sin α", ""),
              F("Keltirish", "sin(180° − α) = sin α; cos(180° − α) = −cos α", ""),
              F("Qo'shimcha ayniyatlar", "1 + tg²α = 1/cos²α", "")],
    worked_examples=[
        W("sin 150° ni hisoblang", ["150° = 180° − 30°", "sin(180° − α) = sin α", "sin 150° = sin 30° = ½"], "1/2"),
        W("cos 120° ni hisoblang", ["120° = 180° − 60°", "cos(180° − α) = −cos α", "cos 120° = −cos 60° = −½"], "−1/2")],
    problems=[
        P("sin 150° nechaga teng? (kasr)", "1/2", "", "sin 30°"),
        P("cos 120° nechaga teng? (kasr)", "-1/2", "II chorakda cos manfiy.", "−cos 60° = −½"),
        P("tg 225° nechaga teng?", "1", "225° = 180° + 45°", "tg 45° = 1"),
        P("sin 330° nechaga teng? (kasr)", "-1/2", "IV chorak: sin manfiy.", "−sin 30° = −½"),
        P("O'tkir α uchun sin α = 0,6 bo'lsa, cos α nechaga teng?", "0,8", "", "√(1 − 0,36) = 0,8"),
        P("tg α = 2 bo'lsa, cos²α nechaga teng? (kasr)", "1/5", "1 + tg²α = 1/cos²α", "1 + 4 = 5 ⇒ cos²α = 1/5")],
    sentence_practice=[ORD("cos 120° ni hisoblash tartibi", ["120° = 180° − 60°", "cos(180° − α) = −cos α", "cos 120° = −cos 60°", "cos 120° = −½"])],
)

EXTRAS['m6c'] = dict(
    formulas=[F("Qo'shish", "sin(α ± β) = sinα cosβ ± cosα sinβ", ""),
              F("Qo'shish (kosinus)", "cos(α ± β) = cosα cosβ ∓ sinα sinβ", ""),
              F("Ikkilangan", "sin 2α = 2 sinα cosα; cos 2α = 1 − 2sin²α", ""),
              F("Tangens yig'indisi", "tg(α + β) = (tgα + tgβ)/(1 − tgα·tgβ)", "")],
    worked_examples=[
        W("sin α = 3/5 (o'tkir). sin 2α ni toping", ["cos α = 4/5", "sin 2α = 2 sin α cos α", "= 2 · 3/5 · 4/5", "= 24/25"], "24/25"),
        W("tg α = 1/2 va tg β = 1/3. tg(α + β) ni toping", ["tg(α + β) = (tg α + tg β)/(1 − tg α tg β)", "Surat: 1/2 + 1/3 = 5/6", "Maxraj: 1 − 1/6 = 5/6", "5/6 : 5/6 = 1"], "1")],
    problems=[
        P("sin α = 3/5 (o'tkir) bo'lsa, sin 2α nechaga teng? (kasr)", "24/25", "", "2·(3/5)(4/5)"),
        P("sin α = 3/5 (o'tkir) bo'lsa, cos 2α nechaga teng? (kasr)", "7/25", "1 − 2sin²α", "1 − 18/25 = 7/25"),
        P("cos α = 0,6 bo'lsa, cos 2α nechaga teng?", "-0,28", "2cos²α − 1", "2·0,36 − 1 = −0,28"),
        P("sin 15° · cos 15° nechaga teng? (kasr)", "1/4", "½ sin 30°", "½ · ½ = ¼"),
        P("tg α = 1/2, tg β = 1/3 bo'lsa, tg(α + β) nechaga teng?", "1", "", "(5/6)/(5/6) = 1"),
        P("sin 40° cos 5° + cos 40° sin 5° ifodaning qiymatini toping (sin x ko'rinishida x = ?)", "45", "sin(α + β)", "sin 45°", unit="°")],
    sentence_practice=[ORD("sin 2α ni topish tartibi (sin α = 3/5)", ["cos α = √(1 − 9/25) = 4/5", "sin 2α = 2 sin α cos α", "sin 2α = 2 · 3/5 · 4/5", "sin 2α = 24/25"])],
)

EXTRAS['m6d'] = dict(
    formulas=[F("Davrlar", "sin, cos: 2π; tg, ctg: π", ""),
              F("Umumiy ko'rinish", "y = A sin(ωx + φ) + B", "amplituda |A|, davr 2π/|ω|"),
              F("Teskari funksiyalar", "arcsin ∈ [−π/2; π/2]; arccos ∈ [0; π]", ""),
              F("Munosabat", "arcsin a + arccos a = π/2", "")],
    worked_examples=[
        W("y = 3 sin 2x ning amplitudasi va davrini toping", ["A = 3 — amplituda", "ω = 2", "Davr T = 2π/2 = π"], "amplituda 3, davr π"),
        W("arccos(−1/2) ni gradusda toping", ["cos x = −½, x ∈ [0°; 180°]", "cos 120° = −½", "x = 120°"], "120°")],
    problems=[
        P("y = 3 sin 2x funksiyaning davri π ning necha barobari?", "1", "T = 2π/ω", "2π/2 = π"),
        P("y = 2 cos(x/2) funksiyaning davri π ning necha barobari?", "4", "T = 2π/(1/2)", "4π"),
        P("arcsin(1/2) necha graduslik?", "30", "", "30°", unit="°"),
        P("arccos(−1/2) necha graduslik?", "120", "", "120°", unit="°"),
        P("arctg(−1) necha graduslik?", "-45", "arctg ∈ (−90°; 90°)", "−45°", unit="°"),
        P("y = 3 sin x + 4 cos x funksiyaning eng katta qiymati?", "5", "√(a² + b²)", "√(9 + 16) = 5")],
    sentence_practice=[ORD("y = 3 sin 2x ning davrini topish tartibi", ["Funksiya y = A sin(ωx), A = 3, ω = 2", "T = 2π/|ω|", "T = 2π/2", "T = π"])],
)

EXTRAS['m6e'] = dict(
    formulas=[F("sin x = a", "x = (−1)ⁿ arcsin a + πn", ""),
              F("cos x = a", "x = ± arccos a + 2πn", ""),
              F("tg x = a", "x = arctg a + πn", ""),
              F("Cheklov", "|a| > 1 da sin x = a, cos x = a yechimsiz", "")],
    worked_examples=[
        W("[0; 2π] da sin x = ½ ni yeching", ["Asosiy yechim x = π/6", "Ikkinchisi: π − π/6 = 5π/6", "Ikkalasi [0; 2π] da"], "π/6 va 5π/6"),
        W("2sin²x − sin x − 1 = 0 ni yeching", ["t = sin x: 2t² − t − 1 = 0", "t = 1 yoki t = −½", "sin x = 1 ⇒ x = π/2 + 2πn", "sin x = −½ ⇒ x = (−1)ⁿ⁺¹ π/6 + πn"], "t = 1; −1/2")],
    problems=[
        P("sin x = 1/2 tenglamaning [0; 2π] dagi ildizlari yig'indisi π ning necha barobari?", "1", "π/6 + 5π/6", "π"),
        P("cos x = 1/2 tenglamaning [0; 2π] dagi ildizlari yig'indisi π ning necha barobari?", "2", "π/3 + 5π/3", "2π"),
        P("sin x = 0 tenglamaning [0; 2π] kesmadagi ildizlari soni?", "3", "0, π, 2π", "3 ta"),
        P("tg x = 1 tenglamaning [0; 2π] dagi ildizlari soni?", "2", "π/4 va 5π/4", "2 ta"),
        P("2sin²x − sin x − 1 = 0 tenglamaning [0; 2π) dagi ildizlari soni?", "3", "sin x = 1 yoki −½", "π/2, 7π/6, 11π/6 — 3 ta"),
        P("cos 2x = 1 tenglamaning [0; 2π] dagi ildizlari soni?", "3", "2x = 2πn", "x = 0, π, 2π — 3 ta")],
    sentence_practice=[ORD("sin x = ½ ([0; 2π] da) ni yechish tartibi", ["Asosiy yechim: x = arcsin ½ = π/6", "Ikkinchi yechim: π − π/6", "x₂ = 5π/6", "Javob: π/6 va 5π/6"])],
)

EXTRAS['m6f'] = dict(
    formulas=[F("Kosinuslar teoremasi", "c² = a² + b² − 2ab cos C", ""),
              F("Sinuslar teoremasi", "a/sin A = b/sin B = c/sin C = 2R", ""),
              F("Yuza", "S = ½ ab sin C", ""),
              F("Burchakni topish", "cos C = (a² + b² − c²)/(2ab)", "")],
    worked_examples=[
        W("a = 5, b = 8, C = 60° bo'lsa, c ni toping", ["c² = 25 + 64 − 2·5·8·cos 60°", "= 89 − 80 · ½ = 89 − 40 = 49", "c = 7"], "7"),
        W("Tomonlari 5, 7, 8 bo'lgan uchburchakda 7 qarshisidagi burchak?", ["cos α = (5² + 8² − 7²)/(2·5·8)", "= (25 + 64 − 49)/80 = 40/80 = ½", "α = 60°"], "60°")],
    problems=[
        P("a = 5, b = 8, C = 60° bo'lsa, c ni toping.", "7", "", "c² = 49"),
        P("Tomonlari 5, 7, 8 bo'lgan uchburchakda 7 qarshisidagi burchak necha graduslik?", "60", "cos = ½", "60°", unit="°"),
        P("a = 6, A = 30° bo'lsa, tashqi aylana radiusi?", "6", "a/sin A = 2R", "6/(2·½) = 6"),
        P("Ikki tomoni 10 va 10, ular orasidagi burchak 30°. Yuzi?", "25", "½ab sin C", "½ · 100 · ½"),
        P("Tomonlari 3, 4, 5 bo'lgan uchburchakning eng katta burchagi?", "90", "5² = 3² + 4²", "90°", unit="°"),
        P("A = 30°, B = 45°, a = 4 bo'lsa, b ning kvadrati nechaga teng?", "32", "b = a sin B / sin A = 4√2", "(4√2)² = 32")],
    sentence_practice=[ORD("Kosinuslar teoremasi bilan c ni topish (a = 5, b = 8, C = 60°)", ["c² = a² + b² − 2ab cos C", "c² = 25 + 64 − 80 · ½", "c² = 49", "c = 7"])],
)
