# -*- coding: utf-8 -*-
from dsl import topic
from svglib import *

IMAGES = {}
TOPICS = []

C_ALL = {'afrika': '#fbbf24', 'avstraliya': '#fb923c', 'j_amerika': '#34d399', 'sh_amerika': '#60a5fa', 'yevroosiyo': '#c4b5fd', 'antarktida': '#e0f2fe', 'grenlandiya': '#bfdbfe'}


def _hl(name):
    return {name: '#86efac'}


def _dunyo_materik():
    return world('Dunyo materiklari', hl=C_ALL, grid=True,
                 labels=[(-105, 45, 'Shimoliy Amerika'), (-60, -15, 'Janubiy Amerika'), (20, 5, 'Afrika'), (80, 55, 'Yevroosiyo (Yevropa + Osiyo)'), (135, -25, 'Avstraliya'), (0, -80, 'Antarktida'),
                          (-150, 15, 'Tinch okean'), (-35, 25, 'Atlantika'), (80, -15, 'Hind okeani')])


def _materik_maydon():
    return bars('Materiklar maydoni', [('Osiyo', 44.4), ('Afrika', 30.3), ('Shimoliy Amerika', 24.2), ('Janubiy Amerika', 17.8), ('Antarktida', 14.1), ('Yevropa', 10.5), ('Avstraliya', 7.7)], 'mln km²',
                note="Yevroosiyo = Osiyo + Yevropa (~54,9 mln km²); Osiyo + Yevropa — bitta materik, ikki qism")


def _afrika():
    return world('Afrika (sxematik xarita)', bbox=(-22, 56, -38, 40), hl=_hl('afrika'),
                 points=[(31.2, 30.0, 'Qohira'), (3.4, 6.5, 'Lagos'), (18.4, -33.9, 'Keyptaun'), (36.8, -1.3, 'Nayrobi'), (37.4, -3.1, 'Kilimanjaro'), (33, 0, 'Viktoriya ko\'li'), (22, -4, 'Kongo havzasi'), (0, 33, 'Atlas tog\'lari')],
                 labels=[(12, 22, 'SAHROI KABIR'), (22, -22, 'Kalaxari'), (46, 6, 'Afrika shoxi')])


def _afrika_aholi():
    return bars('Afrikaning eng gavjum davlatlari (taxminan)', [('Nigeriya', 220), ('Efiopiya', 125), ('Misr', 110), ('Kongo DR', 100), ('Tanzaniya', 65)], 'mln')


def _avstr():
    return world('Avstraliya va Okeaniya (sxematik)', bbox=(108, 180, -50, -2), hl=_hl('avstraliya'),
                 points=[(149.1, -35.3, 'Kanberra'), (151.2, -33.9, 'Sidney'), (145, -37.8, 'Melburn'), (131, -25.3, 'Uluru'), (147, -18, 'Buyuk to\'siq rifi'), (174.8, -36.9, 'Oklend'), (172.6, -43.5, 'Yangi Zelandiya')],
                 labels=[(135, -27, 'AVSTRALIYA'), (150, -6, 'Papua—Yangi Gvineya')])


def _avstr_shahar():
    return bars("Avstraliyaning yirik shaharlari (mln aholi, taxminan)", [('Sidney', 5.3), ('Melburn', 5.1), ('Brisben', 2.6), ('Perth', 2.2), ('Adelaida', 1.4)], 'mln')


def _jam():
    return world('Janubiy Amerika (sxematik)', bbox=(-84, -33, -57, 15), hl=_hl('j_amerika'),
                 points=[(-47.9, -15.8, 'Braziliya'), (-58.4, -34.6, 'Buenos-Ayres'), (-77, -12, 'Lima'), (-70, -32.7, 'Akonkagua'), (-69.4, -15.8, 'Titikaka'), (-60, -3, 'Manaus (Amazonka)')],
                 labels=[(-72, -15, 'And tog\'lari'), (-62, -8, 'Amazonka pasttekisligi'), (-65, -45, 'Patagoniya')])


def _jam_daryo():
    return bars("Janubiy Amerika yirik daryolari (km)", [('Amazonka', 6400), ('Madeira', 3240), ('Parana', 4880), ('Orinoko', 2140), ('San-Fransisku', 2830)], 'km')


def _sham():
    return world('Shimoliy Amerika (sxematik)', bbox=(-170, -50, 5, 76), hl=_hl('sh_amerika'),
                 points=[(-77, 38.9, 'Vashington'), (-75.7, 45.4, 'Ottava'), (-99.1, 19.4, 'Mexiko'), (-110, 45, 'Qoyali tog\'lar'), (-85, 46, 'Buyuk ko\'llar'), (-90, 30, 'Missisipi deltasi')],
                 labels=[(-100, 38, 'AQSH'), (-100, 58, 'Kanada'), (-102, 25, 'Meksika'), (-42, 72, 'Grenlandiya')])


def _sham_kol():
    return bars("Buyuk ko'llar maydoni", [('Yuqori (Superior)', 82), ('Guron', 60), ('Michigan', 58), ('Eri', 26), ('Ontario', 19)], 'ming km²')


def _yevropa():
    return world('Yevropa (sxematik)', bbox=(-12, 45, 34, 72), hl=_hl('yevroosiyo'),
                 points=[(-0.1, 51.5, 'London'), (2.3, 48.9, 'Parij'), (13.4, 52.5, 'Berlin'), (12.5, 41.9, 'Rim'), (-3.7, 40.4, 'Madrid'), (37.6, 55.8, 'Moskva'), (10, 46.5, 'Alp'), (24, 60, 'Helsinki')],
                 labels=[(-4, 63, 'Atlantika okeani'), (20, 69, 'Skandinaviya')])


def _yevropa_aholi():
    return bars("Yevropaning yirik davlatlari aholisi (taxminan)", [('Germaniya', 84), ('Fransiya', 68), ('Italiya', 59), ('Ispaniya', 48), ('Ukraina', 38)], 'mln')


def _osiyo():
    return world('Osiyo (sxematik)', bbox=(25, 150, -12, 62), hl=_hl('yevroosiyo'),
                 points=[(69.2, 41.3, 'Toshkent'), (116.4, 39.9, 'Pekin'), (139.7, 35.7, 'Tokio'), (77.2, 28.6, 'Dehli'), (84, 28, 'Himolay'), (108, 53, 'Baykal'), (100.5, 13.7, 'Bangkok'), (106.8, -6.2, 'Jakarta')],
                 labels=[(95, 62, 'Sibir'), (100, 40, 'Markaziy Osiyo'), (50, 25, 'Arabiston')])


def _osiyo_aholi():
    return bars("Osiyoning eng gavjum davlatlari (taxminan)", [('Hindiston', 1430), ('Xitoy', 1410), ('Indoneziya', 277), ('Pokiston', 240), ('Bangladesh', 172)], 'mln')


def _antarktida():
    return world('Antarktida (sxematik, silindrik proyeksiya)', bbox=(-180, 180, -90, -55), hl={'antarktida': '#f1f5f9'},
                 points=[(106.8, -78.5, 'Vostok (−89 °C)'), (166.7, -77.8, 'Maktyurdo'), (-85, -78.5, 'Vinson'), (-60, -65, 'Antarktika yarimoroli'), (0, -90, 'Janubiy qutb')],
                 labels=[(0, -62, 'Janubiy okean')])


def _antarktida_muz():
    return bars("Antarktida muz qatlami (m)", [('O\'rtacha qalinlik', 2160), ('Eng qalin joy', 4776), ('Vinson cho\'qqisi (balandlik)', 4892)], 'm', note="Muz erib ketsa, Dunyo okeani sathi ~58 m ko'tarilar edi")


IMAGES.update({'g6_dunyo': _dunyo_materik(), 'g6_maydon': _materik_maydon(), 'g6_afrika': _afrika(), 'g6_afrika_aholi': _afrika_aholi(), 'g6_avstr': _avstr(), 'g6_avstr_shahar': _avstr_shahar(),
               'g6_jam': _jam(), 'g6_jam_daryo': _jam_daryo(), 'g6_sham': _sham(), 'g6_sham_kol': _sham_kol(), 'g6_yevropa': _yevropa(), 'g6_yevropa_aholi': _yevropa_aholi(),
               'g6_osiyo': _osiyo(), 'g6_osiyo_aholi': _osiyo_aholi(), 'g6_antarktida': _antarktida(), 'g6_antarktida_muz': _antarktida_muz()})

