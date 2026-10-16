# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from tarix_svg import *

I = {}
add = adder('o7', I)

add('m01', 'Ma\'naviy qadriyatlar', [('Qadimgi davr', 'Og\'zaki ijod'), ('Mil.avv. I ming', 'Avesto'), ('Mil.avv.', 'Yozuv rivoji'), ('Ilk o\'rta asr', 'Ilm-fan'), ('IX-XII asrlar', 'Ilm-fan gullashi')],
    'qad', 'Qadriyatlar turlari', tree('Qadriyatlar', 'Ma\'naviy meros', [('Din', 'Zardushtiylik, buddizm, islom'), ('Yozuv', 'So\'g\'d, run, arab'), ('Adabiyot', 'Afsona va dostonlar'), ('San\'at', 'Me\'morchilik')]))
add('m02', 'IV-VII asr turmush tarzi', [('IV asr', 'Dehqonchilik vohalari'), ('V asr', 'Xioniylar'), ('VI asr', 'Turk xoqonligi'), ('VII asr', 'Savdo karvonlari'), ('VII asr', 'Qal\'a-shaharlar')],
    'kasb', 'Aholining kasblari', tree('Kasblar', 'Turmush', [('Dehqonchilik', 'Sug\'oriladigan yerlar'), ('Chorvachilik', 'Ko\'chmanchilar'), ('Hunarmandchilik', 'Shaharlarda'), ('Savdo', 'Ipak yo\'li')]))
add('m03_04', 'Xorazm IV-VII asr', [('IV asr', 'Afrig\'iylar sulolasi (305)'), ('VI asr', 'Turk xoqonligi ta\'siri'), ('VII asr', 'Xorazmshohlar'), ('Poytaxt', 'Kat'), ('995', 'Afrig\'iylar tugadi')],
    'afrig', 'Xorazm davlati', tree('Xorazm', 'Afrig\'iylar', [('Poytaxt', 'Kat shahri'), ('Hukmdor', 'Xorazmshoh'), ('Yozuv', 'Xorazm yozuvi')]))
add('m05', 'Xioniylar va kidariylar', [('IV asr', 'Xioniylar kirib keldi'), ('~350', 'Kidariylar'), ('IV asr', 'Kidariylar davlati'), ('V asr', 'Eftaliylar kuchayishi'), ('V asr', 'Kidariylar tarqaldi')],
    'jam', 'Xioniy va kidariylar', compare('Ikki qabila', 'Xioniylar', ['Kelib chiqishi: Xun', 'Tinch-mulkdorlik', 'Oldin kirib keldi'], 'Kidariylar', ['Baqtriya va Gandxara', 'Qo\'shni davlatlarga bosim', 'Eftaliylar siqib chiqardi']))
add('m06_07', 'Eftaliylar', [('V asr', 'Eftaliylar paydo bo\'ldi'), ('484', 'Eron shohi halok bo\'ldi'), ('V-VI asrlar', 'Baqtriya zabt etildi'), ('VI asr', 'Hindistonga yurish'), ('567', 'Turk xoqonligi mag\'lub etdi')],
    'ichki', 'Eftaliylar davlati', tree('Eftaliylar', 'Davlat', [('Poytaxt', 'Baqtriya shaharlari'), ('Hukmdor', 'Shoh'), ('Savdo', 'Ipak yo\'li nazorati')]))
add('m08_09', 'Turk xoqonligi', [('552', 'Bumin asos soldi'), ('553', 'Istami'), ('567', 'Eftaliylar mag\'lub'), ('603', 'G\'arbiy va Sharqiy'), ('630', 'Sharqiy xoqonlik mag\'lub')],
    'bol', 'Xoqonlik bo\'linishi', compare('Xoqonlik', 'Sharqiy', ['Markaz: Mo\'g\'uliston', 'Bumin (asoschi)', 'Xitoy bilan raqobat'], 'G\'arbiy', ['Markaz: Yettisuv', 'Istami (xoqon)', 'Ipak yo\'li nazorati']))
add('m10_11', 'G\'arbiy Turk xoqonligi', [('603', 'G\'arbiy xoqonlik'), ('VII asr', 'Tong Yabg\'u'), ('630', 'Yabg\'u xoqon'), ('VII asr', 'Siyosiy zaiflik'), ('659', 'Xitoy hujumi')],
    'markaz', 'Boshqaruv', tree('Boshqaruv', 'G\'arbiy xoqonlik', [('Xoqon', 'Oliy hukmdor'), ('Yabg\'u', 'Xoqonning o\'rinbosari'), ('Tudun', 'Hududlar nazoratchisi')]))
