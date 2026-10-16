# -*- coding: utf-8 -*-
from dsl import P, ORD, TR, MT

EXTRAS = {}

TALABA = "talaba:\nid | ism   | yosh\n1  | Ali   | 15\n2  | Vali  | 16\n3  | Sami  | 15\n4  | Dilya | 17\n\n"

EXTRAS['s7a'] = dict(
    matching=MT(("BMBT", "MB ni yaratish va boshqarish tizimi"), ("Birlamchi kalit", "Har bir yozuvni noyob aniqlaydi"), ("Tashqi kalit", "Boshqa jadval kalitiga havola"),
                ("Normallashtirish", "Ortiqcha takrorlanishni yo'qotish"), ("Indeks", "Qidiruvni tezlashtiradi"), ("Tranzaksiya", "Bo'linmas amallar guruhi")),
    problems=[
        P("Jadvalda 5 ta yozuv va 4 ta maydon bor. Jami nechta katak (qiymat) bor?", "20", "", "5 · 4 = 20"),
        P("Relyatsion modelni taklif qilgan olim familiyasi?", "Kodd", "", "Edgar Kodd (1970)"),
        P("ACID dagi A harfi nimani bildiradi (bir so'z, o'zbekcha)?", "atomarlik", "", "Atomarlik"),
        P("Birlamchi kalit takrorlanishi mumkinmi? (ha/yo'q — 'yo'q' deb yozing)", ["yo'q", "yoq", "yo`q"], "", "Yo'q")],
    sentence_practice=[ORD("Ma'lumotlar bazasini loyihalash bosqichlari", ["Talablarni aniqlash", "ER-diagramma (konseptual model)", "Jadvallar (mantiqiy model)", "Normallashtirish", "BMBT da amalga oshirish"])],
)

EXTRAS['s7b'] = dict(
    matching=MT(("SELECT", "Ma'lumotni tanlash"), ("INSERT", "Yangi yozuv qo'shish"), ("UPDATE", "Yozuvni o'zgartirish"), ("DELETE", "Yozuvni o'chirish"),
                ("WHERE", "Shart bo'yicha filtrlash"), ("GROUP BY", "Yozuvlarni guruhlash")),
    problems=[
        P("WHERE yozilmagan DELETE FROM talaba; nechta yozuvni o'chiradi (jadvalda 4 ta yozuv bor)?", "4", "", "Hammasini — 4 ta"),
        P("Natijani kamayish tartibida saralash kalit so'zi (ORDER BY ... nima)?", "DESC", "", "DESC"),
        P("Takrorlanuvchi qiymatlarni olib tashlovchi kalit so'z?", "DISTINCT", "", "DISTINCT"),
        P("Guruhga shart qo'yish uchun qaysi kalit so'z (WHERE emas)?", "HAVING", "", "HAVING")],
    code_trace=[
        TR(TALABA + "SELECT COUNT(*) FROM talaba WHERE yosh = 15;", "So'rov nima qaytaradi?", "2", "Ali va Sami — 15 yoshda."),
        TR(TALABA + "SELECT ism FROM talaba WHERE yosh > 15 ORDER BY ism;", "So'rov qaytaradigan ismlar (har biri alohida qatorda)?", "Dilya\nVali", "Vali (16) va Dilya (17); alifbo tartibida.", lines=2),
        TR(TALABA + "SELECT MAX(yosh) FROM talaba;", "So'rov nima qaytaradi?", "17", ""),
        TR(TALABA + "SELECT AVG(yosh) FROM talaba;", "So'rov nima qaytaradi?", ["15.75", "15,75"], "(15 + 16 + 15 + 17) / 4 = 15,75"),
        TR(TALABA + "SELECT ism FROM talaba WHERE ism LIKE 'A%';", "So'rov nima qaytaradi?", "Ali", "'A' bilan boshlanuvchi ism.")],
    sentence_practice=[ORD("SQL so'rovi qismlarini to'g'ri tartibda yozing", ["SELECT ism, yosh", "FROM talaba", "WHERE yosh > 15", "ORDER BY ism;"], mono=True)],
)

