# -*- coding: utf-8 -*-
from dsl import topic
from svglib import *

IMAGES = {}
TOPICS = []


def _aholi_osish():
    return linechart("Dunyo aholisi o'sishi (mlrd)", ['1800', '1900', '1950', '1975', '2000', '2023'], [1.0, 1.6, 2.5, 4.1, 6.1, 8.0], 'Yil', 'Aholi (mlrd)', labels=[(5, '8 mlrd'), (2, '2,5 mlrd')], color='#16a34a')


def _zichlik():
    return bars("Aholi zichligi (kishi/km², taxminan)", [('Bangladesh', 1100), ('Hindiston', 480), ('Yaponiya', 330), ('Yevropa (o\'rtacha)', 73), ('Qozog\'iston', 7), ('Avstraliya', 3), ('Mongoliya', 2)], 'kishi/km²')


def _dinlar():
    return pie("Dunyo aholisining diniy tarkibi (taxminan)", [('Nasroniylik', 31), ('Islom', 25), ('Hinduizm', 15), ('Buddizm', 7), ('Boshqa va dinsizlar', 22)])


def _tillar():
    return bars("Eng ko'p so'zlashuvchi tillar (mln kishi, taxminan)", [('Ingliz', 1500), ('Xitoy (mandarin)', 1100), ('Hind', 610), ('Ispan', 560), ('Arab', 380), ('Bengal', 270), ('Rus', 255)], 'mln')


def _urb():
    return linechart("Shahar aholisi ulushi (%)", ['1950', '1975', '2000', '2023', '2050'], [30, 38, 47, 57, 68], 'Yil', 'Shahar aholisi (%)', labels=[(3, '57 %'), (4, 'bashorat 68 %')], color='#7c3aed')


def _megapolis():
    return bars("Eng yirik shahar agglomeratsiyalari (mln aholi, taxminan)", [('Tokio', 37), ('Dehli', 33), ('Shanxay', 29), ('Dakka', 23), ('San-Paulu', 22), ('Mexiko', 22)], 'mln')


def _energiya():
    return pie("Dunyo birlamchi energiya balansi (taxminan)", [('Neft', 31), ('Ko\'mir', 27), ('Tabiiy gaz', 24), ('Gidro, quyosh, shamol va boshqa', 14), ('Atom energiyasi', 4)])


def _resurs_turlari():
    return flow("Tabiiy resurslar tasnifi", [('Tugaydigan', 'neft, gaz, ko\'mir'), ('Qayta tiklanadigan', "o'rmon, tuproq, baliq"), ('Tugamaydigan', 'quyosh, shamol, suv'), ('Mineral', 'ruda, tuz, qurilish')], note="Tabiiy resurslarni oqilona va tejab ishlatish zarur")


def _sektorlar():
    return pie("Jahon iqtisodiyoti tarmoqlari (YaIM ulushi, taxminan)", [('Xizmat ko\'rsatish', 65), ('Sanoat', 28), ('Qishloq xo\'jaligi', 4), ('Boshqa', 3)])


def _xojalik_tarmoq():
    return flow("Xo'jalik tarmoqlari", [("Birlamchi", "qishloq xo'jaligi, konchilik"), ("Ikkilamchi", "sanoat, qurilish"), ('Uchlamchi', "transport, savdo, xizmat"), ("To'rtlamchi", "ilm-fan, axborot, IT")], note="Rivojlangan davlatlarda xizmat ko'rsatish tarmoqlari ustun")


IMAGES.update({'g7_aholi_osish': _aholi_osish(), 'g7_zichlik': _zichlik(), 'g7_dinlar': _dinlar(), 'g7_tillar': _tillar(), 'g7_urb': _urb(), 'g7_megapolis': _megapolis(),
               'g7_energiya': _energiya(), 'g7_resurs_turlari': _resurs_turlari(), 'g7_sektorlar': _sektorlar(), 'g7_tarmoq': _xojalik_tarmoq()})

