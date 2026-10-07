# -*- coding: utf-8 -*-
"""Turk tili A2 (Yedi Iklim Turkce A2 mundarijasi asosida) to'liq kurs JSON'ini quradi.

MUHIM: turkcha matn to'g'ri imlo bilan (ç, ğ, ı, İ, ö, ş, ü harflari bilan) yoziladi -
A1 kursi bilan bir xil andozada (soddalashtirilgan/ASCII shakl EMAS).
"""
import json
import os

FORMAT_VERSION = 1


def block(heading, text):
    return {'heading': heading, 'text': text}


def fact(text, page=None):
    d = {'fact': text}
    if page is not None:
        d['page'] = page
    return d


def voc(tr, uz, ex_tr=None, ex_uz=None):
    d = {'tr': tr, 'uz': uz}
    if ex_tr:
        d['example_tr'] = ex_tr
    if ex_uz:
        d['example_uz'] = ex_uz
    return d


def mcq(question, options, correct_index, page=None):
    d = {'question': question, 'options': options, 'correct_index': correct_index}
    if page is not None:
        d['page'] = page
    return d


def choice(prompt, options, correct_index):
    return {'type': 'choice', 'prompt': prompt, 'options': options, 'correct_index': correct_index}


def order(prompt, words):
    return {'type': 'order', 'prompt': prompt, 'words': words}


def dialogue_line(speaker, text):
    return {'speaker': speaker, 'text': text}


def fill_blank(question, answer):
    return {'type': 'fill_blank', 'question': question, 'answer': answer}


def ordering(question, items):
    return {'type': 'ordering', 'question': question, 'items': items}


sections = []

# ============================================================
# 1-UNITE: ZAMAN-MEKAN
# ============================================================
sections.append({
    'key': 'u1', 'title': "1-ünite. Zaman-Mekân",
    'topics': [
        {
            'key': 'u1a', 'title': "A. Geçmiş, Şimdi, Gelecek — Belirsiz geçmiş zaman (-mış)",
            'start_page': 1, 'end_page': 1,
            'explanation': {
                'goals': [
                    "Belirsiz geçmiş zamanı (-mış) tanıyish va tushunish",
                    "-mış va -di (aniq geçmiş) orasidagi farqni bilish",
                ],
                'blocks': [
                    block(
                        "Belirsiz geçmiş zaman (-mış) nima?",
                        "Turkchada ikkita geçmiş zamon bor: **-di** (aniq geçmiş - siz o'zingiz "
                        "ko'rgan/bilgan voqea) va **-mış** (==belgisiz/eshitilgan geçmiş== - "
                        "boshqadan eshitgan, keyin bilib qolgan yoki taxmin qilingan voqea).\n\n"
                        "Solishtiring:\n"
                        "- **Ali geldi.** = Ali keldi (men o'zim ko'rdim/bilaman)\n"
                        "- **Ali gelmiş.** = Ali kelgan ekan (menga aytishdi, yoki keyin bilib qoldim)\n\n"
                        "**-mış** yana ==kutilmagan narsani anglab yetganda== ham ishlatiladi: "
                        "\"Saat çok geç olmuş!\" - \"Voy, vaqt juda kech bo'lib qolgan ekan!\".",
                    ),
                    block(
                        "Qo'shish qoidasi va tuslanishi",
                        "Fe'l tub + **-mış/-miş/-muş/-müş** (unli uyg'unligiga qarab) + shaxs "
                        "qo'shimchasi:\n\n"
                        "gel + miş -> **gelmişim** (kelgan ekanman), **gelmişsin**, **gelmiş**, "
                        "**gelmişiz**, **gelmişsiniz**, **gelmişler**.\n\n"
                        "Masalan: \"Ahmet dün bize gelmiş, ama biz evde yokmuşuz\" = \"Ahmet kecha "
                        "bizga kelgan ekan, lekin biz uyda yo'q ekanmiz\" - bu gap ikkalamiz ham "
                        "o'sha voqeani keyin bilib qolganimizni ko'rsatadi.",
                    ),
                ],
                'key_facts': [
                    fact("-di - aniq geçmiş (o'zi ko'rgan/bilgan), -mış - belgisiz geçmiş (eshitgan/bilib qolgan)."),
                    fact("-mış kutilmagan narsani endi anglab yetganda ham ishlatiladi."),
                ],
                'summary': "**-mış** = eshitgan yoki keyin bilib qolgan voqea uchun geçmiş zaman, "
                           "==-di (o'zi ko'rgan) dan farqli==.",
                'vocabulary': [
                    voc('geçmiş', "o'tmish", "Geçmişte burada bir kale varmış.", "O'tmishda bu yerda bir qal'a bo'lgan ekan."),
                    voc('şimdi', 'hozir', 'Şimdi ne yapıyorsun?', 'Hozir nima qilyapsan?'),
                    voc('gelecek', 'kelajak', 'Gelecekte doktor olmak istiyorum.', "Kelajakda shifokor bo'lishni xohlayman."),
                    voc('duymak', 'eshitmoq', 'Bu haberi dün duydum.', 'Bu xabarni kecha eshitdim.'),
                    voc('anlamak', 'tushunmoq', 'Şimdi anladım.', 'Endi tushundim.'),
                    voc('fark', 'farq', 'İki kelime arasında fark var.', "Ikki so'z orasida farq bor."),
                    voc('tanıdık', 'tanish (odam)', 'O benim eski bir tanıdığım.', 'U mening eski tanishim.'),
                    voc('haber', 'xabar', 'Haberi aldın mı?', 'Xabarni oldingmi?'),
                    voc('keşfetmek', 'kashf qilmoq', "Kolomb Amerika'yı keşfetti.", 'Kolumb Amerikani kashf qildi.'),
                    voc('meğer', 'chamasi (ekan)', 'Meğer çok yorgunmuş.', 'Chamasi, u juda charchagan ekan.'),
                    voc('şaşırmak', "hayron bo'lmoq", 'Çok şaşırdım.', "Juda hayron bo'ldim."),
                    voc('değişmek', "o'zgarmoq", 'Şehir çok değişmiş.', "Shahar juda o'zgargan ekan."),
                ],
                'listening': {
                    'dialogue': [
                        dialogue_line('Ayşe', "Duydun mu, eski komşumuz İstanbul'a taşınmış!"),
                        dialogue_line('Murat', 'Gerçekten mi? Ne zaman?'),
                        dialogue_line('Ayşe', 'Geçen ay taşınmış. Yeni bir işte çalışmaya başlamış.'),
                        dialogue_line('Murat', 'Vay, hiç haberim yoktu. Mutlu mu peki?'),
                        dialogue_line('Ayşe', "Çok mutluymuş, yeni şehri çok beğenmiş."),
                    ],
                    'questions': [
                        mcq("Komşuları nereye taşınmış?", ["İstanbul'a", "Ankara'ya", "İzmir'e", "Bursa'ya"], 0),
                        mcq('Bu bilgiyi Ayşe nasıl öğrenmiş?', ['Başkasından duyarak', "Kendi görerek", 'Mektup okuyarak', 'Televizyondan'], 0),
                    ],
                },
                'reading': {
                    'title': 'Eski Bir Şehir Efsanesi',
                    'text': "Rivayete göre, bu şehir çok eski zamanlarda küçük bir köymüş. Bir gün "
                            "buraya bir tüccar gelmiş ve altın bulmuş. Haber çabuk yayılmış, çok "
                            "insan buraya taşınmış. Zamanla köy büyümüş ve bugünkü şehir olmuş. "
                            "Kimse bu hikâyenin gerçek olup olmadığını bilmiyor, ama herkes anlatıyor.",
                    'questions': [
                        mcq('Şehir önce neymiş?', ['Küçük bir köy', 'Büyük bir şehir', 'Boş bir orman', 'Bir ada'], 0),
                        mcq('Tüccar ne bulmuş?', ['Altın', 'Su', 'Kitap', 'Hayvan'], 0),
                    ],
                },
                'sentence_practice': [
                    choice('"Ali geldi" ile "Ali gelmiş" arasındaki fark nedir?', [
                        '"Geldi" - görmüş, "gelmiş" - başkasından duymuş',
                        'Hiçbir fark yok', '"Gelmiş" gelecek zaman demek', '"Geldi" soru demek',
                    ], 0),
                    choice('"Saat çok geç ___ !" (fark etme anlamında)', ['olmuş', 'oldu', 'olacak', 'olur'], 0),
                    order("Kelimeleri doğru sıraya dizin: 'Ahmet dün bize gelmiş'", ['Ahmet', 'dün', 'bize', 'gelmiş']),
                    choice("'gel' fiiline -miş ekleyince 3. tekil şahıs nasıl olur?", ['gelmiş', 'gelmişim', 'gelmişsin', 'gelmişiz'], 0),
                    choice('Bir masal/hikâye anlatırken hangi zaman kullanılır?', ['-mış (belirsiz geçmiş)', '-di (aniq geçmiş)', '-ecek (gelecek)', '-iyor (şimdiki)'], 0),
                ],
                'writing_prompt': {
                    'instruction': "Ailenizden birinden duyduğunuz eski bir hikâyeyi -mış zamanını "
                                   "kullanarak 3-4 cümleyle yazın.",
                    'sample_answer': "Dedem küçükken bu köyde yaşarmış. O zamanlar burada hiç ev "
                                     "yokmuş, sadece tarlalar varmış. Dedem her gün okula çok uzak "
                                     "yürümüş. Sonra şehir büyümüş ve her şey değişmiş.",
                },
                'speaking_prompt': {
                    'sentences': [
                        'Geçen hafta arkadaşımdan ilginç bir haber duydum.',
                        'Meğer komşumuz yeni bir iş bulmuş.',
                        'Çocukken bu şehir çok küçükmüş.',
                    ],
                },
            },
            'test': [
                mcq('"-mış" eki hangi durumda kullanılır?', ['Başkasından duyulan/sonradan öğrenilen geçmiş için', 'Sadece gelecek zaman için', 'Sadece soru cümlelerinde', 'Sadece olumsuz cümlelerde'], 0),
                mcq('"Ali gelmiş" cümlesinin anlamı nedir?', ["Ali'nin geldiğini sonradan öğrendim", "Ali'nin geldiğini kendim gördüm", 'Ali gelecek', 'Ali gelmiyor'], 0),
                mcq('Masallar genellikle hangi zamanla anlatılır?', ['-mış (belirsiz geçmiş)', '-iyor (şimdiki zaman)', '-ecek (gelecek zaman)', 'Emir kipi'], 0),
                mcq('"gel" + miş + 1. tekil şahıs (ben) nasıl olur?', ['gelmişim', 'gelmişsin', 'gelmiş', 'gelmişiz'], 0),
                mcq("'Meğer' kelimesinin anlamı nedir?", ["Chamasi, ma'lum bo'lishicha", "Albatta", "Hech qachon", "Tez orada"], 0),
                mcq("'Haber' so'zi o'zbekchada nima?", ['Xabar', "Kitob", "Uy", "Kecha"], 0),
                fill_blank('"Ali dün bize gel___" (başkasından duyulan geçmiş, 3. tekil şahıs)', 'gelmiş'),
                ordering("Cümleyi doğru sıraya dizin: 'Komşumuz İstanbul'a taşınmış'", ["Komşumuz", "İstanbul'a", 'taşınmış']),
            ],
        },
    ],
})

sections[0]['topics'].append({
    'key': 'u1b', 'title': "B. Zaman Planlaması — -DAn önce / -DAn sonra",
    'start_page': 2, 'end_page': 2,
    'explanation': {
        'goals': ["-DAn önce va -DAn sonra qo'shimchalarini o'rganish", "Kun tartibi haqida gapirishni bilish"],
        'blocks': [
            block(
                "-DAn önce / -DAn sonra",
                "Bu ikki qo'shimcha **ot (narsa/vaqt)** dan keyin qo'shiladi va \"NARSAdan oldin\" / "
                "\"NARSAdan keyin\" degan ma'noni beradi:\n\n"
                "- **Dersten önce** = darsdan oldin\n"
                "- **Yemekten sonra** = ovqatdan keyin\n"
                "- **Saat beşten önce** = soat beshdan oldin\n\n"
                "Diqqat: bu -DAn qo'shimchasi (chiqish kelishigi, o'zbekcha \"-dan\"ga o'xshash) + "
                "**önce/sonra** so'zlaridan iborat - ==fe'lga emas, otga qo'shiladi==.",
            ),
            block(
                "Kun tartibini tasvirlash",
                "Bu qurilma kundalik reja haqida gapirishda juda foydali: \"İşten önce spor "
                "yaparım\" (ishdan oldin sport qilaman), \"Akşamdan sonra kitap okurum\" "
                "(kechqurundan keyin kitob o'qiyman). Vaqt ifodalarini tartib bilan aytish - "
                "A2 darajasida muhim ko'nikma.",
            ),
        ],
        'key_facts': [
            fact("-DAn önce = otdan oldin, -DAn sonra = otdan keyin."),
            fact("Bu qo'shimcha otga (ism) qo'shiladi, fe'lga emas."),
        ],
        'summary': "**-DAn önce** (oldin) va **-DAn sonra** (keyin) - otlarga qo'shilib, vaqt tartibini bildiradi.",
        'vocabulary': [
            voc('önce', 'oldin', 'Dersten önce kahvaltı yaparım.', 'Darsdan oldin nonushta qilaman.'),
            voc('sonra', 'keyin', 'İşten sonra eve giderim.', 'Ishdan keyin uyga ketaman.'),
            voc('gün', 'kun', 'Günüm çok yoğun.', 'Kunim juda band.'),
            voc('kahvaltı', 'nonushta', 'Kahvaltımı yaptım.', 'Nonushtamni qildim.'),
            voc('öğle yemeği', 'tushlik', 'Öğle yemeğini birlikte yiyelim.', 'Tushlikni birga yeylik.'),
            voc('akşam', 'kechqurun', 'Akşam ne yapıyorsun?', 'Kechqurun nima qilasan?'),
            voc('toplantı', "yig'ilish", 'Saat üçte bir toplantım var.', "Soat uchda yig'ilishim bor."),
            voc('randevu', 'uchrashuv', 'Doktordan randevu aldım.', 'Shifokordan uchrashuv oldim.'),
            voc('erken', 'erta', 'Erken kalkarım.', 'Erta turaman.'),
            voc('geç', 'kech', 'Geç yattım.', 'Kech yotdim.'),
            voc('yoğun', "band (mashg'ul)", 'Bu hafta çok yoğunum.', "Bu hafta juda bandman."),
        ],
        'listening': {
            'dialogue': [
                dialogue_line('Elif', 'Yarın çok yoğun bir günün var mı?'),
                dialogue_line('Kaan', 'Evet, işten önce spor yapacağım, sonra toplantım var.'),
                dialogue_line('Elif', 'Toplantıdan sonra ne yapacaksın?'),
                dialogue_line('Kaan', 'Öğle yemeğinden sonra doktora gideceğim.'),
            ],
            'questions': [
                mcq("Kaan işten önce ne yapacak?", ['Spor yapacak', 'Uyuyacak', 'Kitap okuyacak', 'Yemek yiyecek'], 0),
                mcq('Kaan ne zaman doktora gidecek?', ["Öğle yemeğinden sonra", "Sabah erken", 'Akşamdan önce', 'Toplantıdan önce'], 0),
            ],
        },
        'reading': {
            'title': 'Benim Günüm',
            'text': "Her sabah kahvaltıdan önce yürüyüş yaparım. Kahvaltıdan sonra işe giderim. "
                    "Öğle yemeğinden önce biraz çalışırım, yemekten sonra toplantılara katılırım. "
                    "Akşam işten sonra ailemle vakit geçirmeyi severim.",
            'questions': [
                mcq('Kahvaltıdan önce ne yapıyor?', ['Yürüyüş', 'Toplantı', 'Ders', 'Uyku'], 0),
                mcq('Akşam işten sonra ne yapıyor?', ['Ailesiyle vakit geçiriyor', 'Yürüyüş yapıyor', 'Toplantıya gidiyor', 'Kahvaltı yapıyor'], 0),
            ],
        },
        'sentence_practice': [
            choice("'Dersten ___ kahvaltı yaparım' (darsdan OLDIN)", ['önce', 'sonra', 'için', 'gibi'], 0),
            choice("'Yemek___ sonra dişlerimi fırçalarım'", ['ten', 'tan', 'dan', 'den'], 0),
            order("Kelimeleri doğru sıraya dizin: 'İşten önce spor yaparım'", ['İşten', 'önce', 'spor', 'yaparım']),
            choice("'Toplantıdan ___ eve gittim' (yig'ilishdan KEYIN)", ['sonra', 'önce', 'ile', 'için'], 0),
        ],
        'writing_prompt': {
            'instruction': "-DAn önce va -DAn sonra qo'shimchalarini ishlatib, o'z kun tartibingizni 3-4 gapda yozing.",
            'sample_answer': "Kahvaltıdan önce spor yaparım. Kahvaltıdan sonra derslere giderim. "
                             "Derslerden sonra ev ödevimi yaparım. Akşam yemeğinden önce biraz dinlenirim.",
        },
        'speaking_prompt': {'sentences': ['İşten önce spor yaparım.', 'Yemekten sonra dişlerimi fırçalarım.', 'Toplantıdan önce hazırlanırım.']},
    },
    'test': [
        mcq("'-DAn önce' qo'shimchasi nimani bildiradi?", ["Otdan oldin", "Otdan keyin", "Ot bilan", "Ot uchun"], 0),
        mcq("'-DAn sonra' qo'shimchasi nimani bildiradi?", ["Otdan keyin", "Otdan oldin", "Ot bilan", "Ot uchun"], 0),
        mcq("'Dersten önce' iborasi qanday tarjima qilinadi?", ["Darsdan oldin", "Darsdan keyin", "Dars bilan", "Dars uchun"], 0),
        mcq("Bu qo'shimcha nimaga qo'shiladi?", ["Otga (ism)", "Faqat fe'lga", "Faqat sifatga", "Faqat songa"], 0),
        mcq("'Yemekten sonra' qanday tarjima qilinadi?", ["Ovqatdan keyin", "Ovqatdan oldin", "Ovqat bilan", "Ovqatsiz"], 0),
        mcq("'Kahvaltı' so'zi nima?", ["Nonushta", "Tushlik", "Kechki ovqat", "Choy"], 0),
        fill_blank("'İşten ___ spor yaparım' (ishdan OLDIN)", 'önce'),
        ordering("Cümleyi doğru sıraya dizin: 'Öğle yemeğinden sonra doktora gideceğim'", ['Öğle', 'yemeğinden', 'sonra', 'doktora', 'gideceğim']),
    ],
})

sections[0]['topics'].append({
    'key': 'u1c', 'title': "C. Farklı Şehirler, Farklı Hayatlar — -mAdAn önce / -DIktAn sonra",
    'start_page': 3, 'end_page': 3,
    'explanation': {
        'goals': ["-mAdAn önce (fe'lga qo'shilib 'qilishdan oldin') qurilmasini o'rganish",
                  "-DIktAn sonra (fe'lga qo'shilib 'qilgandan keyin') qurilmasini o'rganish"],
        'blocks': [
            block(
                "-mAdAn önce: 'qilishdan oldin'",
                "1B'da o'rgangan **-DAn önce** OTGA qo'shilardi. Endi FE'LGA qo'shiladigan "
                "shaklni ko'ramiz: fe'l tub + **-madan/-meden** + önce = \"...qilishdan oldin\":\n\n"
                "- **Yemek yemeden önce ellerini yıka.** = Ovqat yeishdan oldin qo'lingni yuv.\n"
                "- **Çıkmadan önce kapıyı kilitle.** = Chiqishdan oldin eshikni qulfla.\n\n"
                "Diqqat: bu yerda **olumsuz (-ma/-me) shakl + önce** ishlatiladi, lekin ma'no "
                "==olumsuz emas== - bu shunchaki qurilmaning o'zi shunday.",
            ),
            block(
                "-DIktAn sonra: 'qilgandan keyin'",
                "Fe'l tub + **-dıktan/-dikten/-duktan/-dükten** (undosh va unli uyg'unligi) + "
                "sonra = \"...qilgandan keyin\":\n\n"
                "- **Yemek yedikten sonra dişlerini fırçala.** = Ovqat yegandan keyin tishingni "
                "yuv.\n"
                "- **İş bitirdikten sonra eve gideriz.** = Ishni tugatgandan keyin uyga ketamiz.\n\n"
                "Solishtiring: **-mAdAn önce** (qilishdan OLDIN) va **-DIktAn sonra** (qilgandan "
                "KEYIN) - ikkalasi ham FE'LGA qo'shiladi, ==-DAn önce/sonra esa OTGA==.",
            ),
        ],
        'key_facts': [
            fact("-mAdAn önce = fe'lga qo'shilib 'qilishdan oldin'."),
            fact("-DIktAn sonra = fe'lga qo'shilib 'qilgandan keyin'."),
            fact("-DAn önce/sonra - otga, -mAdAn önce / -DIktAn sonra - fe'lga qo'shiladi."),
        ],
        'summary': "Fe'lga qo'shiladi: **-mAdAn önce** (qilishdan oldin), **-DIktAn sonra** (qilgandan keyin).",
        'vocabulary': [
            voc('yıkamak', 'yuvmoq', 'Ellerini yıka.', "Qo'lingni yuv."),
            voc('kilitlemek', 'qulflamoq', 'Kapıyı kilitle.', 'Eshikni qulfla.'),
            voc('fırçalamak', "cho'tkalamoq", 'Dişlerini fırçala.', "Tishingni yuv (cho'tkala)."),
            voc('bitirmek', 'tugatmoq', 'İşimi bitirdim.', 'Ishimni tugatdim.'),
            voc('başlamak', 'boshlamoq', 'Derse başladık.', 'Darsni boshladik.'),
            voc('hazırlanmak', "tayyorgarlik ko'rmoq", 'Sınava hazırlanıyorum.', "Imtihonga tayyorgarlik ko'ryapman."),
            voc('çıkmak', 'chiqmoq', 'Evden çıktım.', 'Uydan chiqdim.'),
            voc('girmek', 'kirmoq', 'İçe girdi.', 'Ichkariga kirdi.'),
            voc('uyumak', 'uxlamoq', 'Erken uyudum.', 'Erta uxladim.'),
            voc('uyanmak', "uyg'onmoq", 'Sabah uyandım.', "Ertalab uyg'ondim."),
        ],
        'listening': {
            'dialogue': [
                dialogue_line('Anne', "Yemek yemeden önce ellerini yıkadın mı?"),
                dialogue_line('Çocuk', 'Evet anne, yıkadım.'),
                dialogue_line('Anne', 'Peki, yemek yedikten sonra ne yapacaksın?'),
                dialogue_line('Çocuk', 'Ödevimi bitirdikten sonra oyun oynayacağım.'),
            ],
            'questions': [
                mcq('Çocuk ne zaman ellerini yıkadı?', ['Yemekten önce', 'Yemekten sonra', 'Uyumadan önce', 'Okula giderken'], 0),
                mcq('Çocuk ödevini bitirdikten sonra ne yapacak?', ['Oyun oynayacak', 'Uyuyacak', 'Yemek yiyecek', 'Okula gidecek'], 0),
            ],
        },
        'reading': {
            'title': 'Günlük Alışkanlıklar',
            'text': "Uyandıktan sonra önce yüzümü yıkarım. Kahvaltı yapmadan önce dişimi "
                    "fırçalarım. İşten çıkmadan önce masamı düzenlerim. Eve geldikten sonra "
                    "biraz dinlenirim.",
            'questions': [
                mcq('Uyandıktan sonra ilk ne yapıyor?', ['Yüzünü yıkıyor', 'Kahvaltı yapıyor', 'İşe gidiyor', 'Uyuyor'], 0),
                mcq('İşten çıkmadan önce ne yapıyor?', ['Masasını düzenliyor', 'Uyuyor', 'Yemek yiyor', 'Dişini fırçalıyor'], 0),
            ],
        },
        'sentence_practice': [
            choice("'Yemek ye___ önce ellerini yıka' (fe'lga OLDIN qurilmasi)", ['meden', 'dikten', 'den', 'diği'], 0),
            choice("'İş bitir___ sonra eve gideriz' (fe'lga KEYIN qurilmasi)", ['dikten', 'meden', 'den', 'diği'], 0),
            order("Cümleyi doğru sıraya dizin: 'Dişlerini fırçaladıktan sonra uyu'", ['Dişlerini', 'fırçaladıktan', 'sonra', 'uyu']),
            choice("'-mAdAn önce' va '-DAn önce' orasidagi farq nima?", ["Birinchisi fe'lga, ikkinchisi otga qo'shiladi", "Hech qanday farq yo'q", "Ikkalasi ham otga qo'shiladi", "Ikkalasi ham fe'lga qo'shiladi"], 0),
        ],
        'writing_prompt': {
            'instruction': "-mAdAn önce va -DIktAn sonra qurilmalarini ishlatib, o'zingizning ertalabki odatlaringiz haqida 3 gap yozing.",
            'sample_answer': "Uyandıktan sonra önce su içerim. Kahvaltı yapmadan önce yüzümü yıkarım. "
                             "Kahvaltı yaptıktan sonra derslere giderim.",
        },
        'speaking_prompt': {'sentences': ['Yemek yemeden önce ellerimi yıkarım.', 'Uyumadan önce kitap okurum.', 'İşi bitirdikten sonra dinlenirim.']},
    },
    'test': [
        mcq("'-mAdAn önce' qanday ma'no beradi?", ["...qilishdan oldin", "...qilgandan keyin", "...qilish bilan", "...qilish uchun"], 0),
        mcq("'-DIktAn sonra' qanday ma'no beradi?", ["...qilgandan keyin", "...qilishdan oldin", "...qilish bilan", "...qilish uchun"], 0),
        mcq("'Yemek yemeden önce' qanday tarjima qilinadi?", ["Ovqat yeishdan oldin", "Ovqat yegandan keyin", "Ovqat yeyish bilan", "Ovqatsiz"], 0),
        mcq("Bu ikki qurilma nimaga qo'shiladi?", ["Fe'lga", "Faqat otga", "Faqat sifatga", "Faqat songa"], 0),
        mcq("'-DAn önce/sonra' (1B) va '-mAdAn önce/-DIktAn sonra' (1C) orasidagi asosiy farq nima?", ["Biri otga, ikkinchisi fe'lga qo'shiladi", "Hech qanday farq yo'q", "Ikkalasi bir xil ma'noda", "Biri savol, ikkinchisi javob"], 0),
        mcq("'Yıkamak' fe'li nima?", ["Yuvmoq", "Kirmoq", "Chiqmoq", "Uxlamoq"], 0),
        fill_blank("'İş bitir___ sonra eve gideriz' (fe'lga qo'shiluvchi shakl)", 'dikten'),
        ordering("Cümleyi doğru sıraya dizin: 'Ellerini yıkamadan önce yemek yeme'", ['Ellerini', 'yıkamadan', 'önce', 'yemek', 'yeme']),
    ],
})

