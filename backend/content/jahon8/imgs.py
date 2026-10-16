# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from tarix_svg import *

I = {}
add = adder('j8', I)

add('j01', 'Fransiya markazlashuvi', [('987', 'Kapetinglar sulolasi boshlandi'), ('1180-1223', 'Filipp II Avgust'), ('1302', 'Birinchi General shtatlar'), ('1356', 'Etyen Marsel islohoti'), ('1328', 'Valua sulolasi')],
    'shtat', 'General shtatlar tarkibi', tree('General shtatlar', 'General shtatlar', [('I toifa', 'Ruhoniylar'), ('II toifa', 'Zodagonlar'), ('III toifa', 'Shaharliklar va boshqa aholi')]))
add('j02', 'Yuz yillik urush', [('1337', 'Urush boshlandi'), ('1346', 'Kresi jangi'), ('1356', 'Puatye jangi'), ('1429', 'Orlean qamali, Janna d\'Ark'), ('1453', 'Urush tugadi')],
    'sabab', 'Yuz yillik urush sabablari va natijalari', compare('Yuz yillik urush', 'Sabablar', ['Angliyaning Fransiyadagi yerlari', 'Fransiya taxti uchun da\'vo', 'Flandriya savdosi uchun kurash'], 'Natijalar', ['Angliya deyarli hamma yerni yo\'qotdi', 'Fransiya birlashdi', 'Doimiy armiya paydo bo\'ldi']))
add('j03', 'Fransiyaning birlashishi', [('1453', 'Yuz yillik urush tugadi'), ('1461-1483', 'Lyudovik XI davri'), ('1477', 'Burgundiya olindi'), ('1491', 'Bretan qo\'shildi'), ('1494', 'Italiya urushlari boshlandi')],
    'yol', 'Mamlakatni birlashtirish yo\'li', flow('Birlashish yo\'li', [('Urush tugadi', '1453'), ('Yerlar qaytdi', 'Burgundiya'), ('Armiya', 'doimiy'), ('Soliq', 'qirol soliqlari'), ('Markazlashuv', 'mutlaqiyat sari')]))
add('j04', 'Angliyada markazlashuv', [('1066', 'Normanlar fathi'), ('1154', 'Plantagenetlar'), ('1215', 'Buyuk erkinlik xartiyasi'), ('1265', 'Parlament tarkibi kengaydi'), ('1295', 'Namunaviy parlament')],
    'parl', 'Parlament palatalari', compare('Parlament', 'Lordlar palatasi', ['Yirik zodagonlar', 'Yuqori ruhoniylar', 'Irsiy a\'zolik'], 'Jamoalar palatasi', ['Ritsarlar', 'Shahar vakillari', 'Soliqlarni tasdiqlash']))
add('j05', 'XIV-XV asrlarda Angliya', [('1348', 'Vabo epidemiyasi'), ('1381', 'Uot Tayler qo\'zg\'oloni'), ('1337-1453', 'Yuz yillik urush'), ('1455-1485', 'Qizil va Oq atirgullar urushi'), ('1485', 'Tyudorlar sulolasi')],
    'atirgul', 'Qizil va Oq atirgullar urushi', compare('Atirgullar urushi', 'Lankasterlar', ['Gerbi: qizil atirgul', 'Taxtga da\'vogar'], 'Yorklar', ['Gerbi: oq atirgul', 'Taxtga da\'vogar', '1485: Tyudorlar g\'olib']))
add('j06', 'Germaniya', [('1356', 'Oltin bulla'), ('1438', 'Gabsburglar imperator'), ('1495', 'Vorms rayxstagi'), ('XIV asr', 'Gansa gullagan'), ('XV asr', 'Gutenberg bosmaxonasi')],
    'imp', 'Germaniya siyosiy bo\'linishi', tree('Germaniya', 'Muqaddas Rim imperiyasi', [('Imperator', 'Nomigagina markaziy hokimiyat'), ('Knyazliklar', 'Deyarli mustaqil hukmdorlar'), ('Erkin shaharlar', 'Gansa va savdo markazlari')]))
