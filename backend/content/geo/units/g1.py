# -*- coding: utf-8 -*-
import math
from dsl import topic
from svglib import *

IMAGES = {}
TOPICS = []


# ---------------------------------------------------------------- rasmlar
def _quyosh_tizimi():
    pl = [('Merkuriy', 4.9, '#94a3b8'), ('Venera', 12.1, '#fbbf24'), ('Yer', 12.7, '#60a5fa'), ('Mars', 6.8, '#f87171'),
          ('Yupiter', 80, '#fb923c'), ('Saturn', 66, '#fde68a'), ('Uran', 28, '#2dd4bf'), ('Neptun', 27, '#6366f1')]
    out = [circle(42, 215, 46, '#fbbf24', '#f59e0b', 3), T(42, 285, 'Quyosh', 13, INK, weight='700')]
    x = 108
    for name, d, col in pl:
        r = max(4, d * 0.55)
        x += r + 8
        out.append(circle(x, 215, r, col, '#475569', 1.5))
        if name == 'Saturn':
            out.append(f'<ellipse cx="{x}" cy="215" rx="{r*1.7:.1f}" ry="{r*0.35:.1f}" fill="none" stroke="#a16207" stroke-width="2"/>')
        out.append(T(x, 325 if pl.index((name, d, col)) % 2 else 345, name, 12, INK, weight='700'))
        out.append(line(x, 215 + r + 2, x, 305 if pl.index((name, d, col)) % 2 else 328, '#cbd5e1', 1))
        x += r
    out.append(T(W / 2, 75, 'Quyosh atrofidagi 8 ta sayyora (o\'lchamlari taxminan nisbatda, masofalar sxematik)', 12, MUTED))
    out.append(T(W / 2, 100, 'Ichki (quruqlik) sayyoralar: Merkuriy, Venera, Yer, Mars  |  Tashqi (gaz va muz) gigantlar: Yupiter, Saturn, Uran, Neptun', 11, MUTED))
    return svg('Quyosh tizimi', ''.join(out))


def _yer_shakli():
    cx, cy = 360, 215
    out = [f'<ellipse cx="{cx}" cy="{cy}" rx="150" ry="146" fill="#93c5fd" stroke="#1d4ed8" stroke-width="3"/>',
           line(cx, cy - 175, cx, cy + 175, '#334155', 2, '6 4'), line(cx - 190, cy, cx + 190, cy, '#ef4444', 3),
           T(cx, cy - 182, 'Shimoliy qutb', 12, INK, weight='700'), T(cx, cy + 195, 'Janubiy qutb', 12, INK, weight='700'),
           T(cx + 195, cy + 4, 'Ekvator', 12, '#b91c1c', anchor='start', weight='700'),
           T(cx - 195, cy - 8, 'Ekvator radiusi', 12, INK, anchor='end'), T(cx - 195, cy + 8, '6378 km', 13, INK, anchor='end', weight='700'),
           T(cx + 12, cy - 100, 'Qutb radiusi 6357 km', 12, INK, anchor='start', weight='700'),
           T(cx, cy + 40, 'Yer — geoid (qutblarda biroz yassilangan shar)', 12, '#1e3a8a'),
           T(110, 120, 'Ekvator uzunligi ≈ 40 075 km', 13, INK, anchor='start'),
           T(110, 142, 'Meridian uzunligi ≈ 40 008 km', 13, INK, anchor='start'),
           T(110, 164, "Yer yuzi: 510 mln km²", 13, INK, anchor='start')]
    return svg('Yerning shakli va o\'lchamlari', ''.join(out))


def _fasllar():
    cx, cy = 360, 238
    out = [ARROW_DEF, f'<ellipse cx="{cx}" cy="{cy}" rx="250" ry="105" fill="none" stroke="#94a3b8" stroke-width="2" stroke-dasharray="6 5"/>',
           circle(cx, cy, 32, '#fbbf24', '#f59e0b', 3), T(cx, cy + 5, 'Quyosh', 12, INK, weight='700')]
    spots = [(cx - 250, cy, '21 mart', 'Bahorgi tengkunlik'), (cx, cy - 105, '22 iyun', 'Shimolda yoz'),
             (cx + 250, cy, '23 sentyabr', 'Kuzgi tengkunlik'), (cx, cy + 105, '22 dekabr', 'Shimolda qish')]
    for x, y, d, t in spots:
        out.append(circle(x, y, 18, '#60a5fa', '#1d4ed8', 2))
        out.append(line(x + 6, y - 24, x - 6, y + 24, '#334155', 2))
        out.append(T(x, y - 30 if y <= cy else y + 40, d, 12, INK, weight='700'))
        out.append(T(x, y - 44 if y <= cy else y + 55, t, 11, MUTED))
    out.append(T(W / 2, 70, 'Yer o\'qi orbita tekisligiga 66,5° og\'ma — shu sababli fasllar almashadi', 12, MUTED))
    return svg('Fasllar almashinuvi', ''.join(out))


