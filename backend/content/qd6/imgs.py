# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from tarix_svg import *

I = {}
add = adder('q6', I)

add('p01', 'Tarix ildizlari', [('~3 mln yil', 'Eng qadimgi odamlar'), ('~40 ming yil', 'Aql-idrokli odam'), ('~10 ming yil', 'Dehqonchilik boshlandi'), ('~5 ming yil', 'Ilk davlatlar'), ('476', 'Antik davr oxiri')],
    'manba', 'Tarix manbalari', tree('Tarix manbalari', 'Tarixni o\'rganish', [('Moddiy', 'Qurol, idish, qal\'a'), ('Yozma', 'Kitob, yilnoma, yozuv'), ('Og\'zaki', 'Afsona, rivoyat')]))
add('p02', 'Qadimgi odamlar', [('Eng qadimgi', 'Tosh qurollar'), ('Neandertal', 'Olovdan foydalandi'), ('Kromanyon', 'Aql-idrokli odam'), ('Tosh asri', 'Ov va termachilik'), ('Neolit', 'Dehqonchilik')],
    'bos', 'Rivojlanish bosqichlari', flow('Odam rivoji', [('Ilk odam', 'tosh qurol'), ('Mohir odam', 'ov'), ('To\'g\'ri odam', 'olov'), ('Neandertal', 'g\'or'), ('Aql-idrokli', 'madaniyat')]))
add('p03', 'Urug\'chilik jamiyati', [('Ona urug\'i', 'Ayollar yetakchi'), ('Ota urug\'i', 'Erkaklar yetakchi'), ('Qabila', 'Urug\'lar birlashmasi'), ('Qo\'shni jamoa', 'Mulkiy tabaqalanish'), ('Davlat', 'Ilk davlatlar')],
    'urug', 'Urug\', qabila, ittifoq', layers('Jamiyat birliklari', [('Qabilalar ittifoqi', 'eng katta', '#a78bfa', 1), ('Qabila', 'urug\'lar yig\'indisi', '#fbbf24', 1), ('Urug\'', 'qarindoshlar', '#34d399', 1), ('Oila', 'asosiy hujayra', '#60a5fa', 1)]))
add('p04', 'Eneolit va bronza davri', [('Mis davri', 'Eneolit'), ('Bronza', 'Mis va qalay'), ('Ko\'chmanchi', 'Chorvadorlik'), ('Dehqonlar', 'Sug\'orish'), ('Shahar', 'Qadimgi shaharlar')],
    'metal', 'Tosh, mis, bronza, temir', flow('Metallar', [('Tosh', 'ilk qurol'), ('Mis', 'eneolit'), ('Bronza', 'qattiq'), ('Temir', 'eng mustahkam'), ('Qurol', 'rivojlandi')]))
add('p05', 'O\'rta Osiyo temir asri', [('Mil.avv. I ming', 'Temir davri boshi'), ('VII-VI asrlar', 'Xorazm, Baqtriya, So\'g\'d'), ('Sug\'orish', 'Kanallar qurildi'), ('Qal\'alar', 'Shahar tipidagi'), ('VI asr', 'Ahamoniylar fathi')],
    'mintaqa', 'Qadimgi viloyatlar', tree('Mintaqa', 'O\'rta Osiyo', [('Xorazm', 'Amudaryo quyi oqimi'), ('Baqtriya', 'Janub'), ('So\'g\'d', 'Zarafshon vodiysi'), ('Parfiya', 'Janubi-g\'arb')]))
add('p06', 'Nil vodiysi', [('Mil.avv. 4000', 'Nil bo\'yida dehqonlar'), ('Mil.avv. 3000', 'Misr birlashdi'), ('Nomlar', 'Hududiy birliklar'), ('Fir\'avn', 'Hokimiyat markazi'), ('Nil toshqini', 'Hosil manbayi')],
    'nil', 'Nil toshqini va dehqonchilik', cycle('Nil yillik sikli', [('Toshqin', 'iyun-sentyabr'), ('Ekish', 'oktyabr'), ('Hosil', 'mart-aprel')], 'Nil'))