TOPICS.append(topic(21, 'g6a', "21-mavzu. Materiklar va okeanlar — umumiy tavsif",
    ["Yer yuzidagi materiklar va okeanlarni sanash", "Materiklarni maydoni bo'yicha solishtirish", "Quruqlik va suv nisbatini bilish"],
    [("Materiklar", "Materik (qit'a) — atrofi okean bilan o'ralgan keng quruqlik massasi. Oltita materik bor: Yevroosiyo, Afrika, Shimoliy Amerika, Janubiy Amerika, Antarktida, Avstraliya. Yevroosiyo odatda Yevropa va Osiyo qismlariga bo'linadi, shuning uchun «dunyo qismlari» soni oltita (Yevropa, Osiyo, Afrika, Amerika, Avstraliya va Okeaniya, Antarktida). Materik va unga yaqin orollar birgalikda dunyo qismini tashkil qiladi.", 'g6_dunyo', "Dunyo materiklari va okeanlari"),
     ("Maydon va taqsimot", "Eng katta materik — Yevroosiyo (~54,9 mln km²), eng kichigi — Avstraliya (7,7 mln km²). Osiyo dunyo qismi sifatida eng katta (44,4 mln km²) va eng gavjum (dunyo aholisining ~60 % i). Quruqlikning ko'p qismi shimoliy yarimsharda (68 %). Yer yuzining 29 % i quruqlik: bu ~149 mln km². Materiklar yer po'sti plitalari ustida joylashgan va yuz millionlab yillar davomida siljigan: ilgari yagona Pangeya bo'lgan.", 'g6_maydon', "Materiklar maydoni"),
     ("Okeanlar", "Dunyo okeani to'rt qismga bo'linadi: Tinch (eng katta va chuqur), Atlantika, Hind va Shimoliy Muz okeani. Okeanlar materiklarni ajratib turadi, lekin ayni paytda ularni bog'laydi: transport yo'llari, oqimlar, iqlimga ta'sir. Ba'zan Janubiy okean (Antarktida atrofida) beshinchi okean sifatida ajratiladi."),
     ("Materiklarni o'rganish rejasi", "Har bir materikni o'rganishda quyidagi reja qo'llanadi: geografik o'rni va chegaralari, tadqiqot tarixi, relyef va foydali qazilmalar, iqlim, ichki suvlar, tabiat zonalari, aholi va davlatlar. Shu reja asosida solishtirish (masalan, Afrika va Janubiy Amerika) o'xshashlik va farqlarni ko'rsatadi.")],
    ["Oltita materik: Yevroosiyo, Afrika, Sh. Amerika, J. Amerika, Antarktida, Avstraliya.", "Eng katta materik — Yevroosiyo; eng kichigi — Avstraliya.", "Osiyo dunyo aholisining ~60 % ini tashkil etadi.", "Okeanlar: Tinch, Atlantika, Hind, Shimoliy Muz.", "Quruqlik 29 %, okean 71 %.", "Pangeya — qadimgi o'ta qit'a."],
    "Yer yuzida oltita materik va to'rtta okean bor; ularni maydoni va joylashuvi bo'yicha solishtirish geografiyaning asosi.",
    [("Nechta materik bor?", "6", "5", "7", "4"), ("Eng katta materik?", "Yevroosiyo", "Afrika", "Antarktida", "Avstraliya"), ("Eng kichik materik?", "Avstraliya", "Antarktida", "Yevropa", "Janubiy Amerika"),
     ("Eng katta okean?", "Tinch", "Atlantika", "Hind", "Shimoliy Muz"), ("Dunyo aholisining ko'p qismi qaysi qismda?", "Osiyo", "Afrika", "Yevropa", "Amerika"), ("Quruqlik yer yuzining necha foizi?", "29 %", "71 %", "50 %", "10 %")],
    [("Pangeya nima?", "Qadimgi yagona o'ta qit'a", "Okean", "Tog'", "Daryo"), ("Qaysi materik eng sovuq?", "Antarktida", "Afrika", "Avstraliya", "Yevropa"), ("Afrika maydoni?", "30,3 mln km²", "7,7", "44,4", "10,5"), ("Yevropa va Osiyo qaysi materik qismlari?", "Yevroosiyo", "Afrika", "Amerika", "Avstraliya"),
     ("Quruqlik asosan qaysi yarimsharda?", "Shimoliy", "Janubiy", "Teng", "Ekvatorda"), ("Janubiy okean qayerda?", "Antarktida atrofida", "Ekvatorda", "Shimolda", "Hind okeanida"), ("Shimoliy Amerika maydoni?", "24,2 mln km²", "44,4", "7,7", "10,5"),
     ("Janubiy Amerika maydoni?", "17,8 mln km²", "30,3", "24,2", "44,4"), ("Antarktida maydoni?", "14,1 mln km²", "7,7", "30,3", "17,8"), ("Dunyo qismlari nechta?", "6", "4", "5", "7"), ("Okeanlar materiklarni nima qiladi?", "Ajratadi va bog'laydi", "Faqat ajratadi", "Faqat bog'laydi", "Yo'q qiladi"),
     ("Materikni o'rganish rejasida birinchi nima?", "Geografik o'rni", "Aholi soni", "Davlatlar", "Hayvonlar"), ("Osiyoning maydoni?", "44,4 mln km²", "30,3", "17,8", "10,5"), ("Avstraliya qaysi yarimsharda?", "Janubiy", "Shimoliy", "Ikkala", "Hech qaysi"),
     ("Materiklar nima ustida joylashgan?", "Litosfera plitalari", "Muz", "Suv", "Havo")],
    gallery=[('g6_maydon', "Materiklar maydoni", ("Diagrammada eng kichik materik?", "Avstraliya", "Yevropa", "Antarktida", "Janubiy Amerika")),
             ('g6_dunyo', "Dunyo materiklari", ("Xaritada sariq rangda ko'rsatilgan materik?", "Afrika", "Avstraliya", "Antarktida", "Shimoliy Amerika"))],
    extra={'problems': [
        {'question': "Afrika 30,3, Avstraliya 7,7 mln km². Afrika taxminan necha marta katta (butungacha yaxlitlang)?", 'answer': '4', 'solution': "30,3 : 7,7 ≈ 3,9 ≈ 4"},
        {'question': "Yer yuzi 510 mln km², quruqlik 29 %. Quruqlik necha mln km² (butungacha)?", 'answer': '148', 'solution': "510 · 0,29 = 147,9 ≈ 148"},
        {'question': "Osiyo 44,4, Yevropa 10,5 mln km². Yevroosiyo maydoni necha mln km²?", 'answer': '54,9', 'solution': "44,4 + 10,5"}],
        'matching': [{'left': 'Yevroosiyo', 'right': 'Eng katta materik'}, {'left': 'Avstraliya', 'right': 'Eng kichik materik'}, {'left': 'Antarktida', 'right': 'Eng sovuq materik'}, {'left': 'Tinch okean', 'right': 'Eng katta okean'}, {'left': 'Pangeya', 'right': "Qadimgi o'ta qit'a"}, {'left': 'Osiyo', 'right': "Eng gavjum dunyo qismi"}]}))

