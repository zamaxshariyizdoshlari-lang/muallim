# -*- coding: utf-8 -*-
import math
from dsl import topic
from svglib import *

IMAGES = {}
TOPICS = []


def _suv_aylanishi():
    return cycle('Suvning katta aylanishi', [("Bug'lanish", 'okean, ko\'l, o\'simlik'), ('Kondensatsiya', 'bulut hosil bo\'ladi'), ("Yog'in", 'yomg\'ir, qor'), ('Oqim', 'daryo va yer osti suvi')], 'Quyosh energiyasi')


def _suv_taqsimoti():
    return pie("Yerdagi suvning taqsimlanishi", [('Okean va dengizlar', 96.5), ('Muzliklar', 1.7), ('Yer osti suvlari', 1.7), ("Ko'l, daryo, atmosfera va boshqa", 0.1)],
               note="Chuchuk suv jami suvning atigi ~2,5 % i")


def _chuchuk():
    return pie('Chuchuk suvning tarkibi', [('Muzliklar va doimiy qor', 68.7), ('Yer osti suvlari', 30.1), ("Ko'l, daryo, tuproq, atmosfera", 1.2)],
               note="Insonga qulay ochiq chuchuk suv — jami suvning ~0,01 % i")


def _okean_maydon():
    return bars("Dunyo okeanlarining maydoni", [('Tinch okean', 179), ('Atlantika okeani', 92), ('Hind okeani', 76), ('Shimoliy Muz okeani', 15)], 'mln km²', note='Dunyo okeani yer yuzasining ~71 % ini egallaydi')


def _oqimlar():
    def ov(P):
        o = []
        def arr(pts, col):
            q = [P(*p) for p in pts]
            o.append(poly(q, '', col, 4, close=False))
            a, b = q[-2], q[-1]
            o.append(line(a[0], a[1], b[0], b[1], col, 4, arrow=True))
        arr([(-80, 25), (-70, 33), (-45, 42), (-20, 52)], '#dc2626')       # Golfstrim
        arr([(-75, -40), (-80, -20), (-85, -5), (-100, 0)], '#2563eb')       # Peru (sovuq)
        arr([(125, 20), (135, 30), (150, 38), (170, 42)], '#dc2626')         # Kuroshio
        arr([(-20, 15), (-40, 14), (-60, 14)], '#dc2626')                    # Shimoliy Passat
        arr([(-175, -55), (-100, -56), (-30, -56), (60, -55)], '#2563eb')    # G'arbiy shamollar oqimi
        arr([(-135, 50), (-125, 40), (-120, 25)], '#2563eb')                  # Kaliforniya
        return ''.join(o)
    return world('Dunyo okeanining asosiy oqimlari (sxematik)', overlay=ov, labels=[(-45, 48, 'Golfstrim'), (-95, -12, 'Peru'), (155, 35, 'Kuroshio'), (-100, -52, "G'arbiy shamollar oqimi"), (-125, 30, 'Kaliforniya')],
                 legend=[('#dc2626', 'Iliq oqimlar'), ('#2563eb', 'Sovuq oqimlar')])


def _sholurlik():
    return bars("Suvning sho'rligi", [('Baltika dengizi', 7), ('Qora dengiz', 18), ('Dunyo okeani (o\'rtacha)', 35), ('Qizil dengiz', 41)], '‰', note="1 ‰ = 1 litr suvda 1 g tuz; O'lik dengiz ~340 ‰ (eng sho'r)")


def _daryo_qismlari():
    return flow('Daryo qismlari', [('Boshlanish (manba)', 'buloq, muzlik, ko\'l'), ('Yuqori oqim', 'tez, tor vodiy'), ("O'rta oqim", 'tinchroq, vodiy kengayadi'), ('Quyi oqim', 'sekin, meandra'), ("Quyilish (og'iz)", "delta yoki estuariy")])


def _uzun_daryolar():
    return bars("Eng uzun daryolar", [('Nil', 6650), ('Amazonka', 6400), ('Yantszi', 6300), ('Missisipi', 6275), ('Yenisey', 5539), ('Volga', 3530), ('Amudaryo', 2540), ('Sirdaryo', 2212)], 'km')


def _daryo_rejimi():
    return linechart('Tog\' muzlaridan to\'yinadigan daryo rejimi (sxematik)', ['Y', 'F', 'M', 'A', 'M', 'I', 'I', 'A', 'S', 'O', 'N', 'D'], [600, 550, 650, 900, 1500, 2300, 3000, 2800, 1800, 1100, 800, 650],
                     'Oylar', 'Sarf (m³/s)', labels=[(6, 'yozgi toshqin (muz erishi)'), (1, 'qishki kam suv')], color='#2563eb')


def _kollar():
    return bars("Dunyoning eng katta ko'llari (maydoni)", [('Kaspiy dengizi', 371), ('Yuqori ko\'l (Superior)', 82), ('Viktoriya', 69), ('Guron', 60), ('Michigan', 58)], 'ming km²')


