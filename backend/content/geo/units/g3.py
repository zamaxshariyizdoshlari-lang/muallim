# -*- coding: utf-8 -*-
import math
from dsl import topic
from svglib import *

IMAGES = {}
TOPICS = []


def _qatlamlar():
    return layers('Atmosfera qatlamlari', [
        ("Ekzosfera", "800 km dan yuqori, havo juda siyrak", '#1e293b', 10),
        ("Termosfera", "85–800 km, shimol yog'dulari, yo'ldoshlar", '#4338ca', 14),
        ("Mezosfera", "50–85 km, meteorlar yonadi (−90 °C)", '#6366f1', 12),
        ("Stratosfera", "12–50 km, ozon qatlami (20–25 km)", '#38bdf8', 22),
        ("Troposfera", "0–12 km, ob-havo shu yerda (havoning 80 %)", '#bae6fd', 24)],
        note="Troposferada balandlik oshgani sari harorat har 1 km da ~6 °C pasayadi")


def _havo_tarkibi():
    return pie('Atmosfera havosi tarkibi', [('Azot (N₂)', 78), ('Kislorod (O₂)', 21), ('Argon, CO₂ va boshqalar', 1)],
               note="Karbonat angidrid ~0,04 %, ammo issiqxona effekti uchun muhim")


def _harorat_balandlik():
    return linechart('Harorat balandlik bo\'yicha (o\'rtacha)', ['0', '12', '25', '50', '85', '100'], [15, -56, -50, -2, -90, -60],
                     'Balandlik (km)', 'Harorat (°C)', labels=[(1, 'tropopauza'), (3, 'stratopauza'), (4, 'mezopauza')])


def _issiqlik():
    return flow('Havo qanday isiydi?', [('Quyosh nuri', 'qisqa to\'lqin'), ('Yer yuzasi isiydi', 'nur yutiladi'), ('Yer issiqlik chiqaradi', 'uzun to\'lqin'), ('Havo pastdan isiydi', 'troposfera')],
                note="Atmosfera havosi Quyosh nuridan emas, asosan isigan Yer yuzasidan isiydi")


def _bosim_balandlik():
    return linechart('Atmosfera bosimi balandlik bo\'yicha', ['0', '1', '2', '3', '5', '8'], [1013, 899, 795, 701, 540, 356], 'Balandlik (km)', 'Bosim (gPa)', labels=[(0, 'dengiz sathi'), (5, 'Everest ~300 gPa')])


def _harorat_kenglik():
    return linechart('Yillik o\'rtacha harorat kenglik bo\'yicha', ['0°', '20°', '40°', '60°', '80°'], [26, 24, 12, -1, -16], 'Kenglik (shimoliy yarimshar)', 'Harorat (°C)', labels=[(0, 'Ekvator'), (4, 'Qutb')])


def _shamol_aylanma():
    def ov(P):
        o = []
        for lat, lon0, lon1, col, lab in ((15, 150, 40, '#2563eb', 'Passat'), (45, -150, -60, '#16a34a', "G'arbiy shamollar"), (75, 100, 20, '#7c3aed', 'Qutb sharqiy'),
                                         (-15, 150, 40, '#2563eb', ''), (-45, -150, -60, '#16a34a', ''), (-75, 100, 20, '#7c3aed', '')):
            ax, ay = P(lon0, lat)
            bx, by = P(lon1, lat)
            o.append(line(ax, ay, bx, by, col, 3.5, arrow=True))
        return ''.join(o)
    return world('Global shamollar sxemasi', overlay=ov, grid=True,
                 labels=[(-120, 12, 'Passat (sharqdan)'), (-110, 50, "G'arbiy shamollar"), (60, 80, 'Qutb sharqiy shamollari'), (-110, -50, "G'arbiy shamollar"), (-120, -12, 'Passat')],
                 legend=[('#2563eb', 'Passatlar (tropiklarda)'), ('#16a34a', "G'arbiy shamollar"), ('#7c3aed', 'Qutb sharqiy')])


def _briz():
    out = [ARROW_DEF]
    for i, (t, a, b) in enumerate((('Kunduzgi briz (dengizdan quruqlikka)', 'sovuq havo', 'issiq havo ko\'tariladi'), ('Tungi briz (quruqlikdan dengizga)', 'issiq havo ko\'tariladi', 'sovuq havo'))):
        x = 20 + i * 350
        out.append(box(x, 60, 330, 300, '#f0f9ff', '#94a3b8', rx=12))
        out.append(T(x + 165, 85, t, 12, INK, weight='700'))
        out.append(box(x + 10, 290, 150, 60, '#60a5fa', rx=4))
        out.append(box(x + 160, 290, 160, 60, '#c4a574', rx=4))
        out.append(T(x + 85, 325, 'Dengiz', 12, '#fff', weight='700'))
        out.append(T(x + 240, 325, 'Quruqlik', 12, INK, weight='700'))
        if i == 0:
            out.append(line(x + 90, 270, x + 240, 270, '#2563eb', 3, arrow=True))
            out.append(line(x + 240, 250, x + 240, 140, '#dc2626', 3, arrow=True))
            out.append(line(x + 240, 130, x + 90, 130, '#2563eb', 3, arrow=True))
            out.append(line(x + 90, 140, x + 90, 250, '#2563eb', 3, arrow=True))
        else:
            out.append(line(x + 240, 270, x + 90, 270, '#2563eb', 3, arrow=True))
            out.append(line(x + 90, 250, x + 90, 140, '#dc2626', 3, arrow=True))
            out.append(line(x + 90, 130, x + 240, 130, '#2563eb', 3, arrow=True))
            out.append(line(x + 240, 140, x + 240, 250, '#2563eb', 3, arrow=True))
        out.append(T(x + 165, 200, 'bosim farqi', 11, MUTED))
    return svg('Briz shamollari', ''.join(out))


def _namlik():
    return linechart('Havoning maksimal namlik sig\'imi', ['−10°', '0°', '10°', '20°', '30°'], [2.1, 4.8, 9.4, 17.3, 30.4], 'Harorat', 'Suv bug\'i (g/m³)', labels=[(3, '20 °C: 17 g/m³'), (4, 'issiq havo ko\'proq namlik oladi')])


def _orografik():
    return profile('Tog\' oldi yog\'inlari (orografik)', [(0, 4), (20, 6), (45, 60), (52, 90), (60, 60), (75, 12), (100, 8)],
                   [(22, 40, 'Nam shamol →'), (30, 70, 'Yog\'in ko\'p'), (78, 40, 'Yog\'in kam (yomg\'ir soyasi)'), (52, 98, 'Tog\' tizmasi')])


