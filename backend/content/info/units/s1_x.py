# -*- coding: utf-8 -*-
from dsl import P, ORD, TR, MT

EXTRAS = {}

EXTRAS['s1a'] = dict(
    matching=MT(("Ma'lumot", "Talqin qilinmagan xom fakt"), ("Axborot", "Ma'no kasb etgan, noaniqlikni kamaytiruvchi ma'lumot"),
                ("Bilim", "Axborotni tushunib qo'llash natijasi"), ("Shovqin", "Uzatishda axborotni buzuvchi xalaqit"),
                ("Aloqa kanali", "Manba va qabul qiluvchini bog'lovchi vosita"), ("Bit", "Axborotning eng kichik birligi")),
    problems=[
        P("1 bayt necha bitga teng?", "8", "", "1 bayt = 8 bit"),
        P("Fayl hajmi 2 KB. Bu necha bayt? (1 KB = 1024 bayt)", "2048", "", "2 · 1024 = 2048", unit="bayt"),
        P("3 MB necha KB ga teng? (1 MB = 1024 KB)", "3072", "", "3 · 1024", unit="KB"),
        P("Axborot jarayonlari nechta (yig'ish, saqlash, ...)?", "4", "Yig'ish, saqlash, qayta ishlash, ...", "Yig'ish, saqlash, qayta ishlash, uzatish — 4 ta"),
        P("4 bayt axborot necha bit?", "32", "", "4 · 8 = 32", unit="bit")],
    sentence_practice=[ORD("Axborot uzatish zanjirini to'g'ri tartibga soling", ["Axborot manbasi", "Kodlash", "Aloqa kanali (shovqin ta'siri)", "Dekodlash", "Qabul qiluvchi"])],
)

EXTRAS['s1b'] = dict(
    matching=MT(("Ikkilik sistema", "Asosi 2, raqamlari 0 va 1"), ("Sakkizlik sistema", "Asosi 8, bitta raqam = 3 bit"),
                ("O'n oltilik sistema", "Asosi 16, A–F harflari, bitta raqam = 4 bit"), ("Rim raqamlari", "Nopozitsion sanoq sistemasi"),
                ("Razryad", "Raqamning sondagi o'rni"), ("1 + 1 (ikkilik)", "10")),
    problems=[
        P("1101 (ikkilik) sonini o'nlik sistemada yozing.", "13", "8 + 4 + 0 + 1", "13"),
        P("25 (o'nlik) sonini ikkilik sistemada yozing.", "11001", "2 ga ketma-ket bo'ling.", "25 = 16 + 8 + 1 → 11001", fmt="faqat 0 va 1"),
        P("1F (o'n oltilik) sonini o'nlik sistemada yozing.", "31", "1·16 + 15", "31"),
        P("255 ni o'n oltilik sistemada yozing (harflar bilan).", "FF", "255 = 15·16 + 15", "FF"),
        P("101 (ikkilik) + 11 (ikkilik) = ? (ikkilikda)", "1000", "5 + 3 = 8", "1000"),
        P("10110 (ikkilik) sonini o'nlikda yozing.", "22", "16 + 4 + 2", "22")],
    code_trace=[
        TR('print(int("1010", 2))', "Dastur nimani chiqaradi?", "10", "int(satr, 2) — ikkilik satrni o'nlik songa aylantiradi."),
        TR("print(bin(13))", "Dastur nimani chiqaradi?", "0b1101", "bin() ikkilik ko'rinishni \"0b\" prefiksi bilan qaytaradi."),
        TR("print(hex(255))", "Dastur nimani chiqaradi?", "0xff", "hex() o'n oltilik ko'rinishni \"0x\" prefiksi bilan qaytaradi.")],
    sentence_practice=[ORD("13 ni ikkilik sistemaga o'tkazish tartibi", ["13 : 2 = 6 (qoldiq 1)", "6 : 2 = 3 (qoldiq 0)", "3 : 2 = 1 (qoldiq 1)", "1 : 2 = 0 (qoldiq 1)", "Qoldiqlar teskari yoziladi: 1101"])],
)

