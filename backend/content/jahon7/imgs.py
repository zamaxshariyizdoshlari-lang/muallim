# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from tarix_svg import *

I = {}


def add(k, tl, tle, f2, t2, s2):
    I[k] = [(f'j7_{k}_vaqt', tl + ': vaqt chizig\'i', timeline(tl, tle)), (f'j7_{k}_{f2}', t2, s2)]


add('m01', 'German qabilalari va Rim', [('I-IV asrlar', 'Germanlar Reyn va Elba oralig\'ida'), ('375', 'Xunnlar hujumi boshlandi'), ('395', 'Rim ikkiga bo\'lindi'), ('410', 'Alarix Rimni egalladi'), ('476', 'Odoakr so\'nggi imperatorni ag\'dardi')],
    'sabab', 'Rim imperiyasi inqirozi sabablari', tree('Rim imperiyasi inqirozi', 'Rim inqirozi', [('Iqtisod', 'Qullar mehnati samarasiz, soliqlar og\'ir'), ('Siyosat', 'Imperatorlar tez-tez almashdi, 395-yilda bo\'linish'), ('Tashqi xavf', 'Xunnlar bosimi, german qabilalari bostirib kirdi')]))
add('m02_03', 'Franklar davlati', [('481-511', 'Xlodvig franklarni birlashtirdi'), ('496', 'Xlodvig xristianlikni qabul qildi'), ('732', 'Karl Martell Puatye jangida'), ('751', 'Pipin Kichik qirol bo\'ldi'), ('800', 'Karl Buyuk imperator deb e\'lon qilindi'), ('843', 'Verden shartnomasi')],
    'tuzum', 'Franklar davlati: qirollikdan imperiyaga', flow('Qirollikdan imperiyaga', [('Merovinglar', 'Xlodvig'), ('Mayordomlar', 'Karl Martell'), ('Karolinglar', 'Pipin Kichik'), ('Imperiya', 'Karl Buyuk'), ('Bo\'linish', 'Verden, 843')]))
add('m04', 'Angliya tarixi', [('V asr', 'Anglosakslar Britaniyaga kela boshladi'), ('VII asr', 'Yetti qirollik davri'), ('829', 'Angliya Ueseks atrofida birlashdi'), ('1066', 'Gastings jangi'), ('1215', 'Buyuk erkinlik xartiyasi')],
    'tuzum', 'Angliyada davlat tuzumi', flow('Angliya: qirollikdan parlamentga', [('Anglosaksonlar', 'yetti qirollik'), ('Norman fathi', '1066-yil'), ('Qirol hokimiyati', 'kuchaydi'), ('Xartiya', '1215-yil'), ('Parlament', 'XIII asr')]))
add('m05', 'Muqaddas Rim imperiyasi', [('843', 'Franklar davlati bo\'linishi'), ('919', 'Genrix I Saksoniya qiroli'), ('962', 'Otton I imperator toji'), ('1075', 'Investitura uchun kurash'), ('1122', 'Vorms konkordati')],
    'kuch', 'Imperator va papa kurashi', compare('Imperator va papa', 'Imperator', ['Dunyoviy hokimiyat boshlig\'i', 'Episkoplarni tayinlashni xohladi', 'Otton I (962)'], 'Papa', ['Cherkov boshlig\'i', 'Investituraga qarshi chiqdi', 'Grigoriy VII (1073-1085)']))
add('m06', 'Vizantiya tarixi', [('395', 'Sharqiy Rim imperiyasi'), ('527-565', 'Yustinian davri'), ('726', 'Ikonoborchlik boshlandi'), ('1054', 'Cherkovlar ajralishi'), ('1204', 'Salibchilar Konstantinopolni oldi'), ('1453', 'Usmonlilar fathi')],
    'yustinian', 'Yustinian islohotlari', tree('Yustinian davri', 'Yustinian I', [('Qonunlar', 'Yustinian kodeksi tuzildi'), ('Qurilish', 'Ayasofya sobori qurildi'), ('Fathlar', 'G\'arbiy hududlarni qaytarishga urindi')]))
