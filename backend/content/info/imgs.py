# -*- coding: utf-8 -*-
import sys, os, math
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from tarix_svg import *

I = {}
add = adder1('in', I)
C1, C2, C3 = '#ef4444', '#2563eb', '#16a34a'


def table(title, head, rows, widths=None, note=''):
    n = len(head)
    widths = widths or [600 / n] * n
    x0, y0 = 60, 60
    o = []
    x = x0
    for h, w in zip(head, widths):
        o += [box(x, y0, w, 36, '#1f2937', rx=0), T(x + w / 2, y0 + 23, h, 13, '#fff', weight='700')]
        x += w
    for r, row in enumerate(rows):
        x = x0
        for c, (v, w) in enumerate(zip(row, widths)):
            o += [box(x, y0 + 36 + r * 34, w, 34, '#f1f5f9' if r % 2 == 0 else '#fff', '#cbd5e1', rx=0), T(x + w / 2, y0 + 58 + r * 34, v, 13, INK)]
            x += w
    if note:
        o.append(T(360, y0 + 36 + len(rows) * 34 + 32, note, 13, MUTED))
    return svg(title, ''.join(o))


def blocks(title, items, y=140):
    """Ketma-ket sxema bloklari: oval, to'rtburchak, romb."""
    o = [ARROW_DEF]
    n = len(items)
    gap = (W - 80) / n
    for i, (kind, txt) in enumerate(items):
        x = 40 + gap * i + gap / 2
        if kind == 'oval':
            o.append(f'<ellipse cx="{x}" cy="{y}" rx="{gap/2-12}" ry="26" fill="#bbf7d0" stroke="#14532d" stroke-width="2"/>')
        elif kind == 'rhomb':
            w = gap / 2 - 10
            o.append(poly([(x - w, y), (x, y - 38), (x + w, y), (x, y + 38)], '#fde68a', '#78350f', 2))
        else:
            o.append(box(x - gap / 2 + 12, y - 28, gap - 24, 56, '#bfdbfe', '#1e3a8a', rx=6, sw=2))
        for j, ln in enumerate(wrap(txt, 11)[:3]):
            o.append(T(x, y - 4 + j * 14 - (len(wrap(txt, 11)[:3]) - 1) * 6, ln, 11, INK, weight='700'))
        if i < n - 1:
            o.append(line(x + gap / 2 - 10, y, x + gap / 2 + 10, y, '#334155', 2, arrow=True))
    return svg(title, ''.join(o))


