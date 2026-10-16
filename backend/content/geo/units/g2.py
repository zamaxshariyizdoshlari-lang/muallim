# -*- coding: utf-8 -*-
import math
from dsl import topic
from svglib import *

IMAGES = {}
TOPICS = []


def _yer_tuzilishi():
    return layers('Yerning ichki tuzilishi', [
        ("Yer po'sti", "5–70 km, qattiq tog' jinslari (materik va okean)", '#c4a574', 5),
        ("Mantiya", "~2900 km, qizigan yarim plastik massa", '#f59e0b', 30),
        ("Tashqi yadro", "~2200 km, suyuq temir-nikel (4000–5000 °C)", '#ef4444', 22),
        ("Ichki yadro", "~1200 km radiusli, qattiq (taxminan 5400 °C)", '#fde047', 14)],
        note="Chuqurlik oshgani sari harorat va bosim ortadi (Yer markazida ~6371 km)")


def _tosh_aylanishi():
    return cycle('Tog\' jinslarining hosil bo\'lishi (tosh aylanishi)',
                 [('Magma', 'erigan massa'), ('Magmatik jins', 'granit, bazalt'), ('Cho\'kindi jins', 'ohaktosh, qumtosh'), ('Metamorfik jins', 'marmar, gneys')], 'Tosh aylanishi')


def _plitalar():
    def ov(P):
        o = []
        # O'rta Atlantika tizmasi
        o.append(poly([P(-20, 80), P(-30, 62), P(-33, 45), P(-27, 25), P(-15, 5), P(-13, -15), P(-15, -35), P(-5, -52), P(5, -55)], '', '#dc2626', 3, close=False))
        # Tinch okean olov halqasi (g'arb va sharq)
        o.append(poly([P(-170, 60), P(-150, 58), P(-125, 48), P(-118, 33), P(-105, 18), P(-85, 8), P(-78, -10), P(-72, -30), P(-72, -50)], '', '#ea580c', 3, close=False))
        o.append(poly([P(162, 58), P(150, 46), P(142, 38), P(130, 30), P(122, 15), P(125, 5), P(145, -5), P(165, -15), P(176, -30), P(176, -40)], '', '#ea580c', 3, close=False))
        # Alp-Himolay kamari
        o.append(poly([P(-8, 36), P(15, 40), P(35, 38), P(55, 34), P(70, 35), P(85, 29), P(95, 25)], '', '#7c3aed', 3, close=False))
        # Sharqiy Afrika riftlari
        o.append(poly([P(38, 12), P(37, 2), P(34, -10), P(35, -20)], '', '#0d9488', 3, close=False))
        for (a, b, c, d) in ((-45, 30, -38, 30), (-40, -25, -33, -25)):
            pass
        return ''.join(o)
    return world('Yirik litosfera plitalari va ularning chegaralari', overlay=ov,
                 labels=[(-100, 55, 'Shimoliy Amerika'), (-60, -15, 'Janubiy Amerika'), (20, 5, 'Afrika'), (80, 55, 'Yevroosiyo plitasi'), (-155, 15, 'Tinch okean plitasi'), (80, -25, 'Hind-Avstraliya'), (0, -80, 'Antarktida plitasi')],
                 legend=[('#dc2626', "O'rta okean tizmasi"), ('#ea580c', "Olov halqasi"), ('#7c3aed', "Alp-Himolay kamari"), ('#0d9488', "Sharqiy Afrika riftlari")])


def _chegara_turlari():
    out = [ARROW_DEF]
    panels = [("Uzoqlashuvchi (divergent)", "Rift, o'rta okean tizmasi", '#fecaca', 'div'), ("Yaqinlashuvchi (konvergent)", "Tog'lar, chuqur novlar, vulqonlar", '#fde68a', 'conv'), ("Sirpanuvchi (transform)", "Zilzilalar (San-Andreas yoriq)", '#bfdbfe', 'tr')]
    for i, (t, sub, col, kind) in enumerate(panels):
        x = 20 + i * 232
        out.append(box(x, 55, 220, 300, col, '#94a3b8', rx=12))
        out.append(T(x + 110, 80, t, 13, INK, weight='700'))
        out.append(T(x + 110, 100, sub, 11, MUTED))
        out.append(box(x + 15, 180, 90, 40, '#c4a574', '#8b6b3d', rx=3))
        out.append(box(x + 115, 180, 90, 40, '#a98c5c', '#8b6b3d', rx=3))
        if kind == 'div':
            out.append(line(x + 100, 160, x + 40, 160, '#dc2626', 3, arrow=True))
            out.append(line(x + 120, 160, x + 180, 160, '#dc2626', 3, arrow=True))
            out.append(box(x + 105, 220, 10, 90, '#ef4444', rx=2))
        elif kind == 'conv':
            out.append(line(x + 40, 160, x + 95, 160, '#dc2626', 3, arrow=True))
            out.append(line(x + 180, 160, x + 125, 160, '#dc2626', 3, arrow=True))
            out.append(poly([(x + 85, 180), (x + 110, 140), (x + 135, 180)], '#a16207', '#78350f', 2))
        else:
            out.append(line(x + 60, 170, x + 60, 120, '#dc2626', 3, arrow=True))
            out.append(line(x + 160, 230, x + 160, 280, '#dc2626', 3, arrow=True))
        out.append(T(x + 110, 330, ['Yangi po\'st hosil bo\'ladi', 'Plita cho\'kadi yoki ko\'tariladi', 'Plitalar yonma-yon suriladi'][i], 11, INK))
    return svg('Plita chegaralarining turlari', ''.join(out))


