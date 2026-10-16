# -*- coding: utf-8 -*-
from dsl import topic
from svglib import *

IMAGES = {}
TOPICS = []

CITIES = [(69.2, 41.3, 'Toshkent'), (66.9, 39.65, 'Samarqand'), (64.4, 39.8, 'Buxoro'), (60.6, 41.4, 'Xiva'), (71.7, 40.4, 'Andijon'), (59.6, 42.5, 'Nukus'), (65.8, 38.9, 'Qarshi'), (67.8, 40.1, 'Jizzax')]


def _uzb_xarita():
    return world("O'zbekiston (sxematik xarita)", bbox=(55, 74, 36, 46), uzb='#86efac', points=CITIES,
                 labels=[(63, 42.8, "Orol bo'yi"), (63.5, 41.8, 'Qizilqum'), (56.5, 40.5, "Ustyurt"), (70.5, 42.0, "Chotqol")])


def _uzb_relef():
    return profile("O'zbekiston relefi (g'arbdan sharqqa kesim)", [(0, 6), (15, 8), (30, 10), (45, 14), (60, 22), (72, 35), (85, 70), (100, 95)],
                   [(8, 15, "Orol, Ustyurt"), (32, 20, "Qizilqum"), (58, 30, "Zarafshon vodiysi"), (84, 80, "Tyan-Shan, Pomir-Oloy"), (93, 100, "Hisor (4643 m)")])


def _uzb_iqlim():
    return linechart("Toshkentda o'rtacha oylik harorat (°C)", ['Yan', 'Mar', 'May', 'Iyul', 'Sen', 'Noy'], [-1, 9, 20, 28, 21, 8], 'Oy', 'Harorat', labels=[(3, 'Iyul +28'), (0, 'Yanvar −1')], color='#ef4444')


def _uzb_suv():
    return bars("O'zbekiston asosiy daryolari uzunligi (km)", [('Amudaryo', 2540), ('Sirdaryo', 2212), ('Zarafshon', 877), ('Qashqadaryo', 378), ('Surxondaryo', 175)], 'km')


def _uzb_viloyat():
    return bars("Aholisi ko'p viloyatlar (mln, taxminan)", [('Samarqand', 4.1), ("Farg'ona", 3.9), ('Qashqadaryo', 3.4), ('Andijon', 3.3), ('Toshkent sh.', 3.1), ('Namangan', 2.9)], 'mln')


def _uzb_xojalik():
    return pie("O'zbekiston YaIM tarkibi (taxminan)", [('Xizmatlar', 40), ('Sanoat', 25), ("Qishloq xo'jaligi", 25), ('Qurilish', 7), ('Boshqa', 3)])


def _orol():
    return linechart("Orol dengizi maydoni (ming km²)", ['1960', '1975', '1990', '2005', '2020'], [68, 56, 36, 17, 6], 'Yil', 'Maydon', labels=[(0, '68 ming km²'), (4, '~6')], color='#0284c7')


IMAGES.update({'g8_xarita': _uzb_xarita(), 'g8_relef': _uzb_relef(), 'g8_iqlim': _uzb_iqlim(), 'g8_suv': _uzb_suv(), 'g8_viloyat': _uzb_viloyat(), 'g8_xojalik': _uzb_xojalik(), 'g8_orol': _orol()})

