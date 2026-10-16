# -*- coding: utf-8 -*-
from dsl import topic
from svglib import *

IMAGES = {}
TOPICS = []

IMAGES.update({
    'g9_co2': linechart("Atmosferada CO₂ miqdori (ppm)", ['1960', '1980', '2000', '2010', '2023'], [317, 339, 369, 390, 421], 'Yil', 'CO₂ (ppm)', labels=[(0, '317'), (4, '421')], color='#dc2626'),
    'g9_harorat': linechart("Yer o'rtacha haroratining o'zgarishi (°C, 1951–1980 ga nisbatan)", ['1900', '1950', '1980', '2000', '2023'], [-0.3, 0.0, 0.25, 0.4, 1.2], 'Yil', '°C', labels=[(4, '+1,2 °C')], color='#ea580c'),
    'g9_muammolar': flow("Global muammolar", [('Ekologik', 'isish, ifloslanish, o\'rmon yo\'qolishi'), ('Demografik', 'aholi o\'sishi va qarish'), ('Ijtimoiy', 'ochlik, kambag\'allik, kasallik'), ('Xavfsizlik', 'urush, terrorizm')], note="Global muammolarni faqat hamkorlikda hal qilish mumkin"),
    'g9_chiqindi': bars("Plastik chiqindining parchalanish muddati (yil)", [('Qog\'oz', 1), ('Alyuminiy banka', 200), ('Plastik butilka', 450), ('Shisha', 1000)], 'yil'),
    'g9_orol_suv': pie("Chuchuk suv taqsimoti (taxminan)", [('Muzliklar', 69), ('Yer osti suvi', 30), ('Daryo, ko\'l va boshqa', 1)]),
    'g9_energiya': pie("O'zbekistonda elektr ishlab chiqarish (taxminan)", [('Tabiiy gaz', 80), ('Gidro (GES)', 8), ('Quyosh va shamol', 6), ('Boshqa', 6)]),
})