TOPICS.append(topic(29, 'g7a', "29-mavzu. Dunyo aholisi: soni, zichligi va o'sishi",
    ["Dunyo aholisi o'sish sur'atini tushuntirish", "Aholi zichligini hisoblash", "Tabiiy o'sishning tarkibiy qismlarini bilish"],
    [("Aholi soni va o'sishi", "2022-yil noyabrda dunyo aholisi 8 mlrd dan oshdi. Aholi 1800-yilda ~1 mlrd bo'lgan, 1927-yilda 2 mlrd, 1960-yilda 3 mlrd, 1974-yilda 4 mlrd, 1999-yilda 6 mlrd ga yetgan: har keyingi milliard tobora tez qo'shilgan. XX asrda tibbiyot va gigiyena rivojlanishi o'lim ko'rsatkichini keskin kamaytirdi — «demografik portlash». Hozir o'sish sur'ati sekinlashmoqda va aholi XXI asr oxirida ~10,4 mlrd da barqarorlashishi kutiladi.", 'g7_aholi_osish', "Dunyo aholisi o'sishi"),
     ("Tabiiy va mexanik o'sish", "Aholi o'zgarishi tabiiy (tug'ilish − o'lim) va mexanik (immigratsiya − emigratsiya, migratsiya) qismlardan iborat. Tabiiy o'sish promillarda (‰) hisoblanadi: 1000 kishiga to'g'ri keladigan farq. Eng yuqori tabiiy o'sish Afrika (Sahroosti) davlatlarida, eng past yoki manfiy — Yevropa va Yaponiyada, bu yerda aholi qarimoqda. O'zbekistonda yillik tug'ilish ~ 22‰ atrofida, aholi tez o'sadigan yosh jamiyat."),
     ("Aholi zichligi", "Aholi zichligi — 1 km² maydonga to'g'ri keladigan odam soni: zichlik = aholi soni : maydon. Dunyo o'rtacha ~60 kishi/km². Eng zich: Janubiy va Sharqiy Osiyo (Bangladesh >1000, Hindiston, Xitoy sharqi, Yava oroli), G'arbiy Yevropa. Eng siyrak: Avstraliya, Grenlandiya, Mongoliya, Sahroi Kabir, Sibir, Antarktida. Aholi tekisliklarda, daryo vodiylarida, qirg'oqlarda, mo'tadil va subtropik iqlimda ko'p to'planadi.", 'g7_zichlik', "Aholi zichligi"),
     ("Aholi tarkibi", "Aholi yosh va jins tarkibi bo'yicha tavsiflanadi: yosh-jins piramidasi keng asosli (yosh, tez o'sayotgan — Afrika) yoki tor asosli (qarigan — Yevropa, Yaponiya). Kutilayotgan umr: Yaponiya ~84, O'zbekiston ~74, ba'zi Afrika davlatlari ~55–60 yil. Savodxonlik darajasi, ta'lim, ish bandligi ham muhim ko'rsatkichlar. «Inson taraqqiyoti indeksi» (INI) daromad, ta'lim va sog'liqni birlashtiradi.")],
    ["2022-yil noyabrda aholi 8 mlrd dan oshdi.", "Tabiiy o'sish = tug'ilish − o'lim (‰).", "Zichlik = aholi : maydon (kishi/km²).", "Eng zich: Janubiy va Sharqiy Osiyo, G'arbiy Yevropa.", "Demografik portlash — XX asrda tez o'sish.", "Yevropa va Yaponiyada aholi qarimoqda."],
    "Dunyo aholisi 8 mlrd dan oshdi; o'sish sur'ati sekinlashmoqda, taqsimoti esa notekis.",
    [("Dunyo aholisi qachon 8 mlrd dan oshdi?", "2022-yil", "1999-yil", "1960-yil", "2050-yil"), ("Aholi zichligi qanday topiladi?", "Aholi soni : maydon", "Maydon : aholi soni", "Aholi · maydon", "Aholi − maydon"), ("Tabiiy o'sish nima?", "Tug'ilish va o'lim farqi", "Migratsiya", "Aholi soni", "Zichlik"),
     ("Eng zich qaysi hudud?", "Janubiy Osiyo", "Antarktida", "Grenlandiya", "Sahro"), ("Aholi qarigan davlat?", "Yaponiya", "Nigeriya", "Niger", "Uganda"), ("Demografik portlash qachon?", "XX asrda", "XV asrda", "I asrda", "XXI asrda boshlandi")],
    [("Dunyo o'rtacha zichligi?", "~60 kishi/km²", "~6", "~600", "~6000"), ("Eng siyrak joylardan biri?", "Mongoliya", "Bangladesh", "Yava", "Hindiston"), ("Mexanik o'sish nima?", "Migratsiya hisobiga", "Tug'ilishga", "O'limga", "Zichlikka"), ("Immigratsiya nima?", "Davlatga kirib kelish", "Chiqib ketish", "Tug'ilish", "O'lim"),
     ("Emigratsiya nima?", "Davlatdan chiqib ketish", "Kirib kelish", "O'lim", "Tug'ilish"), ("Tabiiy o'sish birligi?", "Promille (‰)", "Metr", "Kilogramm", "Gradus"), ("Keng asosli piramida nimani bildiradi?", "Yosh, o'sayotgan aholi", "Qarigan aholi", "Kam aholi", "Cho'l"), ("Eng yuqori tabiiy o'sish?", "Afrika (Sahroosti)", "Yevropa", "Yaponiya", "Rossiya"),
     ("Aholi 2 mlrd ga qachon yetgan?", "1927-yil", "1827", "1960", "1999"), ("2100-yilga bashorat?", "~10,4 mlrd", "~20 mlrd", "~2 mlrd", "~5 mlrd"), ("Aholi qayerda ko'p to'planadi?", "Tekislik va daryo vodiylarida", "Qutbda", "Cho'lda", "Tog' cho'qqisida"), ("INI nimani birlashtiradi?", "Daromad, ta'lim, sog'liq", "Faqat daromad", "Faqat maydon", "Faqat aholi"),
     ("O'zbekiston aholisi qanday?", "Yosh, tez o'sayotgan", "Qarigan", "Kamaymoqda", "Juda siyrak"), ("Qarish nimani anglatadi?", "Keksalar ulushi ortadi", "Bolalar ortadi", "Aholi ko'payadi", "Hech nima"), ("Kutilayotgan umr Yaponiyada?", "~84 yil", "~54", "~104", "~34")],
    gallery=[('g7_aholi_osish', "Dunyo aholisi o'sishi", ("Grafikda 1950-yilda aholi taxminan?", "2,5 mlrd", "1 mlrd", "6 mlrd", "8 mlrd")),
             ('g7_zichlik', "Aholi zichligi", ("Diagrammada eng zich hudud?", "Bangladesh", "Avstraliya", "Mongoliya", "Yevropa"))],
    extra={'problems': [
        {'question': "Davlat maydoni 200 000 km², aholisi 30 mln. Zichlik necha kishi/km²?", 'answer': '150', 'solution': "30 000 000 : 200 000 = 150"},
        {'question': "Tug'ilish 25‰, o'lim 7‰. Tabiiy o'sish necha ‰?", 'answer': '18', 'solution': "25 − 7"},
        {'question': "Aholisi 5 mln bo'lgan mamlakatda tabiiy o'sish 20‰. Yiliga necha kishiga ko'payadi?", 'answer': '100000', 'solution': "5 000 000 · 0,02"}],
        'matching': [{'left': 'Zichlik', 'right': 'Aholi soni : maydon'}, {'left': 'Tabiiy o\'sish', 'right': 'Tug\'ilish − o\'lim'}, {'left': 'Immigratsiya', 'right': 'Davlatga kirib kelish'}, {'left': 'Emigratsiya', 'right': 'Davlatdan chiqib ketish'}, {'left': 'Demografik portlash', 'right': 'Aholining tez o\'sishi'}, {'left': 'Yosh-jins piramidasi', 'right': 'Aholi tarkibi grafigi'}]}))