TOPICS.append(topic(34, 'g8a', "34-mavzu. O'zbekistonning geografik o'rni va chegaralari",
    ["O'zbekistonning geografik o'rnini tavsiflash", "Qo'shni davlatlarni bilish", "Ma'muriy tuzilishni sanash"],
    [("Geografik o'rni", "O'zbekiston Markaziy Osiyoning markaziy qismida, Amudaryo va Sirdaryo oralig'ida joylashgan. Maydoni 448,9 ming km², aholisi ~36 mln dan ortiq — Markaziy Osiyoda eng ko'p. G'arbdan sharqqa ~1425 km, shimoldan janubga ~930 km cho'zilgan. Dengizga chiqish yo'li yo'q — ikki karra yopiq davlat.", 'g8_xarita', "O'zbekiston xaritasi"),
     ("Qo'shni davlatlar", "O'zbekiston 5 davlat bilan chegaradosh: shimol va shimoli-g'arbda Qozog'iston, shimoli-sharqda va sharqda Qirg'iziston, janubi-sharqda Tojikiston, janubda Afg'oniston, janubi-g'arbda Turkmaniston. Eng uzun chegara Qozog'iston bilan. Dengizga chiqish uchun qo'shni davlatlar orqali transport koridorlari kerak."),
     ("Ma'muriy tuzilishi", "O'zbekiston 12 viloyat, Qoraqalpog'iston Respublikasi va Toshkent shahridan iborat. Viloyatlar: Andijon, Buxoro, Farg'ona, Jizzax, Xorazm, Namangan, Navoiy, Qashqadaryo, Samarqand, Sirdaryo, Surxondaryo, Toshkent. Poytaxt — Toshkent. Davlat tili o'zbek tili. Mustaqillik 1991-yil 1-sentabrda e'lon qilingan.", 'g8_viloyat', "Aholisi ko'p viloyatlar"),
     ("Geografik o'rinning ahamiyati", "O'zbekiston Buyuk Ipak yo'lining markazida joylashgan — qadimdan Sharq va G'arb savdosida muhim bo'lgan (Samarqand, Buxoro, Xiva, Termiz). Bugun ham transport koridorlari orqali ahamiyati ortmoqda. Salbiy tomoni: dengizdan uzoqlik, cho'l iqlimi va suv taqchilligi.")],
    ["Maydoni 448,9 ming km².", "5 davlat bilan chegaradosh.", "12 viloyat + Qoraqalpog'iston + Toshkent shahri.", "Ikki karra yopiq davlat.", "Poytaxt — Toshkent.", "Mustaqillik — 1991-yil 1-sentabr."],
    "O'zbekiston Markaziy Osiyo markazida joylashgan, 5 davlat bilan chegaradosh, dengizga chiqishi yo'q.",
    [("O'zbekiston maydoni?", "448,9 ming km²", "44,8 ming km²", "4489 ming km²", "89 ming km²"), ("Qo'shni davlatlar soni?", "5", "3", "7", "9"), ("Qaysi davlat bilan chegara yo'q?", "Eron", "Qozog'iston", "Tojikiston", "Afg'oniston"),
     ("Viloyatlar soni?", "12", "14", "10", "8"), ("Poytaxt?", "Toshkent", "Samarqand", "Buxoro", "Nukus"), ("Mustaqillik kuni?", "1-sentabr", "1-yanvar", "9-may", "21-mart")],
    [("Ikki karra yopiq nima?", "Dengizga chiqishi yo'q, qo'shnilari ham shunday", "Orol", "Yarim orol", "Qirg'oq davlat"), ("Chegara bo'lmagan davlat?", "Rossiya", "Turkmaniston", "Qirg'iziston", "Tojikiston"), ("Qoraqalpog'iston markazi?", "Nukus", "Xiva", "Qarshi", "Termiz"), ("Xorazm markazi?", "Urganch", "Nukus", "Termiz", "Navoiy"),
     ("Surxondaryo markazi?", "Termiz", "Qarshi", "Guliston", "Jizzax"), ("Qashqadaryo markazi?", "Qarshi", "Termiz", "Guliston", "Navoiy"), ("Sirdaryo markazi?", "Guliston", "Jizzax", "Navoiy", "Nukus"), ("G'arbdan sharqqa uzunligi?", "~1425 km", "~142 km", "~14 250 km", "~500 km"),
     ("Buyuk Ipak yo'li nimani bog'lagan?", "Sharq va G'arbni", "Faqat Yevropani", "Qutblarni", "Okeanlarni"), ("Eng uzun chegara kim bilan?", "Qozog'iston", "Tojikiston", "Afg'oniston", "Turkmaniston"), ("O'zbekiston qaysi mintaqada?", "Markaziy Osiyo", "Janubiy Osiyo", "Yaqin Sharq", "Sharqiy Yevropa"), ("Aholisi?", "~36 mln dan ortiq", "~3,6 mln", "~360 mln", "~3,6 mlrd"),
     ("Ma'muriy birliklar tarkibi?", "12 viloyat, 1 respublika, 1 shahar", "14 viloyat", "10 viloyat", "5 viloyat"), ("Davlat tili?", "O'zbek tili", "Rus tili", "Ingliz tili", "Arab tili"), ("Afg'oniston qaysi tomonda?", "Janubda", "Shimolda", "G'arbda", "Sharqda")],
    gallery=[('g8_xarita', "O'zbekiston xaritasi", ("Xaritada qaysi shahar sharqda?", "Andijon", "Nukus", "Xiva", "Buxoro")),
             ('g8_viloyat', "Viloyatlar aholisi", ("Diagrammada eng gavjum viloyat?", "Samarqand", "Namangan", "Qashqadaryo", "Andijon"))],
    extra={'problems': [
        {'question': "G'arbdan sharqqa 1425 km, shimoldan janubga 930 km. Farqi necha km?", 'answer': '495', 'solution': "1425 − 930"},
        {'question': "Mustaqillik 1991-yilda. 2026-yilda necha yil to'ladi?", 'answer': '35', 'solution': "2026 − 1991"}],
        'matching': [{'left': 'Toshkent', 'right': 'Poytaxt'}, {'left': 'Nukus', 'right': "Qoraqalpog'iston markazi"}, {'left': 'Termiz', 'right': 'Surxondaryo markazi'}, {'left': 'Qarshi', 'right': 'Qashqadaryo markazi'}, {'left': 'Guliston', 'right': 'Sirdaryo markazi'}, {'left': 'Urganch', 'right': 'Xorazm markazi'}]}))