add('j07', 'Italiya', [('XI asr', 'Shahar-respublikalar'), ('XII asr', 'Venetsiya, Genuya gullagan'), ('XIII asr', 'Florensiya to\'qimachiligi'), ('XV asr', 'Medicilar hukmronligi'), ('1494', 'Italiya urushlari')],
    'shahar', 'Italiyaning yirik shahar-davlatlari', tree('Shahar-davlatlar', 'Italiya', [('Venetsiya', 'Dengiz savdosi'), ('Genuya', 'Qora dengiz savdosi'), ('Florensiya', 'To\'qimachilik, banklar'), ('Papa davlati', 'Markaziy Italiya')]))
add('j08', 'Pireney yarimoroli', [('711', 'Arablar Ispaniyada'), ('1085', 'Toledo qaytarildi'), ('1212', 'Las-Navas-de-Tolosa'), ('1469', 'Izabella va Ferdinand nikohi'), ('1492', 'Granada qulashi')],
    'reko', 'Rekonkista bosqichlari', flow('Rekonkista', [('711', 'Arab fathi'), ('XI asr', 'Toledo'), ('1212', 'Las-Navas'), ('XIII asr', 'Kordova, Sevilya'), ('1492', 'Granada')]))
add('j09', 'Rus knyazliklari', [('XII asr', 'Kiyev Rusi tarqoqligi'), ('1240', 'Mo\'g\'ullar Kiyevni oldi'), ('1242', 'Muz ustidagi jang'), ('1380', 'Kulikovo jangi'), ('1480', 'Mo\'g\'ul boshqaruvining oxiri')],
    'yer', 'Rus yerlari', tree('Rus knyazliklari', 'Tarqoq Rus', [('Novgorod', 'Boyar respublikasi'), ('Vladimir-Suzdal', 'Moskva ko\'tarilishi'), ('Galisiya-Volin', 'Janubi-g\'arbiy yerlar')]))
add('j10', 'Bolqon va Sharqiy Yevropa', [('1018', 'Vizantiya Bolgariyani oldi'), ('1389', 'Kosovo jangi'), ('1410', 'Grunvald jangi'), ('1444', 'Varna jangi'), ('1453', 'Usmonlilar Konstantinopolda')],
    'jang', 'Usmonlilarga qarshi kurash', flow('Qarshilik', [('Kosovo', '1389'), ('Nikopol', '1396'), ('Varna', '1444'), ('Konstantinopol', '1453'), ('Bolqon', 'bo\'ysundi')]))
add('j11', 'Usmoniy sultonligi', [('1299', 'Usmon asos soldi'), ('1389', 'Kosovo jangi'), ('1453', 'Konstantinopol olindi'), ('1517', 'Misr olindi'), ('1520-1566', 'Sulaymon Qonuniy')],
    'qit', 'Uch qit\'a', tree('Usmoniy sultonligi', 'Uch qit\'a', [('Yevropa', 'Bolqon, Vengriya'), ('Osiyo', 'Anatoliya, Suriya, Iroq'), ('Afrika', 'Misr, Shimoliy Afrika')]))
add('j12', 'Eron', [('XI asr', 'Saljuqiylar hukmronligi'), ('1219-1221', 'Mo\'g\'ullar fathi'), ('1256', 'Elxonlar davlati'), ('1370-1405', 'Amir Temur yurishlari'), ('1501', 'Safaviylar davlati')],
    'ada', 'Eron adabiyoti', tree('Eron madaniyati', 'Fors adabiyoti', [('Firdavsiy', '"Shohnoma"'), ('Umar Xayyom', 'Ruboiylar, astronomiya'), ('Sa\'diy', '"Guliston", "Bo\'ston"'), ('Hofiz', 'G\'azallar')]))