def _yer_osti():
    return layers("Yer osti suvlari qatlamlari", [("Tuproq va havo oqimi", "yuqori qatlam", '#a16207', 14), ("Grunt suvi", "birinchi suv o'tkazmas qatlamgacha (quduqlar)", '#38bdf8', 14),
                                                 ("Suv o'tkazmas qatlam (gil)", "suvni o'tkazmaydi", '#92400e', 12), ("Artezian suvi", "ikki gil orasida, bosim ostida", '#0ea5e9', 14), ("Suv o'tkazmas qatlam", "pastki to'siq", '#78350f', 12)])


def _muzlik():
    return profile('Tog\' muzligi', [(0, 95), (15, 85), (30, 60), (45, 40), (60, 25), (75, 14), (90, 8), (100, 6)], [(18, 98, "To'planish (oziqlanish) zonasi"), (60, 52, 'Muzlik tili'), (82, 30, 'Erish zonasi'), (95, 12, "Muzlik suvi → daryo")])


IMAGES.update({'g4_aylanish': _suv_aylanishi(), 'g4_taqsimot': _suv_taqsimoti(), 'g4_chuchuk': _chuchuk(), 'g4_okeanlar': _okean_maydon(), 'g4_oqimlar': _oqimlar(), 'g4_sholurlik': _sholurlik(),
               'g4_daryo_qismlari': _daryo_qismlari(), 'g4_uzun_daryolar': _uzun_daryolar(), 'g4_daryo_rejimi': _daryo_rejimi(), 'g4_kollar': _kollar(), 'g4_yer_osti': _yer_osti(), 'g4_muzlik': _muzlik()})