# ============================================================
# 2-UNITE: SAGLIKLI YASAM
# ============================================================
sections.append({'key': 'u2', 'title': "2-ünite. Sağlıklı Yaşam", 'topics': []})

sections[1]['topics'].append({
    'key': 'u2a', 'title': "A. Her Şeyin Başı Sağlık", 'start_page': 4, 'end_page': 4,
    'explanation': {
        'goals': ["Sog'liq va kasallik haqida so'zlashishni o'rganish", "Shifokorga borish vaziyatida muloqot qilish"],
        'blocks': [
            block(
                "Sağlık - eng muhim boylik",
                "Turk madaniyatida \"Sağlık olmadan hiçbir şey olmaz\" (Sog'liqsiz hech narsa "
                "bo'lmaydi) degan naql juda mashhur - shuning uchun bu darsning nomi \"**Her şeyin "
                "başı sağlık**\" (Hamma narsaning boshi - sog'liq). Bu darsda tana a'zolari, "
                "kasallik alomatlari va shifokorga murojaat qilish iboralari bilan tanishasiz.",
            ),
            block(
                "Shifokorga borganda ishlatiladigan iboralar",
                "- **Neyiniz var?** = Sizga nima bo'ldi? (shifokor so'raydi)\n"
                "- **Başım ağrıyor.** = Boshim og'riyapti.\n"
                "- **Ateşim var.** = Isitmam bor.\n"
                "- **Kendimi iyi hissetmiyorum.** = O'zimni yaxshi his qilmayapman.\n\n"
                "==\"Ağrımak\" (og'rimoq)== fe'li tana a'zosi + -ım/-im agriyor shaklida "
                "ishlatiladi: başım ağrıyor, karnım ağrıyor, boğazım ağrıyor.",
            ),
        ],
        'key_facts': [
            fact("'Neyiniz var?' - shifokorning odatiy savoli."), fact("'[Tana a'zosi] ağrıyor' - og'riq bildirish qurilmasi."),
        ],
        'summary': "Sog'liq mavzusida asosiy qurilma: **[tana a'zosi] + ağrıyor** (og'riyapti).",
        'vocabulary': [
            voc('sağlık', "sog'liq", 'Sağlık çok önemli.', "Sog'liq juda muhim."),
            voc('hasta', 'bemor/kasal', 'Hasta oldum.', 'Kasal bo\'lib qoldim.'),
            voc('ağrı', "og'riq", "Başımda ağrı var.", "Boshimda og'riq bor."),
            voc('ateş', 'isitma', 'Ateşim yükseldi.', "Isitmam ko'tarildi."),
            voc('doktor', 'shifokor', 'Doktora gittim.', 'Shifokorga bordim.'),
            voc('ilaç', 'dori', 'İlaç aldım.', 'Dori oldim.'),
            voc('baş', 'bosh', 'Başım ağrıyor.', "Boshim og'riyapti."),
            voc('karın', 'qorin', 'Karnım ağrıyor.', "Qornim og'riyapti."),
            voc('boğaz', 'tomoq', 'Boğazım ağrıyor.', "Tomog'im og'riyapti."),
            voc('geçmiş olsun', "tuzalib keting", 'Geçmiş olsun!', "Tuzalib keting!"),
            voc('iyileşmek', 'tuzalmoq', 'Çabuk iyileştim.', 'Tez tuzaldim.'),
        ],
        'listening': {
            'dialogue': [
                dialogue_line('Doktor', 'Merhaba, neyiniz var?'),
                dialogue_line('Hasta', 'Başım ağrıyor ve ateşim var.'),
                dialogue_line('Doktor', 'Boğazınızda da ağrı var mı?'),
                dialogue_line('Hasta', 'Evet, biraz var.'),
                dialogue_line('Doktor', 'Size ilaç yazacağım, geçmiş olsun.'),
            ],
            'questions': [
                mcq('Hastanın şikâyeti nedir?', ["Baş ağrısı ve ateş", "Karın ağrısı", 'Diş ağrısı', 'Göz ağrısı'], 0),
                mcq('Doktor ne yapacak?', ["İlaç yazacak", 'Ameliyat yapacak', 'Hiçbir şey yapmayacak', 'Hastaneye yatıracak'], 0),
            ],
        },
        'reading': {
            'title': 'Sağlıklı Kalmanın Yolları',
            'text': "Sağlıklı kalmak için düzenli spor yapmak, sağlıklı beslenmek ve yeterince "
                    "uyumak gerekir. Her gün bol su içmek de çok önemlidir. Hasta olduğunuzda "
                    "dinlenmeli ve gerekirse doktora gitmelisiniz.",
            'questions': [
                mcq('Sağlıklı kalmak için ne yapmak gerekir?', ['Spor, sağlıklı beslenme, uyku', 'Sadece uyumak', 'Sadece spor', 'Hiçbir şey'], 0),
                mcq('Hasta olduğunuzda ne yapmalısınız?', ['Dinlenmeli ve doktora gitmeli', "Spor yapmaya devam etmeli", "Hiçbir şey yapmamalı", "Sadece uyumamalı"], 0),
            ],
        },
        'sentence_practice': [
            choice("'Baş___ ağrıyor' (bosh og'riyapti)", ['ım', 'ın', 'ı', 'ımız'], 0),
            choice("Shifokor 'Neyiniz var?' deganda nimani so'raydi?", ["Sizga nima bo'lganini", "Ismingizni", "Yoshingizni", "Uyingiz qayerda ekanini"], 0),
            order("Cümleyi doğru sıraya dizin: 'Başım ağrıyor ve ateşim var'", ['Başım', 'ağrıyor', 've', 'ateşim', 'var']),
            choice("'Geçmiş olsun' qachon aytiladi?", ["Kasal odamga", "Bayramda", "Xayrlashganda", "Tabriklaganda"], 0),
        ],
        'writing_prompt': {
            'instruction': "Shifokorga bemor sifatida murojaat qilib, sog'liq shikoyatingizni 3 gapda yozing.",
            'sample_answer': "Merhaba doktor bey. İki gündür başım ağrıyor ve ateşim var. Ayrıca "
                             "boğazım da ağrıyor. Bana ilaç verebilir misiniz?",
        },
        'speaking_prompt': {'sentences': ['Başım ağrıyor.', 'Ateşim var.', 'Kendimi iyi hissetmiyorum.']},
    },
    'test': [
        mcq("'Neyiniz var?' iborasi nima uchun ishlatiladi?", ["Shifokor bemordan shikoyatini so'raganda", "Salomlashganda", "Xayrlashganda", "Taom buyurtma qilganda"], 0),
        mcq("'Başım ağrıyor' qanday tarjima qilinadi?", ["Boshim og'riyapti", "Qornim og'riyapti", "Men yaxshiman", "Men kasalman"], 0),
        mcq("'Ateş' so'zi qaysi ma'noda ishlatilgan?", ["Isitma (tana harorati)", "Olov", "Rang", "Ovqat"], 0),
        mcq("'Geçmiş olsun' nimani anglatadi?", ["Tuzalib keting (tilak)", "Xayr", "Rahmat", "Kechirasiz"], 0),
        mcq("Sog'liqni saqlash uchun nima tavsiya etiladi?", ["Spor, to'g'ri ovqatlanish, uyqu", "Faqat uxlash", "Faqat sport", "Hech narsa qilmaslik"], 0),
        fill_blank("'Boğaz___ ağrıyor' (tomoq og'riyapti)", 'ım'),
    ],
})

sections[1]['topics'].append({
    'key': 'u2b', 'title': "B. Dünyamız Kirleniyor — Pekiştirme, gibi, kadar",
    'start_page': 5, 'end_page': 5,
    'explanation': {
        'goals': ["Pekiştirme (kuchaytirish) shaklini o'rganish", "'gibi' va 'kadar' qo'shimchalarini bilish", "Atrof-muhit lug'atini o'zlashtirish"],
        'blocks': [
            block(
                "Pekiştirme (kuchaytirish shakli)",
                "Turkchada sifatni **kuchaytirish** uchun maxsus usul bor: sifatning birinchi "
                "bo'g'inini olib, oxiriga **p, s, m yoki r** undoshlaridan birini qo'shib, keyin "
                "sifatning o'zini takrorlaysiz:\n\n"
                "- **temiz** (toza) -> **tertemiz** (chippa-chiroq toza)\n"
                "- **kara** (qora) -> **kapkara** (qop-qora)\n"
                "- **yeşil** (yashil) -> **yemyeşil** (yam-yashil)\n"
                "- **beyaz** (oq) -> **bembeyaz** (oppoq)\n\n"
                "Bu shakl o'zbekchadagi \"qop-qora\", \"yam-yashil\" kabi kuchaytirilgan "
                "sifatlarga juda o'xshash!",
            ),
            block(
                "'gibi' (kabi/dek) va 'kadar' (qadar/gacha)",
                "**gibi** = \"kabi, -dek\" (o'xshatish): \"Deniz gibi mavi\" = Dengizdek ko'k.\n\n"
                "**kadar** = ikki xil ma'noda ishlatiladi:\n"
                "1. O'xshatish/daraja: \"Deniz kadar mavi\" = Dengiz qadar ko'k\n"
                "2. Vaqt chegarasi \"...gacha\": \"Akşama kadar çalışırım\" = Kechgacha ishlayman\n\n"
                "Bu ikkala qo'shimcha ham atrof-muhit haqida ta'sirli tasvirlar yaratishda juda "
                "foydali: \"Hava kar kadar beyaz\", \"Nehir çöp kadar kirli\" kabi.",
            ),
        ],
        'key_facts': [
            fact("Pekiştirme - sifatni kuchaytirish (tertemiz, kapkara, yemyeşil)."),
            fact("gibi = kabi/dek (o'xshatish)."), fact("kadar = qadar (daraja) yoki gacha (vaqt chegarasi)."),
        ],
        'summary': "**Pekiştirme** (tertemiz, kapkara) - kuchaytirish; **gibi/kadar** - o'xshatish va chegara bildiradi.",
        'vocabulary': [
            voc('dünya', 'dunyo', 'Dünyamız kirleniyor.', 'Dunyomiz ifloslanmoqda.'),
            voc('kirlenmek', 'ifloslanmoq', 'Hava kirleniyor.', 'Havo ifloslanmoqda.'),
            voc('çevre', 'atrof-muhit', 'Çevreyi korumalıyız.', 'Atrof-muhitni asrashimiz kerak.'),
            voc('çöp', 'chiqindi', 'Çöpü yere atma.', "Chiqindini yerga tashlama."),
            voc('geri dönüşüm', 'qayta ishlash', 'Geri dönüşüm önemli.', 'Qayta ishlash muhim.'),
            voc('orman', "o'rmon", 'Ormanlar azalıyor.', "O'rmonlar kamaymoqda."),
            voc('temiz', 'toza', 'Temiz hava önemli.', 'Toza havo muhim.'),
            voc('kirli', 'iflos', 'Bu nehir çok kirli.', 'Bu daryo juda iflos.'),
            voc('korumak', 'asramoq/saqlamoq', 'Doğayı korumalıyız.', 'Tabiatni asrashimiz kerak.'),
        ],
        'listening': {
            'dialogue': [
                dialogue_line('Öğretmen', "Çocuklar, dünyamız neden kirleniyor?"),
                dialogue_line('Öğrenci', "Çöp yere atıldığı için, öğretmenim."),
                dialogue_line('Öğretmen', 'Doğru! Ormanlar da ağaç gibi değil, kapkara duman içinde.'),
                dialogue_line('Öğrenci', 'Geri dönüşüm yapmalıyız!'),
            ],
            'questions': [
                mcq('Öğrenciye göre dünya neden kirleniyor?', ["Çöp yere atıldığı için", 'Çok yağmur yağdığı için', 'Çok soğuk olduğu için', 'Çok insan olduğu için'], 0),
                mcq('Çözüm olarak ne teklif edildi?', ['Geri dönüşüm', 'Daha çok çöp atmak', 'Ormanları kesmek', 'Hiçbir şey yapmamak'], 0),
            ],
        },
        'reading': {
            'title': 'Temiz Bir Dünya İçin',
            'text': "Eskiden nehirlerimiz tertemizdi, gökyüzü bembeyaz bulutlarla doluydu. Şimdi "
                    "ise fabrikalar yüzünden hava kapkara dumanla doluyor. Nehirler çöp kadar "
                    "kirli hale geldi. Ama geç değil - geri dönüşüm yaparak ve ağaç dikerek "
                    "dünyamızı tekrar yemyeşil yapabiliriz.",
            'questions': [
                mcq('Eskiden nehirler nasılmış?', ["Tertemiz", "Kapkara", 'Kirli', "Kuru"], 0),
                mcq("Yazara göre dünyayı nasıl kurtarabiliriz?", ['Geri dönüşüm ve ağaç dikişle', 'Hiçbir şey yapmadan', 'Daha çok fabrika açarak', "Ormanları keserek"], 0),
            ],
        },
        'sentence_practice': [
            choice("'temiz' so'zining kuchaytirilgan (pekiştirme) shakli qaysi?", ['tertemiz', 'temizkiz', 'temizmiz', 'temizler'], 0),
            choice("'kara' so'zining kuchaytirilgan shakli qaysi?", ['kapkara', 'karakiz', 'karamış', 'karalar'], 0),
            choice("'Deniz ___ mavi' (dengizdek ko'k, o'xshatish)", ['gibi', 'kadar', 'için', 'ile'], 0),
            choice("'Akşama ___ çalışırım' (kechgacha, vaqt chegarasi)", ['kadar', 'gibi', 'önce', 'sonra'], 0),
        ],
        'writing_prompt': {
            'instruction': "Pekiştirme shaklini (masalan tertemiz, kapkara) ishlatib, atrof-muhit haqida 3 gap yozing.",
            'sample_answer': "Eskiden köyümüzdeki nehir tertemizdi. Şimdi fabrikalar yüzünden "
                             "kapkara oldu. Umarım yakında tekrar yemyeşil bir dünyada yaşarız.",
        },
        'speaking_prompt': {'sentences': ["Dünyamız kirleniyor.", 'Çevreyi korumalıyız.', 'Geri dönüşüm önemlidir.']},
    },
    'test': [
        mcq("'Pekiştirme' nima?", ["Sifatni kuchaytirish shakli", "Fe'lni kelasi zamonga o'tkazish", "Otni ko'plikka aylantirish", "Savol yasash usuli"], 0),
        mcq("'temiz' so'zining kuchaytirilgan shakli qaysi?", ['tertemiz', 'temizsiz', 'temizlik', 'temizdi'], 0),
        mcq("'gibi' so'zi qanday ma'no beradi?", ["Kabi/dek (o'xshatish)", "Bilan", "Uchun", "Ichida"], 0),
        mcq("'kadar' so'zining ikkinchi ma'nosi (vaqt bilan) nima?", ["...gacha", "...dan keyin", "...bilan birga", "...ostida"], 0),
        mcq("'yeşil' so'zining kuchaytirilgan shakli qaysi?", ['yemyeşil', 'yeşilkiz', 'yeşilmiş', 'yeşillik'], 0),
        mcq("'Geri dönüşüm' nima?", ["Qayta ishlash", "Chiqindi tashlash", "Suv ichish", "Daraxt kesish"], 0),
        fill_blank("'beyaz' (oq) so'zining kuchaytirilgan (pekiştirme) shakli", 'bembeyaz'),
    ],
})

sections[1]['topics'].append({
    'key': 'u2c', 'title': "C. Trafik Canavarı", 'start_page': 6, 'end_page': 6,
    'explanation': {
        'goals': ["Yo'l harakati xavfsizligi lug'atini o'rganish", "Transport va qoidalar haqida gapirish"],
        'blocks': [
            block(
                "Trafik canavarı nima?",
                "\"**Trafik canavarı**\" (yo'l harakati yirtqichi) - tez haydash, qoidalarni "
                "buzish natijasida yuz beradigan baxtsiz hodisalarga nisbatan ishlatiladigan "
                "obrazli ibora. Bu darsda yo'l harakati xavfsizligi va transport lug'ati bilan "
                "tanishasiz.",
            ),
            block(
                "Muhim qoidalar va iboralar",
                "- **Kırmızı ışıkta dur!** = Qizil chiroqda to'xta!\n"
                "- **Emniyet kemerini tak.** = Xavfsizlik kamarini tak.\n"
                "- **Hız limitine uy.** = Tezlik chegarasiga rioya qil.\n"
                "- **Yaya geçidinden geç.** = Piyodalar o'tish joyidan o't.\n\n"
                "Bu iboralar barchasi ==buyruq maylida (emir kipi)== berilgan - xavfsizlik "
                "qoidalari ko'pincha shu tarzda ifodalanadi.",
            ),
        ],
        'key_facts': [
            fact("'Trafik canavarı' - qoida buzilishi natijasidagi baxtsiz hodisalarga ishora."),
            fact("Xavfsizlik qoidalari ko'pincha buyruq maylida (emir kipi) beriladi."),
        ],
        'summary': "Yo'l xavfsizligi lug'ati: **kırmızı ışık, emniyet kemeri, hız limiti, yaya geçidi**.",
        'vocabulary': [
            voc('trafik', "yo'l harakati", "Trafik çok yoğun.", "Yo'l harakati juda band."),
            voc('kaza', "baxtsiz hodisa", "Kaza oldu.", "Baxtsiz hodisa yuz berdi."),
            voc('hız', 'tezlik', 'Hızını azalt.', 'Tezligingni kamaytir.'),
            voc('ışık', "chiroq (svetofor)", "Kırmızı ışıkta durduk.", "Qizil chiroqda to'xtadik."),
            voc('emniyet kemeri', 'xavfsizlik kamari', "Emniyet kemerini tak.", 'Xavfsizlik kamarini tak.'),
            voc('yaya', 'piyoda', 'Yayalar dikkatli olmalı.', "Piyodalar ehtiyot bo'lishi kerak."),
            voc('sürücü', "haydovchi", "Sürücü çok dikkatliydi.", "Haydovchi juda ehtiyotkor edi."),
            voc('durmak', "to'xtamoq", "Kırmızıda dur.", "Qizilda to'xta."),
            voc('dikkat etmek', "e'tiborli bo'lmoq", 'Yola dikkat et.', "Yo'lga e'tiborli bo'l."),
        ],
        'listening': {
            'dialogue': [
                dialogue_line('Polis', 'Emniyet kemerinizi neden takmadınız?'),
                dialogue_line('Sürücü', 'Özür dilerim, unuttum.'),
                dialogue_line('Polis', 'Bu çok tehlikeli, lütfen dikkat edin.'),
                dialogue_line('Sürücü', 'Tamam, bir daha unutmayacağım.'),
            ],
            'questions': [
                mcq('Polis sürücüye neyi sordu?', ['Emniyet kemeri neden takılmadı', "Hızı neden yüksek", 'Nereye gidiyor', 'Ehliyeti var mı'], 0),
                mcq('Sürücü ne söz verdi?', ['Bir daha unutmayacağını', "Hemen durduracağını", 'Hız yapmaya devam edeceğini', "Polisle tartışacağını"], 0),
            ],
        },
        'reading': {
            'title': 'Yol Güvenliği',
            'text': "Trafik kazaların çoğu dikkatsizlik yüzünden olur. Sürücüler hız limitine "
                    "uymalı, emniyet kemerini takmalı ve telefonla konuşmamalıdır. Yayalar da "
                    "yaya geçidinden geçmeli ve kırmızı ışıkta durmalıdır. Herkes kurallara "
                    "uyarsa, kazalar azalır.",
            'questions': [
                mcq('Kazaların çoğu neden olur?', ["Dikkatsizlik", "Yağmur", 'Kar', "Rüzgar"], 0),
                mcq('Yayalar nereden geçmeli?', ["Yaya geçidinden", "Yoldan istedikleri yerden", "Sadece geceleri", "Arabaların arasından"], 0),
            ],
        },
        'sentence_practice': [
            choice("'Kırmızı ışıkta ___' (to'xta, buyruq)", ['dur', 'durma', 'durdu', 'duracak'], 0),
            choice("'Emniyet kemerini ___' (tak, buyruq)", ['tak', 'takma', 'taktı', 'takacak'], 0),
            order("Cümleyi doğru sıraya dizin: 'Yayalar yaya geçidinden geçmeli'", ['Yayalar', 'yaya', 'geçidinden', 'geçmeli']),
            choice("'Trafik kazası' nima?", ["Yo'lda yuz beradigan baxtsiz hodisa", "Yo'l qurilishi", "Avtobus bekati", "Svetofor"], 0),
        ],
        'writing_prompt': {
            'instruction': "Yo'l xavfsizligi qoidalari haqida 3 ta buyruq mayli bilan gap yozing.",
            'sample_answer': "Kırmızı ışıkta dur. Emniyet kemerini tak. Yaya geçidinden geç.",
        },
        'speaking_prompt': {'sentences': ['Emniyet kemerini takmayı unutma.', 'Kırmızı ışıkta dur.', 'Hız limitine uy.']},
    },
    'test': [
        mcq("'Trafik canavarı' iborasi nimani anglatadi?", ["Qoida buzish natijasidagi baxtsiz hodisalar", "Yangi mashina turi", "Yo'l nomi", "Politsiya lavozimi"], 0),
        mcq("'Emniyet kemeri' nima?", ["Xavfsizlik kamari", "Svetofor", "Yo'l belgisi", "Haydovchilik guvohnomasi"], 0),
        mcq("'Kırmızı ışıkta dur' qaysi maylda?", ["Buyruq (emir kipi)", "Savol", "Kelasi zamon", "O'tgan zamon"], 0),
        mcq("Trafik kazolarining ko'pi nima sababdan yuz beradi?", ["E'tiborsizlik", "Yomon ob-havo", "Eski mashinalar", "Ko'p yo'llar"], 0),
        mcq("'Yaya' so'zi kim?", ["Piyoda", "Haydovchi", "Politsiya", "Yo'lovchi (avtobusda)"], 0),
        fill_blank("'Hız limitine ___ ' (rioya qil, buyruq)", 'uy'),
    ],
})