EXTRAS['s1c'] = dict(
    matching=MT(("ASCII", "7 (8) bitli belgilar kodlash jadvali"), ("Unicode (UTF-8)", "Dunyo tillari belgilarini kodlash, 1–4 bayt"),
                ("RGB", "Ekran uchun qizil-yashil-ko'k rang modeli"), ("CMYK", "Bosma (poligrafiya) rang modeli"),
                ("JPEG", "Yo'qotishli rasm siqish formati"), ("PNG", "Yo'qotishsiz siqish, shaffoflik")),
    problems=[
        P("5 MB necha KB? (1 MB = 1024 KB)", "5120", "", "5 · 1024", unit="KB"),
        P("1000 ta lotin harfidan iborat matn UTF-8 da necha bayt joy egallaydi?", "1000", "Lotin harfi — 1 bayt", "1000", unit="bayt"),
        P("1920×1080 piksellik 24 bitli rasm (siqilmagan) necha KB? (1 KB = 1024 bayt)", "6075", "Piksel soni × 3 bayt ÷ 1024", "1920·1080·3 = 6 220 800 bayt = 6075 KB", unit="KB"),
        P("44100 Hz, 16 bit, 1 kanalli audio 10 soniyada necha bayt?", "882000", "44100 · 2 bayt · 10", "882 000", unit="bayt"),
        P("256 xil rangni kodlash uchun piksel boshiga necha bit kerak?", "8", "2ⁿ = 256", "2⁸ = 256"),
        P("'A' harfining ASCII kodi 65 bo'lsa, 'C' harfining kodi?", "67", "Harflar ketma-ket", "65 + 2 = 67")],
    code_trace=[
        TR("print(ord('A'))", "Dastur nimani chiqaradi?", "65", "ord() belgining kodini qaytaradi."),
        TR("print(chr(97 + 2))", "Dastur nimani chiqaradi?", "c", "chr(99) — kichik 'c' harfi."),
        TR('print(len("salom".encode("utf-8")))', "Dastur nimani chiqaradi?", "5", "Lotin harflari UTF-8 da 1 baytdan.")],
    sentence_practice=[ORD("Rasm hajmini hisoblash tartibi", ["Piksellar sonini toping: eni × bo'yi", "Piksel boshiga bitlarni aniqlang (24 bit = 3 bayt)", "Piksellar soni × bayt", "Natijani KB/MB ga o'tkazing"])],
)

EXTRAS['s1d'] = dict(
    matching=MT(("Blez Paskal", "1642-yilda mexanik qo'shuvchi mashina"), ("Charlz Bebbij", "Dasturlanadigan \"Analitik mashina\" loyihasi"),
                ("Ada Lavleys", "Birinchi dasturchi hisoblanadi"), ("Fon Neyman", "Saqlanuvchi dastur tamoyili (1945)"),
                ("ENIAC", "1946-yildagi elektron lampali kompyuter"), ("Intel 4004", "1971-yildagi birinchi mikroprotsessor")),
    problems=[
        P("Intel 4004 (1971) va IBM PC (1981) o'rtasida necha yil bor?", "10", "", "1981 − 1971 = 10", unit="yil"),
        P("Fon Neyman tamoyillari nechta (ikkilik kodlash, saqlanuvchi dastur, manzillilik, ketma-ket bajarish)?", "4", "", "4 ta"),
        P("Paskalning mexanik mashinasi yaratilgan yilda 2026-yildan necha yil o'tgan? (1642)", "384", "2026 − 1642", "384", unit="yil"),
        P("1-avlod (lampa), 2-avlod (tranzistor), 3-avlod (mikrosxema). 4-avlod elementi qaysi? (bir so'z: mikroprotsessor)", "mikroprotsessor", "BIS va ... ", "Mikroprotsessor va katta integral sxemalar"),
        P("Qaysi avlodda shaxsiy kompyuterlar paydo bo'ldi? (raqam)", "4", "", "To'rtinchi avlod")],
    sentence_practice=[ORD("Kompyuter avlodlarini element bazasi bo'yicha tartiblang", ["Elektron lampalar", "Tranzistorlar", "Integral sxemalar", "Mikroprotsessorlar"])],
)

EXTRAS['s1e'] = dict(
    matching=MT(("CPU", "Buyruqlarni bajaruvchi protsessor"), ("RAM", "Tez, vaqtinchalik operativ xotira"),
                ("SSD", "Harakatlanuvchi qismsiz tez doimiy xotira"), ("Anakart", "Barcha qurilmalarni bog'lovchi asosiy plata"),
                ("GPU", "Tasvir hosil qiluvchi grafik protsessor"), ("BIOS/UEFI", "Kompyuter yoqilganda ishga tushadigan dastur")),
    problems=[
        P("8 GB RAM necha MB? (1 GB = 1024 MB)", "8192", "", "8 · 1024", unit="MB"),
        P("512 GB necha MB? (1 GB = 1024 MB)", "524288", "", "512 · 1024", unit="MB"),
        P("1920×1080 monitorda piksellar soni?", "2073600", "", "1920 · 1080", unit="piksel"),
        P("USB 3.0 (5 Gbit/s) da 1 GB (8 Gbit) fayl necha soniyada ko'chadi (nazariy)?", "1,6", "8 : 5", "1,6", unit="soniya"),
        P("3 GHz protsessor 1 soniyada necha milliard takt beradi?", "3", "", "3 · 10⁹", unit="mlrd")],
    sentence_practice=[ORD("Kompyuter yoqilganda ketma-ketlik", ["Quvvat ulanadi", "BIOS/UEFI ishga tushadi", "Operatsion tizim yuklanadi", "Foydalanuvchi dasturlari ishlaydi"])],
)