TOPICS.append(topic(14, 'g4a', "14-mavzu. Gidrosfera va suvning aylanishi",
    ["Gidrosfera tarkibini bilish", "Suvning katta va kichik aylanishini tushuntirish", "Suv zaxiralari taqsimotini tahlil qilish"],
    [("Gidrosfera", "Gidrosfera — Yerning suv qobig'i: Dunyo okeani, quruqlikdagi suvlar (daryo, ko'l, botqoq, muzlik, yer osti suvlari) va atmosferadagi bug'. Yerdagi suvning umumiy hajmi ~1,4 mlrd km³; uning 96,5 % i sho'r okean suvi. Gidrosfera atmosfera, litosfera va biosfera bilan doimiy aloqada, suv aylanishida bog'langan.", 'g4_taqsimot', "Yerdagi suvning taqsimlanishi"),
     ("Chuchuk suv zaxirasi", "Chuchuk suv jami suvning atigi ~2,5 % i. Uning katta qismi (~69 %) muzliklarda (Antarktida, Grenlandiya), ~30 % yer osti suvlarida; daryo va ko'llardagi oson olinadigan suv 1 % dan kam. Shu sababli suvni tejash va ifloslanishdan saqlash dolzarb. Hozir dunyo aholisining har to'rtinchisi toza ichimlik suvidan qiyinchilik bilan foydalanadi.", 'g4_chuchuk', "Chuchuk suvning tarkibi"),
     ("Suvning aylanishi", "Quyosh energiyasi ta'sirida okeandan suv bug'lanadi, bug' ko'tarilib sovuydi, kondensatsiyalanib bulut hosil qiladi va yog'in sifatida yerga tushadi. Suvning bir qismi daryolar orqali okeanga qaytadi, bir qismi yer ostiga singadi, qolgani qayta bug'lanadi. Okean–atmosfera–okean yo'li kichik (okean) aylanish; okean–quruqlik–okean yo'li katta aylanish; quruqlik ichida (ichki) aylanish ham bor.", 'g4_aylanish', "Suvning aylanishi"),
     ("Suvning ahamiyati", "Suv — hayot manbai: o'simlik va hayvonlar tanasining 60–90 % ini tashkil etadi, sanoat, qishloq xo'jaligi (sug'orish ~70 %), energetika va transportda zarur. Suv iqlimni yumshatadi: issiqlik sig'imi katta bo'lgani uchun sekin isiydi va sekin soviydi. O'zbekistonda suv resurslarining ko'p qismi transchegaraviy daryolar (Amudaryo, Sirdaryo) orqali keladi va tejab ishlatilishi shart.")],
    ["Suvning 96,5 % i okeanlarda.", "Chuchuk suv ~2,5 %: 69 % muzlik, 30 % yer osti.", "Suv aylanishi: bug'lanish → kondensatsiya → yog'in → oqim.", "Kichik aylanish: okean–atmosfera–okean.", "Sug'orish dunyo suvining ~70 % ini ishlatadi.", "Suvning issiqlik sig'imi katta — iqlimni yumshatadi."],
    "Gidrosfera suv aylanishi orqali Yer qobiqlarini bog'laydi; chuchuk suv juda kam.",
    [("Dunyo suvining necha foizi okeanda?", "96,5 %", "50 %", "10 %", "2,5 %"), ("Chuchuk suvning ko'p qismi qayerda?", "Muzliklarda", "Daryolarda", "Ko'llarda", "Atmosferada"), ("Suv aylanishining harakatlantiruvchi kuchi?", "Quyosh energiyasi", "Oy", "Zilzila", "Shamol faqat"),
     ("Suvning bug'ga aylanishi?", "Bug'lanish", "Kondensatsiya", "Yog'in", "Muzlash"), ("Suv bug'ining bulutga aylanishi?", "Kondensatsiya", "Bug'lanish", "Oqim", "Singish"), ("Sug'orish dunyo suvining qancha qismini ishlatadi?", "~70 %", "~7 %", "~1 %", "~20 %")],
    [("Gidrosfera nima?", "Yerning suv qobig'i", "Havo qobig'i", "Tosh qobig'i", "Hayot qobig'i"), ("Chuchuk suv jami suvning qancha qismi?", "~2,5 %", "~25 %", "~50 %", "~97 %"), ("Qaysi suv zaxirasi eng katta chuchuk?", "Muzliklar", "Daryo", "Ko'l", "Bulut"),
     ("Yer osti suvlari chuchuk suvning qancha qismi?", "~30 %", "~3 %", "~60 %", "~0,3 %"), ("Katta aylanish qayerda?", "Okean–quruqlik–okean", "Faqat okeanda", "Faqat quruqlikda", "Atmosferada faqat"), ("Yog'in suvi qayerga boradi?", "Oqim, singish, bug'lanish", "Faqat yo'qoladi", "Kosmosga", "Yerning ichiga"),
     ("Suvning issiqlik sig'imi?", "Katta", "Kichik", "Nol", "Cheksiz"), ("Transchegaraviy daryo nima?", "Bir necha davlat orqali oqadigan", "Faqat bitta davlatda", "Kichik daryo", "Quriydigan"), ("O'zbekiston asosiy daryolari?", "Amudaryo va Sirdaryo", "Nil", "Volga", "Amazonka"),
     ("Gidrosfera hajmi taxminan?", "1,4 mlrd km³", "14 km³", "1,4 mln km³", "140 km³"), ("Hayvon tanasida suv ulushi?", "60–90 %", "5 %", "10 %", "100 %"), ("Ichimlik suvidan qiynalayotganlar ulushi?", "Har to'rtinchi odam", "Hech kim", "Har yuzinchi", "Hamma"),
     ("Kondensatsiya qaysi bosqichda?", "Bulut hosil bo'lishida", "Bug'lanishda", "Oqimda", "Muzlashda"), ("Muzlar erishi nimaga olib keladi?", "Okean sathi ko'tariladi", "Okean sathi tushadi", "Hech nima", "Daryo quriydi"), ("Ichki aylanish nima?", "Quruqlik ichidagi suv aylanishi", "Okeandagi aylanish", "Atmosfera", "Muz aylanishi"),
     ("Suvni tejash nega kerak?", "Chuchuk suv kam", "Suv ko'p", "Suv arzon", "Ahamiyati yo'q")],
    gallery=[('g4_taqsimot', "Suvning taqsimlanishi", ("Diagrammada eng katta ulush?", "Okean va dengizlar", "Muzliklar", "Yer osti suvlari", "Daryolar")),
             ('g4_aylanish', "Suv aylanishi", ("Bug'lanishdan keyingi bosqich?", "Kondensatsiya (bulut)", "Yog'in", "Oqim", "Singish")),
             ('g4_chuchuk', "Chuchuk suv", ("Chuchuk suvning ko'p qismi qayerda?", "Muzliklarda", "Daryolarda", "Ko'llarda", "Tuproqda"))],
    extra={'problems': [
        {'question': "Jami suv 1400 mln km³, chuchuk suv 2,5 %. Chuchuk suv necha mln km³?", 'answer': '35', 'solution': "1400 · 0,025 = 35"},
        {'question': "Chuchuk suvning 69 % i muzlikda. 35 mln km³ chuchuk suvning muzlikdagi qismi taxminan necha mln km³? (butungacha yaxlitlang)", 'answer': '24', 'solution': "35 · 0,69 ≈ 24"},
        {'question': "Dunyo suvining 96,5 % i okeanda. Qolgan necha foiz?", 'answer': '3,5', 'solution': "100 − 96,5 = 3,5 %"}],
        'matching': [{'left': 'Bug\'lanish', 'right': 'Suvning bug\'ga aylanishi'}, {'left': 'Kondensatsiya', 'right': "Bug'ning suvga aylanishi"}, {'left': 'Katta aylanish', 'right': 'Okean–quruqlik–okean'}, {'left': 'Muzlik', 'right': 'Eng katta chuchuk suv zaxirasi'}, {'left': 'Transchegaraviy daryo', 'right': 'Bir necha davlatdan oqadi'}, {'left': 'Gidrosfera', 'right': 'Suv qobig\'i'}]}))

