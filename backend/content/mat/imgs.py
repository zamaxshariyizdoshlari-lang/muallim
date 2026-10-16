# -*- coding: utf-8 -*-
import sys, os, math
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from tarix_svg import *

I = {}
add = adder1('mt', I)
C1, C2, C3 = '#ef4444', '#2563eb', '#16a34a'


def R(*a):
    return box(*a)


# ---------------- 1-bo'lim: arifmetika
add('m1a', 'Natural sonlar va amallar', tree('Natural sonlar', 'N = {1, 2, 3, ...}', [('Qo\'shish', 'a + b = b + a'), ('Ko\'paytirish', 'a·b = b·a'), ('Taqsimot', 'a(b+c) = ab + ac'), ('Bo\'lish', 'a : b ≠ b : a')]))
o = [ARROW_DEF, T(360, 60, 'EKUB(48, 18) — Evklid algoritmi', 16, INK, weight='700')]
rows = [('48 = 2·18 + 12', '#60a5fa'), ('18 = 1·12 + 6', '#34d399'), ('12 = 2·6 + 0', '#fbbf24')]
for i, (t, c) in enumerate(rows):
    o.append(box(190, 100 + i * 70, 340, 52, tint(c, 0.3), c, rx=10, sw=2))
    o.append(T(360, 133 + i * 70, t, 17, INK, weight='700'))
    if i < 2:
        o.append(line(360, 152 + i * 70, 360, 170 + i * 70, '#334155', 2, arrow=True))
o.append(T(360, 340, 'Oxirgi nolga teng bo\'lmagan qoldiq 6 — EKUB(48, 18) = 6', 14, C3, weight='700'))
add('m1b', 'EKUB — Evklid algoritmi', svg('EKUB topish', ''.join(o)))
o = [T(360, 60, '3/4 kasrni tasvirlash', 16, INK, weight='700')]
for i in range(4):
    o.append(box(120 + i * 120, 120, 120, 80, '#93c5fd' if i < 3 else '#f1f5f9', '#1e3a8a', rx=0, sw=2))
o += [T(360, 240, '3/4 = 4 qismdan 3 tasi', 15, INK), T(360, 290, '3/4 = 6/8 = 9/12  (kasrning asosiy xossasi)', 14, MUTED),
      T(360, 335, 'Qo\'shish: 1/4 + 2/4 = 3/4 (maxraj o\'zgarmaydi)', 14, INK)]
add('m1c', 'Oddiy kasrlar', svg('Oddiy kasrlar', ''.join(o)))
o = [T(360, 60, '3 452,718 sonining xonalari', 16, INK, weight='700')]
cells = [('3', 'minglik'), ('4', 'yuzlik'), ('5', 'o\'nlik'), ('2', 'birlik'), (',', ''), ('7', 'o\'ndan bir'), ('1', 'yuzdan bir'), ('8', 'mingdan bir')]
x = 60
for d, nm in cells:
    w = 50 if d == ',' else 100
    if d != ',':
        o.append(box(x, 120, w - 8, 70, tint('#60a5fa' if x < 400 else '#f87171', .3), '#334155', rx=8, sw=1.5))
        o.append(T(x + w / 2 - 4, 168, d, 32, INK, weight='800'))
        o.append(T(x + w / 2 - 4, 215, nm, 11, MUTED))
    else:
        o.append(T(x + 14, 168, ',', 36, INK, weight='800'))
    x += w - 8 if d != ',' else 30
add('m1d', 'O\'nli kasrlar', svg('O\'nli kasrlar', ''.join(o)))
o = [T(360, 60, 'Nisbat va foiz', 16, INK, weight='700'), box(60, 100, 600, 40, '#e2e8f0', '#334155', rx=6)]
o += [box(60, 100, 150, 40, '#60a5fa', rx=6), T(135, 126, '25%', 16, '#fff', weight='800'), T(360, 126, '100% = butun', 14, INK),
      T(360, 190, '200 ning 25% i = 200 · 0,25 = 50', 15, INK, weight='700'),
      T(360, 235, 'Proporsiya: a : b = c : d  ⇒  a·d = b·c', 15, INK),
      T(360, 285, 'Misol: 3 : 5 = 12 : x  ⇒  x = 20', 15, C3, weight='700')]
add('m1e', 'Nisbat, proporsiya, foiz', svg('Nisbat va foiz', ''.join(o)))
p = P((-5, 5), (-1, 1), (60, 150, 660, 250))
o = [line(60, 200, 660, 200, '#334155', 3, arrow=True)]
for v in range(-5, 6):
    x = 60 + (v + 5) * 60
    o += [line(x, 190, x, 210, '#334155', 2), T(x, 232, v, 13, INK)]
o += [circle(60 + (-3 + 5) * 60, 200, 7, C1), circle(60 + (2 + 5) * 60, 200, 7, C2), T(180, 175, '-3', 14, C1, weight='700'), T(420, 175, '2', 14, C2, weight='700'),
      T(360, 290, '|-3| = 3,   |2| = 2   (modul — 0 gacha masofa)', 14, INK),
      T(360, 325, 'Manfiy son 0 dan chapda, musbat son o\'ngda', 13, MUTED)]