def _relyef_profili():
    return profile('Relyef shakllari kesimi', [(0, 0), (8, 0), (10, 4), (22, 8), (30, 10), (36, 22), (42, 55), (47, 90), (52, 58), (58, 28), (64, 24), (72, 38), (80, 36), (90, 14), (100, 6)],
                   [(8, 12, 'Dengiz sathi'), (23, 20, 'Pasttekislik'), (47, 96, "Baland tog' (8 km+)"), (62, 34, 'Vodiy'), (76, 50, 'Plato'), (92, 22, 'Qirlar')], water=(0, 9, 3))


def _tog_balandliklari():
    return bars("Dunyo materiklaridagi eng baland cho'qqilar", [('Everest (Osiyo)', 8849), ('Akonkagua (J. Amerika)', 6961), ('Denali (Sh. Amerika)', 6190), ('Kilimanjaro (Afrika)', 5895), ('Elbrus (Yevropa)', 5642), ('Vinson (Antarktida)', 4892), ('Kostyushko (Avstraliya)', 2228)], 'm')


def _nurash():
    return flow('Fizik nurash bosqichlari', [('Kunduz isish', 'jins kengayadi'), ('Tun sovish', 'jins qisqaradi'), ('Yoriqlar paydo bo\'ladi', 'darz ketadi'), ('Suv muzlaydi', 'yoriqlar kengayadi'), ('Bo\'laklarga bo\'linadi', 'shag\'al, qum')])


def _daryo_vodiysi():
    return profile('Daryo vodiysi kesimi (V-shakl)', [(0, 62), (14, 58), (30, 38), (42, 14), (50, 6), (58, 14), (70, 38), (86, 58), (100, 62)],
                   [(50, 20, 'Daryo o\'zani'), (20, 52, 'Yonbag\'ir'), (80, 52, 'Yonbag\'ir'), (50, 72, 'Eroziya vodiyni chuqurlashtiradi')], water=(46, 54, 6))


def _barxan():
    out = [ARROW_DEF, box(40, 60, 640, 290, '#fef3c7', rx=6)]
    out.append(poly([(40, 330), (160, 330), (300, 190), (360, 330), (680, 330), (680, 345), (40, 345)], '#f6d38b', '#b45309', 2))
    out.append(line(80, 220, 210, 240, '#2563eb', 3, arrow=True))
    out.append(line(80, 250, 220, 265, '#2563eb', 3, arrow=True))
    out.append(T(120, 205, 'Shamol yo\'nalishi', 12, '#1d4ed8', weight='700'))
    out.append(T(250, 175, 'Barxan cho\'qqisi', 12, INK, weight='700'))
    out.append(T(330, 300, 'tik (shamolga teskari) yonbag\'ir', 11, INK, anchor='start'))
    out.append(T(120, 322, 'yotiq yonbag\'ir', 11, INK, anchor='start'))
    out.append(T(W / 2, 372, "Shamol qumni yotiq yonbag'irdan tik yonbag'irga ko'chirib, barxanni asta siljitadi", 12, MUTED))
    return svg('Barxan — shamol yaratgan qum tepaligi', ''.join(out))


IMAGES.update({'g2_yer_tuzilishi': _yer_tuzilishi(), 'g2_tosh_aylanishi': _tosh_aylanishi(), 'g2_plitalar': _plitalar(), 'g2_chegara_turlari': _chegara_turlari(),
               'g2_relyef_profili': _relyef_profili(), 'g2_tog_balandliklari': _tog_balandliklari(), 'g2_nurash': _nurash(), 'g2_daryo_vodiysi': _daryo_vodiysi(), 'g2_barxan': _barxan()})