TOPICS.append(topic(15, 'g4b', "15-mavzu. Dunyo okeani, sho'rlik va oqimlar",
    ["Dunyo okeani tarkibini sanash", "Suv sho'rligi va uni hisoblash", "Okean oqimlari turlari va ahamiyatini bilish"],
    [("Dunyo okeani va uning qismlari", "Dunyo okeani — yer yuzasining ~71 % ini egallagan yagona suv massasi. U to'rt okeanga bo'linadi: Tinch (179 mln km²), Atlantika (92), Hind (76) va Shimoliy Muz (15). Okean qismlari: dengiz (materiklar orasida yoki chekkasida: Qora, Oraliq, Qizil), ko'rfaz (Fors, Meksika, Bengal), bo'g'oz (Gibraltar, Bosfor, Beringov). Okeanning o'rtacha chuqurligi ~3700 m, eng chuqur joy — Mariana novi (~11 km).", 'g4_okeanlar', "Okeanlar maydoni"),
     ("Sho'rlik va harorat", "Okean suvining sho'rligi — 1 litr suvda erigan tuz grammi (promille, ‰). O'rtacha 35 ‰. Sho'rlik bug'lanish ko'p, yog'in kam joylarda (tropiklar, Qizil dengiz 41 ‰) yuqori; daryolar quyiladigan yoki muz erigan joylarda (Baltika 7 ‰) past. Eng sho'r joy — O'lik dengiz (~340 ‰), unda cho'kib ketmaydi. Okean sirtining harorati ekvatorda ~27 °C, qutbda −1,8 °C; chuqurlashgan sari pasayadi, 1000 m dan chuqurda +2…+4 °C.", 'g4_sholurlik', "Dengizlar sho'rligi"),
     ("Okean oqimlari", "Okean oqimlari — okean ichida suvning doimiy harakati. Shamollar (shamol oqimlari), suv zichligi farqi va Yer aylanishi (Koriolis) ularni hosil qiladi. Iliq oqimlar (Golfstrim, Kuroshio) past kengliklardan yuqorisiga, sovuq oqimlar (Peru, Labrador, Kaliforniya) qutblardan ekvator tomon yo'naladi. Golfstrim G'arbiy Yevropa iqlimini yumshatadi, Peru oqimi esa Atakama cho'lining hosil bo'lishiga hissa qo'shadi.", 'g4_oqimlar', "Asosiy okean oqimlari"),
     ("To'lqin, qaytish va sunami", "Shamol to'lqinlari suv sirtida shamol ta'sirida hosil bo'ladi. Qabariq va qaytish (suv sathi sutkada ikki marta ko'tarilib-tushishi) Oy va Quyosh tortishidan. Sunami — okean tubidagi zilzila yoki vulqon tufayli hosil bo'ladigan ulkan to'lqin (2004-yil Hind okeanida, 2011-yil Yaponiyada). Sunami okeanda sezilmaydi, qirg'oqqa yetganda balandligi 10–30 m ga yetadi; ogohlantirish tizimlari xavfni kamaytiradi.")],
    ["Dunyo okeani 71 %: Tinch, Atlantika, Hind, Shimoliy Muz.", "O'rtacha sho'rlik 35 ‰.", "O'lik dengiz ~340 ‰ — eng sho'r.", "Golfstrim — iliq; Peru — sovuq oqim.", "Qabariq va qaytish Oy va Quyosh tortishidan.", "Sunami zilzila/vulqondan hosil bo'ladi."],
    "Dunyo okeani to'rt okeandan iborat; sho'rlik va oqimlar uning xossalarini va iqlimni belgilaydi.",
    [("Eng katta okean?", "Tinch okean", "Atlantika", "Hind", "Shimoliy Muz"), ("Dunyo okeanining o'rtacha sho'rligi?", "35 ‰", "3,5 ‰", "350 ‰", "0,35 ‰"), ("Golfstrim qanday oqim?", "Iliq", "Sovuq", "Muzli", "Daryo"),
     ("Peru oqimi qanday?", "Sovuq", "Iliq", "Issiq", "Oqim emas"), ("Sunami nimadan hosil bo'ladi?", "Zilzila yoki vulqondan", "Shamoldan", "Yomg'irdan", "Oydan"), ("Qaysi dengiz eng sho'r?", "O'lik dengiz", "Baltika", "Qora", "Oq")],
    [("Eng kichik okean?", "Shimoliy Muz", "Hind", "Atlantika", "Tinch"), ("Dunyo okeani yer yuzining necha foizi?", "71 %", "29 %", "50 %", "90 %"), ("Mariana novi chuqurligi?", "~11 km", "~1 km", "~110 km", "~110 m"), ("Qizil dengiz sho'rligi?", "41 ‰", "7 ‰", "18 ‰", "340 ‰"),
     ("Baltika sho'rligi nega past?", "Ko'p daryolar quyiladi", "Issiq", "Bug'lanish ko'p", "Muz yo'q"), ("1 promille nima?", "1 l suvda 1 g tuz", "1 kg suvda 1 kg tuz", "100 l da 1 g", "1 ml"), ("Kuroshio qayerda?", "Tinch okean (Yaponiya)", "Atlantika", "Hind", "Shimoliy Muz"),
     ("Golfstrim qaysi iqlimni yumshatadi?", "G'arbiy Yevropa", "Avstraliya", "Hindiston", "Afrika"), ("Peru oqimi nimaga hissa qo'shadi?", "Atakama cho'li hosil bo'lishiga", "O'rmonga", "Yomg'irga", "Qorga"), ("Oqimlarni nima hosil qiladi?", "Shamol, zichlik farqi, Yer aylanishi", "Zilzila faqat", "Vulqon faqat", "Muz faqat"),
     ("Qabariq va qaytish sababi?", "Oy va Quyosh tortishi", "Shamol", "Daryolar", "Vulqon"), ("Qabariq sutkada necha marta?", "2 marta", "1 marta", "5 marta", "Hech"), ("Sunami balandligi qirg'oqda?", "10–30 m gacha", "1 sm", "100 m doim", "Sezilmaydi"),
     ("Bo'g'oz nima?", "Ikki suv havzasini bog'lovchi tor suv", "Ko'l", "Daryo", "Orol"), ("Gibraltar nima?", "Bo'g'oz", "Ko'rfaz", "Orol", "Tog'"), ("Bengal nima?", "Ko'rfaz", "Bo'g'oz", "Dengiz", "Orol"), ("Chuqurlikda harorat?", "Pasayadi", "Oshadi", "O'zgarmaydi", "100 °C")],
    gallery=[('g4_okeanlar', "Okeanlar maydoni", ("Diagrammadagi eng kichik okean?", "Shimoliy Muz", "Hind", "Atlantika", "Tinch")),
             ('g4_oqimlar', "Okean oqimlari", ("Xaritada qizil strelkalar qanday oqimlar?", "Iliq oqimlar", "Sovuq oqimlar", "Daryolar", "Shamollar")),
             ('g4_sholurlik', "Sho'rlik", ("Diagrammada eng sho'r dengiz?", "Qizil dengiz", "Baltika", "Qora", "Okean o'rtacha"))],
    extra={'problems': [
        {'question': "1 litr dengiz suvida 35 g tuz bor. 20 litr suvda necha g tuz?", 'answer': '700', 'solution': "35 · 20 = 700"},
        {'question': "Okean sirtida +27 °C. Chuqurlikda har 100 m da o'rtacha 2 °C pasaysa (sxematik), 500 m da necha °C?", 'answer': '17', 'solution': "27 − 5·2 = 17"},
        {'question': "Tinch okean 179 mln km², Atlantika 92 mln km². Farqi necha mln km²?", 'answer': '87', 'solution': "179 − 92 = 87"}],
        'matching': [{'left': 'Golfstrim', 'right': 'Iliq oqim (Atlantika)'}, {'left': 'Peru', 'right': 'Sovuq oqim'}, {'left': 'Sunami', 'right': 'Zilzila yaratgan ulkan to\'lqin'}, {'left': "O'lik dengiz", 'right': "Eng sho'r suv"}, {'left': 'Bo\'g\'oz', 'right': 'Ikki havzani bog\'laydi'}, {'left': 'Promille', 'right': "Sho'rlik birligi"}]}))