add('p07', 'Qadimgi Misr', [('3100', 'Menes Misrni birlashtirdi'), ('~2600', 'Eski podsholik, piramidalar'), ('~2000', 'O\'rta podsholik'), ('~1550', 'Yangi podsholik'), ('1479-1425', 'Tutmos III')],
    'pod', 'Misr podsholiklari', flow('Podsholiklar', [('Eski', 'piramidalar'), ('O\'rta', 'gullash'), ('Yangi', 'fathlar'), ('Tutmos III', 'qudrat'), ('Pasayish', 'fors fathi')]))
add('p08', 'Qadimgi Misr dini', [('Ra', 'Quyosh xudosi'), ('Osiris', 'O\'liklar hukmdori'), ('Isis', 'Ona ma\'budasi'), ('Anubis', 'Murdalar posboni'), ('Mumiyolash', 'O\'lim keyingi hayot')],
    'xudo', 'Misr xudolari', tree('Xudolar', 'Misr xudolari', [('Ra', 'Quyosh'), ('Osiris', 'Narigi dunyo'), ('Isis', 'Oila homiysi'), ('Anubis', 'Mumiyolash')]))
add('p09', 'Piramidalar', [('~2650', 'Djoser pog\'onali piramidasi'), ('~2560', 'Xeops piramidasi'), ('~2500', 'Xafre va Menkaure'), ('O\'rta pod.', 'Yangi qabr turlari'), ('Yangi pod.', 'Shoh vodiysi')],
    'jam', 'Piramida: qurilish va maqsadi', compare('Piramida', 'Maqsad', ['Fir\'avn maqbarasi', 'Keyingi hayotga tayyorgarlik', 'Hokimiyat ramzi'], 'Qurilish', ['Tosh bloklar', 'Ming-minglab ishchi', 'Xeops: ~146 m']))
add('p10', 'Misr madaniyati', [('~3000', 'Ieroglif yozuv'), ('Papirus', 'Yozuv materiali'), ('Taqvim', '365 kunlik yil'), ('Tibbiyot', 'Jarrohlik'), ('Me\'morchilik', 'Ibodatxonalar')],
    'ilm', 'Misr yutuqlari', tree('Misr yutuqlari', 'Misr', [('Yozuv', 'Ieroglif, papirus'), ('Fan', 'Geometriya, taqvim'), ('Tibbiyot', 'Davolash usullari'), ('San\'at', 'Haykal, relyef')]))
add('p11', 'Mesopotamiya', [('~3500', 'Shumer shaharlari'), ('~2350', 'Akkad (Sargon)'), ('~2100', 'Ur shohligi'), ('~1800', 'Bobil kuchaydi'), ('~1100', 'Ossuriya yuksalishi')],
    'shumer', 'Shumer ixtirolari', tree('Shumer', 'Shumerlar', [('Mixxat yozuv', 'Loy lavhalar'), ('G\'ildirak', 'Transport'), ('60 lik sanoq', 'Vaqt, burchak'), ('Zikkurat', 'Ibodatxona')]))
add('p12', 'Bobil podsholigi', [('~1894', 'Bobil shahri asos solindi'), ('1792-1750', 'Xammurapi'), ('~1760', 'Xammurapi qonunlari'), ('~1595', 'Xett bosqini'), ('604-562', 'Navuxodonosor II')],
    'qonun', 'Xammurapi qonunlari', compare('Xammurapi qonunlari', 'Mohiyati', ['282 modda', 'Tosh ustunga yozilgan', 'Qasos tamoyili'], 'Ahamiyati', ['Adolat va tartib', 'Jamiyat tabaqalari', 'Eng qadimgi qonunlardan']))
add('p13', 'Old Osiyo davlatlari', [('~1600', 'Xett davlati'), ('~1200', 'Finikiya shaharlari'), ('~1000', 'Isroil-Yahudo'), ('IX-VII', 'Ossuriya imperiyasi'), ('612', 'Nineviya qulashi')],
    'davlat', 'Old Osiyo xalqlari', tree('Old Osiyo', 'Davlatlar', [('Finikiya', 'Alifbo, dengiz savdosi'), ('Xett', 'Temir ishlash'), ('Ossuriya', 'Kuchli armiya'), ('Yahudo', 'Yakkaxudolik')]))
add('p14', 'Ahamoniylar', [('550', 'Kir II Midiyani oldi'), ('539', 'Bobil olindi'), ('522-486', 'Doro I'), ('490', 'Marafon jangi'), ('330', 'Iskandar zabt etdi')],
    'vil', 'Satrapliklar tizimi', tree('Boshqaruv', 'Shohanshoh', [('Satrap', 'Viloyat hokimi'), ('Yo\'llar', 'Shoh yo\'li'), ('Soliq', 'Tangalar, solig\''), ('Armiya', 'Doimiy qo\'shin')]))