# ============================================================
# 3-UNITE: SOSYAL ETKINLIKLER
# ============================================================
sections.append({'key': 'u3', 'title': "3-ünite. Sosyal Etkinlikler", 'topics': []})

sections[2]['topics'].append({
    'key': 'u3a', 'title': "A. Okumayı Seviyorum — Geniş zaman (-Ir/-Ar/-r)",
    'start_page': 7, 'end_page': 7,
    'explanation': {
        'goals': ["Geniş zamanni (har doim/odatda sodir bo'ladigan harakat) o'rganish", "Kitob o'qish va sevimli mashg'ulotlar haqida gapirish"],
        'blocks': [
            block(
                "Geniş zaman nima?",
                "**Geniş zaman** (-Ir/-Ar/-r) o'zbekchadagi \"hozirgi-kelasi zamon\" (masalan "
                "\"o'qiyman\", \"boraman\" - umumiy, odatiy harakat)ga to'g'ri keladi. Bu zaman "
                "==doimiy odat, umumiy haqiqat yoki xarakterni== bildiradi, aynan hozir sodir "
                "bo'layotgan harakatni emas:\n\n"
                "- **Ben her gün kitap okurum.** = Men har kuni kitob o'qiyman. (odat)\n"
                "- **Güneş doğudan doğar.** = Quyosh sharqdan chiqadi. (umumiy haqiqat)",
            ),
            block(
                "Qo'shish qoidasi",
                "Ko'p bo'g'inli fe'llarga **-Ir/-Ir/-Ur/-Ür** (unli bilan tugasa) yoki bir "
                "bo'g'inlilarga **-Ar/-Er** qo'shiladi, keyin shaxs qo'shimchasi:\n\n"
                "oku + r -> **okurum** (o'qiyman), **okursun**, **okur**, **okuruz**, "
                "**okursunuz**, **okurlar**.\n\n"
                "sev + er -> **severim** (sevaman), **seversin**, **sever**...\n\n"
                "Olumsuz shakl: **oku-maz** (o'qimaydi), **sev-mez** (sevmaydi) - diqqat, "
                "==olumsuz shaklda -r yo'qoladi==!",
            ),
        ],
        'key_facts': [
            fact("Geniş zaman (-Ir/-Ar/-r) - odat, umumiy haqiqat yoki xarakterni bildiradi."),
            fact("Olumsuz shaklda -maz/-mez ishlatiladi, -r qo'shilmaydi."),
        ],
        'summary': "**Geniş zaman** (-Ir/-Ar/-r) - o'zbekchadagi umumiy hozirgi-kelasi zamonga mos, odat va haqiqatni bildiradi.",
        'vocabulary': [
            voc('okumak', "o'qimoq", "Kitap okurum.", "Kitob o'qiyman."),
            voc('roman', 'roman', 'Roman okumayı severim.', "Roman o'qishni yaxshi ko'raman."),
            voc('yazar', 'muallif/yozuvchi', 'Sevdiğim bir yazar var.', "Sevimli yozuvchim bor."),
            voc('kütüphane', 'kutubxona', 'Kütüphaneye giderim.', 'Kutubxonaga boraman.'),
            voc('hikâye', "hikoya", 'Kısa hikâyeler okurum.', "Qisqa hikoyalar o'qiyman."),
            voc('sevmek', 'yoqtirmoq/sevmoq', 'Okumayı severim.', "O'qishni yaxshi ko'raman."),
            voc('boş vakit', "bo'sh vaqt", "Boş vaktimde okurum.", "Bo'sh vaqtimda o'qiyman."),
            voc('ilginç', 'qiziqarli', 'Bu kitap çok ilginç.', 'Bu kitob juda qiziqarli.'),
            voc('sıkıcı', 'zerikarli', 'Bu kitap biraz sıkıcı.', 'Bu kitob birozgina zerikarli.'),
            voc('tavsiye etmek', 'tavsiya qilmoq', 'Bu kitabı tavsiye ederim.', 'Bu kitobni tavsiya qilaman.'),
        ],
        'listening': {
            'dialogue': [
                dialogue_line('Elif', "Boş vaktinde ne yaparsın?"),
                dialogue_line('Can', 'Genellikle kitap okurum. Sen ne yaparsın?'),
                dialogue_line('Elif', 'Ben de okumayı severim, özellikle roman okurum.'),
                dialogue_line('Can', 'Bana bir kitap tavsiye eder misin?'),
            ],
            'questions': [
                mcq('Can boş vaktinde ne yapar?', ['Kitap okur', 'Spor yapar', 'Uyur', 'Televizyon izler'], 0),
                mcq('Elif özellikle ne tür kitap okur?', ['Roman', "Şiir", "Ders kitabı", 'Gazete'], 0),
            ],
        },
        'reading': {
            'title': 'Benim Bir Alışkanlığım',
            'text': "Her akşam yatmadan önce en az yarım saat kitap okurum. Bu benim en "
                    "sevdiğim alışkanlık. Roman okumayı severim, ama bazen hikâye kitapları "
                    "da okurum. Kitap okumak insana çok şey öğretir.",
            'questions': [
                mcq('Yazar ne zaman kitap okur?', ["Yatmadan önce", "Sabah erken", "İşten sonra", "Öğle yemeğinde"], 0),
                mcq('Yazara göre kitap okumak ne yapar?', ["İnsana çok şey öğretir", "Vakit kaybettirir", "Yorucu olur", "Faydasızdır"], 0),
            ],
        },
        'sentence_practice': [
            choice("'oku' fe'liga geniş zaman qo'shimchasi qanday qo'shiladi?", ['okurum', 'okuyorum', 'okudum', 'okuyacağım'], 0),
            choice("'sev' fe'lining olumsuz geniş zamon shakli qaysi?", ['sevmez', 'sever', 'sevecek', 'sevdi'], 0),
            order("Cümleyi doğru sıraya dizin: 'Ben her gün kitap okurum'", ['Ben', 'her', 'gün', 'kitap', 'okurum']),
            choice("'Güneş doğudan doğar' qaysi zamon?", ["Geniş zaman", "O'tgan zamon", "Kelasi zamon", "Hozirgi zamon (-yor)"], 0),
        ],
        'writing_prompt': {
            'instruction': "Geniş zamon (-Ir/-Ar/-r) ishlatib, o'zingizning odatlaringiz haqida 3 gap yozing.",
            'sample_answer': "Her gün kitap okurum. Akşamları müzik dinlerim. Hafta sonları arkadaşlarımla buluşurum.",
        },
        'speaking_prompt': {'sentences': ['Her gün kitap okurum.', 'Roman okumayı severim.', 'Boş vaktimde müzik dinlerim.']},
    },
    'test': [
        mcq("Geniş zaman (-Ir/-Ar/-r) nimani bildiradi?", ["Odat, umumiy haqiqat", "Faqat hozirgi payt harakati", "Faqat o'tmish", "Faqat kelajak"], 0),
        mcq("'okumak' fe'lining geniş zaman 1-shaxs shakli qaysi?", ['okurum', 'okuyorum', 'okudum', 'okumuş'], 0),
        mcq("Geniş zamonning olumsuz shaklida qaysi qo'shimcha ishlatiladi?", ['-maz/-mez', '-r/-Ir', '-di', '-ecek'], 0),
        mcq("'Güneş doğudan doğar' gapi nimani ifodalaydi?", ["Umumiy haqiqat", "Bir martalik voqea", "Savol", "Buyruq"], 0),
        mcq("'sevmek' so'zi nima?", ["Sevmoq/yoqtirmoq", "O'qimoq", "Yozmoq", "Ko'rmoq"], 0),
        fill_blank("'sev' fe'liga geniş zamon 3-shaxs (u) qo'shimchasi (olumsuz EMAS)", 'sever'),
    ],
})

sections[2]['topics'].append({
    'key': 'u3b', 'title': "B. Hangi Filme Gidelim? — hem...hem, ne...ne, ya...ya, ister...ister",
    'start_page': 8, 'end_page': 8,
    'explanation': {
        'goals': ["Juft bog'lovchilarni (hem...hem, ne...ne, ya...ya, ister...ister) o'rganish", "Kino va bo'sh vaqt haqida tanlov bildirish"],
        'blocks': [
            block(
                "To'rtta juft bog'lovchi",
                "Turkchada tanlov, birgalik yoki inkorni bildiruvchi **juft (takrorlanuvchi) "
                "bog'lovchilar** bor:\n\n"
                "- **hem...hem (de)** = \"ham...ham\" (ikkalasi ham): *Hem yorgunum hem açım.* "
                "(Ham charchaganman, ham ochman.)\n"
                "- **ne...ne (de)** = \"na...na\" (ikkalasi ham emas): *Ne çay ne kahve içerim.* "
                "(Na choy, na qahva ichaman - hech birini ichmayman.)\n"
                "- **ya...ya (da)** = \"yo...yo\" (ikkitadan biri): *Ya sinemaya ya tiyatroya "
                "gidelim.* (Yo kinoga, yo teatrga boraylik.)\n"
                "- **ister...ister** = \"xoh...xoh\" (farqi yo'q, ikkalasi ham mumkin): "
                "*İster gel ister gelme.* (Xoh kel, xoh kelma.)",
            ),
            block(
                "Amaliy qo'llanilishi",
                "Bu qurilmalar do'stlar bilan reja tuzishda juda foydali - kino tanlash, "
                "restoran tanlash kabi vaziyatlarda: \"Ya komedi ya aksiyon filmi izleyelim\" "
                "(Yo komediya, yo jangari film ko'raylik). Diqqat qiling: ==har bir bog'lovchi "
                "ikki marta takrorlanadi==, ikkita variant/holat oldidan.",
            ),
        ],
        'key_facts': [
            fact("hem...hem = ham...ham (ikkalasi ham to'g'ri)."), fact("ne...ne = na...na (ikkalasi ham emas)."),
            fact("ya...ya = yo...yo (ikkitadan biri)."), fact("ister...ister = xoh...xoh (farqi yo'q)."),
        ],
        'summary': "To'rtta juft bog'lovchi: **hem...hem** (ikkalasi), **ne...ne** (hech biri), "
                   "**ya...ya** (biri), **ister...ister** (farqi yo'q).",
        'vocabulary': [
            voc('film', 'film', 'Bu akşam film izleyelim.', "Bugun kechqurun film ko'raylik."),
            voc('sinema', 'kinoteatr', "Sinemaya gidelim.", "Kinoteatrga boraylik."),
            voc('komedi', 'komediya', 'Komedi filmi severim.', "Komediya filmini yoqtiraman."),
            voc('aksiyon', 'jangari (aksiya)', 'Aksiyon filmi izlerim.', "Jangari film ko'raman."),
            voc('bilet', 'chipta', 'Bilet aldık.', 'Chipta oldik.'),
            voc('tiyatro', 'teatr', "Tiyatroya gitmeyi severim.", "Teatrga borishni yaxshi ko'raman."),
            voc('seçim', 'tanlov', "Zor bir seçim.", "Qiyin tanlov."),
            voc('fark etmez', "farqi yo'q", "Bana fark etmez.", "Menga farqi yo'q."),
        ],
        'listening': {
            'dialogue': [
                dialogue_line('Deniz', 'Bu akşam hangi filme gidelim?'),
                dialogue_line('Ece', "İster komedi ister aksiyon, bana fark etmez."),
                dialogue_line('Deniz', 'O zaman ya yeni komedi ya da o aksiyon filmine gidelim.'),
                dialogue_line('Ece', "Hem komedi hem aksiyon seven bir film var mı?"),
            ],
            'questions': [
                mcq("Ece hangi janrı tercih ediyor?", ["Fark etmez, ikisi de", "Sadece komedi", 'Sadece aksiyon', "Hiçbirini"], 0),
                mcq('Deniz sonunda ne teklif etti?', ["Ya komedi ya aksiyon", "Sadece drama", 'Hiçbir film', 'Konser'], 0),
            ],
        },
        'reading': {
            'title': 'Hafta Sonu Planı',
            'text': "Hafta sonu ne yapacağımıza karar veremedik. Ben ister sinemaya ister "
                    "tiyatroya gidelim dedim, arkadaşım ise ne sinema ne tiyatro istiyor, "
                    "sadece evde dinlenmek istiyor. Sonunda hem evde dinlenip hem de akşam "
                    "kısa bir yürüyüş yapmaya karar verdik.",
            'questions': [
                mcq('Arkadaşı ne istiyor?', ["Evde dinlenmek", "Sinemaya gitmek", 'Tiyatroya gitmek', "Konsere gitmek"], 0),
                mcq('Sonunda ne karar verdiler?', ["Hem dinlenmek hem yürüyüş", "Sadece sinema", 'Sadece tiyatro', "Hiçbir şey"], 0),
            ],
        },
        'sentence_practice': [
            choice("'___ çay ___ kahve içerim' (na choy na qahva)", ['Ne / ne', 'Hem / hem', 'Ya / ya', 'İster / ister'], 0),
            choice("'___ gel ___ gelme' (xoh kel, xoh kelma)", ['İster / ister', 'Ne / ne', 'Hem / hem', 'Ya / ya'], 0),
            choice("'___ yorgunum ___ açım' (ham charchagan, ham och)", ['Hem / hem', 'Ne / ne', 'Ya / ya', 'İster / ister'], 0),
            order("Cümleyi doğru sıraya dizin: 'Ya sinemaya ya tiyatroya gidelim'", ['Ya', 'sinemaya', 'ya', 'tiyatroya', 'gidelim']),
        ],
        'writing_prompt': {
            'instruction': "Juft bog'lovchilardan (hem...hem, ne...ne, ya...ya, ister...ister) ikkitasini ishlatib, 2 gap yozing.",
            'sample_answer': "Hem kitap okumayı hem film izlemeyi severim. İster sinemaya ister eve gidelim, ikisi de olur.",
        },
        'speaking_prompt': {'sentences': ['Hem yorgunum hem açım.', 'Ne çay ne kahve içerim.', 'İster gel ister gelme.']},
    },
    'test': [
        mcq("'hem...hem' qanday ma'no beradi?", ["Ikkalasi ham (ham...ham)", "Hech biri", "Ikkitadan biri", "Farqi yo'q"], 0),
        mcq("'ne...ne' qanday ma'no beradi?", ["Ikkalasi ham emas (na...na)", "Ikkalasi ham", "Ikkitadan biri", "Albatta"], 0),
        mcq("'ya...ya' qanday ma'no beradi?", ["Ikkitadan biri (yo...yo)", "Ikkalasi ham", "Hech biri", "Har doim"], 0),
        mcq("'ister...ister' qanday ma'no beradi?", ["Farqi yo'q, ikkalasi ham mumkin", "Faqat birinchisi", "Faqat ikkinchisi", "Hech qaysisi mumkin emas"], 0),
        mcq("'Ne çay ne kahve içerim' jumlasining ma'nosi nima?", ["Ikkalasini ham ichmayman", "Ikkalasini ham ichaman", "Faqat choy ichaman", "Faqat qahva ichaman"], 0),
        fill_blank("'___ gel ister gelme, bana fark etmez' (xoh kel, xoh kelma) - bosh bo'shliqqa yoziladigan so'z", 'ister'),
    ],
})

sections[2]['topics'].append({
    'key': 'u3c', 'title': "C. Spor Yap, Zinde Kal — -A göre, bu yüzden/bu sebeple",
    'start_page': 9, 'end_page': 9,
    'explanation': {
        'goals': ["'-A göre' (fikricha/ga ko'ra) qurilmasini o'rganish", "'bu yüzden/bu sebeple' (shuning uchun) bog'lovchisini bilish", "Sport haqida gapirish"],
        'blocks': [
            block(
                "'-A göre': fikr va manbaga ko'ra",
                "**[ot/kishi] + -a/-e göre** = \"...ga ko'ra, ...fikricha\":\n\n"
                "- **Bana göre spor çok önemli.** = Menimcha (menga ko'ra), sport juda muhim.\n"
                "- **Doktora göre günde 30 dakika yürüyüş yeterli.** = Shifokorga ko'ra, kuniga "
                "30 daqiqa yurish yetarli.\n\n"
                "Bu qurilma fikr bildirish yoki biror manbaga tayanib gapirishda juda ko'p "
                "ishlatiladi - jurnalistika va kundalik nutqda ham.",
            ),
            block(
                "'bu yüzden / bu sebeple': natija bog'lovchisi",
                "Bu ikki ibora ==sabab-natija bog'lash== uchun ishlatiladi, o'zbekchadagi "
                "\"shuning uchun\" ga to'g'ri keladi:\n\n"
                "**Spor yapmıyorum, bu yüzden yorgun hissediyorum.** = Sport qilmayman, "
                "shuning uchun charchagan his qilaman.\n\n"
                "**bu sebeple** biroz rasmiyroq uslub, **bu yüzden** kundalik so'zlashuvda "
                "ko'proq ishlatiladi - ikkalasi ham bir xil ma'noni beradi.",
            ),
        ],
        'key_facts': [
            fact("-A göre = ...ga ko'ra/fikricha (fikr yoki manbaga tayanish)."),
            fact("bu yüzden/bu sebeple = shuning uchun (sabab-natija bog'lovchisi)."),
        ],
        'summary': "**-A göre** - fikr bildirish ('...ga ko'ra'), **bu yüzden/bu sebeple** - sabab-natija ('shuning uchun').",
        'vocabulary': [
            voc('spor', 'sport', 'Spor yapmak sağlıklı.', "Sport qilish foydali."),
            voc('zinde', "baquvvat/tetik", 'Kendimi zinde hissediyorum.', "O'zimni baquvvat his qilyapman."),
            voc('koşmak', 'yugurmoq', 'Her sabah koşarım.', 'Har ertalab yuguraman.'),
            voc('yüzmek', "suzmoq", "Yüzmeyi severim.", "Suzishni yaxshi ko'raman."),
            voc('antrenman', "mashg'ulot", 'Antrenmana gittim.', "Mashg'ulotga bordim."),
            voc('form', 'shakl (jismoniy)', 'Formda kalmak istiyorum.', "Jismoniy shaklda qolishni xohlayman."),
            voc('enerji', 'energiya', 'Spor bana enerji verir.', 'Sport menga energiya beradi.'),
            voc('tembel', 'dangasa', 'Bugün biraz tembelim.', "Bugun birozgina dangasaman."),
        ],
        'listening': {
            'dialogue': [
                dialogue_line('Ahmet', "Bana göre spor yapmak şart."),
                dialogue_line('Zeynep', "Katılıyorum. Ben spor yapmıyorum, bu yüzden hep yorgunum."),
                dialogue_line('Ahmet', 'Doktoruma göre haftada üç gün yeterli.'),
                dialogue_line('Zeynep', 'O zaman yarından itibaren başlayacağım.'),
            ],
            'questions': [
                mcq("Zeynep neden hep yorgun?", ["Spor yapmadığı için", "Çok uyuduğu için", 'Çok yediği için', "Hasta olduğu için"], 0),
                mcq('Doktoruna göre haftada kaç gün spor yeterli?', ['Üç gün', 'Bir gün', 'Her gün', 'Altı gün'], 0),
            ],
        },
        'reading': {
            'title': 'Neden Spor Yapmalıyız?',
            'text': "Uzmanlara göre düzenli spor yapmak hem bedeni hem zihni güçlendirir. "
                    "Spor yapmayan insanlar bu yüzden daha çabuk yorulur ve hastalanır. Bana "
                    "göre herkes en azından haftada iki-üç kez spor yapmalıdır.",
            'questions': [
                mcq('Uzmanlara göre spor ne yapar?', ["Bedeni ve zihni güçlendirir", 'Sadece yorar', "Hiçbir etkisi yok", "Sadece vakit kaybettirir"], 0),
                mcq("Yazara göre haftada kaç kez spor yapılmalı?", ["İki-üç kez", 'Bir kez', 'Her gün', "Hiç yapılmamalı"], 0),
            ],
        },
        'sentence_practice': [
            choice("'Bana ___ spor önemli' (menimcha)", ['göre', 'için', 'ile', 'kadar'], 0),
            choice("'Spor yapmıyorum, ___ yorgunum' (shuning uchun)", ['bu yüzden', 've', 'ama', 'gibi'], 0),
            order("Cümleyi doğru sıraya dizin: 'Doktora göre spor önemli'", ['Doktora', 'göre', 'spor', 'önemli']),
        ],
        'writing_prompt': {
            'instruction': "'-A göre' va 'bu yüzden' ishlatib, sport haqida 2 gap yozing.",
            'sample_answer': "Bana göre spor çok önemli. Her gün spor yapıyorum, bu yüzden kendimi zinde hissediyorum.",
        },
        'speaking_prompt': {'sentences': ['Bana göre spor önemli.', 'Doktora göre su içmek gerekli.', 'Yorgunum, bu yüzden dinleniyorum.']},
    },
    'test': [
        mcq("'-A göre' qurilmasi nima uchun ishlatiladi?", ["Fikr bildirish yoki manbaga tayanish", "Vaqt bildirish", "Joy bildirish", "Miqdor bildirish"], 0),
        mcq("'Bana göre' qanday tarjima qilinadi?", ["Menimcha/menga ko'ra", "Men uchun", "Men bilan", "Mendan keyin"], 0),
        mcq("'bu yüzden' qanday ma'no beradi?", ["Shuning uchun", "Ammo", "Va", "Yoki"], 0),
        mcq("'Spor yapmıyorum, bu yüzden yorgunum' gapida sabab nima?", ["Sport qilmaslik", "Charchash", "Uxlash", "Ovqatlanish"], 0),
        mcq("'zinde' so'zi nima?", ["Baquvvat/tetik", "Charchagan", "Kasal", "Uyqusiz"], 0),
        fill_blank("'Doktora ___ günde 30 dakika yürüyüş yeterli' (ga ko'ra)", 'göre'),
    ],
})

# ============================================================
# 4-UNITE: GUZEL ULKEM
# ============================================================
sections.append({'key': 'u4', 'title': "4-ünite. Güzel Ülkem", 'topics': []})