TOPICS.append(topic(22, 'g6b', "22-mavzu. Afrika",
    ["Afrikaning geografik o'rni va relyefini tavsiflash", "Iqlimi, daryolari va tabiat zonalarini bilish", "Aholisi va asosiy mintaqalarini sanash"],
    [("Geografik o'rni va relyef", "Afrika ekvator bo'ylab ikki yarimsharda joylashgan, tropik iqlimli materik; shimolda O'rta dengiz, sharqda Qizil dengiz va Hind okeani, g'arbda Atlantika okeani bilan o'ralgan. Suvaysh kanali Afrikani Osiyodan ajratadi. Relyefi asosan platolar va tekisliklardan iborat: shimoli-g'arbda Atlas tog'lari, sharqda Efiopiya tog'ligi, Sharqiy Afrika platosi va Kilimanjaro (5895 m, eng baland cho'qqi). Sharqiy Afrika rift tizimi tektonik yoriq bo'lib, ulkan ko'llar (Tanganika, Nyasa) hosil qilgan.", 'g6_afrika', "Afrika xaritasi (sxematik)"),
     ("Iqlim va ichki suvlar", "Afrika Yerdagi eng issiq materik. Ekvatorda nam va issiq iqlim (Kongo havzasi), shimol va janubda tropik cho'l iqlimi: Sahroi Kabir (~9 mln km², dunyoning eng katta issiq cho'li), Kalaxari, Namib. Eng uzun daryo — Nil (6650 km), u Viktoriya ko'lidan boshlanib O'rta dengizga quyiladi; boshqalari: Kongo (eng sersuv), Niger, Zambezi (Viktoriya sharsharasi). Eng katta ko'l — Viktoriya."),
     ("Tabiat zonalari", "Afrikada tabiat zonalari ekvatordan har ikki tomonga simmetrik joylashgan: nam ekvatorial o'rmonlar (Kongo havzasi), savannalar (eng keng zona; fil, sher, jirafa, zebra), tropik cho'llar (Sahro, Kalaxari), subtropik qattiq bargli o'rmon va butazorlar (shimol va janub chekkalari). Savanna milliy bog'lari (Serengeti) dunyoga mashhur. Afrikada eng boy foydali qazilmalar: oltin, olmos (Janubiy Afrika, Botsvana), mis, neft (Nigeriya, Liviya, Jazoir), uran."),
     ("Aholi va davlatlar", "Afrika aholisi ~1,4 mlrd, dunyo aholisining ~18 % i, eng tez o'sayotgan hudud. Eng gavjum davlatlar: Nigeriya, Efiopiya, Misr, Kongo DR. 54 ta mustaqil davlat bor. Mintaqalari: Shimoliy Afrika (arab madaniyati, Misr), Tropik (Sahroosti), Janubiy Afrika. Aholining ko'pi qishloq xo'jaligida band, urbanizatsiya tez. Misr tsivilizatsiyasi (piramidalar) insoniyat tarixidagi eng qadimgi tsivilizatsiyalardan biri.", 'g6_afrika_aholi', "Afrikaning yirik davlatlari aholisi")],
    ["Afrika — ekvator kesib o'tadigan issiq materik.", "Eng baland: Kilimanjaro (5895 m).", "Sahroi Kabir — eng katta issiq cho'l (~9 mln km²).", "Nil — eng uzun daryo; Kongo — eng sersuv.", "Savanna — eng keng tabiat zonasi.", "Aholi ~1,4 mlrd, 54 davlat."],
    "Afrika issiq tropik materik bo'lib, ekvator bo'ylab simmetrik tabiat zonalari, boy foydali qazilmalar va tez o'sayotgan aholiga ega.",
    [("Afrikaning eng baland cho'qqisi?", "Kilimanjaro", "Elbrus", "Everest", "Atlas"), ("Eng katta cho'l?", "Sahroi Kabir", "Kalaxari", "Gobi", "Atakama"), ("Eng uzun daryo?", "Nil", "Kongo", "Niger", "Zambezi"),
     ("Eng sersuv Afrika daryosi?", "Kongo", "Nil", "Niger", "Orange"), ("Afrikada eng keng tabiat zonasi?", "Savanna", "Tayga", "Tundra", "Dasht"), ("Eng katta ko'l?", "Viktoriya", "Tanganika", "Nyasa", "Chad")],
    [("Afrikaning shimolida qaysi dengiz?", "O'rta dengiz", "Qora", "Baltika", "Oq"), ("Suvaysh kanali nimani ajratadi?", "Afrikani Osiyodan", "Yevropani Osiyodan", "Amerikani", "Avstraliyani"), ("Atlas tog'lari qayerda?", "Shimoli-g'arb", "Janub", "Sharq", "Markaz"), ("Viktoriya sharsharasi qaysi daryoda?", "Zambezi", "Nil", "Kongo", "Niger"),
     ("Serengeti nima?", "Savanna milliy bog'i", "Cho'l", "Tog'", "Daryo"), ("Olmos qayerda ko'p?", "Janubiy Afrika, Botsvana", "Misr", "Liviya", "Marokash"), ("Afrika aholisi?", "~1,4 mlrd", "~140 mln", "~14 mlrd", "~14 mln"), ("Afrikada nechta davlat?", "54", "20", "100", "10"),
     ("Misr tsivilizatsiyasi nimasi bilan mashhur?", "Piramidalar", "Ko'priklar", "Sirk", "Metro"), ("Rift tizimi nima?", "Tektonik yoriq", "Daryo", "Cho'l", "Tog' tizmasi"), ("Tanganika qanday ko'l?", "Tektonik, chuqur", "Vulqon", "Muz", "Qoldiq"), ("Afrika iqlimi?", "Eng issiq materik", "Eng sovuq", "Mo'tadil", "Qutb"),
     ("Kalaxari qayerda?", "Janubiy Afrika", "Shimol", "Sharq", "G'arb"), ("Nigeriya nima bilan mashhur?", "Aholisi eng ko'p, neft", "Cho'l", "Tog'", "Okean"), ("Nil qaysi dengizga quyiladi?", "O'rta dengiz", "Qizil", "Qora", "Kaspiy"), ("Namib qayerda?", "Atlantika sohili (janubi-g'arb)", "Sharq", "Markaz", "Shimol")],
    gallery=[('g6_afrika', "Afrika xaritasi", ("Xaritadagi eng baland cho'qqi belgisi qaysi?", "Kilimanjaro", "Atlas", "Kongo", "Nil")),
             ('g6_afrika_aholi', "Aholi", ("Diagrammada eng gavjum davlat?", "Nigeriya", "Efiopiya", "Misr", "Tanzaniya"))],
    extra={'problems': [
        {'question': "Nil 6650 km, Kongo 4700 km. Nil necha km uzunroq?", 'answer': '1950', 'solution': "6650 − 4700"},
        {'question': "Kilimanjaro 5895 m. Tog' etagida +30 °C bo'lsa, cho'qqida (6 °C/km) taxminan necha °C (butungacha)?", 'answer': '-5', 'solution': "5,895 · 6 ≈ 35,4; 30 − 35 ≈ −5"},
        {'question': "Nigeriya aholisi 220 mln, Misr 110 mln. Nigeriya necha marta ko'p?", 'answer': '2', 'solution': "220 : 110 = 2"}],
        'matching': [{'left': 'Sahroi Kabir', 'right': 'Eng katta issiq cho\'l'}, {'left': 'Kilimanjaro', 'right': 'Afrika cho\'qqisi'}, {'left': 'Nil', 'right': 'Eng uzun daryo'}, {'left': 'Kongo', 'right': 'Eng sersuv daryo'}, {'left': 'Viktoriya', 'right': "Eng katta ko'l"}, {'left': 'Savanna', 'right': 'Fil, sher, zebra zonasi'}]}))

