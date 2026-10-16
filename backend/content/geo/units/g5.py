# -*- coding: utf-8 -*-
from dsl import topic
from svglib import *

IMAGES = {}
TOPICS = []


def _oziq_zanjiri():
    return flow('Oziq zanjiri', [('Quyosh', 'energiya manbai'), ('O\'simlik', 'ishlab chiqaruvchi'), ('O\'txo\'r hayvon', '1-tartib iste\'molchi'), ('Yirtqich', '2-tartib iste\'molchi'), ('Chirituvchilar', 'bakteriya, zamburug\'')], note="Har bir bosqichda energiyaning ~90 % i yo'qoladi")


def _energiya_piramidasi():
    return layers('Ekologik energiya piramidasi', [("3-tartib iste'molchi", "0,1 % energiya (burgut, bo'ri)", '#ef4444', 10), ("2-tartib iste'molchi", "1 % energiya (yirtqichlar)", '#f59e0b', 14), ("1-tartib iste'molchi", "10 % energiya (o'txo'rlar)", '#84cc16', 18), ("Ishlab chiqaruvchilar", "100 % energiya (o'simliklar)", '#22c55e', 30)])


def _tuproq_profil():
    return layers('Tuproq profili (gorizontlar)', [("O — to'shama", "o'simlik qoldiqlari", '#78350f', 8), ("A — gumusli gorizont", "unumdor, qora/to'q rangli", '#451a03', 16), ("B — to'planish", "suv bilan yuvilgan moddalar", '#a16207', 16),
                                              ("C — ona jins", "mayda jins bo'laklari", '#d6b88a', 16), ("R — tog' jinsi", "qattiq jins", '#94a3b8', 14)], note="Tuproq qatlami juda yupqa (1–2 m), ammo hayot uchun asos")


def _tuproq_tarkib():
    return pie('Tuproq tarkibi (hajm bo\'yicha, o\'rtacha)', [('Mineral zarrachalar', 45), ('Suv', 25), ('Havo', 25), ('Organik moddalar (gumus)', 5)])


def _gumus():
    return bars('Tuproqdagi gumus miqdori', [('Qora tuproq (chernozem)', 10), ('Kashtan tuproq', 4), ('Bo\'z tuproq (O\'zbekiston)', 1.5), ('Sahro (qumli) tuproq', 0.5)], '%', note='Gumus qancha ko\'p bo\'lsa, tuproq shuncha unumdor')


def _zonalar():
    return zones('Tabiat zonalari (shimoliy yarimshar, tekisliklarda)', [
        ('Arktika cho\'li', 'muz va qor, kam o\'simlik', '#e0f2fe', 90, 70), ('Tundra', 'moxlar, lishayniklar, bodom', '#bfdbfe', 70, 62), ('Tayga', 'ignabargli o\'rmon', '#86efac', 62, 52),
        ('Aralash va keng bargli o\'rmon', 'emen, qayin, qarag\'ay', '#4ade80', 52, 45), ('Dasht', "o'tlar, qora tuproq", '#fde68a', 45, 40), ('Cho\'l va yarim cho\'l', "saksovul, yantoq", '#fdba74', 40, 25),
        ('Savanna', "baland o'tlar, daraxt-butalar", '#fbbf24', 25, 8), ('Nam ekvatorial o\'rmon', "ko'p qavatli, doim yashil", '#22c55e', 8, 0)],
        note="Zonalar kenglik bo'yicha o'zgaradi (iqlim va tuproq bilan birga)")


def _vertikal():
    return profile('Tyan-Shan tog\'larida vertikal mintaqalilik', [(0, 4), (12, 8), (28, 22), (45, 40), (62, 62), (78, 85), (88, 100), (100, 96)],
                   [(6, 14, "Cho'l (500 m gacha)"), (20, 34, "Adir (dasht)"), (36, 54, "Tog' o'rmon-butazor"), (52, 72, "Subalp o'tloqlari"), (68, 92, "Alp o'tloqlari"), (92, 100, "Muz va qor")])