TOPICS.append(topic(5, 'g2a', "5-mavzu. Yerning ichki tuzilishi va tog' jinslari",
    ["Yer qobiqlari (po'st, mantiya, yadro)ni bilish", "Tog' jinslari turlarini farqlash", "Geotermik gradientni hisoblash"],
    [("Yerning ichki qatlamlari", "Yer markaziga qarab uch asosiy qatlamga bo'linadi: Yer po'sti, mantiya va yadro. Yer po'sti eng yupqa qobiq: materiklar ostida 35–70 km, okeanlar ostida 5–10 km. Mantiya ~2900 km qalinlikda, qizigan yarim plastik modda. Yadro tashqi (suyuq) va ichki (qattiq) qismlardan iborat, asosan temir va nikeldan. Yer po'sti va mantiyaning yuqori qismi litosferani tashkil etadi. Yer ichi seysmik to'lqinlar yordamida o'rganiladi: eng chuqur parma quduq (Kola) atigi ~12 km ga yetgan.", 'g2_yer_tuzilishi', "Yerning ichki qatlamlari"),
     ("Minerallar va tog' jinslari", "Mineral — tabiiy kimyoviy birikma (kvars, dala shpati, slyuda, kalsit). Tog' jinsi — minerallar yig'indisi. Kelib chiqishiga ko'ra uch tur: magmatik (magma qotishidan: granit, bazalt, andezit), cho'kindi (cho'kib to'planishdan: qumtosh, ohaktosh, gil, tuz) va metamorfik (bosim va harorat ta'sirida o'zgargan: marmar, gneys, kvarsit). Jinslar doimiy aylanishda — tosh aylanishida.", 'g2_tosh_aylanishi', "Tosh aylanishi sxemasi"),
     ("Geotermik gradient", "Yer ichida chuqurlashgan sari harorat ortadi. Geotermik pog'ona — haroratni 1 °C ga oshirish uchun kerak bo'ladigan chuqurlik, o'rtacha 33 m. Masalan, yer yuzida harorat 15 °C bo'lsa, 1650 m chuqurlikdagi shaxtada: 15 + 1650 : 33 = 65 °C. Bu issiqlikdan geotermal elektr stansiyalari va issiq suv ta'minotida foydalaniladi (Islandiya, Italiya, Kamchatka)."),
     ("Foydali qazilmalar", "Qatlamlarda hosil bo'lgan foydali qazilmalar: yonuvchi (neft, gaz, ko'mir, torf), ruda (temir, mis, oltin, uran) va noruda (tuz, fosforit, qurilish materiallari). Cho'kindi jinslarda ko'mir, neft, gaz, tuz; magmatik jinslar bilan metall rudalar bog'liq. O'zbekistonda oltin (Muruntau), mis (Olmaliq), gaz (Shurtan), uran (Navoiy) konlari mashhur.")],
    ["Yer qatlamlari: po'st, mantiya, yadro.", "Materiklar ostida po'st 35–70 km, okeanda 5–10 km.", "Tog' jinslari: magmatik, cho'kindi, metamorfik.", "Geotermik pog'ona ≈ 33 m / 1 °C.", "Granit va bazalt — magmatik jinslar.", "Neft, gaz, ko'mir — cho'kindi jinslarda."],
    "Yer po'st, mantiya va yadrodan iborat; tog' jinslari uch turga bo'linadi, chuqurlikda harorat ortib boradi.",
    [("Yerning eng yupqa qobig'i?", "Yer po'sti", "Mantiya", "Tashqi yadro", "Ichki yadro"), ("Granit qaysi tur tog' jinsi?", "Magmatik", "Cho'kindi", "Metamorfik", "Organik"),
     ("Marmar qaysi tur tog' jinsi?", "Metamorfik", "Magmatik", "Cho'kindi", "Suyuq"), ("Geotermik pog'ona o'rtacha qancha?", "33 m", "3,3 m", "330 m", "3300 m"),
     ("Yerning qaysi qatlami suyuq?", "Tashqi yadro", "Ichki yadro", "Yer po'sti", "Litosfera"), ("Ohaktosh qaysi tur tog' jinsi?", "Cho'kindi", "Magmatik", "Metamorfik", "Vulqon")],
    [("Mantiya qalinligi taxminan?", "2900 km", "29 km", "290 km", "29 000 km"), ("Yer yadrosi asosan nimadan iborat?", "Temir va nikel", "Granit", "Suv", "Qum"), ("Litosferaga nima kiradi?", "Yer po'sti va mantiyaning yuqori qismi", "Faqat yadro", "Faqat okean", "Atmosfera"),
     ("Bazalt qaysi tur jins?", "Magmatik", "Cho'kindi", "Metamorfik", "Organik"), ("Qumtosh qaysi tur jins?", "Cho'kindi", "Magmatik", "Metamorfik", "Vulqon"), ("Gneys qaysi tur jins?", "Metamorfik", "Magmatik", "Cho'kindi", "Organik"),
     ("Mineral nima?", "Tabiiy kimyoviy birikma", "Tog' jinslari to'plami", "Tuproq turi", "Suv turi"), ("Eng chuqur parma quduq (Kola) taxminan necha km?", "12 km", "120 km", "1,2 km", "1200 km"),
     ("Yer ichi qanday o'rganiladi?", "Seysmik to'lqinlar yordamida", "Faqat teleskop bilan", "Faqat xarita bilan", "Radio bilan"), ("Chuqurlashgan sari harorat?", "Ortadi", "Pasayadi", "O'zgarmaydi", "Tebranadi"),
     ("Okean ostida po'st qalinligi?", "5–10 km", "35–70 km", "100 km", "1 km"), ("Metamorfik jinslar nima ta'sirida hosil bo'ladi?", "Yuqori bosim va harorat", "Faqat shamol", "Faqat yomg'ir", "Faqat muz"),
     ("Neft qaysi jinslar bilan bog'liq?", "Cho'kindi", "Magmatik", "Metamorfik", "Hech biri"), ("Muruntau nima konlari bilan mashhur?", "Oltin", "Neft", "Ko'mir", "Tuz"),
     ("Olmaliq nima bilan mashhur?", "Mis", "Gaz", "Uran", "Tuz"), ("Shurtan nima konlari bilan mashhur?", "Gaz", "Oltin", "Mis", "Fosforit"), ("Geotermal energiya nima?", "Yer issiqligi energiyasi", "Quyosh energiyasi", "Shamol energiyasi", "Suv energiyasi")],
    gallery=[('g2_yer_tuzilishi', "Yerning tuzilishi", ("Rasmda eng yupqa qatlam qaysi?", "Yer po'sti", "Mantiya", "Tashqi yadro", "Ichki yadro")),
             ('g2_tosh_aylanishi', "Tosh aylanishi", ("Magma qotishidan hosil bo'lgan jins qanday ataladi?", "Magmatik jins", "Cho'kindi jins", "Metamorfik jins", "Organik jins"))],
    extra={'problems': [
        {'question': "Yer yuzida harorat 15 °C. Geotermik pog'ona 33 m bo'lsa, 1650 m chuqurlikda harorat necha °C?", 'answer': '65', 'hint': "1650 : 33 = 50", 'solution': "15 + 50 = 65 °C"},
        {'question': "Shaxta 990 m chuqurlikda. Yuzada harorat 12 °C, pog'ona 33 m. Shaxta tubida harorat?", 'answer': '42', 'solution': "990 : 33 = 30; 12 + 30 = 42"},
        {'question': "Haroratni 1 °C ga oshirish uchun 33 m chuqurlashish kerak. 99 m da harorat necha °C ga oshadi?", 'answer': '3', 'solution': "99 : 33 = 3"}],
        'matching': [{'left': 'Granit', 'right': 'Magmatik jins'}, {'left': 'Ohaktosh', 'right': "Cho'kindi jins"}, {'left': 'Marmar', 'right': 'Metamorfik jins'}, {'left': 'Mantiya', 'right': "~2900 km qalinlikdagi qatlam"}, {'left': 'Tashqi yadro', 'right': 'Suyuq temir-nikel'}, {'left': 'Litosfera', 'right': "Po'st va mantiyaning yuqori qismi"}]}))