add('m12_13', 'Mahalliy hokimliklar', [('VI asr', 'Hokimliklar paydo bo\'ldi'), ('VII asr', 'Choch'), ('VII asr', 'Farg\'ona'), ('VII asr', 'Ustrushona'), ('VIII asr', 'Arablar bosqini')],
    'hokim', 'Hokimliklar', tree('Hokimliklar', 'Turon', [('Choch', 'Toshkent'), ('Farg\'ona', 'Axsikat'), ('Ustrushona', 'Zomin'), ('So\'g\'d', 'Samarqand')]))
add('m14_15', 'Harbiy san\'at', [('VI asr', 'Turk qo\'shinlari'), ('VII asr', 'Otliq qo\'shin'), ('Qurol', 'Kamon, qilich'), ('Mudofaa', 'Qal\'a devorlari'), ('Taktika', 'Pistirma')],
    'qurol', 'Qurol turlari', compare('Harbiy san\'at', 'Hujum', ['Kamon va o\'q', 'Qilich', 'Nayza'], 'Himoya', ['Sovut', 'Qalqon', 'Dubulg\'a']))
add('m16_17', 'Madaniy hayot VI-VII asr', [('VI asr', 'So\'g\'d yozuvi'), ('VI asr', 'Buddizm tarqaldi'), ('VII asr', 'Afrosiyob rasmlari'), ('VII asr', 'Varaxsha'), ('VII asr', 'Turk run yozuvi')],
    'san', 'Madaniyat sohalari', tree('Madaniyat', 'VI-VII asr', [('Yozuv', 'So\'g\'d, turk runik'), ('Rassomlik', 'Afrosiyob devoriy rasmlari'), ('Din', 'Zardushtiylik, buddizm')]))
add('m18_19', 'VII-VIII asr boshi', [('651', 'Eron arablarga'), ('654', 'Marv olindi'), ('705', 'Qutayba Xurosonda'), ('712', 'Samarqand olindi'), ('719', 'Xitoyga elchi')],
    'siyosat', 'Siyosiy kuchlar', compare('Turon', 'Mahalliy kuchlar', ['So\'g\'d, Farg\'ona, Choch', 'Parchalanib qolgan', 'Turk ta\'siri'], 'Arablar', ['Xalifalik', 'Qutayba ibn Muslim', 'Fath siyosati']))
add('m20_21', 'VIII asrda Xuroson va Movarounnahr', [('712', 'Samarqand arablarga'), ('720', 'Muqanna qo\'zg\'oloni oldi'), ('750', 'Abbosiylar'), ('776-783', 'Muqanna qo\'zg\'oloni'), ('751', 'Talas jangi')],
    'qozg', 'Muqanna qo\'zg\'oloni', tree('Qo\'zg\'olon', 'Muqanna (776-783)', [('Sabab', 'Soliq va zulm'), ('Markaz', 'Kesh, Navqad'), ('Natija', 'Mag\'lub bo\'ldi')]))
add('m22_23', 'Qarluqlar, o\'g\'uzlar, tohiriylar', [('VIII asr', 'Qarluqlar kuchaydi'), ('751', 'Talas jangi'), ('IX asr', 'O\'g\'uzlar'), ('821', 'Tohiriylar davlati'), ('873', 'Tohiriylar tugadi')],
    'davlat', 'Tohiriylar', compare('Tohiriylar', 'Asoschisi', ['Tohir ibn Husayn', 'Poytaxt: Nishopur', '821-873'], 'Xususiyatlari', ['Xalifaga bo\'ysunish', 'Madaniyat rivoji', 'Mustaqillikka intilish']))
add('m24_25', 'Somoniylar', [('874', 'Nasr I Samarqandda'), ('892', 'Ismoil Somoniy'), ('900', 'Amr Safforiy mag\'lub'), ('943', 'Nuh I'), ('999', 'Qoraxoniylar')],
    'poytaxt', 'Somoniylar boshqaruvi', tree('Boshqaruv', 'Amir', [('Devon', 'Davlat idoralari'), ('Vazir', 'Bosh maslahatchi'), ('Poytaxt', 'Buxoro')]))