add('j13', 'Oltin O\'rda', [('1243', 'Botuxon Saroyda'), ('1313-1341', 'O\'zbekxon, islom'), ('1380', 'Kulikovo jangi'), ('1391', 'To\'xtamish va Temur'), ('1502', 'Oltin O\'rda tugadi')],
    'tuzum', 'Oltin O\'rda hokimiyat tuzilmasi', layers('Oltin O\'rda', [('Xon', 'oliy hokim', '#a78bfa', 1), ('Beklarbek, noyonlar', 'mahalliy hukmdorlar', '#f87171', 1.1), ('Askarlar, dehqonlar', 'soliq to\'lovchilar', '#fbbf24', 1.2)]))
add('j14', 'Hindiston', [('1206', 'Dehli sultonligi'), ('1336', 'Vijayanagar'), ('1398', 'Amir Temur Dehlida'), ('1451', 'Lodiylar'), ('1526', 'Boburiylar')],
    'din', 'Hindistondagi dinlar', tree('Dinlar', 'Hindiston', [('Hinduizm', 'Ko\'pchilik aholi'), ('Islom', 'Dehli sultonligi hukmdorlari'), ('Buddizm', 'Ta\'siri susaydi')]))
add('j15', 'Xitoy', [('960', 'Sun sulolasi'), ('1271', 'Yuan sulolasi'), ('1368', 'Min sulolasi'), ('1405-1433', 'Chjen He dengiz yurishlari'), ('XV asr', 'Buyuk Xitoy devori qayta qurildi')],
    'sul', 'Xitoy sulolalari', flow('Sulolalar', [('Sun', '960-1279'), ('Yuan', '1271-1368'), ('Min', '1368-1644'), ('Chjen He', '1405-1433'), ('Devor', 'mustahkamlandi')]))
add('j16', 'Yaponiya va Koreya', [('794', 'Xeyan davri'), ('1192', 'Kamakura syogunligi'), ('1392', 'Choson sulolasi'), ('1443', 'Xangul'), ('1603', 'Tokugava syogunligi')],
    'jam', 'Yaponiya va Koreya', compare('Taqqoslash', 'Yaponiya', ['Syogunlar hokimiyati', 'Samuraylar', 'Sintoizm va buddizm'], 'Koreya', ['Choson sulolasi', 'Konfutsiychilik', 'Xangul yozuvi (1443)']))
add('j17', 'Afrika', [('IV asr', 'Aksum davlati'), ('VII asr', 'Gana imperiyasi'), ('XIII asr', 'Mali imperiyasi'), ('1324', 'Mansa Muso haji'), ('XV asr', 'Songxay imperiyasi')],
    'davlat', 'G\'arbiy Afrika davlatlari', flow('Sudan davlatlari', [('Gana', 'oltin savdosi'), ('Mali', 'Mansa Muso'), ('Songxay', 'Timbuktu'), ('Savdo', 'sahro karvonlari'), ('Islom', 'tarqaldi')]))
add('j18', 'Amerika xalqlari', [('VII asr', 'Mayya gullagan'), ('1325', 'Tenochtitlan'), ('1438', 'Inklar kengayishi'), ('1492', 'Kolumb'), ('1519', 'Kortes Meksikada')],
    'xalq', 'Uch tsivilizatsiya', tree('Amerika', 'Hind tsivilizatsiyalari', [('Mayya', 'Ierogliflar, taqvim'), ('Asteklar', 'Tenochtitlan'), ('Inklar', 'Kusko, yo\'llar')]))
add('j19', 'Kundalik hayot', [('V-X asrlar', 'Qishloq hayoti'), ('XI asr', 'Uch dala tizimi'), ('XII asr', 'Shaharlar o\'sishi'), ('XIV asr', 'Vabo epidemiyasi'), ('XV asr', 'Savdo kengayishi')],
    'sinf', 'O\'rta asr jamiyati', layers('O\'rta asr jamiyati', [('Ruhoniylar', 'cherkov', '#a78bfa', 1), ('Zodagonlar', 'feodallar', '#f87171', 1), ('Shaharliklar', 'hunarmand, savdogar', '#fbbf24', 1), ('Dehqonlar', 'eng ko\'p aholi', '#34d399', 1.3)]))