def _kecha_kunduz():
    out = [circle(110, 215, 38, '#fbbf24', '#f59e0b', 3)]
    for k in range(-3, 4):
        out.append(line(150, 215 + k * 22, 290, 215 + k * 18, '#f59e0b', 2, arrow=False))
    out.insert(0, ARROW_DEF)
    out.append(f'<path d="M420 95 A120 120 0 0 0 420 335 Z" fill="#fde68a" stroke="#1d4ed8" stroke-width="3"/>')
    out.append(f'<path d="M420 95 A120 120 0 0 1 420 335 Z" fill="#334155" stroke="#1d4ed8" stroke-width="3"/>')
    out.append(T(385, 215, 'KUNDUZ', 14, INK, weight='700'))
    out.append(T(460, 215, 'TUN', 14, '#fff', weight='700'))
    out.append(f'<path d="M520 190 A60 28 0 1 0 520 240" fill="none" stroke="#ef4444" stroke-width="3" marker-end="url(#ar)"/>')
    out.append(T(590, 165, 'Yer o\'z o\'qi', 12, INK, anchor='start'))
    out.append(T(590, 182, 'atrofida 24 soatda', 12, INK, anchor='start'))
    out.append(T(590, 199, 'bir marta aylanadi', 12, INK, anchor='start'))
    out.append(T(W / 2, H - 22, 'Aylanish natijasi: kecha-kunduz almashinuvi, Koriolis kuchi, oqimlar og\'ishi', 12, MUTED))
    return svg('Yerning o\'z o\'qi atrofida aylanishi', ''.join(out))


def _koordinata_setka():
    def ov(P):
        o = []
        for lat, col, w, dash in ((0, '#dc2626', 3, ''), (23.5, '#ea580c', 2, '6 4'), (-23.5, '#ea580c', 2, '6 4'), (66.5, '#2563eb', 2, '6 4'), (-66.5, '#2563eb', 2, '6 4')):
            a, b = P(-180, lat), P(180, lat)
            o.append(line(a[0], a[1], b[0], b[1], col, w, dash))
        a, b = P(0, 90), P(0, -90)
        o.append(line(a[0], a[1], b[0], b[1], '#7c3aed', 3))
        return ''.join(o)
    return world('Parallellar va meridianlar', overlay=ov, grid=True,
                 labels=[(-150, 4, 'Ekvator 0°'), (-150, 27, 'Shimol tropigi 23,5°'), (-150, -20, 'Janub tropigi 23,5°'), (-150, 70, 'Shimol qutb doirasi 66,5°'), (-150, -63, 'Janub qutb doirasi 66,5°'), (30, 80, 'Grinvich 0°')])


def _vaqt_mintaqalari():
    out = []
    x0, bw = 30, 27.5
    for i in range(24):
        off = i - 12
        col = PAL[i % 2] + '66'
        out.append(box(x0 + i * bw, 100, bw - 2, 180, col, '#fff', rx=2))
        out.append(T(x0 + i * bw + bw / 2, 195, f'{off:+d}' if off else '0', 12, INK, weight='700'))
    out.append(T(W / 2, 75, 'Yer 24 ta vaqt mintaqasiga bo\'lingan (har biri 15° uzunlik = 1 soat)', 13, MUTED))
    out.append(T(x0 + 12 * bw, 300, '↑ Grinvich (UTC)', 12, INK, weight='700'))
    out.append(T(W / 2, 335, "Sharqqa 15° borganda vaqt +1 soatga ilgarilaydi; Toshkent UTC+5", 13, INK))
    out.append(T(W / 2, 360, "Ko'rsatilgan qiymatlar: UTC ga nisbatan soat farqi (sxematik)", 11, MUTED))
    return svg('Vaqt mintaqalari', ''.join(out))


def _masshtab():
    out = [T(W / 2, 80, '1 : 100 000 masshtab — xaritada 1 sm yerda 1 km', 15, INK, weight='700')]
    for k in range(6):
        out.append(box(100 + k * 80, 120, 80, 18, '#1f2937' if k % 2 == 0 else '#fff', '#1f2937', rx=0, sw=2))
        out.append(T(100 + k * 80, 160, f'{k}', 12, INK))
    out.append(T(580, 160, '5 km', 12, INK, anchor='start'))
    out.append(T(W / 2, 195, 'Chiziqli masshtab: kesma bo\'laklari yerdagi masofani ko\'rsatadi', 12, MUTED))
    rows = [('1 : 10 000', '1 sm = 100 m', 'Eng yirik (reja)'), ('1 : 100 000', '1 sm = 1 km', 'Yirik'), ('1 : 1 000 000', '1 sm = 10 km', 'O\'rta'), ('1 : 50 000 000', '1 sm = 500 km', 'Mayda (dunyo xaritasi)')]
    for i, (a, b, c) in enumerate(rows):
        y = 225 + i * 32
        out.append(box(100, y - 18, 520, 28, PAL[i] + '33', rx=6))
        out.append(T(120, y, a, 13, INK, anchor='start', weight='700'))
        out.append(T(300, y, b, 13, INK, anchor='start'))
        out.append(T(460, y, c, 12, MUTED, anchor='start'))
    return svg('Xarita masshtabi', ''.join(out))


