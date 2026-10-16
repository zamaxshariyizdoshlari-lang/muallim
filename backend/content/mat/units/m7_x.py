# -*- coding: utf-8 -*-
from dsl import F, W, P, ORD

EXTRAS = {}

EXTRAS['m7a'] = dict(
    formulas=[F("n-had", "aₙ = a₁ + (n − 1)d", ""),
              F("Yig'indi", "Sₙ = (a₁ + aₙ)/2 · n", "yoki (2a₁ + (n − 1)d)/2 · n"),
              F("Xossa", "aₙ = (aₙ₋₁ + aₙ₊₁)/2", ""),
              F("Natural sonlar yig'indisi", "1 + 2 + ... + n = n(n + 1)/2", "")],
    worked_examples=[
        W("3, 7, 11, ... progressiyaning 10-hadi va dastlabki 10 had yig'indisini toping", ["a₁ = 3, d = 4", "a₁₀ = 3 + 9·4 = 39", "S₁₀ = (3 + 39)/2 · 10", "S₁₀ = 210"], "a₁₀ = 39; S₁₀ = 210"),
        W("a₃ = 7, a₈ = 22 bo'lsa, d va a₁ ni toping", ["a₈ − a₃ = 5d = 15 ⇒ d = 3", "a₃ = a₁ + 2d ⇒ 7 = a₁ + 6", "a₁ = 1"], "d = 3; a₁ = 1")],
    problems=[
        P("3, 7, 11, ... progressiyaning 10-hadini toping.", "39", "", "3 + 9·4 = 39"),
        P("3, 7, 11, ... progressiyaning dastlabki 10 had yig'indisi?", "210", "", "(3 + 39)/2 · 10 = 210"),
        P("1 + 2 + 3 + ... + 100 yig'indisi?", "5050", "n(n + 1)/2", "100·101/2"),
        P("Arifmetik progressiyada a₃ = 7, a₈ = 22. Ayirma d?", "3", "", "15 : 5 = 3"),
        P("3, 7, 11, ... progressiyaning qaysi hadi 51 ga teng? (tartib raqami)", "13", "3 + (n − 1)·4 = 51", "n = 13"),
        P("Dastlabki 20 ta toq natural son yig'indisi?", "400", "Dastlabki n ta toq son yig'indisi n²", "20² = 400")],
    sentence_practice=[ORD("3, 7, 11, ... ning dastlabki 10 had yig'indisini topish", ["a₁ = 3, d = 4", "a₁₀ = 3 + 9·4 = 39", "S₁₀ = (3 + 39)/2 · 10", "S₁₀ = 210"])],
)

EXTRAS['m7b'] = dict(
    formulas=[F("n-had", "bₙ = b₁ · qⁿ⁻¹", ""),
              F("Yig'indi", "Sₙ = b₁(qⁿ − 1)/(q − 1)", "q ≠ 1"),
              F("Cheksiz kamayuvchi", "S = b₁/(1 − q)", "|q| < 1"),
              F("Murakkab foiz", "S = P(1 + r)ⁿ", "")],
    worked_examples=[
        W("6 + 2 + 2/3 + ... qatorning yig'indisini toping", ["b₁ = 6; q = 2/6 = 1/3", "|q| < 1 — yig'indi mavjud", "S = 6/(1 − 1/3) = 6/(2/3)", "S = 9"], "9"),
        W("0,(3) ni oddiy kasrga aylantiring", ["0,(3) = 0,3 + 0,03 + 0,003 + ...", "b₁ = 0,3; q = 0,1", "S = 0,3/(1 − 0,1) = 0,3/0,9", "= 1/3"], "1/3")],
    problems=[
        P("2, 6, 18, ... progressiyaning 5-hadi?", "162", "2·3⁴", "162"),
        P("2, 6, 18, 54, 162 sonlar yig'indisi?", "242", "S = b₁(qⁿ − 1)/(q − 1)", "2(243 − 1)/2 = 242"),
        P("1 + 1/2 + 1/4 + 1/8 + ... qator yig'indisi?", "2", "S = 1/(1 − ½)", "2"),
        P("6 + 2 + 2/3 + ... qator yig'indisi?", "9", "q = 1/3", "6/(2/3) = 9"),
        P("0,(3) oddiy kasr ko'rinishida (kasr)?", "1/3", "", "0,3/0,9 = 1/3"),
        P("1000 so'm yiliga 10% murakkab foizda 3 yildan keyin necha so'm bo'ladi?", "1331", "1000·1,1³", "1331")],
    sentence_practice=[ORD("6 + 2 + 2/3 + ... yig'indisini topish", ["b₁ = 6, q = 1/3", "|q| < 1 — yig'indi mavjud", "S = b₁/(1 − q) = 6/(2/3)", "S = 9"])],
)