TOPICS.append(topic(38, 'g9a', "38-mavzu. Global muammolar va iqlim o'zgarishi",
    ["Global muammolarni sanash", "Global isish sabablarini tushuntirish", "Iqlim o'zgarishiga qarshi choralarni bilish"],
    [("Global muammolar nima?", "Global muammolar — butun insoniyatga tegishli va faqat davlatlarning hamkorligida hal etiladigan masalalar: ekologik (iqlim o'zgarishi, ifloslanish, o'rmonlar va biologik xilma-xillikning kamayishi), demografik, oziq-ovqat va ochlik, kambag'allik, kasalliklar (pandemiyalar), xavfsizlik va tinchlik. Ular bir-biri bilan bog'liq: masalan, qurg'oqchilik ochlik va migratsiyani kuchaytiradi.", 'g9_muammolar', "Global muammolar guruhlari"),
     ("Global isish", "Yer atmosferasida karbonat angidrid (CO₂), metan kabi issiqxona gazlari issiqlikni ushlab turadi (issiqxona effekti). Sanoat inqilobidan beri ko'mir, neft, gaz yoqilishi, o'rmonlar kesilishi tufayli CO₂ miqdori ~280 ppm dan ~421 ppm gacha oshdi, Yer o'rtacha harorati ~1,2 °C ko'tarildi. Oqibatlari: muzliklar erishi, dengiz sathining ko'tarilishi, qurg'oqchilik va toshqin, issiq to'lqinlari, ekotizimlarning buzilishi.", 'g9_co2', "CO₂ miqdori"),
     ("Boshqa ekologik muammolar", "Havo ifloslanishi (zavod va transport tutuni, kislotali yomg'ir), suv ifloslanishi, tuproq eroziyasi va sho'rlanishi, cho'llashish, o'rmonlarning kesilishi, plastik chiqindilar (dengizlarda «chiqindi orollari»), ozon qatlamining yupqalashishi (freonlar tufayli, Monreal protokoli bilan to'xtatilgan). Orol dengizi — mintaqaviy ekologik falokat namunasi.", 'g9_chiqindi', "Chiqindi parchalanish muddati"),
     ("Yechimlar", "Parij kelishuvi (2015): global isishni 2 °C dan, imkon bo'lsa 1,5 °C dan oshirmaslik. Choralar: qayta tiklanadigan energiya (quyosh, shamol), energiyani tejash, jamoat transporti va elektromobil, o'rmon ekish, chiqindini saralash va qayta ishlash, suvni tejash. Har bir inson tabiatni asrashga hissa qo'shadi: elektrni o'chirish, plastikni kamaytirish, daraxt ekish. O'zbekiston «Yashil makon» dasturi doirasida ko'p million daraxt ekmoqda.", 'g9_harorat', "Harorat o'zgarishi")],
    ["Global muammolarni davlatlar hamkorlikda hal qiladi.", "Issiqxona gazlari: CO₂, metan.", "Yer harorati ~1,2 °C ga ko'tarilgan.", "Parij kelishuvi — isishni 1,5–2 °C da cheklash.", "Ozon qatlamini freonlar yupqalashtirgan.", "«Yashil makon» — daraxt ekish dasturi."],
    "Global isish va ifloslanish insoniyatning umumiy muammosi; yechim — hamkorlik, toza energiya va har kimning mas'uliyati.",
    [("Asosiy issiqxona gazi?", "CO₂", "O₂", "N₂", "Ar"), ("Global isish natijasi?", "Muzliklar erishi", "Muzliklar ko'payishi", "Dengiz kamayishi", "Yomg'ir to'xtashi"), ("Parij kelishuvi qaysi yilda?", "2015", "1815", "1915", "2115"),
     ("Ozon qatlamini nima yupqalashtirgan?", "Freonlar", "Kislorod", "Suv", "Azot"), ("Qaysi muammo global?", "Iqlim o'zgarishi", "Bir mahalladagi tirbandlik", "Kichik ko'l", "Bir daraxt"), ("«Yashil makon» nima?", "Daraxt ekish dasturi", "Zavod", "Yo'l", "Bank")],
    [("CO₂ miqdori hozir?", "~421 ppm", "~42 ppm", "~4210 ppm", "~4 ppm"), ("Harorat qanchaga ko'tarilgan?", "~1,2 °C", "~12 °C", "~0,01 °C", "~30 °C"), ("Issiqxona effekti nima?", "Gazlar issiqlikni ushlab turishi", "Sovish", "Yomg'ir", "Shamol"), ("Dengiz sathi nega ko'tariladi?", "Muzliklar erishi", "Zilzila", "Vulqon", "Oy"),
     ("Qaysi energiya toza?", "Quyosh", "Ko'mir", "Neft", "Gaz"), ("Plastik butilka parchalanishi?", "~450 yil", "~1 yil", "~1 kun", "~1 oy"), ("Cho'llashish nima?", "Yerning cho'lga aylanishi", "Cho'l o'rmonga", "Dengiz hosil", "Tog' o'sishi"), ("Kislotali yomg'ir sababi?", "Sanoat gazlari", "Oy", "Shamol", "Tuz"),
     ("Chiqindini saralash nima uchun?", "Qayta ishlash uchun", "Yoqish uchun", "Ko'mish uchun", "Hech nima"), ("Elektromobil afzalligi?", "Tutun chiqarmaydi", "Ko'p tutun", "Ko'p chang", "Hech nima"), ("Monreal protokoli nimaga?", "Ozon qatlamini asrash", "Savdo", "Urush", "Sport"), ("Metan nima?", "Issiqxona gazi", "Suv", "Tosh", "Metall"),
     ("O'rmon kesilishi natijasi?", "CO₂ ko'payishi", "Havo tozaligi", "Yomg'ir ko'payishi", "Hech nima"), ("Eng yaxshi shaxsiy hissa?", "Tejamkorlik, daraxt ekish", "Isrofgarchilik", "Chiqindi tashlash", "Hech nima"), ("Sanoat inqilobidan keyin CO₂ ...", "Oshdi", "Kamaydi", "O'zgarmadi", "Yo'qoldi")],
    gallery=[('g9_co2', "CO₂ o'sishi", ("1960-yilda CO₂ taxminan?", "317 ppm", "421 ppm", "280 ppm", "500 ppm")),
             ('g9_chiqindi', "Chiqindi", ("Diagrammada eng tez parchalanadigan?", "Qog'oz", "Shisha", "Plastik", "Alyuminiy")),
             ('g9_harorat', "Harorat", ("2023-yilda harorat qancha ko'tarilgan?", "+1,2 °C", "+0,4 °C", "+5 °C", "−0,3 °C"))],
    extra={'problems': [
        {'question': "CO₂ 317 ppm dan 421 ppm ga oshdi. Necha ppm ortgan?", 'answer': '104', 'solution': "421 − 317"},
        {'question': "Har bir inson yiliga 1 daraxt ekadi. 36 mln kishi necha mln daraxt ekadi?", 'answer': '36', 'solution': "36 · 1"}],
        'matching': [{'left': 'CO₂', 'right': 'Issiqxona gazi'}, {'left': 'Freon', 'right': 'Ozon qatlamini buzadi'}, {'left': 'Parij kelishuvi', 'right': 'Isishni cheklash'}, {'left': 'Quyosh energiyasi', 'right': 'Toza energiya'}, {'left': 'Cho\'llashish', 'right': 'Yer degradatsiyasi'}, {'left': 'Yashil makon', 'right': 'Daraxt ekish'}]}))