TOPICS.append(topic(23, 'g6c', "23-mavzu. Avstraliya va Okeaniya",
    ["Avstraliyaning o'rnini va tabiatini tavsiflash", "Endemik hayvonot dunyosini bilish", "Okeaniya orollari guruhlarini sanash"],
    [("Geografik o'rni", "Avstraliya — eng kichik va eng tekis materik; butunlay janubiy yarimsharda. Atrofi Hind va Tinch okeanlari bilan o'ralgan. Materik davlati — Avstraliya Ittifoqi, poytaxti Kanberra (eng katta shahri Sidney emas, Kanberra poytaxt!). Kapitan Kuk 1770-yilda sharqiy qirg'oqni xaritaga tushirgan. Avstraliya va Okeaniya birgalikda dunyo qismini tashkil qiladi.", 'g6_avstr', "Avstraliya va Okeaniya xaritasi"),
     ("Relyef va iqlim", "Relyef: g'arbda keng platolar, markazda pasttekislik, sharqda Buyuk Suvayirg'ich tizmasi (eng baland cho'qqi Kostyushko, 2228 m). Materikning ko'p qismi (~40 %) cho'l va yarim cho'l (Katta Qum, Gibson, Katta Viktoriya cho'llari), chunki iqlim tropik va subtropik qurg'oqchil. Eng yirik daryo — Murrey va Darling; Eyr ko'li vaqtli suvlidan iborat (cho'ldagi eng katta ko'l, ba'zan qurib qoladi). Sharqiy qirg'oqda dunyoning eng katta marjon riffi — Buyuk To'siq rifi (~2300 km)."),
     ("Tabiat va endemiklar", "Materik uzoq vaqt boshqa qit'alardan ajralgan holda rivojlangani uchun hayvon va o'simliklarning ~80 % i endemik: kenguru, koala, emu, platipus (tuxum qo'yuvchi sut emizuvchi), tasmaniya ayig'i, dingo. Qopchiqli sut emizuvchilar keng tarqalgan. O'simliklar: evkalipt (ko'p turli), akatsiya. Chorvachilik (qo'y, mol) rivojlangan: Avstraliya jun yetkazib berishda dunyoda yetakchi. Foydali qazilmalar: temir rudasi, ko'mir, boksit, oltin, uran."),
     ("Okeaniya", "Okeaniya — Tinch okeanning markaziy va janubiy qismidagi minglab orollar: Melaneziya (Yangi Gvineya, Fiji), Mikroneziya, Polineziya (Gavayi, Samoa, Taiti), shuningdek Yangi Zelandiya. Orollar vulqon (baland) va marjon (past atoll) kelib chiqishiga ega. Iqlim — ekvatorial va tropik, dengiz iqlimi. Yangi Zelandiya (poytaxti Vellington) fyordlari va geyzerlari bilan mashhur. Iqlim isishi tufayli past atollar dengiz ostida qolish xavfi ostida.", 'g6_avstr_shahar', "Avstraliyaning yirik shaharlari")],
    ["Avstraliya — eng kichik va eng tekis materik.", "Poytaxti — Kanberra.", "Eng baland cho'qqi: Kostyushko (2228 m).", "~40 % maydon cho'l va yarim cho'l.", "Endemiklar: kenguru, koala, emu, platipus.", "Okeaniya: Melaneziya, Mikroneziya, Polineziya."],
    "Avstraliya quruq, tekis va endemiklarga boy materik; Okeaniya Tinch okeandagi orollar dunyosi.",
    [("Avstraliyaning poytaxti?", "Kanberra", "Sidney", "Melburn", "Perth"), ("Eng baland cho'qqi?", "Kostyushko", "Everest", "Elbrus", "Kilimanjaro"), ("Kenguru qayerda yashaydi?", "Avstraliya", "Afrika", "Janubiy Amerika", "Yevropa"),
     ("Buyuk To'siq rifi nima?", "Marjon riff", "Tog'", "Daryo", "Cho'l"), ("Avstraliya qaysi yarimsharda?", "Janubiy", "Shimoliy", "Ikkalasida", "Hech qaysi"), ("Okeaniyaga qaysi orollar kiradi?", "Polineziya", "Yevropa", "Antarktida", "Grenlandiya")],
    [("Avstraliyaning eng yirik shaharlaridan biri?", "Sidney", "Berlin", "Rim", "Toshkent"), ("Koala nima?", "Qopchiqli hayvon", "Qush", "Baliq", "Sudralib yuruvchi"), ("Emu nima?", "Uchmaydigan yirik qush", "Hayvon", "Baliq", "O'simlik"), ("Platipus nimasi bilan mashhur?", "Tuxum qo'yuvchi sut emizuvchi", "Uchadi", "Baliq", "O'txo'r qush"),
     ("Endemik nima?", "Faqat shu yerda yashovchi tur", "Ko'chib yuruvchi", "Yirtqich", "Qush"), ("Murrey daryosi qayerda?", "Avstraliya", "Afrika", "Osiyo", "Yevropa"), ("Eyr ko'li qanday?", "Vaqtli suvli cho'l ko'li", "Doim chuchuk", "Muz", "Vulqon"), ("Avstraliya nimada yetakchi?", "Jun yetkazib berishda", "Paxta", "Banan", "Neft"),
     ("Yangi Zelandiya poytaxti?", "Vellington", "Oklend", "Sidney", "Kanberra"), ("Atoll nima?", "Halqasimon marjon orol", "Vulqon", "Daryo", "Tog'"), ("Gavayi qaysi guruhda?", "Polineziya", "Melaneziya", "Mikroneziya", "Yevropa"), ("Fiji qaysi guruhda?", "Melaneziya", "Polineziya", "Mikroneziya", "Afrika"),
     ("Avstraliyada qaysi o'simlik ko'p?", "Evkalipt", "Palma", "Qarag'ay", "Chinor"), ("Buyuk Suvayirg'ich tizmasi qayerda?", "Sharqda", "G'arbda", "Markazda", "Shimolda"), ("Kapitan Kuk sharqiy qirg'oqni qachon xaritaga tushirgan?", "1770", "1470", "1870", "1970")],
    gallery=[('g6_avstr', "Avstraliya xaritasi", ("Xaritada Buyuk To'siq rifi qayerda?", "Sharqiy qirg'oq yaqinida", "G'arbda", "Markazda", "Janubda")),
             ('g6_avstr_shahar', "Yirik shaharlar", ("Diagrammada eng ko'p aholili shahar?", "Sidney", "Perth", "Adelaida", "Brisben"))],
    extra={'problems': [
        {'question': "Avstraliya maydoni 7,7 mln km², shundan ~40 % cho'l. Cho'l necha mln km²?", 'answer': '3,08', 'solution': "7,7 · 0,4 = 3,08"},
        {'question': "Buyuk To'siq rifi ~2300 km. Poyezd 100 km/soat bilan shuncha masofani necha soatda bosadi?", 'answer': '23', 'solution': "2300 : 100 = 23"}],
        'matching': [{'left': 'Kanberra', 'right': 'Poytaxt'}, {'left': 'Kostyushko', 'right': 'Eng baland cho\'qqi'}, {'left': 'Kenguru', 'right': 'Endemik qopchiqli'}, {'left': 'Murrey', 'right': 'Yirik daryo'}, {'left': 'Atoll', 'right': 'Marjon halqa-orol'}, {'left': 'Polineziya', 'right': 'Okeaniya guruhi'}]}))