add('m1f', 'Butun sonlar va modul', svg('Sonlar o\'qi', ''.join(o)))

# ---------------- 2-bo'lim: algebra
o = [T(360, 56, '(a + b)² = a² + 2ab + b²', 17, INK, weight='700'),
     box(160, 90, 200, 200, '#bfdbfe', '#1e3a8a', rx=0, sw=2), box(360, 90, 120, 200, '#fde68a', '#78350f', rx=0, sw=2),
     box(160, 290, 200, 80, '#fde68a', '#78350f', rx=0, sw=2), box(360, 290, 120, 80, '#bbf7d0', '#14532d', rx=0, sw=2),
     T(260, 195, 'a²', 26, INK, weight='800'), T(420, 195, 'ab', 22, INK, weight='800'), T(260, 337, 'ab', 22, INK, weight='800'), T(420, 337, 'b²', 22, INK, weight='800'),
     T(260, 82, 'a', 14, MUTED), T(420, 82, 'b', 14, MUTED)]
add('m2a', 'Qisqa ko\'paytirish formulasi', svg('Yuza orqali isbot', ''.join(o)))
add('m2b', 'Ko\'paytuvchilarga ajratish', tree('Ko\'paytuvchilarga ajratish', 'Usullar', [('Umumiy ko\'paytuvchi', 'ax + ay = a(x + y)'), ('Guruhlash', 'ax + ay + bx + by = (a+b)(x+y)'), ('Formulalar', 'a² − b² = (a−b)(a+b)')]))
p = P((-3, 5), (-5, 9))
p.axes().curve(lambda x: 2 * x + 1, C2).pt(2, 5, '(2; 5)', C1).pt(-0.5, 0, '(−0,5; 0)', C3, dy=18).text(2.2, 8, 'y = 2x + 1', 14, C2, weight='700')
add('m2c', 'Chiziqli tenglama grafigi', p.done('Chiziqli funksiya y = 2x + 1'))
o = [T(360, 56, 'Tengsizlik: x ≥ 2 va x < 6  →  [2; 6)', 16, INK, weight='700'), line(60, 200, 660, 200, '#334155', 3, arrow=True), box(210, 190, 300, 20, '#93c5fd', rx=4)]
for v in range(0, 9):
    x = 60 + v * 70
    o += [line(x, 192, x, 208, '#334155', 2), T(x, 232, v, 13, INK)]
o += [circle(60 + 2 * 70, 200, 8, '#1e3a8a'), circle(60 + 6 * 70, 200, 8, '#fff', '#1e3a8a', 3), T(360, 290, '● — chegara kiradi (≥ yoki ≤)', 14, INK), T(360, 320, '○ — chegara kirmaydi (> yoki <)', 14, INK)]
add('m2d', 'Tengsizlik oraliqlari', svg('Sonli oraliq', ''.join(o)))
p = P((-1, 7), (-1, 7))
p.axes().curve(lambda x: 6 - x, C2).curve(lambda x: 2 * x, C1).pt(2, 4, '(2; 4) — yechim', C3, dx=10).text(5.6, 1.5, 'x + y = 6', 13, C2, weight='700').text(3.2, 6.6, 'y = 2x', 13, C1, weight='700')
add('m2e', 'Tenglamalar sistemasi', p.done('Sistema yechimi — chiziqlar kesishishi'))
add('m2f', 'Algebraik kasrlar', flow('Kasrni soddalashtirish', [('Surat', 'ko\'paytuvchilarga'), ('Maxraj', 'ko\'paytuvchilarga'), ('Qisqartirish', 'umumiy ifoda'), ('Natija', 'sodda kasr'), ('Tekshirish', 'maxraj ≠ 0')]))