TOPICS.append(topic(30, 'g7b', "30-mavzu. Xalqlar, tillar va dinlar",
    ["Dunyo xalqlari va til oilalarini bilish", "Jahon dinlarini sanash", "Madaniy xilma-xillikni hurmat qilishni tushunish"],
    [("Xalqlar va tillar", "Yer yuzida 2000 dan ortiq xalq (etnos) va ~7000 til bor. Tillar oilalarga bo'linadi: hind-yevropa (ingliz, rus, hind, ispan, fors — eng keng tarqalgan), sino-tibet (xitoy), turkiy (o'zbek, turk, qozoq, ozarbayjon, uyg'ur), semit-xamit (arab, ivrit), fin-ugor, uralaltoy va boshqalar. Eng ko'p so'zlashadigan tillar: ingliz (jami), xitoy (ona tili sifatida), hind, ispan, arab. Davlat tili va xalqaro til (BMT: ingliz, fransuz, ispan, rus, arab, xitoy) tushunchalari bor.", 'g7_tillar', "Ko'p so'zlashadigan tillar"),
     ("Jahon dinlari", "Dunyo aholisining ko'pchiligi biror dinga e'tiqod qiladi. Jahon dinlari: nasroniylik (~31 %, Yevropa, Amerika, Avstraliya; katolik, pravoslav, protestant), islom (~25 %, Yaqin Sharq, Markaziy va Janubi-Sharqiy Osiyo, Shimoliy Afrika; Muhammad payg'ambar), buddizm (Sharqiy va Janubi-Sharqiy Osiyo), hinduizm (Hindiston). Shuningdek yahudiylik, konfutsiychilik, sintoizm. Dinlar madaniyat, urf-odat, bayramlar va hatto xo'jalik hayotiga ta'sir qiladi.", 'g7_dinlar', "Jahon dinlari ulushi"),
     ("O'zbekiston xalqlari", "O'zbekistonda 130 dan ortiq millat va elat vakillari yashaydi; aholining ~84 % i o'zbeklar, shuningdek tojik, qozoq, rus, qoraqalpoq, tatar, qirg'iz, turkman, koreys va boshqalar. Davlat tili — o'zbek tili (turkiy tillar oilasi), qoraqalpoq tili Qoraqalpog'istonda ham davlat tili. Aksariyat aholi islomga e'tiqod qiladi. Madaniy xilma-xillik va o'zaro hurmat tinchlik va barqarorlik asosi."),
     ("Madaniy meros va muloqot", "Xalq o'z tili, urf-odati, kiyimi, taomi, musiqasi bilan ajralib turadi. YuNESKO Butunjahon merosi ro'yxatiga Samarqand, Buxoro, Xiva, Shahrisabz shaharlari, «Shashmaqom», «Navro'z», «Lazgi» kiritilgan. Globallashuv davrida madaniyatlar aralashadi, lekin o'z qadriyatlarimizni asrash muhim. Boshqa xalqlar bilan muloqotda hurmat, bag'rikenglik va til bilish asosiy omillardir.")],
    ["Dunyoda ~7000 til va 2000 dan ortiq xalq bor.", "Til oilalari: hind-yevropa, sino-tibet, turkiy, semit-xamit.", "Jahon dinlari: nasroniylik, islom, buddizm, hinduizm.", "O'zbek tili turkiy tillar oilasiga kiradi.", "O'zbekistonda 130 dan ortiq millat yashaydi.", "Samarqand, Buxoro, Xiva — YuNESKO merosi."],
    "Dunyo xalqlari tili va dini bilan farqlanadi; O'zbekiston ko'p millatli davlat, bag'rikenglik muhim qadriyat.",
    [("O'zbek tili qaysi tillar oilasida?", "Turkiy", "Hind-yevropa", "Sino-tibet", "Semit"), ("Eng keng tarqalgan din (ulushi bo'yicha)?", "Nasroniylik", "Hinduizm", "Buddizm", "Yahudiylik"), ("Islomning vatani?", "Arabiston yarimoroli", "Hindiston", "Xitoy", "Yaponiya"),
     ("Hinduizm asosan qayerda?", "Hindiston", "Yaponiya", "Braziliya", "Rossiya"), ("O'zbekistonda necha millat?", "130 dan ortiq", "10", "5", "1000"), ("YuNESKO ro'yxatidagi shahar?", "Samarqand", "Chikago", "Dubay", "Seul")],
    [("Dunyoda taxminan nechta til?", "~7000", "~70", "~700", "~70 000"), ("BMT rasmiy tillaridan biri?", "Arab", "O'zbek", "Yapon", "Hind"), ("Turkiy tilga qaysi biri kiradi?", "Turk", "Fransuz", "Nemis", "Italyan"), ("Buddizm asosan qayerda?", "Sharqiy va Janubi-Sharqiy Osiyo", "Amerika", "Afrika", "Yevropa"),
     ("O'zbeklar aholining necha foizi?", "~84 %", "~20 %", "~50 %", "~100 %"), ("Navro'z qanday meros?", "Nomoddiy madaniy meros", "Tog'", "Daryo", "Shahar"), ("Shashmaqom nima?", "Musiqa janri (nomoddiy meros)", "Taom", "Kiyim", "Bino"), ("Buxoro YuNESKO ro'yxatidami?", "Ha", "Yo'q", "Faqat Xiva", "Faqat Toshkent"),
     ("Etnos nima?", "Xalq", "Til", "Din", "Shahar"), ("Qoraqalpoq tili qayerda davlat tili?", "Qoraqalpog'istonda", "Butun Rossiyada", "Xitoyda", "Turkiyada"), ("Hind-yevropa tiliga misol?", "Rus", "O'zbek", "Xitoy", "Arab"), ("Sino-tibet tiliga misol?", "Xitoy", "Ingliz", "Ispan", "Turk"),
     ("Bag'rikenglik nima?", "Boshqa madaniyatga hurmat", "Dushmanlik", "Befarqlik", "Qo'rquv"), ("Pravoslavlik qaysi dinning yo'nalishi?", "Nasroniylik", "Islom", "Buddizm", "Hinduizm"), ("Mandarin qaysi til?", "Xitoy", "Yapon", "Koreys", "Hind")],
    gallery=[('g7_dinlar', "Dunyo dinlari", ("Diagrammada eng katta ulush?", "Nasroniylik", "Islom", "Hinduizm", "Buddizm")),
             ('g7_tillar', "Tillar", ("Diagrammada eng ko'p so'zlashuvchi til?", "Ingliz", "Rus", "Arab", "Bengal"))],
    extra={'problems': [
        {'question': "Dunyo aholisi 8 mlrd, islom ~25 %. Musulmonlar taxminan necha mlrd?", 'answer': '2', 'solution': "8 · 0,25 = 2"},
        {'question': "Ingliz tilida 1500 mln, ispan tilida 560 mln so'zlashadi. Farq necha mln?", 'answer': '940', 'solution': "1500 − 560"}],
        'matching': [{'left': 'Islom', 'right': 'Yaqin Sharq va Markaziy Osiyo'}, {'left': 'Buddizm', 'right': 'Sharqiy Osiyo'}, {'left': 'Hinduizm', 'right': 'Hindiston'}, {'left': 'Turkiy tillar', 'right': "O'zbek, turk, qozoq"}, {'left': 'Hind-yevropa', 'right': 'Ingliz, rus, hind'}, {'left': 'YuNESKO', 'right': 'Jahon merosi ro\'yxati'}]}))

