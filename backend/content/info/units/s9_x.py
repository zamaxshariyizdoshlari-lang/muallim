# -*- coding: utf-8 -*-
from dsl import P, ORD, TR, MT

EXTRAS = {}

EXTRAS['s9a'] = dict(
    matching=MT(("Nazoratli o'rganish", "Yorliqli ma'lumot bilan o'qitish"), ("Nazoratsiz o'rganish", "Yorliqsiz ma'lumotdan tuzilma topish"), ("Mustahkamlovchi o'rganish", "Mukofot va jazo orqali o'rganish"),
                ("Overfitting", "Modelning o'quv ma'lumotini yodlab olishi"), ("LLM", "Katta til modeli"), ("Gallyutsinatsiya", "Modelning ishonchli ko'ringan noto'g'ri javobi")),
    problems=[
        P("Model 100 ta namunadan 80 tasini to'g'ri aniqlasa, aniqlik necha foiz?", "80", "", "80%", unit="%"),
        P("100 ta spam xatdan model 90 tasini topdi. Qamrov (recall) necha foiz?", "90", "", "90%", unit="%"),
        P("Tyuring testi qaysi yilda taklif qilingan?", "1950", "", "1950-yil"),
        P("'Sun'iy intellekt' atamasi qaysi yilda taklif qilingan?", "1956", "", "1956-yil (Dartmut)")],
    code_trace=[
        TR("w = 2\nx = 5\nprint(w * x)", "Dastur nimani chiqaradi? (y = w·x modeli bashorati)", "10", ""),
        TR("w = 1.0\ngrad = 0.5\nlr = 0.1\nw = w - lr * grad\nprint(w)", "Dastur nimani chiqaradi? (gradiyentli tushishning bir qadami)", "0.95", "1.0 − 0.1·0.5 = 0.95")],
    sentence_practice=[ORD("Mashinaviy o'rganish jarayoni", ["Ma'lumot yig'ish", "Tozalash", "Model tanlash", "O'qitish", "Test to'plamida baholash", "Joriy etish"])],
)

EXTRAS['s9b'] = dict(
    matching=MT(("IoT", "Internet orqali ma'lumot almashadigan qurilmalar tarmog'i"), ("Sensor", "Muhit ma'lumotini o'lchaydi"), ("Aktuator", "Harakat/amalni bajaradi (motor, rele)"),
                ("Arduino", "Mikrokontrollerli ochiq platforma"), ("Raspberry Pi", "Linux li kichik kompyuter"), ("Sanoat 4.0", "IoT, SI va robotlar ishlab chiqarishda")),
    problems=[
        P("Sensor har 5 soniyada bir marta o'lchasa, 1 soatda nechta o'lchov bo'ladi?", "720", "3600 : 5", "720"),
        P("Arduino dasturida bir marta bajariladigan funksiya nomi?", "setup", "", "setup()"),
        P("Arduino dasturida doimiy takrorlanadigan funksiya nomi?", "loop", "", "loop()"),
        P("Robot so'zini 1920-yilda kim ishlatgan? (familiyasi)", "Chapek", "", "Karel Chapek")],
    code_trace=[
        TR("void setup() { pinMode(13, OUTPUT); }\nvoid loop() {\n  digitalWrite(13, HIGH); delay(1000);\n  digitalWrite(13, LOW);  delay(1000);\n}", "LED 1 daqiqada necha marta yonadi?", "30", "Bir sikl 2 soniya; 60 : 2 = 30."),
        TR("void loop() {\n  digitalWrite(13, HIGH); delay(500);\n  digitalWrite(13, LOW);  delay(500);\n}", "LED 10 soniyada necha marta yonadi?", "10", "Bir sikl 1 soniya.")],
    sentence_practice=[ORD("IoT tizimi ma'lumot yo'li", ["Sensor muhitni o'lchaydi", "Mikrokontroller ma'lumotni qayta ishlaydi", "Aloqa orqali bulutga yuboriladi", "Ilovada natija ko'rsatiladi", "Aktuator buyruq bajaradi"])],
)

EXTRAS['s9c'] = dict(
    matching=MT(("IaaS", "Virtual serverlar ijarasi"), ("PaaS", "Ishlab chiqish platformasi"), ("SaaS", "Tayyor dastur (Gmail, Docs)"),
                ("Blokcheyn", "Xeshlar bilan bog'langan blok zanjiri"), ("Kubit", "Superpozitsiyadagi kvant bit"), ("Git", "Kod versiyalarini boshqarish")),
    problems=[
        P("3 kubit bir vaqtda nechta holatni tasvirlay oladi (2ⁿ)?", "8", "", "2³ = 8"),
        P("Blokcheynda 5 ta blok bor. 3-blok ma'lumoti o'zgartirilsa, undan keyingi nechta blokning xeshi buziladi?", "2", "4- va 5-bloklar", "2"),
        P("Bitcoin g'oyasini 2008-yilda taklif qilgan taxallus?", "Nakamoto", "", "Satoshi Nakamoto"),
        P("Versiyalarni boshqarish tizimi nomi (3 harf)?", "Git", "", "Git")],
    code_trace=[
        TR('import hashlib\nprint(hashlib.sha256(b"abc").hexdigest()[:8])', "Dastur nimani chiqaradi?", "ba7816bf", "Bir xil kirish — doim bir xil xesh."),
        TR('import hashlib\na = hashlib.sha256(b"abc").hexdigest()\nb = hashlib.sha256(b"abd").hexdigest()\nprint(a == b)', "Dastur nimani chiqaradi?", "False", "Bir belgi farqi — butunlay boshqa xesh.")],
    sentence_practice=[ORD("Git bilan o'zgarishni saqlash tartibi", ["git add .", "git commit -m \"izoh\"", "git push"], mono=True)],
)

EXTRAS['s9d'] = dict(
    matching=MT(("Mualliflik huquqi", "Ijodiy asarlarni himoya qiladi"), ("Patent", "Ixtiroyni himoya qiladi"), ("Creative Commons", "Ijodni ochiq litsenziya bilan ulashish"),
                ("Etik haker", "Ruxsat bilan zaiflikni sinaydi"), ("Plagiat", "Boshqaning ishini o'zinikidek ko'rsatish"), ("Raqamli tafovut", "Texnologiyaga kirishdagi tengsizlik")),
    problems=[
        P("Dirixle prinsipi: 13 kishi orasida kamida nechtasi bir oyda tug'ilgan (12 oy)?", "2", "", "Kamida 2 kishi"),
        P("'Kiberxavfsizlik to'g'risida'gi O'zbekiston qonuni qaysi yili qabul qilingan?", "2022", "", "2022-yil"),
        P("Kitob bosishni (Gutenberg) ixtiro qilgan asr (rim emas, raqam)?", "15", "", "XV asr"),
        P("CC BY litsenziyasi nimani talab qiladi? (bir so'z: muallif ... ko'rsatish) — 'muallifni' deb yozing", "muallifni", "", "Muallifni ko'rsatish")],
    sentence_practice=[ORD("Manbadan to'g'ri foydalanish tartibi", ["Ma'lumotni topish", "Muallif va manbani aniqlash", "Litsenziya shartlarini tekshirish", "Iqtibos keltirib, manbani ko'rsatish"])],
)