# ---- 1-bo'lim
add('s1a', 'Axborot va informatika', flow('Axborot aylanishi', [('Yig\'ish', 'manbadan'), ('Saqlash', 'xotirada'), ('Qayta ishlash', 'kompyuterda'), ('Uzatish', 'tarmoq orqali'), ('Foydalanish', 'qaror')]))
add('s1b', 'Sanoq sistemalari', table('Sanoq sistemalari', ['O\'nlik', 'Ikkilik', 'Sakkizlik', 'O\'n oltilik'], [['5', '101', '5', '5'], ['10', '1010', '12', 'A'], ['15', '1111', '17', 'F'], ['26', '11010', '32', '1A'], ['255', '11111111', '377', 'FF']], note='1011₂ = 1·8 + 0·4 + 1·2 + 1 = 11₁₀'))
add('s1c', 'Axborot o\'lchovi', table('Axborot birliklari', ['Birlik', 'Qiymati', 'Misol'], [['1 bit', '0 yoki 1', 'eng kichik'], ['1 bayt', '8 bit', '1 belgi'], ['1 KB', '1024 bayt', 'matn sahifasi'], ['1 MB', '1024 KB', 'rasm'], ['1 GB', '1024 MB', 'film'], ['1 TB', '1024 GB', 'disk']], [200, 200, 200]))
add('s1d', 'Kompyuter tarixi', timeline('Kompyuter tarixi', [('~1642', 'Paskal arifmometri'), ('1837', 'Bebbij analitik mashinasi'), ('1946', 'ENIAC — birinchi EHM'), ('1971', 'Birinchi mikroprotsessor'), ('1981', 'IBM PC'), ('1991', 'Internet — WWW')]))
add('s1e', 'Kompyuter qurilmalari', tree('Kompyuter tuzilishi', 'Kompyuter', [('Kiritish', 'Klaviatura, sichqoncha'), ('Protsessor', 'Hisoblash va boshqaruv'), ('Xotira', 'RAM, SSD/HDD'), ('Chiqarish', 'Monitor, printer')]))
# ---- 2-bo'lim
add('s2a', 'Dasturiy ta\'minot turlari', tree('Dasturiy ta\'minot', 'Dasturlar', [('Tizim', 'Operatsion tizim, drayverlar'), ('Amaliy', 'Word, brauzer, o\'yinlar'), ('Instrumental', 'Kompilyator, IDE')]))
add('s2b', 'Operatsion tizimlar', layers('Kompyuter qatlamlari', [('Foydalanuvchi', 'siz', '#a78bfa', 1), ('Amaliy dasturlar', 'brauzer, Word', '#60a5fa', 1), ('Operatsion tizim', 'Windows, Linux, Android', '#fbbf24', 1.2), ('Apparat', 'protsessor, xotira', '#94a3b8', 1)]))
o = [T(360, 56, 'Fayl tizimi — daraxt shakli', 16, INK, weight='700'), box(300, 80, 120, 36, '#1f2937', rx=8), T(360, 103, 'C:\\', 14, '#fff', weight='700')]
for i, (nm, kids) in enumerate([('Hujjatlar', ['hisobot.docx', 'jadval.xlsx']), ('Rasmlar', ['foto.jpg', 'logo.png']), ('Dasturlar', ['python.exe', 'chrome.exe'])]):
    x = 130 + i * 230
    o += [line(360, 116, x, 170, '#64748b', 2), box(x - 55, 170, 110, 34, tint(PAL[i], .4), PAL[i], rx=8, sw=2), T(x, 193, nm, 13, INK, weight='700')]
    for j, k in enumerate(kids):
        o += [line(x, 204, x, 245 + j * 45, '#cbd5e1', 2), box(x - 60, 230 + j * 45, 120, 30, '#fff', '#94a3b8', rx=6), T(x, 250 + j * 45, k, 12, INK)]
add('s2c', 'Fayl va papkalar', svg('Fayl tizimi', ''.join(o)))
add('s2d', 'Xavfsiz foydalanish', tree('Kompyuterdan foydalanish', 'Xavfsiz ish', [('Ergonomika', 'To\'g\'ri o\'tirish, 20-20-20'), ('Zaxira', 'Muhim fayllar nusxasi'), ('Antivirus', 'Yangilab turish')]))
# ---- 3-bo'lim
add('s3a', 'Mantiq algebrasi', table('Mantiq jadvali', ['A', 'B', 'A AND B', 'A OR B', 'NOT A'], [['0', '0', '0', '0', '1'], ['0', '1', '0', '1', '1'], ['1', '0', '0', '1', '0'], ['1', '1', '1', '1', '0']]))
add('s3b', 'Algoritm', tree('Algoritm xossalari', 'Algoritm', [('Aniqlik', 'Har qadam tushunarli'), ('Cheklilik', 'Tugallanadi'), ('Natijaviylik', 'Javob beradi'), ('Ommaviylik', 'Ko\'p holat uchun')]))
add('s3c', 'Blok-sxema', blocks('Blok-sxema: juft yoki toq', [('oval', 'Boshlash'), ('rect', 'n kiritish'), ('rhomb', 'n % 2 == 0?'), ('rect', '"Juft" chiqar'), ('oval', 'Tugash')]))
o = [T(360, 56, 'Binar qidiruv: 7 ni topish', 16, INK, weight='700')]
arr = [1, 3, 5, 7, 9, 11, 13]
for i, v in enumerate(arr):
    col = '#fde68a' if i == 3 else '#e2e8f0'
    o += [box(75 + i * 85, 160, 75, 60, col, '#334155', rx=8, sw=2), T(112 + i * 85, 198, v, 22, INK, weight='800'), T(112 + i * 85, 245, f'[{i}]', 11, MUTED)]