def _iqlim_mintaqalar():
    return zones('Iqlim mintaqalari (kenglik bo\'yicha)', [
        ('Arktika (qutb) mintaqasi', 'juda sovuq, quruq', '#e0f2fe', 90, 66.5), ('Subarktika', 'qisqa sovuq yoz', '#bfdbfe', 66.5, 55),
        ('Mo\'tadil', 'to\'rt fasl, o\'rtacha yog\'in', '#bbf7d0', 55, 40), ('Subtropik', 'quruq issiq yoz, yumshoq qish', '#fef08a', 40, 23.5),
        ('Tropik', 'issiq va quruq (cho\'llar)', '#fdba74', 23.5, 10), ('Subekvatorial', 'nam va quruq mavsum', '#fde68a', 10, 5), ('Ekvatorial', 'doim issiq va nam', '#86efac', 5, -5)],
        note='Janubiy yarimsharda mintaqalar simmetrik takrorlanadi')


def _iqlimogramma():
    xs = ['Y', 'F', 'M', 'A', 'M', 'I', 'I', 'A', 'S', 'O', 'N', 'D']
    return linechart('Toshkent iqlimogrammasi (taxminiy)', xs, [-1, 1, 8, 15, 21, 26, 28, 26, 20, 13, 6, 1], 'Oylar', 'Harorat (°C)',
                     bars_y=[40, 45, 60, 55, 35, 15, 5, 2, 6, 30, 40, 45], labels=[(6, 'Iyul ~28 °C'), (0, 'Yanvar ~ −1 °C')])


def _iqlim_dunyo():
    def ov(P):
        cols = [(90, 66.5, '#bfdbfe'), (66.5, 50, '#93c5fd'), (50, 35, '#86efac'), (35, 23.5, '#fde047'), (23.5, 8, '#fdba74'), (8, -8, '#4ade80'), (-8, -23.5, '#fdba74'), (-23.5, -35, '#fde047'), (-35, -50, '#86efac'), (-50, -66.5, '#93c5fd'), (-66.5, -90, '#bfdbfe')]
        o = []
        for a, b, col in cols:
            p1, p2 = P(-180, a), P(180, b)
            o.append(f'<rect x="{p1[0]:.1f}" y="{p1[1]:.1f}" width="{p2[0]-p1[0]:.1f}" height="{p2[1]-p1[1]:.1f}" fill="{col}" opacity="0.45"/>')
        return ''.join(o)
    return world('Iqlim mintaqalari xaritasi (sxematik)', overlay=ov, legend=[('#bfdbfe', 'Qutb'), ('#93c5fd', 'Subarktika'), ('#86efac', "Mo'tadil"), ('#fde047', 'Subtropik'), ('#fdba74', 'Tropik'), ('#4ade80', 'Ekvatorial')])


IMAGES.update({'g3_qatlamlar': _qatlamlar(), 'g3_tarkib': _havo_tarkibi(), 'g3_harorat_balandlik': _harorat_balandlik(), 'g3_issiqlik': _issiqlik(), 'g3_bosim': _bosim_balandlik(),
               'g3_harorat_kenglik': _harorat_kenglik(), 'g3_shamollar': _shamol_aylanma(), 'g3_briz': _briz(), 'g3_namlik': _namlik(), 'g3_orografik': _orografik(),
               'g3_mintaqalar': _iqlim_mintaqalar(), 'g3_iqlimogramma': _iqlimogramma(), 'g3_iqlim_dunyo': _iqlim_dunyo()})