sections[3]['topics'].append({
    'key': 'u4a', 'title': "A. Her Yer Tarih — -mA/-mAk/-Iş va dolaylı anlatımda buyruq",
    'start_page': 10, 'end_page': 10,
    'explanation': {
        'goals': ["Fe'lni otga aylantiruvchi -mA, -mAk, -Iş qo'shimchalarini farqlash", "Boshqa odamning buyrug'ini qayta aytish (dolaylı anlatım) qurilmasini o'rganish"],
        'blocks': [
            block(
                "Fe'ldan ot yasash: -mA, -mAk, -Iş",
                "Uchala qo'shimcha ham fe'lni **otga** aylantiradi, lekin nozik farqlar bor:\n\n"
                "- **-mAk** - fe'lning lug'aviy (infinitiv) shakli: **okumak** (o'qish/o'qimoq - "
                "lug'atdagi shakl)\n"
                "- **-mA** - umumiy harakat oti: **okuma** (o'qish, masalan \"okuma alışkanlığı\" "
                "= o'qish odati)\n"
                "- **-Iş** - ko'pincha harakat **tarzi** yoki bir martalik holatni bildiradi: "
                "**yürüyüş** (sayr, yurish tarzi, yürümekdan), **bakış** (bir qarash, bakmakdan), "
                "**gülüş** (kulgi, gülmekdan)\n\n"
                "Solishtiring: \"yüzme\" (suzish - umumiy harakat) va \"yüzüş\" (suzish uslubi) - "
                "ikkalasi ham to'g'ri, lekin ohang farqli.",
            ),
            block(
                "Boshqa odamning buyrug'ini qayta aytish (dolaylı anlatım)",
                "Kimdir sizga biror narsa qilishni **buyurgan/so'ragan** bo'lsa va buni "
                "boshqasiga aytib berayotgan bo'lsangiz, to'g'ridan-to'g'ri buyruqni "
                "takrorlamaysiz, balki ==fe'l + -mAsInI + söyledi/istedi== qurilmasidan "
                "foydalanasiz:\n\n"
                "To'g'ridan-to'g'ri: **\"Otur!\"** (O'tir!)\n"
                "Qayta aytilganda: **\"Oturmasını söyledi.\"** (U o'tirishini aytdi = U unga "
                "o'tirishni buyurdi.)\n\n"
                "Yana misol: **\"Kapıyı kapat!\"** -> **\"Kapıyı kapatmasını istedi.\"** "
                "(Eshikni yopishini so'radi.)",
            ),
        ],
        'key_facts': [
            fact("-mAk - fe'lning lug'aviy shakli, -mA - umumiy harakat oti, -Iş - harakat tarzi/bir martaligi."),
            fact("Buyruqni qayta aytish: fe'l + -mAsInI + söyledi/istedi."),
        ],
        'summary': "**-mAk/-mA/-Iş** - fe'ldan ot yasaydi (nozik farq bilan); buyruqni qayta aytishda "
                   "**-mAsInI söyledi/istedi** qurilmasi ishlatiladi.",
        'vocabulary': [
            voc('tarih', 'tarix', 'Bu şehir tarih doludur.', 'Bu shahar tarixga boy.'),
            voc('eser', 'asar', 'Tarihi eserleri gezdik.', 'Tarixiy obidalarni aylandik.'),
            voc('müze', 'muzey', 'Müzeye gittik.', 'Muzeyga bordik.'),
            voc('kale', "qal'a", "Eski bir kale var.", "Eski bir qal'a bor."),
            voc('yürüyüş', "sayr/yurish", "Akşam yürüyüşü yaptık.", "Kechqurun sayr qildik."),
            voc('bakış', "qarash", "Güzel bir bakışı var.", "Uning chiroyli qarashi bor."),
            voc('söylemek', 'aytmoq', 'Bana gelmesini söyledi.', 'U menga kelishimni aytdi.'),
            voc('istemek', "xohlamoq/so'ramoq", 'Kapıyı kapatmamı istedi.', 'U mendan eshikni yopishimni so\'radi.'),
            voc('medeniyet', 'sivilizatsiya', 'Bu bölgede eski bir medeniyet yaşamış.', 'Bu hududda qadimiy sivilizatsiya yashagan.'),
            voc('kazı', 'qazishma (arxeologik)', 'Burada kazı yapılıyor.', 'Bu yerda arxeologik qazishma olib borilmoqda.'),
            voc('koruma altında', "muhofaza ostida", 'Bu eser koruma altında.', 'Bu obida muhofaza ostida.'),
        ],
        'listening': {
            'dialogue': [
                dialogue_line('Rehber', 'Bu kale 500 yıl önce yapılmış.'),
                dialogue_line('Turist', 'Çok etkileyici! Fotoğraf çekebilir miyiz?'),
                dialogue_line('Rehber', 'Evet, ama müzede fotoğraf çekmemenizi rica ediyorum.'),
                dialogue_line('Turist', 'Tamam, anladım.'),
            ],
            'questions': [
                mcq('Kale ne zaman yapılmış?', ["500 yıl önce", "5 yıl önce", "50 yıl önce", "Bu yıl"], 0),
                mcq('Rehber turistten ne rica etti?', ['Müzede fotoğraf çekmemesini', "Erken gelmesini", 'Sessiz olmasını', 'Bilet almasını'], 0),
            ],
        },
        'reading': {
            'title': 'Her Yer Tarih',
            'text': "Bu ülkede her şehrin kendi tarihi vardır. Eski kaleler, müzeler ve "
                    "tarihi evler her yerde görülebilir. Rehberimiz bize fotoğraf çekmemizi "
                    "ve sessiz olmamızı söyledi, çünkü bazı yerler çok hassastır. Bazı "
                    "bölgelerde hâlâ kazı çalışmaları devam ediyor - arkeologlar toprağın "
                    "altında eski bir medeniyetin izlerini arıyor. Bulunan her eser dikkatle "
                    "koruma altına alınıyor, çünkü bu eserler sadece bu ülkenin değil, tüm "
                    "insanlığın ortak mirasıdır.",
            'questions': [
                mcq('Ülkede neler görülebilir?', ["Kaleler, müzeler, tarihi evler", "Sadece deniz", "Sadece dağlar", "Hiçbir şey"], 0),
                mcq('Rehber ne söyledi?', ["Fotoğraf çekmelerini ve sessiz olmalarını", "Yüksek sesle konuşmalarını", "Koşmalarını", "Yemek yemelerini"], 0),
                mcq('Bazı bölgelerde hâlâ ne devam ediyor?', ['Kazı çalışmaları', 'İnşaat', 'Tatil', 'Spor müsabakası'], 0),
                mcq('Bulunan eserlere ne yapılıyor?', ['Koruma altına alınıyor', 'Satılıyor', "Yok ediliyor", "Unutuluyor"], 0),
            ],
        },
        'sentence_practice': [
            choice("'yürümek' fe'lidan 'sayr/yurish' (tarz) oti qaysi?", ['yürüyüş', 'yürüme', 'yürümek', 'yürüyor'], 0),
            choice("Fe'lning lug'atdagi (infinitiv) shakli qaysi qo'shimcha bilan tugaydi?", ['-mak/-mek', '-ma/-me', '-ış/-üş', '-di'], 0),
            order("Cümleyi doğru sıraya dizin: 'Bana gelmesini söyledi'", ['Bana', 'gelmesini', 'söyledi']),
        ],
        'writing_prompt': {
            'instruction': "Kimdir sizga biror narsa qilishni buyurganini 'dolaylı anlatım' bilan (masalan: '...mesini söyledi') 2 gapda yozing.",
            'sample_answer': "Annem bana odamı temizlememi söyledi. Öğretmenim de ödevi bitirmemi istedi.",
        },
        'speaking_prompt': {'sentences': ['Bana kapıyı kapatmamı söyledi.', 'Yürüyüş yapmayı severim.', 'Bu şehir tarih doludur.']},
    },
    'test': [
        mcq("'-mAk' qo'shimchasi fe'lning qaysi shaklini yasaydi?", ["Lug'aviy (infinitiv) shakl", "Buyruq shakli", "O'tgan zamon", "Kelasi zamon"], 0),
        mcq("'yürümek' dan yasalgan 'yürüyüş' so'zi nimani bildiradi?", ["Sayr/yurish tarzi", "Yugurish", "Uxlash", "Gapirish"], 0),
        mcq("Boshqa odamning buyrug'ini qayta aytish uchun qanday qurilma ishlatiladi?", ["Fe'l + -mAsInI + söyledi/istedi", "Fe'l + -yor", "Fe'l + -ecek", "Fe'l + -di"], 0),
        mcq("'Oturmasını söyledi' jumlasi qaysi asl buyruqdan kelib chiqqan?", ["Otur!", "Oturuyor.", "Oturacak.", "Oturdu."], 0),
        mcq("'müze' so'zi nima?", ["Muzey", "Bozor", "Maktab", "Kasalxona"], 0),
        mcq("'kazı' so'zi nima?", ["Arxeologik qazishma", "Sayohat", "Savdo", "Qurilish"], 0),
        mcq("'medeniyet' so'zi nima?", ["Sivilizatsiya", "Shahar nomi", "Muzey turi", "Bayram"], 0),
        fill_blank("'Kapıyı kapat___ söyledi' (u eshikni yopishimni aytdi, 1-shaxsga)", 'mamı'),
    ],
})

sections[3]['topics'].append({
    'key': 'u4b', 'title': "B. Dört Mevsim Yedi Bölge", 'start_page': 11, 'end_page': 11,
    'explanation': {
        'goals': ["Mavsumlar va Turkiya geografik hududlari haqida lug'at o'rganish", "Iqlim haqida gapirish"],
        'blocks': [
            block(
                "To'rt mavsum",
                "Turkiyada **to'rt mavsum** aniq bilinadi: **ilkbahar** (bahor), **yaz** "
                "(yoz), **sonbahar** (kuz), **kış** (qish). Har bir mavsumning o'z go'zalligi "
                "bor: ilkbaharda gullar ochiladi, yozda dengizga boriladi, kuzda barglar "
                "to'kiladi, qishda qor yog'adi.",
            ),
            block(
                "Yedi coğrafi bölge",
                "Turkiya **yetti coğrafi hududga** bo'lingan, va ==har hududning o'z iqlimi== "
                "bor: Qora dengiz hududida yomg'ir ko'p yog'adi, O'rta dengiz hududida yozlar "
                "issiq va quruq, Ichki Anadoluda esa qishlar sovuq va qorli o'tadi. Bu "
                "xilma-xillik Turkiyani geografik jihatdan juda boy qiladi.",
            ),
        ],
        'key_facts': [
            fact("To'rt mavsum: ilkbahar, yaz, sonbahar, kış."), fact("Turkiya yetti coğrafi hududga bo'lingan, har birining o'z iqlimi bor."),
        ],
        'summary': "Turkiyada **to'rt mavsum** va **yetti hudud** bor - har birining o'ziga xos iqlimi.",
        'vocabulary': [
            voc('mevsim', 'mavsum', 'Dört mevsim yaşıyoruz.', "To'rt mavsumni his qilamiz."),
            voc('bölge', 'hudud', 'Bu bölgede kışlar çok soğuk.', "Bu hududda qishlar juda sovuq."),
            voc('ilkbahar', 'bahor', 'İlkbaharda çiçekler açar.', 'Bahorda gullar ochiladi.'),
            voc('sonbahar', 'kuz', 'Sonbaharda yapraklar dökülür.', "Kuzda barglar to'kiladi."),
            voc('kış', 'qish', 'Kışın kar yağar.', "Qishda qor yog'adi."),
            voc('iklim', 'iqlim', 'Bu bölgenin iklimi çok değişken.', "Bu hududning iqlimi juda o'zgaruvchan."),
            voc('dağ', 'tog\'', 'Dağlara tırmanmak zor.', "Tog'ga chiqish qiyin."),
            voc('göl', "ko'l", 'Göl çok güzel.', "Ko'l juda chiroyli."),
            voc('nem', 'namlik', 'Bu bölgede nem oranı yüksek.', 'Bu hududda namlik darajasi yuqori.'),
            voc('kurak', 'quruq (iqlim haqida)', 'Yaz ayları kurak geçer.', "Yoz oylari quruq o'tadi."),
            voc('rüzgâr', 'shamol', 'Bugün rüzgâr çok güçlü.', "Bugun shamol juda kuchli."),
        ],
        'listening': {
            'dialogue': [
                dialogue_line('Aslı', 'Hangi mevsimi seversin?'),
                dialogue_line('Emre', 'Ben yazı severim, çünkü denize girebiliyorum.'),
                dialogue_line('Aslı', 'Ben kışı severim, kar yağmasını çok seviyorum.'),
                dialogue_line('Emre', 'Her mevsimin güzelliği var.'),
            ],
            'questions': [
                mcq('Emre hangi mevsimi sever?', ['Yaz', 'Kış', 'İlkbahar', 'Sonbahar'], 0),
                mcq("Aslı kışı neden sever?", ["Kar yağmasını sevdiği için", "Sıcak olduğu için", "Deniz olduğu için", "Okul olmadığı için"], 0),
            ],
        },
        'reading': {
            'title': "Türkiye'nin Bölgeleri",
            'text': "Türkiye'nin yedi coğrafi bölgesi vardır. Her bölgenin kendine özgü "
                    "iklimi ve doğası vardır. Karadeniz Bölgesi'nde yağmur çok yağar ve nem "
                    "oranı yüksektir, bu yüzden burada çay ve fındık çok iyi yetişir. "
                    "Akdeniz Bölgesi'nde ise yazlar sıcak ve kurudur, kış ayları bile ılıman "
                    "geçer. İç Anadolu'da kışlar soğuk ve karlı, yazlar ise kurak ve "
                    "rüzgârlı geçer. Doğu Anadolu'da ise kışlar öyle sert olur ki, bazı "
                    "yıllar sıcaklık eksi otuz dereceye kadar düşebilir.",
            'questions': [
                mcq("Türkiye'nin kaç bölgesi vardır?", ['Yedi', 'Beş', 'Üç', 'On'], 0),
                mcq('Karadeniz Bölgesi nasıldır?', ['Yağmur çok yağar', 'Çok kurak', 'Hep karlı', 'Çölümsü'], 0),
                mcq('Karadeniz Bölgesinde ne iyi yetişir?', ['Çay ve fındık', 'Zeytin', 'Pirinç', 'Pamuk'], 0),
                mcq('Doğu Anadolu kışları nasıl olabilir?', ["Eksi otuz dereceye kadar soğuk", "Hep sıcak", "Yağmurlu ama ılık", "Hiç kar yağmaz"], 0),
            ],
        },
        'sentence_practice': [
            choice("Turkiyada nechta mavsum bor?", ["To'rtta", "Ikkita", "Beshta", "Oltita"], 0),
            choice("'Kışın kar ___' (yog'adi)", ['yağar', 'yağmıyor', 'yağmadı', 'yağmayacak'], 0),
            order("Cümleyi doğru sıraya dizin: 'İlkbaharda çiçekler açar'", ['İlkbaharda', 'çiçekler', 'açar']),
        ],
        'writing_prompt': {
            'instruction': "Eng sevimli mavsumingiz haqida 3 gap yozing.",
            'sample_answer': "Ben ilkbaharı severim. Çiçekler açar, hava ısınır. Doğada yürüyüş yapmak çok güzel oluyor.",
        },
        'speaking_prompt': {'sentences': ['En sevdiğim mevsim yaz.', "Kışın kar yağar.", 'Sonbaharda yapraklar dökülür.']},
    },
    'test': [
        mcq("Turkiyada nechta mavsum bor?", ["To'rtta", "Ikkita", "Beshta", "Uchta"], 0),
        mcq("'kış' so'zi qaysi mavsumni bildiradi?", ["Qish", "Yoz", "Bahor", "Kuz"], 0),
        mcq("Turkiya nechta coğrafi hududga bo'lingan?", ["Yettita", "Beshta", "O'nta", "Uchta"], 0),
        mcq("Karadeniz hududida qanday iqlim bor?", ["Yomg'irli", "Juda issiq va quruq", "Cho'l iqlimi", "Doim qorli"], 0),
        mcq("'göl' so'zi nima?", ["Ko'l", "Dengiz", "Daryo", "Tog'"], 0),
        mcq("'nem' so'zi nima?", ["Namlik", "Quruqlik", "Issiqlik", "Sovuqlik"], 0),
        mcq("'kurak' so'zi iqlim haqida qanday ma'no beradi?", ["Quruq", "Yomg'irli", "Qorli", "Shamolli"], 0),
    ],
})

sections[3]['topics'].append({
    'key': 'u4c', 'title': "C. Tatlı Yiyelim, Tatlı Konuşalım", 'start_page': 12, 'end_page': 12,
    'explanation': {
        'goals': ["Turk shirinliklari lug'atini o'rganish", "Pazandalik retsepti haqida gapirish"],
        'blocks': [
            block(
                "Turk shirinliklari",
                "\"**Tatlı yiyelim, tatlı konuşalım**\" (Shirin narsa yeylik, shirin "
                "gaplashaylik) - Turk madaniyatida mehmondo'stlik va yaxshi kayfiyatni "
                "bildiruvchi mashhur ibora. **Baklava** va **lokum** - dunyoga mashhur ikki "
                "turk shirinligi.",
            ),
            block(
                "Retsept haqida gapirish",
                "Pazandalik retsepti tasvirlashda ko'pincha **buyruq/taklif mayli** (-(y)AlIm) "
                "ishlatiladi: \"Önce malzemeleri hazırlayalım\" (Avval malzemalarni "
                "tayyorlaylik), \"Şekeri ekleyelim\" (Shakarni qo'shaylik). Bu ==birgalikda "
                "taklif qilish== shaklidir - o'zbekchadagi \"-aylik\" ga to'g'ri keladi.",
            ),
        ],
        'key_facts': [
            fact("Baklava va lokum - dunyoga mashhur turk shirinliklari."), fact("-(y)AlIm - birgalikda taklif qilish shakli ('...aylik')."),
        ],
        'summary': "Retsept tasvirlashda **-(y)AlIm** ('...aylik') shakli ishlatiladi: hazırlayalım, ekleyelim.",
        'vocabulary': [
            voc('tatlı', 'shirinlik', 'Tatlı yemeyi severim.', "Shirinlik yeishni yaxshi ko'raman."),
            voc('baklava', 'baklava', 'Baklava çok lezzetli.', 'Baklava juda mazali.'),
            voc('lokum', "rohatjon (lukum)", 'Lokum aldık.', 'Lukum oldik.'),
            voc('şeker', 'shakar', 'Şeker koydum.', 'Shakar qo\'shdim.'),
            voc('tarif', 'retsept', 'Bu tarif çok kolay.', 'Bu retsept juda oson.'),
            voc('malzeme', 'malzama', 'Malzemeleri hazırladım.', 'Malzamalarni tayyorladim.'),
            voc('pişirmek', 'pishirmoq', 'Pastayı fırında pişirdim.', 'Tortni pechda pishirdim.'),
            voc('fırın', 'pech', 'Fırın çok sıcak.', 'Pech juda issiq.'),
            voc('ceviz', "yong'oq", 'Baklavada ceviz var.', 'Baklavada yong\'oq bor.'),
            voc('hamur', 'xamir', 'Hamuru yoğurdum.', 'Xamirni qordim.'),
            voc('lezzetli', 'mazali', 'Bu tatlı çok lezzetli.', 'Bu shirinlik juda mazali.'),
        ],
        'listening': {
            'dialogue': [
                dialogue_line('Anne', 'Bugün baklava yapacağız.'),
                dialogue_line('Kız', 'Harika! Önce malzemeleri hazırlayalım.'),
                dialogue_line('Anne', 'Şekeri ne zaman ekleyeceğiz?'),
                dialogue_line('Kız', 'Pişirdikten sonra ekleriz.'),
            ],
            'questions': [
                mcq('Ne yapacaklar?', ['Baklava', 'Lokum', 'Ekmek', 'Çorba'], 0),
                mcq('Şeker ne zaman eklenir?', ["Pişirdikten sonra", "Pişirmeden önce", "Fırına koymadan önce", "Hiç eklenmez"], 0),
            ],
        },
        'reading': {
            'title': 'Türk Tatlıları',
            'text': "Türk mutfağında birçok meşhur tatlı vardır. Baklava, ince hamur "
                    "yapraklarından ve cevizden yapılır. Lokum ise şekerden yapılan yumuşak "
                    "bir tatlıdır. Misafirlerinize tatlı ikram etmek Türk kültüründe çok "
                    "önemlidir. Baklava yapmak aslında sanattır - hamur o kadar ince "
                    "açılmalıdır ki, neredeyse şeffaf görünmelidir. Ustalar bu ustalığı "
                    "yıllarca çalışarak öğrenir. Bugün baklava dünyanın birçok ülkesinde "
                    "tanınan ve sevilen bir tatlı hâline gelmiştir.",
            'questions': [
                mcq('Baklava neyden yapılır?', ['İnce hamur ve ceviz', 'Sadece şeker', 'Süt ve un', 'Meyve'], 0),
                mcq('Misafire tatlı ikram etmek ne anlama gelir?', ["Türk kültüründe önemli bir gelenek", "Gereksiz bir davranış", "Sadece bayramda yapılır", "Yasak bir şey"], 0),
                mcq('Baklava hamuru nasıl açılmalıdır?', ["Neredeyse şeffaf olacak kadar ince", "Çok kalın", "Hiç açılmaz", "Sadece elle"], 0),
            ],
        },
        'sentence_practice': [
            choice("'Malzemeleri hazırla___' (tayyorlaylik, taklif)", ['yalım', 'dık', 'yor', 'acak'], 0),
            choice("'Baklava' nima?", ["Turk shirinligi", "Ichimlik", "Sabzavot", "Go'sht taomi"], 0),
            order("Cümleyi doğru sıraya dizin: 'Önce malzemeleri hazırlayalım'", ['Önce', 'malzemeleri', 'hazırlayalım']),
        ],
        'writing_prompt': {
            'instruction': "-(y)AlIm shaklini ishlatib, birga ovqat/shirinlik tayyorlash haqida 2 taklif gap yozing.",
            'sample_answer': "Önce fırını ısıtalım. Sonra malzemeleri karıştıralım.",
        },
        'speaking_prompt': {'sentences': ['Baklava çok lezzetli.', 'Tatlı yiyelim, tatlı konuşalım.', 'Önce malzemeleri hazırlayalım.']},
    },
    'test': [
        mcq("'Tatlı yiyelim, tatlı konuşalım' iborasi nimani anglatadi?", ["Mehmondo'stlik va yaxshi kayfiyat", "Ovqatlanish qoidasi", "Salomlashish usuli", "Xayrlashish iborasi"], 0),
        mcq("Baklava nimadan tayyorlanadi?", ["Yupqa xamir va yong'oq", "Faqat shakar", "Sut va un", "Go'sht"], 0),
        mcq("'-(y)AlIm' shakli nimani bildiradi?", ["Birgalikda taklif ('...aylik')", "O'tgan zamon", "Kelasi zamon", "Savol"], 0),
        mcq("'fırın' so'zi nima?", ["Pech", "Muzlatgich", "Idish", "Qoshiq"], 0),
        mcq("'Şekeri ekleyelim' jumlasi qaysi shaklda?", ["Taklif (-(y)AlIm)", "Buyruq", "Savol", "Inkor"], 0),
        mcq("'ceviz' so'zi nima?", ["Yong'oq", "Shakar", "Xamir", "Sut"], 0),
        mcq("'lezzetli' so'zi nima?", ["Mazali", "Achchiq", "Tuzli", "Nordon"], 0),
    ],
})

# ============================================================
# 5-UNITE: URETIMDEN TUKETIME
# ============================================================
sections.append({'key': 'u5', 'title': "5-ünite. Üretimden Tüketime", 'topics': []})