IMAGES.update({'g5_oziq_zanjiri': _oziq_zanjiri(), 'g5_energiya': _energiya_piramidasi(), 'g5_tuproq_profil': _tuproq_profil(), 'g5_tuproq_tarkib': _tuproq_tarkib(), 'g5_gumus': _gumus(),
               'g5_zonalar': _zonalar(), 'g5_vertikal': _vertikal()})

TOPICS.append(topic(18, 'g5a', "18-mavzu. Biosfera va ekotizimlar",
    ["Biosfera chegaralarini va tarkibini bilish", "Ekotizim tarkibini va oziq zanjirini tuzish", "Energiya piramidasi qoidasini qo'llash"],
    [("Biosfera", "Biosfera — Yer yuzasida hayot tarqalgan qobiq: litosferaning yuqori qismi, butun gidrosfera va atmosferaning quyi qismi. Biosfera haqidagi ta'limotni V. I. Vernadskiy yaratgan. Hayot dengiz tubidan (~11 km) tog' cho'qqilarigacha (~6–8 km) uchraydi, eng boy qismi — tuproq va okean sirti. Tirik organizmlar modda va energiya aylanishida ishtirok etib, atmosferadagi kislorod miqdorini va iqlimni shakllantirgan."),
     ("Ekotizim va oziq zanjiri", "Ekotizim (ekologik tizim) — tirik organizmlar va ular yashaydigan muhitning birligi (o'rmon, ko'l, cho'l). Tarkibi: ishlab chiqaruvchilar (o'simliklar, fotosintez bilan organik modda yaratadi), iste'molchilar (hayvonlar: o'txo'r, yirtqich) va chirituvchilar (bakteriya, zamburug'lar, organik qoldiqlarni oddiy moddalarga ajratadi). Oziq zanjiri: o'simlik → quyon → tulki → burgut. Ko'plab zanjirlar oziq to'ri hosil qiladi.", 'g5_oziq_zanjiri', "Oziq zanjiri"),
     ("Energiya oqimi", "Quyosh energiyasi o'simliklarda organik modda sifatida to'planadi, keyingi bosqichlarga o'tganda taxminan 10 % i uzatiladi (10 % qoidasi), qolgani issiqlik sifatida yo'qoladi. Shuning uchun zanjir uzun bo'lmaydi (3–5 bo'g'in) va yirtqichlar soni o'txo'rlardan kam bo'ladi. Energiya piramidasi shu qonuniyatni ko'rsatadi. Modda esa aylanadi: uglerod, azot, suv, kislorod.", 'g5_energiya', "Energiya piramidasi"),
     ("Biologik xilma-xillik", "Biologik xilma-xillik — turlar, genlar va ekotizimlar boyligi. Eng boy ekotizimlar: nam ekvatorial o'rmonlar va marjon riflari. Hozir turlar tabiiy tezlikdan 100–1000 marta tez yo'qolmoqda (o'rmonlar kesilishi, ifloslanish, ov, iqlim o'zgarishi). Himoya uchun qo'riqxonalar, milliy bog'lar va Qizil kitob tashkil etilgan. O'zbekistonda Zomin, Chatqol, Nurota qo'riqxonalari mavjud.")],
    ["Biosfera — hayot qobig'i (Vernadskiy).", "Ekotizim: ishlab chiqaruvchi, iste'molchi, chirituvchi.", "10 % qoidasi: har bosqichda energiyaning ~10 % i uzatiladi.", "Oziq zanjiri odatda 3–5 bo'g'indan iborat.", "Eng boy biologik xilma-xillik: nam ekvatorial o'rmon va marjon riflari.", "Qizil kitob — yo'qolayotgan turlar ro'yxati."],
    "Biosfera hayot qobig'i bo'lib, ekotizimlarda moddalar aylanadi va energiya bosqichma-bosqich kamayadi.",
    [("Biosfera haqidagi ta'limotni kim yaratgan?", "V. I. Vernadskiy", "Darvin", "Gumbolt", "Dokuchayev"), ("Ishlab chiqaruvchilar kimlar?", "O'simliklar", "Yirtqichlar", "Bakteriyalar", "O'txo'rlar"), ("Chirituvchilar kimlar?", "Bakteriya va zamburug'lar", "Yirtqichlar", "O'simliklar", "Baliqlar"),
     ("Energiyaning qancha qismi keyingi bosqichga o'tadi?", "~10 %", "~90 %", "100 %", "~50 %"), ("Qizil kitob nima?", "Yo'qolayotgan turlar ro'yxati", "Kitob do'koni", "Xarita", "Lug'at"), ("Eng boy ekotizim?", "Nam ekvatorial o'rmon", "Cho'l", "Tundra", "Arktika")],
    [("Fotosintez nima?", "O'simlikda nur energiyasidan organik modda hosil bo'lishi", "Nafas olish", "Yog'in", "Bug'lanish"), ("Yirtqich qaysi toifaga kiradi?", "Iste'molchi", "Ishlab chiqaruvchi", "Chirituvchi", "Mineral"), ("Oziq to'ri nima?", "Ko'p oziq zanjirlarining birikuvi", "Baliq to'ri", "Yo'l tarmog'i", "Daryo"),
     ("Oziq zanjiri nega qisqa?", "Energiya yo'qolishi tufayli", "Hayvon yo'qligidan", "Suv yo'qligidan", "Qor tufayli"), ("Energiya piramidasi asosida kimlar?", "Ishlab chiqaruvchilar", "Yirtqichlar", "Chirituvchilar", "Odamlar"), ("Marjon riflari qayerda?", "Issiq dengizlarda", "Qutbda", "Cho'lda", "Tog'da"),
     ("Zomin qo'riqxonasi qaysi viloyatda?", "Jizzax", "Samarqand", "Xorazm", "Navoiy"), ("Qo'riqxona nima?", "Tabiat to'liq muhofaza qilinadigan hudud", "Dam olish maskani", "Ferma", "Ko'l"), ("Biosfera chegarasi dengiz tubida?", "~11 km", "~1 km", "~100 km", "0"),
     ("Turlarning yo'qolishi sababi?", "O'rmon kesish, ifloslanish, ov", "Faqat zilzila", "Faqat vulqon", "Faqat shamol"), ("Biologik xilma-xillik nima?", "Turlar, genlar, ekotizimlar boyligi", "Faqat hayvon soni", "Faqat o'simlik soni", "Daryolar soni"), ("Quyon qaysi toifaga kiradi?", "1-tartib iste'molchi (o'txo'r)", "Yirtqich", "Chirituvchi", "Ishlab chiqaruvchi"),
     ("Tulki qaysi toifaga kiradi?", "2-tartib iste'molchi", "Ishlab chiqaruvchi", "Chirituvchi", "1-tartib"), ("Moddalar ekotizimda qanday?", "Aylanadi", "Yo'qoladi", "Faqat to'planadi", "Muzlaydi"), ("Energiya ekotizimda?", "Bir tomonlama oqadi va kamayadi", "Aylanadi", "Oshadi", "O'zgarmaydi"),
     ("Nurota qo'riqxonasi qayerda?", "Navoiy viloyati", "Qoraqalpog'iston", "Toshkent", "Surxondaryo")],
    gallery=[('g5_oziq_zanjiri', "Oziq zanjiri", ("Rasmda ishlab chiqaruvchi qaysi?", "O'simlik", "O'txo'r", "Yirtqich", "Chirituvchi")),
             ('g5_energiya', "Energiya piramidasi", ("Piramidaning eng keng pog'onasi nimani bildiradi?", "Ishlab chiqaruvchilar (eng ko'p energiya)", "Yirtqichlar", "Chirituvchilar", "Odamlar"))],
    extra={'problems': [
        {'question': "O'simliklar 10 000 kJ energiya saqlaydi. 10 % qoidasi bo'yicha 2-tartibli iste'molchiga (o'simlik → o'txo'r → yirtqich) necha kJ o'tadi?", 'answer': '100', 'solution': "10 000 → 1000 → 100"},
        {'question': "Zanjir: o't → quyon → tulki → burgut. Burgutgacha necha bo'g'in (hammasi)?", 'answer': '4', 'solution': "4 ta bo'g'in"},
        {'question': "Ishlab chiqaruvchilar 5000 kJ energiya beradi. 1-tartibli iste'molchiga (10 %) necha kJ yetadi?", 'answer': '500', 'solution': "5000 · 0,1 = 500"}],
        'matching': [{'left': 'Ishlab chiqaruvchi', 'right': "Fotosintez qiluvchi o'simlik"}, {'left': "Iste'molchi", 'right': 'Tayyor organik moddani iste\'mol qiladi'}, {'left': 'Chirituvchi', 'right': 'Bakteriya va zamburug\'lar'}, {'left': '10 % qoidasi', 'right': 'Har bosqichda energiya kamayishi'}, {'left': 'Qizil kitob', 'right': 'Yo\'qolayotgan turlar'}, {'left': 'Biosfera', 'right': 'Hayot qobig\'i'}]}))