add('m07', 'Slavyanlar davlatlari', [('VI asr', 'Slavyanlar Bolqonga yoyildi'), ('862', 'Ryurik Novgorodda'), ('863', 'Kirill va Mefodiy yozuv yaratdi'), ('IX asr', 'Buyuk Moraviya'), ('988', 'Kiyev Rusi xristianlikni qabul qildi')],
    'guruh', 'Slavyanlarning uch tarmog\'i', tree('Slavyanlar', 'Slavyanlar', [('Sharqiy', 'Ruslar, ukrainlar, belaruslar'), ('G\'arbiy', 'Chexlar, slovaklar, polyaklar'), ('Janubiy', 'Serblar, xorvatlar, bolgarlar')]))
add('m08', 'Islom dinining paydo bo\'lishi', [('570 y.', 'Muhammad (s.a.v.) Makkada tug\'ildi'), ('610', 'Birinchi vahiy'), ('622', 'Hijrat: Makkadan Madinaga'), ('630', 'Makka fath etildi'), ('632', 'Payg\'ambar vafoti')],
    'tayanch', 'Islomning besh ustuni', tree('Islom ustunlari', 'Islom arkonlari', [('Shahodat', 'Imon kalimasi'), ('Namoz', 'Kuniga besh vaqt'), ('Zakot', 'Mol-mulkdan ehson'), ('Ro\'za', 'Ramazon oyida'), ('Haj', 'Makkaga ziyorat')]))
add('m09', 'Arab xalifaligi', [('632-661', 'To\'rt solih xalifa davri'), ('661-750', 'Umaviylar sulolasi'), ('711', 'Ispaniyaning fath etilishi'), ('750-1258', 'Abbosiylar sulolasi'), ('762', 'Bag\'dod barpo etildi'), ('1258', 'Mo\'g\'ullar Bag\'dodni oldi')],
    'sulola', 'Umaviylar va Abbosiylar', compare('Ikki sulola', 'Umaviylar', ['Poytaxt: Damashq', 'Hukmronlik: 661-750', 'Arablar imtiyozli edi'], 'Abbosiylar', ['Poytaxt: Bag\'dod', 'Hukmronlik: 750-1258', 'Boshqa xalqlar ham mansabga chiqdi']))
add('m10', 'Saljuqiylar davlati', [('XI asr', 'Saljuqiylar Movarounnahr va Xurosonda'), ('1040', 'Dandanakan jangi'), ('1055', 'Tug\'rulbek Bag\'dodda'), ('1071', 'Malazgirt jangi'), ('1092', 'Nizomulmulk vafoti')],
    'idora', 'Saljuqiylar idora tizimi', tree('Saljuqiylar boshqaruvi', 'Sulton', [('Vazir', 'Nizomulmulk — davlat ishlari'), ('Iqta', 'Yer berish tizimi, harbiy xizmat evaziga'), ('Nizomiya', 'Madrasalar tarmog\'i')]))
add('m11', 'Mo\'g\'ullar davlati', [('1206', 'Chingizxon qurultoyi'), ('1219-1221', 'Markaziy Osiyoga yurish'), ('1227', 'Chingizxon vafoti'), ('1236-1242', 'Botuxon Yevropaga yurishi'), ('1260', 'Mo\'g\'ul imperiyasining bo\'linishi')],
    'ulus', 'Mo\'g\'ul imperiyasi uluslari', tree('Imperiya uluslari', 'Mo\'g\'ul imperiyasi', [('Oltin O\'rda', 'Botuxon, Sharqiy Yevropa'), ('Chig\'atoy ulusi', 'Markaziy Osiyo'), ('Elxonlar', 'Eron va Old Osiyo'), ('Yuan', 'Xitoy, Xubilay')]))
add('m12', 'Hindiston tarixi', [('IV-VI asrlar', 'Gupta imperiyasi'), ('VII asr', 'Harshavardxana davri'), ('XI asr', 'G\'aznaviylar yurishlari'), ('1206', 'Dehli sultonligi'), ('XIII asr', 'Qutb Minor qurilishi')],
    'kasta', 'Hind jamiyatidagi to\'rt varna', layers('Hind jamiyati (varnalar)', [('Braxmanlar', 'ruhoniylar', '#a78bfa', 1), ('Kshatriyalar', 'jangchilar', '#f87171', 1), ('Vayshyalar', 'dehqon va savdogarlar', '#fbbf24', 1), ('Shudralar', 'xizmatkorlar', '#60a5fa', 1)]))
