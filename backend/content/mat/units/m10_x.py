# -*- coding: utf-8 -*-
from dsl import F, W, P, ORD

EXTRAS = {}

EXTRAS['m10a'] = dict(
    formulas=[F("Kompleks son", "z = a + bi, i² = −1", ""),
              F("Modul va qo'shma", "|z| = √(a² + b²); z̄ = a − bi", "z·z̄ = |z|²"),
              F("Ko'paytirish", "(a + bi)(c + di) = (ac − bd) + (ad + bc)i", ""),
              F("Muavr", "zⁿ = rⁿ(cos nφ + i sin nφ)", "")],
    worked_examples=[
        W("(2 + 3i)(1 − i) ni hisoblang", ["Ko'paytiramiz: 2 − 2i + 3i − 3i²", "i² = −1 ⇒ −3i² = +3", "(2 + 3) + (−2 + 3)i", "5 + i"], "5 + i"),
        W("x² − 2x + 5 = 0 ni yeching", ["D = 4 − 20 = −16", "√D = 4i", "x = (2 ± 4i)/2", "x = 1 ± 2i"], "1 ± 2i")],
    problems=[
        P("(2 + 3i)(1 − i) ko'paytmaning haqiqiy qismi?", "5", "", "5 + i"),
        P("|3 + 4i| nechaga teng?", "5", "", "√(9 + 16)"),
        P("i²⁰²⁴ nechaga teng?", "1", "i⁴ = 1", "2024 = 4·506"),
        P("(1 + i)² = a + bi bo'lsa, b nechaga teng?", "2", "1 + 2i + i²", "2i"),
        P("(1 + i)⁸ nechaga teng?", "16", "(1+i)² = 2i", "(2i)⁴ = 16"),
        P("x² − 2x + 5 = 0 ildizlarining mavhum qismi (musbat qiymat)?", "2", "x = 1 ± 2i", "2")],
    sentence_practice=[ORD("(2 + 3i)(1 − i) ni hisoblash", ["2·1 − 2i + 3i·1 − 3i·i", "2 − 2i + 3i − 3i²", "i² = −1: 2 + i + 3", "5 + i"])],
)

EXTRAS['m10b'] = dict(
    formulas=[F("2×2 determinant", "det [[a, b], [c, d]] = ad − bc", ""),
              F("Ko'paytma", "cᵢⱼ = Σ aᵢₗ bₗⱼ", "AB ≠ BA"),
              F("det(AB)", "det A · det B", ""),
              F("Teskari 2×2", "A⁻¹ = 1/(ad − bc) · [[d, −b], [−c, a]]", "det ≠ 0")],
    worked_examples=[
        W("[[1,2],[3,4]] · [[0,1],[1,0]] ni hisoblang", ["c₁₁ = 1·0 + 2·1 = 2", "c₁₂ = 1·1 + 2·0 = 1", "c₂₁ = 3·0 + 4·1 = 4; c₂₂ = 3·1 + 4·0 = 3", "[[2, 1], [4, 3]]"], "[[2,1],[4,3]]"),
        W("A = [[2,1],[1,1]] ning teskari matritsasini toping", ["det A = 2·1 − 1·1 = 1", "A⁻¹ = (1/1)·[[1, −1], [−1, 2]]", "A⁻¹ = [[1, −1], [−1, 2]]"], "[[1,−1],[−1,2]]")],
    problems=[
        P("det [[3, 2], [1, 4]] nechaga teng?", "10", "ad − bc", "12 − 2"),
        P("det [[2, 1], [1, 1]] nechaga teng?", "1", "", "2 − 1"),
        P("[[1,2],[3,4]] · [[0,1],[1,0]] ko'paytmada 2-qator 1-ustun elementi?", "4", "3·0 + 4·1", "4"),
        P("det [[1,0,0],[0,2,0],[0,0,3]] nechaga teng?", "6", "Diagonal matritsa", "1·2·3"),
        P("det A = 2, det B = 5 bo'lsa det(AB) nechaga teng?", "10", "", "2 · 5"),
        P("A = [[2,1],[1,1]] ning teskari matritsasida 2-qator 2-ustun elementi?", "2", "", "[[1,−1],[−1,2]]")],
    sentence_practice=[ORD("2×2 matritsa teskarisini topish tartibi (A = [[2,1],[1,1]])", ["det A = 2·1 − 1·1 = 1", "det A ≠ 0 — teskari bor", "A⁻¹ = (1/det)·[[d, −b], [−c, a]]", "A⁻¹ = [[1, −1], [−1, 2]]"])],
)