EXTRAS['m7c'] = dict(
    formulas=[F("O'rin almashtirish", "Pₙ = n!", ""),
              F("O'rinlashtirish", "Aₙᵏ = n!/(n − k)!", "tartib muhim"),
              F("Guruhlash", "Cₙᵏ = n!/(k!(n − k)!)", "tartib muhim emas"),
              F("Nyuton binomi", "(a + b)ⁿ = ΣCₙᵏ aⁿ⁻ᵏ bᵏ", "koeffitsientlar yig'indisi 2ⁿ")],
    worked_examples=[
        W("5 nomzoddan 3 lavozimga (tartib bilan) necha usulda saylash mumkin?", ["Tartib muhim — o'rinlashtirish A₅³", "A₅³ = 5!/(5 − 3)! = 120/2", "= 60"], "60"),
        W("10 kishi bir-biri bilan qo'l siqishsa, nechta qo'l siqish bo'ladi?", ["Tartib muhim emas — guruhlash C₁₀²", "C₁₀² = 10·9/2", "= 45"], "45")],
    problems=[
        P("C₅³ ni hisoblang.", "10", "5!/(3!·2!)", "10"),
        P("5! nechaga teng?", "120", "", "120"),
        P("5 nomzoddan 3 lavozimga tartib bilan saylash usullari soni?", "60", "A₅³", "5·4·3 = 60"),
        P("10 kishi bir-biri bilan bir martadan qo'l siqishsa, nechta qo'l siqish bo'ladi?", "45", "C₁₀²", "45"),
        P("4 xonali PIN-kod (har xonada 0–9, takrorlanishi mumkin) nechta?", "10000", "10⁴", "10 000"),
        P("(x + 2)³ yoyilmasida x² oldidagi koeffitsient?", "6", "C₃¹ · 2", "3·2 = 6")],
    sentence_practice=[ORD("5 nomzoddan 3 lavozimga saylash usullari soni", ["Tartib muhim — o'rinlashtirish A₅³", "A₅³ = 5!/(5 − 3)!", "= 120/2", "= 60"])],
)

EXTRAS['m7d'] = dict(
    formulas=[F("Klassik ehtimollik", "P(A) = m/n", ""),
              F("Qarama-qarshi hodisa", "P(Ā) = 1 − P(A)", ""),
              F("Bog'liqsiz hodisalar", "P(AB) = P(A)·P(B)", ""),
              F("Bernulli sxemasi", "Pₙ(k) = Cₙᵏ pᵏ (1 − p)ⁿ⁻ᵏ", "")],
    worked_examples=[
        W("Tanga 5 marta tashlanganda aynan 2 marta gerb tushish ehtimoli?", ["Bernulli: n = 5, k = 2, p = ½", "C₅² = 10", "P = 10 · (½)² · (½)³ = 10/32", "= 5/16"], "5/16"),
        W("Qutida 3 oq, 2 qora shar. Qaytarmasdan ketma-ket ikkita oq shar olish ehtimoli?", ["Birinchi oq: 3/5", "Ikkinchi oq (qolgan 2 oq, 4 shar): 2/4", "P = 3/5 · 2/4", "= 3/10"], "3/10")],
    problems=[
        P("O'yin kubigi tashlanganda juft son tushish ehtimoli (kasr)?", "1/2", "", "3/6"),
        P("Ikki tanga tashlanganda ikkalasi ham gerb tushish ehtimoli (kasr)?", "1/4", "", "½·½"),
        P("Ikki o'yin kubigi tashlanganda ochkolar yig'indisi 7 bo'lish ehtimoli (kasr)?", "1/6", "36 ta natijadan 6 tasi", "6/36 = 1/6"),
        P("3 oq va 2 qora shardan qaytarmasdan ketma-ket ikkita oq shar olish ehtimoli (kasr)?", "3/10", "", "3/5 · 2/4"),
        P("Tanga 5 marta tashlanganda aynan 2 marta gerb tushish ehtimoli (kasr)?", "5/16", "", "10/32"),
        P("3 ta tanga tashlanganda kamida bitta gerb tushish ehtimoli (kasr)?", "7/8", "1 − P(hech gerb yo'q)", "1 − 1/8")],
    sentence_practice=[ORD("Ketma-ket ikkita oq shar olish ehtimoli (3 oq, 2 qora)", ["Birinchi shar oq: 3/5", "Ikkinchi shar oq: 2/4", "P = 3/5 · 2/4", "P = 3/10"])],
)