sections[4]['topics'].append({
    'key': 'u5a', 'title': "A. Üretim-Tüketim — -(y)Ip va -(y)ArAk",
    'start_page': 13, 'end_page': 13,
    'explanation': {
        'goals': ["-(y)Ip (ketma-ket harakat) qurilmasini o'rganish", "-(y)ArAk (usul/vosita) qurilmasini bilish", "Ishlab chiqarish-iste'mol lug'atini o'rganish"],
        'blocks': [
            block(
                "-(y)Ip: ketma-ket harakatlarni bog'lash",
                "**-(y)Ip** ikki (yoki undan ko'p) harakatni ==bir egaga tegishli holda "
                "ketma-ket== bog'lash uchun ishlatiladi - o'zbekchadagi \"-b\" ravishdoshiga "
                "o'xshash (\"borib\", \"kelib\"):\n\n"
                "- **Markete gidip ekmek aldım.** = Do'konga borib, non oldim.\n"
                "- **Parayı verip ürünü aldım.** = Pulni berib, mahsulotni oldim.\n\n"
                "Diqqat: faqat ==oxirgi fe'lga== zamon/shaxs qo'shimchasi qo'shiladi, "
                "oldingi fe'l(lar)ga faqat -(y)Ip qo'shiladi.",
            ),
            block(
                "-(y)ArAk: usul/vosita bildirish",
                "**-(y)ArAk** biror harakat ==qanday amalga oshirilganini== (usul/vosita) "
                "bildiradi, o'zbekchadagi \"-b\" yoki \"orqali\" ga o'xshaydi:\n\n"
                "- **Koşarak geldi.** = Yugurib keldi (yugurish orqali keldi).\n"
                "- **Çalışarak para kazanırız.** = Ishlash orqali pul topamiz.\n\n"
                "Farqi: **-(y)Ip** ikki alohida harakatni ketma-ket bog'laydi, **-(y)ArAk** "
                "esa ==birinchi harakat ikkinchisining USULI== ekanini ko'rsatadi.",
            ),
        ],
        'key_facts': [
            fact("-(y)Ip - ketma-ket harakatlarni bog'laydi (borib, kelib)."),
            fact("-(y)ArAk - harakat usulini bildiradi (yugurib, ishlab)."),
        ],
        'summary': "**-(y)Ip** - ketma-ket harakat ('borib, kelib'), **-(y)ArAk** - usul/vosita ('yugurib, ishlab').",
        'vocabulary': [
            voc('üretim', 'ishlab chiqarish', 'Bu fabrika çok ürün üretiyor.', "Bu fabrika ko'p mahsulot ishlab chiqaradi."),
            voc('tüketim', "iste'mol", "Tüketim artıyor.", "Iste'mol ortmoqda."),
            voc('fabrika', 'fabrika', 'Fabrikada çalışıyorum.', 'Fabrikada ishlayman.'),
            voc('ürün', 'mahsulot', 'Ürünleri satarız.', 'Mahsulotlarni sotamiz.'),
            voc('satmak', 'sotmoq', 'Bu mağazada elbise satarlar.', "Bu do'konda kiyim sotishadi."),
            voc('almak', 'sotib olmoq', 'Market\'ten ekmek aldım.', "Do'kondan non oldim."),
            voc('işçi', 'ishchi', 'İşçiler çok çalışıyor.', "Ishchilar ko'p ishlayapti."),
            voc('para', 'pul', 'Param yeterli değil.', 'Pulim yetarli emas.'),
            voc('hammadde', 'xomashyo', 'Hammadde fabrikaya gelir.', 'Xomashyo fabrikaga keladi.'),
            voc('dağıtım', 'tarqatish', 'Ürünlerin dağıtımı hızlıdır.', 'Mahsulotlarni tarqatish tez.'),
            voc('depo', 'ombor', 'Ürünler depoda bekler.', 'Mahsulotlar omborda kutadi.'),
            voc('talep', 'talab', 'Bu ürüne talep çok yüksek.', 'Bu mahsulotga talab juda yuqori.'),
            voc('arz', 'taklif (iqtisodiy)', "Arz ve talep dengesi önemlidir.", "Taklif va talab muvozanati muhim."),
        ],
        'listening': {
            'dialogue': [
                dialogue_line('Ali', 'Nereye gidiyorsun?'),
                dialogue_line('Veli', 'Markete gidip birkaç şey alacağım.'),
                dialogue_line('Ali', 'Ben de çalışarak para biriktiriyorum, yeni bir telefon almak için.'),
                dialogue_line('Veli', 'İyi fikir, ben de öyle yapmalıyım.'),
            ],
            'questions': [
                mcq('Veli nereye gidiyor?', ['Markete', 'Okula', 'Fabrikaya', 'Hastaneye'], 0),
                mcq('Ali ne için para biriktiriyor?', ['Yeni telefon almak için', 'Ev almak için', 'Araba almak için', 'Tatile gitmek için'], 0),
            ],
        },
        'reading': {
            'title': 'Bir Ürünün Yolculuğu',
            'text': "Bir ürünün yolculuğu, hammaddenin fabrikaya getirilmesiyle başlar. "
                    "İşçiler çalışarak hammaddeyi işleyip ürünü hazırlar. Ürün hazır "
                    "olduktan sonra depoya konur ve oradan mağazalara dağıtılır. Bir ürünün "
                    "ne kadar üretileceğine karar verirken şirketler arz ve talep dengesine "
                    "bakar: eğer bir ürüne talep çoksa, daha fazla üretilir. Sonunda "
                    "müşteriler mağazaya gidip istedikleri ürünü satın alır. Böylece "
                    "üretimden tüketime uzun bir yolculuk tamamlanmış olur.",
            'questions': [
                mcq('Ürünün yolculuğu nasıl başlar?', ['Hammaddenin fabrikaya gelmesiyle', 'Mağazada satılmasıyla', 'Reklamla', 'Depoda beklemesiyle'], 0),
                mcq('Müşteriler ürünü nasıl alır?', ['Mağazaya gidip satın alarak', 'Fabrikadan direkt alarak', 'Postayla', 'Ücretsiz olarak'], 0),
                mcq('Şirketler ne kadar üretileceğine karar verirken nelere bakar?', ['Arz ve talep dengesine', 'Sadece hava durumuna', 'Sadece renklere', 'Hiçbir şeye bakmaz'], 0),
                mcq('Ürün fabrikadan sonra nereye gider?', ['Depoya', 'Doğrudan eve', 'Okula', 'Hastaneye'], 0),
            ],
        },
        'sentence_practice': [
            choice("'Markete git___ ekmek aldım' (borib, ketma-ket harakat)", ['ip', 'erek', 'meden', 'dikten'], 0),
            choice("'Koş___ geldi' (yugurib, usul)", ['arak', 'up', 'madan', 'dıktan'], 0),
            order("Cümleyi doğru sıraya dizin: 'Parayı verip ürünü aldım'", ['Parayı', 'verip', 'ürünü', 'aldım']),
        ],
        'writing_prompt': {
            'instruction': "-(y)Ip va -(y)ArAk qurilmalarini ishlatib, kunlik faoliyatingiz haqida 2 gap yozing.",
            'sample_answer': "Sabah kalkıp kahvaltı yaptım. Koşarak işe yetiştim.",
        },
        'speaking_prompt': {'sentences': ['Markete gidip ekmek aldım.', 'Çalışarak para kazanırız.', 'Eve gelip dinlendim.']},
    },
    'test': [
        mcq("'-(y)Ip' qanday harakatlarni bog'laydi?", ["Bir egaga tegishli ketma-ket harakatlarni", "Faqat savol gaplarni", "Faqat inkor gaplarni", "Ikki xil egani"], 0),
        mcq("'-(y)ArAk' nimani bildiradi?", ["Harakat usuli/vositasini", "Faqat vaqtni", "Faqat joyni", "Faqat sababni"], 0),
        mcq("'Koşarak geldi' qanday tarjima qilinadi?", ["Yugurib keldi", "Yurib keldi", "Uxlab keldi", "Kelmadi"], 0),
        mcq("'-(y)Ip' qo'shimchasida zamon/shaxs qo'shimchasi qaysi fe'lga qo'shiladi?", ["Faqat oxirgi fe'lga", "Har bir fe'lga", "Hech qaysi fe'lga", "Faqat birinchi fe'lga"], 0),
        mcq("'üretim' so'zi nima?", ["Ishlab chiqarish", "Iste'mol", "Sotish", "Xarid qilish"], 0),
        mcq("'talep' so'zi nima?", ["Talab", "Taklif", "Narx", "Chegirma"], 0),
        mcq("'depo' so'zi nima?", ["Ombor", "Do'kon", "Fabrika", "Bozor"], 0),
        fill_blank("'Markete git___ ekmek aldım' (borib)", 'ip'),
    ],
})

sections[4]['topics'].append({
    'key': 'u5b', 'title': "B. İş Yemeği", 'start_page': 14, 'end_page': 14,
    'explanation': {
        'goals': ["Restoran va ishbilarmonlik uchrashuvi lug'atini o'rganish", "Taom buyurtma qilish muloqotini bilish"],
        'blocks': [
            block(
                "İş yemeği nima?",
                "**İş yemeği** (biznes tushligi/kechki ovqati) - hamkorlar yoki ishdoshlar "
                "bilan restoranda o'tkaziladigan rasmiy uchrashuv. Bunday vaziyatlarda "
                "==rasmiy va xushmuomala nutq== muhim: \"Buyurabilir miyim?\" (Buyurtma "
                "berishim mumkinmi?), \"Afiyet olsun\" (Yoqimli ishtaha).",
            ),
            block(
                "Restoran muloqoti",
                "- **Masayı ayırtmıştım.** = Men stolni band qilib qo'ygandim.\n"
                "- **Menüyü alabilir miyim?** = Menyuni olsam bo'ladimi?\n"
                "- **Hesabı alabilir miyiz?** = Hisobni olsak bo'ladimi?\n\n"
                "Bu iboralar barchasi ==xushmuomalalik shakli (-abilir miyim)== bilan "
                "berilgan - rasmiy so'rov qilishning odobli yo'li.",
            ),
        ],
        'key_facts': [
            fact("İş yemeği - hamkorlar bilan restoranda o'tkaziladigan rasmiy uchrashuv."),
            fact("'-abilir miyim?' - xushmuomalalik bilan so'rov qilish shakli."),
        ],
        'summary': "Restoranda xushmuomala so'rov: **[fe'l]+abilir miyim/miyiz?** (...sam bo'ladimi?).",
        'vocabulary': [
            voc('restoran', 'restoran', 'Güzel bir restorana gittik.', 'Chiroyli restoranga bordik.'),
            voc('menü', 'menyu', 'Menüyü inceledik.', "Menyuni ko'rib chiqdik."),
            voc('garson', 'ofitsiant', 'Garson geldi.', 'Ofitsiant keldi.'),
            voc('hesap', 'hisob (to\'lov)', 'Hesabı istedik.', "Hisobni so'radik."),
            voc('masa', 'stol', 'Masayı ayırttık.', 'Stolni band qildirdik.'),
            voc('sipariş', 'buyurtma', 'Siparişimizi verdik.', 'Buyurtmamizni berdik.'),
            voc('afiyet olsun', 'yoqimli ishtaha', 'Afiyet olsun!', 'Yoqimli ishtaha!'),
            voc('rezervasyon', 'bron qilish', 'Rezervasyon yaptırdım.', 'Bron qildirdim.'),
            voc('anlaşma', 'kelishuv/shartnoma', 'Anlaşmayı imzaladık.', 'Shartnomani imzoladik.'),
            voc('ortak', 'sherik/hamkor', 'Yeni bir ortakla tanıştım.', 'Yangi hamkor bilan tanishdim.'),
        ],
        'listening': {
            'dialogue': [
                dialogue_line('Garson', 'Hoş geldiniz, masanız hazır.'),
                dialogue_line('Müşteri', 'Teşekkürler. Menüyü alabilir miyim?'),
                dialogue_line('Garson', 'Tabii, buyurun.'),
                dialogue_line('Müşteri', "Siparişimizi verelim: iki çorba, iki ana yemek."),
            ],
            'questions': [
                mcq('Müşteri ilk ne istedi?', ['Menüyü', 'Hesabı', 'Suyu', 'Ekmeği'], 0),
                mcq('Müşteri ne sipariş verdi?', ['Çorba ve ana yemek', 'Sadece tatlı', 'Sadece içecek', 'Hiçbir şey'], 0),
            ],
        },
        'reading': {
            'title': 'Bir İş Yemeği',
            'text': "Bugün önemli bir müşteriyle iş yemeğine gittik. Bir hafta önceden "
                    "rezervasyon yaptırmıştık, güzel bir restoranda masamız hazırdı. Garson "
                    "geldi, menüyü aldık ve siparişimizi verdik. Yemekten sonra yeni "
                    "ortaklığımız hakkında konuştuk ve sonunda bir anlaşmaya vardık. Bu "
                    "anlaşma şirketimiz için çok önemliydi, çünkü aylardır bu ortakla "
                    "görüşüyorduk. Hesabı ödeyip mutlu bir şekilde restorandan çıktık.",
            'questions': [
                mcq('Kiminle iş yemeğine gittiler?', ['Önemli bir müşteriyle', 'Aileyle', 'Arkadaşlarla', 'Yalnız'], 0),
                mcq('Yemekten sonra ne yaptılar?', ['Ortaklık hakkında konuşup anlaşmaya vardılar', 'Hemen çıktılar', 'Uyudular', 'Film izlediler'], 0),
                mcq('Restoranda rezervasyon ne zaman yapılmıştı?', ['Bir hafta önceden', 'O gün sabah', 'Hiç yapılmamıştı', 'Bir ay önce'], 0),
            ],
        },
        'sentence_practice': [
            choice("'Menüyü al___ miyim?' (olsam bo'ladimi, xushmuomala so'rov)", ['abilir', 'dı', 'acak', 'ıyor'], 0),
            choice("'Afiyet olsun' qachon aytiladi?", ["Ovqatlanishdan oldin/vaqtida", "Xayrlashganda", "Tabriklaganda", "Salomlashganda"], 0),
            order("Cümleyi doğru sıraya dizin: 'Hesabı alabilir miyiz?'", ['Hesabı', 'alabilir', 'miyiz']),
        ],
        'writing_prompt': {
            'instruction': "Restoranda xushmuomala so'rov qilib ('-abilir miyim?') 2 gap yozing.",
            'sample_answer': "Menüyü alabilir miyim? Hesabı alabilir miyiz?",
        },
        'speaking_prompt': {'sentences': ['Menüyü alabilir miyim?', 'Hesabı alabilir miyiz?', 'Afiyet olsun!']},
    },
    'test': [
        mcq("'İş yemeği' nima?", ["Hamkorlar bilan rasmiy restoran uchrashuvi", "Oddiy uy ovqati", "Bayram taomi", "Nonushta"], 0),
        mcq("'Afiyet olsun' qachon aytiladi?", ["Ovqatlanish paytida/oldida", "Xayrlashganda", "Uyg'onganda", "Ishga borganda"], 0),
        mcq("'-abilir miyim?' shakli nimani bildiradi?", ["Xushmuomala so'rov", "Buyruq", "Kelasi zamon", "O'tgan zamon"], 0),
        mcq("'hesap' so'zi restoran kontekstida nima?", ["Hisob (to'lov)", "Matematik masala", "Kitob", "Xat"], 0),
        mcq("'garson' kim?", ["Ofitsiant", "Oshpaz", "Mijoz", "Egasi"], 0),
        mcq("'rezervasyon' so'zi nima?", ["Bron qilish", "To'lov", "Chegirma", "Menyu"], 0),
        mcq("'ortak' so'zi nima?", ["Sherik/hamkor", "Mijoz", "Ofitsiant", "Musofir"], 0),
    ],
})

sections[4]['topics'].append({
    'key': 'u5c', 'title': "C. Alışveriş", 'start_page': 15, 'end_page': 15,
    'explanation': {
        'goals': ["Xarid qilish lug'atini o'rganish", "Do'konda muloqot qilishni bilish"],
        'blocks': [
            block(
                "Do'konda muloqot",
                "Xarid qilishda eng ko'p ishlatiladigan iboralar: **\"Bu elbiseyi "
                "deneyebilir miyim?\"** (Bu ko'ylakni kiyib ko'rsam bo'ladimi?), **\"İndirim "
                "var mı?\"** (Chegirma bormi?), **\"Başka rengi var mı?\"** (Boshqa rangi "
                "bormi?).",
            ),
            block(
                "Narx haqida gapirish",
                "- **pahalı** (qimmat) va **ucuz** (arzon) - eng asosiy sifatlar\n"
                "- **Fiyatı ne kadar?** = Narxi qancha?\n"
                "- **Biraz indirim yapabilir misiniz?** = Biroz chegirma qila olasizmi?\n\n"
                "Bu savollar ==bozorlashish (pazarlık)== madaniyatida juda foydali - ba'zi "
                "do'konlarda narx haqida savdolashish odatiy holdir.",
            ),
        ],
        'key_facts': [
            fact("pahalı = qimmat, ucuz = arzon."), fact("'Fiyatı ne kadar?' - narxni so'rash iborasi."),
        ],
        'summary': "Xarid lug'ati: **mağaza, fiyat, indirim, pahalı, ucuz** - va xushmuomala so'rov shakli.",
        'vocabulary': [
            voc('alışveriş', 'xarid qilish', 'Alışverişe çıktık.', 'Xarid qilgani chiqdik.'),
            voc('mağaza', "do'kon", 'Bu mağaza çok büyük.', "Bu do'kon juda katta."),
            voc('fiyat', 'narx', 'Fiyatı çok yüksek.', "Narxi juda baland."),
            voc('indirim', 'chegirma', 'İndirim var mı?', "Chegirma bormi?"),
            voc('pahalı', 'qimmat', 'Bu çok pahalı.', 'Bu juda qimmat.'),
            voc('ucuz', 'arzon', 'Daha ucuz bir şey var mı?', "Arzonroq narsa bormi?"),
            voc('beden', "o'lcham", 'Bedeniniz nedir?', "O'lchamingiz qancha?"),
            voc('renk', 'rang', 'Hangi rengi istersiniz?', "Qaysi rangni xohlaysiz?"),
            voc('değiştirmek', 'almashtirmoq', 'Bu ürünü değiştirebilir miyim?', "Bu mahsulotni almashtira olamanmi?"),
            voc('iade etmek', 'qaytarmoq', "Ürünü iade ettim.", "Mahsulotni qaytardim."),
            voc('fiş', 'chek', "Fişinizi saklayın.", "Chekingizni saqlang."),
        ],
        'listening': {
            'dialogue': [
                dialogue_line('Müşteri', 'Bu elbiseyi deneyebilir miyim?'),
                dialogue_line('Satıcı', 'Tabii, kabin şurada.'),
                dialogue_line('Müşteri', 'Beğendim, ama biraz pahalı. İndirim var mı?'),
                dialogue_line('Satıcı', 'Size yüzde on indirim yapabilirim.'),
            ],
            'questions': [
                mcq('Müşteri ne yapmak istiyor?', ['Elbiseyi denemek', 'Elbiseyi iade etmek', 'Elbiseyi satmak', 'Elbiseyi yıkamak'], 0),
                mcq('Satıcı ne kadar indirim yaptı?', ['Yüzde on', 'Yüzde elli', 'Hiç indirim yapmadı', 'Yüzde yüz'], 0),
            ],
        },
        'reading': {
            'title': 'Alışveriş Merkezinde',
            'text': "Hafta sonu alışveriş merkezine gittim. Birçok mağazayı gezdim. "
                    "Beğendiğim bir ceket buldum ama fiyatı çok yüksekti. Satıcıya indirim "
                    "olup olmadığını sordum. Neyse ki yüzde yirmi indirimle aldım. Eve "
                    "geldiğimde ceketi tekrar denedim ve beden biraz büyük geldiğini fark "
                    "ettim. Ertesi gün fişimle birlikte mağazaya geri döndüm ve daha küçük "
                    "bedenle değiştirdim. Satıcı çok yardımcı oldu ve hiçbir sorun "
                    "çıkmadı.",
            'questions': [
                mcq('Ne satın aldı?', ['Ceket', 'Ayakkabı', 'Çanta', 'Gömlek'], 0),
                mcq('Ne kadar indirimle aldı?', ['Yüzde yirmi', 'Yüzde on', 'İndirimsiz', 'Yüzde elli'], 0),
                mcq('Eve geldiğinde ne fark etti?', ['Bedenin büyük olduğunu', 'Rengin yanlış olduğunu', "Fiyatın yanlış olduğunu", "Hiçbir şey fark etmedi"], 0),
                mcq('Mağazaya geri dönerken yanında ne götürdü?', ['Fişini', 'Sadece parayı', "Hiçbir şey", 'Eski bir ceket'], 0),
            ],
        },
        'sentence_practice': [
            choice("'Bu elbiseyi dene___ miyim?' (kiyib ko'rsam bo'ladimi)", ['yebilir', 'di', 'yecek', 'yor'], 0),
            choice("'Fiyatı ne ___?' (qancha)", ['kadar', 'gibi', 'için', 'ile'], 0),
            order("Cümleyi doğru sıraya dizin: 'İndirim var mı?'", ['İndirim', 'var', 'mı']),
        ],
        'writing_prompt': {
            'instruction': "Do'konda xarid qilish haqida 3 gapli qisqa dialog yozing.",
            'sample_answer': "Bu ayakkabıyı deneyebilir miyim? Beden kaç? Fiyatı ne kadar?",
        },
        'speaking_prompt': {'sentences': ['İndirim var mı?', 'Bu çok pahalı.', 'Fiyatı ne kadar?']},
    },
    'test': [
        mcq("'pahalı' so'zining ma'nosi nima?", ["Qimmat", "Arzon", "Chiroyli", "Xunuk"], 0),
        mcq("'ucuz' so'zining ma'nosi nima?", ["Arzon", "Qimmat", "Katta", "Kichik"], 0),
        mcq("'İndirim var mı?' qanday tarjima qilinadi?", ["Chegirma bormi?", "Narxi qancha?", "Bu nima?", "Qayerda?"], 0),
        mcq("'Fiyatı ne kadar?' savoli nima haqida?", ["Narx", "Rang", "O'lcham", "Vaqt"], 0),
        mcq("'mağaza' so'zi nima?", ["Do'kon", "Uy", "Maktab", "Kasalxona"], 0),
        mcq("'iade etmek' so'zi nima?", ["Qaytarmoq", "Sotib olmoq", "Almashtirmoq", "Sinab ko'rmoq"], 0),
        mcq("'fiş' so'zi nima?", ["Chek", "Chipta", "Xat", "Kitob"], 0),
    ],
})

# ============================================================
# 6-UNITE: DUYGULAR
# ============================================================
sections.append({'key': 'u6', 'title': "6-ünite. Duygular", 'topics': []})