add('p15', 'Hindiston sivilizatsiyasi', [('~2600', 'Xarappa, Mohenjo-Daro'), ('~1800', 'Sivilizatsiya tanazzuli'), ('~1500', 'Oriylar kirib keldi'), ('Veda davri', 'Ilk matnlar'), ('~500', 'Buddizm paydo bo\'ldi')],
    'shahar', 'Hind vodiysi shaharlari', tree('Ilk shaharlar', 'Hind vodiysi', [('Xarappa', 'Yirik shahar'), ('Mohenjo-Daro', 'Hammom, kanalizatsiya'), ('Tartib', 'To\'g\'ri ko\'chalar')]))
add('p16', 'Hindiston madaniyati', [('Veda', 'Muqaddas matnlar'), ('~500', 'Buddizm'), ('Mahabharata', 'Dostonlar'), ('Ramayana', 'Dostonlar'), ('Raqamlar', 'Nol va o\'nlik tizim')],
    'din', 'Hind dinlari', tree('Dinlar', 'Hindiston', [('Braxmanizm', 'Veda diniga asoslangan'), ('Buddizm', 'Budda ta\'limoti'), ('Jaynizm', 'Zo\'ravonlikka qarshi')]))
add('p17', 'Qadimgi Xitoy', [('~2070', 'Syaskaya sulola'), ('~1600', 'Shan sulolasi'), ('~1046', 'Chjou'), ('551', 'Konfutsiy tug\'ildi'), ('221', 'Sin Shixuandi birlashtirdi')],
    'taqqos', 'Xitoy kashfiyotlari', tree('Xitoy', 'Kashfiyotlar', [('Ipak', 'To\'qimachilik'), ('Qog\'oz', 'Yozuv'), ('Kompas', 'Yo\'nalish'), ('Yozuv', 'Ieroglif')]))
add('p18', 'III asr Xitoy', [('221', 'Sin Shixuandi imperiya'), ('213', 'Kitoblarni yoqish'), ('~214', 'Buyuk Xitoy devori'), ('206', 'Xan sulolasi'), ('~138', 'Chjan Szyan sayohati')],
    'sin', 'Sin Shixuandi islohotlari', tree('Birlashtirish', 'Sin Shixuandi', [('Yagona pul', 'Savdo osonlashdi'), ('Yagona yozuv', 'Aloqa'), ('Devor', 'Shimoldan himoya')]))
add('p19_20', 'O\'zbekiston davlatlari', [('VII-VI asrlar', 'Xorazm, Baqtriya'), ('550-330', 'Ahamoniylar'), ('329-327', 'Iskandarga qarshi kurash'), ('III-II asr', 'Yunon-Baqtriya'), ('I-IV asrlar', 'Kushon davlati')],
    'davlat', 'Ilk davlatlar', tree('Davlatlar', 'O\'zbekiston hududi', [('Xorazm', 'Amudaryo bo\'yi'), ('Baqtriya', 'Surxondaryo'), ('So\'g\'d', 'Samarqand')]))
add('p21', 'Zardushtiylik', [('Mil.avv. I ming', 'Zardusht ta\'limoti'), ('Avesto', 'Muqaddas kitob'), ('Ahuramazda', 'Ezgulik xudosi'), ('Axriman', 'Yovuzlik'), ('Xorazm', 'Avesto vatani')],
    'jam', 'Ezgulik va yovuzlik', compare('Zardushtiylik', 'Ahuramazda', ['Ezgulik xudosi', 'Yorug\'lik', 'Haqiqat'], 'Axriman', ['Yovuzlik', 'Zulmat', 'Yolg\'on']))
add('p22', 'Antik tarix', [('~2000', 'Krit madaniyati'), ('~1600', 'Miken davri'), ('XII asr', 'Dorilar kirishi'), ('VIII asr', 'Polislar'), ('776', 'Ilk Olimpiya')],
    'jam', 'Antik davr', tree('Antik davr', 'Antik dunyo', [('Yunoniston', 'Polislar'), ('Rim', 'Respublika, imperiya'), ('Madaniyat', 'Fan va san\'at')]))