# ---------------- 3-bo'lim: funksiyalar
p = P((-2, 6), (-4, 6))
f = lambda x: x * x - 4 * x + 3
p.axes().curve(f, C2).pt(1, 0, 'x₁ = 1', C1, dy=20, dx=-30).pt(3, 0, 'x₂ = 3', C1, dy=20).pt(2, -1, 'uchi (2; −1)', C3, dy=22).text(4.0, 5.5, 'y = x² − 4x + 3', 13, C2, weight='700')
add('m3a', 'Kvadrat tenglama ildizlari', p.done('Parabola va uning ildizlari'))
p = P((-4, 4), (-4, 4))
p.axes().curve(lambda x: x, C2).curve(lambda x: -x + 1, C1).curve(lambda x: 2, C3).text(2.6, 3.2, 'y = x', 12, C2, weight='700').text(-3.5, 3.6, 'y = −x + 1', 12, C1, weight='700').text(2.2, 2.4, 'y = 2', 12, C3, weight='700')
add('m3b', 'Chiziqli funksiyalar', p.done('Chiziqli funksiya turlari'))
p = P((-4, 4), (-2, 8))
p.axes().curve(lambda x: x * x, C2).curve(lambda x: -x * x + 4, C1).pt(0, 0, '(0; 0)', C2, dx=-45, dy=18).pt(0, 4, '(0; 4)', C1, dx=10, dy=-4).text(2.2, 6.5, 'y = x² (a>0, shoxlar yuqoriga)', 12, C2, weight='700').text(0.4, -1.0, 'y = −x² + 4 (a<0, pastga)', 12, C1, weight='700')
add('m3c', 'Kvadrat funksiya', p.done('Parabola: a ishorasi'))
p = P((-4, 4), (-1, 9))
p.axes().curve(lambda x: 2 ** x, C2).curve(lambda x: 0.5 ** x, C1).pt(0, 1, '(0; 1)', C3).text(2.6, 7.0, 'y = 2ˣ (o\'suvchi)', 12, C2, weight='700').text(-3.8, 7.6, 'y = (½)ˣ (kamayuvchi)', 12, C1, weight='700')
add('m3d', 'Ko\'rsatkichli funksiya', p.done('Ko\'rsatkichli funksiya'))
p = P((-3, 8), (-3, 8))
p.axes().curve(lambda x: x, '#94a3b8', sw=2).curve(lambda x: 2 ** x, C2, x0=-3, x1=3).curve(lambda x: math.log2(x) if x > 0 else None, C1, x0=0.01, x1=8).pt(1, 0, '(1; 0)', C3, dy=18).text(0.2, 7.2, 'y = 2ˣ', 12, C2, weight='700').text(5.2, 3.4, 'y = log₂x', 12, C1, weight='700')
add('m3e', 'Logarifm — ko\'rsatkichli funksiyaning teskarisi', p.done('y = 2ˣ va y = log₂x (y = x ga nisbatan simmetrik)'))
p = P((-5, 5), (-1, 5))
p.axes().curve(abs, C2).curve(lambda x: 1 / x if abs(x) > 0.2 else None, C1, n=300).text(-4.8, 4.6, 'y = |x|', 13, C2, weight='700').text(2.8, 3.2, 'y = 1/x (kasr-ratsional)', 12, C1, weight='700')
add('m3f', 'Modulli va kasr-ratsional funksiyalar', p.done('Modul va kasr-ratsional funksiyalar'))

# ---------------- 4-bo'lim: planimetriya
o = [T(360, 56, 'Asosiy geometrik shakllar', 16, INK, weight='700')]
for i, (nm, f) in enumerate([('Nuqta', 0), ('To\'g\'ri chiziq', 1), ('Nur', 2), ('Kesma', 3)]):
    y = 110 + i * 70
    o.append(T(130, y + 5, nm, 15, INK, anchor='end', weight='700'))
    if f == 0:
        o.append(circle(330, y, 6, C1))
    elif f == 1:
        o.append(line(200, y, 640, y, C2, 3, arrow=True))
    elif f == 2:
        o += [circle(250, y, 6, C1), line(250, y, 640, y, C2, 3, arrow=True)]
    else:
        o += [circle(250, y, 6, C1), circle(550, y, 6, C1), line(250, y, 550, y, C2, 3)]
add('m4a', 'Asosiy tushunchalar', svg('Asosiy geometrik tushunchalar', ''.join(o)))
o = [T(360, 56, 'Uchburchak turlari', 16, INK, weight='700')]
tris = [('Teng tomonli', [(80, 300), (200, 300), (140, 196)]), ('Teng yonli', [(300, 300), (420, 300), (360, 170)]), ('To\'g\'ri burchakli', [(520, 300), (520, 180), (650, 300)])]
for nm, pts in tris:
    o.append(poly(pts, '#dbeafe', '#1e3a8a', 2.5))
    o.append(T(sum(a for a, _ in pts) / 3, 335, nm, 13, INK, weight='700'))
o.append(box(520, 288, 12, 12, 'none', '#1e3a8a', rx=0, sw=2))
o.append(T(360, 375, 'Burchaklar yig\'indisi: ∠A + ∠B + ∠C = 180°', 14, C3, weight='700'))
add('m4b', 'Uchburchaklar', svg('Uchburchaklar', ''.join(o)))
o = [T(360, 56, 'Pifagor teoremasi: a² + b² = c²', 17, INK, weight='700'),
     poly([(260, 300), (260, 180), (400, 300)], '#fef3c7', '#78350f', 2.5),
     box(260, 288, 12, 12, 'none', '#78350f', rx=0, sw=2),
     box(140, 180, 120, 120, '#bfdbfe', '#1e3a8a', rx=0, sw=2), T(200, 245, 'a²', 22, INK, weight='800'),
     box(260, 300, 140, 100, '#bbf7d0', '#14532d', rx=0, sw=2), T(330, 358, 'b²', 22, INK, weight='800'),
     poly([(260, 180), (400, 300), (480, 200), (340, 80)], '#fecaca', '#7f1d1d', 2), T(380, 190, 'c²', 22, INK, weight='800'),
     T(500, 320, '3² + 4² = 5²', 16, C3, weight='700')]