add('m13', 'Xitoy tarixi', [('589', 'Sui sulolasi birlashtirdi'), ('618-907', 'Tan sulolasi'), ('960-1279', 'Sun sulolasi'), ('1271-1368', 'Yuan (mo\'g\'ullar)'), ('1368', 'Min sulolasi')],
    'kashf', 'Xitoyliklarning to\'rt buyuk kashfiyoti', tree('Xitoy kashfiyotlari', 'To\'rt kashfiyot', [('Qog\'oz', 'Yozuv va kitob uchun'), ('Kitob bosish', 'Yog\'och tamg\'ali bosma'), ('Porox', 'Harbiy ishda'), ('Kompas', 'Dengiz yo\'nalishi uchun')]))
add('m14', 'Koreya tarixi', [('I-VII asrlar', 'Uch qirollik: Koguryo, Pekche, Silla'), ('668', 'Silla Koreyani birlashtirdi'), ('918', 'Koryo davlati'), ('1392', 'Choson sulolasi'), ('1443', 'Xangul alifbosi yaratildi')],
    'qirollik', 'Koreyadagi uch qirollik', tree('Uch qirollik', 'Koreya (IV-VII asr)', [('Koguryo', 'Shimol'), ('Pekche', 'Janubi-g\'arb'), ('Silla', 'Janubi-sharq, keyin birlashtirdi')]))
add('m15', 'Yaponiya tarixi', [('645', 'Taika islohotlari'), ('710', 'Nara poytaxt'), ('794', 'Xeyan (Kioto) poytaxt'), ('1192', 'Minamoto Yoritomo syogun'), ('XII-XIX asrlar', 'Syogunlar hukmronligi')],
    'tuzum', 'Yaponiya jamiyati', layers('Yaponiya jamiyati', [('Imperator', 'ramziy hukmdor', '#a78bfa', 1), ('Syogun', 'haqiqiy hokimiyat', '#f87171', 1), ('Daymyo va samuraylar', 'harbiylar', '#fbbf24', 1.2), ('Dehqonlar', 'hunarmand, savdogar', '#34d399', 1.2)]))
add('m16', 'Amerika xalqlari', [('VII asr', 'Mayya shahar-davlatlari gullagan'), ('XII asr', 'Tolteklar tanazzuli'), ('1325', 'Tenochtitlan (asteklar) asos solindi'), ('XV asr', 'Inklar imperiyasi'), ('1492', 'Kolumb Amerikaga yetdi')],
    'xalq', 'Amerikaning uch buyuk xalqi', tree('Hind tsivilizatsiyalari', 'Amerika', [('Mayya', 'Mesoamerika, ierogliflar va taqvim'), ('Asteklar', 'Tenochtitlan, Meksika vodiysi'), ('Inklar', 'And tog\'lari, Kusko')]))
add('m17', 'Xristian olamidagi o\'zgarishlar', [('1054', 'Katolik va pravoslav ajraldi'), ('XI asr', 'Cherkov islohoti'), ('1095', 'Birinchi salib yurishiga chaqiriq'), ('XIII asr', 'Dominikanlar va fransiskanlar'), ('1215', 'IV Lateran kengashi')],
    'cherkov', 'Katolik va pravoslav', compare('Cherkovlar', 'Katolik', ['Markazi: Rim', 'Boshlig\'i: Rim papasi', 'Lotin tilida xizmat'], 'Pravoslav', ['Markazi: Konstantinopol', 'Patriarxlar boshqaradi', 'Mahalliy tillarda xizmat']))
add('m18', 'Salib yurishlari', [('1095', 'Papa Urban II chaqirig\'i'), ('1099', 'Quddus olindi'), ('1187', 'Salohiddin Quddusni qaytardi'), ('1204', 'IV yurish: Konstantinopol'), ('1270', 'So\'nggi, VIII yurish')],
    'sabab', 'Salib yurishlarining sabablari va natijalari', compare('Sabablar va natijalar', 'Sabablar', ['Muqaddas joylarni ozod etish', 'Papa hokimiyatini kuchaytirish', 'Yer va boylik izlash'], 'Natijalar', ['Sharq bilan savdo kengaydi', 'Feodallar kuchsizlandi', 'Yevropaga yangi bilimlar keldi']))