TOPICS.append(topic(6, 'g2b', "6-mavzu. Litosfera plitalari, vulqon va zilzilalar",
    ["Litosfera plitalari nazariyasini tushunish", "Plita chegaralari turlarini farqlash", "Vulqon va zilzilalarning sabab va oqibatlarini bilish"],
    [("Litosfera plitalari", "Litosfera yaxlit emas: u yirik va kichik plitalarga bo'lingan. Eng yiriklari: Tinch okean, Shimoliy Amerika, Janubiy Amerika, Yevroosiyo, Afrika, Hind-Avstraliya va Antarktida plitalari. Plitalar mantiyaning plastik qatlami ustida yiliga 1–10 sm tezlikda sekin harakatlanadi. Bu nazariyani 1912-yilda Alfred Vegener materiklar dreyfi g'oyasi bilan boshlab bergan, XX asr o'rtalarida okean tubi o'rganilgach tasdiqlangan.", 'g2_plitalar', "Litosfera plitalari va chegaralari"),
     ("Plita chegaralari", "Plitalar uchta yo'l bilan o'zaro ta'sirlashadi. Uzoqlashganda (divergent) yoriqlar hosil bo'ladi, yangi po'st vujudga keladi: O'rta Atlantika tizmasi, Sharqiy Afrika riftlari. Yaqinlashganda (konvergent) tog'lar ko'tariladi yoki bir plita ikkinchisi tagiga cho'kadi (subduksiya): Himolay (Hind va Yevroosiyo plitalari to'qnashuvi), And tog'lari, Mariana novi. Yonma-yon sirpanganda (transform) kuchli zilzilalar bo'ladi: San-Andreas yorig'i (AQSH).", 'g2_chegara_turlari', "Plita chegaralarining turlari"),
     ("Vulqonlar", "Vulqon — Yer yuzasida magma otilib chiqadigan joy. Magma yuzaga chiqqanda lava deyiladi. Vulqon konusi, krater, kul va gazlar uning tarkibiy qismlari. Faol, so'ngan va o'chgan vulqonlar bo'ladi. Dunyoning ~75 % faol vulqonlari Tinch okean atrofidagi «Olov halqasi»da: Fudziyama, Krakatau, Sent-Xelens. Yevroosiyoda Elbrus, Klyuchevskaya Sopka, Italiyada Vezuviy va Etna mashhur. Vulqon tuprog'i unumdor, ammo otilish xavfli.", None),
     ("Zilzilalar", "Zilzila — yer ostidagi zarbalar va tebranishlar. Zilzila o'chog'i — chuqurlikda tebranish boshlangan joy, epitsentr — uning yuzadagi proyeksiyasi. Kuchi Rixter shkalasida magnituda bilan (1–10) o'lchanadi, har bir birlik energiyani ~32 marta oshiradi; ta'siri 12 ballik shkalada baholanadi. Eng kuchli zilzila 1960-yil Chilida (M 9,5). O'zbekistonda 1966-yil Toshkent zilzilasi shaharni qayta qurishga sabab bo'lgan. Seysmik hududlarda binolar zilzilabardosh qilib quriladi.")],
    ["Litosfera plitalarga bo'lingan, ular yiliga 1–10 sm siljiydi.", "Chegaralar: uzoqlashuvchi, yaqinlashuvchi, sirpanuvchi.", "Faol vulqonlarning ~75 % i Tinch okean «Olov halqasi»da.", "Himolay Hind va Yevroosiyo plitalari to'qnashuvidan.", "Zilzila kuchi Rixter shkalasi (magnituda) bilan o'lchanadi.", "Epitsentr — o'choqning yuzadagi proyeksiyasi."],
    "Litosfera plitalari harakati tog'lar, vulqonlar va zilzilalarni hosil qiladi.",
    [("Litosfera plitalari yiliga o'rtacha qancha siljiydi?", "1–10 sm", "1–10 m", "1–10 km", "O'zgarmaydi"), ("Olov halqasi qaysi okean atrofida?", "Tinch okean", "Atlantika", "Hind", "Shimoliy Muz"),
     ("Himolay qanday hosil bo'lgan?", "Hind va Yevroosiyo plitalari to'qnashuvidan", "Vulqondan", "Daryo eroziyasidan", "Muzlikdan"), ("Zilzila o'chog'ining yuzadagi proyeksiyasi?", "Epitsentr", "Krater", "Magma", "Gipotsentr"),
     ("Zilzila kuchi nimada o'lchanadi?", "Rixter shkalasi (magnituda)", "Kelvin", "Pa", "Joul"), ("Materiklar dreyfi g'oyasini kim ilgari surgan?", "Alfred Vegener", "Nyuton", "Dekart", "Gumbolt")],
    [("Magma yuzaga chiqqanda nima deyiladi?", "Lava", "Kul", "Gaz", "Tuz"), ("O'rta Atlantika tizmasi qanday chegara?", "Uzoqlashuvchi", "Yaqinlashuvchi", "Sirpanuvchi", "Chegara emas"), ("San-Andreas yorig'i qanday chegara?", "Sirpanuvchi (transform)", "Uzoqlashuvchi", "Yaqinlashuvchi", "Okean"),
     ("Subduksiya nima?", "Bir plita ikkinchisi tagiga cho'kishi", "Plitalarning uzoqlashishi", "Vulqon otilishi", "Tog' nurashi"), ("Mariana novi qanday joy?", "Eng chuqur okean novi", "Eng baland tog'", "Daryo", "Cho'l"),
     ("Fudziyama qayerda?", "Yaponiya", "Italiya", "AQSH", "Rossiya"), ("Vezuviy qayerda?", "Italiya", "Yaponiya", "Chili", "Islandiya"), ("Eng kuchli zilzila (1960) qayerda bo'lgan?", "Chili", "Yaponiya", "O'zbekiston", "Italiya"),
     ("Toshkent zilzilasi yili?", "1966", "1866", "1996", "1946"), ("Rixter shkalasida har bir birlik energiyani taxminan necha marta oshiradi?", "32 marta", "2 marta", "10 marta", "100 marta"),
     ("Vulqon konusining tepasidagi chuqurcha?", "Krater", "Epitsentr", "Rift", "Delta"), ("Faol vulqonlarning taxminan qancha qismi Olov halqasida?", "75 %", "10 %", "25 %", "5 %"),
     ("Seysmik hududlarda binolar qanday qurilishi kerak?", "Zilzilabardosh", "Faqat baland", "Faqat shisha", "Faqat yog'och emas, beton"), ("Vulqon tuprog'i qanday?", "Unumdor", "Unumsiz", "Sho'r", "Muzli"),
     ("Pangeya nima?", "Qadimgi yagona o'ta qit'a", "Okean nomi", "Vulqon", "Daryo"), ("Zilzila o'chog'i nima?", "Tebranish boshlangan chuqurlikdagi joy", "Yuzadagi nuqta", "Daryo boshi", "Vulqon krateri"),
     ("Sharqiy Afrika riftlari qanday chegara?", "Uzoqlashuvchi", "Yaqinlashuvchi", "Sirpanuvchi", "Okean"), ("And tog'lari qanday hosil bo'lgan?", "Plita cho'kishi (subduksiya) natijasida", "Daryo eroziyasidan", "Muz tufayli", "Shamoldan")],
    gallery=[('g2_plitalar', "Plitalar xaritasi (sxematik)", ("Qizil chiziq qaysi tizmani ko'rsatadi?", "O'rta Atlantika tizmasi", "Himolay", "And", "Ural")),
             ('g2_chegara_turlari', "Chegara turlari", ("Plitalar bir-biridan uzoqlashganda nima hosil bo'ladi?", "Yangi po'st (rift/tizma)", "Baland tog'", "Faqat zilzila", "Chuqur nov"))],
    extra={'problems': [
        {'question': "Plita yiliga 5 sm siljiydi. 2 mln yilda necha km siljiydi?", 'answer': '100', 'hint': "5 sm · 2 000 000 = 10 000 000 sm", 'solution': "10 000 000 sm = 100 km"},
        {'question': "Rixter shkalasida 7 magnitudali zilzila 5 magnitudalidan necha marta ko'p energiya ajratadi (har birlikda 32 marta, ≈ 1000)? Taxminiy sonni yozing: 32² ni hisoblang.", 'answer': '1024', 'solution': "32 · 32 = 1024"}],
        'matching': [{'left': 'Epitsentr', 'right': "O'choqning yuzadagi proyeksiyasi"}, {'left': 'Lava', 'right': 'Yuzaga chiqqan magma'}, {'left': 'Subduksiya', 'right': 'Plitaning boshqasi tagiga cho\'kishi'}, {'left': 'Rift', 'right': 'Plitalar uzoqlashgan yoriq'}, {'left': 'Magnituda', 'right': 'Zilzila kuchi o\'lchovi'}, {'left': 'Olov halqasi', 'right': 'Tinch okean vulqonlar zonasi'}]}))

