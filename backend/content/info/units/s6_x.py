# -*- coding: utf-8 -*-
from dsl import P, ORD, TR, MT

EXTRAS = {}

EXTRAS['s6a'] = dict(
    matching=MT(("LAN", "Lokal tarmoq"), ("WAN", "Global tarmoq"), ("Switch", "LAN ichida ma'lumotni kerakli portga yo'naltiradi"),
                ("Router", "Turli tarmoqlarni bog'laydi"), ("Optik tola", "Yorug'lik bilan eng tez uzatadi"), ("Mijoz-server", "Server xizmat beradi, mijoz so'rov yuboradi")),
    problems=[
        P("100 Mbit/s tarmoqda 50 MB (400 Mbit) fayl necha soniyada ko'chadi?", "4", "", "400 : 100 = 4", unit="soniya"),
        P("1 Gbit/s necha Mbit/s? (1 Gbit = 1000 Mbit)", "1000", "", "1000"),
        P("Yulduz topologiyada markaziy qurilma nomi? (inglizcha bir so'z)", "switch", "", "Switch (kommutator)"),
        P("Wi-Fi qaysi IEEE standartiga asoslangan? (raqam: 802.11)", "802.11", "", "IEEE 802.11")],
    sentence_practice=[ORD("Uy tarmog'i qurish tartibi", ["Provayder kabelini modemga ulang", "Modemni routerga ulang", "Router orqali Wi-Fi nomi va parolini sozlang", "Qurilmalarni Wi-Fi ga ulang"])],
)

EXTRAS['s6b'] = dict(
    matching=MT(("IPv4", "32 bit, 4 ta bayt: 192.168.1.1"), ("IPv6", "128 bit manzil"), ("DNS", "Domen nomini IP ga aylantiradi"),
                ("HTTPS", "Shifrlangan veb protokol, port 443"), ("TCP", "Ishonchli uzatish protokoli"), ("404", "Sahifa topilmadi kodi")),
    problems=[
        P("IPv4 da nechta mumkin bo'lgan manzil bor (2³²)?", "4294967296", "", "4 294 967 296"),
        P("IPv4 manzilidagi har bir sonning eng katta qiymati?", "255", "", "255"),
        P("HTTP ning standart porti?", "80", "", "80"),
        P("HTTPS ning standart porti?", "443", "", "443"),
        P("127.0.0.1 manzil nima deb ataladi? (inglizcha bir so'z)", "localhost", "", "localhost")],
    code_trace=[
        TR("ip = \"192.168.1.10\"\nprint(ip.split(\".\")[0])", "Dastur nimani chiqaradi?", "192", "split('.') manzilni 4 ta bo'lakka ajratadi."),
        TR("print(len(\"192.168.1.10\".split(\".\")))", "Dastur nimani chiqaradi?", "4", "")],
    sentence_practice=[ORD("Brauzerga manzil kiritilgandan keyingi bosqichlar", ["DNS domenni IP manzilga aylantiradi", "Brauzer serverga TCP ulanishini o'rnatadi", "HTTP(S) so'rov yuboradi", "Server HTML javob qaytaradi", "Brauzer sahifani ko'rsatadi"])],
)

EXTRAS['s6c'] = dict(
    matching=MT(("<a href>", "Havola"), ("<img src>", "Rasm"), ("<h1>", "Eng katta sarlavha"), ("<ul> va <li>", "Markerli ro'yxat"),
                ("CSS", "Sahifa ko'rinishini belgilaydi"), ("JavaScript", "Sahifani interaktiv qiladi")),
    problems=[
        P("Xatboshi (paragraf) uchun HTML teg nomi? (<> belgilarsiz)", "p", "", "<p>"),
        P("CSS da klass selektori qaysi belgi bilan boshlanadi?", ".", "", "Nuqta (.)"),
        P("CSS da identifikator selektori qaysi belgi bilan boshlanadi?", "#", "", "Panjara (#)"),
        P("Quti modelida ichki masofa qaysi xususiyat? (inglizcha)", "padding", "", "padding")],
    code_trace=[
        TR("<h1>Salom</h1>\n<p>Dunyo</p>", "Brauzerda nechta qator matn ko'rinadi?", "2", "Har bir blok teg yangi qatordan boshlanadi."),
        TR('<a href="https://uz.wikipedia.org">Vikipediya</a>', "Havola matnida nima ko'rinadi?", "Vikipediya", "Teg ichidagi matn ko'rinadi, href — manzil."),
        TR("p { color: red; }", "p tegli matnlar qaysi rangda bo'ladi? (bir so'z)", "qizil", ""),
        TR("let a = 3;\na *= 2;\nconsole.log(a);", "Konsolga nima chiqadi?", "6", "a = a * 2")],
    sentence_practice=[ORD("Oddiy HTML sahifa tuzilmasini tartiblang", ["<!DOCTYPE html>", "<html>", "<head><title>Sahifa</title></head>", "<body>", "<h1>Salom</h1>", "</body>", "</html>"], mono=True)],
)

EXTRAS['s6d'] = dict(
    matching=MT(("Brauzer", "Veb-sahifalarni ko'rsatuvchi dastur"), ("Gmail", "Elektron pochta xizmati"), ("Google Drive", "Bulutli xotira"),
                ("Fishing", "Soxta xat/sayt orqali ma'lumot o'g'irlash"), ("Deepfake", "SI bilan yaratilgan soxta video/audio"), ("Netiket", "Internetdagi muloqot odobi")),
    problems=[
        P("Qidiruvda so'zni natijadan chiqarib tashlash uchun qaysi belgi qo'yiladi?", "-", "", "Minus (−)"),
        P("Qidiruvda faqat bitta saytda qidirish operatori (site: ...) — operator nomi?", "site", "", "site:"),
        P("Pochtada yashirin nusxa maydoni nomi (3 harf)?", "Bcc", "", "Bcc"),
        P("Axborotni nechta mustaqil manba bilan solishtirish tavsiya etiladi (kamida)?", "2", "", "Kamida ikkita")],
    sentence_practice=[ORD("Internetdagi axborotni tekshirish tartibi", ["Manbaning kimligini aniqlang", "Sanasiga qarang", "Boshqa mustaqil manbalar bilan solishtiring", "Rasm/videoni teskari qidiruv bilan tekshiring"])],
)

EXTRAS['s6e'] = dict(
    matching=MT(("2G", "Raqamli ovoz va SMS"), ("3G", "Mobil Internet boshlanishi"), ("4G/LTE", "Tezkor mobil Internet"), ("5G", "Gbit/s va kichik kechikish"),
                ("NFC", "Aloqasiz to'lov uchun ~4 sm masofa"), ("WPA3", "Zamonaviy Wi-Fi shifrlash")),
    problems=[
        P("5G tarmog'ida 1 Gbit/s tezlikda 500 MB (4000 Mbit) fayl necha soniyada yuklanadi?", "4", "4000 : 1000", "4", unit="soniya"),
        P("Bluetooth radiusi taxminan necha metr?", "10", "", "~10 m", unit="m"),
        P("Android ilova fayli kengaytmasi? (3 harf)", "apk", "", "APK"),
        P("Wi-Fi ishlaydigan diapazonlardan biri necha GHz? (2,4 yoki 5)", ["2,4", "5"], "", "2,4 va 5 GHz")],
    sentence_practice=[ORD("Telefon yo'qolganda harakatlar tartibi", ["Qurilmani masofadan joylashuv bo'yicha toping", "Qurilmani bloklang", "Muhim akkaunt parollarini almashtiring", "Zarur bo'lsa SIM-kartani bloklang"])],
)