TOPICS.append(topic(9, 'g3a', "9-mavzu. Atmosfera tuzilishi va tarkibi",
    ["Atmosfera tarkibini bilish", "Atmosfera qatlamlarini ketma-ket sanash", "Troposferada harorat o'zgarishini hisoblash"],
    [("Atmosfera nima?", "Atmosfera — Yerni o'rab turgan havo qobig'i. Uning massasi Yer massasining milliondan bir qismidan kam bo'lsa-da, hayot uchun beqiyos ahamiyatga ega: nafas olish uchun kislorod beradi, zararli ultrabinafsha nurlardan (ozon qatlami) saqlaydi, issiqlikni ushlab turadi, suv aylanishida ishtirok etadi. Atmosferaning umumiy qalinligi 2000–3000 km, ammo havoning 99 % i dastlabki 30 km da.", 'g3_tarkib', "Atmosfera tarkibi"),
     ("Qatlamlar", "Atmosfera balandlik bo'yicha qatlamlarga bo'linadi: troposfera (0–8/18 km; qutbda 8–10, ekvatorda 16–18 km), stratosfera (50 km gacha; ozon qatlami 20–25 km da), mezosfera (85 km gacha), termosfera (800 km gacha, shimol yog'dulari) va ekzosfera. Ob-havo hodisalari, bulutlar va yog'in deyarli faqat troposferada. Troposferada harorat har 1 km balandlikda o'rtacha 6 °C pasayadi, stratosferada esa ozon ultrabinafsha nurni yutgani uchun ko'tariladi.", 'g3_qatlamlar', "Atmosfera qatlamlari"),
     ("Harorat balandlik bo'yicha", "Atmosfera harorati balandlik bo'yicha tekis o'zgarmaydi: troposferada pasayadi (tropopauzada ~−56 °C), stratosferada ozon hisobiga ko'tariladi (stratopauzada ~0 °C), mezosferada yana pasayadi (~−90 °C), termosferada sezilarli ortadi (yuzlab gradus, lekin havo juda siyrak). Qatlamlar orasidagi o'tish zonalari «-pauza» deb ataladi.", 'g3_harorat_balandlik', "Harorat va balandlik"),
     ("Ozon va havo muhofazasi", "Ozon qatlami (O₃) stratosferada Quyoshning zararli ultrabinafsha nurini yutadi. XX asr oxirida freonlar tufayli Antarktida ustida «ozon tuynugi» paydo bo'ldi; 1987-yilgi Monreal protokoli freonlar ishlatilishini taqiqladi va qatlam tiklana boshladi. Havo ifloslanishi (sanoat, transport, yoqilg'i) shahar aholisi salomatligiga zarar yetkazadi.")],
    ["Havo tarkibi: azot 78 %, kislorod 21 %, boshqalar 1 %.", "Qatlamlar: troposfera, stratosfera, mezosfera, termosfera, ekzosfera.", "Ob-havo troposferada shakllanadi.", "Troposferada harorat 1 km da ~6 °C pasayadi.", "Ozon qatlami stratosferada (20–25 km).", "Monreal protokoli (1987) ozonni himoya qiladi."],
    "Atmosfera havoning qatlamli qobig'i bo'lib, troposferada ob-havo shakllanadi, ozon qatlami esa ultrabinafsha nurdan saqlaydi.",
    [("Atmosferada eng ko'p gaz?", "Azot", "Kislorod", "Argon", "Karbonat angidrid"), ("Ob-havo qaysi qatlamda shakllanadi?", "Troposfera", "Stratosfera", "Mezosfera", "Termosfera"), ("Ozon qatlami qaysi qatlamda?", "Stratosfera", "Troposfera", "Termosfera", "Ekzosfera"),
     ("Troposferada har 1 km da harorat qanday o'zgaradi?", "6 °C pasayadi", "6 °C ko'tariladi", "O'zgarmaydi", "60 °C pasayadi"), ("Kislorod havoda necha foiz?", "21 %", "78 %", "1 %", "50 %"), ("Ozon qatlami nimadan saqlaydi?", "Ultrabinafsha nurlardan", "Yomg'irdan", "Shamoldan", "Zilziladan")],
    [("Havodagi azot ulushi?", "78 %", "21 %", "1 %", "0,04 %"), ("Troposferaning qutbdagi qalinligi taxminan?", "8–10 km", "50 km", "100 km", "1 km"), ("Troposferaning ekvatordagi qalinligi?", "16–18 km", "5 km", "50 km", "1 km"),
     ("Shimol yog'dulari qaysi qatlamda?", "Termosfera", "Troposfera", "Stratosfera", "Mezosfera"), ("Meteorlar qaysi qatlamda yonadi?", "Mezosfera", "Troposfera", "Ekzosfera", "Stratosfera"), ("Eng yuqori qatlam?", "Ekzosfera", "Troposfera", "Termosfera", "Stratosfera"),
     ("Ozon formulasi?", "O₃", "O₂", "CO₂", "N₂"), ("Ozon tuynugi qayerda paydo bo'lgan?", "Antarktida ustida", "Sahroda", "Amazonkada", "Himolayda"), ("Ozon tuynugiga nima sabab bo'lgan?", "Freonlar", "Vulqonlar", "Shamollar", "Yomg'ir"),
     ("Monreal protokoli yili?", "1987", "1887", "1997", "2007"), ("Havoning qancha qismi dastlabki 30 km da?", "99 %", "10 %", "50 %", "1 %"), ("Atmosfera qalinligi taxminan?", "2000–3000 km", "20 km", "200 m", "2 km"),
     ("Tropopauza qanday joy?", "Troposfera va stratosfera chegarasi", "Mezosfera cho'qqisi", "Yer yuzasi", "Okean"), ("Stratosferada harorat nega ko'tariladi?", "Ozon nurni yutadi", "Quyosh yaqin", "Suv bug'i ko'p", "Shamol ko'p"),
     ("Karbonat angidridning havodagi ulushi?", "~0,04 %", "21 %", "78 %", "10 %"), ("Atmosfera qaysi jarayonda ishtirok etadi?", "Suv aylanishida", "Faqat zilzilada", "Faqat vulqonda", "Hech qaysisida"), ("Havo massasi nimaga bog'liq?", "Balandlik oshgani sari kamayadi", "Doimiy", "Oshadi", "Nolga teng"),
     ("Havo ifloslanishining sababi?", "Sanoat va transport", "Faqat vulqon", "Faqat o'simlik", "Okean")],
    gallery=[('g3_qatlamlar', "Atmosfera qatlamlari", ("Rasmda ob-havo shakllanadigan qatlam qaysi?", "Troposfera", "Stratosfera", "Mezosfera", "Termosfera")),
             ('g3_tarkib', "Havo tarkibi", ("Diagrammada eng katta ulushli gaz?", "Azot", "Kislorod", "Argon", "CO₂")),
             ('g3_harorat_balandlik', "Harorat va balandlik", ("12 km balandlikdagi tropopauzada harorat qanday?", "Taxminan −56 °C", "+15 °C", "+100 °C", "0 °C"))],
    extra={'problems': [
        {'question': "Yer yuzida harorat +24 °C. Har 1 km da 6 °C pasaysa, 3 km balandlikda harorat necha °C?", 'answer': '6', 'solution': "24 − 18 = 6 °C"},
        {'question': "Tog' etagida +20 °C, cho'qqisida +2 °C. Cho'qqi balandligi (nisbiy) necha km (6 °C/km)?", 'answer': '3', 'solution': "18 : 6 = 3 km"},
        {'question': "Havoda 21 % kislorod bor. 200 litr havoda necha litr kislorod?", 'answer': '42', 'solution': "200 · 0,21 = 42"}],
        'matching': [{'left': 'Troposfera', 'right': 'Ob-havo hosil bo\'ladigan qatlam'}, {'left': 'Stratosfera', 'right': 'Ozon qatlami'}, {'left': 'Mezosfera', 'right': 'Meteorlar yonadi'}, {'left': 'Termosfera', 'right': 'Shimol yog\'dulari'}, {'left': 'Azot', 'right': 'Havoning 78 %'}, {'left': 'Freon', 'right': 'Ozonni yemiradi'}]}))