add('m4c', 'Pifagor teoremasi', svg('Pifagor teoremasi', ''.join(o)))
add('m4d', 'To\'rtburchaklar', tree('To\'rtburchaklar', 'To\'rtburchak', [('Parallelogram', 'Qarama-qarshi tomonlar parallel'), ('To\'g\'ri to\'rtburchak', 'Barcha burchaklar 90°'), ('Romb', 'Barcha tomonlar teng'), ('Kvadrat', 'To\'g\'ri to\'rtburchak va romb')]))
o = [T(360, 56, 'Aylana elementlari', 16, INK, weight='700'), circle(300, 215, 130, '#eff6ff', '#1e3a8a', 3), circle(300, 215, 5, C1),
     line(300, 215, 430, 215, C1, 3), T(365, 205, 'r', 15, C1, weight='700'), line(170, 215, 430, 215, '#94a3b8', 1.5, '5 4'),
     line(215, 125, 395, 125, C2, 3), T(305, 115, 'vatar', 13, C2, weight='700'), line(430, 80, 430, 350, C3, 3), T(450, 215, 'urinma', 13, C3, anchor='start', weight='700'),
     T(520, 120, 'C = 2πr', 16, INK, anchor='start', weight='700'), T(520, 160, 'S = πr²', 16, INK, anchor='start', weight='700'), T(520, 200, 'Urinma ⟂ radius', 14, MUTED, anchor='start')]
add('m4e', 'Aylana va doira', svg('Aylana va doira', ''.join(o)))
o = [T(360, 56, 'O\'xshash uchburchaklar: k = 2', 16, INK, weight='700'), poly([(70, 330), (210, 330), (140, 230)], '#bfdbfe', '#1e3a8a', 2.5), poly([(280, 330), (560, 330), (420, 130)], '#bbf7d0', '#14532d', 2.5),
     T(140, 355, 'a, b, c', 13, INK), T(420, 355, '2a, 2b, 2c', 13, INK), T(360, 385, 'Yuzalar nisbati: k² = 4', 14, C3, weight='700')]
add('m4f', 'O\'xshashlik va yuza', svg('O\'xshashlik', ''.join(o)))

# ---------------- 5-bo'lim: stereometriya
o = [T(360, 56, 'Fazoda to\'g\'ri chiziq va tekislik', 16, INK, weight='700'), poly([(120, 300), (480, 300), (560, 210), (200, 210)], '#dbeafe', '#1e3a8a', 2.5), line(340, 255, 340, 90, C1, 3, arrow=True),
     circle(340, 255, 5, C1), T(360, 120, 'a ⟂ α', 15, C1, anchor='start', weight='700'), T(500, 320, 'α — tekislik', 13, MUTED), T(360, 360, 'Chiziq tekislikdagi ikki kesishuvchi chiziqqa perpendikulyar bo\'lsa, tekislikka perpendikulyar', 12, MUTED)]
add('m5a', 'Chiziq va tekislik', svg('Perpendikulyarlik', ''.join(o)))
o = [T(360, 56, 'Prizma va piramida', 16, INK, weight='700'),
     poly([(100, 320), (240, 320), (300, 280), (160, 280)], '#bfdbfe', '#1e3a8a', 2), poly([(100, 190), (240, 190), (300, 150), (160, 150)], '#dbeafe', '#1e3a8a', 2),
     line(100, 320, 100, 190, '#1e3a8a', 2), line(240, 320, 240, 190, '#1e3a8a', 2), line(300, 280, 300, 150, '#1e3a8a', 2), line(160, 280, 160, 150, '#1e3a8a', 2, '4 4'),
     T(200, 360, 'V = S · h', 15, INK, weight='700'),
     poly([(420, 320), (600, 320), (660, 280), (480, 280)], '#bbf7d0', '#14532d', 2), line(420, 320, 540, 110, '#14532d', 2), line(600, 320, 540, 110, '#14532d', 2), line(660, 280, 540, 110, '#14532d', 2), line(480, 280, 540, 110, '#14532d', 2, '4 4'),
     T(540, 360, 'V = ⅓ S · h', 15, INK, weight='700')]
add('m5b', 'Prizma va piramida', svg('Prizma va piramida', ''.join(o)))
o = [T(360, 56, 'Silindr, konus, shar', 16, INK, weight='700')]
o += ['<ellipse cx="130" cy="150" rx="70" ry="22" fill="#dbeafe" stroke="#1e3a8a" stroke-width="2.5"/>', line(60, 150, 60, 290, '#1e3a8a', 2.5), line(200, 150, 200, 290, '#1e3a8a', 2.5),
      '<path d="M60 290 A70 22 0 0 0 200 290" fill="#bfdbfe" stroke="#1e3a8a" stroke-width="2.5"/>', T(130, 340, 'V = πr²h', 15, INK, weight='700')]
o += ['<ellipse cx="360" cy="290" rx="70" ry="22" fill="#bbf7d0" stroke="#14532d" stroke-width="2.5"/>', line(290, 290, 360, 100, '#14532d', 2.5), line(430, 290, 360, 100, '#14532d', 2.5), T(360, 340, 'V = ⅓πr²h', 15, INK, weight='700')]
o += [circle(580, 200, 90, '#fef3c7', '#78350f', 2.5), '<ellipse cx="580" cy="200" rx="90" ry="26" fill="none" stroke="#78350f" stroke-width="1.5" stroke-dasharray="5 4"/>', T(580, 340, 'V = ⁴⁄₃πr³', 15, INK, weight='700')]
add('m5c', 'Aylanish jismlari', svg('Aylanish jismlari', ''.join(o)))
add('m5d', 'Jismlar hajmi va sirti', compare('Hajm formulalari', 'Ko\'pyoqlar', ['Kub: V = a³', 'Prizma: V = S·h', 'Piramida: V = ⅓S·h'], 'Aylanish jismlari', ['Silindr: V = πr²h', 'Konus: V = ⅓πr²h', 'Shar: V = ⁴⁄₃πr³']))