add('j20', 'Yevropa iqtisodiyoti', [('XI asr', 'Uch dala tizimi'), ('XII asr', 'Yarmarkalar'), ('XIII asr', 'Sexlar'), ('XIV asr', 'Bank ishi'), ('XV asr', 'Manufaktura boshlandi')],
    'hunar', 'Sexdan manufakturagacha', flow('Ishlab chiqarish', [('Hunarmand', 'yakka'), ('Sex', 'tartib-qoida'), ('Savdo', 'yarmarka'), ('Bank', 'qarz'), ('Manufaktura', 'ish taqsimoti')]))
add('j21', 'Boshqa qit\'alar iqtisodi', [('XI asr', 'Sahro savdosi'), ('XIII asr', 'Ipak yo\'li'), ('XIV asr', 'Hind okeani savdosi'), ('XV asr', 'Xitoy bosma pullari'), ('XV asr', 'Inklar yo\'l tarmog\'i')],
    'yo', 'Asosiy savdo yo\'llari', tree('Savdo yo\'llari', 'Qadimgi savdo', [('Ipak yo\'li', 'Xitoy - O\'rta yer dengizi'), ('Sahro yo\'li', 'Afrika - Shimol'), ('Hind okeani', 'Dengiz savdosi')]))
add('j22', 'Yevropada ilm-fan', [('1088', 'Boloniya universiteti'), ('XII asr', 'Parij universiteti'), ('XIII asr', 'Oksford, Kembrij'), ('XIII asr', 'Tomas Akvinskiy'), ('1450', 'Gutenberg bosmaxonasi')],
    'fan', 'Universitet fakultetlari', tree('Universitet', 'O\'rta asr universiteti', [('Artes', 'Dastlabki fakultet'), ('Huquq', 'Qonunshunoslik'), ('Tibbiyot', 'Davolash'), ('Ilohiyot', 'Eng obro\'li')]))
add('j23', 'Me\'morchilik va san\'at', [('XI asr', 'Roman uslubi'), ('XII asr', 'Gotika uslubi'), ('XIII asr', 'Notr-Dam qurilishi'), ('XIV asr', 'Vitrajlar'), ('XV asr', 'Ilk Uyg\'onish')],
    'uslub', 'Roman va gotika', compare('Uslublar', 'Roman', ['Yarim doira ravoq', 'Qalin devor', 'Kichik oynalar'], 'Gotika', ['Uchli ravoq', 'Baland minora', 'Vitraj oynalar']))
add('j24', 'Ilk Uyg\'onish', [('XIV asr', 'Petrarka, Dante'), ('1348', 'Bokkachcho "Dekameron"'), ('XV asr', 'Medicilar homiyligi'), ('1450', 'Bosmaxona'), ('XV asr', 'Gumanizm')],
    'ijod', 'Ilk Uyg\'onish ijodkorlari', tree('Uyg\'onish', 'Ilk Uyg\'onish', [('Dante', '"Ilohiy komediya"'), ('Petrarka', 'Sonetlar'), ('Giotto', 'Rassomlikda yangilik')]))
add('j25', 'Boshqa qit\'alar madaniyati', [('IX asr', 'Bag\'dod "Bilimlar uyi"'), ('XI asr', 'Beruniy, Ibn Sino'), ('XIII asr', 'Marko Polo sayohati'), ('XV asr', 'Ulug\'bek rasadxonasi'), ('XV asr', 'Maya taqvimi')],
    'ilm', 'Sharq ilm-fani', tree('Sharq fani', 'Olimlar', [('Al-Xorazmiy', 'Algebra'), ('Beruniy', 'Astronomiya'), ('Ibn Sino', 'Tibbiyot'), ('Ulug\'bek', 'Rasadxona')]))

inject('jahon8', I)