TOPICS.append(topic(24, 'g6d', "24-mavzu. Janubiy Amerika",
    ["Janubiy Amerika relyefi va daryolarini tavsiflash", "Tabiat zonalari va iqlimini bilish", "Aholi va davlatlarini sanash"],
    [("Geografik o'rni va relyef", "Janubiy Amerika G'arbiy yarimsharda, asosan janubiy yarimsharda joylashgan; g'arbda Tinch okean, sharqda Atlantika okeani. Kolumb 1498-yilda sharqiy qirg'oqqa yetgan. Relyefi: g'arbida eng uzun (~9000 km) tog' tizmasi — And tog'lari (eng baland Akonkagua, 6961 m — G'arbiy yarimsharning eng baland cho'qqisi), sharqda Amazonka pasttekisligi, Gviana va Braziliya platolari.", 'g6_jam', "Janubiy Amerika xaritasi"),
     ("Daryolar va iqlim", "Amazonka — dunyoning eng sersuv daryosi (dunyo daryo oqimining ~20 % i), uzunligi ~6400 km, havzasi ~7 mln km². Boshqa yirik daryolar: Orinoko, Parana, San-Fransisku. Eng baland sharshara — Anxel (979 m, Venesuela). Titikaka — dunyodagi eng baland (3812 m) kemalar qatnaydigan ko'l. Iqlim: ekvatorial (Amazonka), subekvatorial, tropik, subtropik, janubda mo'tadil. Peru oqimi tufayli g'arbiy sohilda Atakama — eng quruq cho'l.", 'g6_jam_daryo', "Janubiy Amerika daryolari"),
     ("Tabiat zonalari", "Nam ekvatorial o'rmonlar (selvas — Amazoniya, dunyodagi eng katta tropik o'rmon, biologik xilma-xillik markazi), savannalar (lyanos, kampos), cho'llar (Atakama, Patagoniya), dashtlar (pampa — Argentina, unumdor tekislik). Hayvonot dunyosi: yaguar, tapir, anakonda, kolibri, kondor, lama, alpaka. Ekinlar: kofe (Braziliya), kakao, shakarqamish, kartoshka va makkajo'xori shu yerdan tarqalgan."),
     ("Aholi va davlatlar", "Aholisi ~440 mln. 12 ta mustaqil davlat: Braziliya (eng katta va gavjum, portugal tili, ~215 mln), Argentina, Peru, Kolumbiya, Chili va boshqalar. Ko'pchilik ispan tilida so'zlashadi, Braziliyada portugal tilida. Aholi tarkibi aralash: hindular, yevropaliklar, afrikaliklar avlodlari. Yirik shaharlar: San-Paulu, Buenos-Ayres, Lima, Bogota. Inklar qadimgi imperiyasi (Machu-Pikchu) And tog'larida bo'lgan.")],
    ["And — eng uzun tog' tizmasi; Akonkagua 6961 m.", "Amazonka — eng sersuv daryo.", "Anxel — eng baland sharshara (979 m).", "Atakama — eng quruq cho'l.", "Amazoniya — eng katta tropik o'rmon.", "Braziliya — eng katta va gavjum davlat."],
    "Janubiy Amerika And tog'lari, Amazonka va Amazoniya o'rmonlari bilan mashhur; aholisi aralash, Braziliya eng yirik davlat.",
    [("Janubiy Amerikaning eng baland cho'qqisi?", "Akonkagua", "Everest", "Elbrus", "Kilimanjaro"), ("Eng sersuv daryo?", "Amazonka", "Parana", "Orinoko", "Nil"), ("Eng baland sharshara?", "Anxel", "Niagara", "Viktoriya", "Iguasu"),
     ("Eng quruq cho'l?", "Atakama", "Gobi", "Sahro", "Kalaxari"), ("Eng katta davlat?", "Braziliya", "Argentina", "Peru", "Chili"), ("And tog'lari qayerda?", "G'arbda", "Sharqda", "Markazda", "Janubda faqat")],
    [("Pampa nima?", "Argentina dashti", "Cho'l", "Tog'", "Daryo"), ("Titikaka qanday ko'l?", "Eng baland kemalar qatnaydigan ko'l", "Eng katta", "Eng chuqur", "Sho'r"), ("Braziliyada qaysi til?", "Portugal", "Ispan", "Ingliz", "Fransuz"), ("Boshqa davlatlarda asosiy til?", "Ispan", "Portugal", "Rus", "Arab"),
     ("Machu-Pikchu kimlarniki?", "Inklar", "Mayyalar", "Misrliklar", "Ruslar"), ("Kofe qaysi davlatda ko'p?", "Braziliya", "Chili", "Peru", "Bolivia"), ("Yaguar qayerda?", "Amazoniya", "Tundra", "Cho'l", "Qutb"), ("Lama qayerda?", "And tog'larida", "Cho'lda", "Daryoda", "Qutbda"),
     ("Kondor nima?", "Katta qush", "Baliq", "Hayvon", "Ilon"), ("Selvas nima?", "Nam ekvatorial o'rmon", "Cho'l", "Dasht", "Tundra"), ("Amazonka havzasi?", "~7 mln km²", "~700 km²", "~70 km²", "~7 km²"), ("Kolumb sharqiy qirg'oqqa qachon yetgan?", "1498", "1298", "1698", "1798"),
     ("Janubiy Amerikada nechta mustaqil davlat?", "12", "50", "5", "30"), ("Aholisi?", "~440 mln", "~44 mln", "~4,4 mlrd", "~44 ming"), ("San-Paulu qaysi davlatda?", "Braziliya", "Argentina", "Peru", "Chili")],
    gallery=[('g6_jam', "Janubiy Amerika xaritasi", ("Xaritadagi Akonkagua qaysi tog'da?", "And", "Gviana platosi", "Braziliya platosi", "Patagoniya")),
             ('g6_jam_daryo', "Daryolar", ("Diagrammada eng uzun daryo?", "Amazonka", "Parana", "Orinoko", "Madeira"))],
    extra={'problems': [
        {'question': "Amazonka 6400 km, Parana 4880 km. Farq necha km?", 'answer': '1520', 'solution': "6400 − 4880"},
        {'question': "Akonkagua 6961 m. Tog' etagida +25 °C bo'lsa, cho'qqida (6 °C/km) taxminan necha °C (butungacha)?", 'answer': '-17', 'solution': "6,961·6 ≈ 41,8; 25 − 42 ≈ −17"}],
        'matching': [{'left': 'And', 'right': 'Eng uzun tog\' tizmasi'}, {'left': 'Amazonka', 'right': 'Eng sersuv daryo'}, {'left': 'Atakama', 'right': 'Eng quruq cho\'l'}, {'left': 'Pampa', 'right': 'Argentina dashti'}, {'left': 'Anxel', 'right': 'Eng baland sharshara'}, {'left': 'Machu-Pikchu', 'right': 'Inklar shahri'}]}))

TOPICS.append(topic(25, 'g6e', "25-mavzu. Shimoliy Amerika",
    ["Shimoliy Amerika relyefi va iqlimini tavsiflash", "Buyuk ko'llar va yirik daryolarni bilish", "AQSH, Kanada va Meksika haqida asosiy ma'lumotlarni bilish"],
    [("Geografik o'rni va relyef", "Shimoliy Amerika G'arbiy yarimsharda joylashgan; shimolda Shimoliy Muz, g'arbda Tinch, sharqda Atlantika okeani. Panama kesmasi uni Janubiy Amerikadan ajratadi. Relyefi: g'arbda Kordilyera tizmasi (Qoyali tog'lar, Sierra-Nevada; eng baland Denali, 6190 m), sharqda eski Appalachi tog'lari, markazda keng Markaziy (Buyuk) tekislik.", 'g6_sham', "Shimoliy Amerika xaritasi"),
     ("Ichki suvlar", "Eng yirik daryo tizimi — Missisipi (Missuri bilan birga ~6275 km). Buyuk ko'llar (Yuqori, Guron, Michigan, Eri, Ontario) dunyodagi eng katta chuchuk suv zaxiralaridan; ularni Sent-Lorens daryosi okeanga bog'laydi. Niagara sharsharasi Eri va Ontario ko'llari orasida (AQSH va Kanada chegarasida). Kolorado daryosi Grand-Kanyonni o'ygan.", 'g6_sham_kol', "Buyuk ko'llar maydoni"),
     ("Iqlim va tabiat zonalari", "Materik shimoldan janubga uzun bo'lgani uchun deyarli barcha iqlim mintaqalarida joylashgan: arktika va subarktika (Kanada shimoli, Alyaska), mo'tadil (AQSH, Kanada), subtropik (Florida, Texas), tropik (Meksika, Markaziy Amerika). Zonalar: tundra, tayga (Kanada), aralash va keng bargli o'rmonlar, dasht (preriya), cho'l (Sonora, Katta Havza), tropik o'rmonlar. Janubi-sharqiy qirg'oq tropik bo'ronlarga (uraganlar) duchor. Katta tabiiy resurslar: neft, gaz, ko'mir, ruda."),
     ("Aholi va davlatlar", "Aholisi ~600 mln; tub aholi — hindular va inuitlar, hozirgi aholi asosan Yevropadan, Afrikadan va boshqa qit'alardan kelgan muhojirlar avlodi. Yirik davlatlar: AQSH (~335 mln, dunyo iqtisodiyotida yetakchi, poytaxti Vashington), Kanada (maydoni bo'yicha dunyoda 2-o'rin, poytaxti Ottava), Meksika (poytaxti Mexiko). Yirik shaharlar: Nyu-York, Los-Anjeles, Chikago, Toronto, Mexiko. Sanoat, qishloq xo'jaligi va ilmiy-texnik taraqqiyot yuqori darajada.")],
    ["Eng baland: Denali (6190 m).", "Kordilyera g'arbda, Appalachi sharqda.", "Missisipi — eng yirik daryo tizimi.", "Buyuk ko'llar — dunyodagi eng katta chuchuk ko'l tizimi.", "Niagara — mashhur sharshara.", "Davlatlar: AQSH, Kanada, Meksika."],
    "Shimoliy Amerika Kordilyera, Buyuk ko'llar va Missisipi bilan mashhur; AQSH, Kanada va Meksika asosiy davlatlar.",
    [("Shimoliy Amerikaning eng baland cho'qqisi?", "Denali", "Akonkagua", "Elbrus", "Everest"), ("Buyuk ko'llar nechta?", "5", "3", "7", "10"), ("Eng yirik daryo tizimi?", "Missisipi", "Amazonka", "Nil", "Volga"),
     ("AQSH poytaxti?", "Vashington", "Nyu-York", "Los-Anjeles", "Chikago"), ("Kanada poytaxti?", "Ottava", "Toronto", "Vankuver", "Monreal"), ("Niagara sharsharasi qayerda?", "AQSH va Kanada chegarasida", "Meksikada", "Braziliyada", "Afrikada")],
    [("Qoyali tog'lar qayerda?", "G'arbda", "Sharqda", "Janubda", "Markazda faqat"), ("Appalachi qanday tog'lar?", "Eski, past", "Yosh, baland", "Vulqon", "Muz"), ("Preriya nima?", "Shimoliy Amerika dashti", "Cho'l", "Tayga", "Tundra"), ("Uragan nima?", "Tropik bo'ron", "Zilzila", "Qor", "Vulqon"),
     ("Meksika poytaxti?", "Mexiko", "Kankun", "Gvadalaxara", "Akapulko"), ("Grand-Kanyonni qaysi daryo hosil qilgan?", "Kolorado", "Missisipi", "Gudzon", "Yukon"), ("Panama kesmasi nimani ajratadi?", "Shimoliy va Janubiy Amerikani", "Yevropa va Osiyoni", "Afrika va Osiyoni", "Avstraliyani"),
     ("Kanada maydoni bo'yicha dunyoda?", "2-o'rin", "10-o'rin", "1-o'rin", "50-o'rin"), ("Inuitlar kimlar?", "Shimoliy tub xalq", "Janub xalqi", "Yevropaliklar", "Afrikaliklar"), ("AQSH aholisi?", "~335 mln", "~33 mln", "~3,3 mlrd", "~335 ming"), ("Sonora qaysi cho'l?", "Shimoliy Amerikada", "Afrikada", "Osiyoda", "Yevropada"),
     ("Shimoliy Amerika aholisi?", "~600 mln", "~60 mln", "~6 mlrd", "~6 mln"), ("Alyaska qaysi davlatda?", "AQSH", "Kanada", "Rossiya", "Meksika"), ("Sent-Lorens nimaga quyiladi?", "Atlantika okeaniga", "Tinch okeanga", "Shimoliy Muz okeaniga", "Meksika ko'rfaziga"), ("Florida iqlimi?", "Subtropik", "Arktik", "Cho'l", "Ekvatorial")],
    gallery=[('g6_sham', "Shimoliy Amerika xaritasi", ("Xaritada Qoyali tog'lar qaysi qismda?", "G'arbda", "Sharqda", "Janubda", "Shimolda")),
             ('g6_sham_kol', "Buyuk ko'llar", ("Diagrammada eng katta ko'l?", "Yuqori (Superior)", "Guron", "Eri", "Ontario"))],
    extra={'problems': [
        {'question': "Yuqori ko'l 82 ming km², Ontario 19 ming km². Farq necha ming km²?", 'answer': '63', 'solution': "82 − 19"},
        {'question': "Missisipi 6275 km. Poyezd 90 km/soat bilan taxminan necha soatda bosadi (butungacha)?", 'answer': '70', 'solution': "6275 : 90 ≈ 69,7 ≈ 70"}],
        'matching': [{'left': 'Denali', 'right': 'Eng baland cho\'qqi'}, {'left': 'Missisipi', 'right': 'Yirik daryo'}, {'left': 'Niagara', 'right': 'Sharshara'}, {'left': 'Preriya', 'right': 'Dasht'}, {'left': 'Ottava', 'right': 'Kanada poytaxti'}, {'left': 'Vashington', 'right': 'AQSH poytaxti'}]}))