# ---------------- 6-bo'lim: trigonometriya
o = [T(360, 56, 'To\'g\'ri burchakli uchburchakda', 16, INK, weight='700'), poly([(130, 320), (130, 120), (460, 320)], '#fef3c7', '#78350f', 2.5), box(130, 308, 12, 12, 'none', '#78350f', rx=0, sw=2),
     T(110, 225, 'qarshi katet', 13, C1, anchor='end', weight='700'), T(295, 345, 'yondosh katet', 13, C2, weight='700'), T(330, 200, 'gipotenuza', 13, C3, weight='700'), T(420, 308, 'α', 20, INK, weight='800'),
     T(560, 150, 'sin α = qarshi / gip.', 14, INK, anchor='start', weight='700'), T(560, 190, 'cos α = yondosh / gip.', 14, INK, anchor='start', weight='700'), T(560, 230, 'tg α = qarshi / yondosh', 14, INK, anchor='start', weight='700')]
add('m6a', 'Sin, cos, tg', svg('Trigonometrik nisbatlar', ''.join(o)))
cx, cy, r = 360, 215, 140
o = [T(360, 40, 'Birlik aylana', 16, INK, weight='700'), line(190, cy, 530, cy, '#334155', 2, arrow=True), line(cx, 370, cx, 55, '#334155', 2, arrow=True), circle(cx, cy, r, 'none', '#1e3a8a', 2.5)]
a = math.radians(40)
px, py = cx + r * math.cos(a), cy - r * math.sin(a)
o += [line(cx, cy, px, py, C1, 3), line(px, py, px, cy, C2, 3), line(cx, cy, px, cy, C3, 3), circle(px, py, 5, C1), T(px + 10, py - 8, 'M(cos α; sin α)', 13, INK, anchor='start', weight='700'),
      T(cx + 45, cy - 8, 'α', 15, INK, weight='700')]
for nm, x, y in [('I: +  +', 470, 100), ('II: −  +', 250, 100), ('III: −  −', 250, 340), ('IV: +  −', 470, 340)]:
    o.append(T(x, y, nm, 12, MUTED))
add('m6b', 'Birlik aylana', svg('Birlik aylana', ''.join(o)))
add('m6c', 'Trigonometrik formulalar', tree('Asosiy formulalar', 'Trigonometriya', [('Asosiy ayniyat', 'sin²α + cos²α = 1'), ('Yig\'indi', 'sin(α+β) = sinα cosβ + cosα sinβ'), ('Ikkilangan burchak', 'sin2α = 2 sinα cosα')]))
p = P((-0.2, 6.6), (-1.5, 1.5))
p.axes(xs=[], ys=[-1, 1]).curve(math.sin, C1, x0=0, x1=6.4).curve(math.cos, C2, x0=0, x1=6.4)
for v, nm in [(math.pi / 2, 'π/2'), (math.pi, 'π'), (3 * math.pi / 2, '3π/2'), (2 * math.pi, '2π')]:
    p.raw(line(p.X(v), p.Y(0) - 4, p.X(v), p.Y(0) + 4, '#334155', 2)).raw(T(p.X(v), p.Y(0) + 18, nm, 11, MUTED))
p.text(0.7, 1.3, 'y = sin x', 13, C1, weight='700').text(3.4, 1.3, 'y = cos x', 13, C2, weight='700')
add('m6d', 'Sinus va kosinus grafigi', p.done('y = sin x va y = cos x'))
p = P((0, 6.4), (-1.5, 1.5))
p.axes(xs=[], ys=[-1, 1]).curve(math.sin, C1, x0=0, x1=6.4).seg(0, 0.5, 6.4, 0.5, C3, 2, '6 4').pt(math.pi / 6, 0.5, 'π/6', C2, dy=-10).pt(5 * math.pi / 6, 0.5, '5π/6', C2, dy=-10)
p.text(3.2, -1.25, 'sin x = ½  ⇒  x = π/6 + 2πk;  x = 5π/6 + 2πk', 12, INK, anchor='middle', weight='700')
add('m6e', 'Trigonometrik tenglama', p.done('sin x = 1/2 yechimlari'))
o = [T(360, 56, 'Sinuslar teoremasi', 16, INK, weight='700'), poly([(120, 320), (560, 320), (390, 120)], '#e0f2fe', '#0c4a6e', 2.5), T(105, 340, 'A', 18, INK, weight='800'), T(580, 340, 'B', 18, INK, weight='800'), T(390, 108, 'C', 18, INK, weight='800'),
     T(340, 345, 'c', 15, C1, weight='700'), T(500, 215, 'a', 15, C1, weight='700'), T(235, 215, 'b', 15, C1, weight='700'), T(360, 385, 'a/sin A = b/sin B = c/sin C = 2R;   c² = a² + b² − 2ab·cos C', 13, INK, weight='700')]