EXTRAS['m10c'] = dict(
    formulas=[F("Matritsa shakli", "AX = B", ""),
              F("Kramer", "xᵢ = Δᵢ/Δ", "Δ ≠ 0"),
              F("Gauss", "uchburchak shaklga keltirib, pastdan yuqoriga", ""),
              F("Kroneker–Kapelli", "rang A = rang [A|B] — birgalikda", "")],
    worked_examples=[
        W("{2x + y = 5; x − y = 1} ni Kramer usuli bilan yeching", ["Δ = 2·(−1) − 1·1 = −3", "Δx = 5·(−1) − 1·1 = −6 ⇒ x = −6/−3 = 2", "Δy = 2·1 − 5·1 = −3 ⇒ y = 1"], "(2; 1)"),
        W("{x + y + z = 6; 2y + z = 5; z = 1} ni yeching", ["Pastdan: z = 1", "2y + 1 = 5 ⇒ y = 2", "x + 2 + 1 = 6 ⇒ x = 3"], "(3; 2; 1)")],
    problems=[
        P("{2x + y = 5; x − y = 1} sistemada x nechaga teng?", "2", "Qo'shing.", "3x = 6"),
        P("{2x + y = 5; x − y = 1} sistema determinanti Δ nechaga teng?", "-3", "2·(−1) − 1·1", "−3"),
        P("{x + y + z = 6; 2y + z = 5; z = 1} sistemada x nechaga teng?", "3", "", "3"),
        P("{x + y = 3; 2x + 2y = 6} sistema nechta erkin parametrga ega?", "1", "Ikkinchi tenglama birinchisining natijasi.", "1"),
        P("{x + y = 3; 2x + 2y = 7} sistema nechta yechimga ega?", "0", "2(x + y) = 7 ⇒ 6 = 7", "yechim yo'q"),
        P("{x + 2y = 5; 3x − y = 1} sistemada y nechaga teng?", "2", "", "x = 1, y = 2")],
    sentence_practice=[ORD("{x + y + z = 6; 2y + z = 5; z = 1} ni yechish tartibi", ["z = 1 (oxirgi tenglamadan)", "2y + 1 = 5 ⇒ y = 2", "x + 2 + 1 = 6", "x = 3"])],
)

EXTRAS['m10d'] = dict(
    formulas=[F("O'zgaruvchilari ajraladigan", "y′ = f(x)g(y) ⇒ dy/g(y) = f(x)dx", ""),
              F("Eksponensial o'sish", "N = N₀e^(kt)", "dN/dt = kN"),
              F("2-tartibli bir jinsli", "y″ + py′ + qy = 0 ⇒ k² + pk + q = 0", ""),
              F("Koshi masalasi", "tenglama + boshlang'ich shart", "")],
    worked_examples=[
        W("y′ = y, y(0) = 3 ni yeching", ["dy/y = dx ⇒ ln|y| = x + C", "y = Ceˣ", "y(0) = C = 3", "y = 3eˣ"], "y = 3eˣ"),
        W("y″ − 3y′ + 2y = 0 ni yeching", ["Xarakteristik: k² − 3k + 2 = 0", "k = 1, k = 2", "y = C₁eˣ + C₂e^(2x)"], "C₁eˣ + C₂e^(2x)")],
    problems=[
        P("y′ = y, y(0) = 3 bo'lsa, y = Ceˣ dagi C nechaga teng?", "3", "", "y(0) = C"),
        P("y′ = 2x, y(0) = 3 bo'lsa y(2) nechaga teng?", "7", "y = x² + 3", "4 + 3"),
        P("y″ − 3y′ + 2y = 0 xarakteristik tenglamasi ildizlarining yig'indisi?", "3", "k² − 3k + 2 = 0", "1 + 2"),
        P("Bakteriyalar soni har soatda 2 barobar oshadi. Boshida 100 ta bo'lsa, 3 soatdan keyin nechta?", "800", "N = 100·2ᵗ", "100·8"),
        P("y″ + y = 0 ning xarakteristik ildizlari ±i. Yechimdagi chastota ω nechaga teng?", "1", "k = ±iω", "1"),
        P("dN/dt = kN tenglamada N(t) = N₀e^(kt). Agar k = 0 bo'lsa N(5) = ? (N₀ = 7)", "7", "e⁰ = 1", "7")],
    sentence_practice=[ORD("y′ = y, y(0) = 3 ni yechish tartibi", ["dy/y = dx", "ln|y| = x + C", "y = Ceˣ", "y(0) = 3 ⇒ y = 3eˣ"])],
)

EXTRAS['m10e'] = dict(
    formulas=[F("Evklid algoritmi", "EKUB(a, b) = EKUB(b, a mod b)", ""),
              F("Taqqoslama", "a ≡ b (mod m) ⇔ m | a − b", ""),
              F("Ferma", "a^(p−1) ≡ 1 (mod p)", "p tub, p ∤ a"),
              F("RSA", "n = pq; φ = (p−1)(q−1); ed ≡ 1 (mod φ)", "c = mᵉ mod n; m = cᵈ mod n")],
    worked_examples=[
        W("EKUB(1071; 462) ni Evklid algoritmi bilan toping", ["1071 = 2·462 + 147", "462 = 3·147 + 21", "147 = 7·21 + 0", "EKUB = 21"], "21"),
        W("3¹⁰⁰ mod 7 ni toping", ["Ferma: 3⁶ ≡ 1 (mod 7)", "100 = 6·16 + 4", "3¹⁰⁰ ≡ 3⁴ = 81", "81 mod 7 = 4"], "4")],
    problems=[
        P("EKUB(1071; 462) nechaga teng?", "21", "", "21"),
        P("3¹⁰⁰ ni 7 ga bo'lgandagi qoldiq?", "4", "3⁶ ≡ 1 (mod 7)", "3⁴ = 81 ≡ 4"),
        P("φ(12) nechaga teng?", "4", "1, 5, 7, 11", "4"),
        P("2¹⁰ ni 11 ga bo'lgandagi qoldiq?", "1", "Ferma kichik teoremasi", "1"),
        P("7²⁰²⁴ ning oxirgi raqami?", "1", "7 ning darajalari oxirgi raqami davri 4", "2024 : 4 = 506 ⇒ 1"),
        P("RSA: p = 3, q = 11, e = 3. Yopiq kalit d nechaga teng?", "7", "φ = 20; ed ≡ 1 (mod 20)", "3·7 = 21 ≡ 1 (mod 20)")],
    sentence_practice=[ORD("EKUB(1071; 462) ni topish tartibi", ["1071 = 2·462 + 147", "462 = 3·147 + 21", "147 = 7·21 + 0", "EKUB = 21"])],
)