o += [T(360, 300, '1) o\'rtadagi element 7 — topildi!', 14, C3, weight='700'), T(360, 330, 'Murakkabligi: O(log n)   (chiziqli qidiruv: O(n))', 13, MUTED)]
add('s3d', 'Qidiruv algoritmlari', svg('Binar qidiruv', ''.join(o)))
add('s3e', 'Ma\'lumotlar tuzilmalari', tree('Ma\'lumotlar tuzilmalari', 'Tuzilmalar', [('Massiv', 'Indeks bo\'yicha tez'), ('Stek', 'LIFO: oxirgi kirgan birinchi chiqadi'), ('Navbat', 'FIFO: birinchi kirgan birinchi chiqadi'), ('Daraxt', 'Ierarxik ma\'lumot')]))
# ---- 4-bo'lim Python
add('s4a', 'Python asoslari', compare('Python asoslari', 'O\'zgaruvchilar', ['x = 5   (int)', 'name = "Ali"   (str)', 'pi = 3.14   (float)'], 'Amallar', ['+  -  *  /  //  %  **', 'print(x + 2)', 'input() — kiritish']))
add('s4b', 'Shartli operatorlar', blocks('if / elif / else', [('oval', 'Boshlash'), ('rect', 'n kiritish'), ('rhomb', 'n > 0?'), ('rect', 'musbat'), ('oval', 'Tugash')]))
add('s4c', 'Sikllar', compare('Sikllar', 'for', ['for i in range(5):', '    print(i)', 'Aniq takrorlar soni'], 'while', ['while n > 0:', '    n -= 1', 'Shart bajarilguncha']))
add('s4d', 'Funksiyalar', flow('Funksiya chaqirilishi', [('def', 'e\'lon qilish'), ('Argument', 'qiymat berish'), ('Bajarish', 'tana'), ('return', 'natija'), ('Foydalanish', 'x = f(3)')]))
add('s4e', 'Ma\'lumot turlari', table('Python to\'plamlari', ['Tur', 'Belgisi', 'O\'zgaradimi', 'Misol'], [['list', '[ ]', 'ha', '[1, 2, 3]'], ['tuple', '( )', 'yo\'q', '(1, 2)'], ['dict', '{ : }', 'ha', '{"a": 1}'], ['set', '{ }', 'ha', '{1, 2}']], [120, 120, 160, 200]))
add('s4f', 'Fayllar va xatolar', flow('Fayl bilan ishlash', [('open()', 'ochish'), ('read/write', 'o\'qish/yozish'), ('close()', 'yopish'), ('try', 'xatoni kutish'), ('except', 'xatoni ushlash')]))
# ---- 5-bo'lim
add('s5a', 'Word', tree('Matn muharriri', 'Word', [('Shrift', 'Hajm, rang, uslub'), ('Abzas', 'Tekislash, oraliq'), ('Jadval', 'Ma\'lumot tartibi'), ('Sahifa', 'Chegara, raqam')]))
add('s5b', 'Excel', table('Excel: jadval va formula', ['', 'A', 'B', 'C'], [['1', '10', '20', '=A1+B1'], ['2', '5', '8', '=A2+B2'], ['3', '7', '3', '=SUM(A3:B3)'], ['4', '=SUM(A1:A3)', '=AVERAGE(B1:B3)', '=MAX(C1:C3)']], [60, 180, 180, 180]))
add('s5c', 'PowerPoint', flow('Taqdimot tayyorlash', [('Reja', 'mavzu'), ('Slaydlar', 'matn+rasm'), ('Dizayn', 'mavzu va rang'), ('Animatsiya', 'o\'tishlar'), ('Namoyish', 'F5')]))
o = [T(360, 56, 'Rastr va vektor grafika', 16, INK, weight='700'), T(190, 100, 'Rastr (piksel)', 15, INK, weight='700')]
import random as _r
_r.seed(3)
for i in range(8):
    for j in range(8):
        c = ['#1e3a8a', '#3b82f6', '#93c5fd', '#e0f2fe'][(i * j + i) % 4]
        o.append(box(110 + i * 20, 125 + j * 20, 20, 20, c, rx=0))
o += [T(190, 310, 'JPG, PNG — kattalashtirsa xiralashadi', 12, MUTED), T(530, 100, 'Vektor (formula)', 15, INK, weight='700'), circle(530, 205, 62, '#bbf7d0', '#14532d', 3), poly([(480, 260), (580, 260), (530, 170)], 'none', '#14532d', 3), T(530, 310, 'SVG — sifati o\'zgarmaydi', 12, MUTED)]
add('s5d', 'Kompyuter grafikasi', svg('Rastr va vektor', ''.join(o)))
add('s5e', 'Multimedia', table('Multimedia formatlari', ['Tur', 'Format', 'Siqish'], [['Rasm', 'JPG, PNG, GIF', 'yo\'qotishli / yo\'qotishsiz'], ['Audio', 'MP3, WAV', 'MP3 — siqilgan'], ['Video', 'MP4, AVI', 'kodek orqali']], [140, 200, 260]))
# ---- 6-bo'lim
o = [T(360, 56, 'Tarmoq topologiyalari', 16, INK, weight='700')]
def node(x, y, c='#bfdbfe'):
    return box(x - 16, y - 12, 32, 24, c, '#1e3a8a', rx=4, sw=2)