TOPICS.append(topic(26, 'g6f', "26-mavzu. Yevropa",
    ["Yevropaning geografik o'rni va relyefini tavsiflash", "Iqlimi va daryolarini bilish", "Aholisi va yirik davlatlarini sanash"],
    [("Geografik o'rni", "Yevropa — Yevroosiyoning g'arbiy qismi, shimolda Shimoliy Muz okeani, g'arbda Atlantika okeani, janubda O'rta dengiz bilan chegaradosh; Osiyodan Ural tog'lari, Ural daryosi, Kaspiy dengizi va Kavkaz tog'lari bo'ylab ajraladi. Qirg'oq chizig'i juda o'yilgan (yarimorollar: Skandinaviya, Pireney, Apennin, Bolqon). Maydoni ~10,5 mln km², dunyoning eng kichik qit'a qismlaridan biri, ammo aholisi ~750 mln.", 'g6_yevropa', "Yevropa xaritasi"),
     ("Relyef", "Yevropaning katta qismi tekislik: Sharqiy Yevropa (Rus) tekisligi, Markaziy Yevropa tekisligi. Tog'lar: Alp (Monblan, 4806 m — eng baland), Pireney, Karpat, Kavkaz (Elbrus, 5642 m — Yevropaning eng baland cho'qqisi chegaraga bog'liq), Skandinaviya tog'lari. Janubda faol vulqonlar (Vezuviy, Etna) va zilzilalar. Muzlik faoliyati shimolda ko'llar va fyordlarni hosil qilgan."),
     ("Iqlim va suvlar", "Iqlim asosan mo'tadil: g'arbda dengiz (Atlantika va Golfstrim ta'siri, yumshoq qish), sharqda mo'tadil kontinental, janubda subtropik O'rta dengiz iqlimi (yozi quruq issiq, qishi nam iliq). Yevropaning eng uzun daryosi — Volga (3530 km, Kaspiyga quyiladi); boshqalari: Dunay, Reyn, Dnepr, Don, Elba. Yevropa daryolari kemachilik uchun muhim, Reyn–Dunay kanali Shimoliy dengiz va Qora dengizni bog'laydi."),
     ("Aholi va davlatlar", "Yevropada ~45 ta davlat bor; eng yiriklari: Rossiya (Yevropa qismi bilan), Germaniya (~84 mln, eng ko'p aholili Yevropa Ittifoqi davlati), Fransiya, Italiya, Ispaniya, Buyuk Britaniya. Aholi gavjum va urbanlashgan, o'rtacha umr ko'rish yuqori, tug'ilish past. Yevropa Ittifoqi (EI) — 27 davlat iqtisodiy va siyosiy ittifoqi, yagona valyuta — yevro. Mashhur shaharlar: London, Parij, Rim, Berlin, Madrid. Yevropa sanoat, turizm, madaniyat va ilm markazlaridan biri.", 'g6_yevropa_aholi', "Yirik davlatlar aholisi")],
    ["Yevropa Osiyodan Ural, Kavkaz va Kaspiy bo'ylab ajraladi.", "Qirg'oq chizig'i o'yilgan, ko'p yarimorollar.", "Alp tog'lari — Monblan (4806 m).", "Volga — Yevropaning eng uzun daryosi.", "Iqlim mo'tadil; janubda O'rta dengiz iqlimi.", "Yevropa Ittifoqi — 27 davlat, yevro valyutasi."],
    "Yevropa o'yilgan qirg'oqli, mo'tadil iqlimli, gavjum va rivojlangan dunyo qismi.",
    [("Yevropaning eng uzun daryosi?", "Volga", "Dunay", "Reyn", "Dnepr"), ("Alpning eng baland cho'qqisi?", "Monblan", "Elbrus", "Everest", "Etna"), ("Yevropa Osiyodan qaysi tog'lar bo'ylab ajraladi?", "Ural", "Alp", "Pireney", "Karpat"),
     ("Yevropa Ittifoqi valyutasi?", "Yevro", "Dollar", "Funt faqat", "Rubl"), ("O'rta dengiz iqlimi qayerda?", "Janubda", "Shimolda", "Sharqda", "G'arbda"), ("Yevropaning eng ko'p aholili YI davlati?", "Germaniya", "Fransiya", "Italiya", "Ispaniya")],
    [("Skandinaviya nima?", "Yarimorol", "Orol", "Tog'", "Daryo"), ("Pireney qayerda?", "Ispaniya va Fransiya chegarasida", "Italiya", "Germaniya", "Polsha"), ("Vezuviy qayerda?", "Italiya", "Ispaniya", "Fransiya", "Gretsiya"), ("Fyord nima?", "Tor chuqur dengiz ko'rfazi", "Daryo", "Cho'l", "Tog'"),
     ("Dunay qaysi dengizga quyiladi?", "Qora dengiz", "Baltika", "Shimoliy dengiz", "Kaspiy"), ("Reyn qayerda?", "G'arbiy Yevropa", "Sharqiy Yevropa", "Janubiy Yevropa", "Shimoliy"), ("Golfstrim Yevropa iqlimini?", "Yumshatadi", "Sovutadi", "Ta'sir qilmaydi", "Quritadi"), ("Yevropa maydoni?", "~10,5 mln km²", "~105 mln", "~1 mln", "~50 mln"),
     ("Yevropa aholisi?", "~750 mln", "~75 mln", "~7,5 mlrd", "~7 mln"), ("Yevropa Ittifoqi nechta davlat?", "27", "5", "100", "15"), ("Londonda qaysi davlat poytaxti?", "Buyuk Britaniya", "Fransiya", "Italiya", "Germaniya"), ("Rim qaysi davlat poytaxti?", "Italiya", "Ispaniya", "Gretsiya", "Fransiya"),
     ("Pitsa va pasta vatani?", "Italiya", "Fransiya", "Germaniya", "Polsha"), ("Eng baland Yevropa cho'qqisi (Kavkaz)?", "Elbrus", "Monblan", "Etna", "Vezuviy"), ("Yevropa tekisligi nima?", "Katta qismi tekislik", "Faqat tog'", "Faqat cho'l", "Faqat muz")],
    gallery=[('g6_yevropa', "Yevropa xaritasi", ("Xaritada Alp tog'lari qaysi qismda?", "Janubiy-markaziy", "Shimolda", "G'arbda", "Sharqda")),
             ('g6_yevropa_aholi', "Aholi", ("Diagrammada eng ko'p aholili davlat?", "Germaniya", "Fransiya", "Italiya", "Ukraina"))],
    extra={'problems': [
        {'question': "Germaniya 84 mln, Fransiya 68 mln. Farq necha mln?", 'answer': '16', 'solution': "84 − 68"},
        {'question': "Volga 3530 km. Kema 20 km/soat tezlikda taxminan necha soatda bosadi (butungacha)?", 'answer': '177', 'solution': "3530 : 20 = 176,5 ≈ 177"}],
        'matching': [{'left': 'Monblan', 'right': 'Alpning eng baland cho\'qqisi'}, {'left': 'Volga', 'right': 'Eng uzun Yevropa daryosi'}, {'left': 'Skandinaviya', 'right': 'Shimoliy yarimorol'}, {'left': 'Yevropa Ittifoqi', 'right': '27 davlat ittifoqi'}, {'left': 'Vezuviy', 'right': 'Italiya vulqoni'}, {'left': 'Yevro', 'right': 'Yagona valyuta'}]}))