TOPICS.append(topic(35, 'g8b', "35-mavzu. O'zbekiston relefi va foydali qazilmalari",
    ["Relef shakllarini tavsiflash", "Tog' tizmalarini bilish", "Foydali qazilma konlarini topish"],
    [("Relef tuzilishi", "O'zbekistonning ~80 % i tekislik, ~20 % i tog' va tog' oldi. G'arbda va markazda — Turon pasttekisligi: Qizilqum (cho'l), Ustyurt platosi, Orolbo'yi. Sharq va janubi-sharqda Tyan-Shan (Chotqol, Qurama) va Pomir-Oloy (Hisor) tizmalari. Eng baland nuqta — Hisor tizmasidagi Xo'ja-Gurgur-Ota (4643 m); eng past — Mingbuloq botig'i (−12 m).", 'g8_relef', "G'arbdan sharqqa kesim"),
     ("Katta vodiylar", "Farg'ona vodiysi — tog'lar bilan o'ralgan pastlik, eng zich aholili hudud. Zarafshon vodiysi (Samarqand, Buxoro), Surxon–Sherobod vodiysi, Toshkent vohasi, Xorazm vohasi — madaniy-iqtisodiy markazlar. Vohalar daryo suvi hisobiga hosil bo'lgan, cho'l o'rtasidagi yashil joylardir."),
     ("Foydali qazilmalar", "Yoqilg'i: tabiiy gaz (Shurtan, Gazli), neft (Farg'ona), ko'mir (Angren). Ruda: oltin (Muruntau), mis (Olmaliq), volfram, uran (Navoiy). Noruda: osh tuzi (Boybichakon), fosforit (Qizilqum), marmar, granit, gips. Ruda konlari odatda tog'larda, neft va gaz cho'kindi havzalarda joylashgan."),
     ("Relef va xo'jalik", "Tekisliklar — sug'orma dehqonchilik, cho'l pasttekisliklari — yaylov chorvachiligi. Tog'lar — yaylov, gidroenergetika (Chorvoq, Tuyamo'yin), turizm (Chimyon, Beldersoy). Tog'li hududlar sel, ko'chki, zilzila xavfi ostida; qurilishda seysmik xavfni hisobga olish shart.")],
    ["80 % tekislik, 20 % tog'.", "Eng baland nuqta — Xo'ja-Gurgur-Ota (4643 m).", "Qizilqum — katta cho'l.", "Farg'ona vodiysi — eng zich aholi.", "Muruntau — oltin; Olmaliq — mis.", "Tog'lar sel va zilzila xavfi bilan bog'liq."],
    "O'zbekiston tekisliklari ko'p; Tyan-Shan va Pomir-Oloy tog'lari sharqda, foydali qazilmalar turli hududlarda joylashgan.",
    [("O'zbekistonda nima ko'proq?", "Tekislik", "Tog'", "Muz", "Dengiz"), ("Eng baland nuqta qaysi tizmada?", "Hisor", "Chotqol", "Qurama", "Nurota"), ("Qizilqum nima?", "Cho'l", "Tog'", "Dengiz", "Daryo"),
     ("Muruntau konida nima qazib olinadi?", "Oltin", "Gaz", "Neft", "Tuz"), ("Olmaliq nimasi bilan mashhur?", "Mis", "Oltin", "Gaz", "Ko'mir"), ("Shurtan nimasi bilan mashhur?", "Gaz", "Mis", "Oltin", "Uran")],
    [("Mingbuloq botig'i balandligi?", "−12 m", "+12 m", "4643 m", "1000 m"), ("Farg'ona vodiysining ahamiyati?", "Zich aholili hudud", "Cho'l", "Dengiz", "Muz"), ("Qaysi hudud tog'li?", "Chotqol", "Qizilqum", "Ustyurt", "Orolbo'yi"), ("Ustyurt nima?", "Plato", "Dengiz", "Vulqon", "Muzlik"),
     ("Sel xavfi qayerda?", "Tog'li hududlarda", "Cho'lda", "Dengizda", "Qutbda"), ("Angren nimasi?", "Ko'mir koni", "Oltin koni", "Neft koni", "Tuz koni"), ("Boybichakon nimasi bilan mashhur?", "Osh tuzi", "Oltin", "Neft", "Gaz"), ("Voha nima?", "Cho'l o'rtasidagi sug'oriladigan hudud", "Tog'", "Dengiz", "Muz"),
     ("Seysmik xavf nima?", "Zilzila xavfi", "Suv ko'pligi", "Issiqlik", "Shamol"), ("Tuyamo'yin nima?", "Suv ombori", "Cho'l", "Tog'", "Shahar"), ("Chorvoq nima?", "Suv ombori", "Vulqon", "Cho'l", "Plato"), ("Fosforit nima uchun?", "Mineral o'g'it", "Yoqilg'i", "Oltin olish", "Kiyim"),
     ("Neft qaysi hududda bor?", "Farg'ona vodiysi", "Qizilqum markazi", "Orol", "Chotqol cho'qqisi"), ("Marmar nima?", "Noruda qurilish materiali", "Ruda", "Gaz", "Neft"), ("Tyan-Shan qayerda?", "Sharqda", "G'arbda", "Shimolda", "Janubi-g'arbda")],
    gallery=[('g8_relef', "Relef kesimi", ("Kesimning eng baland qismi qayerda?", "Sharqda (Hisor)", "G'arbda", "Markazda", "Hamma joy teng")),
             ('g8_xarita', "Xarita", ("Xaritadagi Nukus qaysi tomonda?", "Shimoli-g'arbda", "Sharqda", "Janubda", "Janubi-sharqda"))],
    extra={'problems': [
        {'question': "Eng baland nuqta 4643 m, eng past nuqta −12 m. Balandlik farqi necha m?", 'answer': '4655', 'solution': "4643 + 12"},
        {'question': "Hududning 20 % i tog'. Maydon 450 ming km² bo'lsa, tog' necha ming km²?", 'answer': '90', 'solution': "450 · 0,2"}],
        'matching': [{'left': 'Muruntau', 'right': 'Oltin'}, {'left': 'Olmaliq', 'right': 'Mis'}, {'left': 'Shurtan', 'right': 'Gaz'}, {'left': 'Angren', 'right': "Ko'mir"}, {'left': 'Hisor tizmasi', 'right': 'Eng baland nuqta'}, {'left': 'Qizilqum', 'right': "Cho'l"}]}))