add('m6f', 'Sinuslar va kosinuslar teoremasi', svg('Uchburchakni yechish', ''.join(o)))

# ---------------- 7-bo'lim: ketma-ketlik, ehtimol, statistika
o = [T(360, 56, 'Arifmetik progressiya: aₙ = a₁ + (n−1)d', 16, INK, weight='700')]
for i in range(6):
    h = 50 + 40 * i
    o += [box(80 + i * 95, 340 - h, 70, h, tint(PAL[i], .4), PAL[i], rx=6, sw=2), T(115 + i * 95, 330 - h, 3 + 2 * i, 14, INK, weight='800'), T(115 + i * 95, 360, f'a{i+1}', 12, MUTED)]
o.append(T(360, 385, 'a₁ = 3,  d = 2  →  3, 5, 7, 9, 11, 13', 13, MUTED))
add('m7a', 'Arifmetik progressiya', svg('Arifmetik progressiya', ''.join(o)))
o = [T(360, 56, 'Geometrik progressiya: bₙ = b₁ · qⁿ⁻¹', 16, INK, weight='700')]
for i in range(6):
    v = 2 ** i
    h = 20 + v * 9
    o += [box(80 + i * 95, 340 - h, 70, h, tint(PAL[i], .4), PAL[i], rx=6, sw=2), T(115 + i * 95, 330 - h, v, 14, INK, weight='800'), T(115 + i * 95, 360, f'b{i+1}', 12, MUTED)]
o.append(T(360, 385, 'b₁ = 1,  q = 2  →  S = b₁(qⁿ − 1)/(q − 1)', 13, MUTED))
add('m7b', 'Geometrik progressiya', svg('Geometrik progressiya', ''.join(o)))
o = [ARROW_DEF, T(360, 50, '3 ta harf: A, B, C — o\'rin almashtirishlar P₃ = 3! = 6', 15, INK, weight='700'), box(300, 70, 120, 34, '#1f2937', rx=8), T(360, 93, 'Boshlanish', 13, '#fff')]
perms = [('A', ['BC', 'CB']), ('B', ['AC', 'CA']), ('C', ['AB', 'BA'])]
for i, (a, rest) in enumerate(perms):
    x = 130 + i * 230
    o += [line(360, 104, x, 150, '#64748b', 2, arrow=True), box(x - 30, 150, 60, 34, tint(PAL[i], .4), PAL[i], rx=8, sw=2), T(x, 173, a, 15, INK, weight='800')]
    for j, rs in enumerate(rest):
        xx = x - 55 + j * 110
        o += [line(x, 184, xx, 250, '#64748b', 2, arrow=True), box(xx - 30, 250, 60, 34, tint(PAL[i], .2), PAL[i], rx=8), T(xx, 273, a + rs, 14, INK, weight='700')]
o.append(T(360, 340, 'Ko\'paytirish qoidasi: 3 · 2 · 1 = 6', 14, C3, weight='700'))
add('m7c', 'Kombinatorika', svg('Daraxt diagramma', ''.join(o)))
o = [T(360, 56, 'Ikki kubik tashlanganda yig\'indi ehtimolligi', 15, INK, weight='700')]
vals = [1, 2, 3, 4, 5, 6, 5, 4, 3, 2, 1]
for i, v in enumerate(vals):
    h = v * 40
    o += [box(70 + i * 54, 340 - h, 44, h, tint(PAL[i % 6], .45), PAL[i % 6], rx=4, sw=2), T(92 + i * 54, 358, i + 2, 12, MUTED), T(92 + i * 54, 330 - h, f'{v}/36', 11, INK, weight='700')]
add('m7d', 'Ehtimollik', svg('Ehtimollik taqsimoti', ''.join(o)))
o = [T(360, 56, 'Chastotalar gistogrammasi', 16, INK, weight='700'), line(70, 340, 660, 340, '#334155', 2), line(70, 340, 70, 80, '#334155', 2)]
data = [3, 6, 10, 7, 4]
for i, v in enumerate(data):
    o += [box(90 + i * 110, 340 - v * 25, 100, v * 25, tint(PAL[i], .45), PAL[i], rx=2, sw=2), T(140 + i * 110, 330 - v * 25, v, 13, INK, weight='800'), T(140 + i * 110, 360, f'{i*10}–{i*10+10}', 12, MUTED)]
o.append(T(360, 388, 'O\'rta qiymat = Σxᵢ / n;   mediana — o\'rtadagi qiymat;   moda — eng ko\'p uchraydigan qiymat', 12, MUTED))
add('m7e', 'Statistika', svg('Statistika', ''.join(o)))
o = [T(360, 56, 'To\'plamlar: A ∪ B, A ∩ B', 16, INK, weight='700'), '<circle cx="290" cy="215" r="120" fill="#60a5fa" fill-opacity=".35" stroke="#1e3a8a" stroke-width="2.5"/>', '<circle cx="430" cy="215" r="120" fill="#f87171" fill-opacity=".35" stroke="#7f1d1d" stroke-width="2.5"/>',
     T(230, 220, 'A', 24, INK, weight='800'), T(490, 220, 'B', 24, INK, weight='800'), T(360, 220, 'A ∩ B', 15, INK, weight='800'), T(360, 380, 'Qo\'shish qoidasi: |A ∪ B| = |A| + |B| − |A ∩ B|', 14, C3, weight='700')]