o += [T(130, 330, 'Yulduz', 14, INK, weight='700'), T(360, 330, 'Shina', 14, INK, weight='700'), T(590, 330, 'Halqa', 14, INK, weight='700')]
o.append(node(130, 190, '#fde68a'))
for k in range(5):
    a = 2 * math.pi * k / 5 - math.pi / 2
    x, y = 130 + 85 * math.cos(a), 190 + 85 * math.sin(a)
    o += [line(130, 190, x, y, '#64748b', 2), node(x, y)]
o.append(line(250, 190, 470, 190, '#64748b', 4))
for k in range(5):
    x = 270 + k * 45 if k < 5 else 0
    o += [line(x, 190, x, 150 if k % 2 == 0 else 230, '#64748b', 2), node(x, 140 if k % 2 == 0 else 240)]
for k in range(6):
    a = 2 * math.pi * k / 6
    a2 = 2 * math.pi * (k + 1) / 6
    x, y, x2, y2 = 590 + 85 * math.cos(a), 190 + 85 * math.sin(a), 590 + 85 * math.cos(a2), 190 + 85 * math.sin(a2)
    o += [line(x, y, x2, y2, '#64748b', 2), node(x, y)]
add('s6a', 'Tarmoq asoslari', svg('Tarmoq topologiyalari', ''.join(o)))
add('s6b', 'Internet va IP', flow('Veb sahifa so\'rovi', [('Brauzer', 'URL kiritildi'), ('DNS', 'domen → IP'), ('Server', 'IP manzil'), ('HTTP', 'so\'rov/javob'), ('Sahifa', 'ko\'rsatildi')]))
add('s6c', 'Veb texnologiyalar', tree('Veb sahifa tarkibi', 'Veb sahifa', [('HTML', 'Tuzilma va matn'), ('CSS', 'Dizayn va ranglar'), ('JavaScript', 'Interaktivlik')]))
add('s6d', 'Internetdan foydalanish', tree('Qidiruv ko\'nikmalari', 'Internetda qidirish', [('Kalit so\'z', 'Aniq va qisqa'), ('Manba', 'Ishonchli sayt'), ('Tekshirish', 'Bir necha manba bilan solishtirish')]))
add('s6e', 'Mobil texnologiyalar', compare('Simsiz texnologiyalar', 'Yaqin masofa', ['Bluetooth ~10 m', 'NFC ~4 sm', 'Wi-Fi ~50 m'], 'Uzoq masofa', ['3G/4G/5G', 'Sun\'iy yo\'ldosh', 'Operator tarmog\'i']))
# ---- 7-bo'lim
add('s7a', 'Ma\'lumotlar bazasi', table('Jadval: students', ['id', 'ism', 'yosh', 'sinf'], [['1', 'Ali', '15', '9-A'], ['2', 'Vali', '16', '10-B'], ['3', 'Zilola', '15', '9-A']], [80, 200, 120, 200], note='Ustun = maydon, satr = yozuv, id — birlamchi kalit'))
add('s7b', 'SQL buyruqlari', table('Asosiy SQL buyruqlari', ['Buyruq', 'Vazifasi', 'Misol'], [['SELECT', 'Tanlash', 'SELECT ism FROM t'], ['INSERT', 'Qo\'shish', 'INSERT INTO t ...'], ['UPDATE', 'O\'zgartirish', 'UPDATE t SET ...'], ['DELETE', 'O\'chirish', 'DELETE FROM t ...']], [120, 160, 320]))
o = [T(360, 56, 'JOIN turlari', 16, INK, weight='700')]
for i, (nm, mode) in enumerate([('INNER JOIN', 'in'), ('LEFT JOIN', 'left'), ('FULL JOIN', 'full')]):
    cx = 130 + i * 230
    fa = '#60a5fa' if mode in ('left', 'full') else '#e2e8f0'
    fb = '#f87171' if mode == 'full' else '#e2e8f0'
    o += [f'<circle cx="{cx-28}" cy="200" r="60" fill="{fa}" fill-opacity=".5" stroke="#1e3a8a" stroke-width="2.5"/>', f'<circle cx="{cx+28}" cy="200" r="60" fill="{fb}" fill-opacity=".5" stroke="#7f1d1d" stroke-width="2.5"/>',
          f'<path d="M{cx} 148 A60 60 0 0 1 {cx} 252 A60 60 0 0 1 {cx} 148" fill="#a78bfa" fill-opacity=".8"/>', T(cx, 300, nm, 14, INK, weight='800')]