TOPICS.append(topic(36, 'g8c', "36-mavzu. O'zbekiston iqlimi, suvlari va tabiiy zonalari",
    ["Iqlim xususiyatlarini tushuntirish", "Daryolar va Orol muammosini bilish", "Balandlik mintaqalarini sanash"],
    [("Iqlim", "O'zbekiston iqlimi keskin kontinental, quruq: yoz issiq va uzoq (iyulda +28…+32 °C, cho'lda +45 °C gacha), qish nisbatan sovuq (yanvarda −8…+2 °C). Yog'in kam: cho'llarda 80–200 mm, tog' oldida 300–400 mm, tog'larda 800–1000 mm gacha. Yog'inning ko'p qismi qish va bahorda yog'adi.", 'g8_iqlim', "Toshkentda yillik harorat"),
     ("Daryolar va ko'llar", "Asosiy daryolar: Amudaryo (Pomirdan), Sirdaryo (Tyan-Shandan), Zarafshon, Qashqadaryo, Surxondaryo. Daryolar qor va muz erishi hisobiga to'yinadi, shuning uchun bahor-yozda suvi ko'p. Suv asosan sug'orishga sarflanadi. Suv omborlari: Chorvoq, Andijon, Tuyamo'yin. Suv — O'zbekiston uchun eng qimmat boylik.", 'g8_suv', "Daryolar uzunligi"),
     ("Orol dengizi fojiasi", "Orol dengizi 1960-yilda dunyodagi 4-ko'l edi (~68 ming km²). Amudaryo va Sirdaryo suvlarini paxta va g'allani sug'orishga ko'p olish tufayli u qurib, maydoni 10 baravardan ko'proq kamaydi; 2020-yilga kelib ~6 ming km² qoldi. Tubida Orolqum cho'li paydo bo'ldi, tuz-chang bo'ronlari kasalliklarni ko'paytirdi, baliqchilik yo'q bo'ldi. Hozir Orolqumda saksovul ekilmoqda, suvni tejash va xalqaro hamkorlik olib borilmoqda.", 'g8_orol', "Orol dengizi maydoni"),
     ("Tabiiy zonalar va mintaqalar", "Tekislikda cho'l (Qizilqum, Ustyurt; saksovul, kemiruvchilar, ilonlar, toshbaqa), tog' oldida adir (efemerlar — lola, qizg'aldoq), tog'da archa, yong'oq, pista o'rmonlari; yuqorida subalp va alp o'tloqlari, muzliklar. Qo'riqxonalar: Zomin, Hisor, Chotqol, Nurota. Qizil kitobga qor qoploni, Buxoro bug'usi va boshqalar kiritilgan. Tabiatni asrash har kimning burchi.")],
    ["Iqlimi keskin kontinental va quruq.", "Asosiy daryolar: Amudaryo, Sirdaryo, Zarafshon.", "Orol dengizi 1960-yildan keskin qurib ketdi.", "Orolqum cho'li quruq tubda paydo bo'ldi.", "Balandlik mintaqalari: cho'l, adir, tog', yuqori tog'.", "Qizil kitobga: qor qoploni, Buxoro bug'usi."],
    "O'zbekiston iqlimi quruq va kontinental; suv taqchil, Orol fojiasi suvdan tejamli foydalanish zarurligini ko'rsatadi.",
    [("O'zbekiston iqlimi qanday?", "Keskin kontinental, quruq", "Dengiz", "Ekvator", "Qutb"), ("Orol dengizining qurish sababi?", "Daryo suvining ko'p olinishi", "Zilzila", "Vulqon", "Yong'in"), ("Orol tubida paydo bo'lgan cho'l?", "Orolqum", "Qizilqum", "Qoraqum", "Sahro"),
     ("Amudaryo qayerdan boshlanadi?", "Pomir", "Oltoy", "Ural", "Alp"), ("Qizil kitobga kirgan?", "Qor qoploni", "Sichqon", "Chumchuq", "Qarg'a"), ("Qaysi biri suv ombori?", "Tuyamo'yin", "Qizilqum", "Hisor", "Ustyurt")],
    [("Yog'in cho'lda yiliga?", "80–200 mm", "2000 mm", "5000 mm", "0 mm"), ("Tog'larda yog'in?", "800–1000 mm gacha", "10 mm", "50 mm", "0 mm"), ("Daryolar to'yinadi?", "Qor va muz erishidan", "Faqat yomg'irdan", "Dengizdan", "Vulqondan"), ("Saksovul qayerda o'sadi?", "Cho'lda", "Alp o'tloqlarida", "Muzlikda", "Dengizda"),
     ("Adirda ko'p o'sadi?", "Efemerlar", "Kaktus", "Palma", "Baobab"), ("Qo'riqxona nima?", "Tabiat muhofaza etiladigan hudud", "Shahar", "Zavod", "Bozor"), ("Orol 1960-yilda dunyodagi nechanchi ko'l?", "4-", "1-", "10-", "20-"), ("Orolqumda nima ekilmoqda?", "Saksovul", "Paxta", "Banan", "Shakarqamish"),
     ("Sirdaryo qayerdan boshlanadi?", "Tyan-Shan", "Ural", "Alp", "Oltoy"), ("Orol qurishi oqibati?", "Tuz-chang bo'ronlari", "Yomg'ir ko'payishi", "Muzlik", "Vulqon"), ("Suvni tejash nima uchun kerak?", "Suv taqchil", "Suv juda ko'p", "Cho'l yo'q", "Hech nima"), ("Chotqol qo'riqxonasi qayerda?", "Toshkent viloyatida", "Xorazmda", "Surxondaryoda", "Qoraqalpog'istonda"),
     ("Buxoro bug'usi qayerda yashaydi?", "To'qayzorlarda", "Qutbda", "Muzlikda", "Okeanda"), ("Yog'in qaysi fasllarda ko'proq?", "Qish va bahor", "Faqat yoz", "Faqat kuz", "Hech qachon"), ("Iyulda cho'lda eng yuqori harorat?", "+45 °C gacha", "+5 °C", "0 °C", "−20 °C")],
    gallery=[('g8_iqlim', "Harorat o'zgarishi", ("Grafikda eng issiq oy?", "Iyul", "Yanvar", "Mart", "Noyabr")),
             ('g8_orol', "Orol maydoni", ("2020-yilda Orol maydoni?", "~6 ming km²", "~68 ming km²", "~36 ming km²", "~17 ming km²")),
             ('g8_suv', "Daryolar", ("Eng uzun daryo?", "Amudaryo", "Sirdaryo", "Zarafshon", "Qashqadaryo"))],
    extra={'problems': [
        {'question': "Orol maydoni 68 ming km² dan 6 ming km² ga kamaydi. Necha ming km² yo'qolgan?", 'answer': '62', 'solution': "68 − 6"},
        {'question': "Iyulda +28 °C, yanvarda −1 °C. Yillik amplituda necha °C?", 'answer': '29', 'solution': "28 − (−1)"}],
        'matching': [{'left': 'Amudaryo', 'right': 'Eng uzun daryo'}, {'left': 'Orolqum', 'right': "Orol tubidagi cho'l"}, {'left': 'Saksovul', 'right': "Cho'l o'simligi"}, {'left': 'Chorvoq', 'right': 'Suv ombori'}, {'left': 'Qor qoploni', 'right': 'Qizil kitob'}, {'left': 'Adir', 'right': 'Efemerlar zonasi'}]}))