TOPICS.append(topic(31, 'g7c', "31-mavzu. Shaharlar va urbanizatsiya",
    ["Shahar va qishloq farqini tushuntirish", "Urbanizatsiya jarayonini bilish", "Megapolis va agglomeratsiya tushunchalarini qo'llash"],
    [("Shahar va qishloq", "Shahar — aholisi asosan sanoat, savdo, xizmat va boshqaruvda band bo'lgan, infratuzilmasi rivojlangan aholi punkti. Qishloq — asosan qishloq xo'jaligiga yo'naltirilgan. Shaharlar funksiyasiga ko'ra: sanoat, transport, ma'muriy (poytaxtlar), ilmiy, sayyohlik, portlar. Shaharlar qadimdan daryo bo'ylarida, savdo yo'llari kesishmasida paydo bo'lgan (Samarqand, Buxoro, Qohira)."),
     ("Urbanizatsiya", "Urbanizatsiya — shahar aholisi ulushining ortishi va shahar turmush tarzining tarqalishi. 1950-yilda dunyo aholisining ~30 % i shaharda yashagan, 2007-yildan beri ko'pchilik (>50 %) shaharlarda yashaydi, 2050-yilda ~68 % bo'lishi kutiladi. Rivojlangan davlatlarda shahar aholisi 75–90 %, rivojlanayotganlarda ko'proq o'sish tez, ko'pincha rejasiz (chekka kambag'al mahallalar). Urbanizatsiya iqtisodiy o'sish va ish o'rinlari beradi, lekin transport tirbandligi, havo ifloslanishi, uy-joy tanqisligi muammolarini keltiradi.", 'g7_urb', "Shahar aholisi ulushi"),
     ("Agglomeratsiya va megapolis", "Agglomeratsiya — yirik shahar va uning atrofidagi shaharchalar, qishloqlar birlashgan zich aholi punktlari tizimi. Aholisi 10 mln dan ortiq bo'lgan agglomeratsiyalar megapolislar deyiladi: Tokio (~37 mln), Dehli, Shanxay, Dakka, San-Paulu, Mexiko, Qohira, Nyu-York. Bir necha agglomeratsiya qo'shilib megalopolis (Boston–Vashington) hosil qiladi. Poytaxtlar odatda eng yirik shaharlar (Toshkent ~3 mln).", 'g7_megapolis', "Yirik agglomeratsiyalar"),
     ("Toshkent va O'zbekiston shaharlari", "O'zbekistonda ~120 shahar bor. Eng yirik shahar — Toshkent (poytaxt, ~2,9 mln, Markaziy Osiyoning eng yirik shaharlaridan biri), keyin Samarqand, Namangan, Andijon, Nukus, Buxoro, Qarshi. 1966-yilgi zilziladan keyin Toshkent zilzilabardosh qayta qurilgan. Shahar aholisi ulushi ~50 % atrofida, urbanizatsiya o'sib bormoqda. Yangi shaharlar va «aqlli shahar» loyihalari rivojlantirilmoqda.")],
    ["Urbanizatsiya — shahar aholisi ulushining ortishi.", "2007-yildan beri ko'pchilik shaharda yashaydi.", "Megapolis — 10 mln dan ortiq aholili agglomeratsiya.", "Eng yirik agglomeratsiya: Tokio.", "O'zbekistonning eng yirik shahri — Toshkent.", "Muammolar: tirbandlik, ifloslanish, uy-joy tanqisligi."],
    "Urbanizatsiya jarayonida shaharlar o'sadi, megapolislar paydo bo'ladi; bu ham imkoniyat, ham muammo yaratadi.",
    [("Urbanizatsiya nima?", "Shahar aholisi ulushining ortishi", "Shaharning kichrayishi", "Qishloq o'sishi", "Daryo o'sishi"), ("Megapolis aholisi?", "10 mln dan ortiq", "1 mln", "100 ming", "10 ming"), ("Eng yirik agglomeratsiya?", "Tokio", "Toshkent", "Rim", "Parij"),
     ("O'zbekistonning eng yirik shahri?", "Toshkent", "Samarqand", "Buxoro", "Andijon"), ("Dunyo aholisining ko'pchiligi qachondan shaharda?", "2007-yildan", "1907", "1807", "2107"), ("Shahar muammosi?", "Tirbandlik va ifloslanish", "Faqat sokinlik", "Suv ko'pligi", "Yo'q")],
    [("Agglomeratsiya nima?", "Shahar va atrofidagi aholi punktlarining birlashuvi", "Daryo", "Tog'", "Cho'l"), ("Poytaxt shahar funksiyasi?", "Ma'muriy", "Faqat sanoat", "Faqat port", "Qishloq"), ("1950-yilda shahar aholisi?", "~30 %", "~60 %", "~90 %", "~5 %"), ("2050 bashorat?", "~68 %", "~30 %", "~10 %", "~100 %"),
     ("Dehli qaysi davlatda?", "Hindiston", "Pokiston", "Xitoy", "Yaponiya"), ("San-Paulu qaysi davlatda?", "Braziliya", "Argentina", "Chili", "Peru"), ("Toshkent aholisi?", "~2,9 mln", "~29 mln", "~290 ming", "~29 ming"), ("Megalopolis nima?", "Bir necha agglomeratsiya birlashuvi", "Qishloq", "Daryo", "Tog'"),
     ("Port shahar qanday funksiya?", "Transport", "Ilmiy", "Qishloq", "Ma'muriy"), ("Rivojlangan davlatlarda shahar aholisi?", "75–90 %", "10 %", "30 %", "0 %"), ("Rejasiz urbanizatsiya natijasi?", "Chekka kambag'al mahallalar", "Yangi tog'lar", "Cho'l", "Daryo"), ("Toshkent qayta qurilgan sababi?", "1966-yil zilzilasi", "Toshqin", "Yong'in", "Urush"),
     ("Qadimiy shaharlar qayerda paydo bo'lgan?", "Daryo bo'ylarida, savdo yo'llarida", "Cho'lda", "Tog' cho'qqisida", "Qutbda"), ("Shaharlar soni O'zbekistonda?", "~120", "~12", "~1200", "~2"), ("Aqlli shahar nima?", "Texnologiyadan foydalanuvchi shahar", "Kichik shahar", "Qadimiy shahar", "Qishloq")],
    gallery=[('g7_urb', "Urbanizatsiya", ("Grafikda 2023-yilda shahar aholisi ulushi?", "57 %", "30 %", "68 %", "47 %")),
             ('g7_megapolis', "Megapolislar", ("Diagrammada eng yirik agglomeratsiya?", "Tokio", "Dehli", "Shanxay", "Mexiko"))],
    extra={'problems': [
        {'question': "Davlat aholisi 40 mln, shahar aholisi 60 %. Shaharda necha mln?", 'answer': '24', 'solution': "40 · 0,6"},
        {'question': "Tokio 37 mln, Toshkent ~3 mln. Tokio taxminan necha marta katta (butungacha)?", 'answer': '12', 'solution': "37 : 3 ≈ 12"}],
        'matching': [{'left': 'Urbanizatsiya', 'right': 'Shahar aholisi ulushining ortishi'}, {'left': 'Agglomeratsiya', 'right': 'Shahar va atrofi tizimi'}, {'left': 'Megapolis', 'right': '10 mln dan ortiq aholi'}, {'left': 'Poytaxt', 'right': 'Ma\'muriy markaz'}, {'left': 'Tokio', 'right': 'Eng yirik agglomeratsiya'}, {'left': 'Toshkent', 'right': "O'zbekiston poytaxti"}]}))