JT = ("talaba:\nid | ism  | sinf_id\n1  | Ali  | 1\n2  | Vali | 2\n3  | Sami | NULL\n\nsinf:\nid | nom\n1  | 8-A\n2  | 8-B\n\n")
EXTRAS['s7c'] = dict(
    matching=MT(("INNER JOIN", "Faqat ikkala jadvalda mos yozuvlar"), ("LEFT JOIN", "Chap jadvalning hamma yozuvlari"), ("VIEW", "Saqlangan so'rov (virtual jadval)"),
                ("Indeks", "Qidiruvni tezlashtiradi, yozishni sekinlashtiradi"), ("COMMIT", "Tranzaksiyani tasdiqlash"), ("SQL in'eksiya", "Kiritilgan matn orqali zararli SQL")),
    problems=[
        P("SQL in'eksiyadan himoyalanishning asosiy usuli? (ikki so'z: parametrli ...)", ["parametrli so'rovlar", "parametrli sorovlar", "parametrli so'rov"], "", "Parametrli so'rovlar"),
        P("Tranzaksiyani bekor qiluvchi buyruq?", "ROLLBACK", "", "ROLLBACK"),
        P("Uchta jadval ketma-ket JOIN qilinsa, kamida nechta JOIN kerak?", "2", "", "2")],
    code_trace=[
        TR(JT + "SELECT COUNT(*) FROM talaba t INNER JOIN sinf s ON t.sinf_id = s.id;", "So'rov nima qaytaradi?", "2", "Sami ning sinf_id si NULL — mos kelmaydi."),
        TR(JT + "SELECT COUNT(*) FROM talaba t LEFT JOIN sinf s ON t.sinf_id = s.id;", "So'rov nima qaytaradi?", "3", "LEFT JOIN chap jadvalning barcha 3 yozuvini qaytaradi."),
        TR(JT + "SELECT t.ism FROM talaba t INNER JOIN sinf s ON t.sinf_id = s.id WHERE s.nom = '8-B';", "So'rov nima qaytaradi?", "Vali", "")],
    sentence_practice=[ORD("Bank o'tkazmasi tranzaksiyasi tartibi", ["BEGIN;", "UPDATE hisob SET summa = summa - 100 WHERE id = 1;", "UPDATE hisob SET summa = summa + 100 WHERE id = 2;", "COMMIT;"], mono=True)],
)

EXTRAS['s7d'] = dict(
    matching=MT(("O'rta arifmetik", "Yig'indi / soni"), ("Mediana", "Tartiblangan qatorning o'rtasi"), ("Moda", "Eng ko'p uchraydigan qiymat"),
                ("Dispersiya", "O'rtachadan chetlanish kvadratlarining o'rtachasi"), ("Korrelyatsiya", "Miqdorlar bog'liqligi, sababiyat emas"), ("Big Data", "Hajm, tezlik, xilma-xillik")),
    problems=[
        P("[2, 3, 3, 5, 7] ning o'rta arifmetigi?", "4", "", "20/5"),
        P("[1, 2, 9] ning medianasi?", "2", "", "O'rtadagi son"),
        P("[2, 3, 3, 5, 7] ning modasi?", "3", "", "3"),
        P("Normal taqsimotda x̄ ± 2σ oralig'ida taxminan necha foiz qiymat bor?", "95", "", "95%", unit="%")],
    code_trace=[
        TR("import statistics\nprint(statistics.median([1, 2, 9]))", "Dastur nimani chiqaradi?", "2", ""),
        TR("print(sum([2, 4, 6]) / 3)", "Dastur nimani chiqaradi?", "4.0", "/ doim float qaytaradi."),
        TR("import statistics\nprint(statistics.mode([2, 3, 3, 5, 7]))", "Dastur nimani chiqaradi?", "3", "")],
    sentence_practice=[ORD("Ma'lumotlar tahlili bosqichlari", ["Savol/maqsadni aniqlash", "Ma'lumot yig'ish", "Tozalash", "Tahlil", "Vizualizatsiya", "Xulosa"])],
)