TOPICS.append(topic(10, 'g3b', "10-mavzu. Havo harorati va atmosfera bosimi",
    ["Havo isishi jarayonini tushuntirish", "Harorat amplitudasi va o'rtachasini hisoblash", "Atmosfera bosimi va uning o'zgarishini bilish"],
    [("Havoning isishi", "Quyosh nurlari atmosferadan deyarli to'siqsiz o'tib, Yer yuzasini isitadi; isigan yer yuzasi issiqlikni uzun to'lqinli nur sifatida qaytaradi va havo pastdan isiydi. Shu sababli balandlik oshgani sari havo sovuqroq bo'ladi. Yer yuzasining isishi nur tushish burchagiga, yuza turiga (qum tez isiydi, suv sekin isiydi, qor nurni qaytaradi) va bulutlarga bog'liq.", 'g3_issiqlik', "Havoning isishi"),
     ("Harorat ko'rsatkichlari", "Harorat termometr bilan o'lchanadi (Selsiy, Farengeyt, Kelvin). Kunlik o'rtacha harorat 4 yoki 24 ta o'lchov o'rtachasi. Kunlik amplituda — eng yuqori va eng past harorat farqi, yillik amplituda — eng issiq va eng sovuq oyning o'rtacha harorati farqi. Dengizdan uzoq (kontinental) hududlarda amplituda katta. Eng issiq joylar — Sahroi Kabir, Ko'k Vodiy (+56,7 °C); eng sovuq — Antarktida (Vostok −89,2 °C).", 'g3_harorat_kenglik', "Harorat kenglikka bog'liqligi"),
     ("Atmosfera bosimi", "Atmosfera bosimi — havoning Yer yuzasiga va undagi jismlarga bosimi. Dengiz sathida 0 °C da me'yoriy bosim 760 mm sim. ust. (1013 gPa). Balandlik oshgani sari bosim kamayadi: dastlabki kilometrlarda har 10,5 m da 1 mm sim. ust. (taxminan 100 m da 10 mm). Bosim barometr yoki aneroid bilan o'lchanadi. Havo issiq bo'lsa, ko'tarilib past bosim hosil qiladi; sovuq havo cho'kib yuqori bosim hosil qiladi.", 'g3_bosim', "Bosim balandlik bo'yicha"),
     ("Bosim kamarlari", "Yer yuzasida bosim kamarlari mavjud: ekvatorda past bosim (issiq havo ko'tariladi), tropiklar yaqinida (25–35°) yuqori bosim, mo'tadil kengliklarda (60° atrofida) past bosim, qutblarda yuqori bosim. Havo yuqori bosimdan past bosim tomon harakatlanadi — bu shamol. Bosim farqi qancha katta bo'lsa, shamol shuncha kuchli bo'ladi.")],
    ["Havo asosan isigan yer yuzasidan isiydi.", "Amplituda = eng yuqori − eng past harorat.", "Me'yoriy bosim: 760 mm sim. ust. (1013 gPa).", "Har 10,5 m balandlikda bosim ~1 mm sim. ust. kamayadi.", "Havo yuqori bosimdan past bosimga harakatlanadi (shamol).", "Eng sovuq joy: Vostok (−89,2 °C)."],
    "Havo yer yuzasidan isiydi; bosim balandlik bilan kamayadi, bosim farqi shamolni hosil qiladi.",
    [("Atmosfera havosi asosan nimadan isiydi?", "Isigan yer yuzasidan", "Oydan", "Yulduzlardan", "Okeandan sovishdan"), ("Me'yoriy atmosfera bosimi?", "760 mm sim. ust.", "76 mm sim. ust.", "7600 mm sim. ust.", "100 mm sim. ust."),
     ("Balandlik oshganda bosim?", "Kamayadi", "Oshadi", "O'zgarmaydi", "Nolga tushadi"), ("Amplituda nima?", "Eng yuqori va eng past harorat farqi", "O'rtacha harorat", "Eng past harorat", "Namlik"), ("Bosim qaysi asbobda o'lchanadi?", "Barometr", "Termometr", "Gigrometr", "Flyuger"), ("Ekvatorda bosim qanday?", "Past", "Yuqori", "Nol", "O'zgarmas")],
    [("Qum suvga nisbatan qanday isiydi?", "Tezroq", "Sekinroq", "Bir xil", "Isimaydi"), ("Qor Quyosh nurini qanday ta'sirlaydi?", "Ko'p qaytaradi", "Ko'p yutadi", "Hech", "Isitadi"), ("Eng sovuq harorat qayerda qayd etilgan?", "Antarktida (Vostok)", "Sahro", "Arktika", "Himolay"),
     ("1013 gPa necha mm sim. ust.?", "760", "100", "1013", "500"), ("Taxminan har 100 m ko'tarilishda bosim qancha kamayadi?", "~10 mm sim. ust.", "~100 mm", "~1 mm", "~500 mm"), ("Qutblarda bosim qanday?", "Yuqori", "Past", "Nol", "O'zgaruvchan"),
     ("Shamol nima?", "Havoning gorizontal harakati", "Havo tinchligi", "Yomg'ir", "Bulut"), ("Shamol qaysi yo'nalishda esadi?", "Yuqori bosimdan past bosimga", "Past bosimdan yuqoriga", "Har doim shimolga", "Har doim janubga"),
     ("Kontinental iqlimda amplituda?", "Katta", "Kichik", "Nol", "Doimiy"), ("Dengiz iqlimida amplituda?", "Kichik", "Katta", "Juda katta", "Nol"), ("Kelvin shkalasida mutlaq nol?", "0 K (−273,15 °C)", "100 K", "273 K", "−100 K"),
     ("Issiq havo qanday harakat qiladi?", "Ko'tariladi", "Cho'kadi", "Turadi", "Yon tomonga"), ("Sovuq havo nima hosil qiladi?", "Yuqori bosim", "Past bosim", "Vulqon", "Bulut"), ("Ko'k Vodiydagi rekord harorat?", "+56,7 °C", "+156 °C", "+16 °C", "0 °C"),
     ("Yillik amplituda nima?", "Eng issiq va sovuq oy farqi", "Kun farqi", "Yog'in miqdori", "Bosim farqi"), ("Eng yaxshi qaytaradigan sirt?", "Qor", "Qora tuproq", "Asfalt", "O'rmon"), ("Haroratni kim aniqlaydi?", "Termometr", "Barometr", "Kompas", "Metr")],
    gallery=[('g3_issiqlik', "Havoning isishi", ("Havo birinchi navbatda nimadan isiydi?", "Isigan yer yuzasidan", "Quyosh nuridan bevosita", "Oydan", "Shamoldan")),
             ('g3_bosim', "Bosim balandlik bo'yicha", ("Grafikda 5 km balandlikda bosim taxminan?", "540 gPa", "1013 gPa", "100 gPa", "700 gPa"))],
    extra={'problems': [
        {'question': "Kunduzi eng yuqori harorat +28 °C, kechasi eng past +12 °C. Kunlik amplituda necha °C?", 'answer': '16', 'solution': "28 − 12 = 16"},
        {'question': "Dengiz sathida bosim 760 mm. 420 m balandlikda (har 10,5 m da 1 mm) bosim necha mm sim. ust.?", 'answer': '720', 'hint': "420 : 10,5 = 40", 'solution': "760 − 40 = 720"},
        {'question': "Ertalab +10, tushda +22, kechqurun +16, tunda +8 °C. O'rtacha sutkalik harorat necha °C?", 'answer': '14', 'solution': "(10 + 22 + 16 + 8) : 4 = 14"}],
        'matching': [{'left': 'Barometr', 'right': "Bosimni o'lchaydi"}, {'left': 'Termometr', 'right': "Haroratni o'lchaydi"}, {'left': 'Amplituda', 'right': 'Eng yuqori va past harorat farqi'}, {'left': '760 mm', 'right': 'Me\'yoriy bosim'}, {'left': 'Shamol', 'right': 'Bosim farqidan havo harakati'}, {'left': 'Vostok', 'right': 'Eng sovuq joy'}]}))