TOPICS.append(topic(37, 'g8d', "37-mavzu. O'zbekiston aholisi va xo'jaligi",
    ["Aholi tarkibi va joylashuvini tavsiflash", "Xo'jalik tarmoqlarini bilish", "Hududiy xo'jalik markazlarini topish"],
    [("Aholi", "Aholisi ~36 mln dan oshdi va tez o'sadi; o'rtacha yosh ~28. Eng zich — Farg'ona vodiysi, Toshkent, Samarqand, Zarafshon vohalari, eng siyrak — Navoiy viloyati va Qoraqalpog'iston cho'llari. Shahar aholisi ~50 %. Ko'p millatli: o'zbek, tojik, qozoq, qoraqalpoq, rus va boshqalar."),
     ("Qishloq xo'jaligi", "Sug'orma dehqonchilik: paxta, bug'doy, sholi, sabzavot, uzum, mevalar (o'rik, shaftoli, anor), poliz. Paxta bo'yicha dunyoda yetakchilardan biri. Chorvachilik: qora mol, qo'y, qorako'l (Buxoro, Qashqadaryo), parrandachilik, ipakchilik. Tomchilatib sug'orish suvni tejash uchun joriy etilmoqda. Qishloq xo'jaligi YaIMning ~25 % ini beradi.", 'g8_xojalik', "YaIM tarkibi"),
     ("Sanoat", "Yoqilg'i-energetika (gaz, neft, IESlar, Tuyamo'yin GES, quyosh stansiyalari), kon-metallurgiya (Olmaliq, Navoiy), mashinasozlik (Asaka — avtomobil, Toshkent — samolyot), kimyo (Chirchiq, Farg'ona — o'g'it), to'qimachilik (Toshkent, Namangan, Andijon), oziq-ovqat. IT parklari va xizmatlar tez o'smoqda."),
     ("Transport va savdo", "Temir yo'l (Toshkent–Samarqand «Afrosiyob» tezyurar poyezdi), avtomobil yo'llari, aviatsiya, quvur transporti. Eksport: oltin, gaz, paxta tolasi, meva-sabzavot, to'qimachilik; hamkorlar: Xitoy, Rossiya, Qozog'iston, Turkiya. Turizm — Samarqand, Buxoro, Xiva, Shahrisabz kabi tarixiy shaharlar, Chimyon va Zomin dam olish zonalari.")],
    ["Aholi ~36 mln, yosh jamiyat.", "Eng zich — Farg'ona vodiysi va Toshkent.", "Qishloq xo'jaligi YaIMning ~25 %.", "Asaka — avtomobil sanoati.", "Afrosiyob — tezyurar poyezd.", "Eksport: oltin, gaz, paxta, meva."],
    "O'zbekiston xo'jaligi qishloq xo'jaligi, sanoat va xizmatlardan iborat; aholi vohalarda ko'p to'plangan.",
    [("Eng zich aholili hudud?", "Farg'ona vodiysi", "Qizilqum", "Ustyurt", "Orol"), ("Asakada nima ishlab chiqariladi?", "Avtomobil", "Samolyot", "Paxta", "Gaz"), ("Tezyurar poyezd?", "Afrosiyob", "Titanik", "Sapsan", "Shinkansen"),
     ("Qorako'l qayerda boqiladi?", "Buxoro va Qashqadaryo", "Qutbda", "Okeanda", "Muzlikda"), ("Qishloq xo'jaligining YaIM ulushi?", "~25 %", "~2 %", "~90 %", "~60 %"), ("Eksport mahsuloti?", "Oltin va gaz", "Banan", "Kofe", "Kakao")],
    [("Sholi qayerda ekiladi?", "Suv mo'l joyda", "Quruq cho'lda", "Tog' cho'qqisida", "Muzda"), ("Tomchilatib sug'orish nima uchun?", "Suvni tejash", "Suvni isrof", "Cho'l qilish", "Hech nima"), ("Olmaliq nimasi bilan mashhur?", "Mis", "Avtomobil", "Paxta", "Marmar"), ("Chirchiq kimyo mahsuloti?", "O'g'it", "Mashina", "Non", "Kitob"),
     ("Navoiyda nima qazib olinadi?", "Oltin va uran", "Banan", "Marmar faqat", "Kofe"), ("Hamkor davlat?", "Xitoy", "Chad", "Nepal", "Fiji"), ("IT park nima?", "Dasturiy mahsulot markazi", "Qishloq", "Zavod", "Dala"), ("Turizm markazi?", "Samarqand", "Antarktida", "Sahroi Kabir", "Grenlandiya"),
     ("Ipakchilik nima?", "Ipak qurti boqish", "Baliq ovi", "Neft", "Ko'mir"), ("Paxta qaysi turdagi ekin?", "Texnik", "G'alla", "Poliz", "Meva"), ("Aholi o'rtacha yoshi?", "~28", "~58", "~8", "~88"), ("Tuyamo'yin GES nima?", "Suv elektr stansiyasi", "Atom", "Quyosh", "Shamol"),
     ("Eng siyrak aholili hudud?", "Navoiy cho'llari", "Toshkent", "Andijon", "Farg'ona"), ("Zomin nima?", "Dam olish va qo'riqxona hududi", "Cho'l", "Dengiz", "Port"), ("Toshkent IES nima?", "Issiqlik elektr stansiyasi", "Tog'", "Daryo", "Maktab")],
    gallery=[('g8_xojalik', "YaIM tarkibi", ("Diagrammada eng katta ulush?", "Xizmatlar", "Sanoat", "Qurilish", "Boshqa")),
             ('g8_viloyat', "Aholi", ("Diagrammada eng kam aholili viloyat?", "Namangan", "Samarqand", "Farg'ona", "Qashqadaryo"))],
    extra={'problems': [
        {'question': "YaIM 100 mlrd $, qishloq xo'jaligi 25 %. Necha mlrd $?", 'answer': '25', 'solution': "100 · 0,25"},
        {'question': "Aholi 36 mln, yillik o'sish 1,5 %. Bir yilda necha ming kishi qo'shiladi?", 'answer': '540', 'solution': "36 000 000 · 0,015 = 540 000"}],
        'matching': [{'left': 'Asaka', 'right': 'Avtomobil'}, {'left': 'Olmaliq', 'right': 'Mis'}, {'left': 'Navoiy', 'right': 'Oltin, uran'}, {'left': 'Chirchiq', 'right': "Kimyo (o'g'it)"}, {'left': 'Afrosiyob', 'right': 'Tezyurar poyezd'}, {'left': "Qorako'l", 'right': 'Chorvachilik'}]}))