add('m26_27', 'Somoniylar iqtisodiyoti', [('IX asr', 'Dehqonchilik'), ('X asr', 'Hunarmandchilik'), ('X asr', 'Savdo'), ('Pul', 'Dirham zarbi'), ('Shaharlar', 'Buxoro, Samarqand')],
    'soha', 'Iqtisod', tree('Iqtisod', 'Somoniylar', [('Dehqonchilik', 'Sug\'orish'), ('Hunarmandchilik', 'To\'qimachilik, qog\'oz'), ('Savdo', 'Ipak yo\'li')]))
add('m28_29', 'G\'aznaviylar', [('962', 'Alptegin G\'aznada'), ('977', 'Sabuktegin'), ('998', 'Mahmud G\'aznaviy'), ('1030', 'Mahmud vafoti'), ('1040', 'Dandanakan jangi')],
    'jam', 'G\'aznaviylar davlati', tree('G\'aznaviylar', 'Davlat', [('Poytaxt', 'G\'azna'), ('Mahmud', 'Eng yirik hukmdor'), ('Madaniyat', 'Beruniy, Firdavsiy')]))
add('m30_31', 'Qoraxoniylar', [('999', 'Buxoroni oldilar'), ('XI asr', 'Qoraxoniylar'), ('1041', 'Ikki qismga bo\'linish'), ('1089', 'Saljuqlar qaram qildi'), ('1141', 'Qatvon jangi')],
    'bol', 'Qoraxoniylar bo\'linishi', compare('1041-yil', 'Sharqiy', ['Poytaxt: Bolasog\'un', 'Hukmdor: Arslon xon'], 'G\'arbiy', ['Poytaxt: Samarqand', 'Hukmdor: Ibrohim']))
add('m32_33', 'Saljuqiylar', [('1040', 'Dandanakan jangi'), ('1055', 'Tug\'rulbek Bag\'dodda'), ('1071', 'Malazgirt jangi'), ('1092', 'Nizomulmulk vafot'), ('1157', 'Sanjar vafoti')],
    'org', 'Saljuqiylar', tree('Saljuqiylar', 'Davlat', [('Tug\'rulbek', 'Asoschi'), ('Malikshoh', 'Qudratli davr'), ('Nizomulmulk', 'Vazir'), ('Sanjar', 'So\'nggi hukmdor')]))
add('m34_35', 'Xorazmshohlar', [('1077', 'Anushtegin'), ('1097', 'Qutbiddin Muhammad'), ('1172-1200', 'Takash'), ('1200-1220', 'Muhammad Xorazmshoh'), ('1220', 'Mo\'g\'ullar bosqini')],
    'jam', 'Xorazmshohlar davlati', flow('Yuksalish', [('Anushtegin', 'asos'), ('Otsiz', 'mustaqil'), ('Takash', 'kengayish'), ('Muhammad', 'qudrat'), ('1220', 'halokat')]))
add('m36_37', 'Xorazmshohlar boshqaruvi', [('XII asr', 'Sultonlik'), ('XIII asr', 'Qo\'shin'), ('Devon', 'Idoralar'), ('Soliq', 'Pul tizimi'), ('1220', 'Mo\'g\'ul bosqini')],
    'bosh', 'Davlat boshqaruvi', tree('Boshqaruv', 'Xorazmshoh', [('Devonlar', 'Idoralar'), ('Qo\'shin', 'Qipchoq harbiylar'), ('Soliq', 'Xiroj, jizya')]))
add('m38', 'O\'zbek xalqining shakllanishi', [('Qadimgi davr', 'Sak, So\'g\'d, Baqtriya'), ('VI asr', 'Turk qabilalari'), ('IX-XII', 'Turkiylashuv'), ('XIII asr', 'Mo\'g\'ullar'), ('XV asr', 'Oqibatda o\'zbek xalqi')],
    'etnos', 'Etnik asoslar', compare('Shakllanish', 'Mahalliy', ['Sak, So\'g\'d, Baqtriya', 'Xorazmliklar', 'Fors-tojik ildiz'], 'Turkiy', ['Qarluq, O\'g\'uz', 'Qipchoq, Turk', 'Tilda turkiylashuv']))
add('m39_40', 'Islom dinining yoyilishi', [('651', 'Eron'), ('712', 'Samarqand'), ('IX asr', 'Somoniylarda islom'), ('X asr', 'Qoraxoniylarda islom'), ('XI asr', 'Madrasa va masjid')],
    'jam', 'Islom tarqalishi', tree('Islom', 'Tarqalish omillari', [('Siyosat', 'Arab fathi'), ('Savdo', 'Savdogarlar'), ('Ta\'lim', 'Madrasalar')]))