TOPICS.append(topic(7, 'g2c', "7-mavzu. Relyef shakllari: tog'lar va tekisliklar",
    ["Relyefning asosiy shakllarini farqlash", "Tog'larni balandligi va kelib chiqishiga ko'ra tasniflash", "Tekislik turlarini bilish"],
    [("Relyef", "Relyef — quruqlik va okean tubining notekisliklari majmui. Uni ichki (tektonik, vulqon) va tashqi (nurash, suv, shamol, muz) kuchlar yaratadi. Quruqlikda asosiy shakllar: tekisliklar va tog'lar. Balandlik dengiz sathidan hisoblanadi (absolyut) yoki bir nuqtaning boshqasidan balandligi (nisbiy). Dunyo okeanining o'rtacha sathi nolga teng deb olingan.", 'g2_relyef_profili', "Relyef shakllari kesimi"),
     ("Tekisliklar", "Tekislik — balandligi o'zgarmas yoki salgina o'zgaruvchan keng hudud. Absolyut balandligi bo'yicha: pasttekislik (200 m gacha: Turon, G'arbiy Sibir), qirlar (200–500 m), yassi tog'lik/plato (500 m dan yuqori: Ustyurt, Dekan). Kelib chiqishiga ko'ra: akkumulyativ (yotqiziqlardan) va denudatsion (yemirilgan). Eng katta tekisliklar: Amazonka, Sharqiy Yevropa, G'arbiy Sibir, Buyuk tekislik (AQSH)."),
     ("Tog'lar", "Tog' — dengiz sathidan 500 m dan baland, nisbiy balandligi katta, yonbag'ir va cho'qqisi ajralgan relyef. Balandligiga ko'ra: past (800 m gacha), o'rta (800–3000 m), baland (3000 m dan yuqori). Kelib chiqishiga ko'ra: burmali (Himolay, Alp, And), yoriqli-blokli (Oltoy, Tyan-Shan qisman), vulqon (Kilimanjaro, Fudziyama). Yosh tog'lar baland, o'tkir cho'qqili, eski tog'lar (Ural) past va yumaloq.", 'g2_tog_balandliklari', "Materiklarning eng baland cho'qqilari"),
     ("Okean tubi relyefi", "Okean tubida ham relyef rang-barang: materik sayozligi (shelf, 200 m gacha), materik yonbag'ri, okean tubi tekisliklari, o'rta okean tizmalari va chuqur okean novlari. Eng chuqur joy — Mariana novi (Chelenjer, ~11 034 m). Dunyo okeanining o'rtacha chuqurligi ~3700 m. Shelf zonasi baliqchilik va neft-gaz qazib olish uchun eng boy.")],
    ["Tekislik: pasttekislik (<200 m), qirlar, plato.", "Tog' balandligi: past <800, o'rta 800–3000, baland >3000 m.", "Everest 8849 m — eng baland cho'qqi.", "Mariana novi ~11 034 m — eng chuqur joy.", "Yosh tog'lar baland va o'tkir; eski tog'lar past.", "Shelf — materik sayozligi (200 m gacha)."],
    "Relyef tekislik va tog'larni o'z ichiga oladi; absolyut balandlik dengiz sathidan hisoblanadi.",
    [("Eng baland cho'qqi qaysi?", "Everest", "Akonkagua", "Elbrus", "Kilimanjaro"), ("Eng chuqur okean novi?", "Mariana", "Puerto-Riko", "Yava", "Peru"), ("Past tog'lar balandligi?", "800 m gacha", "3000 m dan yuqori", "8000 m", "200 m"),
     ("Qaysi tog'lar yosh?", "Himolay", "Ural", "Appalachi", "Sharqiy Gat"), ("Pasttekislik balandligi?", "200 m gacha", "500 m dan yuqori", "3000 m", "1000 m"), ("Shelf nima?", "Materik sayozligi", "Okean novi", "Tog' tizmasi", "Vulqon")],
    [("Absolyut balandlik nimadan hisoblanadi?", "Dunyo okeani sathidan", "Yer markazidan", "Eng pastdan", "Shahardan"), ("Baland tog'lar balandligi?", "3000 m dan yuqori", "800 m gacha", "500 m", "200 m"), ("Ural tog'lari qanday?", "Eski, past", "Yosh, baland", "Vulqon", "Muz"),
     ("Kilimanjaro qanday tog'?", "Vulqon", "Burmali", "Plato", "Tekislik"), ("Eng katta tekislik (hajmi bo'yicha)?", "Amazonka", "Ustyurt", "Dekan", "Turon faqat"), ("Plato nima?", "Baland yassi tog'lik", "Chuqur nov", "Vulqon", "Daryo vodiysi"),
     ("Ustyurt qanday relyef?", "Plato", "Vulqon", "Muzlik", "Okean tizmasi"), ("Elbrus qayerda?", "Yevropa (Kavkaz)", "Osiyo", "Afrika", "Avstraliya"), ("Akonkagua qayerda?", "Janubiy Amerika", "Afrika", "Yevropa", "Antarktida"),
     ("Okeanning o'rtacha chuqurligi?", "~3700 m", "~370 m", "~37 000 m", "~37 m"), ("Mariana novi chuqurligi taxminan?", "11 000 m", "1100 m", "110 m", "110 000 m"), ("Burmali tog'ga misol?", "Alp", "Fudziyama", "Etna", "Elbrus faqat vulqon"),
     ("Tektonik kuchlar qanday kuch?", "Ichki kuch", "Tashqi kuch", "Quyosh kuchi", "Inson kuchi"), ("Nurash va eroziya qanday kuchlar?", "Tashqi kuchlar", "Ichki kuchlar", "Magnit", "Tortishish emas"),
     ("Eski tog'lar nega past?", "Uzoq yemirilgan", "Yangi paydo bo'lgan", "Vulqon bo'lgani", "Muzliklar yo'qligi"), ("Himolay qaysi qit'ada?", "Osiyo", "Yevropa", "Afrika", "Amerika"), ("Okean tubi tekisliklari qanday?", "Chuqur, tekis maydonlar", "Baland tog'lar", "Vulqonlar", "Plato")],
    gallery=[('g2_tog_balandliklari', "Cho'qqilar balandligi", ("Rasmdagi eng past balandlikdagi cho'qqi qaysi?", "Kostyushko", "Vinson", "Elbrus", "Denali")),
             ('g2_relyef_profili', "Relyef kesimi", ("Rasmda eng baland shakl qanday atalgan?", "Baland tog'", "Plato", "Pasttekislik", "Vodiy"))],
    extra={'problems': [
        {'question': "Everest (8849 m) va Mariana novi (−11 034 m) orasidagi balandlik farqi necha metr?", 'answer': '19883', 'solution': "8849 + 11034 = 19 883"},
        {'question': "Elbrus 5642 m, Kilimanjaro 5895 m. Qaysi biri necha metr baland? Farqni yozing.", 'answer': '253', 'solution': "5895 − 5642 = 253"},
        {'question': "Plato 800 m, uning ustidagi tepalik 1250 m balandlikda. Nisbiy balandlik necha m?", 'answer': '450', 'solution': "1250 − 800 = 450"}],
        'matching': [{'left': 'Pasttekislik', 'right': '200 m gacha'}, {'left': 'Plato', 'right': 'Baland yassi tog\'lik'}, {'left': 'Himolay', 'right': 'Burmali yosh tog\''}, {'left': 'Kilimanjaro', 'right': "Vulqon tog'"}, {'left': 'Shelf', 'right': 'Materik sayozligi'}, {'left': 'Mariana novi', 'right': 'Eng chuqur nov'}]}))