add('s7c', 'JOIN', svg('Jadvallarni bog\'lash', ''.join(o)))
add('s7d', 'Ma\'lumotlarni tahlil qilish', flow('Tahlil bosqichlari', [('Yig\'ish', 'manbalar'), ('Tozalash', 'xatolarni olib tashlash'), ('Tahlil', 'GROUP BY, COUNT'), ('Vizualizatsiya', 'grafiklar'), ('Qaror', 'xulosa')]))
# ---- 8-bo'lim
add('s8a', 'Axborot xavfsizligi', tree('CIA uchligi', 'Axborot xavfsizligi', [('Maxfiylik', 'Faqat ruxsati borlar ko\'radi'), ('Yaxlitlik', 'Ma\'lumot o\'zgarmaydi'), ('Mavjudlik', 'Kerakda foydalanish mumkin')]))
add('s8b', 'Parollar', compare('Parol', 'Zaif', ['123456', 'ismingiz2010', 'bir xil parol hamma joyda'], 'Kuchli', ['12+ belgi', 'Harf, raqam, belgi', '2 bosqichli autentifikatsiya']))
o = [ARROW_DEF, T(360, 56, 'Simmetrik shifrlash', 16, INK, weight='700'), box(60, 160, 140, 70, '#bfdbfe', '#1e3a8a', rx=10, sw=2), T(130, 190, 'Ochiq matn', 14, INK, weight='700'), T(130, 212, '"SALOM"', 14, INK),
     line(200, 195, 280, 195, '#334155', 2.5, arrow=True), box(280, 160, 160, 70, '#fde68a', '#78350f', rx=10, sw=2), T(360, 190, 'Shifrlash', 14, INK, weight='700'), T(360, 212, 'kalit = 3 (Sezar)', 12, MUTED),
     line(440, 195, 520, 195, '#334155', 2.5, arrow=True), box(520, 160, 140, 70, '#fecaca', '#7f1d1d', rx=10, sw=2), T(590, 190, 'Shifrmatn', 14, INK, weight='700'), T(590, 212, '"VDORP"', 14, INK),
     T(360, 300, 'Sezar shifri: har harf alifboda 3 o\'rin siljiydi', 14, C3, weight='700'), T(360, 330, 'Ochiq kalitli (RSA): shifrlash va ochish kalitlari boshqa', 13, MUTED)]
add('s8c', 'Kriptografiya', svg('Shifrlash sxemasi', ''.join(o)))
# ---- 9-bo'lim
add('s9a', 'Sun\'iy intellekt', layers('AI → ML → DL', [('Sun\'iy intellekt', 'aqlli tizimlar', '#a78bfa', 1), ('Mashinaviy o\'rganish', 'ma\'lumotdan o\'rganadi', '#60a5fa', 1), ('Chuqur o\'rganish', 'neyron tarmoqlar', '#34d399', 1)]))
add('s9b', 'IoT va robototexnika', flow('IoT ishlashi', [('Sensor', 'ma\'lumot yig\'adi'), ('Aloqa', 'Wi-Fi, 5G'), ('Bulut', 'qayta ishlash'), ('Qaror', 'tahlil'), ('Aktuator', 'harakat')]))
add('s9c', 'Bulutli hisoblash', compare('Bulutli hisoblash', 'Afzalliklari', ['Har joydan foydalanish', 'Kuchli resurs', 'Zaxira nusxa'], 'Tashvishlar', ['Internetga bog\'liqlik', 'Ma\'lumot xavfsizligi', 'Obuna to\'lovlari']))
add('s9d', 'Axborot jamiyati', tree('Axborot jamiyati', 'Raqamli axloq', [('Mualliflik huquqi', 'Boshqaning ishini hurmat qilish'), ('Shaxsiy ma\'lumot', 'Himoyalash'), ('Axloq', 'Soxta xabarga qarshi')]))

inject('info', I)
