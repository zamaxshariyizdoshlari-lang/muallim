# -*- coding: utf-8 -*-
from dsl import P, ORD, TR, MT

EXTRAS = {}

EXTRAS['s8a'] = dict(
    matching=MT(("Virus", "Boshqa fayllarga yopishib ko'payadi"), ("Chuvalchang (worm)", "Tarmoq orqali mustaqil tarqaladi"), ("Troyan", "Foydali dastur niqobidagi zararli kod"),
                ("Ransomware", "Fayllarni shifrlab pul talab qiladi"), ("Fishing", "Soxta xat/sayt orqali aldab ma'lumot olish"), ("DDoS", "Ko'p so'rov bilan xizmatni to'xtatish")),
    problems=[
        P("3-2-1 zaxira qoidasida jami nechta nusxa saqlanadi?", "3", "", "3 nusxa"),
        P("4 xonali PIN-kod (har xona 0–9) nechta variantga ega?", "10000", "", "10⁴"),
        P("Faqat kichik lotin harflaridan (26 ta) iborat 6 belgili parol nechta variantga ega?", "308915776", "26⁶", "308 915 776"),
        P("CIA triadasining uchta tamoyilidan biri — maxfiylik (Confidentiality). Qolgan ikkitasidan birini yozing: yaxlitlik yoki mavjudlik.", ["yaxlitlik", "mavjudlik"], "", "Yaxlitlik (Integrity), Mavjudlik (Availability)")],
    code_trace=[
        TR("print(26 ** 6)", "Dastur nimani chiqaradi?", "308915776", "26 harf, 6 pozitsiya."),
        TR("print(10 ** 4)", "Dastur nimani chiqaradi?", "10000", "4 xonali PIN variantlari.")],
    sentence_practice=[ORD("Fishing xatiga duch kelganda harakatlar tartibi", ["Havolani bosmang va biriktirmani ochmang", "Jo'natuvchi manzilini tekshiring", "Rasmiy kanal orqali tashkilotga bog'laning", "Xatni spam deb belgilang va o'chiring"])],
)

EXTRAS['s8b'] = dict(
    matching=MT(("Bilganingiz", "Parol, PIN"), ("Egaligingizdagi", "Telefon, token, karta"), ("O'zingiz", "Barmoq izi, yuz (biometriya)"),
                ("2FA", "Ikki bosqichli autentifikatsiya"), ("Parol menejeri", "Kuchli parollarni xavfsiz saqlaydi"), ("VPN", "Aloqani shifrlovchi xavfsiz tunnel")),
    problems=[
        P("Faqat raqamlardan iborat 6 xonali parol nechta variantga ega?", "1000000", "", "10⁶"),
        P("62 ta belgi (a–z, A–Z, 0–9) dan 4 belgili parol nechta variantga ega?", "14776336", "62⁴", "14 776 336"),
        P("Autentifikatsiyaning nechta omili bor (bilganing, egaliging, o'zing)?", "3", "", "3"),
        P("Kuchli parol uchun tavsiya etilgan minimal uzunlik?", "12", "", "12 belgi")],
    code_trace=[
        TR('p = "Abc123"\nprint(len(p) >= 8)', "Dastur nimani chiqaradi?", "False", "Uzunlik 6 < 8."),
        TR('print(any(c.isdigit() for c in "abc1"))', "Dastur nimani chiqaradi?", "True", "'1' raqam."),
        TR('import hashlib\nprint(len(hashlib.sha256(b"a").hexdigest()))', "Dastur nimani chiqaradi?", "64", "SHA-256 xeshi 64 ta o'n oltilik belgi.")],
    sentence_practice=[ORD("Akkauntni himoyalash tartibi", ["Uzun va noyob parol yarating", "Parol menejerida saqlang", "Ikki bosqichli autentifikatsiyani yoqing", "Kirish qurilmalarini muntazam tekshiring"])],
)

EXTRAS['s8c'] = dict(
    matching=MT(("Simmetrik shifrlash", "Bitta umumiy kalit (AES)"), ("Asimmetrik shifrlash", "Ochiq va yopiq kalit (RSA)"), ("Xesh funksiya", "Bir tomonlama \"barmoq izi\" (SHA-256)"),
                ("ERI", "Elektron imzo: yaxlitlik va muallifni tasdiqlaydi"), ("Sezar shifri", "Harflarni k o'rin siljitish"), ("Steganografiya", "Axborotni boshqa ma'lumot ichiga yashirish")),
    problems=[
        P("Sezar shifri k = 3: 'CAB' so'zi qanday shifrlanadi?", "FDE", "Har harfni 3 o'rin oldinga.", "C→F, A→D, B→E"),
        P("Sezar shifri k = 3 bilan shifrlangan 'FDE' ni ochsangiz (deshifrlash)?", "CAB", "3 o'rin orqaga.", "CAB"),
        P("RSA: p = 3, q = 11 bo'lsa n nechaga teng?", "33", "", "3 · 11"),
        P("RSA: p = 3, q = 11 bo'lsa φ(n) nechaga teng?", "20", "(p−1)(q−1)", "2 · 10 = 20"),
        P("17 mod 5 nechaga teng?", "2", "", "17 = 3·5 + 2")],
    code_trace=[
        TR("print(chr((ord('A') - 65 + 3) % 26 + 65))", "Dastur nimani chiqaradi? (Sezar, k = 3)", "D", "A (0) + 3 = 3 → D"),
        TR("print(pow(8, 7, 33))", "Dastur nimani chiqaradi? (RSA deshifrlash: 8⁷ mod 33)", "2", "8⁷ = 2 097 152; 33 ga bo'lgandagi qoldiq 2."),
        TR('import hashlib\nprint(hashlib.sha256(b"abc").hexdigest()[:8])', "Dastur nimani chiqaradi? (SHA-256 ning dastlabki 8 belgisi)", "ba7816bf", "")],
    sentence_practice=[ORD("RSA bilan xabar yuborish tartibi", ["Qabul qiluvchi kalit juftligini yaratadi", "Ochiq kalit yuboruvchiga beriladi", "Yuboruvchi xabarni ochiq kalit bilan shifrlaydi", "Qabul qiluvchi yopiq kalit bilan deshifrlaydi"])],
)