TOPICS.append(topic(19, 'g5b', "19-mavzu. Tuproq — qimmatli tabiiy boylik",
    ["Tuproq tarkibi va profilini bilish", "Unumdorlik va gumusning ahamiyatini tushuntirish", "Tuproq eroziyasi va muhofazasini bilish"],
    [("Tuproq nima?", "Tuproq — litosferaning yuqori unumdor qatlami. Uning asosiy xususiyati — unumdorlik, ya'ni o'simlikni oziq moddalar va suv bilan ta'minlash qobiliyati. Tuproq ona jinsning nurashi, o'simlik va hayvon qoldiqlari, iqlim, relyef va vaqt ta'sirida hosil bo'ladi. Tuproq hosil bo'lishi juda sekin: 1 sm qatlam yuzlab yillar davomida shakllanadi. Tuproq haqidagi fanning asoschisi — V. V. Dokuchayev.", 'g5_tuproq_tarkib', "Tuproq tarkibi"),
     ("Tuproq profili", "Tuproq kesimi gorizontlardan iborat: O (o'simlik qoldiqlari to'shamasi), A (gumusli — unumdor, to'q rangli), B (to'planish gorizonti), C (ona jins), R (tog' jinsi). Gumus — chirigan organik moddalar; uning miqdori unumdorlikni belgilaydi. Eng unumdor — chernozem (qora tuproq, gumus 10 % gacha, Ukraina, Rossiya dashtlari); kashtan tuproqlar kamroq (4 %); O'zbekiston bo'z tuproqlarida gumus 1–2 %, ammo sug'orish bilan yuqori hosil beradi.", 'g5_tuproq_profil', "Tuproq profili"),
     ("Gumus va unumdorlik", "Gumus tuproqqa to'q rang beradi, suvni ushlaydi, o'simlikka azot, fosfor, kaliy beradi. Gumusga boy tuproqlar zonalarda notekis: o'rmon-dashtda va dashtda ko'p, cho'lda kam. Tuproq unumdorligini oshirish usullari: o'g'itlash (organik va mineral), almashlab ekish, yerni sug'orish va zovurlash, shudgorlash.", 'g5_gumus', "Gumus miqdori"),
     ("Muhofaza va muammolar", "Tuproq eroziyasi (suv va shamol yuvib-uchirishi), sho'rlanish (sug'orishda tuz to'planishi), cho'llanish va ifloslanish (pestitsid, sanoat chiqindisi) — asosiy muammolar. O'zbekiston sug'oriladigan yerlarining katta qismi turli darajada sho'rlangan. Himoya choralari: daraxt-butazor polosalari, terrasalash, tomchilatib sug'orish, zovurlar. Tuproq — qayta tiklanmaydigan resurs, uni asrash har kimning burchi.")],
    ["Tuproq unumdorligi — o'simlikni oziq va suv bilan ta'minlash.", "Profil: O, A (gumus), B, C, R.", "Eng unumdor — chernozem (gumus ~10 %).", "Dokuchayev — tuproqshunoslik asoschisi.", "Muammolar: eroziya, sho'rlanish, cho'llanish, ifloslanish.", "Tuproq hosil bo'lishi juda sekin."],
    "Tuproq unumdor qatlam bo'lib, gumus miqdori va profili uni belgilaydi; eroziya va sho'rlanishdan asrash kerak.",
    [("Tuproqning asosiy xususiyati?", "Unumdorlik", "Rangi", "Og'irligi", "Narxi"), ("Eng unumdor tuproq?", "Chernozem", "Qumli", "Sho'rtob", "Podzol"), ("Gumusli gorizont qaysi?", "A", "C", "R", "B"),
     ("Tuproqshunoslik asoschisi?", "Dokuchayev", "Vernadskiy", "Darvin", "Gumbolt"), ("Sug'orishda tuzlar to'planishi nima deyiladi?", "Sho'rlanish", "Eroziya", "Nurash", "Muzlash"), ("Shamol va suv tuproqni yuvishi?", "Eroziya", "Sho'rlanish", "Nurash", "Cho'llanish")],
    [("Gumus nima?", "Chirigan organik moddalar", "Tosh", "Suv", "Havo"), ("Chernozemda gumus?", "~10 % gacha", "~0,1 %", "~50 %", "0 %"), ("O'zbekiston bo'z tuproqlarida gumus?", "~1–2 %", "~10 %", "~30 %", "0 %"), ("O gorizont nima?", "O'simlik qoldiqlari to'shamasi", "Tosh", "Gumusli qatlam", "Ona jins"),
     ("C gorizont nima?", "Ona jins", "Gumus", "To'shama", "Suv"), ("Tuproq hosil bo'lish tezligi?", "Juda sekin", "Tez", "Bir kunda", "Bir soatda"), ("Tuproq tarkibida eng ko'p?", "Mineral zarrachalar", "Gumus", "Suv", "Muz"), ("Zovur nima uchun?", "Ortiqcha suv va tuzni chiqarish", "Sug'orish", "Ekin ekish", "Yo'l"),
     ("Almashlab ekish nima?", "Ekinlarni navbat bilan ekish", "Bir ekin ekish", "Yerni tashlab qo'yish", "Faqat o'g'it"), ("Tomchilatib sug'orish afzalligi?", "Suvni tejaydi, sho'rlanishni kamaytiradi", "Suvni oshiradi", "Tuproqni quritadi", "Zararli"), ("Terrasa nima?", "Yonbag'irdagi zinapoyasimon dalalar", "Daryo", "Yo'l", "Ko'l"),
     ("Pestitsid nima?", "Zararkunandaga qarshi kimyoviy vosita", "Suv", "O'g'it", "Tuz"), ("Cho'llanish nima?", "Unumdor yerning cho'lga aylanishi", "Cho'lning ko'payishi tabiiy", "O'rmon", "Daryo"), ("Daraxt polosalari nima uchun?", "Shamol eroziyasidan himoya", "Bezak", "Suv uchun", "Yo'l"), ("Tuproq qayta tiklanadimi?", "Juda sekin, resurs sifatida cheklangan", "Bir yilda", "Tez", "Doim"),
     ("Tuproq rangi nimaga bog'liq?", "Gumus miqdoriga", "Faqat suvga", "Faqat quyoshga", "Faqat havoga")],
    gallery=[('g5_tuproq_profil', "Tuproq profili", ("Rasmda eng unumdor (gumusli) qatlam qaysi?", "A", "C", "R", "O faqat")),
             ('g5_gumus', "Gumus miqdori", ("Diagrammada eng yuqori gumusli tuproq?", "Qora tuproq (chernozem)", "Kashtan", "Bo'z", "Sahro"))],
    extra={'problems': [
        {'question': "Tuproqning 1 sm qatlami 300 yilda hosil bo'lsa, 30 sm qatlam necha yilda hosil bo'ladi?", 'answer': '9000', 'solution': "30 · 300 = 9000"},
        {'question': "Tuproq hajmining 45 % i mineral. 2000 sm³ tuproqda necha sm³ mineral zarracha?", 'answer': '900', 'solution': "2000 · 0,45 = 900"},
        {'question': "Chernozemda gumus 10 %. 500 kg tuproqda necha kg gumus?", 'answer': '50', 'solution': "500 · 0,1 = 50"}],
        'matching': [{'left': 'Gumus', 'right': 'Unumdorlik asosi'}, {'left': 'Eroziya', 'right': 'Tuproqni yuvib-uchirish'}, {'left': "Sho'rlanish", 'right': 'Tuz to\'planishi'}, {'left': 'Chernozem', 'right': 'Eng unumdor qora tuproq'}, {'left': 'Zovur', 'right': 'Ortiqcha suvni chiqaradi'}, {'left': 'Dokuchayev', 'right': 'Tuproqshunoslik asoschisi'}]}))