sections[5]['topics'].append({
    'key': 'u6a', 'title': "A. Mektup Yazalım", 'start_page': 16, 'end_page': 16,
    'explanation': {
        'goals': ["Hissiyot (duygu) lug'atini o'rganish", "Mektub yozish uslubini bilish"],
        'blocks': [
            block(
                "His-tuyg'u so'zlari",
                "Turkchada asosiy hissiyotlar: **mutlu** (baxtli), **üzgün** (xafa), "
                "**kızgın** (jahldor), **korkmuş** (qo'rqqan), **şaşkın** (hayron), "
                "**heyecanlı** (hayajonli). Bu so'zlar odatda \"olmak\" (bo'lmoq) fe'li "
                "bilan yoki to'g'ridan-to'g'ri predikat sifatida ishlatiladi: \"Mutluyum\" "
                "(Baxtliman).",
            ),
            block(
                "Mektub yozish uslubi",
                "An'anaviy turk mektubi shunday boshlanadi: **\"Sevgili [ism],\"** (Aziz "
                "[ism],) va shunday tugaydi: **\"Sevgilerimle,\"** (Mehr bilan,) yoki "
                "**\"Seni özledim,\"** (Seni sog'indim,). Mektub matnida ==his-tuyg'ularni "
                "ochiq ifodalash== odatiy holdir - bu til o'rganuvchilar uchun yozma nutqni "
                "mashq qilishning ajoyib usuli.",
            ),
            block(
                "Hissiyotni kuchaytirish: 'çok', 'son derece', 'oldukça'",
                "Oddiy \"mutluyum\" (baxtliman) o'rniga, hissiyotni ==darajasiga qarab== "
                "turlicha kuchaytirish mumkin:\n\n"
                "- **çok mutluyum** = juda baxtliman (kundalik, eng ko'p ishlatiladigan)\n"
                "- **son derece mutluyum** = nihoyatda baxtliman (kuchliroq, biroz rasmiyroq)\n"
                "- **oldukça üzgünüm** = ancha xafaman (o'rtacha darajadagi kuchaytirish)\n\n"
                "Mektub yozganda shu darajalardan foydalanish fikringizni ==aniqroq va "
                "nozikroq== ifodalash imkonini beradi - har doim \"çok\" bilan "
                "cheklanmang.",
            ),
        ],
        'key_facts': [
            fact("mutlu, üzgün, kızgın, korkmuş - asosiy hissiyot so'zlari."), fact("Mektub 'Sevgili...' bilan boshlanib, 'Sevgilerimle' bilan tugaydi."),
            fact("'çok/son derece/oldukça' - hissiyot kuchini turlicha darajada bildiradi."),
        ],
        'summary': "Hissiyot so'zlari predikat sifatida ishlatiladi: **Mutluyum, üzgünüm, kızgınım**.",
        'vocabulary': [
            voc('mektup', 'xat', 'Sana bir mektup yazıyorum.', 'Senga bir xat yozyapman.'),
            voc('duygu', "his-tuyg'u", 'Duygularımı anlatmak istiyorum.', "His-tuyg'ularimni aytib berishni xohlayman."),
            voc('mutlu', 'baxtli', 'Bugün çok mutluyum.', 'Bugun juda baxtliman.'),
            voc('üzgün', 'xafa', 'Biraz üzgünüm.', 'Birozgina xafaman.'),
            voc('kızgın', 'jahldor', 'Neden kızgınsın?', 'Nega jahlding chiqyapti?'),
            voc('korkmuş', "qo'rqqan", 'Çok korkmuştum.', "Juda qo'rqqandim."),
            voc('özlemek', "sog'inmoq", 'Seni özledim.', "Men seni sog'indim."),
            voc('göndermek', "yubormoq", 'Mektubu gönderdim.', 'Xatni yubordim.'),
            voc('heyecanlı', 'hayajonli', 'Sınavdan önce çok heyecanlıydım.', "Imtihondan oldin juda hayajonlangan edim."),
            voc('şaşkın', "hayron", 'Haberi duyunca şaşkına döndüm.', "Xabarni eshitib hayron bo'lib qoldim."),
            voc('rahatlamak', 'yengil tortmoq', 'Konuştuktan sonra rahatladım.', "Gaplashgandan keyin yengil tortdim."),
            voc('içten', 'samimiy', 'İçten bir mektup yazdı.', "Samimiy xat yozdi."),
        ],
        'listening': {
            'dialogue': [
                dialogue_line('Anne', 'Kime mektup yazıyorsun?'),
                dialogue_line('Kız', 'Arkadaşıma. Onu çok özledim.'),
                dialogue_line('Anne', 'Ne yazdın?'),
                dialogue_line('Kız', "Sevgili Zeynep, seni çok özledim, diye başladım."),
            ],
            'questions': [
                mcq('Kız kime mektup yazıyor?', ['Arkadaşına', 'Annesine', 'Öğretmenine', 'Kardeşine'], 0),
                mcq('Mektup nasıl başlıyor?', ["'Sevgili Zeynep' ile", "'Merhaba' ile", "'Selam' ile", "İsimsiz"], 0),
            ],
        },
        'reading': {
            'title': 'Bir Mektup',
            'text': "Sevgili arkadaşım, nasılsın? Ben burada çok mutluyum ama seni de çok "
                    "özledim. Yeni şehrimde ilginç insanlarla tanıştım. Bazen üzgün "
                    "oluyorum çünkü ailemi görmüyorum. İlk geldiğimde oldukça şaşkındım, "
                    "çünkü her şey çok farklıydı. Ama şimdi buraya alıştım ve son derece "
                    "mutluyum. Yeni arkadaşlarımla konuşurken kendimi çok rahat "
                    "hissediyorum. Umarım yakında görüşürüz. Sevgilerimle, Ayşe.",
            'questions': [
                mcq('Ayşe genel olarak nasıl hissediyor?', ['Mutlu ama arkadaşını özlemiş', 'Çok kızgın', 'Çok korkmuş', 'Hiçbir şey hissetmiyor'], 0),
                mcq('Ayşe bazen neden üzgün oluyor?', ['Ailesini görmediği için', 'Hasta olduğu için', 'Parası olmadığı için', 'İşi olmadığı için'], 0),
                mcq('Ayşe ilk geldiğinde nasıl hissetmiş?', ['Oldukça şaşkın', 'Çok kızgın', 'Hiç şaşırmamış', 'Çok korkmuş'], 0),
            ],
        },
        'sentence_practice': [
            choice("'Bugün çok ___' (baxtliman)", ['mutluyum', 'mutlusun', 'mutlu', 'mutluyuz'], 0),
            choice("Mektub odatda qanday so'z bilan boshlanadi?", ['Sevgili', 'Merhaba', 'Hoşça kal', 'Teşekkürler'], 0),
            order("Cümleyi doğru sıraya dizin: 'Seni çok özledim'", ['Seni', 'çok', 'özledim']),
        ],
        'writing_prompt': {
            'instruction': "Do'stingizga qisqa mektub yozing (3-4 gap), his-tuyg'u so'zlaridan foydalaning.",
            'sample_answer': "Sevgili arkadaşım, seni çok özledim. Burada mutluyum ama sen de burada olsan daha iyi olurdu. Sevgilerimle.",
        },
        'speaking_prompt': {'sentences': ['Bugün çok mutluyum.', 'Seni özledim.', 'Biraz üzgünüm.']},
    },
    'test': [
        mcq("'mutlu' so'zining ma'nosi nima?", ["Baxtli", "Xafa", "Jahldor", "Qo'rqqan"], 0),
        mcq("'üzgün' so'zining ma'nosi nima?", ["Xafa", "Baxtli", "Xursand", "Xotirjam"], 0),
        mcq("Turk mektubi odatda qanday boshlanadi?", ["'Sevgili...' bilan", "'Hoşça kal' bilan", "Raqam bilan", "Sana bilan"], 0),
        mcq("'özlemek' fe'li nima?", ["Sog'inmoq", "Unutmoq", "Yozmoq", "O'qimoq"], 0),
        mcq("'Seni özledim' qanday tarjima qilinadi?", ["Men seni sog'indim", "Men senga achinaman", "Men seni yaxshi ko'raman", "Men senga xafaman"], 0),
        mcq("'son derece' so'zi hissiyotni qanday kuchaytiradi?", ["Nihoyatda (kuchli, rasmiyroq)", "Juda oz", "O'rtacha", "Umuman kuchaytirmaydi"], 0),
        mcq("'şaşkın' so'zining ma'nosi nima?", ["Hayron", "Xursand", "Charchagan", "Uyqusiz"], 0),
    ],
})

sections[5]['topics'].append({
    'key': 'u6b', 'title': "B. Mutlu Olmak — -(y)Abil- (qobiliyat/imkoniyat)",
    'start_page': 17, 'end_page': 17,
    'explanation': {
        'goals': ["-(y)Abil- (qila olish/imkoniyat) qo'shimchasini o'rganish", "Uning olumsuz shaklini (-(y)AmA-) bilish"],
        'blocks': [
            block(
                "-(y)Abil-: qila olish/imkoniyat",
                "**-(y)Abil-** fe'lga qo'shilib, ==\"qila olish\" (qobiliyat) yoki \"mumkin "
                "bo'lish\" (imkoniyat)== ma'nosini beradi - o'zbekchadagi \"-a olmoq\"ga "
                "to'g'ri keladi:\n\n"
                "- **Bu işi başarabilirim.** = Men bu ishni uddasidan chiqa olaman.\n"
                "- **Yarın gelebilir misin?** = Ertaga kela olasanmi?\n\n"
                "Qo'shish qoidasi: fe'l tub (undosh bilan tugasa +ebil/abil, unli bilan "
                "tugasa +yebil/yabil) + zamon + shaxs: gel+ebil+ir+im = **gelebilirim**.",
            ),
            block(
                "Olumsuz shakl: -(y)AmA-",
                "Diqqat: -(y)Abil-ning olumsuzi ==-(y)Abil+mez EMAS==, balki butunlay boshqa "
                "**-(y)AmA-** shaklidan foydalaniladi:\n\n"
                "- **Bunu yapamam.** = Buni qila olmayman. (yap+ama+m)\n"
                "- **Gelemem.** = Kela olmayman. (gel+eme+m)\n\n"
                "Bu turk tilidagi eng muhim istisnolardan biri - ==\"qila olmaslik\" uchun "
                "alohida qo'shimcha== ishlatiladi, oddiy \"-mez\" bilan emas.",
            ),
        ],
        'key_facts': [
            fact("-(y)Abil- = qila olish/imkoniyat ('...a olmoq')."), fact("Olumsuz shakl -(y)AmA- (masalan: yapamam, gelemem), -abil+mez EMAS."),
        ],
        'summary': "**-(y)Abil-** = qila olish (gelebilirim - kela olaman); olumsuzi **-(y)AmA-** (gelemem - kela olmayman).",
        'vocabulary': [
            voc('mutlu olmak', 'baxtli bo\'lmoq', 'Mutlu olmak için gülümsemeliyiz.', "Baxtli bo'lish uchun tabassum qilishimiz kerak."),
            voc('gülmek', 'kulmoq', 'Çok güldük.', "Ko'p kuldik."),
            voc('gülümsemek', 'tabassum qilmoq', 'Bana gülümsedi.', 'Menga tabassum qildi.'),
            voc('eğlenmek', "yayramoq/zavqlanmoq", 'Çok eğlendik.', "Ko'p yayradik."),
            voc('başarmak', "uddasidan chiqmoq", 'Bu işi başarabilirim.', "Men bu ishni uddasidan chiqa olaman."),
            voc('hayal', 'orzu/xayol', 'Hayalimi gerçekleştirdim.', "Orzuimni ro'yobga chiqardim."),
            voc('umut', 'umid', 'Umudumu kaybetmedim.', "Umidimni yo'qotmadim."),
            voc('pes etmek', 'taslim bo\'lmoq', 'Asla pes etmem.', "Men hech qachon taslim bo'lmayman."),
            voc('inanmak', 'ishonmoq', 'Kendime inanıyorum.', "O'zimga ishonaman."),
            voc('gerçekleştirmek', "ro'yobga chiqarmoq", 'Hayalimi gerçekleştirdim.', "Orzuimni ro'yobga chiqardim."),
        ],
        'listening': {
            'dialogue': [
                dialogue_line('Deniz', "Yarın toplantıya gelebilir misin?"),
                dialogue_line('Ece', "Maalesef gelemem, çok işim var."),
                dialogue_line('Deniz', 'Peki, sonraki hafta gelebilir misin?'),
                dialogue_line('Ece', 'Evet, o zaman gelebilirim.'),
            ],
            'questions': [
                mcq('Ece yarın gelebilir mi?', ['Hayır, gelemez', 'Evet, gelebilir', 'Belki gelir', 'Hiç cevap vermedi'], 0),
                mcq('Ece ne zaman gelebilir?', ['Sonraki hafta', 'Yarın', 'Bugün', 'Hiçbir zaman'], 0),
            ],
        },
        'reading': {
            'title': 'Hayallerime Ulaşabilirim',
            'text': "Küçükken doktor olmak istiyordum. Şimdi üniversitede tıp okuyorum ve "
                    "hayalime yaklaşıyorum. Zor günler oldu, bazen başaramayacağımı "
                    "düşündüm ve pes etmek istedim. Ama ailem bana her zaman "
                    "destek oldu ve kendime tekrar inanmayı öğrendim. Şimdi "
                    "anlıyorum ki, zorluklar aslında bizi güçlendiriyor. Hayallerime "
                    "ulaşabileceğime inanıyorum, çünkü artık hiçbir zorluk beni "
                    "durduramaz.",
            'questions': [
                mcq('Yazar küçükken ne olmak istiyordu?', ['Doktor', "Öğretmen", 'Sporcu', 'Yazar'], 0),
                mcq("Yazar neye inanıyor?", ["Hayallerine ulaşabileceğine", "Hiçbir şeye ulaşamayacağına", "Okulun gereksiz olduğuna", "Pes etmesi gerektiğine"], 0),
                mcq('Yazara göre zorluklar ne yapar?', ['Bizi güçlendirir', 'Bizi zayıflatır', 'Hiçbir etkisi yok', "Bizi durdurur"], 0),
                mcq('Zor günlerde yazara kim destek oldu?', ['Ailesi', "Hiç kimse", 'Sadece kendisi', "Öğretmeni"], 0),
            ],
        },
        'sentence_practice': [
            choice("'Bunu yap___' (qila olmayman, olumsuz)", ['amam', 'abilirim', 'ıyorum', 'acağım'], 0),
            choice("'Yarın gel___ misin?' (kela olasanmi)", ['ebilir', 'emez', 'di', 'ecek'], 0),
            order("Cümleyi doğru sıraya dizin: 'Bu işi başarabilirim'", ['Bu', 'işi', 'başarabilirim']),
            choice("-(y)Abil- ning olumsuz shakli qaysi?", ['-(y)AmA-', '-(y)Abilmez', '-mIş', '-(y)AcAk'], 0),
        ],
        'writing_prompt': {
            'instruction': "-(y)Abil- va -(y)AmA- shakllarini ishlatib, o'z qobiliyatlaringiz haqida 2 gap yozing.",
            'sample_answer': "Türkçe konuşabilirim ama çok hızlı yazamam.",
        },
        'speaking_prompt': {'sentences': ['Bu işi başarabilirim.', 'Yarın gelemem.', 'Hayallerime ulaşabilirim.']},
    },
    'test': [
        mcq("'-(y)Abil-' qo'shimchasi nimani bildiradi?", ["Qila olish/imkoniyat", "O'tgan zamon", "Kelasi zamon", "Buyruq"], 0),
        mcq("'-(y)Abil-'ning olumsuz shakli qaysi?", ["-(y)AmA-", "-(y)Abilmez", "-mIş", "-(y)Or"], 0),
        mcq("'Bunu yapamam' qanday tarjima qilinadi?", ["Buni qila olmayman", "Buni qilaman", "Buni qildim", "Buni qilmoqchiman"], 0),
        mcq("'Gelebilir misin?' qanday tarjima qilinadi?", ["Kela olasanmi?", "Kelding mi?", "Kelasanmi (oddiy)?", "Kelmaysanmi?"], 0),
        mcq("'başarmak' fe'li nima?", ["Uddasidan chiqmoq", "Boshlamoq", "Tugatmoq", "Unutmoq"], 0),
        mcq("'pes etmek' iborasi nima?", ["Taslim bo'lmoq", "G'alaba qozonmoq", "Boshlamoq", "Kutmoq"], 0),
        mcq("'inanmak' fe'li nima?", ["Ishonmoq", "Shubhalanmoq", "Unutmoq", "Qo'rqmoq"], 0),
        fill_blank("'Bu işi başar___' (uddasidan chiqa olaman, 1-shaxs)", 'abilirim'),
    ],
})

sections[5]['topics'].append({
    'key': 'u6c', 'title': "C. Gülelim, Eğlenelim!", 'start_page': 18, 'end_page': 18,
    'explanation': {
        'goals': ["Hazil va o'yin-kulgi lug'atini o'rganish", "Bayram va tantana haqida gapirish"],
        'blocks': [
            block(
                "Hazil va kulgi",
                "**Şaka** (hazil) - har qanday madaniyatda muloqotni yengillashtiradi. "
                "Turkchada \"**Şaka yapıyorum!**\" (Hazillashyapman!) - jiddiy gapdan keyin "
                "\"bu hazil edi\" deb tushuntirish uchun ishlatiladi.",
            ),
            block(
                "Bayram va tantana",
                "**Parti**, **kutlama** (tantana) so'zlari va \"**Doğum günün kutlu "
                "olsun!**\" (Tug'ilgan kuning muborak bo'lsin!) kabi tabrik iboralari "
                "==quvonchli lahzalarni ifodalash== uchun ishlatiladi.",
            ),
        ],
        'key_facts': [
            fact("'Şaka yapıyorum' - hazillashganingizni bildirish uchun ishlatiladi."),
            fact("'Doğum günün kutlu olsun!' - tug'ilgan kun tabrigi."),
        ],
        'summary': "Kulgi va bayram lug'ati: **şaka, komik, eğlence, parti, kutlamak**.",
        'vocabulary': [
            voc('şaka', 'hazil', 'Şaka yapıyorum!', 'Hazillashyapman!'),
            voc('komik', 'kulgili', 'Bu film çok komik.', 'Bu film juda kulgili.'),
            voc('eğlence', "o'yin-kulgi", 'Bu parti çok eğlenceli.', "Bu ziyofat juda quvnoq."),
            voc('parti', 'ziyofat', 'Bu akşam bir parti var.', 'Bugun kechqurun ziyofat bor.'),
            voc('kutlamak', 'nishonlamoq', 'Doğum günümü kutladık.', "Tug'ilgan kunimni nishonladik."),
            voc('neşeli', 'quvnoq', 'Herkes çok neşeliydi.', "Hamma juda quvnoq edi."),
            voc('sürpriz', 'syurpriz', 'Ona sürpriz yaptık.', "Unga syurpriz qildik."),
            voc('hediye', 'sovg\'a', 'Ona bir hediye aldım.', "Unga sovg'a oldim."),
            voc('davet etmek', 'taklif qilmoq', 'Onu partiye davet ettim.', "Uni ziyofatga taklif qildim."),
        ],
        'listening': {
            'dialogue': [
                dialogue_line('Can', "Yarın benim doğum günüm, parti veriyorum!"),
                dialogue_line('Ela', 'Harika! Kaç kişi geliyor?'),
                dialogue_line('Can', 'Yaklaşık yirmi arkadaş. Çok eğlenceli olacak.'),
                dialogue_line('Ela', 'Doğum günün şimdiden kutlu olsun!'),
            ],
            'questions': [
                mcq('Yarın ne var?', ["Can'ın doğum günü", "Okul", 'Sınav', 'Tatil'], 0),
                mcq('Partiye kaç kişi geliyor?', ['Yaklaşık yirmi', 'Beş', 'Yüz', 'İki'], 0),
            ],
        },
        'reading': {
            'title': 'Unutulmaz Bir Parti',
            'text': "Geçen hafta arkadaşımın doğum günü partisine gittim. Aslında bu bir "
                    "sürprizdi - arkadaşım hiçbir şeyden haberi yokken, hepimiz onu davet "
                    "ettiğimiz evde gizlice bekledik. Kapıdan girdiğinde herkes birden "
                    "\"Sürpriz!\" diye bağırdı, o da çok şaşırdı ve güldü. Herkes çok "
                    "neşeliydi. Komik şakalar yaptık, müzik dinledik ve dans ettik. Pasta "
                    "kesildiğinde herkes birlikte şarkı söyledi ve herkes ona güzel "
                    "hediyeler verdi. Gerçekten unutulmaz bir eğlenceydi.",
            'questions': [
                mcq('Yazar nereye gitti?', ["Doğum günü partisine", "Okula", 'İşe', 'Hastaneye'], 0),
                mcq('Pasta kesildiğinde ne yaptılar?', ['Şarkı söylediler', 'Ağladılar', 'Uyudular', 'Eve gittiler'], 0),
                mcq('Parti aslında ne türdeydi?', ['Sürpriz parti', 'Sıradan bir akşam yemeği', 'İş toplantısı', 'Okul etkinliği'], 0),
                mcq("Arkadaşı kapıdan girince ne yaptı?", ['Şaşırdı ve güldü', 'Ağladı', 'Hiçbir şey hissetmedi', 'Kızdı'], 0),
            ],
        },
        'sentence_practice': [
            choice("'Şaka ___' (hazillashyapman)", ['yapıyorum', 'yaptım', 'yapacağım', 'yapmam'], 0),
            choice("Tug'ilgan kun tabrigi qanday aytiladi?", ["Doğum günün kutlu olsun!", "Afiyet olsun!", "Geçmiş olsun!", "Hoşça kal!"], 0),
            order("Cümleyi doğru sıraya dizin: 'Bu parti çok eğlenceli'", ['Bu', 'parti', 'çok', 'eğlenceli']),
        ],
        'writing_prompt': {
            'instruction': "O'tkazgan quvnoq bir kechangiz (parti/bayram) haqida 3 gap yozing.",
            'sample_answer': "Geçen hafta bir doğum günü partisine gittim. Çok eğlendik, müzik dinledik ve dans ettik.",
        },
        'speaking_prompt': {'sentences': ['Şaka yapıyorum!', 'Doğum günün kutlu olsun!', 'Bu çok eğlenceli.']},
    },
    'test': [
        mcq("'Şaka yapıyorum' nima uchun aytiladi?", ["Hazillashganini bildirish uchun", "Jiddiy gapni tasdiqlash uchun", "Xayrlashish uchun", "Tabriklash uchun"], 0),
        mcq("'komik' so'zining ma'nosi nima?", ["Kulgili", "Jiddiy", "Xafa", "Qo'rqinchli"], 0),
        mcq("'Doğum günün kutlu olsun!' qanday tarjima qilinadi?", ["Tug'ilgan kuning muborak bo'lsin!", "Xayrli tong!", "Yoqimli ishtaha!", "Tuzalib keting!"], 0),
        mcq("'eğlence' so'zi nima?", ["O'yin-kulgi", "Ish", "Maktab", "Kasallik"], 0),
        mcq("'neşeli' so'zining ma'nosi nima?", ["Quvnoq", "Xafa", "Charchagan", "Uyqusiz"], 0),
        mcq("'sürpriz' so'zi nima?", ["Syurpriz", "Sovg'a", "Bayram", "Taklif"], 0),
        mcq("'davet etmek' fe'li nima?", ["Taklif qilmoq", "Kutmoq", "Unutmoq", "Rad etmoq"], 0),
    ],
})

# ============================================================
# 7-UNITE: TEKNOLOJI VE ILETISIM
# ============================================================
sections.append({'key': 'u7', 'title': "7-ünite. Teknoloji ve İletişim", 'topics': []})