TOPICS.append(topic(32, 'g7d', "32-mavzu. Tabiiy resurslar va energetika",
    ["Tabiiy resurslarni tasniflash", "Dunyo energiya balansini bilish", "Qayta tiklanadigan energiyaning ahamiyatini tushuntirish"],
    [("Resurs turlari", "Tabiiy resurslar — inson ehtiyojlari uchun foydalaniladigan tabiat boyliklari. Tugaydigan: mineral (neft, gaz, ko'mir, ruda) — hosil bo'lishi millionlab yil talab etadi. Qayta tiklanadigan: o'rmon, tuproq, hayvonot dunyosi, chuchuk suv — to'g'ri foydalanilsa tiklanadi. Tugamaydigan: quyosh nuri, shamol, to'lqin, geotermal issiqlik. Foydalanish yo'nalishi bo'yicha: yoqilg'i-energetika, ruda, noruda, suv, yer, o'rmon, rekreatsiya resurslari.", 'g7_resurs_turlari', "Resurslar tasnifi"),
     ("Dunyo energiya balansi", "Dunyo energiya iste'molida hali ham qazilma yoqilg'i ustun: neft (~31 %), ko'mir (~27 %), tabiiy gaz (~24 %); atom ~4 %, gidro, quyosh, shamol va boshqa qayta tiklanadigan manbalar jami ~14 %. Neft eng yirik zaxiralar: Saudiya Arabistoni, Venesuela, Eron, Iroq, Kanada. Gaz: Rossiya, Eron, Qatar, AQSH. Ko'mir: Xitoy, AQSH, Hindiston, Rossiya. Qazilma yoqilg'i yoqilganda CO₂ chiqadi va global isishga sabab bo'ladi.", 'g7_energiya', "Dunyo energiya balansi"),
     ("Qayta tiklanadigan energiya", "Quyosh (fotoelektrik batareyalar), shamol (turbinalar), gidroenergiya (GES), geotermal va biomassa energiyasi kam ifloslantiradi va tugamaydi. Quyosh energiyasi ayniqsa O'zbekiston kabi quyoshli joylarda istiqbolli (yiliga 300 dan ortiq quyoshli kun). Xitoy, AQSH, Hindiston quyosh va shamol quvvatida yetakchi. Narxi tez pasaymoqda. Kamchiliklari: ob-havoga bog'liqlik, energiyani saqlash zaruriyati."),
     ("O'zbekiston resurslari", "O'zbekiston resurslarga boy: gaz (Shurtan, Kandim), neft, ko'mir (Angren — qo'ng'ir ko'mir), oltin (Muruntau — dunyodagi eng yirik ochiq konlardan biri), mis va molibden (Olmaliq), uran (Navoiy), volfram, tuz, qurilish xomashyosi. Suv resurslari cheklangan, shuning uchun suvni tejash strategik vazifa. Davlat quyosh va shamol stansiyalarini (Navoiy, Buxoro) qurmoqda.")],
    ["Resurslar: tugaydigan, qayta tiklanadigan, tugamaydigan.", "Dunyo energiyasida neft, ko'mir, gaz ustun.", "Qazilma yoqilg'i CO₂ chiqaradi.", "Quyosh va shamol — tugamaydigan energiya.", "Muruntau — yirik oltin koni.", "Angren — ko'mir koni."],
    "Tabiiy resurslar tugaydigan va tugamaydigan bo'ladi; energiyada hali qazilma yoqilg'i ustun, ammo qayta tiklanadigan energiya o'sib bormoqda.",
    [("Qaysi resurs tugamaydi?", "Quyosh energiyasi", "Neft", "Ko'mir", "Gaz"), ("Dunyo energiyasida eng katta ulush?", "Neft", "Atom", "Shamol", "Quyosh"), ("Qazilma yoqilg'i yoqilganda nima ajraladi?", "CO₂", "O₂", "N₂", "H₂"),
     ("Muruntau nimasi bilan mashhur?", "Oltin", "Neft", "Ko'mir", "Tuz"), ("Angren nimasi bilan mashhur?", "Ko'mir", "Oltin", "Gaz", "Mis"), ("Qayta tiklanadigan resursga misol?", "O'rmon", "Neft", "Ko'mir", "Gaz")],
    [("Olmaliq nimasi bilan mashhur?", "Mis", "Gaz", "Oltin", "Ko'mir"), ("Shurtan nimasi bilan mashhur?", "Gaz", "Mis", "Uran", "Oltin"), ("Navoiy nima bilan mashhur?", "Uran va oltin", "Neft", "Ko'mir", "Tuz"), ("GES nima?", "Gidroelektrostansiya", "Atom", "Quyosh", "Issiqlik"),
     ("Shamol energiyasi manbasi?", "Shamol turbinalari", "Neft", "Gaz", "Ko'mir"), ("Geotermal energiya nima?", "Yer issiqligi", "Quyosh", "Shamol", "To'lqin"), ("Neft zaxirasi yirik davlat?", "Saudiya Arabistoni", "Monako", "Fiji", "Nepal"), ("Gaz bo'yicha yirik davlat?", "Rossiya", "Nepal", "Bolivia", "Chad"),
     ("Ko'mir bo'yicha yetakchi?", "Xitoy", "Fiji", "Panama", "Monako"), ("Neft ulushi?", "~31 %", "~3 %", "~81 %", "~1 %"), ("Atom energiyasi ulushi?", "~4 %", "~40 %", "~80 %", "~0,4 %"), ("O'zbekistonda quyoshli kunlar?", "300 dan ortiq", "30", "100", "10"),
     ("Suv resursi nima?", "Qayta tiklanadigan, ammo cheklangan", "Tugamaydigan", "Mineral", "Yo'q"), ("Fotoelektrik batareya nima?", "Quyosh nurini elektrga aylantiradi", "Shamol turbinasi", "Neft", "Gaz"), ("Resurslarni nima qilish kerak?", "Tejab, oqilona ishlatish", "Isrof qilish", "Yo'q qilish", "Saqlamaslik")],
    gallery=[('g7_energiya', "Energiya balansi", ("Diagrammada eng katta ulushli manba?", "Neft", "Ko'mir", "Gaz", "Atom")),
             ('g7_resurs_turlari', "Resurslar tasnifi", ("Qaysi turga o'rmon kiradi?", "Qayta tiklanadigan", "Tugaydigan", "Tugamaydigan", "Mineral"))],
    extra={'problems': [
        {'question': "Dunyo energiyasining 31 % i neft, 27 % ko'mir, 24 % gaz. Jami qazilma yoqilg'i necha %?", 'answer': '82', 'solution': "31 + 27 + 24"},
        {'question': "Quyosh paneli kuniga 5 kVt·soat beradi. 30 kunda necha kVt·soat?", 'answer': '150', 'solution': "5 · 30"}],
        'matching': [{'left': 'Neft', 'right': 'Tugaydigan yoqilg\'i'}, {'left': 'Quyosh', 'right': 'Tugamaydigan energiya'}, {'left': 'O\'rmon', 'right': 'Qayta tiklanadigan resurs'}, {'left': 'GES', 'right': 'Suv energiyasi'}, {'left': 'Muruntau', 'right': 'Oltin koni'}, {'left': 'Angren', 'right': "Ko'mir koni"}]}))