TOPICS.append(topic(39, 'g9b', "39-mavzu. Suv, oziq-ovqat va barqaror rivojlanish",
    ["Chuchuk suv taqchilligini tushuntirish", "Oziq-ovqat xavfsizligini bilish", "Barqaror rivojlanish maqsadlarini sanash"],
    [("Chuchuk suv taqchilligi", "Yer suvining 97 % i sho'r okean suvi, chuchuk suv atigi ~3 %; uning ~69 % i muzliklarda, ~30 % i yer ostida, daryo va ko'llarda 1 % ga yaqin. Dunyoda ~2 mlrd kishi toza ichimlik suvidan yetarlicha foydalana olmaydi. Qishloq xo'jaligi suvning ~70 % ini sarflaydi. Markaziy Osiyoda suv taqchilligi ayniqsa dolzarb: Amudaryo va Sirdaryo suvini davlatlar birgalikda boshqaradi.", 'g9_orol_suv', "Chuchuk suv taqsimoti"),
     ("Oziq-ovqat xavfsizligi", "Dunyoda ~700–800 mln kishi surunkali ochlikdan aziyat chekadi, asosan Afrika va Janubiy Osiyoda. Sabablar: kambag'allik, urushlar, qurg'oqchilik, taqsimot muammolari; shu bilan birga ishlab chiqarilgan oziqning ~1/3 qismi isrof bo'ladi. Yechim: sug'orish texnologiyalari, hosildor navlar, oziqni isrof qilmaslik, adolatli savdo."),
     ("Barqaror rivojlanish", "Barqaror rivojlanish — kelajak avlodlar imkoniyatini kamaytirmasdan hozirgi ehtiyojlarni qondirish. BMT 2015-yilda 2030-yilgacha 17 ta Barqaror Rivojlanish Maqsadini (BRM) qabul qilgan: kambag'allik va ochlikka barham berish, sifatli ta'lim, toza suv, arzon va toza energiya, iqlim choralari, tinchlik va hamkorlik va boshqalar. O'zbekiston ham BRMni milliy strategiyasiga kiritgan."),
     ("Energiya va O'zbekiston", "O'zbekistonda elektr energiyasining katta qismi hali gazdan olinadi, ammo quyosh va shamol stansiyalari (Navoiy, Buxoro, Qoraqalpog'iston) tez qurilmoqda, 2030-yilga qadar qayta tiklanadigan energiya ulushini ~40 % ga yetkazish rejalashtirilgan. Suvni tejash, tomchilatib sug'orish, chiqindini qayta ishlash va yashil hududlarni ko'paytirish — milliy ustuvor vazifalar.", 'g9_energiya', "Elektr ishlab chiqarish")],
    ["Chuchuk suv ~3 %.", "~2 mlrd kishi toza suvdan mahrum.", "Oziq-ovqatning 1/3 qismi isrof bo'ladi.", "BMT: 17 ta Barqaror Rivojlanish Maqsadi (2030).", "Barqaror rivojlanish — kelajakni ham o'ylash.", "O'zbekiston qayta tiklanadigan energiyani ko'paytirmoqda."],
    "Suv, oziq-ovqat va energiya o'zaro bog'liq; barqaror rivojlanish kelajak avlodlar manfaatini himoya qiladi.",
    [("Chuchuk suv ulushi?", "~3 %", "~30 %", "~97 %", "~60 %"), ("BRM nechta?", "17", "7", "70", "170"), ("Qishloq xo'jaligi suvning qancha qismini sarflaydi?", "~70 %", "~7 %", "~1 %", "~99 %"),
     ("Chuchuk suvning ko'pi qayerda?", "Muzliklarda", "Daryolarda", "Atmosferada", "Ko'llarda"), ("Barqaror rivojlanish nima?", "Kelajak avlod manfaatini ham hisobga olish", "Faqat bugun foyda", "Faqat urush", "Hech nima"), ("BRM qaysi yilgacha?", "2030", "2010", "2300", "2100")],
    [("Ochlik asosan qayerda ko'p?", "Afrika va Janubiy Osiyo", "Yevropa", "Avstraliya", "Yaponiya"), ("Oziqning qancha qismi isrof?", "~1/3", "~1/100", "~3/4", "~0"), ("Qaysi BRM suvga oid?", "Toza suv va sanitariya", "Arzon tolalar", "Kosmos", "Sport"), ("Suv tejash usuli?", "Tomchilatib sug'orish", "Ariqlarni ochiq qoldirish", "Suvni to'kish", "Hech nima"),
     ("Qayta tiklanadigan energiya maqsadi 2030?", "~40 %", "~4 %", "~100 %", "0 %"), ("Quyosh stansiyasi qayerda?", "Navoiy", "Antarktida", "Okean tubi", "Everest"), ("Amudaryo suvini kim boshqaradi?", "Davlatlar birgalikda", "Faqat bitta", "Hech kim", "Okean"), ("Qaysi sabab ochlikka olib keladi?", "Urush va qurg'oqchilik", "Yomg'ir bayrami", "Tinchlik", "Ko'p hosil"),
     ("Toza ichimlik suvidan mahrum?", "~2 mlrd kishi", "~2 ming", "~2 mln", "Hech kim"), ("Okean suvi qanday?", "Sho'r", "Chuchuk", "Distillangan", "Shirin"), ("BMT qachon BRM qabul qildi?", "2015", "1945", "1990", "2030"), ("Hosildor navlar nima uchun?", "Oziq-ovqat ko'paytirish", "Ochlik ko'paytirish", "Suv ifloslash", "Hech nima"),
     ("Yashil hududlar nima beradi?", "Toza havo", "Ifloslanish", "Chang", "Shovqin"), ("Isrofgarchilikni kamaytirish?", "Oziq va suvni tejash", "Ko'p tashlash", "Ko'p ishlab chiqarish", "Yo'q"), ("Barqaror rivojlanish kimga tegishli?", "Hammaga", "Faqat boylarga", "Faqat bir davlatga", "Hech kimga")],
    gallery=[('g9_orol_suv', "Chuchuk suv", ("Chuchuk suvning eng katta qismi?", "Muzliklar", "Daryolar", "Yer osti", "Ko'llar")),
             ('g9_energiya', "Elektr ishlab chiqarish", ("Diagrammada asosiy manba?", "Tabiiy gaz", "Gidro", "Quyosh", "Boshqa")),
             ('g9_muammolar', "Global muammolar", ("Ochlik qaysi guruhga kiradi?", "Ijtimoiy", "Ekologik", "Demografik", "Xavfsizlik"))],
    extra={'problems': [
        {'question': "Dunyoda 100 litr suvning 3 litri chuchuk. Chuchuk suv necha foiz?", 'answer': '3', 'solution': "3 : 100 · 100"},
        {'question': "1000 tonna oziqning 1/3 qismi isrof. Necha tonna (butungacha) isrof?", 'answer': '333', 'solution': "1000 : 3 ≈ 333"},
        {'question': "17 BRM dan 6 tasi bajarildi. Necha tasi qoldi?", 'answer': '11', 'solution': "17 − 6"}],
        'matching': [{'left': 'BRM', 'right': 'Barqaror Rivojlanish Maqsadlari'}, {'left': 'Chuchuk suv', 'right': '~3 %'}, {'left': 'Tomchilatib sug\'orish', 'right': 'Suvni tejash'}, {'left': 'Quyosh stansiyasi', 'right': 'Toza energiya'}, {'left': 'Oziq isrofi', 'right': '~1/3'}, {'left': 'BMT', 'right': 'Xalqaro tashkilot'}]}))