TOPICS.append(topic(27, 'g6g', "27-mavzu. Osiyo",
    ["Osiyoning geografik o'rni va relyefini tavsiflash", "Iqlim, daryolar va tabiat zonalarini bilish", "Aholisi va mintaqalarini sanash"],
    [("Geografik o'rni va relyef", "Osiyo — dunyoning eng katta qismi (~44,4 mln km²): Yevroosiyoning sharqiy qismi, to'rt okean (Shimoliy Muz, Tinch, Hind) bilan chegaradosh va deyarli barcha iqlim mintaqalarini o'z ichiga oladi. Relyefi: Yer yuzidagi eng baland tog'lar — Himolay (Everest 8849 m, Jomolungma), Tibet platosi (dunyo tomi), Pomir, Tyan-Shan, Oltoy, Kavkaz; keng tekisliklar: G'arbiy Sibir, Turon, Hind-Gang, Buyuk Xitoy. Shuningdek Yerdagi eng chuqur chuqurlik (Mertvoye dengiz suvi sathi −430 m) bu yerda.", 'g6_osiyo', "Osiyo xaritasi"),
     ("Iqlim va ichki suvlar", "Osiyoda iqlim juda xilma-xil: arktik, subarktik, mo'tadil kontinental va keskin kontinental (Yakutiya — shimoliy yarimsharning sovuq qutbi), tropik cho'l (Arabiston), musson (Hindiston, Janubi-Sharqiy Osiyo, Sharqiy Xitoy; yozgi mussonlar katta yog'in beradi), ekvatorial. Yirik daryolar: Yantszi, Huanxe, Gang, Hind, Mekong, Ob, Yenisey, Lena; Amudaryo va Sirdaryo yopiq havzaga quyiladi. Baykal (eng chuqur ko'l) va Kaspiy (eng katta ko'l)."),
     ("Tabiat zonalari", "Osiyoda barcha zonalar uchraydi: tundra va tayga (Sibir — eng katta tayga massivi), mo'tadil dasht va cho'llar (Markaziy Osiyo, Gobi), subtropik va tropik o'rmonlar (Hindixitoy, Indoneziya), musson o'rmonlari, savannalar. Hayvonot dunyosi: yo'lbars, pandalar, fil, tuya, qor qoploni. Foydali qazilmalar: neft va gaz (Fors ko'rfazi, Sibir), ko'mir, temir, rangli metallar, qimmatbaho toshlar."),
     ("Aholi va mintaqalar", "Osiyo aholisi ~4,7 mlrd — dunyo aholisining ~60 % i. Eng gavjum davlatlar: Hindiston (~1,43 mlrd) va Xitoy (~1,41 mlrd). Mintaqalari: Shimoliy, Markaziy (O'zbekiston, Qozog'iston, Qirg'iziston, Tojikiston, Turkmaniston), Sharqiy (Xitoy, Yaponiya, Koreya), Janubi-Sharqiy, Janubiy va G'arbiy Osiyo. Dunyo dinlari (islom, buddizm, hinduizm, nasroniylik) Osiyoda paydo bo'lgan. Buyuk Ipak yo'li Osiyoni Yevropa bilan bog'lagan. Hozir Osiyo iqtisodiy o'sishda yetakchi.", 'g6_osiyo_aholi', "Osiyoning gavjum davlatlari")],
    ["Osiyo — eng katta dunyo qismi (44,4 mln km²).", "Himolay va Everest (8849 m) — eng baland.", "Yakutiya — shimoliy yarimsharning sovuq qutbi.", "Musson iqlimi Hindiston va Janubi-Sharqiy Osiyoda.", "Aholisi ~4,7 mlrd (dunyoning ~60 %).", "Hindiston va Xitoy — eng gavjum davlatlar."],
    "Osiyo eng katta va eng gavjum dunyo qismi, eng baland tog'lar, turli iqlim va qadimiy madaniyatlar maskani.",
    [("Eng baland cho'qqi?", "Everest (Jomolungma)", "Elbrus", "Akonkagua", "Kilimanjaro"), ("Dunyo aholisining qancha qismi Osiyoda?", "~60 %", "~10 %", "~25 %", "~90 %"), ("Eng gavjum davlat?", "Hindiston", "Yaponiya", "Rossiya", "Indoneziya"),
     ("Musson iqlimi qayerda?", "Hindiston va Janubi-Sharqiy Osiyo", "Yevropa", "Antarktida", "Sahro"), ("Eng chuqur ko'l?", "Baykal", "Kaspiy", "Viktoriya", "Superior"), ("Osiyo maydoni?", "44,4 mln km²", "4,4", "444", "10,5")],
    [("Tibet platosi qanday ataladi?", "Dunyo tomi", "Dunyo bog'i", "Dunyo daryosi", "Dunyo o'rmoni"), ("Himolay qaysi plitalar to'qnashuvidan?", "Hind va Yevroosiyo", "Tinch va Amerika", "Afrika va Yevropa", "Avstraliya"), ("Sibir qanday zona?", "Tayga", "Cho'l", "Savanna", "Tundra"),
     ("Yantszi qayerda?", "Xitoy", "Hindiston", "Yaponiya", "Rossiya"), ("Gang daryosi qayerda?", "Hindiston", "Xitoy", "Rossiya", "Eron"), ("Mekong qayerda?", "Janubi-Sharqiy Osiyo", "Yevropa", "Afrika", "Amerika"), ("Gobi nima?", "Cho'l", "Tog'", "Daryo", "Dengiz"),
     ("Qor qoploni qayerda?", "Tog'larda (Pomir, Tyan-Shan)", "Dengizda", "Cho'lda", "Tropik o'rmonda"), ("Buyuk Ipak yo'li nimani bog'lagan?", "Osiyoni Yevropa bilan", "Amerikani", "Afrikani", "Avstraliyani"), ("Toshkent qaysi mintaqada?", "Markaziy Osiyo", "Sharqiy Osiyo", "G'arbiy Osiyo", "Janubiy Osiyo"),
     ("Yaponiya qaysi mintaqada?", "Sharqiy Osiyo", "Markaziy", "G'arbiy", "Janubiy"), ("Fors ko'rfazi nima bilan boy?", "Neft va gaz", "Oltin faqat", "Ko'mir", "Olmos"), ("Osiyo aholisi?", "~4,7 mlrd", "~470 mln", "~47 mlrd", "~47 mln"), ("Yakutiya qanday?", "Sovuq qutb", "Issiq", "Nam", "Musson"),
     ("Hindixitoy qaysi mintaqada?", "Janubi-Sharqiy Osiyo", "Markaziy", "Shimoliy", "G'arbiy")],
    gallery=[('g6_osiyo', "Osiyo xaritasi", ("Xaritada Himolay qaysi davlat yaqinida?", "Hindiston", "Yaponiya", "Indoneziya", "Rossiya")),
             ('g6_osiyo_aholi', "Aholi", ("Diagrammada eng ko'p aholili davlat?", "Hindiston", "Xitoy", "Indoneziya", "Pokiston"))],
    extra={'problems': [
        {'question': "Hindiston 1430 mln, Xitoy 1410 mln. Farq necha mln?", 'answer': '20', 'solution': "1430 − 1410"},
        {'question': "Osiyo aholisi 4,7 mlrd, dunyo 8 mlrd. Osiyo ulushi necha foiz (taxminan, butungacha)?", 'answer': '59', 'solution': "4,7 : 8 · 100 ≈ 58,75 ≈ 59"}],
        'matching': [{'left': 'Everest', 'right': 'Eng baland cho\'qqi'}, {'left': 'Baykal', 'right': "Eng chuqur ko'l"}, {'left': 'Musson', 'right': 'Fasllar bo\'yicha shamol'}, {'left': 'Gobi', 'right': "Cho'l"}, {'left': 'Yantszi', 'right': 'Xitoyning eng uzun daryosi'}, {'left': 'Hindiston', 'right': 'Eng gavjum davlat'}]}))