sections[6]['topics'].append({
    'key': 'u7a', 'title': "A. Elektrikli Ev Eşyaları — -mAk için / -mAk üzere",
    'start_page': 19, 'end_page': 19,
    'explanation': {
        'goals': ["-mAk için (maqsad bildirish) qurilmasini o'rganish", "-mAk üzere ('...ga yaqin/uchun') qurilmasini bilish", "Maishiy elektr texnika lug'ati"],
        'blocks': [
            block(
                "-mAk için: maqsad bildirish",
                "**-mAk için** = \"...qilish uchun\" - biror harakatning **maqsadini** "
                "bildiradi:\n\n"
                "- **Çamaşır yıkamak için makineyi çalıştırdım.** = Kir yuvish uchun "
                "mashinani ishga tushirdim.\n"
                "- **Yemek pişirmek için fırını açtım.** = Ovqat pishirish uchun pechni "
                "yoqdim.\n\n"
                "Bu qurilma o'zbekchadagi \"...ish uchun\" ga to'g'ridan-to'g'ri mos keladi.",
            ),
            block(
                "-mAk üzere: 'deyarli...', 'aynan shu payt'",
                "**-mAk üzere** ikki xil ma'noda ishlatiladi:\n\n"
                "1. \"...ga yaqin, deyarli\": **Tam çıkmak üzereyken telefon çaldı.** = Aynan "
                "chiqmoqchi bo'lganimda telefon jiringladi.\n"
                "2. Rasmiy maqsad (yozma tilda): **Bu alet, kolay temizlik yapmak üzere "
                "tasarlanmıştır.** = Bu asbob, oson tozalash uchun ishlab chiqilgan.\n\n"
                "Kundalik nutqda ko'proq **birinchi ma'no** (\"aynan shu payt/deyarli\") "
                "ishlatiladi.",
            ),
        ],
        'key_facts': [
            fact("-mAk için = ...qilish uchun (maqsad)."), fact("-mAk üzere = ...ga yaqin/deyarli, yoki rasmiy maqsad."),
        ],
        'summary': "**-mAk için** - oddiy maqsad ('...uchun'), **-mAk üzere** - 'aynan shu payt' yoki rasmiy maqsad.",
        'vocabulary': [
            voc('buzdolabı', 'muzlatgich', 'Buzdolabı boş.', 'Muzlatgich bo\'sh.'),
            voc('çamaşır makinesi', 'kir yuvish mashinasi', 'Çamaşır makinesini çalıştırdım.', 'Kir yuvish mashinasini ishga tushirdim.'),
            voc('elektrik süpürgesi', "changyutgich", 'Elektrik süpürgesiyle temizledim.', "Changyutgich bilan tozaladim."),
            voc('ütü', 'dazmol', 'Ütü çok sıcak.', 'Dazmol juda issiq.'),
            voc('bulaşık makinesi', 'idish yuvish mashinasi', 'Bulaşık makinesi bozuldu.', "Idish yuvish mashinasi buzildi."),
            voc('çalıştırmak', "ishga tushirmoq", 'Makineyi çalıştırdım.', "Mashinani ishga tushirdim."),
            voc('bozulmak', 'buzilmoq', 'Fırın bozuldu.', "Pech buzildi."),
            voc('tamir etmek', "ta'mirlamoq", 'Ustayı çağırıp tamir ettirdim.', "Ustani chaqirib ta'mirlattirdim."),
            voc('fiş (elektrik)', 'shtepsel', 'Fişi prize taktım.', "Shtepselni rozetkaga taqdim."),
            voc('enerji tasarrufu', "energiya tejash", "Bu makine enerji tasarrufu sağlıyor.", "Bu mashina energiya tejashga yordam beradi."),
        ],
        'listening': {
            'dialogue': [
                dialogue_line('Elif', 'Neden mutfaktasın?'),
                dialogue_line('Burak', "Yemek pişirmek için fırını açtım."),
                dialogue_line('Elif', 'Ben de çamaşır yıkamak için makineyi çalıştıracağım.'),
                dialogue_line('Burak', 'İyi fikir, ikimiz de meşgul olacağız.'),
            ],
            'questions': [
                mcq('Burak neden fırını açtı?', ['Yemek pişirmek için', 'Isınmak için', 'Temizlik için', 'Kurutmak için'], 0),
                mcq('Elif ne yapacak?', ['Çamaşır yıkayacak', 'Yemek yapacak', 'Uyuyacak', 'Dışarı çıkacak'], 0),
            ],
        },
        'reading': {
            'title': 'Ev İşleri',
            'text': "Her sabah evi temizlemek için elektrik süpürgesini kullanırım. Sonra "
                    "çamaşır yıkamak için makineyi çalıştırırım. Geçen hafta çamaşır "
                    "makinesi aniden bozuldu, bu yüzden bir usta çağırıp tamir ettirmek "
                    "zorunda kaldım. Usta geldiğinde sorunun basit bir fiş problemi "
                    "olduğunu söyledi. Yeni makineler eskilere göre çok daha az enerji "
                    "tüketiyor - alışveriş yaparken artık herkes enerji tasarrufuna dikkat "
                    "ediyor. Tam işimi bitirmek üzereyken telefonum çaldı. Arkadaşım kahve "
                    "içmeye davet etti.",
            'questions': [
                mcq('Evi temizlemek için ne kullanılıyor?', ['Elektrik süpürgesi', 'Fırın', 'Buzdolabı', 'Ütü'], 0),
                mcq('Telefon ne zaman çaldı?', ['İşi bitirmek üzereyken', 'Sabah erken', 'Uyurken', 'Yemek yerken'], 0),
                mcq('Çamaşır makinesine ne oldu?', ['Bozuldu', 'Kayboldu', 'Satıldı', "Hiçbir şey"], 0),
                mcq('Usta sorunun ne olduğunu söyledi?', ['Basit bir fiş problemi', "Motor arızası", "Hiçbir sorun yok", "Yeni makine gerektiğini"], 0),
            ],
        },
        'sentence_practice': [
            choice("'Yemek piş___ için fırını açtım' (pishirish uchun)", ['irmek', 'iriyor', 'irdi', 'irecek'], 0),
            choice("'Tam çık___ telefon çaldı' (chiqmoqchi bo'lgan payt)", ['mak üzereyken', 'mak için', 'madan', 'tıktan sonra'], 0),
            order("Cümleyi doğru sıraya dizin: 'Çamaşır yıkamak için makineyi çalıştırdım'", ['Çamaşır', 'yıkamak', 'için', 'makineyi', 'çalıştırdım']),
        ],
        'writing_prompt': {
            'instruction': "-mAk için qurilmasini ishlatib, uy ishlari haqida 2 gap yozing.",
            'sample_answer': "Evi temizlemek için elektrik süpürgesini kullandım. Yemek pişirmek için fırını açtım.",
        },
        'speaking_prompt': {'sentences': ['Çamaşır yıkamak için makineyi çalıştırdım.', 'Yemek pişirmek için fırını açtım.', 'Tam çıkmak üzereyken telefon çaldı.']},
    },
    'test': [
        mcq("'-mAk için' qanday ma'no beradi?", ["...qilish uchun (maqsad)", "...qilgandan keyin", "...qilishdan oldin", "...qilish bilan"], 0),
        mcq("'-mAk üzere' ning kundalik nutqdagi asosiy ma'nosi nima?", ["Aynan shu payt/deyarli", "O'tgan zamon", "Kelasi hafta", "Har doim"], 0),
        mcq("'Çamaşır yıkamak için' qanday tarjima qilinadi?", ["Kir yuvish uchun", "Kir yuvgandan keyin", "Kir yuvmasdan", "Kir yuvish bilan"], 0),
        mcq("'buzdolabı' so'zi nima?", ["Muzlatgich", "Dazmol", "Pech", "Changyutgich"], 0),
        mcq("'Tam çıkmak üzereyken telefon çaldı' jumlasi nimani bildiradi?", ["Chiqmoqchi bo'lgan aynan o'sha payt", "Chiqib bo'lgandan keyin", "Chiqishdan ancha oldin", "Hech qachon chiqmagan"], 0),
        mcq("'tamir etmek' fe'li nima?", ["Ta'mirlamoq", "Sotib olmoq", "Sotmoq", "Tashlamoq"], 0),
        mcq("'enerji tasarrufu' iborasi nima?", ["Energiya tejash", "Energiya sarflash", "Elektr toki", "Elektr narxi"], 0),
    ],
})

sections[6]['topics'].append({
    'key': 'u7b', 'title': "B. Büyülü Cam - Televizyon", 'start_page': 20, 'end_page': 20,
    'explanation': {
        'goals': ["Televizyon va OAV lug'atini o'rganish", "Sevimli dastur haqida gapirish"],
        'blocks': [
            block(
                "Büyülü cam nima?",
                "\"**Büyülü cam**\" (sehrli oyna) - televizorga nisbatan ishlatiladigan "
                "she'riy ibora, chunki u ==dunyoning istalgan burchagidan xabar va "
                "ko'ngilochar dasturlarni== uyingizga olib keladi.",
            ),
            block(
                "TV dasturlari haqida gapirish",
                "- **haber** (yangilik) - **dizi** (serial) - **belgesel** (hujjatli film) - "
                "**yarışma programı** (viktorina dasturi)\n"
                "- **Hangi kanalı izliyorsun?** = Qaysi kanalni ko'ryapsan?\n"
                "- **Bu dizi çok ilginç.** = Bu serial juda qiziqarli.\n\n"
                "TV haqida gapirishda **izlemek** (ko'rmoq/tomosha qilmoq) fe'li "
                "\"görmek\"dan farqli - maxsus \"dastur/film ko'rish\" ma'nosida ishlatiladi.",
            ),
        ],
        'key_facts': [
            fact("'Büyülü cam' - televizorga nisbatan ishlatiladigan she'riy ibora."),
            fact("'izlemek' - dastur/film 'tomosha qilish' ma'nosida ishlatiladi."),
        ],
        'summary': "TV lug'ati: **haber, dizi, belgesel, yarışma programı** - va 'izlemek' (tomosha qilish) fe'li.",
        'vocabulary': [
            voc('televizyon', 'televizor', 'Televizyon izliyorum.', "Televizor ko'ryapman."),
            voc('haber', 'yangilik (allaqachon o\'rgangan)', 'Haberleri izledim.', 'Yangiliklarni ko\'rdim.'),
            voc('dizi', 'serial', 'Bu dizi çok popüler.', 'Bu serial juda mashhur.'),
            voc('belgesel', 'hujjatli film', 'Belgesel izlemeyi severim.', "Hujjatli film ko'rishni yaxshi ko'raman."),
            voc('kanal', 'kanal', 'Hangi kanalı izliyorsun?', 'Qaysi kanalni ko\'ryapsan?'),
            voc('izlemek', "tomosha qilmoq", 'Film izledim.', "Film ko'rdim."),
            voc('reklam', 'reklama', 'Reklamlar çok uzun sürüyor.', "Reklamalar juda uzoq davom etadi."),
            voc('yayın', 'efir/translyatsiya', 'Canlı yayın izliyoruz.', "Jonli efirni tomosha qilyapmiz."),
            voc('ekran', 'ekran', 'Büyük bir ekranı var.', "Uning katta ekrani bor."),
        ],
        'listening': {
            'dialogue': [
                dialogue_line('Baba', 'Hangi kanalı izliyorsun?'),
                dialogue_line('Oğul', 'Bir belgesel izliyorum, hayvanlar hakkında.'),
                dialogue_line('Baba', 'İlginç mi?'),
                dialogue_line('Oğul', 'Evet, çok bilgilendirici.'),
            ],
            'questions': [
                mcq('Oğul ne izliyor?', ['Belgesel', 'Haber', 'Dizi', 'Yarışma programı'], 0),
                mcq('Belgesel ne hakkında?', ['Hayvanlar', 'Tarih', 'Spor', 'Müzik'], 0),
            ],
        },
        'reading': {
            'title': 'Televizyon Alışkanlıklarımız',
            'text': "Ailem her akşam birlikte televizyon izler. Babam haberleri, annem "
                    "dizileri sever. Ben ise belgesel izlemeyi tercih ederim. Bazen hep "
                    "birlikte bir yarışma programı izleyip eğleniriz. Eskiden televizyonda "
                    "sadece birkaç kanal vardı, ama şimdi yüzlerce kanal ve canlı yayın "
                    "seçeneği var. Bence en can sıkıcı şey, ilginç bir dizi izlerken "
                    "reklamların çok uzun sürmesi. Yeni televizyonların ekranı da eskilere "
                    "göre çok daha büyük ve net.",
            'questions': [
                mcq('Baba ne izlemeyi sever?', ['Haberleri', 'Dizileri', 'Belgesel', 'Spor'], 0),
                mcq('Aile bazen birlikte ne izler?', ['Yarışma programı', 'Sadece haber', 'Hiçbir şey', 'Film değil'], 0),
                mcq('Yazara göre en can sıkıcı şey nedir?', ['Reklamların uzun sürmesi', 'Kanalların azlığı', 'Ekranın küçük olması', 'Ailesinin televizyon izlememesi'], 0),
                mcq('Eskiden televizyonda ne kadar kanal vardı?', ['Birkaç kanal', 'Yüzlerce kanal', 'Hiç kanal yoktu', 'Binlerce kanal'], 0),
            ],
        },
        'sentence_practice': [
            choice("'Büyülü cam' nimani anglatadi?", ['Televizor', 'Telefon', 'Kompyuter', 'Radio'], 0),
            choice("'Hangi kanalı ___?' (ko'ryapsan)", ['izliyorsun', 'izledin', 'izleyeceksin', 'izlemez'], 0),
            order("Cümleyi doğru sıraya dizin: 'Bu dizi çok ilginç'", ['Bu', 'dizi', 'çok', 'ilginç']),
        ],
        'writing_prompt': {
            'instruction': "Sevimli TV dasturingiz haqida 2-3 gap yozing.",
            'sample_answer': "En sevdiğim program bir belgesel programı. Hayvanlar hakkında çok şey öğreniyorum.",
        },
        'speaking_prompt': {'sentences': ['Hangi kanalı izliyorsun?', 'Bu dizi çok ilginç.', 'Belgesel izlemeyi severim.']},
    },
    'test': [
        mcq("'Büyülü cam' iborasi nimani anglatadi?", ["Televizor", "Oyna", "Telefon", "Deraza"], 0),
        mcq("'dizi' so'zi nima?", ["Serial", "Yangilik", "Hujjatli film", "Sport"], 0),
        mcq("'belgesel' so'zi nima?", ["Hujjatli film", "Komediya", "Musiqa", "Yangilik"], 0),
        mcq("'izlemek' fe'li TV kontekstida nima?", ["Tomosha qilmoq", "Eshitmoq", "O'qimoq", "Yozmoq"], 0),
        mcq("'Hangi kanalı izliyorsun?' savoli nima haqida?", ["Qaysi kanal ko'rilyapti", "Qayerga borilyapti", "Kim keldi", "Necha soat"], 0),
        mcq("'reklam' so'zi nima?", ["Reklama", "Yangilik", "Serial", "Kanal"], 0),
        mcq("'yayın' so'zi nima?", ["Efir/translyatsiya", "Ekran", "Pult", "Ovoz"], 0),
    ],
})

sections[6]['topics'].append({
    'key': 'u7c', 'title': "C. Bitkiler, Hayvanlar ve Biz — ...diye sormak / ...diye cevap vermek",
    'start_page': 21, 'end_page': 21,
    'explanation': {
        'goals': ["'...diye sormak' va '...diye cevap vermek' qurilmalarini o'rganish", "O'simlik va hayvonlar lug'atini bilish"],
        'blocks': [
            block(
                "'...diye sormak': savolni to'g'ridan-to'g'ri keltirish",
                "Kimningdir aynan qanday so'z bilan so'raganini keltirmoqchi bo'lsangiz, "
                "==so'zma-so'z savolni tirnoqqa olib, keyin \"diye sordu\"== qo'shasiz:\n\n"
                "**\"Bu çiçek nedir?\" diye sordu.** = \"Bu gul nima?\" deb so'radi.\n\n"
                "\"diye\" so'zi bu yerda o'zbekchadagi \"deb\" ga aynan mos keladi - ==so'zlarni "
                "o'zgartirmasdan, aynan qanday aytilganini== bildiradi.",
            ),
            block(
                "'...diye cevap vermek': javobni keltirish",
                "Xuddi shunday qurilma javob berish uchun ham ishlatiladi:\n\n"
                "**\"Bu bir gül,\" diye cevap verdim.** = \"Bu atirgul,\" deb javob berdim.\n\n"
                "Bu qurilma ==tabiat, hayvonot va o'simliklar haqidagi suhbatlarni== "
                "tasvirlashda juda foydali - masalan bolalar kitoblari yoki suhbatlarda "
                "tez-tez uchraydi.",
            ),
        ],
        'key_facts': [
            fact("'...diye sordu' = '...deb so'radi' (so'zma-so'z savol keltirish)."),
            fact("'...diye cevap verdi' = '...deb javob berdi' (so'zma-so'z javob keltirish)."),
        ],
        'summary': "**\"...\" diye sordu/cevap verdi** - o'zbekchadagi \"...deb so'radi/javob berdi\" ga mos keladi.",
        'vocabulary': [
            voc('bitki', "o'simlik", 'Bu bitki çok güzel.', "Bu o'simlik juda chiroyli."),
            voc('hayvan', 'hayvon', 'Hayvanları severim.', 'Hayvonlarni yaxshi ko\'raman.'),
            voc('doğa', 'tabiat', 'Doğayı korumalıyız.', 'Tabiatni asrashimiz kerak.'),
            voc('çiçek', 'gul', 'Bu çiçek çok güzel kokuyor.', "Bu gul juda yoqimli hid keladi."),
            voc('ağaç', 'daraxt', 'Bahçede bir ağaç var.', "Bog'da bir daraxt bor."),
            voc('kuş', "qush", 'Kuşlar çok güzel öter.', "Qushlar juda chiroyli sayraydi."),
            voc('böcek', "hasharot", 'Bahçede küçük bir böcek gördüm.', "Bog'da kichkina hasharot ko'rdim."),
            voc('yuva', 'uya', 'Kuşun yuvası ağaçta.', "Qushning uyasi daraxtda."),
            voc('tür', "tur (biologik)", 'Bu nadir bir hayvan türü.', "Bu noyob hayvon turi."),
            voc('nesli tükenmek', "yo'q bo'lib ketmoq (tur haqida)", 'Bu tür nesli tükenmekte olan bir hayvandır.', "Bu tur yo'q bo'lib ketayotgan hayvondir."),
        ],
        'listening': {
            'dialogue': [
                dialogue_line('Çocuk', '"Bu ağaç kaç yaşında?" diye sordu.'),
                dialogue_line('Baba', '"Yüz yaşında," diye cevap verdi.'),
                dialogue_line('Çocuk', '"Peki bu kuş neden burada?" diye sordu.'),
                dialogue_line('Baba', '"Yuvası bu ağaçta," diye cevap verdi.'),
            ],
            'questions': [
                mcq('Çocuk ağaç hakkında ne sordu?', ['Kaç yaşında olduğunu', 'Nerede olduğunu', 'Rengini', 'Boyunu'], 0),
                mcq('Kuşun yuvası nerede?', ['O ağaçta', 'Evde', 'Gökyüzünde', 'Suda'], 0),
            ],
        },
        'reading': {
            'title': 'Doğada Bir Gün',
            'text': "Ormanda yürürken küçük kardeşim \"Bu çiçek nedir?\" diye sordu. Ben de "
                    "\"Bu bir papatya,\" diye cevap verdim. Sonra bir kuş gördük, yuvası "
                    "yüksek bir ağaçtaydı. \"Bu kuş neden şarkı söylüyor?\" diye sordu. "
                    "\"Belki mutludur,\" diye cevap verdim. Biraz sonra küçük bir böcek "
                    "gördük, kardeşim onu incitmeden dikkatlice inceledi. Rehberimiz bize "
                    "bu ormanda bazı nadir hayvan türlerinin yaşadığını, hatta bazılarının "
                    "nesli tükenmekte olduğunu anlattı. Bu yüzden doğayı korumamız gerektiğini "
                    "bir kez daha anladık.",
            'questions': [
                mcq('Kardeş ilk ne sordu?', ["Çiçeğin ne olduğunu", "Kuşun adını", "Ormanın adını", "Saatin kaç olduğunu"], 0),
                mcq('Yazar kuş hakkında ne dedi?', ["Belki mutludur", "Belki hastadır", "Belki açtır", "Belki uykusuzdur"], 0),
                mcq('Rehber ormandaki hayvanlar hakkında ne anlattı?', ['Bazılarının nesli tükenmekte olduğunu', 'Hiç hayvan olmadığını', 'Hepsinin güvende olduğunu', 'Hepsinin yeni geldiğini'], 0),
                mcq('Kardeş böceği nasıl inceledi?', ['İncitmeden dikkatlice', 'Hemen ezerek', 'Hiç bakmadan', "Korkarak kaçarak"], 0),
            ],
        },
        'sentence_practice': [
            choice("'\"Bu nedir?\" ___ sordu' (deb)", ['diye', 'için', 'gibi', 'kadar'], 0),
            choice("'...diye cevap vermek' nimani bildiradi?", ["So'zma-so'z javobni keltirish", "Savol berish", "Buyruq berish", "Xayrlashish"], 0),
            order("Cümleyi doğru sıraya dizin: 'Bu bir gül, diye cevap verdim'", ['Bu', 'bir', 'gül,', 'diye', 'cevap', 'verdim']),
        ],
        'writing_prompt': {
            'instruction': "'...diye sordu' va '...diye cevap verdi' qurilmalarini ishlatib, tabiat haqida qisqa dialog yozing.",
            'sample_answer': "\"Bu ağaç ne kadar eski?\" diye sordum. \"Çok eski,\" diye cevap verdi.",
        },
        'speaking_prompt': {'sentences': ['"Bu nedir?" diye sordu.', '"Bu bir çiçek," diye cevap verdim.', 'Doğayı korumalıyız.']},
    },
    'test': [
        mcq("'...diye sordu' qanday ma'no beradi?", ["...deb so'radi", "...deb javob berdi", "...deb yozdi", "...deb kuldi"], 0),
        mcq("'...diye cevap verdi' qanday ma'no beradi?", ["...deb javob berdi", "...deb so'radi", "...deb qichqirdi", "...deb kuldi"], 0),
        mcq("'diye' so'zi o'zbekchada nimaga mos keladi?", ["deb", "va", "yoki", "lekin"], 0),
        mcq("'ağaç' so'zi nima?", ["Daraxt", "Gul", "Qush", "O'simlik (umumiy)"], 0),
        mcq("'doğa' so'zi nima?", ["Tabiat", "Shahar", "Uy", "Bog'"], 0),
        mcq("'nesli tükenmek' iborasi nimani bildiradi?", ["Tur yo'q bo'lib ketishi", "Tur ko'payishi", "Tur ko'chib ketishi", "Tur uxlashi"], 0),
        mcq("'yuva' so'zi nima?", ["Uya", "Daraxt", "Barg", "Ildiz"], 0),
    ],
})

# ============================================================
# 8-UNITE: INSAN VE TOPLUM
# ============================================================
sections.append({'key': 'u8', 'title': "8-ünite. İnsan ve Toplum", 'topics': []})