TOPICS.append(topic(16, 'g4c', "16-mavzu. Daryolar",
    ["Daryo qismlarini va havzasini aniqlash", "Daryo rejimi va to'yinish manbalarini bilish", "Dunyo va O'zbekiston daryolarini tavsiflash"],
    [("Daryo tuzilishi", "Daryo — doimiy o'zandagi oqim. Boshlanadigan joyi — manba (buloq, muzlik, ko'l), quyiladigan joyi — og'iz (okean, dengiz, ko'l yoki boshqa daryo). Daryo qismlari: yuqori oqim (tez, qiya), o'rta va quyi oqim (sekin, meandra). Asosiy daryoga quyiluvchi daryolar — irmoqlar. Daryo va barcha irmoqlari bilan birga havzani tashkil qiladi; havzalar suvayirg'ich bilan ajraladi. Daryo uzunligi — manbadan og'izgacha masofa.", 'g4_daryo_qismlari', "Daryo qismlari"),
     ("Dunyoning yirik daryolari", "Eng uzun daryolar: Nil (~6650 km, Afrika), Amazonka (~6400 km, eng sersuv, Janubiy Amerika), Yantszi (Osiyo), Missisipi (Shimoliy Amerika). Yevropada eng uzuni Volga (3530 km). O'rta Osiyoda eng uzun daryolar Amudaryo (~2540 km) va Sirdaryo (~2212 km): ular Pomir va Tyan-Shan muzliklaridan boshlanib, ilgari Orol dengiziga quyilgan. Amazonka dunyodagi daryo suvining ~20 % ini okeanga olib boradi.", 'g4_uzun_daryolar', "Eng uzun daryolar"),
     ("Daryo rejimi", "Daryo rejimi — daryo suvi sathi va sarfining yil davomida o'zgarishi. To'yinish manbalari: yomg'ir, qor, muzlik va yer osti suvlari. Tog' muzliklaridan to'yinadigan daryolar (Amudaryo) yozda, muz erishi eng kuchli paytda to'lib oqadi; yomg'irdan to'yinadigan daryolar yog'inli faslda sersuv. Daryo sarfi — 1 soniyada o'zan kesimidan o'tadigan suv hajmi (m³/s). Toshqin — suv sathi keskin ko'tarilishi.", 'g4_daryo_rejimi', "Daryo rejimi (sxematik)"),
     ("Daryolardan foydalanish", "Daryolar sug'orish, ichimlik suvi, gidroelektrostansiyalar (GES), kemachilik, baliqchilik uchun ishlatiladi. Suv omborlari va kanallar oqimni tartibga soladi (Qayroqqum, Tuyamo'yin, Chorvoq, Katta Farg'ona kanali). Ortiqcha olingan suv daryolar quyi oqimini quritadi (Orol fojeasi). Daryoni asrash uchun ifloslanishni kamaytirish va suvni tejash zarur.")],
    ["Daryo: manba, o'zan, irmoq, og'iz, havza.", "Nil — eng uzun; Amazonka — eng sersuv.", "Amudaryo ~2540 km, Sirdaryo ~2212 km.", "Rejim: muz erishi yozda, yomg'ir faslida to'lishi.", "Sarf: m³/s.", "Daryo suvi GES, sug'orish va kema qatnoviga xizmat qiladi."],
    "Daryo manbadan og'izgacha oqadi, rejimi to'yinish manbaiga bog'liq; insoniyat uchun hayotiy ahamiyatga ega.",
    [("Eng uzun daryo?", "Nil", "Amazonka", "Volga", "Amudaryo"), ("Eng sersuv daryo?", "Amazonka", "Nil", "Volga", "Sirdaryo"), ("Irmoq nima?", "Asosiy daryoga quyiluvchi daryo", "Daryo boshi", "Ko'l", "Dengiz"),
     ("Daryo boshlanadigan joy?", "Manba", "Og'iz", "Delta", "Havza"), ("Amudaryo qaysi tog'lardan boshlanadi?", "Pomir", "Alp", "And", "Ural"), ("Delta qayerda hosil bo'ladi?", "Daryo og'zida", "Manbada", "Tog'da", "Cho'lda")],
    [("Daryo sarfi nimada o'lchanadi?", "m³/s", "km", "°C", "gPa"), ("Havza nima?", "Daryo va irmoqlari suv yig'adigan maydon", "Daryo uzunligi", "Daryo chuqurligi", "Ko'l"), ("Suvayirg'ich nima?", "Havzalarni ajratuvchi chiziq", "Daryo o'zani", "Ko'l", "Delta"),
     ("Volga qayerda?", "Yevropa", "Osiyo", "Afrika", "Amerika"), ("Nil qaysi materikda?", "Afrika", "Osiyo", "Avstraliya", "Amerika"), ("Sirdaryo qaysi tog'lardan boshlanadi?", "Tyan-Shan", "Alp", "And", "Ural"),
     ("Amudaryo yozda nega sersuv?", "Muzliklar erishi tufayli", "Yomg'ir ko'pligi", "Quyosh yo'qligi", "Shamol"), ("Toshqin nima?", "Suv sathining keskin ko'tarilishi", "Quriy", "Muzlash", "Past suv"), ("Qayroqqum qanday obyekt?", "Suv ombori", "Cho'l", "Tog'", "Shahar"),
     ("Tuyamo'yin nima?", "Suv ombori va gidrouzel", "Shahar", "Tog'", "Cho'l"), ("Katta Farg'ona kanali nima uchun?", "Sug'orish", "Transport faqat", "Sayyohlik", "Ov"), ("Orol fojeasiga sabab?", "Daryo suvining ko'p olinishi", "Zilzila", "Vulqon", "Muz"),
     ("Quyi oqimda daryo?", "Sekin oqadi, meandra hosil qiladi", "Juda tez", "Quriydi doim", "Muzlaydi"), ("Yuqori oqimda daryo?", "Tez, tor vodiy", "Sekin", "Delta hosil qiladi", "Ko'lga aylanadi"), ("Daryodan energiya olish?", "GES", "TES", "AES", "Quyosh"),
     ("Estuariy nima?", "Daryoning voronkasimon og'zi", "Delta", "Kanal", "Ko'l")],
    gallery=[('g4_uzun_daryolar', "Eng uzun daryolar", ("Diagrammada O'rta Osiyodagi eng uzun daryo?", "Amudaryo", "Volga", "Missisipi", "Nil")),
             ('g4_daryo_qismlari', "Daryo qismlari", ("Qaysi qism daryoning boshlanishi?", "Manba", "Og'iz", "Delta", "Irmoq")),
             ('g4_daryo_rejimi', "Daryo rejimi", ("Grafikda daryo qaysi oylarda eng sersuv?", "Iyun–avgust", "Dekabr–fevral", "Mart", "Noyabr"))],
    extra={'problems': [
        {'question': "Daryo oqim tezligi 2 m/s. 1 soatda suv necha km yo'l bosadi (1 m/s = 3,6 km/soat)?", 'answer': '7,2', 'solution': "2 · 3,6 = 7,2 km"},
        {'question': "Daryo kesimida 1 soniyada 500 m³ suv o'tadi. 1 soatda necha m³?", 'answer': '1800000', 'solution': "500 · 3600 = 1 800 000"},
        {'question': "Nil 6650 km, Amudaryo 2540 km. Farq necha km?", 'answer': '4110', 'solution': "6650 − 2540 = 4110"}],
        'matching': [{'left': 'Manba', 'right': 'Daryo boshlanadigan joy'}, {'left': 'Og\'iz', 'right': 'Daryo quyiladigan joy'}, {'left': 'Irmoq', 'right': 'Asosiy daryoga quyiluvchi daryo'}, {'left': 'Havza', 'right': 'Daryo suv yig\'adigan maydon'}, {'left': 'Delta', 'right': 'Og\'izdagi yotqiziqlar'}, {'left': 'Sarf', 'right': 'Soniyada o\'tgan suv hajmi'}]}))