TOPICS.append(topic(28, 'g6h', "28-mavzu. Antarktida va Arktika",
    ["Antarktidaning tabiati va tadqiqot tarixini bilish", "Arktika va Antarktida farqini aytish", "Qutb hududlarining iqlim uchun ahamiyatini tushuntirish"],
    [("Antarktida", "Antarktida — Janubiy qutb atrofidagi materik (14,1 mln km²), deyarli butunlay muz bilan qoplangan. Uni 1820-yilda F. Bellinsgauzen va M. Lazarev ekspeditsiyasi kashf etgan; Janubiy qutbga birinchi bo'lib 1911-yil R. Amundsen yetib borgan. Muz qalinligi o'rtacha ~2160 m (eng qalin joyi ~4776 m); u Yer chuchuk suvining ~60 % ini saqlaydi. 1959-yilgi Antarktika shartnomasi materikni faqat tinch ilmiy maqsadda foydalanish uchun ajratgan; doimiy aholisi yo'q, faqat tadqiqotchilar.", 'g6_antarktida', "Antarktida (sxematik)"),
     ("Iqlim va tabiat", "Antarktida — eng sovuq, eng quruq va eng shamolli materik: Vostok stansiyasida 1983-yilda −89,2 °C qayd etilgan, yog'in juda kam (cho'l!), shamol tezligi 80 m/s gacha. Yozda (dekabr–fevral) qutb kuni, qishda qutb tuni. O'simliklar — moxlar va lishayniklar; qirg'oqlarda pingvinlar (imperator pingvin), tyulenlar, kitlar, albatros; Janubiy okeanda krill (mayda qisqichbaqa) oziq zanjirining asosi. Muz ostida ko'llar (Vostok) va tog'lar (Vinson, 4892 m) bor.", 'g6_antarktida_muz', "Antarktida muzi"),
     ("Arktika", "Arktika — Shimoliy qutb atrofidagi hudud: materik emas, Shimoliy Muz okeani (muz bilan qoplangan) va uning atrofidagi quruqlik (Grenlandiya, Kanada, Rossiya, Alyaska, Skandinaviya shimoli). Qutb ayig'i, morj, tyulen, shimol bug'usi, shimol tulkisi yashaydi; tub xalqlar — inuitlar, nenetslar, saamlar. Arktikada neft va gaz zaxiralari, shimoliy dengiz yo'llari (Shimoliy dengiz yo'li) mavjud."),
     ("Qutb muzlari va iqlim o'zgarishi", "Qutb muzlari Quyosh nurini qaytarib (albedo), Yer iqlimini sovutib turadi. Global isish tufayli Arktikada dengiz muzi qisqarmoqda (har o'n yilda ~13 %), Grenlandiya va Antarktida muzliklari erib, Dunyo okeani sathi yiliga ~3–4 mm ko'tarilmoqda. Qutb ayig'ining yashash joyi qisqarmoqda. Qutb hududlarini muhofaza qilish butun insoniyat uchun muhim.")],
    ["Antarktida — materik; Arktika — okean va uning atrofi.", "Antarktida — eng sovuq (−89,2 °C), eng quruq materik.", "Antarktida muzi chuchuk suvning ~60 % i.", "Janubiy qutbga 1911-yil Amundsen yetib borgan.", "Antarktida shartnomasi — 1959-yil.", "Muzlar erishi okean sathini ko'taradi."],
    "Antarktida muz bilan qoplangan materik, Arktika esa muzli okean; ikkala qutb ham iqlim uchun muhim va global isishdan zarar ko'rmoqda.",
    [("Antarktidani kim kashf etgan?", "Bellinsgauzen va Lazarev", "Kolumb", "Magellan", "Kuk"), ("Antarktida iqlimi?", "Eng sovuq va quruq", "Issiq va nam", "Mo'tadil", "Tropik"), ("Janubiy qutbga birinchi yetgan?", "Amundsen", "Skott", "Piri", "Nansen"),
     ("Arktika nima?", "Shimoliy qutb atrofi (okean va quruqlik)", "Janubiy materik", "Cho'l", "Tog' tizmasi"), ("Pingvinlar qayerda yashaydi?", "Antarktida va janubiy yarimshar", "Arktika", "Sahro", "Amazonka"), ("Antarktida shartnomasi?", "1959-yil", "1859", "1959-yil emas, 1759", "2009")],
    [("Qutb ayig'i qayerda?", "Arktika", "Antarktida", "Afrika", "Avstraliya"), ("Antarktida muzining chuchuk suvdagi ulushi?", "~60 %", "~6 %", "~1 %", "~100 %"), ("Eng past harorat qayd etilgan joy?", "Vostok", "Moskva", "Yakutsk", "Oymyakon"), ("Eng baland Antarktida cho'qqisi?", "Vinson", "Everest", "Elbrus", "Denali"),
     ("Krill nima?", "Mayda qisqichbaqa", "Baliq", "Qush", "Kit"), ("Muz Quyosh nurini?", "Qaytaradi", "Yutadi", "Ko'paytiradi", "Yo'q qiladi"), ("Dengiz muzi Arktikada?", "Qisqarmoqda", "Kengaymoqda", "O'zgarmaydi", "Yo'q"), ("Okean sathi yiliga?", "~3–4 mm ko'tarilmoqda", "~3–4 m", "~3–4 sm", "Tushmoqda"),
     ("Antarktidada doimiy aholi?", "Yo'q, faqat tadqiqotchilar", "Millionlab", "Minglab", "Yuzlab doimiy"), ("Inuitlar kimlar?", "Arktikaning tub xalqi", "Antarktika", "Afrika xalqi", "Yevropaliklar"), ("Albedo nima?", "Sirtning nurni qaytarish xususiyati", "Harorat", "Bosim", "Shamol"),
     ("Antarktidada yog'in?", "Juda kam", "Ko'p", "Doim yomg'ir", "Har kuni"), ("Qutb kuni nima?", "Yarim yil davomida Quyosh botmaydi", "Bir kunlik", "Oy yorug'i", "Doimiy tun"), ("Antarktida maydoni?", "14,1 mln km²", "1,4", "141", "7,7"), ("Shimoliy dengiz yo'li qayerda?", "Arktikada (Rossiya shimolida)", "Antarktidada", "Hind okeanida", "Sahroda")],
    gallery=[('g6_antarktida', "Antarktida xaritasi", ("Xaritadagi Vostok stansiyasi nimasi bilan mashhur?", "Eng past harorat", "Eng issiq joy", "Eng baland cho'qqi", "Eng katta shahar")),
             ('g6_antarktida_muz', "Muz qalinligi", ("Eng qalin joyda muz qalinligi?", "4776 m", "2160 m", "1000 m", "100 m"))],
    extra={'problems': [
        {'question': "Muz qalinligi o'rtacha 2160 m. Eng qalin joyi 4776 m. Farq necha m?", 'answer': '2616', 'solution': "4776 − 2160"},
        {'question': "Dengiz sathi yiliga 3 mm ko'tarilsa, 50 yilda necha mm?", 'answer': '150', 'solution': "3 · 50"},
        {'question': "Vostokda −89 °C, Toshkentda yanvarda −1 °C. Farq necha °C?", 'answer': '88', 'solution': "−1 − (−89) = 88"}],
        'matching': [{'left': 'Amundsen', 'right': 'Janubiy qutbga birinchi yetgan'}, {'left': 'Vostok', 'right': 'Eng past harorat qayd etilgan'}, {'left': 'Krill', 'right': 'Oziq zanjiri asosi'}, {'left': 'Arktika', 'right': 'Muzli okean va atrofi'}, {'left': 'Antarktida', 'right': 'Muz bilan qoplangan materik'}, {'left': 'Albedo', 'right': 'Nurni qaytarish'}]}))