add('p23_24', 'Qadimgi Yunoniston', [('VIII asr', 'Polislar'), ('776', 'Olimpiya o\'yinlari'), ('Spartada', 'Harbiy tarbiya'), ('Afinada', 'Demokratiya'), ('Peloponnes', 'Ikki ittifoq')],
    'tuzum', 'Afina va Sparta', compare('Afina va Sparta', 'Afina', ['Demokratiya', 'Savdo, san\'at', 'Fuqarolik ta\'limi'], 'Sparta', ['Harbiy jamiyat', 'Qattiq tarbiya', 'Oligarxiya']))
add('p25', 'Yunon koloniyalari', [('VIII asr', 'Koloniyalar tashkil topdi'), ('Italiya', 'Janubiy Italiya'), ('Qora dengiz', 'Savdo markazlari'), ('Marsel', 'G\'arbiy O\'rta yer'), ('Natija', 'Savdo va madaniyat')],
    'sabab', 'Koloniyalar sabablari', tree('Koloniyalar', 'Mustamlakalar', [('Yer yetishmasligi', 'Aholi ko\'paydi'), ('Savdo', 'Yangi bozorlar'), ('Siyosiy', 'Fuqarolar kurashi')]))
add('p26', 'Afinada demokratiya', [('594', 'Solon islohoti'), ('508', 'Klisfen'), ('461', 'Perikl davri'), ('Xalq majlisi', 'Oliy organ'), ('Ostrakizm', 'Qora ro\'yxat')],
    'org', 'Afina boshqaruvi', tree('Afina', 'Demokratiya', [('Xalq majlisi', 'Hamma fuqaro'), ('Besh yuzlar kengashi', 'Qonun tayyorlash'), ('Strateglar', 'Harbiy rahbarlar')]))
add('p27_28', 'Yunon-fors urushlari', [('499', 'Ioniya qo\'zg\'oloni'), ('490', 'Marafon jangi'), ('480', 'Termopila, Salamin'), ('479', 'Platey jangi'), ('338', 'Xeroneya jangi')],
    'jang', 'Asosiy janglar', flow('Janglar', [('Marafon', '490'), ('Termopila', '480'), ('Salamin', '480'), ('Platey', '479'), ('Xeroneya', '338')]))
add('p29', 'Yunon tarbiyasi', [('7 yoshda', 'Maktab'), ('Gimnastika', 'Jismoniy tarbiya'), ('Musiqa', 'Ruhiy tarbiya'), ('18 yosh', 'Efebiya'), ('Fuqaro', 'Polis himoyachisi')],
    'jam', 'Afina va Sparta tarbiyasi', compare('Tarbiya', 'Afina', ['Maktab, musiqa, she\'riyat', 'Jismoniy mashqlar', 'Fuqarolik tayyorgarligi'], 'Sparta', ['7 yoshdan harbiy lager', 'Qattiq intizom', 'Jangchi tayyorlash']))
add('p30', 'Yunoniston madaniyati', [('VIII asr', 'Gomer'), ('V asr', 'Parfenon qurildi'), ('V asr', 'Teatr: Sofokl, Evripid'), ('V asr', 'Gerodot, Fukidid'), ('Olimpiya', 'Sport o\'yinlari')],
    'jam', 'Yunon san\'ati', tree('Madaniyat', 'Yunoniston', [('Me\'morchilik', 'Parfenon'), ('Teatr', 'Fojia, komediya'), ('Haykal', 'Fidiy, Miron'), ('Adabiyot', 'Gomer')]))
add('p31', 'Yunon olimlari', [('VI asr', 'Fales'), ('~500', 'Pifagor'), ('V asr', 'Demokrit, Gerodot'), ('IV asr', 'Platon, Aristotel'), ('III asr', 'Arximed, Yevklid')],
    'olim', 'Olimlar va sohalar', tree('Olimlar', 'Yunon fani', [('Pifagor', 'Matematika'), ('Gippokrat', 'Tibbiyot'), ('Arximed', 'Fizika'), ('Aristotel', 'Falsafa')]))
add('p32', 'Yunon afsonalari', [('Zevs', 'Xudolar sardori'), ('Gera', 'Oila homiysi'), ('Afina', 'Donolik'), ('Apollon', 'San\'at'), ('Gerakl', 'Dostonlar')],
    'xudo', 'Olimp xudolari', tree('Olimp', 'Xudolar', [('Zevs', 'Osmon'), ('Poseydon', 'Dengiz'), ('Gades', 'Narigi dunyo'), ('Afina', 'Donolik')]))