TOPICS.append(topic(11, 'g3c', "11-mavzu. Shamollar va havo massalari",
    ["Shamol turlarini bilish", "Global shamol kamarlarini sanash", "Havo massalari va frontlarni tushunish"],
    [("Shamol va uning xarakteristikasi", "Shamol — havoning gorizontal harakati. U yo'nalishi (qaysi tomondan esishi), tezligi (m/s) va kuchi (ball, Bofort shkalasi 0–12) bilan tavsiflanadi. Shamol yo'nalishi shamol guli diagrammasida ko'rsatiladi. Tezlik 33 m/s dan oshsa — bo'ron (12 ball). Shamol yer aylanishi (Koriolis kuchi) va yer yuzasi ishqalanishi ta'sirida yo'nalishini o'zgartiradi."),
     ("Doimiy shamollar", "Yer yuzida doimiy shamollar bor: passatlar (tropiklardan ekvatorga, shimol yarimsharda shimoli-sharqdan, janubda janubi-sharqdan), g'arbiy shamollar (mo'tadil kengliklarda g'arbdan sharqqa — «bo'ronli qirq»), qutb sharqiy shamollari. Ular bosim kamarlari va Yer aylanishi natijasida shakllanadi. Passatlar yo'nalishi barqaror bo'lgani uchun burungi yelkanli kemalar okean kesib o'tgan.", 'g3_shamollar', "Global shamollar sxemasi"),
     ("Mahalliy shamollar", "Briz — dengiz va quruqlik qirg'og'ida kunduzi dengizdan quruqlikka, kechasi quruqlikdan dengizga esadigan shamol (kunduz quruqlik tezroq isiydi, past bosim hosil bo'ladi). Mussonlar — fasllar bo'yicha yo'nalishi o'zgaradigan shamollar (yozda okeandan quruqlikka — nam, qishda quruqlikdan okeanga — quruq): Hindiston, Janubi-Sharqiy Osiyoda. Fen — tog'dan oqib tushadigan issiq va quruq shamol; bora — sovuq shamol. O'zbekistonda «Afg'on», «Qo'zi» va «Bahorak» mahalliy shamollari bor.", 'g3_briz', "Briz shamollari"),
     ("Havo massalari va frontlar", "Havo massasi — harorat, namlik jihatidan bir xil katta havo hajmi. Turlari: arktik, mo'tadil, tropik, ekvatorial; shuningdek dengiz (nam) va kontinental (quruq). Ikki xil havo massasi chegarasi — front: iliq front (iliq havo sovuq havo ustiga chiqadi, ko'p yog'in, ob-havo asta o'zgaradi) va sovuq front (sovuq havo iliq havoni siqib chiqaradi, jala, momaqaldiroq, keskin sovish). Siklon (past bosim markazi) — yomg'irli, bulutli ob-havo; antisiklon (yuqori bosim) — ochiq, quruq.")],
    ["Shamol yo'nalishi va tezligi bilan tavsiflanadi.", "Doimiy: passat, g'arbiy shamollar, qutb sharqiy.", "Briz kunduzi dengizdan, kechasi quruqlikdan esadi.", "Mussonlar fasllar bo'yicha yo'nalishini o'zgartiradi.", "Front — ikki xil havo massasi chegarasi.", "Siklon — yog'in, antisiklon — ochiq ob-havo."],
    "Shamol bosim farqidan hosil bo'ladi; doimiy va mahalliy shamollar mavjud, havo massalari chegarasida frontlar vujudga keladi.",
    [("Shamol nima?", "Havoning gorizontal harakati", "Havoning vertikal harakati", "Bulut", "Yog'in"), ("Tropiklardan ekvatorga esadigan doimiy shamol?", "Passat", "Muson", "Briz", "Fen"), ("Kunduzgi briz qayerdan esadi?", "Dengizdan quruqlikka", "Quruqlikdan dengizga", "Tog'dan", "Cho'ldan"),
     ("Mussonlar nimasi bilan ajralib turadi?", "Fasllar bo'yicha yo'nalishi o'zgaradi", "Doim bir yo'nalish", "Faqat tunda", "Faqat tog'da"), ("Siklon qanday ob-havo keltiradi?", "Bulutli va yog'inli", "Ochiq va quruq", "Doim issiq", "Doim sovuq"), ("Bofort shkalasi nimani o'lchaydi?", "Shamol kuchi", "Harorat", "Bosim", "Namlik")],
    [("Shamol tezligi qanday birlikda o'lchanadi?", "m/s", "mm", "gPa", "°C"), ("12 ball nimani bildiradi?", "Bo'ron (33 m/s dan yuqori)", "Shamol yo'q", "Yengil shabada", "Kuchsiz shamol"), ("Shamol guli nima?", "Shamol yo'nalishlari diagrammasi", "O'simlik", "Asbob", "Xarita"),
     ("Passatlar qaysi kengliklarda?", "Tropik kengliklarda", "Qutbda", "Mo'tadilda", "Ekvatorda faqat"), ("G'arbiy shamollar qaysi kengliklarda?", "Mo'tadil", "Tropik", "Ekvator", "Qutb"), ("Qutb shamollari qayerdan esadi?", "Sharqdan", "G'arbdan", "Shimoldan faqat", "Yuqoridan"),
     ("Muson yozda qayerdan esadi (Hindiston)?", "Okeandan quruqlikka", "Quruqlikdan okeanga", "Shimoldan", "Tog'dan"), ("Fen nima?", "Tog'dan esadigan issiq quruq shamol", "Dengiz shabadasi", "Qutb shamoli", "Bo'ron"), ("Bora nima?", "Sovuq kuchli shamol", "Issiq shamol", "Yomg'ir", "Briz"),
     ("Front nima?", "Ikki havo massasi chegarasi", "Tog' tizmasi", "Daryo", "Shamol turi"), ("Sovuq front nimaga olib keladi?", "Jala va keskin sovish", "Doim issiq", "Tinch ob-havo", "Hech nimaga"), ("Antisiklon qanday ob-havo?", "Ochiq, quruq", "Yog'inli", "Bo'ronli", "Qorli doim"),
     ("Kontinental havo massasi qanday?", "Quruq", "Nam", "Doim sovuq", "Doim issiq"), ("Dengiz havo massasi qanday?", "Nam", "Quruq", "Muzli", "Chang"), ("Koriolis kuchi nima ta'sir qiladi?", "Shamol yo'nalishini og'diradi", "Haroratni oshiradi", "Yomg'ir yog'diradi", "Tuproq hosil qiladi"),
     ("O'zbekistonda bahorda esadigan mahalliy shamol?", "Bahorak (Qo'zi)", "Passat", "Bora", "Muson"), ("Briz kechasi qayerdan esadi?", "Quruqlikdan dengizga", "Dengizdan quruqlikka", "Havodan", "Yo'q"), ("Iliq front nimaga olib keladi?", "Ko'p yog'in, ob-havoning asta o'zgarishi", "Quruq sovuq", "Bo'ron", "Zilzila")],
    gallery=[('g3_shamollar', "Global shamollar", ("Rasmda mo'tadil kengliklarda esuvchi yashil strelkalar qaysi shamol?", "G'arbiy shamollar", "Passat", "Qutb shamollari", "Muson")),
             ('g3_briz', "Briz", ("Kunduzgi brizda issiq havo qayerda ko'tariladi?", "Quruqlik ustida", "Dengiz ustida", "Tog'da", "Ko'lda"))],
    extra={'problems': [
        {'question': "Shamol 15 m/s tezlikda esmoqda. Soatiga necha km tezlikda (1 m/s = 3,6 km/soat)?", 'answer': '54', 'solution': "15 · 3,6 = 54"},
        {'question': "Shamol 10 m/s tezlik bilan 2 soat esdi. Havo massasi necha km masofani bosdi (1 m/s = 3,6 km/soat)?", 'answer': '72', 'solution': "10 · 3,6 · 2 = 72"}],
        'matching': [{'left': 'Passat', 'right': 'Tropikdan ekvatorga doimiy shamol'}, {'left': 'Muson', 'right': "Fasllar bo'yicha o'zgaradigan shamol"}, {'left': 'Briz', 'right': "Qirg'oqdagi kunlik shamol"}, {'left': 'Fen', 'right': 'Tog\'dan issiq quruq shamol'}, {'left': 'Siklon', 'right': 'Past bosim markazi'}, {'left': 'Front', 'right': 'Havo massalari chegarasi'}]}))