add('m19', 'Yevropa shaharlari', [('X-XI asrlar', 'Shaharlar tiklana boshladi'), ('XII asr', 'Shaharlar mustaqillik oldi'), ('XII-XIII', 'Hunarmand sexlari'), ('XIII asr', 'Savdo ittifoqi: Gansa'), ('XIII asr', 'Gildiyalar kuchaydi')],
    'sinf', 'O\'rta asr shahri aholisi', layers('Shahar aholisi', [('Patritsiylar', 'boy savdogarlar', '#a78bfa', 1), ('Sex ustalari', 'hunarmandlar', '#fbbf24', 1), ('Shogirdlar', 'yollanma ishchilar', '#34d399', 1), ('Shahar kambag\'allari', 'ishsizlar', '#94a3b8', 1)]))
add('m20', 'Osiyo shaharlari', [('VIII asr', 'Bag\'dod, Damashq gullagan'), ('IX-X asrlar', 'Buxoro, Samarqand'), ('X asr', 'Qohira shahri'), ('XIII asr', 'Xitoyda Dadu (Pekin)'), ('XIII asr', 'Sharq savdosi gullagan')],
    'taqqos', 'Yevropa va Osiyo shaharlari', compare('Shaharlarni taqqoslash', 'Yevropa shahri', ['Mustaqillik uchun kurash', 'Sex va gildiyalar', 'Shahar devori va ratusha'], 'Osiyo shahri', ['Hokimga bo\'ysungan', 'Bozor va karvonsaroylar', 'Katta shahar aholisi (Bag\'dod)']))
add('m21', 'Yevropa madaniyati', [('XI asr', 'Roman uslubi'), ('1088', 'Boloniya universiteti'), ('XII asr', 'Universitetlar ochildi'), ('XII-XIII', 'Gotika uslubi'), ('XIII asr', 'Tomas Akvinskiy')],
    'uslub', 'Roman va gotika uslubi', compare('Me\'morchilik uslublari', 'Roman', ['Yarim doira ravoq', 'Qalin devor, kichik oyna', 'Qal\'aga o\'xshash'], 'Gotika', ['Uchli ravoq', 'Baland minoralar, vitraj oynalar', 'Yorug\'lik ko\'p']))
add('m22', 'Arab xalifaligi madaniyati', [('VIII asr', 'Tarjimonlik harakati'), ('IX asr', 'Bag\'dodda "Bilimlar uyi"'), ('IX asr', 'Al-Xorazmiy algebra asarini yozdi'), ('XI asr', 'Beruniy va Ibn Sino'), ('XII asr', 'Ibn Rushd Kordovada')],
    'olim', 'Mashhur olimlar va ularning sohalari', tree('Olimlar', 'Xalifalik fani', [('Al-Xorazmiy', 'Matematika, algebra'), ('Beruniy', 'Astronomiya, geografiya'), ('Ibn Sino', 'Tibbiyot, "Tib qonunlari"'), ('Ibn Rushd', 'Falsafa, tibbiyot')]))
add('m23', 'Sharq xalqlari madaniyati', [('VII-X asrlar', 'Tan davrida she\'riyat gullagan'), ('IX asr', 'Bosma kitob (Xitoy)'), ('XI asr', 'Yaponiyada "Genji haqida roman"'), ('1443', 'Xangul alifbosi (Koreya)'), ('XIII asr', 'Konarak ibodatxonasi (Hindiston)')],
    'din', 'Sharq xalqlarining dinlari', tree('Dinlar va qarashlar', 'Sharq', [('Buddizm', 'Hindistondan Xitoy, Koreya, Yaponiyaga tarqaldi'), ('Konfutsiychilik', 'Xitoyda davlat va oila tartibi'), ('Sintoizm', 'Yaponiyada tabiat ruhlariga e\'tiqod')]))

inject('jahon7', I)
