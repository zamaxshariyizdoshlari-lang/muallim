# -*- coding: utf-8 -*-
from dsl import P, ORD, TR, MT

EXTRAS = {}

EXTRAS['s5a'] = dict(
    matching=MT(("Ctrl+B", "Qalin shrift"), ("Ctrl+I", "Kursiv shrift"), ("Ctrl+U", "Tagiga chizish"), ("Ctrl+H", "Matnni almashtirish"),
                ("Kolontitul", "Har sahifada takrorlanuvchi yuqori/pastki qism"), ("Stil (Heading)", "Mundarija tuzishga yordam beruvchi sarlavha formati")),
    problems=[
        P("A4 qog'oz o'lchami necha mm? (eni×bo'yi: masalan 210x297)", ["210x297", "210×297", "210 x 297"], "", "210×297 mm"),
        P("Matnni qidirish tugmalari birikmasi?", "Ctrl+F", "", "Ctrl+F"),
        P("Hujjatni PDF kabi o'zgarmas ko'rinishda saqlash uchun qaysi format? (kengaytma harflari)", "pdf", "", "PDF"),
        P("Rasmiy hujjatlarda qator oralig'i odatda necha?", "1,5", "", "1,5")],
    sentence_practice=[ORD("Hujjatni rasmiylashtirish tartibi", ["Matnni kiriting", "Sarlavhalarga stil (Heading) bering", "Sahifa parametrlarini (A4, maydonlar) sozlang", "Imlo tekshiruvi (F7)", "Chop etishdan oldin Print Preview"])],
)

EXTRAS['s5b'] = dict(
    matching=MT(("=SUM(A1:A5)", "Yig'indi"), ("=AVERAGE(...)", "O'rta arifmetik"), ("=IF(shart; a; b)", "Shartga qarab qiymat tanlash"),
                ("$A$1", "Mutlaq adres"), ("#DIV/0!", "Nolga bo'lish xatosi"), ("Fill Handle", "Formulani cho'zib nusxalash")),
    problems=[
        P("A1 = 5 va B1 = 7 bo'lsa, =A1+B1 natijasi?", "12", "", "12"),
        P("A1:A4 kataklarda 1, 2, 3, 4 bor. =SUM(A1:A4) natijasi?", "10", "", "10"),
        P("=AVERAGE(2;4;6) natijasi?", "4", "", "4"),
        P("=MAX(3;9;2) natijasi?", "9", "", "9"),
        P("=COUNT(1;\"a\";3) natijasi (faqat sonlarni sanaydi)?", "2", "", "2")],
    code_trace=[
        TR('A1: 5     B1: 7     C1: =A1*B1+3', "C1 katakda qanday son ko'rinadi?", "38", "5 · 7 + 3 = 38"),
        TR('B2: 60\nC2: =IF(B2>=55;"O\'tdi";"Yiqildi")', "C2 katakda nima ko'rinadi?", "O'tdi", "60 ≥ 55 — shart chin."),
        TR('A1: 10    B1: 2\nC1: =A1/(B1-2)', "C1 katakda qanday xato ko'rinadi?", "#DIV/0!", "B1 − 2 = 0 — nolga bo'lish.")],
    sentence_practice=[ORD("Elektron jadvalda o'rtacha ballni hisoblash tartibi", ["Ballarni A1:A5 ga kiriting", "C1 katakka = belgisini yozing", "AVERAGE(A1:A5) funksiyasini yozing", "Enter bosing"])],
)

EXTRAS['s5c'] = dict(
    matching=MT(("Slayd", "Taqdimotning alohida sahifasi"), ("Maket (layout)", "Slaydda elementlar joylashuvi"), ("Mavzu (theme)", "Butun taqdimotga yagona ko'rinish"),
                ("Animatsiya", "Ob'ektlarga harakat berish"), ("Transition", "Slaydlar almashinuvi effekti"), ("Speaker Notes", "Auditoriyaga ko'rinmaydigan nutq izohlari")),
    problems=[
        P("20 daqiqalik taqdimotga har slaydga 2 daqiqadan ajratilsa, eng ko'pi bilan nechta slayd?", "10", "", "20 : 2 = 10"),
        P("Namoyishni boshlash tugmasi? (F bilan raqam)", "F5", "", "F5"),
        P("Asosiy matn kegli kamida necha pt bo'lishi tavsiya etiladi?", "24", "", "24 pt"),
        P("Bir slaydda taxminan nechta qator tavsiya etiladi (yuqori chegara)?", "6", "", "5–6 qator")],
    sentence_practice=[ORD("Taqdimot tayyorlash bosqichlari", ["Maqsad va auditoriyani aniqlash", "Reja tuzish", "Slaydlarni dizayn qilish", "Mashq qilish", "Taqdim etish"])],
)

EXTRAS['s5d'] = dict(
    matching=MT(("Rastr grafika", "Piksellardan iborat tasvir"), ("Vektor grafika", "Formulalar bilan berilgan, sifat yo'qolmaydi"), ("RGB", "Ekran uchun rang modeli"),
                ("CMYK", "Bosma uchun rang modeli"), ("Qatlam (layer)", "Tasvir qismlarini mustaqil tahrirlash"), ("dpi", "Dyuymdagi nuqtalar soni")),
    problems=[
        P("800×600 piksellik 24 bitli rasm (siqilmagan) necha bayt?", "1440000", "800·600·3", "1 440 000", unit="bayt"),
        P("#FF0000 qaysi rang? (bir so'z)", "qizil", "", "Qizil"),
        P("RGB(0, 255, 0) qaysi rang? (bir so'z)", "yashil", "", "Yashil"),
        P("100×100 piksellik oq-qora (1 bit) tasvir necha bit?", "10000", "", "10 000", unit="bit")],
    code_trace=[
        TR('<p style="color: #0000FF">Salom</p>', "Matn qaysi rangda ko'rinadi? (bir so'z)", "ko'k", "#0000FF — ko'k kanal 255.")],
    sentence_practice=[ORD("Rastr rasmni tahrirlash tartibi", ["Rasmni oching", "Kerakli qismni qirqing (Crop)", "Yorqinlik va kontrastni sozlang", "Kerakli formatda (JPEG/PNG) saqlang"])],
)

EXTRAS['s5e'] = dict(
    matching=MT(("MP3", "Yo'qotishli audio format"), ("FLAC", "Yo'qotishsiz siqilgan audio"), ("MP4", "Eng ommabop video format"),
                ("Kodek", "Siquvchi va ochuvchi algoritm"), ("Full HD", "1920×1080 ruxsat"), ("AR", "Real dunyoga raqamli ob'ekt qo'shish")),
    problems=[
        P("44100 Hz, 16 bit, stereo (2 kanal) audio 1 soniyada necha bayt?", "176400", "44100·2·2", "176 400", unit="bayt"),
        P("30 kadr/s videoning 10 soniyasida nechta kadr bor?", "300", "", "300"),
        P("1920×1080 ruxsatda piksellar soni?", "2073600", "", "2 073 600"),
        P("Bitreyt 128 kbit/s bo'lgan audioning 1 daqiqasi necha KB? (1 bayt = 8 bit, 1 KB = 1000 bayt)", "960", "128·60/8", "960", unit="KB")],
    sentence_practice=[ORD("Video montaj tartibi", ["Material (kliplar) import qilish", "Kesish va joylashtirish", "O'tish effektlari, titr va musiqa qo'shish", "Rang korreksiyasi", "Eksport (render)"])],
)