add('m7f', 'To\'plamlar va mantiq', svg('Eyler–Venn diagrammasi', ''.join(o)))

# ---------------- 8-bo'lim: koordinatalar va vektorlar
p = P((-1, 8), (-1, 7))
p.axes().seg(1, 1, 7, 5, C1, 3).pt(1, 1, 'A(1; 1)', C2, dx=-5, dy=22).pt(7, 5, 'B(7; 5)', C2, dx=-30, dy=-10)
p.seg(1, 1, 7, 1, '#94a3b8', 1.5, '5 4').seg(7, 1, 7, 5, '#94a3b8', 1.5, '5 4').text(3.2, 6.7, 'AB = √((7−1)² + (5−1)²) = √52', 13, C3, weight='700')
add('m8a', 'Ikki nuqta orasidagi masofa', p.done('Koordinatalar tekisligi'))
p = P((-6, 6), (-5, 5), (150, 55, 570, 365))
p.axes().curve(lambda t: 0, 'none').raw(circle(p.X(0), p.Y(0), (p.X(3) - p.X(0)), 'none', C2, 3)).curve(lambda x: x / 2 + 1, C1).text(-5.6, 4.5, 'x² + y² = 9', 13, C2, weight='700').text(1.5, 4.6, 'y = x/2 + 1', 13, C1, weight='700')
add('m8b', 'To\'g\'ri chiziq va aylana', p.done('Aylana va to\'g\'ri chiziq tenglamasi'))
o = [T(360, 56, 'Konik kesimlar', 16, INK, weight='700'),
     '<ellipse cx="130" cy="190" rx="90" ry="55" fill="#dbeafe" stroke="#1e3a8a" stroke-width="3"/>', T(130, 290, 'Ellips', 15, INK, weight='700'), T(130, 315, 'x²/a² + y²/b² = 1', 13, MUTED),
     '<path d="M300 90 Q380 190 300 290" fill="none" stroke="#7f1d1d" stroke-width="3"/><path d="M420 90 Q340 190 420 290" fill="none" stroke="#7f1d1d" stroke-width="3"/>', T(360, 335, 'Giperbola', 15, INK, weight='700'), T(360, 360, 'x²/a² − y²/b² = 1', 13, MUTED),
     '<path d="M520 90 Q580 320 640 90" fill="none" stroke="#14532d" stroke-width="3"/>', T(580, 335, 'Parabola', 15, INK, weight='700'), T(580, 360, 'y² = 2px', 13, MUTED)]
add('m8c', 'Konik kesimlar', svg('Ellips, giperbola, parabola', ''.join(o)))
p = P((-1, 9), (-1, 7))
p.axes().seg(0, 0, 4, 1, C1, 3, arrow=True).seg(4, 1, 7, 5, C2, 3, arrow=True).seg(0, 0, 7, 5, C3, 3, arrow=True).text(1.6, 0.1, 'a', 14, C1, weight='700').text(6.0, 3.0, 'b', 14, C2, weight='700').text(2.5, 3.4, 'a + b', 14, C3, weight='700').text(0.3, 6.5, 'a = (4; 1),  b = (3; 4),  a + b = (7; 5)', 13, INK, weight='700')
add('m8d', 'Vektorlarni qo\'shish', p.done('Vektorlarni qo\'shish (uchburchak qoidasi)'))

# ---------------- 9-bo'lim: analiz
p = P((-1, 6), (-1, 6))
p.axes().curve(lambda x: (x * x - 4) / (x - 2) if abs(x - 2) > 0.001 else None, C2, x0=-1, x1=6).pt(2, 4, '', '#fff', r=6).text(2.3, 4.5, 'lim (x→2) = 4', 13, C1, weight='700').text(-0.8, 5.5, 'f(x) = (x² − 4)/(x − 2) = x + 2', 12, C2, weight='700')
add('m9a', 'Limit', p.done('Funksiya limiti'))
p = P((-1, 5), (-1, 9))
p.axes().curve(lambda x: x * x, C2, x0=-1, x1=3).curve(lambda x: 4 * x - 4, C1, x0=0.5, x1=4).pt(2, 4, '(2; 4)', C3, dx=-70, dy=-6).text(2.9, 7.7, 'y = x², k = f\'(2) = 4', 13, INK, weight='700')
add('m9b', 'Hosila — urinma qiyaligi', p.done('Hosilaning geometrik ma\'nosi'))
p = P((-1, 7), (-3, 6))
g = lambda x: -0.35 * (x - 1) * (x - 5) * (x - 3) / 2 + 1.5
p.axes().curve(g, C2, n=300).pt(2, g(2) , 'max', C1, dy=-12).pt(4, g(4), 'min', C3, dy=22).text(0.1, 5.5, 'f\'(x) = 0 nuqtalar — ekstremum', 13, INK, weight='700')
add('m9c', 'Hosila va ekstremumlar', p.done('Funksiyaning ekstremumlari'))
add('m9d', 'Boshlang\'ich funksiya', tree('Boshlang\'ich funksiya', 'F\'(x) = f(x)', [('∫ xⁿ dx', 'xⁿ⁺¹/(n+1) + C'), ('∫ sin x dx', '−cos x + C'), ('∫ eˣ dx', 'eˣ + C')]))
p = P((-0.5, 4.5), (-0.5, 9))
xs = [0 + i * 0.05 for i in range(0, 61)]
poly_pts = [(p.X(0), p.Y(0))] + [(p.X(x), p.Y(x * x)) for x in [i * 0.05 for i in range(0, 61)]] + [(p.X(3), p.Y(0))]
p.axes().raw(poly(poly_pts, '#bfdbfe', 'none')).curve(lambda x: x * x, C2, x0=-0.5, x1=3.2).text(0.1, 8.3, '∫₀³ x² dx = x³/3 |₀³ = 9', 14, C1, weight='700').text(1.6, 1.4, 'yuza', 14, INK, weight='700')
add('m9e', 'Aniq integral', p.done('Aniq integral — egri chiziqli trapetsiya yuzi'))
add('m9f', 'Ko\'p o\'zgaruvchili funksiyalar', tree('z = f(x, y)', 'Ikki o\'zgaruvchi', [('∂z/∂x', 'y ni o\'zgarmas deb x bo\'yicha hosila'), ('∂z/∂y', 'x ni o\'zgarmas deb y bo\'yicha hosila'), ('Gradient', '(∂z/∂x; ∂z/∂y) — eng tez o\'sish yo\'nalishi')]))