EXTRAS['m7e'] = dict(
    formulas=[F("O'rta arifmetik", "x̄ = Σxᵢ / n", ""),
              F("Mediana", "tartiblangan qatorning o'rtasi", "juft soni — ikki o'rtadagining o'rtachasi"),
              F("Dispersiya", "σ² = Σ(xᵢ − x̄)²/n", "σ = √σ²"),
              F("Normal taqsimot", "x̄ ± σ → 68%; ±2σ → 95%; ±3σ → 99,7%", "")],
    worked_examples=[
        W("2, 3, 3, 5, 7 sonlarining o'rtasi, medianasi va modasini toping", ["O'rta: (2 + 3 + 3 + 5 + 7)/5 = 20/5 = 4", "Mediana: o'rtadagi son = 3", "Moda: eng ko'p uchragan = 3"], "4; 3; 3"),
        W("2, 4, 6 sonlarning dispersiyasini toping", ["x̄ = 4", "Chetlanishlar kvadratlari: 4, 0, 4", "σ² = (4 + 0 + 4)/3", "σ² = 8/3"], "8/3")],
    problems=[
        P("2, 3, 3, 5, 7 sonlarining o'rta arifmetigi?", "4", "", "20/5 = 4"),
        P("1, 2, 3, 4 sonlarining medianasi?", "2,5", "Ikki o'rtadagining o'rtachasi", "(2 + 3)/2"),
        P("2, 3, 3, 5, 7 sonlarining modasi?", "3", "Eng ko'p uchragani", "3"),
        P("2, 4, 6 sonlarining dispersiyasi (kasr)?", "8/3", "", "(4 + 0 + 4)/3"),
        P("Maoshlar: 100, 100, 100, 100, 1000. O'rta arifmetik?", "280", "", "1400/5 = 280"),
        P("5 ta sonning o'rtasi 20 bo'lsa, ularning yig'indisi?", "100", "", "5 · 20 = 100")],
    sentence_practice=[ORD("2, 4, 6 ning dispersiyasini topish tartibi", ["O'rta: x̄ = 4", "Chetlanish kvadratlari: 4, 0, 4", "σ² = (4 + 0 + 4)/3", "σ² = 8/3"])],
)

EXTRAS['m7f'] = dict(
    formulas=[F("Birlashma elementlari", "|A ∪ B| = |A| + |B| − |A ∩ B|", ""),
              F("Qism to'plamlar soni", "2ⁿ", "n elementli to'plam uchun"),
              F("De Morgan", "(A ∪ B)‾ = Ā ∩ B̄; (A ∩ B)‾ = Ā ∪ B̄", ""),
              F("Implikatsiya", "A ⇒ B faqat A chin, B yolg'on bo'lganda yolg'on", "")],
    worked_examples=[
        W("Sinfda 30 o'quvchi: 18 tasi matematika, 15 tasi fizika to'garagida, 5 tasi ikkalasida. Hech qaysisida qatnashmaydigan nechta?", ["|M ∪ F| = 18 + 15 − 5 = 28", "Hech qaysisida: 30 − 28 = 2"], "2"),
        W("3 elementli to'plamning nechta qism to'plami bor?", ["Formula: 2ⁿ", "2³ = 8"], "8")],
    problems=[
        P("4 elementli to'plamning qism to'plamlari soni?", "16", "2ⁿ", "2⁴ = 16"),
        P("A = {1,2,3,4}, B = {3,4,5} bo'lsa, A ∪ B nechta element saqlaydi?", "5", "", "{1,2,3,4,5}"),
        P("Sinfda 30 o'quvchi: 18 matematika, 15 fizika, 5 tasi ikkalasida. Hech qaysisida qatnashmaydiganlar soni?", "2", "", "30 − 28 = 2"),
        P("1 dan 100 gacha 2 ga yoki 3 ga bo'linadigan sonlar nechta?", "67", "50 + 33 − 16", "67"),
        P("n elementli to'plamning qism to'plamlari 64 ta. n nechaga teng?", "6", "2ⁿ = 64", "6"),
        P("|A| = 10, |B| = 7, |A ∩ B| = 3 bo'lsa, |A ∪ B|?", "14", "", "10 + 7 − 3 = 14")],
    sentence_practice=[ORD("Hech qaysi to'garakka qatnashmaydiganlar sonini topish", ["|M ∪ F| = |M| + |F| − |M ∩ F|", "|M ∪ F| = 18 + 15 − 5 = 28", "Hammasi 30 ta", "30 − 28 = 2"])],
)