TOPICS.append(topic(12, 'g3d', "12-mavzu. Namlik, bulut va yog'in",
    ["Mutlaq va nisbiy namlikni farqlash", "Bulut va yog'in turlarini bilish", "Nisbiy namlikni hisoblash"],
    [("Havo namligi", "Havodagi suv bug'i miqdori — namlik. Mutlaq namlik — 1 m³ havodagi suv bug'i grammi. Nisbiy namlik — mavjud suv bug'ining shu haroratda mumkin bo'lgan maksimal miqdoriga foizdagi nisbati. Havo qancha issiq bo'lsa, shuncha ko'p bug' sig'adi: 0 °C da 4,8 g/m³, 20 °C da 17,3 g/m³, 30 °C da 30,4 g/m³. To'yinish nuqtasiga (100 %) yetganda bug' kondensatsiyalanib tuman, bulut hosil qiladi. Nisbiy namlik gigrometr bilan o'lchanadi.", 'g3_namlik', "Harorat va namlik sig'imi"),
     ("Bulutlar", "Bulut — kondensatsiyalangan mayda suv tomchilari va muz kristallari yig'indisi. Asosiy turlari: yuqori darajadagi patsimon (sirrus, 6 km dan baland), o'rta darajadagi baland-g'ovak (altokumulus) va pastki darajadagi to'p (kumulus), qatlamli (stratus), yomg'irli qatlamli (nimbostratus). Kumulonimbus — jala va momaqaldiroq bulutlari. Osmonning bulut bilan qoplanishi ballarda (0–10) baholanadi."),
     ("Yog'inlar", "Yog'in — bulutdan yerga tushadigan suv: yomg'ir, qor, do'l, shabnam, qirov (yer yuzida hosil bo'ladi). Yog'in millimetrda o'lchanadi (yomg'ir o'lchagich — pluviometr): 1 mm = 1 m² ga 1 litr suv. Yog'in turlari: konvektiv (isigan havo ko'tarilishidan, ekvatorda), frontal (frontlarda, mo'tadil kengliklarda), orografik (tog' yonbag'rida). Dunyoda eng ko'p yog'in Cherrapunji (Hindiston, ~11 000 mm), eng kam — Atakama cho'li (Chili) va Sahroi Kabir.", 'g3_orografik', "Orografik yog'inlar"),
     ("Yog'in taqsimoti", "Yog'in kenglik bo'yicha notekis: ekvatorda ko'p (1500–3000 mm), tropik cho'llarda kam (<250 mm), mo'tadil kengliklarda o'rtacha (500–1000 mm), qutblarda kam. Okean yaqini va tog' yonbag'rining shamolga qaragan tomoni yog'inga boy; tog' orti «yomg'ir soyasi»da qurg'oqchil. O'zbekistonda yillik yog'in tekislikda 100–200 mm, tog'larda 800 mm gacha.")],
    ["Nisbiy namlik = (haqiqiy bug' / maks. bug') × 100 %.", "Havo isigan sari ko'proq bug' sig'adi.", "Yog'in turlari: yomg'ir, qor, do'l; shabnam va qirov — yerdagi hosilalar.", "Yog'in mm da o'lchanadi (1 mm = 1 l/m²).", "Yog'in: konvektiv, frontal, orografik.", "Cherrapunji eng ko'p yog'inli joy."],
    "Namlik haroratga bog'liq; bulutdan yog'in yog'adi, taqsimoti kenglik va relyefga bog'liq.",
    [("Nisbiy namlik qanday birlikda?", "Foiz (%)", "g/m³", "mm", "°C"), ("Yog'in qanday o'lchanadi?", "Millimetrda", "Kilometrda", "Gradusda", "Metrda"), ("Havo isigan sari namlik sig'imi?", "Oshadi", "Kamayadi", "O'zgarmaydi", "Nolga tushadi"),
     ("Eng ko'p yog'in qayerda?", "Cherrapunji", "Sahro", "Atakama", "Antarktida"), ("Shabnam nima?", "Yer yuzasidagi suv tomchilari", "Bulut", "Qor", "Do'l"), ("Orografik yog'in qayerda ko'p?", "Tog' yonbag'rida (shamolga qarashli)", "Cho'lda", "Okeanda", "Qutbda")],
    [("Mutlaq namlik nima?", "1 m³ havodagi bug' grammi", "Foizdagi nisbat", "Yog'in miqdori", "Bosim"), ("20 °C da maksimal bug' miqdori?", "17,3 g/m³", "4,8 g/m³", "30,4 g/m³", "100 g/m³"), ("To'yinish nuqtasida nisbiy namlik?", "100 %", "0 %", "50 %", "10 %"),
     ("Gigrometr nimani o'lchaydi?", "Namlikni", "Bosimni", "Haroratni", "Shamolni"), ("Pluviometr nimani o'lchaydi?", "Yog'inni", "Shamolni", "Bosimni", "Haroratni"), ("1 mm yog'in 1 m² ga necha litr?", "1 litr", "10 litr", "0,1 litr", "100 litr"),
     ("Sirrus bulutlari qanday?", "Patsimon, yuqorida", "Past qatlamli", "Jala bulut", "Tuman"), ("Kumulonimbus qanday bulut?", "Jala va momaqaldiroq", "Patsimon", "Qatlamli", "Tuman"), ("Konvektiv yog'in qayerda ko'p?", "Ekvatorda", "Qutbda", "Cho'lda", "Okeanda faqat"),
     ("Frontal yog'in qayerda?", "Mo'tadil kengliklarda", "Ekvatorda", "Sahroda", "Antarktidada"), ("Eng kam yog'in qayerda?", "Atakama cho'li", "Amazonka", "Cherrapunji", "Yevropa"), ("Yomg'ir soyasi nima?", "Tog' orti qurg'oqchil hudud", "Yomg'irli tog'", "Ko'l", "Okean"),
     ("Qirov nima?", "Yer yuzasida muz kristallari", "Bulut", "Yomg'ir", "Do'l"), ("Ekvatorda yillik yog'in?", "1500–3000 mm", "<250 mm", "10 mm", "100 mm"), ("O'zbekiston tekisliklarida yillik yog'in?", "100–200 mm", "2000 mm", "5000 mm", "10 mm"),
     ("Do'l nima?", "Muz bo'laklari ko'rinishidagi yog'in", "Qor", "Shabnam", "Tuman"), ("Bulut ballari qanday?", "0–10", "0–100", "1–3", "0–360"), ("Havo sovuganda namlik sig'imi?", "Kamayadi", "Oshadi", "O'zgarmaydi", "Cheksiz")],
    gallery=[('g3_namlik', "Namlik sig'imi", ("20 °C havo maksimal necha g/m³ bug' saqlaydi?", "17,3", "4,8", "30,4", "9,4")),
             ('g3_orografik', "Orografik yog'in", ("Rasmda yog'in ko'p tomon qaysi?", "Shamolga qaragan (nam shamol keladigan) yonbag'ir", "Shamolga teskari yonbag'ir", "Tog' cho'qqisi", "Tekislik"))],
    extra={'problems': [
        {'question': "20 °C da 1 m³ havoda maksimal 17,3 g bug' bor. Haqiqatda 8,65 g bo'lsa, nisbiy namlik necha %?", 'answer': '50', 'solution': "8,65 : 17,3 · 100 = 50 %"},
        {'question': "Bir yilda 360 mm yog'in yog'di. Bir kunga (365 kun) o'rtacha necha mm? Butungacha yaxlitlang (1 ga).", 'answer': '1', 'solution': "360 : 365 ≈ 1 mm"},
        {'question': "Maydoni 2 m² bo'lgan idishga 15 mm yog'in tushdi. Necha litr suv to'planadi?", 'answer': '30', 'solution': "15 · 2 = 30 litr"}],
        'matching': [{'left': 'Sirrus', 'right': 'Patsimon yuqori bulut'}, {'left': 'Kumulonimbus', 'right': 'Jala bulutlari'}, {'left': 'Gigrometr', 'right': 'Namlik asbobi'}, {'left': 'Pluviometr', 'right': 'Yog\'in o\'lchagich'}, {'left': 'Cherrapunji', 'right': 'Eng ko\'p yog\'inli joy'}, {'left': 'Qirov', 'right': 'Yer yuzasidagi muz kristallari'}]}))