add('m41_42', 'Ta\'lim', [('VII asr', 'Maktab'), ('IX asr', 'Madrasa'), ('X asr', 'Kutubxonalar'), ('XI asr', 'Nizomiya madrasasi'), ('XII asr', 'Buxoro madrasalari')],
    'dar', 'Ta\'lim bosqichlari', flow('Ta\'lim', [('Maktab', 'savod'), ('Madrasa', 'fan'), ('Ustoz', 'shogird'), ('Kitob', 'kutubxona'), ('Olim', 'ilm')]))
add('m43_44', 'Ma\'naviyat', [('IX asr', 'Imom Buxoriy'), ('IX asr', 'Termiziy'), ('X asr', 'Firdavsiy'), ('XI asr', 'Yassaviy'), ('XII asr', 'Najmiddin Kubro')],
    'azo', 'Mutafakkirlar', tree('Mutafakkirlar', 'Ma\'naviyat', [('Imom Buxoriy', 'Hadis ilmi'), ('Termiziy', 'Hadis'), ('Yassaviy', 'Tasavvuf'), ('Kubro', 'Tasavvuf')]))
add('m45_46', 'IX-XII asr ilm-fan', [('IX asr', 'Bag\'dod "Bilimlar uyi"'), ('IX asr', 'Al-Xorazmiy'), ('X asr', 'Forobiy'), ('XI asr', 'Beruniy, Ibn Sino'), ('XII asr', 'Zamaxshariy')],
    'olim', 'Olimlar va sohalar', tree('Olimlar', 'IX-XII asr', [('Al-Xorazmiy', 'Matematika'), ('Forobiy', 'Falsafa'), ('Beruniy', 'Astronomiya'), ('Ibn Sino', 'Tibbiyot')]))
add('m47_48', 'Al-Xorazmiy', [('~783', 'Tug\'ildi'), ('813-833', 'Ma\'mun davri'), ('820', 'Bilimlar uyi'), ('830', 'Algebra kitobi'), ('~850', 'Vafot etdi')],
    'asar', 'Al-Xorazmiy asarlari', tree('Asarlar', 'Al-Xorazmiy', [('Algebra', '"Al-jabr val-muqobala"'), ('Hind hisobi', 'Raqamlar'), ('Zij', 'Astronomik jadval'), ('Geografiya', '"Surat ul-arz"')]))
add('m49_50', 'Ahmad Farg\'oniy', [('~797', 'Tug\'ildi'), ('IX asr', 'Bag\'dodda'), ('861', 'Nil o\'lchovi'), ('IX asr', 'Astronomiya'), ('~861', 'Vafot etdi')],
    'asar', 'Farg\'oniy asarlari', tree('Asarlar', 'Ahmad Farg\'oniy', [('Astronomiya asoslari', 'Lotincha: Alfraganus'), ('Quyosh soatlari', 'Qurilma'), ('Nil o\'lchovi', 'Qohirada qurilgan')]))
add('m51_52', 'Forobiy', [('873', 'Tug\'ildi'), ('X asr', 'Bag\'dodda'), ('942', 'Damashq'), ('950', 'Vafot etdi'), ('Unvon', 'Ikkinchi muallim')],
    'asar', 'Forobiy ilmlari', tree('Forobiy', 'Ikkinchi muallim', [('Falsafa', 'Aristotelni sharhladi'), ('Musiqa', '"Katta musiqa kitobi"'), ('Mantiq', 'Ilmlarning tasnifi')]))
add('m53_54', 'Beruniy', [('973', 'Kat shahrida'), ('1017', 'G\'aznada'), ('1030', '"Hindiston"'), ('1048', 'Vafot etdi'), ('"Qonuni Mas\'udiy"', 'Astronomiya')],
    'asar', 'Beruniy asarlari', tree('Asarlar', 'Beruniy', [('Qadimgi xalqlardan', '"Osor ul-boqiya"'), ('Hindiston', 'Hindiston haqida'), ('Qonuni Mas\'udiy', 'Astronomiya'), ('Mineralogiya', 'Qimmatbaho toshlar')]))
add('m55_56', 'Ibn Sino', [('980', 'Afshonada tug\'ildi'), ('1005', 'Urganch'), ('1012', 'Hamadon'), ('1020', '"Tib qonunlari"'), ('1037', 'Vafot etdi')],
    'asar', 'Ibn Sino asarlari', tree('Asarlar', 'Ibn Sino', [('Tib qonunlari', 'Tibbiyot'), ('Kitob ush-shifo', 'Falsafa'), ('Donishnoma', 'Fors tilida')]))

inject('ozb7', I)