TOPICS.append(topic(8, 'g2d', "8-mavzu. Relyefni o'zgartiruvchi tashqi kuchlar",
    ["Nurash turlarini bilish", "Suv, shamol va muzlik faoliyatini tushuntirish", "Cho'l va daryo relyef shakllarini tavsiflash"],
    [("Nurash", "Nurash — tog' jinslarining Quyosh issiqligi, suv, shamol va tirik organizmlar ta'sirida mayda bo'laklarga parchalanishi. Fizik nurashda jins harorat tebranishidan (kunduz isiydi, tunda soviydi) va yoriqlardagi suvning muzlashidan darz ketadi. Kimyoviy nurashda suv va kislorod ta'sirida jinslar eriydi yoki o'zgaradi (ohaktosh erishi, g'orlar). Biologik nurashda o'simlik ildizlari va mikroorganizmlar jinsni yemiradi. Nurash tuproq paydo bo'lishining boshlanishi.", 'g2_nurash', "Fizik nurash bosqichlari"),
     ("Oqar suvlar faoliyati", "Oqar suvlar — daryolar va vaqtinchalik oqimlar — eng kuchli tashqi kuch: yemiradi (eroziya), tashiydi va yotqizadi (akkumulyatsiya). Tog'larda daryo chuqur V-simon vodiy va jarlik hosil qiladi, tekislikda esa yoyilib meandra (egri-bugri o'zan) va delta (quyilish joyidagi yotqiziqlar) yaratadi. Yomg'ir suvlari yonbag'irlarda jarlar paydo qiladi. Eroziya tuproqni yuvib, qishloq xo'jaligiga zarar yetkazadi.", 'g2_daryo_vodiysi', "Daryo vodiysi kesimi"),
     ("Shamol faoliyati", "Shamol — cho'l va qurg'oqchil hududlarda asosiy yaratuvchi kuch. Deflyatsiya — mayda zarrachalarni uchirib ketish, korrazion — qum bilan jinsni silliqlash (qo'ziqorinsimon toshlar). Shamol ko'chirgan qum to'planib barxanlar, qum tepaliklari va dyunalar hosil qiladi. Barxan yilma-yil shamol yo'nalishida siljiydi. O'zbekistonda Qizilqum, Qoraqum va Ustyurt cho'llarida shu shakllar keng tarqalgan.", 'g2_barxan', "Barxanning tuzilishi"),
     ("Muzlik va dengiz faoliyati", "Muzliklar sekin siljib, jinslarni qirib oladi va o'tkir cho'qqilar (kar, trog) hamda morenalar hosil qiladi; ular Tyan-Shan, Pomir, Himolay, Alp tog'larida hamda Antarktida va Grenlandiyada keng. Dengiz to'lqinlari qirg'oqni yemiradi (abraziya), qum va shag'alni yotqizib plyaj va qumtepalar yaratadi. Inson faoliyati (qazish, kesish, shudgorlash) ham relyefni sezilarli o'zgartiradi — antropogen relyef.")],
    ["Nurash turlari: fizik, kimyoviy, biologik.", "Daryo eroziyasi vodiyni chuqurlashtiradi.", "Delta — daryo quyilish joyidagi yotqiziqlar.", "Barxan — shamol yaratgan qum tepaligi.", "Abraziya — dengiz to'lqinlarining qirg'oqni yemirishi.", "Muzliklar morena va trog hosil qiladi."],
    "Tashqi kuchlar (nurash, suv, shamol, muz) relyefni yemiradi, tashiydi va yotqizib, yangi shakllar hosil qiladi.",
    [("Fizik nurashning asosiy sababi?", "Harorat tebranishi va suvning muzlashi", "Faqat kislota", "Faqat o'simlik", "Vulqon"), ("Barxan nimani yaratadi?", "Shamol", "Daryo", "Muzlik", "Zilzila"), ("Delta qayerda hosil bo'ladi?", "Daryo quyilishida", "Daryo boshida", "Tog' cho'qqisida", "Cho'lda"),
     ("Abraziya nima?", "Dengiz to'lqinlari yemirishi", "Shamol yemirishi", "Muz siljishi", "Vulqon otilishi"), ("Tog' daryosi qanday vodiy hosil qiladi?", "V-simon", "Keng yassi", "Cho'l", "Delta"), ("Morena nima?", "Muzlik yotqiziqlari", "Daryo yotqiziqlari", "Vulqon kuli", "Qum")],
    [("Kimyoviy nurashga misol?", "Ohaktoshning erishi", "Suvning muzlashi", "Shamol uchirishi", "Ildiz yorishi"), ("Biologik nurashni nima yaratadi?", "O'simlik ildizlari va organizmlar", "Muzlik", "Shamol", "Zilzila"), ("Eroziya nima?", "Oqar suv yemirishi", "Qum to'planishi", "Magma otilishi", "Muz erishi"),
     ("Meandra nima?", "Daryoning egri-bugri o'zani", "Daryo boshi", "Delta", "Plato"), ("Deflyatsiya nima?", "Shamolning zarrachalarni uchirib ketishi", "Suv yuvishi", "Muz yemirishi", "Vulqon"), ("Korraziya nima?", "Qum bilan jinsni silliqlash", "Suv erishi", "Muzlash", "Zilzila"),
     ("Dyuna qayerda uchraydi?", "Qum cho'l va dengiz qirg'og'ida", "Tog' cho'qqisida", "Daryo boshida", "Muz ostida"), ("Qaysi cho'llar O'zbekistonda?", "Qizilqum", "Sahroi Kabir", "Gobi", "Atakama"), ("Muzliklar qayerda ko'p?", "Antarktida va Grenlandiyada", "Sahroda", "Amazonkada", "Kongoda"),
     ("Kar nima?", "Muzlik o'yib hosil qilgan kosa", "Daryo deltasi", "Barxan", "Vulqon krateri"), ("Antropogen relyef nima?", "Inson yaratgan relyef", "Vulqon relyefi", "Muzlik relyefi", "Dengiz relyefi"), ("Jar nima?", "Oqar suv yuvgan chuqur o'yiq", "Tepalik", "Plato", "Ko'l"),
     ("Qo'ziqorinsimon toshlar qanday hosil bo'ladi?", "Shamol va qum silliqlashidan", "Vulqondan", "Daryodan", "Muzlikdan"), ("Tuproq paydo bo'lishining boshlanishi?", "Nurash", "Vulqon", "Zilzila", "Bo'ron"), ("Tashqi kuchlarga nima kirmaydi?", "Zilzila (ichki)", "Shamol", "Oqar suv", "Muzlik"),
     ("Sayoz qirg'oqda qum yotqizilishi?", "Plyaj hosil bo'ladi", "Vulqon", "Tog'", "Rift"), ("Eroziya qishloq xo'jaligiga qanday ta'sir qiladi?", "Tuproqni yuvib zarar yetkazadi", "Foyda beradi", "Ta'sir qilmaydi", "Hosildorlikni oshiradi")],
    gallery=[('g2_barxan', "Barxan", ("Barxanning yotiq yonbag'ri qaysi tomonda?", "Shamol esadigan tomonda", "Shamolga teskari tomonda", "Tepada", "Yo'q")),
             ('g2_nurash', "Fizik nurash", ("Fizik nurashning oxirgi bosqichi?", "Bo'laklarga bo'linish", "Isish", "Sovish", "Suv muzlashi"))],
    extra={'problems': [
        {'question': "Suv muzlaganda hajmi taxminan 9 % ga ortadi. 200 litr suv muzlasa, necha litr bo'ladi?", 'answer': '218', 'solution': "200 + 200·0,09 = 218"},
        {'question': "Barxan yiliga 20 m siljiydi. 15 yilda necha metr siljiydi?", 'answer': '300', 'solution': "20 · 15 = 300"}],
        'matching': [{'left': 'Eroziya', 'right': 'Oqar suv yemirishi'}, {'left': 'Deflyatsiya', 'right': 'Shamol uchirishi'}, {'left': 'Abraziya', 'right': "Dengiz to'lqini yemirishi"}, {'left': 'Delta', 'right': 'Daryo quyilishidagi yotqiziq'}, {'left': 'Barxan', 'right': 'Shamol yaratgan qum tepaligi'}, {'left': 'Morena', 'right': 'Muzlik yotqiziqlari'}]}))