TOPICS.append(topic(13, 'g3e', "13-mavzu. Ob-havo va iqlim mintaqalari",
    ["Ob-havo va iqlim farqini tushuntirish", "Iqlim mintaqalarini va ularning belgilarini sanash", "Iqlimogramma o'qish"],
    [("Ob-havo va iqlim", "Ob-havo — ma'lum joyda va ma'lum vaqtda atmosferaning holati (harorat, bosim, shamol, namlik, yog'in). Iqlim — ko'p yillik (odatda 30 yil) ob-havo rejimi. Iqlimni belgilovchi omillar: geografik kenglik, dengiz sathidan balandlik, okeandan uzoqlik, okean oqimlari, relyef va hukmron shamollar. Ob-havo ma'lumotlari meteorologik stansiyalar, yo'ldoshlar va radarlar yordamida to'planadi."),
     ("Iqlim mintaqalari", "Iqlim mintaqalari Quyosh nuri tushish burchagi va havo massalari bo'yicha kengliklarda almashadi: ekvatorial (doim issiq va nam), subekvatorial (nam va quruq mavsum), tropik (issiq va quruq, cho'llar), subtropik (yozda quruq issiq, qishda yumshoq yog'inli), mo'tadil (to'rt fasl), subarktik va arktik/antarktik (juda sovuq). Mo'tadil mintaqa ichida dengiz, mo'tadil-kontinental, keskin kontinental va musson turlari ajratiladi.", 'g3_mintaqalar', "Iqlim mintaqalari (kenglik bo'yicha)"),
     ("Iqlim mintaqalari xaritada", "Dunyo xaritasida iqlim mintaqalari kengliklar bo'ylab kamarlar tarzida joylashgan, ammo materiklarda relyef va okean ta'siri tufayli bu kamarlar buziladi. Masalan, Evropaning g'arbi Shimoliy Atlantika oqimi tufayli bir xil kenglikdagi Sibirga nisbatan ancha iliq. Tog'larda iqlim balandlik bo'yicha o'zgaradi (vertikal mintaqalilik).", 'g3_iqlim_dunyo', "Iqlim mintaqalari (sxematik xarita)"),
     ("Iqlimogramma", "Iqlimogramma — bir joyning oylik o'rtacha harorati (chiziq) va yog'in miqdori (ustunlar) grafigi. Unda eng issiq/sovuq oy, yillik amplituda va yog'inli/quruq mavsum ko'rinadi. Toshkent iqlimi subtropik kontinental: yozi quruq issiq (iyul ~28 °C, yog'in deyarli yo'q), qishi sovuqroq (yanvar ~−1 °C), yog'in asosan qish-bahorda (yiliga ~400–450 mm).", 'g3_iqlimogramma', "Toshkent iqlimogrammasi")],
    ["Ob-havo — qisqa muddat; iqlim — ko'p yillik rejim.", "Iqlim omillari: kenglik, balandlik, okean, oqimlar, relyef.", "Mintaqalar: ekvatorial, subekvatorial, tropik, subtropik, mo'tadil, qutb.", "Tog'larda vertikal mintaqalilik bor.", "Iqlimogramma: harorat chizig'i + yog'in ustunlari.", "Toshkent iqlimi: subtropik kontinental."],
    "Iqlim ko'p yillik ob-havo rejimi bo'lib, kenglik va boshqa omillarga qarab mintaqalarga bo'linadi.",
    [("Iqlim nima?", "Ko'p yillik ob-havo rejimi", "Bugungi ob-havo", "Shamol", "Yomg'ir"), ("Doim issiq va nam iqlim?", "Ekvatorial", "Arktik", "Subtropik", "Mo'tadil"), ("Iqlimning asosiy omili?", "Geografik kenglik", "Faqat rang", "Faqat vaqt", "Faqat nom"),
     ("Iqlimogramma nimani ko'rsatadi?", "Oylik harorat va yog'inni", "Faqat bosim", "Faqat shamol", "Aholini"), ("Toshkent iqlimi qanday?", "Subtropik kontinental", "Ekvatorial", "Arktik", "Dengiz"), ("Sahroi Kabir qaysi mintaqada?", "Tropik", "Ekvatorial", "Qutb", "Mo'tadil")],
    [("Ob-havo nima?", "Ma'lum vaqtdagi atmosfera holati", "Ko'p yillik rejim", "Kenglik", "Yog'in"), ("Iqlim odatda necha yillik ma'lumotdan aniqlanadi?", "30 yil", "1 yil", "1 kun", "100 yil"), ("Qaysi omil iqlimga ta'sir qiladi?", "Okean oqimlari", "Faqat yer rangi", "Faqat tuproq", "Faqat xarita"),
     ("G'arbiy Yevropa nega iliq?", "Shimoliy Atlantika oqimi tufayli", "Quyoshga yaqin", "Vulqon", "Cho'l"), ("Tog'da iqlim qanday o'zgaradi?", "Balandlik bo'yicha (vertikal mintaqalilik)", "O'zgarmaydi", "Faqat shimolga", "Faqat g'arbga"), ("Subekvatorial iqlimda nima bor?", "Nam va quruq mavsum", "Faqat qor", "Doim quruq", "Doim sovuq"),
     ("Mo'tadil iqlimning belgisi?", "To'rt fasl", "Fasl yo'q", "Yil bo'yi issiq", "Yil bo'yi muz"), ("Arktik iqlim qanday?", "Juda sovuq", "Issiq", "Nam issiq", "Qurg'oqchil issiq"), ("Tropik iqlimda nima ko'p?", "Cho'llar", "Muz", "Tayga", "Tundra"),
     ("Toshkentda eng issiq oy?", "Iyul", "Yanvar", "Mart", "Noyabr"), ("Toshkentda eng sovuq oy?", "Yanvar", "Iyul", "Aprel", "Sentyabr"), ("Toshkentda yog'in qaysi mavsumda ko'p?", "Qish-bahor", "Yoz", "Faqat yoz", "Faqat kuz"),
     ("Iqlimogrammada ustunlar nimani ko'rsatadi?", "Yog'inni", "Haroratni", "Bosimni", "Shamolni"), ("Iqlimogrammada chiziq nimani ko'rsatadi?", "Haroratni", "Yog'inni", "Shamolni", "Namlikni"), ("Qutb mintaqasi qaysi kenglikda?", "66,5° dan yuqori", "0°", "23,5°", "45°"),
     ("Meteorologik stansiya nima qiladi?", "Ob-havoni kuzatadi", "Yo'l quradi", "Neft qazadi", "Ekin ekadi"), ("Okean iqlimga qanday ta'sir qiladi?", "Yumshatadi", "Keskinlashtiradi", "Ta'sir qilmaydi", "Quritadi"), ("Subtropik iqlim yozi?", "Quruq va issiq", "Sovuq", "Nam sovuq", "Qorli")],
    gallery=[('g3_mintaqalar', "Iqlim mintaqalari", ("Rasmda ekvator yaqinidagi mintaqa?", "Ekvatorial", "Arktika", "Mo'tadil", "Subtropik")),
             ('g3_iqlimogramma', "Toshkent iqlimogrammasi", ("Grafikda eng issiq oy qaysi?", "Iyul", "Yanvar", "Mart", "Oktyabr")),
             ('g3_iqlim_dunyo', "Dunyo iqlim kamarlari", ("Xaritada eng keng kamar ekvator atrofida qanday rangda?", "Yashil (ekvatorial)", "Oq", "Ko'k", "Sariq"))],
    extra={'problems': [
        {'question': "Oylik o'rtacha haroratlar: 4 oy +8, 4 oy +24, 4 oy +16 °C. Yillik o'rtacha harorat necha °C?", 'answer': '16', 'solution': "(4·8 + 4·24 + 4·16) : 12 = 16"},
        {'question': "Eng issiq oy +28 °C, eng sovuq oy −1 °C. Yillik amplituda?", 'answer': '29', 'solution': "28 − (−1) = 29"},
        {'question': "Yillik yog'in 440 mm; shundan 60 % qish-bahorda. Qish-bahorda necha mm?", 'answer': '264', 'solution': "440 · 0,6 = 264"}],
        'matching': [{'left': 'Ob-havo', 'right': 'Ma\'lum vaqtdagi atmosfera holati'}, {'left': 'Iqlim', 'right': "Ko'p yillik ob-havo rejimi"}, {'left': 'Ekvatorial', 'right': 'Doim issiq va nam'}, {'left': 'Tropik', 'right': 'Issiq va quruq, cho\'llar'}, {'left': "Mo'tadil", 'right': "To'rt fasl"}, {'left': 'Iqlimogramma', 'right': 'Harorat va yog\'in grafigi'}]}))