sections[7]['topics'].append({
    'key': 'u8a', 'title': "A. Kişilik Tipleri — -An/-En (sifatdosh)",
    'start_page': 22, 'end_page': 22,
    'explanation': {
        'goals': ["-An/-En (sifatdosh, 'qiluvchi/qiladigan') qo'shimchasini o'rganish", "Xarakter-xususiyat lug'atini bilish"],
        'blocks': [
            block(
                "-An/-En: fe'ldan sifat/sifatdosh yasash",
                "**-An/-En** fe'lga qo'shilib, \"...qiluvchi\" yoki \"...qiladigan\" "
                "ma'nosidagi **sifatdosh** yasaydi - o'zbekchadagi \"-adigan/-uvchi\"ga mos "
                "keladi:\n\n"
                "- **koşan adam** = yuguruvchi/yugurayotgan odam (koş+an)\n"
                "- **gülen çocuk** = kuluvchi/kulayotgan bola (gül+en)\n"
                "- **çalışkan öğrenci** = mehnatkash (ishlaydigan) o'quvchi\n\n"
                "Bu qo'shimcha fe'lni ==otdan oldin sifat sifatida== ishlatish imkonini "
                "beradi, xuddi ingilizchadagi \"-ing\" (running man) kabi.",
            ),
            block(
                "Xarakter tasvirlashda qo'llanilishi",
                "Insonning xarakterini tasvirlashda ko'plab **doimiy sifatlar** ham aslida "
                "shu qolipdan kelib chiqqan: **çalışkan** (mehnatkash, çalış+kan - biroz "
                "boshqacha shakl), **konuşkan** (gapiruvchan/suxandon). Lekin oddiy fe'llardan "
                "==bevosita -an/-en bilan== ham sifat yasash mumkin: **düşünen** (o'ylovchi), "
                "**seven** (sevuvchi).",
            ),
            block(
                "Olumsuz shakli: -mAyAn/-meyen",
                "Sifatdoshning ==olumsuz shakli== fe'l tub + **-mAyAn/-meyen** orqali "
                "yasaladi - \"...qilmaydigan\" ma'nosini beradi:\n\n"
                "- **gülmeyen bir adam** = kulmaydigan odam\n"
                "- **çalışmayan bir öğrenci** = ishlamaydigan (mehnatkash bo'lmagan) "
                "o'quvchi\n\n"
                "Diqqat: bu shakl ==-mAz (geniş zaman olumsuzi)dan farqli== - \"gülmez\" "
                "(kulmaydi, fe'l) va \"gülmeyen\" (kulmaydigan, sifat sifatida otdan oldin "
                "keladi) grammatik vazifasi bo'yicha farqlanadi.",
            ),
        ],
        'key_facts': [
            fact("-An/-En = '...qiluvchi/qiladigan' (sifatdosh, fe'ldan sifat yasaydi)."),
            fact("Masalan: koşan (yuguruvchi), gülen (kuluvchi), seven (sevuvchi)."),
            fact("Olumsuz shakl -mAyAn/-meyen (masalan: gülmeyen) - -mAz (fe'l)dan farqli."),
        ],
        'summary': "**-An/-En** fe'ldan sifatdosh yasaydi: **koşan** (yuguruvchi), **gülen** (kuluvchi).",
        'vocabulary': [
            voc('kişilik', 'shaxsiyat/xarakter', 'Kişiliği çok güzel.', "Uning xarakteri juda yaxshi."),
            voc('çalışkan', 'mehnatkash', 'Çalışkan bir öğrenciyim.', "Men mehnatkash o'quvchiman."),
            voc('dürüst', 'halol/rostgo\'y', 'Dürüst bir insan her zaman güvenilir.', "Halol odam har doim ishonchli."),
            voc('cömert', "saxiy", 'O çok cömert biri.', "U juda saxiy odam."),
            voc('sabırlı', "sabrli", 'Öğretmenim çok sabırlı.', "O'qituvchim juda sabrli."),
            voc('utangaç', 'uyatchan', 'Kardeşim biraz utangaç.', "Ukam biroz uyatchan."),
            voc('inatçı', "qaysar", 'Kardeşim çok inatçı, fikrini değiştirmez.', "Ukam juda qaysar, fikrini o'zgartirmaydi."),
            voc('alçakgönüllü', 'kamtar', 'Başarılı ama alçakgönüllü biri.', "Muvaffaqiyatli, ammo kamtar odam."),
            voc('kararlı', "qat'iyatli", 'Kararlı bir insan hedefine ulaşır.', "Qat'iyatli odam maqsadiga erishadi."),
            voc('bencil', "xudbin", 'Bencil insanlar sadece kendini düşünür.', "Xudbin odamlar faqat o'zini o'ylaydi."),
        ],
        'listening': {
            'dialogue': [
                dialogue_line('Ayla', 'Yeni öğretmenimiz nasıl biri?'),
                dialogue_line('Deniz', "Çok sabırlı ve dürüst biri."),
                dialogue_line('Ayla', 'Peki sınıf arkadaşımız Ali nasıl?'),
                dialogue_line('Deniz', "O da çok çalışkan ve cömert bir çocuk."),
            ],
            'questions': [
                mcq('Yeni öğretmen nasıl biri?', ['Sabırlı ve dürüst', 'Tembel ve kızgın', 'Utangaç ve sessiz', 'Kötü kalpli'], 0),
                mcq("Ali'nin kişiliği nasıl tarif ediliyor?", ['Çalışkan ve cömert', 'Tembel ve cimri', 'Kızgın ve sabırsız', 'Utangaç ve korkak'], 0),
            ],
        },
        'reading': {
            'title': 'İyi Bir Arkadaş',
            'text': "İyi bir arkadaş dürüst ve sabırlı olmalıdır. Gülen bir yüzle yanınıza "
                    "gelen, sizi dinleyen ve size yardım eden biri gerçek bir arkadaştır. "
                    "Çalışkan ve cömert insanlarla arkadaş olmak hayatı güzelleştirir. Öte "
                    "yandan, sürekli şikâyet eden, başkalarını dinlemeyen ve kendinden "
                    "başkasını düşünmeyen bencil insanlarla arkadaş olmak zor olabilir. "
                    "Kararlı ama alçakgönüllü insanlar genellikle en güvenilir "
                    "arkadaşlardır - onlar başarılarıyla övünmez, ama her zaman yanınızda "
                    "olurlar. İyi bir arkadaş seçmek, hayatınızdaki en önemli "
                    "kararlardan biridir.",
            'questions': [
                mcq("Metne göre iyi arkadaş nasıl olmalı?", ['Dürüst ve sabırlı', 'Kızgın ve bencil', 'Tembel ve sessiz', 'Utangaç ve korkak'], 0),
                mcq("'Sizi dinleyen' ifadesindeki 'dinleyen' hangi anlamda?", ["Tinglovchi (sifatdosh)", "Tingladi", "Tinglaydi", "Tinglamaydi"], 0),
                mcq('Metne göre kimlerle arkadaş olmak zor olabilir?', ['Bencil insanlarla', 'Sabırlı insanlarla', 'Dürüst insanlarla', 'Cömert insanlarla'], 0),
                mcq('En güvenilir arkadaşlar nasıl tarif ediliyor?', ['Kararlı ama alçakgönüllü', 'Bencil ve inatçı', 'Utangaç ve sessiz', "Kızgın ve sabırsız"], 0),
            ],
        },
        'sentence_practice': [
            choice("'koş' fe'lidan 'yuguruvchi' sifatdoshi qaysi?", ['koşan', 'koşuyor', 'koştu', 'koşacak'], 0),
            choice("'gül' fe'lidan 'kuluvchi' sifatdoshi qaysi?", ['gülen', 'gülüyor', 'güldü', 'gülecek'], 0),
            order("Cümleyi doğru sıraya dizin: 'Çalışkan bir öğrenciyim'", ['Çalışkan', 'bir', 'öğrenciyim']),
        ],
        'writing_prompt': {
            'instruction': "-An/-En sifatdoshini ishlatib, do'stingiz xarakterini 2-3 gapda tasvirlang.",
            'sample_answer': "Arkadaşım çok gülen bir insan. Herkesi seven ve yardım eden biridir.",
        },
        'speaking_prompt': {'sentences': ['Çalışkan bir öğrenciyim.', 'Dürüst bir insan her zaman güvenilir.', 'O çok cömert biri.']},
    },
    'test': [
        mcq("'-An/-En' qo'shimchasi nima yasaydi?", ["Sifatdosh ('...qiluvchi')", "Kelasi zamon", "O'tgan zamon", "Ko'plik"], 0),
        mcq("'koşan' so'zi qanday tarjima qilinadi?", ["Yuguruvchi/yugurayotgan", "Yugurdi", "Yuguradi", "Yugurmaydi"], 0),
        mcq("'dürüst' so'zining ma'nosi nima?", ["Halol/rostgo'y", "Yolg'onchi", "Jahldor", "Uyatchan"], 0),
        mcq("'cömert' so'zining ma'nosi nima?", ["Saxiy", "Ochko'z", "Kambag'al", "Boy"], 0),
        mcq("'sabırlı' so'zining ma'nosi nima?", ["Sabrli", "Shoshqaloq", "Jahldor", "Dangasa"], 0),
        mcq("'gülmeyen' so'zi qaysi qo'shimcha bilan yasalgan?", ["-mAyAn (olumsuz sifatdosh)", "-An/-En (ijobiy sifatdosh)", "-mAz (geniş zaman olumsuzi)", "-DI (o'tgan zamon)"], 0),
        mcq("'inatçı' so'zining ma'nosi nima?", ["Qaysar", "Yumshoq", "Saxiy", "Kamtar"], 0),
        mcq("'bencil' so'zining ma'nosi nima?", ["Xudbin", "Saxiy", "Mehribon", "Kamtar"], 0),
    ],
})

sections[7]['topics'].append({
    'key': 'u8b', 'title': "B. Başarının Anahtarı Elimde", 'start_page': 23, 'end_page': 23,
    'explanation': {
        'goals': ["Muvaffaqiyat va maqsad haqidagi lug'atni o'rganish", "Motivatsion nutq uslubini bilish"],
        'blocks': [
            block(
                "Muvaffaqiyat kaliti",
                "\"**Başarının anahtarı elimde**\" (Muvaffaqiyat kaliti mening qo'limda) - "
                "==inson o'z taqdirini o'zi belgilaydi== degan g'oyani ifodalovchi "
                "motivatsion ibora. Bu darsda maqsad qo'yish va unga erishish haqidagi "
                "lug'at bilan tanishasiz.",
            ),
            block(
                "Maqsadga erishish so'zlari",
                "- **hedef** (maqsad) - **çaba** (harakat/mehnat) - **azim** (qat'iyat) - "
                "**fırsat** (imkoniyat)\n"
                "- **Hedefime ulaşmak için çok çalışıyorum.** = Maqsadimga erishish uchun "
                "ko'p mehnat qilyapman.\n"
                "- **Her fırsatı değerlendirmeliyiz.** = Har bir imkoniyatdan foydalanishimiz "
                "kerak.",
            ),
        ],
        'key_facts': [
            fact("hedef = maqsad, çaba = harakat, azim = qat'iyat, fırsat = imkoniyat."),
            fact("'Başarının anahtarı elimde' - taqdirni o'zi belgilash g'oyasi."),
        ],
        'summary': "Muvaffaqiyat lug'ati: **hedef, çaba, azim, fırsat** - motivatsion nutqning asosiy so'zlari.",
        'vocabulary': [
            voc('başarı', 'muvaffaqiyat', 'Başarı için çok çalıştım.', 'Muvaffaqiyat uchun ko\'p mehnat qildim.'),
            voc('hedef', 'maqsad', 'Hedefime ulaştım.', 'Maqsadimga erishdim.'),
            voc('çaba', 'harakat', 'Büyük bir çaba gösterdi.', 'Katta harakat qildi.'),
            voc('azim', "qat'iyat", 'Azimle çalıştım.', "Qat'iyat bilan ishladim."),
            voc('fırsat', 'imkoniyat', 'Bu fırsatı kaçırma.', 'Bu imkoniyatni qo\'ldan boy berma.'),
            voc('anahtar', 'kalit', 'Başarının anahtarı çalışmaktır.', 'Muvaffaqiyat kaliti - mehnat qilishdir.'),
            voc('engel', "to'siq", 'Birçok engeli aştım.', "Ko'p to'siqlarni yengib o'tdim."),
            voc('sabretmek', 'sabr qilmoq', 'Sonuç için sabretmelisin.', "Natija uchun sabr qilishing kerak."),
            voc('motivasyon', 'motivatsiya', 'Motivasyonumu kaybetmemeliyim.', "Motivatsiyamni yo'qotmasligim kerak."),
            voc('ilerlemek', 'ilgarilamoq', 'Yavaş ama emin adımlarla ilerliyorum.', "Sekin, ammo ishonchli qadamlar bilan ilgarilayapman."),
        ],
        'listening': {
            'dialogue': [
                dialogue_line('Koç', 'Hedefin nedir?'),
                dialogue_line('Sporcu', 'Şampiyon olmak istiyorum.'),
                dialogue_line('Koç', 'O zaman her gün azimle çalışmalısın.'),
                dialogue_line('Sporcu', 'Söz veriyorum, hiçbir fırsatı kaçırmayacağım.'),
            ],
            'questions': [
                mcq('Sporcunun hedefi nedir?', ['Şampiyon olmak', 'Dinlenmek', 'Okula gitmek', 'Seyahat etmek'], 0),
                mcq('Koç ne tavsiye ediyor?', ['Azimle çalışmasını', "Dinlenmesini", 'Pes etmesini', 'Beklemesini'], 0),
            ],
        },
        'reading': {
            'title': 'Başarının Sırrı',
            'text': "Başarılı insanlar genellikle net bir hedefe sahiptir. Hedeflerine "
                    "ulaşmak için büyük çaba gösterirler ve zorluklar karşısında pes "
                    "etmezler. Yolda birçok engelle karşılaşabilirler, ama bu engeller "
                    "onları durdurmaz - aksine, her engeli aşarak daha da güçlenirler. Her "
                    "fırsatı değerlendirirler ve azimle çalışmaya devam ederler. Sonuçların "
                    "hemen gelmeyeceğini bilirler, bu yüzden sabretmeyi öğrenirler. "
                    "Motivasyonlarını kaybettikleri anlar olsa bile, kendilerine neden "
                    "başladıklarını hatırlatarak yavaş ama emin adımlarla ilerlemeye devam "
                    "ederler.",
            'questions': [
                mcq('Başarılı insanların ortak özelliği nedir?', ['Net bir hedefe sahip olmaları', 'Hiç çalışmamaları', 'Şanslı olmaları', 'Hiç zorluk yaşamamaları'], 0),
                mcq('Zorluklar karşısında ne yapmazlar?', ['Pes etmezler', 'Çalışmazlar', 'Gülmezler', 'Konuşmazlar'], 0),
                mcq('Engellerle karşılaştıklarında ne olur?', ['Daha da güçlenirler', 'Hemen pes ederler', 'Hiçbir şey olmaz', "Hedeflerini unuturlar"], 0),
                mcq('Motivasyonlarını kaybettiklerinde ne yaparlar?', ['Neden başladıklarını hatırlarlar', 'Tamamen pes ederler', "Hemen yeni bir hedef seçerler", "Uyumaya giderler"], 0),
            ],
        },
        'sentence_practice': [
            choice("'Hedefime ulaşmak için çok ___' (ishlayapman)", ['çalışıyorum', 'çalıştım', 'çalışacağım', 'çalışmam'], 0),
            choice("'fırsat' so'zi nima?", ["Imkoniyat", "Xavf", "Qiyinchilik", "Charchoq"], 0),
            order("Cümleyi doğru sıraya dizin: 'Her fırsatı değerlendirmeliyiz'", ['Her', 'fırsatı', 'değerlendirmeliyiz']),
        ],
        'writing_prompt': {
            'instruction': "O'z maqsadingiz (hedef) haqida 2-3 gap yozing.",
            'sample_answer': "Benim hedefim iyi bir Türkçe öğrenmek. Bu yüzden her gün çalışıyorum.",
        },
        'speaking_prompt': {'sentences': ['Hedefime ulaşmak istiyorum.', 'Her fırsatı değerlendirmeliyiz.', 'Azimle çalışıyorum.']},
    },
    'test': [
        mcq("'hedef' so'zining ma'nosi nima?", ["Maqsad", "Imkoniyat", "Qiyinchilik", "Harakat"], 0),
        mcq("'çaba' so'zining ma'nosi nima?", ["Harakat/mehnat", "Dam olish", "Uxlash", "O'ynash"], 0),
        mcq("'fırsat' so'zining ma'nosi nima?", ["Imkoniyat", "Xavf", "Qiyinchilik", "Muvaffaqiyat"], 0),
        mcq("'azim' so'zining ma'nosi nima?", ["Qat'iyat", "Dangasalik", "Qo'rquv", "Xafalik"], 0),
        mcq("Matnga ko'ra, muvaffaqiyatli odamlar zorliklar oldida nima qilishmaydi?", ["Pes etishmaydi", "Ishlashmaydi", "Kulishmaydi", "Gapirishmaydi"], 0),
        mcq("'engel' so'zining ma'nosi nima?", ["To'siq", "Yordam", "Imkoniyat", "Muvaffaqiyat"], 0),
        mcq("'sabretmek' fe'li nima?", ["Sabr qilmoq", "Shoshilmoq", "Jahllanmoq", "Unutmoq"], 0),
        mcq("'motivasyon' so'zi nima?", ["Motivatsiya", "Qiyinchilik", "Charchoq", "Dam olish"], 0),
    ],
})

sections[7]['topics'].append({
    'key': 'u8c', 'title': "C. Empati Kuruyorum — Genel Tekrar", 'start_page': 24, 'end_page': 24,
    'explanation': {
        'goals': ["Empatiya va tushunish lug'atini o'rganish", "Kursda o'rgangan asosiy grammatikani umumlashtirish"],
        'blocks': [
            block(
                "Empati nima?",
                "**Empati** (boshqa odamning holatiga kirib tushunish) - ==o'zingizni "
                "boshqa birovning o'rniga qo'yib, uning his-tuyg'ularini tushunish== "
                "qobiliyati. \"Empati kuruyorum\" (Men empatiya qilyapman/tushunayapman) - "
                "boshqa odamni tinglaganda va uning holatini tushunishga harakat qilganda "
                "aytiladi.",
            ),
            block(
                "Kursda o'rgangan grammatikani eslaylik",
                "A2 kursida biz ko'plab muhim qurilmalarni o'rgandik - keling, ularni "
                "eslaylik:\n\n"
                "- **-mış** (belgisiz geçmiş): *Meğer çok yorgunmuş.*\n"
                "- **Geniş zaman** (-Ir/-Ar/-r): *Her gün kitap okurum.*\n"
                "- **-(y)Abil-** (qila olish): *Bunu yapabilirim.*\n"
                "- **-An/-En** (sifatdosh): *Gülen çocuk.*\n"
                "- **-A göre** (fikricha): *Bana göre bu doğru.*\n\n"
                "Bu qurilmalarning barchasi ==kundalik muloqotda doimiy ishlatiladi== - "
                "ularni amaliyotda qo'llash orqali mustahkamlang.",
            ),
            block(
                "Yana bir necha muhim qurilma",
                "Kursning qolgan qismida o'rgangan yana bir qancha muhim qurilmalar bor "
                "- ularni ham eslab qolish kerak:\n\n"
                "- **-(y)Ip / -(y)ArAk** (ketma-ket harakat/usul): *Markete gidip ekmek "
                "aldım. Koşarak geldi.*\n"
                "- **-mAk için** (maqsad): *Yemek pişirmek için fırını açtım.*\n"
                "- **...diye sordu/cevap verdi** (so'zma-so'z keltirish): *\"Bu nedir?\" "
                "diye sordu.*\n\n"
                "A1'da o'rgangan asoslar (hozirgi zamon, oddiy o'tgan zamon) bilan "
                "birlashtirilganda, ==bu qurilmalar sizga deyarli har qanday kundalik "
                "vaziyatda erkin so'zlashish== imkonini beradi. Endi B1 darajasiga "
                "o'tishga tayyorsiz!",
            ),
        ],
        'key_facts': [
            fact("Empati - boshqa odamning his-tuyg'ularini tushunish qobiliyati."),
            fact("A2 kursida -mış, geniş zaman, -(y)Abil-, -An/-En, -A göre kabi qurilmalar o'rganildi."),
        ],
        'summary': "**Empati** - boshqalarni tushunish san'ati. A2 kursini yakunlab, siz ==muhim turkcha "
                   "qurilmalarni== amaliyotda qo'llashni o'rgandingiz - tabriklaymiz!",
        'vocabulary': [
            voc('empati', 'empatiya', 'Empati kurmak önemlidir.', 'Empatiya qilish muhim.'),
            voc('anlayış', 'tushunish', 'Ona anlayış gösterdi.', "Onasi tushunish ko'rsatdi."),
            voc('hoşgörü', 'bag\'rikenglik', 'Hoşgörülü olmalıyız.', "Bag'rikeng bo'lishimiz kerak."),
            voc('saygı', 'hurmat', 'Herkese saygı duyarım.', 'Men hammaga hurmat qilaman.'),
            voc('yardımlaşma', "o'zaro yordam", 'Yardımlaşma çok önemli.', "O'zaro yordam juda muhim."),
            voc('dinlemek', 'tinglamoq', "Başkalarını dikkatle dinlemeliyiz.", "Boshqalarni diqqat bilan tinglashimiz kerak."),
            voc('paylaşmak', "baham ko'rmoq/bo'lishmoq", 'Duygularını paylaştı.', "His-tuyg'ularini baham ko'rdi."),
            voc('toplum', 'jamiyat', 'Toplumumuz çok çeşitlidir.', "Jamiyatimiz juda xilma-xil."),
            voc('birey', 'shaxs (individ)', 'Her birey farklıdır.', "Har bir shaxs farqli."),
        ],
        'listening': {
            'dialogue': [
                dialogue_line('Ayşe', 'Arkadaşım çok üzgündü, ben de onu dinledim.'),
                dialogue_line('Can', 'Çok iyi yapmışsın, empati kurmuşsun.'),
                dialogue_line('Ayşe', "Evet, kendimi onun yerine koydum."),
                dialogue_line('Can', 'Bu gerçek bir arkadaşlık.'),
            ],
            'questions': [
                mcq('Ayşe ne yaptı?', ['Üzgün arkadaşını dinledi', 'Arkadaşını unuttu', 'Arkadaşına kızdı', 'Hiçbir şey yapmadı'], 0),
                mcq("'Kendimi onun yerine koydum' ne demek?", ['Empati kurdum', 'Ona kızdım', 'Onu terk ettim', "Onunla tartıştım"], 0),
            ],
        },
        'reading': {
            'title': 'Empatinin Gücü',
            'text': "Empati kurabilen insanlar daha iyi arkadaşlar olur. Başkalarının "
                    "duygularını anlayan, onlara saygı gösteren ve yardım eden insanlar "
                    "toplumu güzelleştirir. Her birey farklı bir hayat yaşar, farklı "
                    "zorluklarla karşılaşır - bu yüzden birini gerçekten anlamak için önce "
                    "onu dikkatle dinlemeliyiz. Toplumumuzda yardımlaşma ve paylaşma "
                    "kültürü ne kadar güçlü olursa, hepimiz o kadar mutlu ve güvende "
                    "hissederiz. Bu A2 kursunda öğrendiğimiz her şey gibi, empati de "
                    "pratik yaparak gelişir - küçük adımlarla başlayıp, her gün biraz "
                    "daha iyi bir dinleyici ve anlayışlı bir insan olabiliriz.",
            'questions': [
                mcq('Empati kurabilen insanlar nasıl olur?', ['Daha iyi arkadaşlar', 'Daha yalnız', 'Daha kızgın', 'Daha sessiz'], 0),
                mcq('Metne göre empati nasıl gelişir?', ['Pratik yaparak', 'Kendiliğinden', "Hiç gelişmez", "Sadece kitap okuyarak"], 0),
                mcq('Birini gerçekten anlamak için önce ne yapmalıyız?', ['Dikkatle dinlemeli', 'Hemen tavsiye vermeli', "Onunla tartışmalı", "Görmezden gelmeli"], 0),
                mcq('Metne göre toplumda ne güçlü olmalı?', ['Yardımlaşma ve paylaşma kültürü', "Rekabet", "Yalnızlık", "Sessizlik"], 0),
            ],
        },
        'sentence_practice': [
            choice("'Empati kurmak' nimani anglatadi?", ["Boshqa odamni tushunish", "Boshqa odamdan qochish", "Boshqa odamga achinish (rahmsizlik)", "Boshqa odamni tanqid qilish"], 0),
            choice("'Kendimi onun yerine koydum' iborasi nimani bildiradi?", ["O'zini boshqa birovning o'rniga qo'yish (empatiya)", "Joyni almashtirish", "Uyni sotib olish", "Sayohat qilish"], 0),
            order("Cümleyi doğru sıraya dizin: 'Herkese saygı duyarım'", ['Herkese', 'saygı', 'duyarım']),
        ],
        'writing_prompt': {
            'instruction': "Kursda o'rgangan kamida 2 ta grammatik qurilmani (masalan -mış, -Abil-, -An/-En) ishlatib, do'stingizga yordam bergan holatingiz haqida yozing.",
            'sample_answer': "Arkadaşım üzgündü, ben de onu dinleyebildim. Kendimi onun yerine koyarak, ona yardım eden biri oldum.",
        },
        'speaking_prompt': {'sentences': ['Empati kurmak önemlidir.', 'Herkese saygı duyarım.', 'Kendimi onun yerine koydum.']},
    },
    'test': [
        mcq("'Empati' so'zining ma'nosi nima?", ["Boshqa odamning his-tuyg'usini tushunish", "Boshqa odamdan qo'rqish", "Boshqa odamga xafa bo'lish", "Boshqa odamni unutish"], 0),
        mcq("'Kendimi onun yerine koydum' iborasi qaysi tushunchaga mos keladi?", ["Empati", "G'azab", "Qo'rquv", "Zerikish"], 0),
        mcq("'saygı' so'zining ma'nosi nima?", ["Hurmat", "Nafrat", "Qo'rquv", "Zerikish"], 0),
        mcq("'hoşgörü' so'zining ma'nosi nima?", ["Bag'rikenglik", "Qattiqqo'llik", "Jahl", "Yolg'on"], 0),
        mcq("Matnga ko'ra, empati qanday rivojlanadi?", ["Amaliyot (pratik) orqali", "O'z-o'zidan", "Hech qachon rivojlanmaydi", "Faqat kitob o'qish orqali"], 0),
        mcq("'-(y)Ip' va '-(y)ArAk' orasidagi asosiy farq nima?", ["Biri ketma-ket harakat, ikkinchisi usul/vosita bildiradi", "Hech qanday farq yo'q", "Ikkalasi ham bir xil ma'noda", "Biri savol, ikkinchisi javob"], 0),
        mcq("'...diye sordu' qurilmasi nima uchun ishlatiladi?", ["So'zma-so'z savolni keltirish uchun", "Buyruq berish uchun", "Kelasi zamonni bildirish uchun", "Inkor qilish uchun"], 0),
        mcq("'toplum' so'zining ma'nosi nima?", ["Jamiyat", "Oila", "Shahar", "Davlat"], 0),
        mcq("'paylaşmak' fe'lining ma'nosi nima?", ["Baham ko'rmoq/bo'lishmoq", "Yashirmoq", "Unutmoq", "Tashlamoq"], 0),
        fill_blank("'Empati ___' (qilyapman, hozirgi zamon 1-shaxs)", 'kuruyorum'),
    ],
})

# ============================================================
# YAKUNIY YIG'ISH VA YOZISH
# ============================================================
book_data = {
    'format_version': FORMAT_VERSION,
    'book': {
        'key': 'turk_a2',
        'title': "Turk tili A2 (Yedi İklim)",
        'description': "Yedi İklim Türkçe A2 darsligi mundarijasi asosida tuzilgan, A1'dan "
                       "keyingi bosqich - murakkabroq grammatika va lug'at bilan.",
        'subject': 'turk-tili',
        'subject_title': "Turk tili",
    },
    'sections': sections,
}

with open('backend/content/turk_a2/book.json', 'w', encoding='utf-8') as f:
    json.dump(book_data, f, ensure_ascii=False, indent=2)
    f.write('\n')

n_topics = sum(len(s['topics']) for s in sections)
n_questions = sum(len(t['test']) for s in sections for t in s['topics'])
print(f"Tayyor: {len(sections)} bo'lim, {n_topics} mavzu, {n_questions} test savoli")