add('p33_34', 'Ahamoniylar yurishlari', [('530', 'Kir massagetlarga qarshi'), ('Tomiris', 'Kirni mag\'lub etdi'), ('522', 'Doro hokimiyatga'), ('Behistun', 'Doro bitigi'), ('Sak', 'Sak yurishlari')],
    'jam', 'Tomiris', compare('Kir va Tomiris', 'Kir II', ['Ahamoniylar asoschisi', 'Massagetlarga yurdi', 'Jangda halok bo\'ldi'], 'Tomiris', ['Massagetlar malikasi', 'Vatan himoyasi', 'Kirni mag\'lub etdi']))
add('p35_36', 'Iskandarga qarshi', [('329', 'Iskandar Sirdaryo bo\'yida'), ('329-327', 'Spitamen qo\'zg\'oloni'), ('328', 'Spitamen halok bo\'ldi'), ('327', 'Sisimitr qal\'asi'), ('323', 'Iskandar vafoti')],
    'qahr', 'Spitamen', tree('Qarshilik', 'Mahalliy qahramonlar', [('Spitamen', 'So\'g\'d rahbari'), ('Oksiart', 'Baqtriya zodagoni'), ('Ariamaz', 'Qal\'a himoyachisi')]))
add('p37', 'Salavkiylar va Baqtriya', [('312', 'Salavkiylar davlati'), ('~250', 'Yunon-Baqtriya'), ('Evtidem', 'Yunon-Baqtriya shohi'), ('Demetriy', 'Hindistonga yurish'), ('140', 'Yuyechji bosqini')],
    'jam', 'Salavkiylar va Baqtriya', compare('Ikki davlat', 'Salavkiylar', ['Asoschi: Salavk I', 'Poytaxt: Antioxiya', 'Katta davlat'], 'Yunon-Baqtriya', ['Asoschi: Diodot', 'Hind va Baqtriya', 'Madaniy sintez']))
add('p38_39', 'Qadimgi Xorazm', [('VII-VI asr', 'Xorazm davlati'), ('Qal\'alar', 'Qo\'yqirilgan qal\'a'), ('Toprroq qal\'a', 'Shoh saroyi'), ('Afrig\'iylar', 'IV asr'), ('Zardushtiylik', 'Avesto bog\'liqligi')],
    'jam', 'Xorazm qal\'alari', tree('Xorazm', 'Qal\'alar', [('Qo\'yqirilgan qal\'a', 'Qadimiy qal\'a'), ('Ayozqal\'a', 'Mudofaa'), ('Toprroq qal\'a', 'Saroy majmuasi')]))
add('p40', 'Qang\' va Davan', [('II asr', 'Davan (Farg\'ona)'), ('Qang\'', 'Sirdaryo o\'rtasi'), ('Davan', 'Ot zotlari'), ('Xitoy', 'Chjan Szyan'), ('Savdo', 'Ipak yo\'li')],
    'davlat', 'Qang\' va Davan', compare('Qadimgi davlatlar', 'Davan', ['Farg\'ona vodiysi', 'Shahar: Ershi', 'Chopag\'on otlar'], 'Qang\'', ['Sirdaryo o\'rtasi', 'Chorvador va dehqon', 'Yirik davlat']))
add('p41', 'Kushon davlati', [('~I asr', 'Kujula Kadfiz'), ('78', 'Kanishka (taxminan)'), ('Kanishka', 'Buddizm homiysi'), ('Poytaxt', 'Purushapura'), ('III asr', 'Sosoniylar kuchayishi')],
    'jam', 'Kushon davlati', tree('Kushonlar', 'Kushon', [('Kanishka', 'Eng ulug\' hukmdor'), ('Tangalar', 'Oltin va mis pullar'), ('Buddizm', 'Homiylik')]))
add('p42', 'Buyuk ipak yo\'li', [('II asr', 'Chjan Szyan yo\'li'), ('I asr', 'Yo\'l shakllandi'), ('Samarqand', 'Savdo markazi'), ('Buxoro', 'Savdo markazi'), ('Tovar', 'Ipak, ziravor')],
    'yo', 'Ipak yo\'li tovarlari', compare('Ipak yo\'li', 'Sharqdan', ['Ipak', 'Chinni', 'Choy va ziravorlar'], 'G\'arbdan', ['Shisha', 'Zeb-ziynat', 'Otlar va uzum']))