TOPICS.append(topic(33, 'g7e', "33-mavzu. Jahon xo'jaligi va uning tarmoqlari",
    ["Xo'jalik tarmoqlarini guruhlash", "Rivojlangan va rivojlanayotgan davlatlar iqtisodiyotini solishtirish", "Transport va aloqa ahamiyatini bilish"],
    [("Xo'jalik tarmoqlari", "Jahon xo'jaligi — dunyo mamlakatlari iqtisodiyotining o'zaro bog'langan majmuasi. Tarmoqlar to'rt guruhga bo'linadi: birlamchi (qishloq xo'jaligi, o'rmon, baliq ovi, konchilik), ikkilamchi (sanoat, qurilish), uchlamchi (savdo, transport, xizmat), to'rtlamchi (ilm-fan, ta'lim, axborot texnologiyalari). Rivojlangan davlatlarda xizmat ko'rsatish YaIM ning 70–80 % ini beradi.", 'g7_tarmoq', "Xo'jalik tarmoqlari"),
     ("Jahon iqtisodiyotining tuzilishi", "Dunyo YaIMning ~65 % i xizmat ko'rsatish, ~28 % i sanoat, ~4 % i qishloq xo'jaligiga to'g'ri keladi. Rivojlangan davlatlar (AQSH, Yaponiya, Germaniya) yuqori daromad, zamonaviy texnologiya bilan; rivojlanayotganlar (ko'p Afrika, Osiyo davlatlari) qishloq xo'jaligi va xomashyo eksportiga tayangan. Yangi sanoatlashgan davlatlar (Koreya, Singapur, Xitoy) tez o'sib bormoqda.", 'g7_sektorlar', "Iqtisodiyot tarmoqlari ulushi"),
     ("Qishloq xo'jaligi va sanoat", "Qishloq xo'jaligi: dehqonchilik (g'alla — bug'doy, sholi, makkajo'xori; texnik — paxta, shakarqamish; sabzavot-meva) va chorvachilik (qora mol, qo'y, cho'chqa). Sanoat tarmoqlari: yoqilg'i-energetika, metallurgiya, mashinasozlik, kimyo, yengil va oziq-ovqat sanoati, hozirgi paytda elektronika va IT. Dunyo «fabrikasi» — Xitoy. Yirik mashinasozlik markazlari: AQSH, Yaponiya, Germaniya, Koreya. Paxta yetishtirishda Xitoy, Hindiston, AQSH, O'zbekiston oldingi qatorda."),
     ("Transport va aloqa", "Transport turlari: temir yo'l, avtomobil, dengiz (eng arzon, katta yuk), daryo, havo (tez), quvur (neft, gaz). Dengiz transporti jahon yukining ~80 % ini tashiydi. Muhim kanallar: Suvaysh, Panama. «Buyuk Ipak yo'li»ning zamonaviy davomi — Xitoy–Markaziy Osiyo–Yevropa temir yo'l koridorlari. Aloqa va internet jahon xo'jaligini bir-biriga yaqinlashtirdi (globalizatsiya). O'zbekiston dengizga chiqish yo'lidan mahrum (ikki karra yopiq davlat), shuning uchun transport koridorlari alohida ahamiyatga ega.")],
    ["Tarmoqlar: birlamchi, ikkilamchi, uchlamchi, to'rtlamchi.", "Dunyo YaIMida xizmat ko'rsatish ~65 %.", "Dengiz transporti jahon yukining ~80 % ini tashiydi.", "Xitoy — dunyo «fabrikasi».", "Suvaysh va Panama — muhim kanallar.", "O'zbekiston ikki karra yopiq davlat."],
    "Jahon xo'jaligi birlamchi, ikkilamchi, uchlamchi va to'rtlamchi tarmoqlardan iborat; xizmat ko'rsatish ustun.",
    [("Konchilik qaysi tarmoq?", "Birlamchi", "Uchlamchi", "To'rtlamchi", "Ikkilamchi"), ("Sanoat qaysi tarmoq?", "Ikkilamchi", "Birlamchi", "To'rtlamchi", "Hech qaysi"), ("Eng arzon katta yukli transport?", "Dengiz", "Havo", "Avtomobil", "Quvur"),
     ("Dunyo «fabrikasi»?", "Xitoy", "Chad", "Nepal", "Fiji"), ("YaIMda eng katta ulush?", "Xizmat ko'rsatish", "Qishloq xo'jaligi", "Sanoat", "Konchilik"), ("Suvaysh nimani bog'laydi?", "O'rta dengiz va Qizil dengiz", "Atlantika va Tinch", "Qora va Kaspiy", "Baltika va Oq")],
    [("Ilm-fan qaysi tarmoq?", "To'rtlamchi", "Birlamchi", "Ikkilamchi", "Uchlamchi"), ("Savdo qaysi tarmoq?", "Uchlamchi", "Birlamchi", "Ikkilamchi", "To'rtlamchi"), ("Panama kanali qayerda?", "Markaziy Amerika", "Afrika", "Osiyo", "Yevropa"), ("Havo transporti afzalligi?", "Tezlik", "Arzonlik", "Katta yuk", "Quvur"),
     ("Quvur transporti nimani tashiydi?", "Neft va gazni", "Odamlarni", "Mevani", "Mashinalarni"), ("Paxta yetishtiruvchi davlat?", "O'zbekiston", "Grenlandiya", "Monako", "Islandiya"), ("Mashinasozlik markazi?", "Yaponiya", "Chad", "Nepal", "Bolivia"), ("Qishloq xo'jaligi tarkibi?", "Dehqonchilik va chorvachilik", "Faqat sanoat", "Faqat savdo", "Faqat IT"),
     ("Globalizatsiya nima?", "Dunyo mamlakatlari aloqasining kuchayishi", "Izolyatsiya", "Urush", "Tabiat hodisasi"), ("Ikki karra yopiq davlat nima?", "Dengizga chiqishi yo'q va qo'shnilari ham shunday", "Orol davlat", "Dengiz davlati", "Qishloq"), ("Rivojlangan davlatda YaIM asosan?", "Xizmat ko'rsatishdan", "Qishloq xo'jaligidan", "Konchilikdan", "Ovdan"),
     ("Rivojlanayotgan davlatlar tayanadi?", "Qishloq xo'jaligi va xomashyo", "IT faqat", "Kosmos", "Robot"), ("Makkajo'xori qaysi ekin?", "G'alla", "Texnik", "Sabzavot", "Meva"), ("Shakarqamish qaysi ekin?", "Texnik", "G'alla", "Meva", "Poliz"), ("Sholi qayerda ko'p?", "Janubiy va Sharqiy Osiyo", "Qutb", "Sahro", "Tundra")],
    gallery=[('g7_tarmoq', "Xo'jalik tarmoqlari", ("Rasmda sanoat qaysi tarmoq?", "Ikkilamchi", "Birlamchi", "Uchlamchi", "To'rtlamchi")),
             ('g7_sektorlar', "YaIM tarkibi", ("Diagrammada eng kichik ulush?", "Qishloq xo'jaligi (yoki boshqa)", "Xizmat", "Sanoat", "Hammasi teng"))],
    extra={'problems': [
        {'question': "Mamlakat YaIMi 200 mlrd $; xizmat ulushi 70 %. Xizmat necha mlrd $?", 'answer': '140', 'solution': "200 · 0,7"},
        {'question': "Kema 20 tugun (≈ 37 km/soat) tezlikda 740 km yo'lni taxminan necha soatda bosadi?", 'answer': '20', 'solution': "740 : 37 = 20"}],
        'matching': [{'left': 'Birlamchi', 'right': "Qishloq xo'jaligi, konchilik"}, {'left': 'Ikkilamchi', 'right': 'Sanoat'}, {'left': 'Uchlamchi', 'right': 'Savdo, transport'}, {'left': "To'rtlamchi", 'right': 'Ilm-fan, IT'}, {'left': 'Suvaysh', 'right': 'Kanal'}, {'left': 'Globalizatsiya', 'right': 'Dunyo bog\'lanishi'}]}))