def _gorizontallar():
    out = [ARROW_DEF]
    cx, cy = 230, 225
    for k, (rx, ry, col, h) in enumerate([(150, 110, '#d9f99d', 100), (110, 80, '#bef264', 200), (70, 52, '#fde68a', 300), (30, 22, '#fdba74', 400)]):
        out.append(f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="{col}" stroke="#92400e" stroke-width="2"/>')
        out.append(T(cx + rx - 4, cy - 4, f'{h} m', 11, '#78350f', anchor='end', weight='700')) if h < 400 else None
    out.append(circle(cx, cy, 4, '#7f1d1d'))
    out.append(T(cx, cy + 22, "▲ cho'qqi 420 m", 11, '#7f1d1d', weight='700'))
    out.append(T(520, 120, 'Gorizontallar —', 14, INK, anchor='start', weight='700'))
    out.append(T(520, 140, 'bir xil balandlikdagi', 13, INK, anchor='start'))
    out.append(T(520, 158, 'nuqtalarni tutashtiruvchi', 13, INK, anchor='start'))
    out.append(T(520, 176, 'chiziqlar', 13, INK, anchor='start'))
    out.append(T(520, 215, "Zich — tik qiya;", 13, INK, anchor='start'))
    out.append(T(520, 233, "siyrak — yotiq qiya", 13, INK, anchor='start'))
    out.append(T(520, 270, "Pastdan yuqoriga:", 12, MUTED, anchor='start'))
    out.append(T(520, 287, "100 → 200 → 300 → 400 m", 12, MUTED, anchor='start'))
    return svg('Relyefni xaritada ko\'rsatish: gorizontallar', ''.join(out))


IMAGES.update({
    'g1_quyosh_tizimi': _quyosh_tizimi(), 'g1_yer_shakli': _yer_shakli(), 'g1_fasllar': _fasllar(), 'g1_kecha_kunduz': _kecha_kunduz(),
    'g1_setka': _koordinata_setka(), 'g1_vaqt': _vaqt_mintaqalari(), 'g1_masshtab': _masshtab(), 'g1_gorizontal': _gorizontallar(),
})

# ---------------------------------------------------------------- mavzular
TOPICS.append(topic(1, 'g1a', "1-mavzu. Yer — Quyosh tizimidagi sayyora",
    ["Quyosh tizimi tarkibini bilish", "Yerning shakli va o'lchamlarini aytish", "Yerning hayot uchun qulay sharoitlarini tushuntirish"],
    [("Quyosh tizimi", "Quyosh tizimi markazida Quyosh joylashgan, uning atrofida sakkizta sayyora aylanadi: Merkuriy, Venera, Yer, Mars, Yupiter, Saturn, Uran va Neptun. Dastlabki to'rttasi quruqlik (qattiq) sayyoralar, keyingi to'rttasi gaz va muzdan iborat gigantlar. Sayyoralarning yo'ldoshlari, asteroidlar va kometalar ham tizimga kiradi. Quyosh tizimi taxminan 4,6 mlrd yil oldin paydo bo'lgan.", 'g1_quyosh_tizimi', "Quyosh tizimi sayyoralari (sxematik)"),
     ("Yerning shakli va o'lchami", "Yer qutblarda biroz yassilangan shar — geoid shaklida. Ekvator radiusi 6378 km, qutb radiusi 6357 km, ekvator uzunligi taxminan 40 075 km. Yer yuzasining umumiy maydoni 510 mln km²; uning 71 % ini okeanlar, 29 % ini quruqlik egallaydi. Yerning shar shaklda ekanini kemalarning ufqdan asta-sekin ko'rinishi, Oy tutilishida Yer soyasining dumaloqligi va kosmik suratlar isbotlaydi.", 'g1_yer_shakli', "Yerning shakli: ekvator va qutb radiuslari"),
     ("Nega Yerda hayot bor?", "Yer Quyoshdan o'rtacha 150 mln km uzoqlikda, shu sababli harorat suyuq suv saqlanishiga mos. Atmosfera Yerni zararli nurlardan himoya qiladi va issiqlikni ushlab turadi; kislorod nafas olish uchun zarur. Magnit maydon Quyosh shamolidan saqlaydi. Bunday sharoit Quyosh tizimida boshqa sayyoralarda yo'q."),
     ("Yer — dinamik tizim", "Yer yagona sistema: litosfera (qattiq qobiq), gidrosfera (suv qobig'i), atmosfera (havo) va biosfera (hayot qobig'i) o'zaro bog'liq. Geografiya ana shu qobiqlar orasidagi aloqalarni, ularning hududlar bo'yicha taqsimlanishini o'rganadi.")],
    ["Quyosh tizimida 8 ta sayyora bor.", "Yer geoid — qutblarda yassilangan shar.", "Ekvator radiusi 6378 km, uzunligi ≈ 40 075 km.", "Yer yuzasining 71 % i okean, 29 % i quruqlik.", "Yer Quyoshdan ~150 mln km uzoqda.", "Yer qobiqlari: litosfera, gidrosfera, atmosfera, biosfera."],
    "Yer — Quyosh tizimining uchinchi sayyorasi, geoid shaklida; harorati, atmosferasi va suvi hayot uchun qulay.",
    [("Quyosh tizimida nechta sayyora bor?", "8", "7", "9", "10"), ("Quyoshga eng yaqin sayyora qaysi?", "Merkuriy", "Venera", "Yer", "Mars"),
     ("Yerning shakli qanday?", "Geoid (qutblarda yassilangan shar)", "Ideal shar", "Disk", "Kub"), ("Yer yuzasining necha foizini okean egallaydi?", "71 %", "29 %", "50 %", "90 %"),
     ("Quyosh tizimidagi eng katta sayyora?", "Yupiter", "Saturn", "Yer", "Neptun"), ("Ekvator uzunligi taxminan qancha?", "40 075 km", "4 000 km", "400 000 km", "12 756 km")],
    [("Yer Quyoshdan taxminan qancha uzoqlikda?", "150 mln km", "15 mln km", "1,5 mlrd km", "150 ming km"), ("Quruqlik sayyoralarga qaysi biri kiradi?", "Mars", "Yupiter", "Saturn", "Neptun"),
     ("Gaz giganti sayyoralarga qaysi biri kiradi?", "Saturn", "Merkuriy", "Venera", "Yer"), ("Yer yuzasining necha foizini quruqlik egallaydi?", "29 %", "71 %", "10 %", "50 %"),
     ("Yer yuzasining maydoni?", "510 mln km²", "51 mln km²", "5,1 mlrd km²", "149 mln km²"), ("Ekvator radiusi?", "6378 km", "6357 km", "12 756 km", "40 075 km"),
     ("Qutb radiusi?", "6357 km", "6378 km", "12 000 km", "4 000 km"), ("Yer qobiqlaridan qaysi biri suv qobig'i?", "Gidrosfera", "Litosfera", "Atmosfera", "Biosfera"),
     ("Yer qobiqlaridan qaysi biri hayot qobig'i?", "Biosfera", "Gidrosfera", "Litosfera", "Atmosfera"), ("Yerning qattiq qobig'i qanday ataladi?", "Litosfera", "Atmosfera", "Gidrosfera", "Biosfera"),
     ("Yer atmosferasi nima uchun muhim?", "Zararli nurlardan himoya qiladi va issiqlikni ushlaydi", "Faqat shamol hosil qiladi", "Faqat suv saqlaydi", "Hech qanday ahamiyati yo'q"),
     ("Yerning shar shaklda ekanini nima isbotlaydi?", "Kosmik suratlar va Oy tutilishidagi soya", "Faqat daryolar", "Faqat tog'lar", "Faqat shamollar"),
     ("Quyosh tizimi taxminan qancha yil oldin paydo bo'lgan?", "4,6 mlrd yil", "46 ming yil", "460 mln yil", "4,6 yil"), ("Ichki sayyoralar qanday?", "Qattiq quruqlik sayyoralari", "Gaz gigantlari", "Muz sayyoralar", "Yulduzlar"),
     ("Saturnning o'ziga xos belgisi?", "Halqalar", "Yo'ldoshi yo'q", "Eng kichik sayyora", "Suvli okeanlar"), ("Yerdan keyingi (Quyoshdan uzoqlashish tartibida) sayyora?", "Mars", "Venera", "Merkuriy", "Yupiter"),
     ("Geografiya nimani o'rganadi?", "Yer qobiqlari va ular orasidagi aloqalarni", "Faqat yulduzlarni", "Faqat tarixni", "Faqat sonlarni"), ("Magnit maydon Yerni nimadan himoya qiladi?", "Quyosh shamolidan", "Yomg'irdan", "Zilziladan", "Toshqindan"),
     ("Suyuq suv saqlanishi uchun nima muhim?", "Mos harorat (Quyoshdan optimal masofa)", "Juda yuqori harorat", "Juda past harorat", "Havosizlik")],
    gallery=[('g1_quyosh_tizimi', "Quyosh tizimi", ("Rasmda ko'rsatilgan eng katta sayyora qaysi?", "Yupiter", "Yer", "Mars", "Venera")),
             ('g1_yer_shakli', "Yerning shakli", ("Rasmdagi qizil gorizontal chiziq nimani bildiradi?", "Ekvator", "Meridian", "Tropik", "Qutb"))],
    extra={}))

TOPICS.append(topic(2, 'g1b', "2-mavzu. Yerning harakatlari va ularning natijalari",
    ["Yerning o'z o'qi atrofida va Quyosh atrofida harakatini farqlash", "Kecha-kunduz va fasllar almashinuvi sabablarini tushuntirish", "Tengkunlik va quyosh turish kunlarini bilish"],
    [("O'z o'qi atrofida aylanish", "Yer o'z o'qi atrofida g'arbdan sharqqa tomon 23 soat 56 daqiqada (yulduz sutkasi), Quyosh sutkasi hisobida esa 24 soatda bir marta aylanadi. Ekvatorda aylanish chiziqli tezligi soatiga taxminan 1670 km, qutblarda esa nolga yaqin. Natijada kecha va kunduz almashadi, Quyosh sharqdan chiqib g'arbda botadi, harakatlanayotgan jismlar (shamol, daryo) Koriolis kuchi ta'sirida og'adi: Shimoliy yarimsharda o'ngga, Janubiyda chapga.", 'g1_kecha_kunduz', "Yerning aylanishi: yoritilgan va qorong'i yarim"),
     ("Quyosh atrofida aylanish", "Yer Quyosh atrofida ellips shaklidagi orbita bo'ylab 365 sutka 6 soatda bir marta aylanadi — bu bir yil. Har to'rt yilda ortiqcha soatlar yig'ilib, fevral 29 kunli bo'ladi (kabisa yil). Orbita bo'ylab tezlik taxminan 30 km/s. Yer o'qi orbita tekisligiga nisbatan 66,5° og'ma va shu yo'nalishini saqlab, Quyosh atrofida harakatlanadi.", 'g1_fasllar', "Fasllar almashinuvi"),
     ("Fasllar va yorug'lik", "Yer o'qining og'maligi sababli yil davomida Quyosh nurlari turli kenglikka turlicha burchak ostida tushadi. 22 iyunda (yozgi turish) Shimoliy yarimshar Quyoshga qaragan: u yerda yoz, kunlar eng uzun; 22 dekabrda (qishki turish) aksincha. 21 mart va 23 sentyabrda (tengkunliklar) Quyosh ekvator ustida, hamma joyda kecha va kunduz teng. Ekvatorda kun-tun yil bo'yi deyarli teng, qutbda esa yarim yil kun, yarim yil tun (qutb kuni va tuni)."),
     ("Quyosh balandligi", "Quyoshning tush paytidagi balandligi: h = 90° − |φ − δ|, bunda φ — joyning kengligi, δ — Quyosh og'ish burchagi (22 iyunda +23,5°, 22 dekabrda −23,5°, tengkunlikda 0°). Masalan, Toshkent (φ ≈ 41°) da 22 iyunda tush paytida Quyosh balandligi 90° − (41° − 23,5°) = 72,5°, 22 dekabrda 90° − (41° + 23,5°) = 25,5°.")],
    ["Yer o'z o'qi atrofida 24 soatda bir marta aylanadi (kecha-kunduz).", "Quyosh atrofida 365 sutka 6 soatda aylanadi (yil).", "Yer o'qi 66,5° og'ma — shu sababli fasllar bor.", "Tengkunlik: 21 mart va 23 sentyabr.", "Quyosh turish kunlari: 22 iyun va 22 dekabr.", "Koriolis kuchi: Shimolda o'ngga, Janubda chapga og'diradi."],
    "Yerning aylanishi kecha-kunduzni, Quyosh atrofidagi harakati va o'qining og'maligi esa fasllarni hosil qiladi.",
    [("Yer o'z o'qi atrofida qancha vaqtda bir marta aylanadi (Quyosh sutkasi)?", "24 soat", "12 soat", "365 kun", "30 kun"), ("Yer Quyosh atrofida qancha vaqtda aylanadi?", "365 sutka 6 soat", "24 soat", "30 kun", "10 yil"),
     ("Fasllar nima sababdan almashadi?", "Yer o'qining og'maligi va Quyosh atrofida aylanishi", "Yerning Quyoshga yaqinlashishi", "Oy ta'siri", "Shamollar"), ("Kuzgi tengkunlik qachon?", "23 sentyabr", "21 mart", "22 iyun", "22 dekabr"),
     ("Shimoliy yarimsharda eng uzun kun qachon?", "22 iyun", "22 dekabr", "21 mart", "23 sentyabr"), ("Kabisa yilda fevral necha kun?", "29", "28", "30", "31")],
    [("Yer qaysi yo'nalishda aylanadi?", "G'arbdan sharqqa", "Sharqdan g'arbga", "Shimoldan janubga", "Janubdan shimolga"), ("Yer o'qining og'ish burchagi (orbitaga nisbatan)?", "66,5°", "23,5° (orbitaga)", "90°", "0°"),
     ("Koriolis kuchi Shimoliy yarimsharda jismlarni qayoqqa og'diradi?", "O'ngga", "Chapga", "Yuqoriga", "Og'dirmaydi"), ("21 mart nima deyiladi?", "Bahorgi tengkunlik", "Yozgi turish", "Kuzgi tengkunlik", "Qishki turish"),
     ("22 dekabr nima deyiladi?", "Qishki turish", "Yozgi turish", "Bahorgi tengkunlik", "Kuzgi tengkunlik"), ("Tengkunlikda kun va tun qanday bo'ladi?", "Teng", "Kun uzun", "Tun uzun", "Tun bo'lmaydi"),
     ("Ekvatorda kun va tun yil bo'yi qanday?", "Deyarli teng", "Kun uzun", "Tun uzun", "Kun bo'lmaydi"), ("Qutb kuni nima?", "Yarim yil davom etadigan yorug' vaqt", "Bir soatlik kun", "Oy yorug'i", "Yozning boshi"),
     ("Orbita bo'ylab Yer tezligi taxminan qancha?", "30 km/s", "3 km/s", "300 km/s", "0,3 km/s"), ("Yil davomida 4 ta muhim sana nima deyiladi?", "Tengkunlik va turish kunlari", "Bayramlar", "Oy fazalari", "Tutilishlar"),
     ("Quyosh tush paytidagi balandligi formulasi?", "h = 90° − |φ − δ|", "h = φ + δ", "h = 90° + φ", "h = δ − φ"), ("22 iyunda δ nechaga teng?", "+23,5°", "−23,5°", "0°", "90°"),
     ("Toshkent (41° sh.k.) da 22 iyunda tush paytida Quyosh balandligi?", "72,5°", "25,5°", "90°", "41°"), ("Toshkentda 22 dekabrda tush paytida Quyosh balandligi?", "25,5°", "72,5°", "41°", "0°"),
     ("Ekvatorda Yer aylanish tezligi taxminan?", "1670 km/soat", "167 km/soat", "16 700 km/soat", "0 km/soat"), ("Kabisa yil necha yilda bir marta?", "4 yilda", "2 yilda", "10 yilda", "100 yilda"),
     ("Fasllar almashishi Yerning Quyoshga yaqin-uzoqligidan emas, nimadan?", "O'q og'maligidan", "Oy tortishidan", "Okeandan", "Vulqonlardan"), ("Quyosh sharqdan chiqishi nima bilan bog'liq?", "Yerning g'arbdan sharqqa aylanishi", "Quyoshning harakati", "Oy harakati", "Shamol")],
    gallery=[('g1_fasllar', "Yerning Quyosh atrofidagi orbitasi", ("Rasmda 22 dekabr (pastki holat) Shimoliy yarimshar uchun qaysi fasl?", "Qish", "Yoz", "Bahor", "Kuz")),
             ('g1_kecha_kunduz', "Yoritilgan va qorong'i yarimshar", ("Kecha-kunduz almashinuvi nimaning natijasi?", "Yerning o'z o'qi atrofida aylanishi", "Yerning Quyosh atrofida aylanishi", "Oy harakati", "Shamollar"))]))

TOPICS.append(topic(3, 'g1c', "3-mavzu. Geografik koordinatalar va vaqt",
    ["Parallel, meridian, kenglik va uzunlik tushunchalarini bilish", "Nuqtaning geografik koordinatalarini aniqlash", "Mintaqaviy vaqtni hisoblash"],
    [("Parallellar va meridianlar", "Parallellar — ekvatorga parallel aylanalar; ular sharqdan g'arbga yo'nalgan. Asosiy parallel — ekvator (0°). Muhim parallellar: tropiklar (23,5°) va qutb doiralari (66,5°). Meridianlar — qutblarni tutashtiruvchi yarim aylanalar; asosiy (nolinchi) meridian Londonning Grinvich rasadxonasi orqali o'tadi. Ekvator Yerni Shimoliy va Janubiy yarimsharlarga, Grinvich meridiani (0° va 180°) Sharqiy va G'arbiy yarimsharlarga bo'ladi.", 'g1_setka', "Parallellar va meridianlar"),
     ("Geografik kenglik va uzunlik", "Geografik kenglik — nuqtaning ekvatordan burchak masofasi (0° dan 90° gacha, shimoliy yoki janubiy). Geografik uzunlik — nolinchi meridiandan burchak masofasi (0° dan 180° gacha, sharqiy yoki g'arbiy). Ikkalasi birga geografik koordinatalarni beradi. Toshkent: taxminan 41° sh.k., 69° sh.u.; Samarqand: 39,6° sh.k., 67° sh.u.; Nukus: 42,5° sh.k., 59,6° sh.u. 1° kenglik uzunligi taxminan 111 km."),
     ("Mintaqaviy vaqt", "Yer sutkada 360° ga aylangani uchun har 15° da Quyosh vaqti 1 soatga farq qiladi. Qulaylik uchun Yer 24 ta vaqt mintaqasiga bo'lingan; nolinchi mintaqa — Grinvich vaqti (UTC). Sharq tomonga vaqt ilgarilaydi (+), g'arbga ortda qoladi (−). O'zbekiston UTC+5 mintaqasida. Masalan, Toshkentda soat 12:00 bo'lsa, Londonda (UTC) 07:00, Moskvada (UTC+3) 10:00, Pekinda (UTC+8) 15:00.", 'g1_vaqt', "Vaqt mintaqalari"),
     ("Sana chizig'i", "180-meridian bo'ylab xalqaro sana chizig'i o'tadi: uni g'arbdan sharqqa kesib o'tilsa, sana bir kunga orqaga, sharqdan g'arbga kesib o'tilsa, bir kunga oldinga suriladi. Shu sababli 180° sharqiy yarimshardagi sana g'arbiy yarimshardagidan bir kun ilgari bo'ladi.")],
    ["Ekvator 0° kenglik; Grinvich 0° uzunlik.", "Kenglik 0–90° (sh/j), uzunlik 0–180° (sh/g').", "Tropiklar 23,5°, qutb doiralari 66,5°.", "15° uzunlik = 1 soat vaqt farqi.", "O'zbekiston UTC+5 mintaqasida.", "1° kenglik ≈ 111 km."],
    "Geografik koordinatalar (kenglik va uzunlik) har qanday nuqtani aniqlaydi, uzunlik farqi esa vaqt farqini beradi.",
    [("Ekvator qanday kenglikda?", "0°", "23,5°", "66,5°", "90°"), ("Nolinchi meridian qaysi shahar orqali o'tadi?", "Grinvich (London)", "Parij", "Moskva", "Toshkent"),
     ("Geografik kenglik qaysi oraliqda?", "0°–90°", "0°–180°", "0°–360°", "0°–45°"), ("15° uzunlik farqi qancha vaqt farqini beradi?", "1 soat", "15 daqiqa", "24 soat", "1 daqiqa"),
     ("O'zbekiston qaysi vaqt mintaqasida?", "UTC+5", "UTC+3", "UTC+8", "UTC"), ("Qutb doirasi qanday kenglikda?", "66,5°", "23,5°", "0°", "45°")],
    [("Tropik qanday kenglikda?", "23,5°", "66,5°", "0°", "90°"), ("Parallel nima?", "Ekvatorga parallel aylana", "Qutblarni tutashtiruvchi chiziq", "Daryo", "Tog' tizmasi"),
     ("Meridian nima?", "Qutblarni tutashtiruvchi yarim aylana", "Ekvatorga parallel aylana", "Dengiz qirg'og'i", "Chegara"), ("Geografik uzunlik qaysi oraliqda?", "0°–180°", "0°–90°", "0°–360° faqat", "0°–45°"),
     ("Toshkentning taxminiy kengligi?", "41° sh.k.", "69° sh.k.", "21° sh.k.", "10° j.k."), ("Toshkentning taxminiy uzunligi?", "69° sh.u.", "41° sh.u.", "10° g'.u.", "120° sh.u."),
     ("1° kenglik uzunligi taxminan?", "111 km", "11 km", "1110 km", "1 km"), ("Toshkentda 12:00 bo'lsa, Londonda (UTC) soat nechta?", "07:00", "17:00", "12:00", "05:00"),
     ("Toshkentda 12:00 bo'lsa, Moskvada (UTC+3) soat nechta?", "10:00", "14:00", "12:00", "09:00"), ("Toshkentda 12:00 bo'lsa, Pekinda (UTC+8) soat nechta?", "15:00", "09:00", "12:00", "20:00"),
     ("Yer nechta vaqt mintaqasiga bo'lingan?", "24", "12", "36", "15"), ("Sharqqa borganda vaqt qanday o'zgaradi?", "Ilgarilaydi", "Ortda qoladi", "O'zgarmaydi", "To'xtaydi"),
     ("Xalqaro sana chizig'i qaysi meridian bo'ylab o'tadi?", "180°", "0°", "90°", "45°"), ("Ekvator Yerni nimalarga bo'ladi?", "Shimoliy va Janubiy yarimsharlarga", "Sharqiy va G'arbiy yarimsharlarga", "Materiklarga", "Okeanlarga"),
     ("Qutb doirasi qaysi yarimsharlarda bor?", "Ikkalasida (66,5° sh. va j.)", "Faqat shimoliy", "Faqat janubiy", "Yo'q"), ("Nuqtaning koordinatalari nimadan iborat?", "Kenglik va uzunlik", "Faqat balandlik", "Faqat chuqurlik", "Faqat masofa"),
     ("Samarqand qaysi kenglikka yaqin?", "39,6° sh.k.", "50° sh.k.", "20° sh.k.", "60° sh.k."), ("Quyosh vaqti har 15° da necha soatga farq qiladi?", "1 soat", "2 soat", "30 daqiqa", "15 soat")],
    gallery=[('g1_setka', "Parallellar va meridianlar", ("Rasmda qizil qalin chiziq qaysi parallel?", "Ekvator", "Shimol tropigi", "Janub tropigi", "Qutb doirasi")),
             ('g1_vaqt', "Vaqt mintaqalari", ("Grinvich vaqtidan sharq tomonga har bir mintaqada vaqt qancha o'zgaradi?", "+1 soat", "−1 soat", "+15 soat", "O'zgarmaydi"))],
    extra={'problems': [
        {'question': "Toshkentda soat 15:00. Londonda (UTC) soat nechta? (soat:daqiqa, masalan 09:00)", 'answer': '10:00', 'hint': "Toshkent UTC+5.", 'solution': "15:00 − 5 soat = 10:00"},
        {'question': "Nuqta 60° sh.u. da joylashgan. U Grinvichdan necha soatlik vaqt farqida (UTC dan ilgari)?", 'answer': '4', 'hint': "60° : 15°", 'solution': "60 : 15 = 4 soat"},
        {'question': "Ikki shahar bir meridian bo'ylab, kengliklari 40° va 50° sh.k. Ular orasidagi masofa necha km (1° ≈ 111 km)?", 'answer': '1110', 'solution': "10 · 111 = 1110 km"}],
        'matching': [{'left': 'Ekvator', 'right': '0° kenglik'}, {'left': 'Grinvich', 'right': '0° uzunlik'}, {'left': 'Tropik', 'right': '23,5° kenglik'}, {'left': 'Qutb doirasi', 'right': '66,5° kenglik'}, {'left': 'UTC+5', 'right': "O'zbekiston vaqti"}, {'left': '15°', 'right': '1 soat farq'}]}))

TOPICS.append(topic(4, 'g1d', "4-mavzu. Xarita, masshtab va yo'nalish",
    ["Masshtab turlarini bilish va hisoblash", "Gorizontallar va shartli belgilarni o'qish", "Azimut va yo'nalishlarni aniqlash"],
    [("Xarita va uning turlari", "Xarita — Yer yuzasining kichraytirilgan, shartli belgilar bilan tasvirlangan yassi tasviri. Mazmuniga ko'ra umumgeografik va tematik (iqlim, siyosiy, aholi) xaritalar bo'ladi; qamrab olgan hududiga ko'ra dunyo, materik, davlat, viloyat xaritalari mavjud. Yer yuzasini yassi qog'ozga tushirishda kartografik proyeksiyalar qo'llanadi, shuning uchun har bir xaritada qandaydir buzilish bor."),
     ("Masshtab", "Masshtab — xaritadagi masofaning yerdagi haqiqiy masofaga nisbati. Turlari: sonli (1 : 100 000), nomli (1 sm da 1 km) va chiziqli (kesma). Masshtab yirik bo'lsa (kasr maxraji kichik), joy batafsil ko'rsatiladi. Hisob: haqiqiy masofa = xaritadagi masofa × masshtab maxraji. Misol: 1 : 100 000 masshtabli xaritada 4,5 sm masofa yerda 4,5 · 100 000 sm = 450 000 sm = 4,5 km.", 'g1_masshtab', "Masshtab turlari"),
     ("Relyefni ko'rsatish", "Balandlik va chuqurlikni xaritada ko'rsatishning asosiy usuli — gorizontallar: bir xil balandlikdagi nuqtalarni tutashtiruvchi yopiq egri chiziqlar. Gorizontallar zich joylashgan yonbag'ir tik, siyrak joylashgani yotiq bo'ladi. Umumiy xaritalarda qatlamli bo'yash (bosqichli rang) qo'llanadi: pastlik — yashil, balandlik — jigarrang va oq. Nuqtaviy belgi sifatida absolyut balandlik (dengiz sathidan) raqam bilan yoziladi.", 'g1_gorizontal', "Gorizontallar (tepalik)"),
     ("Yo'nalish va azimut", "Asosiy yo'nalishlar: shimol, janub, sharq, g'arb; oraliq yo'nalishlar: shimoli-sharq, janubi-sharq va h.k. Kompas strelkasi Yerning magnit maydoni tufayli shimolni ko'rsatadi. Azimut — shimol yo'nalishidan soat strelkasi bo'yicha ob'ektgacha hisoblangan burchak (0°–360°): shimol 0°, sharq 90°, janub 180°, g'arb 270°. Xaritada yo'nalish yuqori — shimol, o'ng — sharq qoidasi bilan aniqlanadi.")],
    ["Masshtab = xarita masofasi : yerdagi masofa.", "Yirik masshtab — batafsil, mayda masshtab — umumiy tasvir.", "Gorizontallar — bir xil balandlikdagi nuqtalarni tutashtiruvchi chiziqlar.", "Azimut: shimol 0°, sharq 90°, janub 180°, g'arb 270°.", "Absolyut balandlik dengiz sathidan hisoblanadi.", "Barcha xaritalarda proyeksiya tufayli buzilish bor."],
    "Xarita Yerni kichraytirib ko'rsatadi; masshtab, gorizontal va azimut yordamida masofa, balandlik va yo'nalish aniqlanadi.",
    [("1 : 100 000 masshtabda xaritadagi 1 sm yerda nechaga teng?", "1 km", "100 m", "10 km", "100 km"), ("Gorizontallar nimani ko'rsatadi?", "Relyefni (balandlikni)", "Aholini", "Iqlimni", "Chegarani"),
     ("Azimut janub yo'nalishi uchun qancha?", "180°", "90°", "270°", "0°"), ("Xaritada yuqori tomon odatda qayoqni ko'rsatadi?", "Shimolni", "Janubni", "Sharqni", "G'arbni"),
     ("Qaysi masshtab yirikroq?", "1 : 10 000", "1 : 1 000 000", "1 : 50 000 000", "1 : 100 000 000"), ("Gorizontallar zich joylashgan yonbag'ir qanday?", "Tik", "Yotiq", "Tekis", "Suvli")],
    [("Masshtab nima?", "Xarita masofasining yerdagi masofaga nisbati", "Xarita rangi", "Xarita sarlavhasi", "Yo'nalish"), ("1 : 1 000 000 masshtabda 1 sm yerda nechaga teng?", "10 km", "1 km", "100 km", "1000 km"),
     ("1 : 100 000 masshtabda 4,5 sm masofa yerda necha km?", "4,5 km", "45 km", "0,45 km", "450 km"), ("Chiziqli masshtab nima?", "Kesma ko'rinishidagi masshtab", "Sonli nisbat", "Nomli masshtab", "Gorizontal"),
     ("Sonli masshtab misoli?", "1 : 500 000", "1 sm da 5 km", "Kesma", "5 km"), ("Mayda masshtabli xaritaga qaysi biri misol?", "Dunyo xaritasi", "Shahar rejasi", "Hovli rejasi", "Xona rejasi"),
     ("Gorizontal nima?", "Bir xil balandlikdagi nuqtalarni tutashtiruvchi chiziq", "Daryo yo'nalishi", "Chegara chizig'i", "Yo'l"), ("Absolyut balandlik nimadan hisoblanadi?", "Dunyo okeani sathidan", "Yer markazidan", "Eng baland tog'dan", "Shahardan"),
     ("Azimut shimol uchun?", "0°", "90°", "180°", "270°"), ("Azimut sharq uchun?", "90°", "0°", "180°", "270°"), ("Azimut g'arb uchun?", "270°", "90°", "180°", "0°"),
     ("Kompas strelkasi nimani ko'rsatadi?", "Magnit shimolni", "Sharqni", "Janubni", "Quyoshni"), ("Umumiy xaritada pastlik odatda qanday rangda?", "Yashil", "Oq", "Qora", "Qizil"),
     ("Tematik xaritaga qaysi biri misol?", "Iqlim xaritasi", "Faqat kompas", "Globus", "Rasm"), ("Siyosiy xarita nimani ko'rsatadi?", "Davlatlar va chegaralarni", "Faqat relyefni", "Faqat iqlimni", "Faqat o'simlikni"),
     ("Xaritalarda buzilishlar nega bor?", "Yer shar, xarita esa yassi", "Xato chizilgani uchun", "Kompas tufayli", "Masshtab yo'qligi"), ("Shartli belgilar xaritada nima uchun kerak?", "Ob'ektlarni ixcham ko'rsatish", "Bezak uchun", "Rangni almashtirish", "Masshtabni o'zgartirish"),
     ("Qatlamli bo'yash usuli nimani ko'rsatadi?", "Balandlik zonalarini", "Aholi sonini", "Yo'l uzunligini", "Daryo oqimini")],
    gallery=[('g1_masshtab', "Masshtab turlari", ("1 : 100 000 masshtab nomli ko'rinishda qanday?", "1 sm da 1 km", "1 sm da 100 m", "1 sm da 10 km", "1 mm da 1 km")),
             ('g1_gorizontal', "Tepalik gorizontallari", ("Rasmda tepalikning eng baland nuqtasi qancha?", "420 m", "100 m", "300 m", "200 m"))],
    extra={'problems': [
        {'question': "Xaritada ikki shahar orasidagi masofa 6 sm, masshtab 1 : 500 000. Yerdagi masofa necha km?", 'answer': '30', 'hint': "6 · 500 000 sm", 'solution': "3 000 000 sm = 30 km"},
        {'question': "Yerdagi 20 km masofa 1 : 200 000 masshtabli xaritada necha sm bo'ladi?", 'answer': '10', 'solution': "20 km = 2 000 000 sm; 2 000 000 : 200 000 = 10 sm"},
        {'question': "Masofa xaritada 3 sm, yerda 15 km. Masshtab maxrajini toping (1 : ?). Faqat sonni yozing.", 'answer': ['500000', '500 000'], 'solution': "15 km = 1 500 000 sm; 1 500 000 : 3 = 500 000"}],
        'matching': [{'left': "Masshtab", 'right': "Xarita va yer masofasi nisbati"}, {'left': "Gorizontal", 'right': "Bir xil balandlik chizig'i"}, {'left': "Azimut", 'right': "Shimoldan soat yo'nalishida burchak"}, {'left': "Kompas", 'right': "Magnit shimolni ko'rsatadi"}, {'left': "Proyeksiya", 'right': "Yerni yassi xaritaga tushirish usuli"}]}))
