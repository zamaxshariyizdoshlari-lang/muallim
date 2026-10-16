# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from tarix_svg import *

I = {}
add = adder('u8', I)

add('t01', 'Xorazm XIII asr boshi', [('1200-1220', 'Muhammad Xorazmshoh'), ('1210', 'Samarqand olindi'), ('1212', 'Qoraxitoylar mag\'lub'), ('1215', 'G\'urlar qulatildi'), ('1218', 'Otror voqeasi')],
    'ichki', 'Davlatning ichki ziddiyatlari', compare('Xorazmshohlar davlati', 'Kuchli tomonlari', ['Katta hudud', 'Boy shaharlar', 'Yirik qo\'shin'], 'Zaif tomonlari', ['Qipchoq beklari bilan ziddiyat', 'Turkan xotun ta\'siri', 'Markazlashuvning kuchsizligi']))
add('t02', 'Xorazm va mo\'g\'ullar', [('1218', 'Otror voqeasi'), ('1219', 'Mo\'g\'ul yurishi boshlandi'), ('1220', 'Buxoro va Samarqand'), ('1221', 'Urganch qamali'), ('1231', 'Jaloliddin vafoti')],
    'sabab', 'Urushning sabablari', tree('Sabablar', 'Mo\'g\'ul-Xorazm urushi', [('Otror', 'Savdogarlar o\'ldirildi'), ('Elchilar', 'Mo\'g\'ul elchisi o\'ldirildi'), ('Siyosat', 'Chingizxonning kengayish rejasi')]))
add('t03', 'Mudofaa va oqibatlari', [('1219', 'Qo\'shin bo\'lib tashlandi'), ('1220', 'Buxoro olindi'), ('1220', 'Samarqand olindi'), ('1220', 'Muhammad Xorazmshoh qochdi'), ('1221', 'Urganch quladi')],
    'xato', 'Mudofaa xatolari', tree('Xatolar', 'Mudofaa xatosi', [('Qo\'shin bo\'linishi', 'Kuch tarqatib yuborildi'), ('Shahar devori', 'Faqat qal\'alar himoyasiga tayanish'), ('Rahbar', 'Qochish ruhni susaytirdi')]))
add('t04', 'Jaloliddin Manguberdi', [('1198', 'Tug\'ilgan yili'), ('1220', 'Taxtga o\'tirdi'), ('1221', 'Parvon jangi'), ('1221', 'Sind daryosi'), ('1231', 'Vafot etdi')],
    'jang', 'Jaloliddinning g\'alabalari', flow('Janglar', [('Parvon', '1221'), ('Sind', 'daryodan o\'tdi'), ('Hindiston', 'yurishlar'), ('Eron', 'Tabriz'), ('Vafot', '1231')]))
add('t05', 'Davlatni tiklash yo\'li', [('1221', 'Parvon g\'alabasi'), ('1222', 'Hindistonda'), ('1224', 'Eronga qaytdi'), ('1225', 'Tabriz olindi'), ('1230', 'Yassichimen jangi')],
    'sabab', 'Muvaffaqiyatsizlik sabablari', compare('Tiklash urinishi', 'Yutuqlar', ['Parvon g\'alabasi', 'Tabriz olindi', 'Yangi davlat'], 'Muammolar', ['Beklarning kelishmovchiligi', 'Yassichimen mag\'lubiyati', 'Kuchlar yetmadi']))
add('t06', 'Chig\'atoy ulusi', [('1227', 'Chingizxon vafoti'), ('1227', 'Chig\'atoy ulusi tashkil'), ('1241', 'Chig\'atoy vafoti'), ('1260', 'Mas\'udbek'), ('1266', 'Ulus boshqaruvi')],
    'ulus', 'Mo\'g\'ul uluslari', tree('Uluslar', 'Mo\'g\'ul imperiyasi', [('Joji ulusi', 'Dashti Qipchoq'), ('Chig\'atoy ulusi', 'Movarounnahr, Yettisuv'), ('O\'qtoy ulusi', 'Mo\'g\'uliston'), ('Tuluy ulusi', 'Markaz')]))
add('t07', 'Chig\'atoy ulusining bo\'linishi', [('1321', 'Kebekxon islohotlari'), ('1326', 'Tarmashirin'), ('1346', 'Ulus bo\'linishi'), ('Movarounnahr', 'G\'arbiy qism'), ('Mo\'g\'uliston', 'Sharqiy qism')],
    'iqtisod', 'Kebekxon islohoti', tree('Islohot', 'Kebekxon', [('Pul', 'Yagona kumush tanga'), ('Qarshi', 'Yangi poytaxt'), ('Soliq', 'Tartibga solindi')]))