# ---------------- 10-bo'lim: oliy matematika
p = P((-4, 5), (-3, 5), (110, 55, 610, 365))
p.axes().seg(0, 0, 3, 4, C1, 3, arrow=True).pt(3, 4, 'z = 3 + 4i', C2, dx=8, dy=-6).seg(3, 0, 3, 4, '#94a3b8', 1.5, '5 4').text(0.5, -0.6, 'Re z = 3', 12, INK).text(3.2, 2.0, 'Im z = 4', 12, INK).text(-3.8, 4.5, '|z| = √(3² + 4²) = 5', 13, C3, weight='700')
add('m10a', 'Kompleks sonlar', p.done('Kompleks tekislik'))
o = [T(360, 56, 'Matritsalarni ko\'paytirish', 16, INK, weight='700')]
def mat(x, y, vals, c):
    s = [T(x - 12, y + 40, '[', 80, INK, anchor='end', weight='300'), T(x + 108, y + 40, ']', 80, INK, anchor='start', weight='300')]
    for i, v in enumerate(vals):
        s.append(T(x + 20 + (i % 2) * 60, y + 30 + (i // 2) * 40, v, 18, c, weight='700'))
    return s
o += mat(100, 120, ['1', '2', '3', '4'], C2) + [T(260, 175, '×', 28, INK)] + mat(300, 120, ['5', '6', '7', '8'], C1) + [T(460, 175, '=', 28, INK)] + mat(500, 120, ['19', '22', '43', '50'], C3)
o += [T(360, 310, 'cᵢⱼ = i-satr · j-ustun    (1·5 + 2·7 = 19)', 14, INK, weight='700'), T(360, 345, 'Umuman AB ≠ BA', 13, MUTED)]
add('m10b', 'Matritsalar', svg('Matritsa ko\'paytmasi', ''.join(o)))
add('m10c', 'Chiziqli sistemalar', flow('Gauss usuli', [('Sistema', 'yozish'), ('Matritsa', 'kengaytirilgan'), ('Pog\'onali shakl', 'elementar almashtirish'), ('Teskari yurish', 'noma\'lumlar'), ('Javob', 'yechim')]))
p = P((-0.5, 5), (-0.5, 9))
p.axes().curve(lambda x: math.exp(x * 0.55), C2, x0=0, x1=4).curve(lambda x: 1.2 * math.exp(x * 0.55), C1, x0=0, x1=4).curve(lambda x: 0.6 * math.exp(x * 0.55), C3, x0=0, x1=4).text(0.1, 8.4, 'y\' = ky  ⇒  y = C·e^(kx)', 14, INK, weight='700')
add('m10d', 'Differensial tenglama', p.done('Differensial tenglama yechimlari oilasi'))
cx, cy = 360, 215
o = [T(360, 56, 'Modul bo\'yicha arifmetika: mod 5', 16, INK, weight='700'), circle(cx, cy, 120, 'none', '#94a3b8', 2)]
for i in range(5):
    a = -math.pi / 2 + 2 * math.pi * i / 5
    x, y = cx + 120 * math.cos(a), cy + 120 * math.sin(a)
    o += [circle(x, y, 26, tint(PAL[i], .4), PAL[i], 3), T(x, y + 6, i, 18, INK, weight='800')]
o += [T(cx, cy - 5, '7 ≡ 2', 17, C1, weight='800'), T(cx, cy + 20, '(mod 5)', 13, MUTED), T(360, 385, 'a ≡ b (mod m) ⇔ a − b ga m bo\'linadi', 13, MUTED)]
add('m10e', 'Sonlar nazariyasi va modul', svg('Soat arifmetikasi', ''.join(o)))

root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
inject('mat', {k: v for k, v in I.items()})