TOPICS.append(topic(20, 'g5c', "20-mavzu. Tabiat zonalari va balandlik mintaqalari",
    ["Asosiy tabiat zonalarini ketma-ket sanash", "Zonalarning iqlim, tuproq va jonivorlarini tavsiflash", "Tog'larda vertikal mintaqalilikni tushuntirish"],
    [("Tabiat zonasi", "Tabiat zonasi — iqlim, tuproq, o'simlik va hayvonot dunyosi o'xshash bo'lgan keng hudud. Zonalar asosan geografik kenglik bo'yicha almashadi (kenglik zonalligi), chunki Quyosh issiqligi va namlik kenglikka qarab o'zgaradi. Shimoliy yarimshardagi tekisliklarda shimoldan janubga: arktika cho'li, tundra, tayga, aralash va keng bargli o'rmonlar, dasht, cho'l, savanna, nam ekvatorial o'rmon.", 'g5_zonalar', "Tabiat zonalari"),
     ("Asosiy zonalar", "Tundra: sovuq, abadiy muzloq (mangu muz), moxlar, lishayniklar, shimol bug'usi. Tayga: ignabargli o'rmon (qarag'ay, qoraqarag'ay, qayin), podzol tuproq, bo'ri, ayiq, sincap. Dasht: o'tlar, qora tuproq, quyon, sug'ur, tulki. Cho'l: qurg'oqchil, saksovul, yantoq, qum va bo'z tuproq, sudralib yuruvchilar, tuya. Savanna: baland o'tlar va yakka daraxtlar (akatsiya), fil, jirafa, sher, zebra. Nam ekvatorial o'rmon: doim issiq va nam, ko'p qavatli, eng boy hayot (Amazonka, Kongo)."),
     ("Balandlik mintaqalari", "Tog'larda ham zonalar almashadi, lekin balandlik bo'yicha: har 1 km ko'tarilganda harorat ~6 °C pasayadi va yog'in o'zgaradi. Bu vertikal (balandlik) mintaqalilik. Tyan-Shan va Pomir-Oloyda quyidan yuqoriga: cho'l, adir (efemer o'simliklar), tog' o'rmon-butazor (archa, yong'oq), subalp va alp o'tloqlari, doimiy qor va muz. Mintaqalar soni tog' joylashgan kenglikka bog'liq: ekvator yaqinidagi tog'larda ko'p.", 'g5_vertikal', "Vertikal mintaqalilik"),
     ("Zonalarning inson hayoti bilan aloqasi", "Dasht va o'rmon-dashtlar qadimdan dehqonchilik markazi (buyuk g'alla zonalari), savanna va yarim cho'l chorvachilik, cho'llar — vohalar bo'ylab sug'orma dehqonchilik. Tayga — yog'och va qimmatbaho mo'yna manbai; tundra — bug'ichilik. Nam ekvatorial o'rmonlar «Yer o'pkasi» deb ataladi, ammo har yili millionlab gektar kesilmoqda. Zonalarni saqlash biologik xilma-xillik uchun zarur.")],
    ["Tabiat zonalari kenglik bo'yicha almashadi.", "Tartib: tundra → tayga → aralash o'rmon → dasht → cho'l → savanna → ekvatorial o'rmon.", "Cho'lda saksovul va yantoq o'sadi.", "Savannada fil, jirafa, sher yashaydi.", "Tog'larda zonalar balandlik bo'yicha almashadi.", "Nam ekvatorial o'rmon — eng boy hayot."],
    "Tabiat zonalari iqlim, tuproq va hayotning o'xshashligi bilan ajraladi; tog'larda ular balandlik bo'yicha almashadi.",
    [("Zonalar asosan nima bo'yicha almashadi?", "Geografik kenglik", "Faqat balandlik", "Yo'nalish", "Rang"), ("Abadiy muzloq qaysi zonada?", "Tundra", "Savanna", "Cho'l", "Dasht"), ("Eng boy hayot qaysi zonada?", "Nam ekvatorial o'rmon", "Cho'l", "Tundra", "Dasht"),
     ("Saksovul qaysi zonada?", "Cho'l", "Tayga", "Savanna", "Tundra"), ("Fil va jirafa qaysi zonada?", "Savanna", "Tundra", "Tayga", "Dasht"), ("Tog'larda mintaqalar nima bo'yicha?", "Balandlik", "Kenglik", "Uzunlik", "Daryo")],
    [("Tayga qanday o'rmon?", "Ignabargli", "Keng bargli", "Mangr", "Palma"), ("Tundra o'simligi?", "Moxlar va lishayniklar", "Palma", "Saksovul", "Emen"), ("Dasht tuprog'i?", "Qora tuproq (chernozem)", "Qum", "Sho'rtob", "Podzol"), ("Tayga tuprog'i?", "Podzol", "Chernozem", "Bo'z", "Qum"),
     ("Cho'l hayvoni?", "Tuya", "Shimol bug'usi", "Fil", "Ayiq"), ("Shimol bug'usi qayerda?", "Tundra", "Savanna", "Cho'l", "Dasht"), ("Bo'ri va ayiq qaysi zonada?", "Tayga", "Cho'l", "Savanna", "Tundra"), ("Akatsiya daraxti qaysi zonada?", "Savanna", "Tundra", "Tayga", "Dasht"),
     ("Amazonka qaysi zonada?", "Nam ekvatorial o'rmon", "Savanna", "Cho'l", "Dasht"), ("Yer o'pkasi deb nimaga aytiladi?", "Nam ekvatorial o'rmonlar", "Cho'l", "Tundra", "Okean"), ("Har 1 km ko'tarilganda harorat?", "~6 °C pasayadi", "6 °C ko'tariladi", "O'zgarmaydi", "60 °C pasayadi"),
     ("Adir qaysi mintaqa?", "Tog' etagidagi o'tloq-dasht", "Muz", "Archazor", "Cho'l"), ("Alp o'tloqlari qayerda?", "Tog'ning yuqori qismi", "Etagida", "Daryo bo'yida", "Cho'lda"), ("Dasht qayerda dehqonchilik?", "Buyuk g'alla zonasi", "Yo'q", "Faqat ov", "Faqat baliq"),
     ("Savanna iqlimi?", "Nam va quruq mavsum", "Doim nam", "Doim sovuq", "Doim quruq"), ("Cho'lda dehqonchilik qanday?", "Sug'orma, vohalarda", "Yomg'irli", "Muzli", "Yo'q"), ("Tog' o'rmonida nima o'sadi (O'zbekiston)?", "Archa, yong'oq", "Palma", "Mangr", "Kaktus")],
    gallery=[('g5_zonalar', "Tabiat zonalari", ("Rasmda eng shimoldagi (muzli) zona?", "Arktika cho'li", "Tayga", "Dasht", "Savanna")),
             ('g5_vertikal', "Vertikal mintaqalilik", ("Rasmda eng yuqoridagi mintaqa?", "Muz va qor", "Cho'l", "Adir", "O'rmon"))],
    extra={'problems': [
        {'question': "Tog' etagida harorat +24 °C. 3 km balandlikda (6 °C/km) harorat necha °C?", 'answer': '6', 'solution': "24 − 18 = 6"},
        {'question': "Tog' etagida +18 °C, qor chizig'ida 0 °C. Qor chizig'i necha km balandlikda (6 °C/km)?", 'answer': '3', 'solution': "18 : 6 = 3"}],
        'matching': [{'left': 'Tundra', 'right': "Moxlar va muzloq"}, {'left': 'Tayga', 'right': 'Ignabargli o\'rmon'}, {'left': 'Dasht', 'right': "O'tlar va qora tuproq"}, {'left': "Cho'l", 'right': 'Saksovul, yantoq'}, {'left': 'Savanna', 'right': "Baland o'tlar, fil"}, {'left': 'Ekvatorial o\'rmon', 'right': 'Eng boy hayot'}]}))