add('t08', 'Ilm-fan XIII-XIV asr', [('XIII asr', 'Mo\'g\'ul istilosi'), ('XIII asr', 'Najmiddin Kubro'), ('XIV asr', 'Maxmud Chag\'miniy'), ('XIV asr', 'Sa\'diddin Taftazoniy'), ('XIV asr', 'Alisher Navoiygacha')],
    'olim', 'Ilm va madaniyat', tree('Olimlar', 'XIII-XIV asr', [('Najmiddin Kubro', 'Tasavvuf'), ('Chag\'miniy', 'Astronomiya'), ('Taftazoniy', 'Kalom va mantiq'), ('Qutb Rumiy', 'Astronomiya')]))
add('t09', 'Turon XIV asr o\'rtalari', [('1346', 'Ulus bo\'linishi'), ('1347', 'Qozonxon o\'ldirildi'), ('1348', 'Tug\'luq Temur'), ('1358', 'Amir Husayn'), ('1360', 'Mo\'g\'uliston xoni')],
    'kuch', 'Siyosiy kuchlar', tree('Kuchlar', 'Turon', [('Amir Husayn', 'Qashqadaryo, Balx'), ('Amir Temur', 'Kesh'), ('Mo\'g\'uliston', 'Tug\'luq Temur')]))
add('t10', 'Amir Temur hukmdor', [('1336', 'Tug\'ildi'), ('1360', 'Tug\'luq Temur bilan'), ('1364', 'Chinoz jangi'), ('1366', 'Samarqandda'), ('1370', 'Hokimiyatga keldi')],
    'jang', 'Amir Temur yo\'li', flow('Hokimiyatgacha', [('Tug\'ilish', '1336'), ('Kesh', 'hokim'), ('Husayn', 'ittifoq'), ('Samarqand', '1366'), ('Balx', '1370')]))
add('t11', 'Markazlashgan davlat', [('1370', 'Balxda qurultoy'), ('1372-1388', 'Xorazm yurishlari'), ('1380', 'Mo\'g\'uliston yurishi'), ('1388', 'Xorazm bo\'ysundi'), ('1391', 'To\'xtamishga qarshi')],
    'yurish', 'Dastlabki yurishlar', tree('Yurishlar', 'Markazlashuv', [('Xorazm', '1372-1388'), ('Mo\'g\'uliston', '1371-1390'), ('Oltin O\'rda', '1391-1395')]))
add('t12', 'Tashqi siyosat', [('1381-1387', 'Eron yurishi'), ('1391-1395', 'Oltin O\'rda'), ('1398-1399', 'Hindiston yurishi'), ('1400-1402', 'Suriya, Anqara'), ('1405', 'Xitoy yurishi, vafot')],
    'yurish', 'Yurishlar yo\'nalishi', tree('Yurishlar', 'Amir Temur', [('Shimol', 'Oltin O\'rda'), ('G\'arb', 'Eron, Kavkaz, Anqara'), ('Janub', 'Hindiston'), ('Sharq', 'Xitoy rejasi')]))
add('t13', 'Harbiy strategiya', [('Qo\'shin', 'O\'nlik, yuzlik, mingliklar'), ('Razvedka', 'Josuslar tarmog\'i'), ('Jang', 'Markaz va qanotlar'), ('1402', 'Anqara jangi'), ('Taktika', 'Ko\'ngilli ittifoq')],
    'tuzilma', 'Qo\'shin tuzilmasi', layers('Qo\'shin tuzilishi', [('Ming', 'mingboshi', '#a78bfa', 1), ('Yuz', 'yuzboshi', '#fbbf24', 1), ('O\'n', 'o\'nboshi', '#34d399', 1)]))
add('t14', 'Davlat boshqaruvi', [('1370', 'Markazlashgan davlat'), ('Devon', 'Oliy kengash'), ('Vazir', 'Maslahatchi'), ('Soliq', 'Tartibli'), ('Qonun', 'Tuzuklar')],
    'tuzum', 'Boshqaruv tizimi', tree('Boshqaruv', 'Sohibqiron', [('Devon', 'Davlat kengashi'), ('Vazir', 'Moliya va ma\'muriyat'), ('Viloyatlar', 'Hokimlar boshqardi')]))
add('t15', 'Jahon tarixida o\'rni', [('1370', 'Davlat asoschisi'), ('1402', 'Anqara jangi'), ('Savdo', 'Ipak yo\'lini tikladi'), ('Me\'morchilik', 'Samarqand obodligi'), ('1405', 'Vafot etdi')],
    'ahamiyat', 'Temur davlatining ahamiyati', tree('Ahamiyati', 'Amir Temur', [('Siyosat', 'Markazlashgan davlat'), ('Iqtisod', 'Savdo va hunarmandchilik'), ('Madaniyat', 'Fan va san\'at gullagan')]))