add('p43', 'Qadimgi Italiya', [('~1000', 'Latinlar Italiyada'), ('VIII asr', 'Etrusklar'), ('753', 'Rim asos solindi'), ('VI asr', 'Rim podsholari'), ('509', 'Respublika')],
    'xalq', 'Italiya aholisi', tree('Aholi', 'Italiya', [('Latinlar', 'Rim aholisi'), ('Etrusklar', 'Shimol'), ('Yunonlar', 'Janub')]))
add('p44', 'Rim respublikasi', [('509', 'Respublika e\'lon qilindi'), ('494', 'Plebeylar chiqishi'), ('451', 'XII jadval qonuni'), ('264-241', 'Birinchi Pun urushi'), ('146', 'Karfagen qulashi')],
    'org', 'Rim boshqaruvi', tree('Respublika', 'Rim boshqaruvi', [('Senat', 'Maslahat, nazorat'), ('Konsullar', 'Ikki oliy hokim'), ('Xalq majlisi', 'Saylov va qonunlar')]))
add('p45', 'Rimda hayot', [('Forum', 'Markaziy maydon'), ('Akvedukl', 'Suv ta\'minoti'), ('Termalar', 'Hammomlar'), ('Kolizey', 'Tomosha'), ('Yo\'llar', 'Hamma yo\'llar Rimga')],
    'sinf', 'Rim jamiyati', layers('Rim jamiyati', [('Patrisiylar', 'zodagonlar', '#a78bfa', 1), ('Otliqlar', 'boy savdogarlar', '#fbbf24', 1), ('Plebeylar', 'oddiy fuqarolar', '#34d399', 1.2), ('Qullar', 'huquqsizlar', '#94a3b8', 1)]))
add('p46', 'Qullar va gladiatorlar', [('264', 'Gladiator o\'yinlari'), ('135-132', 'Sitsiliya qo\'zg\'oloni'), ('104-101', 'Ikkinchi Sitsiliya'), ('73', 'Spartak qo\'zg\'oloni'), ('71', 'Spartak halok bo\'ldi')],
    'spartak', 'Spartak qo\'zg\'oloni', flow('Spartak', [('Kapua', 'maktabdan qochish'), ('Vezuviy', 'qal\'a'), ('Qo\'shin', '70 ming'), ('Jang', 'Kras bilan'), ('71', 'mag\'lub')]))
add('p47', 'Respublikaning qulashi', [('133', 'Tiberiy Grakx'), ('88', 'Sulla va Marius'), ('60', 'Birinchi triumvirat'), ('44', 'Sezar o\'ldirildi'), ('27', 'Avgust, imperiya')],
    'sabab', 'Inqiroz sabablari', tree('Inqiroz', 'Respublika tanazzuli', [('Iqtisod', 'Yerning bir qo\'lda to\'planishi'), ('Siyosat', 'Fuqarolar urushi'), ('Armiya', 'Sarkardalarga sodiq')]))
add('p48', 'G\'arbiy Rim imperiyasi', [('284', 'Diokletian'), ('330', 'Konstantinopol'), ('395', 'Rim bo\'linishi'), ('410', 'Alarix Rimni oldi'), ('476', 'Imperiya tugadi')],
    'sabab', 'Inqiroz sabablari', tree('Halokat', 'G\'arbiy Rim', [('Iqtisod', 'Qullar mehnati samarasiz'), ('Siyosat', 'Imperatorlar o\'zgarishi'), ('Tashqi', 'Varvarlar hujumi')]))
add('p49_50', 'Rim madaniyati', [('I asr', 'Vergiliy, Ovidiy'), ('I asr', 'Kolizey qurildi'), ('Latin tili', 'Rim tili'), ('Huquq', 'Rim huquqi'), ('Me\'morchilik', 'Ravoq va gumbaz')],
    'mer', 'Rim qurilishlari', tree('Rim me\'morchiligi', 'Rim ixtirolari', [('Akveduk', 'Suv yetkazish'), ('Yo\'llar', 'Imperiya tarmog\'i'), ('Kolizey', 'Amfiteatr'), ('Gumbaz', 'Panteon')]))

inject('qd6', I)