TOPICS.append(topic(17, 'g4d', "17-mavzu. Ko'llar, muzliklar va yer osti suvlari",
    ["Ko'l turlarini bilish", "Muzlik turlarini va ularning ahamiyatini tushuntirish", "Yer osti suvlari qatlamlarini tavsiflash"],
    [("Ko'llar", "Ko'l — quruqlikdagi tabiiy chuqurlikda to'plangan suv. Hosil bo'lishiga ko'ra: tektonik (Baykal, Issiqko'l), vulqon (kratersimon), muzlik (Shimoliy Amerika, Skandinaviya), karst, to'g'on hosil qilgan, qoldiq (Kaspiy, Orol), deltadagi. Oqar ko'llar (Baykal — Angarani beradi) chuchuk, oqmas ko'llar (Kaspiy, O'lik dengiz) sho'r bo'ladi. Eng katta ko'l — Kaspiy dengizi (371 ming km²), eng chuqur — Baykal (1642 m; dunyo chuchuk suvining ~20 % i).", 'g4_kollar', "Eng katta ko'llar"),
     ("Muzliklar", "Muzlik — quruqlikdagi tabiiy muz massasi, o'z og'irligi bilan sekin siljiydi. Qoplama muzliklar (Antarktida, Grenlandiya) katta maydonni egallaydi: Antarktida muzi dunyo chuchuk suvining ~60 % ini saqlaydi. Tog' muzliklari (Pomir, Tyan-Shan, Alp, Himolay) yuqorida qor to'planishi (oziqlanish zonasi), pastda erishi zonasi bilan tavsiflanadi; ular O'rta Osiyo daryolarining asosiy manbai. Muzliklar iqlim isishi tufayli qisqarmoqda.", 'g4_muzlik', "Tog' muzligi"),
     ("Yer osti suvlari", "Yer osti suvlari tuproq va jinslar g'ovaklarida, yoriqlarida joylashadi. Grunt suvi — birinchi suv o'tkazmas qatlam ustidagi suv (quduqlar shu suv hisobiga); artezian suvi — ikki suv o'tkazmas qatlam orasida, bosim ostida (quduq ochilsa, o'zi otilib chiqadi). Mineral va issiq (termal) suvlar davolashda foydalaniladi. Yer osti suvlari yomg'ir va daryo suvlarining singishi hisobiga to'ladi.", 'g4_yer_osti', "Yer osti suvlari qatlamlari"),
     ("Botqoq va sun'iy suv havzalari", "Botqoq — ortiqcha namlangan, suvni o'tkazmaydigan joy: torf hosil bo'ladi (Sibir, Kanada, Polesye). Botqoqlar suvni saqlab turadi, iqlimni yumshatadi. Suv omborlari — to'g'on bilan to'silgan sun'iy ko'llar (Qayroqqum, Tuyamo'yin, Chorvoq), kanallar — sun'iy suv yo'llari. Ular sug'orish, energetika, baliqchilik va rekreatsiyaga xizmat qiladi, lekin ekotizimni ham o'zgartiradi.")],
    ["Eng katta ko'l — Kaspiy; eng chuqur — Baykal.", "Oqar ko'llar chuchuk, oqmaslar sho'r.", "Antarktida muzi chuchuk suvning ~60 % i.", "Tog' muzliklari O'rta Osiyo daryolarini oziqlantiradi.", "Grunt suvi — birinchi suv o'tkazmas qatlam ustida.", "Artezian suvi bosim ostida bo'ladi."],
    "Ko'llar, muzliklar va yer osti suvlari quruqlikdagi suv zaxiralari bo'lib, har birining o'ziga xos hosil bo'lishi va ahamiyati bor.",
    [("Eng katta ko'l?", "Kaspiy dengizi", "Baykal", "Viktoriya", "Issiqko'l"), ("Eng chuqur ko'l?", "Baykal", "Kaspiy", "Guron", "Michigan"), ("Chuchuk suvning ko'p qismi qaysi muzlikda?", "Antarktida", "Alp", "Pomir", "Himolay"),
     ("Grunt suvi qayerda joylashadi?", "Birinchi suv o'tkazmas qatlam ustida", "Eng chuqurda", "Atmosferada", "Daryoda"), ("Artezian suvi nimasi bilan ajraladi?", "Bosim ostida bo'ladi", "Sho'r", "Muz", "Issiq doim"), ("O'rta Osiyo daryolari asosan nimadan to'yinadi?", "Tog' muzliklari va qorlardan", "Okeandan", "Cho'ldan", "Botqoqdan")],
    [("Baykal qayerda?", "Rossiya (Sibir)", "Hindiston", "Braziliya", "AQSH"), ("Issiqko'l qayerda?", "Qirg'iziston", "O'zbekiston", "Rossiya", "Xitoy"), ("Oqar ko'l qanday?", "Chuchuk", "Sho'r", "Muzli", "Quruq"), ("Oqmas ko'l qanday bo'ladi?", "Ko'pincha sho'r", "Doim chuchuk", "Muz", "Daryo"),
     ("Qoplama muzliklar qayerda?", "Antarktida va Grenlandiya", "Sahroda", "Amazonkada", "Yevropada"), ("Tog' muzligi qismlari?", "Oziqlanish va erish zonalari", "Faqat boshi", "Faqat tili", "Yo'q"), ("Muzliklar hozir?", "Qisqarmoqda", "Kengaymoqda", "O'zgarmaydi", "Yo'q bo'ldi"),
     ("Botqoqda nima hosil bo'ladi?", "Torf", "Neft", "Oltin", "Marmar"), ("Suv ombori nima?", "To'g'on bilan to'silgan sun'iy ko'l", "Tabiiy ko'l", "Daryo", "Dengiz"), ("Qayroqqum qaysi daryoda?", "Sirdaryo", "Amudaryo", "Zarafshon", "Qashqadaryo"),
     ("Chorvoq qayerda?", "Toshkent viloyati (Chirchiq)", "Samarqand", "Nukus", "Termiz"), ("Mineral suvlar nima uchun?", "Davolash", "Faqat sug'orish", "Faqat qurilish", "Ov"), ("Tektonik ko'l qanday hosil bo'ladi?", "Yer po'sti harakati natijasida", "Vulqon kulidan", "Muzdan", "Shamoldan"),
     ("Karst ko'llari qanday jinsda?", "Ohaktosh", "Granit", "Bazalt", "Qum"), ("Kaspiy qaysi turdagi?", "Qoldiq, oqmas", "Oqar chuchuk", "Muzlik", "Vulqon"), ("Baykal chuchuk suvning qanchasini saqlaydi?", "~20 %", "~2 %", "~60 %", "~0,2 %"),
     ("Muz ko'chishi qanday?", "O'z og'irligi bilan siljiydi", "Qotib turadi", "Havoga ko'tariladi", "Shamol bilan")],
    gallery=[('g4_kollar', "Eng katta ko'llar", ("Diagrammada eng katta ko'l?", "Kaspiy dengizi", "Yuqori", "Viktoriya", "Michigan")),
             ('g4_yer_osti', "Yer osti suvlari", ("Rasmda bosim ostidagi suv qaysi?", "Artezian suvi", "Grunt suvi", "Tuproq namligi", "Daryo suvi")),
             ('g4_muzlik', "Tog' muzligi", ("Muzlikning yuqori qismida nima sodir bo'ladi?", "Qor to'planadi (oziqlanish)", "Muz eriydi", "Daryo quriydi", "Ko'l hosil bo'ladi"))],
    extra={'problems': [
        {'question': "Baykal chuqurligi 1642 m, Issiqko'l 668 m. Farq necha m?", 'answer': '974', 'solution': "1642 − 668 = 974"},
        {'question': "Kaspiy 371 ming km², Yuqori ko'l 82 ming km². Kaspiy taxminan necha marta katta (butungacha)?", 'answer': '5', 'solution': "371 : 82 ≈ 4,5 ≈ 5"},
        {'question': "Muz hajmi suvdan 9 % ko'p. 500 litr suv muzlasa, muz hajmi necha litr?", 'answer': '545', 'solution': "500 · 1,09 = 545"}],
        'matching': [{'left': 'Baykal', 'right': 'Eng chuqur ko\'l'}, {'left': 'Kaspiy', 'right': "Eng katta ko'l"}, {'left': 'Artezian suvi', 'right': 'Bosim ostidagi yer osti suvi'}, {'left': 'Grunt suvi', 'right': 'Birinchi qatlam suvi'}, {'left': 'Torf', 'right': 'Botqoqda hosil bo\'ladi'}, {'left': 'Antarktida', 'right': 'Eng katta muz zaxirasi'}]}))
