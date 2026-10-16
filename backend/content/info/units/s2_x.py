# -*- coding: utf-8 -*-
from dsl import P, ORD, TR, MT

EXTRAS = {}

EXTRAS['s2a'] = dict(
    matching=MT(("Tizimli dastur", "Kompyuter resurslarini boshqaradi (OT, drayver)"), ("Amaliy dastur", "Foydalanuvchi vazifalarini bajaradi (Word, brauzer)"),
                ("Instrumental dastur", "Boshqa dastur yaratishga xizmat qiladi (IDE)"), ("Drayver", "OT va qurilma o'rtasidagi vositachi"),
                ("Shareware", "Sinov muddatli dastur"), ("Open source", "Kodi hammaga ochiq dastur")),
    problems=[
        P("Kodi ochiq, o'rganish va o'zgartirish mumkin bo'lgan dasturlar qanday ataladi? (ikki so'z, inglizcha)", ["open source", "opensource"], "", "Open source"),
        P("Sinov muddatida bepul, so'ng pullik dastur turi? (inglizcha bir so'z)", "shareware", "", "Shareware"),
        P("Qurilma va OT o'rtasida aloqa o'rnatuvchi dastur nomi?", ["drayver", "driver"], "", "Drayver"),
        P("Antivirus qaysi turdagi dasturga kiradi: tizimli, amaliy yoki instrumental?", "tizimli", "Utilita", "Tizimli (utilita)")],
    sentence_practice=[ORD("Dasturni xavfsiz o'rnatish tartibi", ["Rasmiy manbadan yuklab olish", "O'rnatuvchi faylni antivirus bilan tekshirish", "Ruxsatlarni diqqat bilan o'qish", "O'rnatish va yangilanishlarni yoqish"])],
)

EXTRAS['s2b'] = dict(
    matching=MT(("Windows", "Microsoft kompaniyasining grafik OT si"), ("macOS", "Apple kompyuterlari uchun OT"),
                ("Linux", "Ochiq manbali OT, yadroni Torvalds yaratgan"), ("Android", "Google mobil OT si (Linux yadrosi asosida)"),
                ("Jarayon", "Bajarilayotgan dastur nusxasi"), ("CLI", "Buyruqlar qatori interfeysi")),
    problems=[
        P("Linux yadrosini kim yaratgan? (familiyasini yozing)", ["torvalds", "linus torvalds"], "", "Linus Torvalds"),
        P("Linux yadrosi qaysi yilda yaratilgan?", "1991", "", "1991-yil"),
        P("Windows qaysi kompaniya mahsuloti?", ["microsoft"], "", "Microsoft"),
        P("Buyruqlar qatori interfeysi qisqartmasi (3 harf)?", "CLI", "", "Command Line Interface")],
    code_trace=[
        TR('import os\nprint(os.name)', "Windows kompyuterida bu kod nimani chiqaradi?", "nt", "Windows da os.name = 'nt', Linux/macOS da 'posix'.")],
    sentence_practice=[ORD("OT yuklanish bosqichlari", ["Elektr ta'minoti ulanadi", "BIOS/UEFI tekshiruv o'tkazadi", "Yuklovchi (bootloader) OT yadrosini yuklaydi", "Foydalanuvchi interfeysi ochiladi"])],
)

EXTRAS['s2c'] = dict(
    matching=MT((".docx", "Word hujjati"), (".xlsx", "Excel jadvali"), (".py", "Python dastur kodi"), (".mp3", "Siqilgan tovush"),
                ("NTFS", "Windows ning zamonaviy fayl tizimi"), ("FAT32", "Bitta fayl 4 GB dan kichik bo'lishi shart")),
    problems=[
        P("C:\\Users\\Ali\\Hujjatlar\\hisobot.docx faylining kengaytmasi?", ["docx", ".docx"], "", ".docx"),
        P("FAT32 da bitta fayl necha GB dan kam bo'lishi kerak?", "4", "", "4 GB"),
        P("Faylni nusxalash uchun qisqa yo'l tugmalari?", "Ctrl+C", "", "Ctrl+C"),
        P("Faylni qayta nomlash tugmasi?", "F2", "", "F2")],
    code_trace=[
        TR('print("hisobot.docx".split(".")[-1])', "Dastur nimani chiqaradi?", "docx", "split('.') nuqta bo'yicha ajratadi; oxirgi element — kengaytma."),
        TR('print("a/b/c.txt".split("/")[-1])', "Dastur nimani chiqaradi?", "c.txt", "Yo'lning oxirgi bo'lagi — fayl nomi.")],
    sentence_practice=[ORD("Faylni xavfsiz ko'chirish tartibi", ["Faylni belgilash", "Ctrl+X (qirqish)", "Maqsad papkani ochish", "Ctrl+V (qo'yish)"])],
)

EXTRAS['s2d'] = dict(
    matching=MT(("Ctrl+Z", "Oxirgi amalni bekor qilish"), ("Ctrl+A", "Hammasini belgilash"), ("Alt+Tab", "Oynalar o'rtasida almashish"),
                ("Win+L", "Ekranni qulflash"), ("Ctrl+Shift+Esc", "Vazifa dispetcherini ochish"), ("20-20-20 qoidasi", "Har 20 daqiqada 20 soniya uzoqqa qarash")),
    problems=[
        P("Matnni qidirish tugmalari birikmasi?", "Ctrl+F", "", "Ctrl+F"),
        P("Oynani yopish tugmalari birikmasi?", "Alt+F4", "", "Alt+F4"),
        P("Monitor ko'zdan necha sm uzoqlikda tursa yaxshi (pastki chegara, sm)?", "50", "50–70 sm", "50–70 sm", unit="sm"),
        P("Hujjatni saqlash tugmalari birikmasi?", "Ctrl+S", "", "Ctrl+S")],
    sentence_practice=[ORD("Ergonomik ish joyini sozlash tartibi", ["Monitorni ko'z darajasiga o'rnating", "Masofa 50–70 sm bo'lsin", "Tizza va tirsaklar ~90° burchakda", "Har 45–60 daqiqada tanaffus qiling"])],
)