add('t16', 'Obodonlashtirish', [('1399', 'Bibixonim masjidi'), ('1380', 'Shahrisabz'), ('1398-1404', 'Oqsaroy'), ('1404', 'Go\'ri Amir'), ('Samarqand', 'Poytaxt')],
    'bino', 'Temur davri binolari', tree('Binolar', 'Me\'morchilik', [('Oqsaroy', 'Shahrisabzda'), ('Bibixonim', 'Samarqandda masjid'), ('Go\'ri Amir', 'Maqbara'), ('Yassaviy', 'Turkistonda')]))
add('t17', 'Temuriylar davri', [('1405', 'Shohruh hokimiyatda'), ('1409', 'Ulug\'bek Samarqandda'), ('1447', 'Shohruh vafoti'), ('1451', 'Abu Said'), ('1469', 'Husayn Boyqaro')],
    'markaz', 'Ikki markaz', compare('Temuriylar', 'Samarqand', ['Poytaxt: Samarqand', 'Ulug\'bek hukmdor', 'Fan markazi'], 'Hirot', ['Poytaxt: Hirot', 'Shohruh va Boyqaro', 'Madaniyat markazi']))
add('t18', 'Mirzo Ulug\'bek', [('1394', 'Tug\'ildi'), ('1409', 'Samarqand hokimi'), ('1420', 'Madrasa qurildi'), ('1428', 'Rasadxona'), ('1449', 'O\'ldirildi')],
    'asar', 'Ulug\'bek yutuqlari', tree('Ulug\'bek', 'Olim hukmdor', [('Rasadxona', 'Samarqand'), ('Zij', '"Ziji jadidi Ko\'ragoniy"'), ('Madrasa', 'Samarqand, Buxoro, G\'ijduvon')]))
add('t19', 'Sulton Husayn Mirzo', [('1438', 'Tug\'ildi'), ('1469', 'Hirotni oldi'), ('1469-1506', 'Hukmronlik'), ('Navoiy', 'Vazir va do\'st'), ('1506', 'Vafot etdi')],
    'davr', 'Hirot madaniy markaz', tree('Hirot', 'Husayn Boyqaro', [('Navoiy', 'Adabiyot'), ('Behzod', 'Miniatyura'), ('Jomiy', 'Shoir va olim')]))
add('t20', 'Iqtisodiy munosabatlar', [('1370', 'Pul tizimi'), ('1380', 'Savdo markazlari'), ('1404', 'Samarqand bozori'), ('1427', 'Soliq tartibi'), ('XV asr', 'Hunarmandchilik')],
    'soha', 'Iqtisod sohalari', tree('Iqtisod', 'Temuriylar', [('Dehqonchilik', 'Sug\'orish'), ('Hunarmandchilik', 'Kulolchilik, to\'qimachilik'), ('Savdo', 'Ipak yo\'li')]))
add('t21', 'Ikkinchi Renessans', [('1370', 'Temur markazlashuvi'), ('1409', 'Ulug\'bek davri'), ('1420', 'Ulug\'bek madrasasi'), ('1469', 'Hirot gullashi'), ('1483', 'Navoiy asarlari')],
    'asos', 'Ikkinchi Renessans asoschilari', tree('Asoschilar', 'Renessans', [('Ulug\'bek', 'Fan'), ('Navoiy', 'Adabiyot'), ('Behzod', 'San\'at'), ('Jomiy', 'Falsafa')]))
add('t22', 'Me\'morchilik', [('1399', 'Bibixonim masjidi'), ('1404', 'Go\'ri Amir'), ('1417-1420', 'Ulug\'bek madrasasi'), ('XV asr', 'Shohi Zinda'), ('1465', 'Gavharshod masjidi')],
    'majmua', 'Mashhur majmualar', tree('Majmualar', 'Temuriylar me\'morchiligi', [('Registon', 'Samarqand'), ('Shohi Zinda', 'Maqbaralar'), ('Go\'ri Amir', 'Temur maqbarasi')]))
add('t23', 'San\'at va hunarmandchilik', [('XIV asr', 'Xattotlik'), ('XV asr', 'Miniatyura'), ('Behzod', 'Hirot maktabi'), ('Kulolchilik', 'Sirli idishlar'), ('Naqqoshlik', 'Binolar bezagi')],
    'san', 'San\'at turlari', tree('San\'at', 'Temuriylar san\'ati', [('Xattotlik', 'Nasta\'liq'), ('Miniatyura', 'Kitob rasmlari'), ('Kulolchilik', 'Sirlangan buyumlar')]))
add('t24', 'Alisher Navoiy', [('1441', 'Hirotda tug\'ildi'), ('1469', 'Husayn bilan'), ('1483', '"Xamsa"'), ('1499', '"Muhokamat ul-lug\'atayn"'), ('1501', 'Vafot etdi')],
    'asar', 'Navoiy asarlari', tree('Asarlar', 'Alisher Navoiy', [('Xamsa', 'Besh doston'), ('G\'azallar', '"Xazoyin ul-maoniy"'), ('Muhokamat', 'Til haqida'), ('Mezon ul-avzon', 'Aruz ilmi')]))

inject('uzt8', I)
