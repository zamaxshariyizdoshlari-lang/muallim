"""Sun'iy intellekt fani uchun to'liq kurs JSON'ini quradi (backend/content/ai/book.json).

Maqsad: kursni tugatgan o'quvchi AI bo'yicha real bilim va ko'nikmaga ega bo'lishi -
AI nima ekanidan tortib, uni kundalik ishda, dasturlashda va pul topishda qanday
qo'llashgacha. Har bir mavzu: tushuntirish bloklari, muhim faktlar, va 10-14 savolli test.
"""
import json

FORMAT_VERSION = 1


def block(heading, text, image=None, image_caption=None):
    b = {'heading': heading, 'text': text}
    if image:
        b['image'] = image
    if image_caption:
        b['image_caption'] = image_caption
    return b


def fact(text):
    return {'fact': text}


def mcq(question, options, correct_index):
    return {'question': question, 'options': options, 'correct_index': correct_index}


def fill_blank(question, answer):
    return {'type': 'fill_blank', 'question': question, 'answer': answer}


def ordering(question, items):
    return {'type': 'ordering', 'question': question, 'items': items}


sections = []

# ============================================================
# BO'LIM 1: SUN'IY INTELLEKT ASOSLARI
# ============================================================
sections.append({
    'key': 's1', 'title': "1-BO'LIM. Sun'iy intellekt asoslari",
    'topics': [
        {
            'key': 't1a', 'title': "Sun'iy intellekt nima?", 'start_page': 1, 'end_page': 1,
            'explanation': {
                'goals': [
                    "Sun'iy intellekt (AI) atamasining ma'nosini tushunish",
                    "AI, mashinaviy o'qitish va chuqur o'qitish orasidagi farqni bilish",
                    "AI kundalik hayotda qayerlarda ishlatilishini aniqlash",
                ],
                'blocks': [
                    block(
                        "Sun'iy intellekt - ta'rif",
                        "**Sun'iy intellekt (Artificial Intelligence, AI)** - bu kompyuter dasturlarining "
                        "inson kabi \"aqlli\" ishlarni bajarish qobiliyati: tilni tushunish, rasmni tanish, "
                        "qaror qabul qilish, muammoni yechish. Muhim narsa shuki, AI \"o'ylamaydi\" - u "
                        "==katta hajmdagi ma'lumotlardan naqshlarni (pattern) o'rganib, shu naqshlar "
                        "asosida bashorat qiladi==. Masalan, agar dasturga million ta mushuk rasmini "
                        "ko'rsatsangiz, u \"mushuk nima ekanini tushunadi\" emas, balki mushuklarga xos "
                        "vizual naqshlarni statistik jihatdan aniqlashni o'rganadi.\n\n"
                        "AI atamasi 1956-yilda Dartmut konferensiyasida John McCarthy tomonidan "
                        "taklif qilingan, ammo g'oyaning o'zi undan ham qadimiy - odamlar doim "
                        "\"o'ylay oladigan mashina\" haqida orzu qilishgan.",
                    ),
                    block(
                        "AI, Machine Learning, Deep Learning - farqi",
                        "Bu uchta atama ko'pincha aralashtirib yuboriladi, lekin ular **bir-birining "
                        "ichiga joylashgan** tushunchalar:\n\n"
                        "1. **Sun'iy intellekt (AI)** - eng katta doira: mashinaning \"aqlli\" harakat "
                        "qilishga urinishi (hatto oddiy \"agar-unda\" qoidalar bilan yozilgan dastur ham "
                        "AI hisoblanishi mumkin).\n"
                        "2. **Mashinaviy o'qitish (Machine Learning, ML)** - AI'ning bir qismi: dastur "
                        "qoidalarni qo'lda yozib berilmaydi, balki ==misollardan (data) o'zi o'rganadi==.\n"
                        "3. **Chuqur o'qitish (Deep Learning)** - ML'ning bir qismi: inson miyasidagi "
                        "neyronlarga o'xshash \"neyron tarmoqlar\" (neural network) yordamida ishlaydi, "
                        "ayniqsa rasm, ovoz va tilni tushunishda juda kuchli.\n\n"
                        "Hozirgi ChatGPT, Claude, Gemini kabi mashhur AI tizimlarning barchasi - "
                        "**chuqur o'qitish** asosida qurilgan.",
                    ),
                    block(
                        "AI kundalik hayotda qayerda ishlatiladi",
                        "AI sizning atrofingizda allaqachon mavjud, ko'pincha buni sezmaysiz ham:\n\n"
                        "- **Telefon**: yuzni tanish orqali qulfni ochish, ovozli yordamchi (Siri, Google Assistant)\n"
                        "- **Ijtimoiy tarmoqlar**: lentangizda qanday post ko'rsatishni AI hal qiladi\n"
                        "- **Onlayn xarid**: \"sizga yoqishi mumkin\" tavsiyalari (Amazon, Uzum)\n"
                        "- **Xarita ilovalari**: eng qisqa yo'lni topish, tirbandlikni bashorat qilish\n"
                        "- **Bank**: firibgarlikni (fraud) aniqlash tizimlari\n"
                        "- **Tibbiyot**: rentgen va MRI rasmlarida kasallikni aniqlashda yordam\n\n"
                        "Shuning uchun AI'ni \"kelajak texnologiyasi\" emas, balki **hozirgi kunning "
                        "asosiy vositasi** deb bilish kerak.",
                    ),
                ],
                'key_facts': [
                    fact("AI atamasi 1956-yilda John McCarthy tomonidan taklif qilingan."),
                    fact("Machine Learning - AI'ning bir qismi, dastur misollardan o'zi o'rganadi."),
                    fact("Deep Learning - ML'ning bir qismi, neyron tarmoqlardan foydalanadi."),
                    fact("ChatGPT, Claude, Gemini - barchasi Deep Learning asosida qurilgan."),
                ],
                'summary': "==AI - katta doira==, uning ichida **Machine Learning**, uning ichida esa "
                           "**Deep Learning** joylashgan. Zamonaviy suhbat-AI'lar aynan Deep Learning asosida ishlaydi.",
            },
            'test': [
                mcq("Sun'iy intellekt atamasini kim va qachon taklif qilgan?", [
                    "John McCarthy, 1956-yil", "Alan Turing, 1950-yil", "Bill Gates, 1980-yil", "Elon Musk, 2015-yil",
                ], 0),
                mcq("Quyidagilardan qaysi biri to'g'ri ierarxiya?", [
                    "AI > Machine Learning > Deep Learning",
                    "Deep Learning > AI > Machine Learning",
                    "Machine Learning > Deep Learning > AI",
                    "Hammasi bir xil narsa",
                ], 0),
                mcq("Machine Learning'ning asosiy g'oyasi nima?", [
                    "Dastur misollardan (data) o'zi o'rganadi",
                    "Dastur faqat qo'lda yozilgan qoidalarni bajaradi",
                    "Dastur internetdan ma'lumot qidiradi",
                    "Dastur insonning har bir harakatini nusxalaydi",
                ], 0),
                mcq("ChatGPT, Claude, Gemini qaysi texnologiyaga asoslangan?", [
                    "Deep Learning (chuqur o'qitish)", "Oddiy agar-unda qoidalar",
                    "Faqat internet qidiruvi", "Qo'lda yozilgan javoblar bazasi",
                ], 0),
                mcq("Quyidagilardan qaysi biri AI ishlatilishiga MISOL EMAS?", [
                    "Oddiy kalkulyatorda qo'shish-ayirish", "Yuzni tanib qulfni ochish",
                    "Onlayn do'konning tavsiyalari", "Bank firibgarligini aniqlash",
                ], 0),
                mcq("Nega AI \"o'ylaydi\" deyish noto'g'ri?", [
                    "U ma'lumotlardagi naqshlarni statistik aniqlaydi, inson kabi anglamaydi",
                    "Chunki AI umuman ishlamaydi",
                    "Chunki AI faqat robotlarda bo'ladi",
                    "Chunki AI insondan aqlliroq",
                ], 0),
                fill_blank("AI ning ichida joylashgan, misollardan o'rganadigan qism qanday ataladi? (inglizcha qisqartma emas, to'liq ibora bilan javob bering: \"Mashinaviy o'qitish\")", "Mashinaviy o'qitish"),
                mcq("Neyron tarmoqlar nimaga o'xshab ishlaydi?", [
                    "Inson miyasidagi neyronlarga", "Kompyuter protsessoriga",
                    "Internet tarmog'iga", "Telefon simiga",
                ], 0),
                ordering("AI ierarxiyasini eng kattasidan eng kichigigacha tartiblang.", [
                    "Sun'iy intellekt (AI)", "Mashinaviy o'qitish (ML)", "Chuqur o'qitish (Deep Learning)",
                ]),
                mcq("Rasmda kasallikni aniqlashga yordam berish qaysi sohaga misol?", [
                    "Tibbiyotda AI", "Bank sohasida AI", "Transport sohasida AI", "Ta'lim sohasida AI",
                ], 0),
            ],
        },
        {
            'key': 't1b', 'title': "Mashinaviy o'qitish qanday ishlaydi", 'start_page': 2, 'end_page': 2,
            'explanation': {
                'goals': [
                    "Mashinaviy o'qitish jarayonini oddiy tilda tushunish",
                    "\"Train\" (o'qitish) va \"model\" tushunchalarini bilish",
                    "Nazorat ostidagi va nazoratsiz o'qitish farqini aniqlash",
                ],
                'blocks': [
                    block(
                        "Mashina qanday \"o'rganadi\"?",
                        "Mashinaviy o'qitishni tushunish uchun oddiy misol: bolaga \"mushuk\" va \"it\" "
                        "rasmlarini ko'p marta ko'rsatib, har birida \"bu mushuk\", \"bu it\" deb aytasiz. "
                        "Vaqt o'tishi bilan bola yangi rasmni ko'rib, o'zi ajrata boshlaydi - garchi unga "
                        "\"mushukning qulog'i uchburchak, mo'ylovi bor\" deb qoidalar yozib berilmagan bo'lsa ham.\n\n"
                        "Mashinaviy o'qitishda ham xuddi shunday: dasturchi kompyuterga ==minglab, hatto "
                        "millionlab misol (data)== beradi, va maxsus algoritm shu misollardagi naqshlarni "
                        "avtomatik topadi. Natijada hosil bo'lgan narsa **\"model\"** deb ataladi - bu "
                        "aslida son (raqam)lardan iborat murakkab matematik formula.",
                    ),
                    block(
                        "O'qitish turlari",
                        "Mashinaviy o'qitishning uchta asosiy turi bor:\n\n"
                        "**1. Nazorat ostidagi o'qitish (Supervised Learning)** - har bir misolga "
                        "\"to'g'ri javob\" (label) biriktirilgan. Masalan: rasm + \"bu mushuk\" yorlig'i. "
                        "Email spam-filtri shunday ishlaydi: minglab email + \"spam\"/\"spam emas\" belgisi.\n\n"
                        "**2. Nazoratsiz o'qitish (Unsupervised Learning)** - misollarga yorliq berilmaydi, "
                        "dastur o'zi o'xshash narsalarni guruhlarga ajratadi. Masalan: onlayn do'kon "
                        "mijozlarini xarid odatlariga qarab avtomatik guruhlarga bo'lish.\n\n"
                        "**3. Mustahkamlovchi o'qitish (Reinforcement Learning)** - dastur \"sinov va "
                        "xato\" orqali o'rganadi, to'g'ri harakat uchun \"mukofot\" oladi. Shaxmat yoki "
                        "Go o'ynaydigan AI'lar (masalan AlphaGo) shunday o'qitilgan.",
                    ),
                    block(
                        "Nega ko'p ma'lumot (data) kerak?",
                        "Model qanchalik ko'p va xilma-xil misoldan o'qitilsa, u shunchalik yaxshi ishlaydi. "
                        "Agar mushuk-rasmlarni faqat oq mushuklardan o'qitsangiz, model qora mushukni "
                        "\"mushuk emas\" deb xato qilishi mumkin - bu **==noto'g'ri yoki bir tomonlama "
                        "ma'lumot (bias)== muammosi** deb ataladi va zamonaviy AI'dagi eng jiddiy "
                        "muammolardan biri hisoblanadi (masalan, ba'zi yuzni tanish tizimlari muayyan "
                        "irqdagi odamlarni yomonroq aniqlaydi, chunki o'qitish ma'lumotida ular kam bo'lgan).",
                    ),
                ],
                'key_facts': [
                    fact("Model - misollardan o'rganish natijasida hosil bo'lgan matematik formula."),
                    fact("Nazorat ostidagi o'qitishda har bir misolga to'g'ri javob (label) biriktirilgan."),
                    fact("Nazoratsiz o'qitishda dastur o'zi o'xshashlarni guruhlaydi."),
                    fact("Mustahkamlovchi o'qitishda dastur mukofot orqali, sinab-xato qilib o'rganadi."),
                    fact("Bias (bir tomonlama ma'lumot) - noto'g'ri yoki cheklangan ma'lumotdan kelib chiquvchi xato."),
                ],
                'summary': "Mashinaviy o'qitish - ko'p misoldan naqsh topib, **model** yaratish jarayoni. "
                           "Uchta asosiy turi: **nazorat ostida**, **nazoratsiz** va **mustahkamlovchi** o'qitish.",
            },
            'test': [
                mcq("\"Model\" atamasi mashinaviy o'qitishda nimani anglatadi?", [
                    "Misollardan o'rganish natijasida hosil bo'lgan matematik formula",
                    "Kompyuterning jismoniy qismi",
                    "Dasturchi yozgan qo'lda qoidalar to'plami",
                    "Internet sayti",
                ], 0),
                mcq("Email spam-filtri qaysi o'qitish turiga misol?", [
                    "Nazorat ostidagi o'qitish", "Nazoratsiz o'qitish",
                    "Mustahkamlovchi o'qitish", "Hech qaysisiga emas",
                ], 0),
                mcq("Mijozlarni xarid odatiga qarab avtomatik guruhlash - bu qanday o'qitish?", [
                    "Nazoratsiz o'qitish", "Nazorat ostidagi o'qitish",
                    "Mustahkamlovchi o'qitish", "Bu mashinaviy o'qitish emas",
                ], 0),
                mcq("AlphaGo kabi o'yin o'ynaydigan AI qanday o'qitilgan?", [
                    "Mustahkamlovchi o'qitish (sinov-xato, mukofot orqali)",
                    "Faqat qo'lda yozilgan qoidalar bilan",
                    "Nazoratsiz o'qitish",
                    "Umuman o'qitilmagan",
                ], 0),
                mcq("\"Bias\" (bir tomonlama ma'lumot) muammosi nimadan kelib chiqadi?", [
                    "O'qitish ma'lumoti to'liq yoki xilma-xil bo'lmaganidan",
                    "Kompyuter juda kuchli bo'lganidan",
                    "Dasturchi juda ko'p kod yozganidan",
                    "Internet tezligi past bo'lganidan",
                ], 0),
                mcq("Nazorat ostidagi o'qitishning asosiy belgisi nima?", [
                    "Har bir misolga to'g'ri javob (label) biriktirilgan",
                    "Hech qanday misol kerak emas",
                    "Faqat rasm bilan ishlaydi",
                    "Internetga ulanish shart",
                ], 0),
                fill_blank("Yuzni tanish tizimi muayyan guruhni yomonroq aniqlasa, bu qanday muammo deb ataladi? (inglizcha so'z bilan javob bering)", "bias"),
                mcq("Bola mushuk va itni farqlashni o'rganishi qaysi jarayonga o'xshatilgan?", [
                    "Nazorat ostidagi o'qitish (misol + to'g'ri javob orqali)",
                    "Mustahkamlovchi o'qitish",
                    "Dasturlash tili o'rganish",
                    "Internetdan qidiruv",
                ], 0),
                mcq("Model qanchalik yaxshi ishlashi asosan nimaga bog'liq?", [
                    "O'qitilgan ma'lumotning ko'pligi va xilma-xilligiga",
                    "Kompyuterning rangiga", "Dasturchining yoshiga", "Internetning narxiga",
                ], 0),
            ],
        },
        {
            'key': 't1c', 'title': "Katta til modellari (LLM) va ChatGPT sirlari", 'start_page': 3, 'end_page': 3,
            'explanation': {
                'goals': [
                    "LLM (Large Language Model) nima ekanini tushunish",
                    "ChatGPT/Claude/Gemini qanday \"javob o'ylab topishini\" bilish",
                    "\"Hallucination\" (to'qib chiqarish) xavfini tushunish",
                ],
                'blocks': [
                    block(
                        "LLM nima?",
                        "**Katta til modeli (Large Language Model, LLM)** - bu internetdagi juda katta "
                        "hajmdagi matn (kitoblar, maqolalar, veb-saytlar) asosida o'qitilgan, ==keyingi "
                        "so'zni bashorat qilishni o'rgangan== neyron tarmoq. ChatGPT (OpenAI), Claude "
                        "(Anthropic) va Gemini (Google) - barchasi LLM'lar.\n\n"
                        "Oddiy qilib aytganda, LLM \"Bugun ob-havo juda...\" gapini ko'rganda, keyingi "
                        "so'z \"issiq\", \"sovuq\" yoki \"yomg'irli\" bo'lishi ehtimolini hisoblab, eng "
                        "mos so'zni tanlaydi. Bu jarayon millionlab marta takrorlanib, butun bir javob "
                        "(bir necha paragraf) hosil bo'ladi - va bu shunchalik silliq ishlaydiki, xuddi "
                        "model \"tushunayotganday\" tuyuladi.",
                    ),
                    block(
                        "Nega ba'zan noto'g'ri javob beradi? (Hallucination)",
                        "LLM **haqiqatni bilmaydi** - u faqat \"qaysi so'z ehtimoli ko'proq\" degan "
                        "statistikaga asoslanadi. Shuning uchun ba'zan u ==ishonchli ohangda, lekin "
                        "noto'g'ri yoki to'qilgan ma'lumot== berishi mumkin - bu hodisa **\"hallucination\"** "
                        "(gallyutsinatsiya) deb ataladi. Masalan, LLM mavjud bo'lmagan kitob nomini yoki "
                        "sana xatosini juda ishonchli tarzda aytib berishi mumkin.\n\n"
                        "**Shuning uchun oltin qoida**: LLM javobini, ayniqsa muhim faktlar (sana, "
                        "statistika, havola)ni har doim boshqa manbadan tekshiring.",
                    ),
                    block(
                        "LLM'ning kuchli va zaif tomonlari",
                        "**Kuchli tomonlari:**\n"
                        "- Matn yozish, qayta yozish, tarjima qilish\n"
                        "- G'oyalarni tushuntirish, murakkab mavzularni soddalashtirish\n"
                        "- Dastur kodi yozish va tushuntirish\n"
                        "- Katta hajmdagi matnni qisqartirish (summarize)\n\n"
                        "**Zaif tomonlari:**\n"
                        "- Aniq matematik hisob-kitoblarda xato qilishi mumkin\n"
                        "- Eng so'nggi voqealarni bilmasligi mumkin (o'qitish sanasidan keyingisini)\n"
                        "- Hallucination xavfi\n"
                        "- Murakkab, ko'p bosqichli mantiqiy masalalarda adashishi mumkin\n\n"
                        "Zamonaviy AI vositalari (masalan Claude Code) bu zaifliklarni **tashqi "
                        "vositalar** (kalkulyator, internet qidiruv, kod ishga tushirish) bilan birlashtirib "
                        "kamaytiradi - bu haqida keyingi bo'limda batafsil o'rganamiz.",
                    ),
                ],
                'key_facts': [
                    fact("LLM - internetdagi katta matn to'plamidan o'qitilgan, keyingi so'zni bashorat qiluvchi model."),
                    fact("ChatGPT, Claude, Gemini - eng mashhur LLM'lar."),
                    fact("Hallucination - LLM ishonchli ohangda noto'g'ri/to'qilgan ma'lumot berishi."),
                    fact("Muhim faktlarni LLM javobidan keyin boshqa manbadan tekshirish kerak."),
                ],
                'summary': "LLM - katta matn to'plamidan **keyingi so'zni bashorat qilishni** o'rgangan model. "
                           "U kuchli, lekin ==hallucination== xavfi bor - shuning uchun muhim faktlarni doim tekshiring.",
            },
            'test': [
                mcq("LLM (Large Language Model) nimani o'rgangan?", [
                    "Keyingi so'zni bashorat qilishni", "Faqat rasmni tanishni",
                    "Faqat matematik masalalarni yechishni", "Faqat video ko'rishni",
                ], 0),
                mcq("\"Hallucination\" atamasi AI kontekstida nimani anglatadi?", [
                    "AI ishonchli ohangda noto'g'ri/to'qilgan ma'lumot berishi",
                    "AI kompyuterni buzib qo'yishi",
                    "AI internetdan uzilib qolishi",
                    "AI juda sekin ishlashi",
                ], 0),
                mcq("Quyidagilardan qaysi biri LLM'ga MISOL EMAS?", [
                    "Oddiy kalkulyator dasturi", "ChatGPT", "Claude", "Gemini",
                ], 0),
                mcq("LLM javobidagi muhim faktlar bilan nima qilish tavsiya etiladi?", [
                    "Boshqa manbadan tekshirish", "Har doim so'zma-so'z ishonish",
                    "E'tiborsiz qoldirish", "Faqat bir marta so'rab, qayta so'ramaslik",
                ], 0),
                mcq("LLM'ning qaysi ishda ko'proq xato qilish ehtimoli bor?", [
                    "Aniq murakkab matematik hisob-kitoblarda", "Matnni qayta yozishda",
                    "G'oyani soddalashtirishda", "Tilni tarjima qilishda",
                ], 0),
                mcq("LLM nega \"eng so'nggi voqealarni\" bilmasligi mumkin?", [
                    "U ma'lum bir sanagacha bo'lgan ma'lumot bilan o'qitilgan",
                    "U internetga umuman ulanmaydi",
                    "U hech qachon yangilanmaydi",
                    "U faqat kitoblarni o'qiydi",
                ], 0),
                fill_blank("AI ishonchli ohangda noto'g'ri yoki to'qilgan ma'lumot berish holati inglizcha qanday ataladi?", "hallucination"),
                mcq("LLM qanday ishlab, javob \"tushunayotganday\" tuyuladi?", [
                    "Millionlab marta so'z bashorat qilish jarayonini takrorlab",
                    "Internetdan real vaqtda qidirib",
                    "Insonlar bilan telefon orqali gaplashib",
                    "Faqat oldindan yozilgan javoblarni o'qib",
                ], 0),
                mcq("Zamonaviy AI vositalari LLM zaifliklarini qanday kamaytiradi?", [
                    "Tashqi vositalar (kalkulyator, qidiruv, kod ishga tushirish) bilan birlashtirib",
                    "LLM'ni butunlay o'chirib",
                    "Faqat insonlarga ishonib",
                    "Internetni o'chirib",
                ], 0),
            ],
        },
    ],
})

# (qolgan bo'limlar pastda qo'shiladi - fayl oxirida yakuniy yozish bor)

# ============================================================
# BO'LIM 2: AI BILAN MULOQOT QILISH SAN'ATI (PROMPT ENGINEERING)
# ============================================================
sections.append({
    'key': 's2', 'title': "2-BO'LIM. Prompt yozish san'ati",
    'topics': [
        {
            'key': 't2a', 'title': "Yaxshi prompt yozish asoslari", 'start_page': 4, 'end_page': 4,
            'explanation': {
                'goals': [
                    "Prompt nima ekanini va nega u muhimligini tushunish",
                    "Yaxshi va yomon promptlar orasidagi farqni ko'rish",
                    "Aniq, kontekstli prompt yozishni o'rganish",
                ],
                'blocks': [
                    block(
                        "Prompt nima?",
                        "**Prompt** - bu siz AI'ga yozadigan so'rov yoki buyruq. AI javobining sifati "
                        "==to'g'ridan-to'g'ri sizning promptingiz sifatiga bog'liq== - shuning uchun "
                        "\"prompt yozish san'ati\" (prompt engineering) alohida ko'nikma hisoblanadi.\n\n"
                        "Solishtiring:\n"
                        "- Yomon prompt: \"Insho yoz\"\n"
                        "- Yaxshi prompt: \"7-sinf o'quvchisi uchun, 'Kitob o'qishning foydalari' "
                        "mavzusida, 150 so'zdan iborat, sodda tilda insho yoz\"\n\n"
                        "Ikkinchi holatda AI aniq nima kerakligini biladi va natija ancha sifatli bo'ladi.",
                    ),
                    block(
                        "Yaxshi promptning 4 ta belgisi",
                        "**1. Aniqlik (Specificity)** - \"nimadir yoz\" emas, aniq nima kerakligini ayting.\n\n"
                        "**2. Kontekst (Context)** - kim uchun, qaysi maqsadda, qanday holatda ekanini "
                        "tushuntiring. Masalan: \"Men boshlang'ich dasturchiman\" deyish AI javobini "
                        "soddalashtiradi.\n\n"
                        "**3. Format (Format)** - javobni qanday ko'rinishda xohlaysiz: ro'yxat, jadval, "
                        "paragraf, kod? Buni oldindan ayting.\n\n"
                        "**4. Cheklov (Constraints)** - uzunlik, til, uslub kabi cheklovlarni belgilang: "
                        "\"3 ta gapdan oshmasin\", \"rasmiy uslubda\", \"o'zbek tilida\".\n\n"
                        "Bu to'rttasini birlashtirib ko'ring: **\"[Kontekst]. [Aniq vazifa]. [Format]da, "
                        "[cheklov] bilan javob ber.\"**",
                    ),
                    block(
                        "Amaliy misol: yomondan yaxshigacha",
                        "**Bosqich 1 (yomon):** \"Marketing haqida gapir\"\n\n"
                        "**Bosqich 2 (yaxshiroq):** \"Kichik biznes uchun marketing strategiyasi haqida gapir\"\n\n"
                        "**Bosqich 3 (yaxshi):** \"Men Toshkentda kichik kafe ochyapman. Byudjetim kam. "
                        "Ijtimoiy tarmoqlar orqali mijoz jalb qilish uchun 5 ta oddiy, arzon strategiya "
                        "taklif qil, har birini 1-2 gapda tushuntir.\"\n\n"
                        "Ko'rib turganingizdek, ==qancha ko'p tegishli detal bersangiz, javob shunchalik "
                        "foydali va amaliy bo'ladi==. AI sizning fikringizni o'qiy olmaydi - siz nima "
                        "kutayotganingizni aniq ayting.",
                    ),
                ],
                'key_facts': [
                    fact("Prompt - AI'ga yoziladigan so'rov; javob sifati prompt sifatiga bog'liq."),
                    fact("Yaxshi promptning 4 belgisi: aniqlik, kontekst, format, cheklov."),
                    fact("AI fikringizni o'qiy olmaydi - kerakli detallarni aniq yozish kerak."),
                ],
                'summary': "Yaxshi prompt = **aniq vazifa** + **kontekst** + **format** + **cheklov**. "
                           "Qancha aniq so'rasangiz, AI javobi shuncha foydali bo'ladi.",
            },
            'test': [
                mcq("Prompt nima?", [
                    "AI'ga yoziladigan so'rov yoki buyruq", "Kompyuter dasturi nomi",
                    "Internet sayti manzili", "Dasturlash tili",
                ], 0),
                mcq("Quyidagilardan qaysi biri YAXSHI prompt misoli?", [
                    "\"7-sinf o'quvchisi uchun 150 so'zli insho yoz, mavzu: kitob o'qish foydasi\"",
                    "\"Insho yoz\"", "\"Nimadir yoz\"", "\"Yordam ber\"",
                ], 0),
                mcq("Yaxshi promptning 4 ta belgisidan biri EMAS qaysi?", [
                    "Uzunlik (har doim eng uzun bo'lishi)", "Aniqlik", "Kontekst", "Format",
                ], 0),
                mcq("\"Kontekst\" prompt yozishda nimani anglatadi?", [
                    "Kim uchun, qaysi maqsadda ekanini tushuntirish",
                    "Faqat inglizcha yozish",
                    "Iloji boricha qisqa yozish",
                    "Savol belgisi qo'yish",
                ], 0),
                mcq("Nega AI'ga aniq detal berish muhim?", [
                    "AI sizning fikringizni o'qiy olmaydi, faqat yozganingizga tayanadi",
                    "AI aks holda ishlamay qoladi", "Bu majburiy qonun talabi",
                    "Aniq bo'lmasa AI xafa bo'ladi",
                ], 0),
                mcq("\"Format\" deganda nima nazarda tutiladi?", [
                    "Javobning ko'rinishi: ro'yxat, jadval, paragraf yoki kod",
                    "Faylning kengaytmasi", "Kompyuterning turi", "Internet tezligi",
                ], 0),
                fill_blank("AI'dan yaxshi javob olish uchun so'rovni qanday yozish sanati deb ataladi? (\"Prompt ...\")", "Prompt engineering"),
                ordering("Yaxshi prompt qurish bosqichlarini mantiqiy tartibda joylashtiring.", [
                    "Kontekstni tushuntirish", "Aniq vazifani belgilash", "Kerakli formatni ko'rsatish", "Cheklovlarni qo'shish",
                ]),
            ],
        },
        {
            'key': 't2b', 'title': "Murakkab promptlash texnikalari", 'start_page': 5, 'end_page': 5,
            'explanation': {
                'goals': [
                    "Rol berish (role prompting) texnikasini o'rganish",
                    "Misol bilan o'rgatish (few-shot) usulini tushunish",
                    "Bosqichma-bosqich fikrlashga undash (chain-of-thought) texnikasini bilish",
                ],
                'blocks': [
                    block(
                        "1-texnika: Rol berish (Role Prompting)",
                        "AI'ga ma'lum bir **rol** berish - javob sifatini oshirishning eng oson yo'llaridan "
                        "biri. Masalan:\n\n"
                        "- \"Sen tajribali tarix o'qituvchisisan. 10 yoshli bolaga Amir Temur haqida gapirib ber.\"\n"
                        "- \"Sen professional dasturchisan. Ushbu kodni ko'rib chiq va xatolarni top.\"\n\n"
                        "Rol berish AI'ning ==qaysi \"uslub\" va \"chuqurlik darajasida\" javob berishini== "
                        "aniqlashtiradi - xuddi haqiqiy hayotda turli mutaxassislardan maslahat so'raganday.",
                    ),
                    block(
                        "2-texnika: Misol bilan o'rgatish (Few-shot Prompting)",
                        "Agar AI'dan aniq bir formatda javob kutayotgan bo'lsangiz, unga **1-2 ta misol** "
                        "ko'rsating. Masalan:\n\n"
                        "\"Quyidagi formatda mahsulot nomlarini tarjima qil:\n"
                        "Apple -> Olma\n"
                        "Banana -> Banan\n"
                        "Endi shularni tarjima qil: Orange, Grape, Mango\"\n\n"
                        "Bu usul **\"few-shot\" (bir necha misol)** deb ataladi va AI'ga aniq nima "
                        "kutilayotganini \"ko'rsatib\" beradi - so'z bilan tushuntirishdan ko'ra ishonchliroq.",
                    ),
                    block(
                        "3-texnika: Bosqichma-bosqich fikrlash (Chain-of-Thought)",
                        "Murakkab, ko'p bosqichli masalalarda AI'dan to'g'ridan-to'g'ri javob emas, "
                        "==\"bosqichma-bosqich o'ylab chiq\" deb so'rash== xatolarni sezilarli kamaytiradi. "
                        "Masalan:\n\n"
                        "- Oddiy: \"37 ta olma bor, har biriga 4 tadan bersam, nechta odamga yetadi va "
                        "nechta qoladi?\"\n"
                        "- Yaxshiroq: \"37 ta olma bor, har biriga 4 tadan bersam, nechta odamga yetadi va "
                        "nechta qoladi? Bosqichma-bosqich hisoblab, oxirida yakuniy javobni ayt.\"\n\n"
                        "Bu texnika ayniqsa matematik, mantiqiy va ko'p qadamli masalalarda juda foydali - "
                        "chunki AI \"shoshilib\" yakuniy javobga o'tish o'rniga, har bir qadamni tekshirib boradi.",
                    ),
                    block(
                        "Texnikalarni birlashtirish",
                        "Eng kuchli natija - bu texnikalarni **birlashtirganda** chiqadi. Masalan: "
                        "\"Sen matematika o'qituvchisisan (rol). Quyidagi 2 ta misolga o'xshab, masalani "
                        "yech (few-shot): [misollar]. Endi mana bu masalani bosqichma-bosqich yech "
                        "(chain-of-thought): [masala]\". Amaliyotda ko'proq mashq qilgan sari, qaysi "
                        "texnika qachon kerakligini his qila boshlaysiz.",
                    ),
                ],
                'key_facts': [
                    fact("Rol berish (role prompting) - AI'ga ma'lum mutaxassis rolini berish."),
                    fact("Few-shot - AI'ga 1-2 ta misol ko'rsatib, kutilgan formatni ko'rsatish."),
                    fact("Chain-of-thought - AI'ni bosqichma-bosqich fikrlashga undash, xatoni kamaytiradi."),
                    fact("Texnikalarni birlashtirish eng kuchli natija beradi."),
                ],
                'summary': "Uchta kuchli texnika: **rol berish**, **misol bilan o'rgatish (few-shot)** va "
                           "**bosqichma-bosqich fikrlash (chain-of-thought)**. Ularni birlashtirib ishlating.",
            },
            'test': [
                mcq("\"Sen tajribali shifokorsan...\" kabi prompt qaysi texnikaga misol?", [
                    "Rol berish (role prompting)", "Few-shot", "Chain-of-thought", "Hech qaysisi",
                ], 0),
                mcq("Few-shot texnikasining mohiyati nima?", [
                    "AI'ga 1-2 ta misol ko'rsatib, kutilgan formatni namoyish qilish",
                    "AI'ga hech qanday misol bermaslik",
                    "Faqat bitta so'z bilan so'rash",
                    "AI'ni imtihon qilish",
                ], 0),
                mcq("\"Bosqichma-bosqich o'ylab chiq\" deb so'rash qaysi texnika?", [
                    "Chain-of-thought", "Role prompting", "Few-shot", "Fine-tuning",
                ], 0),
                mcq("Chain-of-thought texnikasi ayniqsa qaysi turdagi masalalarda foydali?", [
                    "Ko'p bosqichli matematik/mantiqiy masalalarda",
                    "Oddiy salomlashishda",
                    "Bitta so'zli javoblarda",
                    "Rasm chizishda",
                ], 0),
                mcq("Rol berish nimaga yordam beradi?", [
                    "Javob uslubi va chuqurligini aniqlashtirishga",
                    "AI'ni tezroq ishlashga majburlashga",
                    "Internetga ulanishga",
                    "Kompyuterni tezlashtirishga",
                ], 0),
                mcq("Eng kuchli natija odatda qachon chiqadi?", [
                    "Bir nechta texnika birlashtirilganda", "Faqat bitta texnika ishlatilganda",
                    "Hech qanday texnika ishlatilmaganda", "Prompt juda qisqa bo'lganda",
                ], 0),
                fill_blank("AI'ga 1-2 ta namunaviy misol ko'rsatib o'rgatish texnikasi inglizcha qanday ataladi?", "few-shot"),
                mcq("Nega \"bosqichma-bosqich yech\" deb so'rash xatoni kamaytiradi?", [
                    "AI shoshilib yakuniy javobga o'tmay, har qadamni tekshirib boradi",
                    "Chunki bu AI'ni sekinlashtiradi va hech qanday foyda bermaydi",
                    "Chunki bu AI'ni internetdan qidirishga majburlaydi",
                    "Chunki bu qonuniy talab",
                ], 0),
            ],
        },
        {
            'key': 't2c', 'title': "AI bilan matn yozish, tahlil va tadqiqot", 'start_page': 6, 'end_page': 6,
            'explanation': {
                'goals': [
                    "AI yordamida matn yozish va tahrirlashni o'rganish",
                    "Katta hujjatlarni qisqartirish (summarize) usulini bilish",
                    "AI yordamida tadqiqot qilishda ehtiyot choralarini tushunish",
                ],
                'blocks': [
                    block(
                        "AI - yozuvchi emas, yordamchi",
                        "AI'dan matn yozishda foydalanishning eng samarali yo'li - uni **to'liq muallif** "
                        "emas, balki **yordamchi muharrir** sifatida ko'rish. Masalan:\n\n"
                        "- Birinchi qoralamani o'zingiz yozing, AI'dan uni **yaxshilashni** so'rang\n"
                        "- Yoki AI'dan qoralama so'rab, uni **o'zingiz tahrirlang va shaxsiylashtiring**\n\n"
                        "==AI matnini o'zgartirmasdan to'g'ridan-to'g'ri ishlatish== - ayniqsa muhim "
                        "hujjatlar, maqolalar, uy vazifalarida - sifat va halollik nuqtai nazaridan "
                        "muammoli. AI - vaqtingizni tejaydigan vosita, fikringizni almashtiruvchi emas.",
                    ),
                    block(
                        "Katta matnni qisqartirish (Summarization)",
                        "AI'ning eng foydali qobiliyatlaridan biri - ==uzun hujjat, maqola yoki kitobni "
                        "tez qisqartirib berish==. Buning uchun:\n\n"
                        "1. Matnni AI'ga bering (yoki nusxalab joylashtiring)\n"
                        "2. Nima xohlayotganingizni aniq ayting: \"5 ta asosiy fikrni ro'yxat qilib ber\" "
                        "yoki \"3 paragrafda qisqartir\"\n"
                        "3. Kerak bo'lsa, \"kim uchun\" ekanini ayting: \"boshlang'ich darajadagi "
                        "o'quvchi tushunadigan tilda\"\n\n"
                        "Bu usul o'quv materiallarini tezda ko'rib chiqish, ish hujjatlarini tahlil "
                        "qilish uchun juda qulay.",
                    ),
                    block(
                        "AI bilan tadqiqot qilishda ehtiyot choralari",
                        "AI tadqiqot uchun ajoyib **boshlang'ich nuqta**, lekin **yakuniy manba emas**:\n\n"
                        "- AI'dan mavzuni tushuntirishni, asosiy tushunchalarni so'rang\n"
                        "- Keyin **muhim faktlar, statistika, sanalarni** ishonchli manbalardan "
                        "(rasmiy sayt, kitob, ilmiy jurnal) tekshiring\n"
                        "- AI'dan \"bu haqiqatmi yoki bashoratmi?\" deb so'rash ba'zan foydali, lekin "
                        "u hamon xato qilishi mumkinligini unutmang (hallucination, 1-bo'limda o'rgangan edik)\n\n"
                        "**Oltin qoida**: AI - tezkor tushuntiruvchi, sekin lekin ishonchli tekshiruvchi "
                        "emas. Ikkalasini birga ishlatganda eng yaxshi natija chiqadi.",
                    ),
                ],
                'key_facts': [
                    fact("AI'ni to'liq muallif emas, yordamchi muharrir sifatida ishlatish tavsiya etiladi."),
                    fact("Summarization - AI yordamida uzun matnni qisqartirish."),
                    fact("Tadqiqotda AI - boshlang'ich nuqta, muhim faktlarni boshqa manbadan tekshirish kerak."),
                ],
                'summary': "AI matn yozishda **yordamchi**, tadqiqotda **boshlang'ich nuqta** - lekin "
                           "==yakuniy tekshiruv doim insonga== qoladi.",
            },
            'test': [
                mcq("AI'dan matn yozishda foydalanishning eng samarali yo'li qanday?", [
                    "Uni yordamchi muharrir sifatida ishlatish, o'zingiz tahrirlash",
                    "AI yozganini o'zgarishsiz ishlatish",
                    "AI'ga umuman murojaat qilmaslik",
                    "Faqat AI yozgan matnni nusxalash",
                ], 0),
                mcq("\"Summarization\" nima?", [
                    "Uzun matnni qisqartirish", "Matnni tarjima qilish",
                    "Matnni o'chirish", "Matnni chop etish",
                ], 0),
                mcq("AI bilan tadqiqot qilganda muhim faktlarni nima qilish kerak?", [
                    "Boshqa ishonchli manbadan tekshirish", "Har doim so'zma-so'z ishonish",
                    "Umuman tekshirmaslik", "Faqat bitta AI'dan so'rab qo'ya qolish",
                ], 0),
                mcq("Nega AI matnini o'zgartirmasdan ishlatish muammoli bo'lishi mumkin?", [
                    "Sifat va halollik nuqtai nazaridan muammoli bo'lishi mumkin",
                    "Chunki bu texnik jihatdan imkonsiz",
                    "Chunki AI hech qachon matn yoza olmaydi",
                    "Chunki bu juda qimmat",
                ], 0),
                mcq("AI tadqiqotda qanday rol o'ynaydi?", [
                    "Boshlang'ich nuqta, yakuniy ishonchli manba emas",
                    "Yagona va yetarli manba",
                    "Hech qanday foyda bermaydi",
                    "Faqat rasm chizish uchun",
                ], 0),
                mcq("Uzun hujjatni qisqartirishni so'raganda nimani aniq aytish foydali?", [
                    "Necha fikr yoki paragraf kerakligini va kim uchun ekanini",
                    "Faqat \"qisqartir\" deb yozish yetarli",
                    "Hech narsa aytish shart emas",
                    "Faqat inglizcha yozish kerak",
                ], 0),
            ],
        },
    ],
})

# ============================================================
# BO'LIM 3: AI YORDAMIDA DASTURLASH
# ============================================================
sections.append({
    'key': 's3', 'title': "3-BO'LIM. AI yordamida dasturlash",
    'topics': [
        {
            'key': 't3a', 'title': "Dasturlashga kirish va AI yordamchi vositalar", 'start_page': 7, 'end_page': 7,
            'explanation': {
                'goals': [
                    "Dasturlash nima ekanini oddiy tilda tushunish",
                    "AI yordamchi kod vositalarini (Claude Code, Cursor, Copilot) bilish",
                    "AI yordamida dasturlashni boshlashning to'g'ri yo'lini aniqlash",
                ],
                'blocks': [
                    block(
                        "Dasturlash - bu kompyuterga vazifa berish",
                        "**Dasturlash** - kompyuterga aniq, qadam-baqadam ko'rsatmalar (kod) yozib, unga "
                        "biror vazifani bajartirish. Masalan, veb-sahifa yaratish, hisob-kitob qilish, "
                        "ma'lumotlarni saralash. Kod - bu inson va kompyuter orasidagi \"til\".\n\n"
                        "Ilgari dasturlashni o'rganish uchun yillar kerak bo'lgan, ammo endi ==AI "
                        "yordamchilar tufayli oddiy odam ham (chuqur texnik bilimsiz) kichik dasturlar "
                        "yarata oladi== - bu haqiqiy inqilob va shu sababli bu bo'lim alohida muhim.",
                    ),
                    block(
                        "AI yordamchi kod vositalari",
                        "Bugungi kunda dasturchilar (va endilikda oddiy foydalanuvchilar ham) quyidagi "
                        "AI vositalaridan foydalanadi:\n\n"
                        "- **Claude Code** (Anthropic) - terminalda ishlaydigan, butun loyihalarni "
                        "tushunib, kod yozadigan, testlaydigan AI yordamchi\n"
                        "- **Cursor** - kod muharriri (editor) bo'lib, ichiga AI o'rnatilgan\n"
                        "- **GitHub Copilot** - kod yozayotganda avtomatik taklif beradigan yordamchi\n"
                        "- **ChatGPT/Claude/Gemini** (veb-versiya) - kod parchalarini yozib berish, "
                        "tushuntirish uchun\n\n"
                        "Bu vositalarning barchasi bir xil g'oyaga asoslanadi: siz **nima kerakligini "
                        "so'zlar bilan tasvirlaysiz**, AI esa kodni yozadi.",
                    ),
                    block(
                        "To'g'ri boshlash yo'li",
                        "AI yordamida dasturlashni boshlashda ko'p odamlar xato qiladigan narsa - "
                        "==to'g'ridan-to'g'ri murakkab loyihaga urinish==. To'g'ri yondashuv:\n\n"
                        "1. **Kichikdan boshlang**: \"Salom dunyo\" chiqaradigan oddiy dastur\n"
                        "2. **Nima ekanini tushunishga harakat qiling**: AI yozgan kodni o'qing, "
                        "\"nega bu qator kerak?\" deb so'rang\n"
                        "3. **O'zgartirib ko'ring**: kodning bir qismini o'zingiz o'zgartirib, natijani "
                        "kuzating\n"
                        "4. **Asta-sekin murakkablashtiring**: har safar bitta yangi narsa qo'shing\n\n"
                        "Maqsad - AI'ga \"faqat buyruq berish\" emas, balki **birga ishlab, nima "
                        "sodir bo'layotganini tushunish**. Shunda siz haqiqatan dasturlashni o'rganasiz, "
                        "shunchaki AI'ga qaram bo'lib qolmaysiz.",
                    ),
                ],
                'key_facts': [
                    fact("Dasturlash - kompyuterga aniq ko'rsatmalar (kod) berish jarayoni."),
                    fact("Claude Code, Cursor, GitHub Copilot - mashhur AI kod yordamchilari."),
                    fact("To'g'ri yo'l: kichikdan boshlash, kodni tushunishga harakat qilish, asta-sekin murakkablashtirish."),
                ],
                'summary': "AI yordamchilar dasturlashni ==ancha osonlashtirdi==, lekin eng yaxshi natija "
                           "faqat buyruq berish emas, **birga ishlab tushunishdan** kelib chiqadi.",
            },
            'test': [
                mcq("Dasturlash nima?", [
                    "Kompyuterga aniq ko'rsatmalar (kod) berish", "Faqat internetdan foydalanish",
                    "Video o'yin o'ynash", "Kompyuterni yig'ish",
                ], 0),
                mcq("Quyidagilardan qaysi biri AI kod yordamchisi EMAS?", [
                    "Microsoft Word", "Claude Code", "Cursor", "GitHub Copilot",
                ], 0),
                mcq("AI yordamida dasturlashni boshlashda to'g'ri yondashuv qanday?", [
                    "Kichikdan boshlab, asta-sekin murakkablashtirish",
                    "To'g'ridan-to'g'ri murakkab loyihaga urinish",
                    "Kodni umuman o'qimaslik",
                    "Faqat AI'ga ishonib, hech narsani tushunmaslik",
                ], 0),
                mcq("Nega AI yozgan kodni tushunishga harakat qilish muhim?", [
                    "Shunda haqiqatan dasturlashni o'rganasiz, AI'ga qaram bo'lib qolmaysiz",
                    "Chunki AI hech qachon to'g'ri kod yozmaydi",
                    "Bu majburiy qonun talabi",
                    "Aks holda kompyuter ishlamay qoladi",
                ], 0),
                mcq("Kod nima uchun kerak?", [
                    "Inson va kompyuter orasidagi \"til\" sifatida, vazifa berish uchun",
                    "Faqat o'yin o'ynash uchun", "Faqat rasm chizish uchun",
                    "Internetni tezlashtirish uchun",
                ], 0),
                fill_blank("Terminalda ishlaydigan, butun loyihani tushunib kod yozadigan Anthropic'ning AI yordamchisi nima deb ataladi? (2 so'z: \"Claude ...\")", "Claude Code"),
            ],
        },
        {
            'key': 't3b', 'title': "AI bilan birinchi loyihani yaratish", 'start_page': 8, 'end_page': 8,
            'explanation': {
                'goals': [
                    "AI yordamida oddiy veb-sahifa yaratish jarayonini bilish",
                    "Vazifani AI'ga qanday to'g'ri tushuntirishni o'rganish",
                    "Natijani tekshirish va takomillashtirish jarayonini tushunish",
                ],
                'blocks': [
                    block(
                        "Loyihani rejalashtirish",
                        "Har qanday loyihani boshlashdan oldin, ==nima yaratmoqchi ekaningizni aniq "
                        "tasavvur qiling==. Masalan: \"Shaxsiy vizit-karta sahifasi yaratmoqchiman: "
                        "ism-familiyam, kasbim, ijtimoiy tarmoq havolalarim ko'rinsin.\"\n\n"
                        "Bu tasavvurni AI'ga aynan shunday, aniq tasvirlab bering - qanchalik aniq "
                        "bo'lsa, natija shunchalik kutganingizga yaqin chiqadi (2-bo'limda o'rgangan "
                        "prompt yozish qoidalarini shu yerda qo'llaysiz).",
                    ),
                    block(
                        "Qadam-baqadam jarayon",
                        "1. **So'rov yozing**: \"HTML va CSS yordamida oddiy vizit-karta sahifa yarat: "
                        "ism, kasb, 3 ta ijtimoiy tarmoq havolasi bo'lsin, rangi ko'k-oq\"\n"
                        "2. **Natijani ko'ring**: AI kod yozadi (yoki, Claude Code kabi vositada, "
                        "to'g'ridan-to'g'ri faylni yaratadi)\n"
                        "3. **Sinab ko'ring**: sahifani brauzerda oching, qanday ko'rinishini tekshiring\n"
                        "4. **O'zgartirish so'rang**: \"Fon rangini och ko'kka o'zgartir\", \"Shriftni "
                        "kattaroq qil\" kabi aniq so'rovlar bilan yaxshilang\n\n"
                        "Bu **\"iteratsiya\" (takrorlash)** jarayoni - birinchi urinishda mukammal "
                        "chiqishi shart emas, ==asta-sekin yaxshilab borish== normal holat.",
                    ),
                    block(
                        "Xatolarga tayyor bo'ling",
                        "Birinchi urinishda hammasi ishlamasligi mumkin - bu **normal**. Muhimi, "
                        "xatoni ko'rib, AI'ga aniq tasvirlab berish: \"Tugma bosilganda hech narsa "
                        "bo'lmayapti\" yoki \"Rasm ko'rinmayapti\". Bu haqida keyingi mavzuda "
                        "(debugging) batafsil gaplashamiz.\n\n"
                        "**Eslatma**: kichik loyihalar bilan boshlab, muvaffaqiyatni his qilish - "
                        "motivatsiyani saqlashning eng yaxshi usuli. Bitta ishlaydigan sahifa yaratish "
                        "= katta yutuq!",
                    ),
                ],
                'key_facts': [
                    fact("Loyihani boshlashdan oldin nima yaratmoqchi ekaningizni aniq tasavvur qilish kerak."),
                    fact("Iteratsiya - natijani ko'rib, asta-sekin yaxshilab borish jarayoni."),
                    fact("Birinchi urinishda xato chiqishi normal holat."),
                ],
                'summary': "Loyiha yaratish = **aniq so'rov** + **natijani tekshirish** + **asta-sekin "
                           "yaxshilash (iteratsiya)**. Xato chiqishi normal - bu jarayonning bir qismi.",
            },
            'test': [
                mcq("Loyihani boshlashdan oldin nima qilish kerak?", [
                    "Nima yaratmoqchi ekaningizni aniq tasavvur qilish",
                    "Darhol kod yozishni boshlash", "Hech narsa rejalashtirmaslik",
                    "Faqat AI'ga \"ajoyib narsa yarat\" deyish",
                ], 0),
                mcq("\"Iteratsiya\" jarayoni nimani anglatadi?", [
                    "Natijani ko'rib, asta-sekin yaxshilab borish", "Loyihani butunlay o'chirish",
                    "Faqat bir marta urinib ko'rish", "Kodni hech qachon o'zgartirmaslik",
                ], 0),
                mcq("Birinchi urinishda loyiha to'liq ishlamasa, nima qilish kerak?", [
                    "Xatoni aniq tasvirlab, AI'dan yordam so'rash", "Loyihani butunlay tashlab yuborish",
                    "Hech narsa qilmaslik", "AI'ni ayblash",
                ], 0),
                mcq("Nega kichik loyihalar bilan boshlash tavsiya etiladi?", [
                    "Muvaffaqiyatni his qilib, motivatsiyani saqlash uchun",
                    "Chunki katta loyiha texnik jihatdan imkonsiz",
                    "Chunki AI faqat kichik loyihalarni tushunadi",
                    "Bu majburiy qoida",
                ], 0),
                mcq("AI'ga so'rov yozganda qanday bo'lishi kerak?", [
                    "Iloji boricha aniq va tasvirlangan", "Iloji boricha noaniq",
                    "Faqat bitta so'zdan iborat", "Faqat ingliz tilida",
                ], 0),
            ],
        },
        {
            'key': 't3c', 'title': "AI bilan xatolarni topish va tuzatish", 'start_page': 9, 'end_page': 9,
            'explanation': {
                'goals': [
                    "\"Debugging\" (xato tuzatish) tushunchasini bilish",
                    "Xatoni AI'ga qanday tasvirlab berishni o'rganish",
                    "Xato xabarlari (error message)ni o'qishni tushunish",
                ],
                'blocks': [
                    block(
                        "Debugging nima?",
                        "**Debugging (xato tuzatish)** - dasturdagi xatoni topib, tuzatish jarayoni. "
                        "\"Bug\" (nasoz/xato) atamasi 1940-yillarda haqiqiy kapalak kompyuter ichiga "
                        "kirib, nosozlik keltirib chiqarganidan kelib chiqqan degan mashhur rivoyat bor.\n\n"
                        "Dasturlashning katta qismi aslida ==kod yozishdan ko'ra, nima uchun ishlamayotganini "
                        "aniqlashdan iborat== - hatto tajribali dasturchilar ham doim xato bilan ishlaydi. "
                        "Bu normal va kutilgan jarayon.",
                    ),
                    block(
                        "Xatoni AI'ga qanday tasvirlash kerak",
                        "Xato haqida AI'dan yordam so'raganda, quyidagilarni albatta kiriting:\n\n"
                        "1. **Nima qilmoqchi edingiz** - \"Tugmani bossam, forma yuborilishi kerak edi\"\n"
                        "2. **Nima sodir bo'ldi** - \"Hech narsa bo'lmadi\" yoki \"Xato xabari chiqdi\"\n"
                        "3. **Xato xabarining o'zi** (agar bo'lsa) - to'liq matnini nusxalab bering\n"
                        "4. **Tegishli kod** - muammo bo'lgan qismni ko'rsating\n\n"
                        "==\"Ishlamayapti\" deyish yetarli emas== - bu xuddi shifokorga \"yomon his "
                        "qilyapman\" deyishga o'xshaydi. Qancha aniq tasvirlasangiz, AI shuncha tez va "
                        "to'g'ri yordam beradi.",
                    ),
                    block(
                        "Xato xabarlarini o'qishni o'rganish",
                        "Ko'p yangi boshlovchilar xato xabarini (error message) ko'rib qo'rqib ketadi va "
                        "o'qimasdan yopib qo'yadi. Aslida xato xabari odatda ==aynan qayerda va nima "
                        "sababdan muammo borligini aytib turadi==. Masalan: \"Line 12: undefined variable "
                        "'nom'\" - bu 12-qatorda \"nom\" degan o'zgaruvchi aniqlanmaganini bildiradi.\n\n"
                        "Maslahat: xato xabarini to'liq o'qing (yoki AI'ga to'liq nusxalab bering) - "
                        "yechim ko'pincha xabarning o'zida yashiringan bo'ladi.",
                    ),
                ],
                'key_facts': [
                    fact("Debugging - dasturdagi xatoni topib, tuzatish jarayoni."),
                    fact("Xatoni tasvirlashda: nima qilmoqchi edingiz, nima sodir bo'ldi, xato matni, tegishli kod."),
                    fact("Xato xabari odatda muammoning aniq joyi va sababini ko'rsatadi."),
                ],
                'summary': "Debugging - dasturlashning tabiiy qismi. Xatoni AI'ga ==aniq tasvirlab== "
                           "(nima kutilgan, nima bo'ldi, xato matni) bering - tezroq yechim topasiz.",
            },
            'test': [
                mcq("\"Debugging\" atamasi nimani anglatadi?", [
                    "Dasturdagi xatoni topib, tuzatish", "Yangi dastur yozish",
                    "Kompyuterni o'chirish", "Internetga ulanish",
                ], 0),
                mcq("Xato haqida AI'dan yordam so'raganda nimani albatta aytish kerak?", [
                    "Nima kutilgan edi, nima sodir bo'ldi va xato matnini",
                    "Faqat \"ishlamayapti\" deb yozish yetarli",
                    "Hech narsa aytmasdan kutish",
                    "Faqat kompyuter modelini aytish",
                ], 0),
                mcq("Xato xabari (error message) odatda nimani ko'rsatadi?", [
                    "Muammoning aniq joyi va sababini", "Hech qanday foydali ma'lumot bermaydi",
                    "Faqat internet holatini", "Kompyuter narxini",
                ], 0),
                mcq("Tajribali dasturchilar xato bilan qanday munosabatda bo'ladi?", [
                    "Bu normal jarayon deb qabul qiladi, doim xato bilan ishlaydi",
                    "Hech qachon xato qilmaydi", "Xato chiqsa darhol ishni tashlab yuboradi",
                    "Xatoni ko'rmaslikka harakat qiladi",
                ], 0),
                mcq("\"Ishlamayapti\" deb aytishning kamchiligi nima?", [
                    "Bu aniq emas, AI muammoni tushunmaydi",
                    "Bu juda uzun jumla", "Bu noto'g'ri grammatika",
                    "Bu AI'ni xafa qiladi",
                ], 0),
                fill_blank("Dasturdagi xatoni topib tuzatish jarayoni inglizcha qanday ataladi?", "debugging"),
            ],
        },
    ],
})

# ============================================================
# BO'LIM 4: AI AGENTLAR VA AVTOMATLASHTIRISH
# ============================================================
sections.append({
    'key': 's4', 'title': "4-BO'LIM. AI agentlar va avtomatlashtirish",
    'topics': [
        {
            'key': 't4a', 'title': "AI agent nima va qanday ishlaydi", 'start_page': 10, 'end_page': 10,
            'explanation': {
                'goals': [
                    "\"AI agent\" tushunchasini oddiy chatbotdan farqlab tushunish",
                    "Agentning \"vosita (tool) ishlatish\" qobiliyatini bilish",
                    "Agentlar qayerda ishlatilishini aniqlash",
                ],
                'blocks': [
                    block(
                        "Oddiy chatbot va AI agent farqi",
                        "Oddiy chatbot faqat **savolga javob beradi** - matn kiritasiz, matn olasiz. "
                        "**AI agent** esa bundan ancha ilg'or: u ==vazifani bajarish uchun harakatlar "
                        "ketma-ketligini o'zi rejalashtiradi va \"vositalar\" (tools)dan foydalanadi==.\n\n"
                        "Masalan, \"Toshkentdagi ob-havoni ayt\" so'rovida:\n"
                        "- Oddiy chatbot: o'qitilgan ma'lumotidan taxminiy javob beradi (yangilanmagan bo'lishi mumkin)\n"
                        "- AI agent: internetga chiqib, ob-havo saytidan **haqiqiy, joriy ma'lumotni** oladi, "
                        "so'ng javob shakllantiradi",
                    ),
                    block(
                        "Agent qanday ishlaydi: fikrlash-harakat aylanishi",
                        "AI agent odatda quyidagi tsiklda ishlaydi (**\"think-act-observe\"**):\n\n"
                        "1. **O'ylaydi** - vazifani bajarish uchun nima qilish kerakligini rejalashtiradi\n"
                        "2. **Harakat qiladi** - tegishli vositadan foydalanadi (internet qidiruv, "
                        "fayl o'qish, kod ishga tushirish, kalkulyator)\n"
                        "3. **Natijani ko'radi** - vosita natijasini tahlil qiladi\n"
                        "4. **Takrorlaydi** - kerak bo'lsa, yana boshqa harakat qiladi, toki vazifa "
                        "bajarilguncha\n\n"
                        "Aynan shu Claude Code kabi vositalarning ==fayllarni o'qib, kod yozib, uni "
                        "ishga tushirib, xatoni ko'rib, tuzatib== - hammasini avtomatik qilishining sababi.",
                    ),
                    block(
                        "Agentlar qayerda ishlatiladi",
                        "- **Dasturlash yordamchilari**: Claude Code - loyihani tushunib, kod yozib, "
                        "test qilib beradi\n"
                        "- **Mijozlarga xizmat**: ko'p kompaniyalar AI agentlarni buyurtma holatini "
                        "tekshirish, qaytarish jarayonini boshqarish uchun ishlatadi\n"
                        "- **Tadqiqot yordamchilari**: bir nechta internet manbani o'qib, xulosa chiqaradi\n"
                        "- **Shaxsiy yordamchilar**: uchrashuv rejalashtirish, email yozish kabi vazifalarni "
                        "avtomatlashtirish\n\n"
                        "Kelgusi yillarda AI agentlar yanada ko'proq **murakkab, ko'p bosqichli ish "
                        "jarayonlarini** o'z zimmasiga oladi deb kutilmoqda.",
                    ),
                ],
                'key_facts': [
                    fact("AI agent - vazifani bajarish uchun vositalardan (tools) foydalanib, harakatlar rejalashtiradi."),
                    fact("Agent tsikli: o'ylash -> harakat qilish -> natijani ko'rish -> takrorlash."),
                    fact("Claude Code - dasturlash uchun AI agentga misol."),
                ],
                'summary': "AI agent = oddiy chatbot + **vosita ishlatish qobiliyati** + **rejalashtirish**. "
                           "U vazifani bosqichma-bosqich, natijani tekshirib borib bajaradi.",
            },
            'test': [
                mcq("AI agentni oddiy chatbotdan farqlaydigan asosiy xususiyat nima?", [
                    "Vositalar (tools)dan foydalanib, harakatlarni o'zi rejalashtirishi",
                    "Faqat tezroq javob berishi", "Faqat ingliz tilida ishlashi", "Hech qanday farq yo'q",
                ], 0),
                mcq("Agentning \"think-act-observe\" tsiklida nima keladi?", [
                    "O'ylash, harakat qilish, natijani ko'rish, takrorlash",
                    "Faqat harakat qilish", "Faqat kutish", "Faqat o'chirish",
                ], 0),
                mcq("Claude Code qaysi turdagi AI vositasiga misol?", [
                    "AI agent (dasturlash uchun)", "Oddiy kalkulyator",
                    "Faqat rasm ko'ruvchi dastur", "Video pleer",
                ], 0),
                mcq("Ob-havo haqida so'ralganda, AI agent oddiy chatbotdan farqli qanday harakat qiladi?", [
                    "Internetga chiqib, haqiqiy joriy ma'lumotni oladi",
                    "Hech narsa qilmaydi", "Faqat taxmin qiladi",
                    "Foydalanuvchiga savol bilan javob qaytaradi",
                ], 0),
                mcq("Quyidagilardan qaysi biri AI agent ishlatilishiga misol EMAS?", [
                    "Oddiy statik veb-sahifa", "Mijozlarga xizmat ko'rsatish boti",
                    "Dasturlash yordamchisi", "Tadqiqot yordamchisi",
                ], 0),
            ],
        },
        {
            'key': 't4b', 'title': "No-code avtomatlashtirish vositalari", 'start_page': 11, 'end_page': 11,
            'explanation': {
                'goals': [
                    "\"No-code/low-code\" tushunchasini bilish",
                    "Mashhur avtomatlashtirish vositalarini (Zapier, Make) tanishtirish",
                    "Oddiy avtomatlashtirish stsenariysini tushunish",
                ],
                'blocks': [
                    block(
                        "No-code nima?",
                        "**No-code (kodsiz)** vositalar - dasturlash bilmasdan, ==tugmalarni bosib va "
                        "bloklarni ulab avtomatlashtirish yaratish imkonini beradigan== platformalar. "
                        "\"Agar X sodir bo'lsa, Y qil\" mantig'iga asoslangan.\n\n"
                        "Masalan: \"Agar menga yangi email kelsa VA u mijozdan bo'lsa, avtomatik ravishda "
                        "Google Sheets jadvaliga qo'sh\" - buni kod yozmasdan, faqat sozlash orqali "
                        "amalga oshirish mumkin.",
                    ),
                    block(
                        "Mashhur vositalar",
                        "- **Zapier** - eng mashhur avtomatlashtirish platformasi, 5000+ ilova bilan "
                        "ishlaydi (Gmail, Google Sheets, Telegram, Instagram va h.k.)\n"
                        "- **Make (avvalgi Integromat)** - Zapier'ga o'xshash, vizual sxema ko'rinishida\n"
                        "- **n8n** - bepul, o'zingiz serverga o'rnatishingiz mumkin bo'lgan variant\n\n"
                        "Bu platformalarning aksariyati endi ==AI blokларini ham qo'shgan== - masalan, "
                        "\"kelgan xabarni AI orqali tahlil qilib, tilini aniqla, keyin tegishli tilda "
                        "javob yubor\" kabi zanjirlar yaratish mumkin.",
                    ),
                    block(
                        "Amaliy misol: oddiy avtomatlashtirish",
                        "Kichik biznes egasi uchun foydali stsenariy:\n\n"
                        "1. **Trigger (qo'zg'atuvchi)**: Instagram'da yangi \"direct message\" keladi\n"
                        "2. **AI qadam**: xabar matnini AI orqali tahlil qiladi - \"bu narx haqida "
                        "so'rovmi?\"\n"
                        "3. **Harakat**: agar ha bo'lsa, avtomatik narxlar ro'yxatini yuboradi; aks "
                        "holda, insonga (sizga) bildirishnoma yuboradi\n\n"
                        "Bu tarzda ==kichik biznes soatlab qo'lda javob berish o'rniga==, asosiy "
                        "so'rovlarni avtomatlashtirib, faqat murakkab holatlarga vaqt sarflaydi.",
                    ),
                ],
                'key_facts': [
                    fact("No-code - dasturlashsiz, tugma va bloklar orqali avtomatlashtirish yaratish."),
                    fact("Zapier, Make, n8n - mashhur no-code avtomatlashtirish platformalari."),
                    fact("Zamonaviy platformalar AI bloklarini ham qo'llab-quvvatlaydi."),
                ],
                'summary': "No-code vositalar (**Zapier, Make**) yordamida dasturlash bilmasdan ham "
                           "==\"agar X bo'lsa, Y qil\"== mantig'idagi avtomatlashtirish yaratish mumkin.",
            },
            'test': [
                mcq("\"No-code\" atamasi nimani anglatadi?", [
                    "Dasturlashsiz, tugma/bloklar orqali avtomatlashtirish yaratish",
                    "Faqat professional dasturchilar uchun vosita",
                    "Kompyutersiz ishlaydigan dastur",
                    "Internetsiz ishlaydigan dastur",
                ], 0),
                mcq("Quyidagilardan qaysi biri no-code avtomatlashtirish platformasi?", [
                    "Zapier", "Microsoft Excel", "Google Chrome", "WhatsApp",
                ], 0),
                mcq("No-code platformalarning asosiy mantig'i qanday?", [
                    "\"Agar X sodir bo'lsa, Y qil\"", "\"Har doim hech narsa qilma\"",
                    "\"Faqat bir marta ishla\"", "\"Faqat kechqurun ishla\"",
                ], 0),
                mcq("Zamonaviy no-code platformalar yana nimani qo'shgan?", [
                    "AI bloklarini (matnni tahlil qilish, javob yaratish)",
                    "Faqat rasm chizish funksiyasini",
                    "Faqat video montaj funksiyasini",
                    "Hech narsa qo'shmagan",
                ], 0),
                mcq("Kichik biznes uchun avtomatlashtirishning foydasi nima?", [
                    "Oddiy so'rovlarga avtomatik javob berib, vaqtni tejash",
                    "Barcha mijozlarni yo'qotish", "Internetni sekinlashtirish",
                    "Hech qanday foyda yo'q",
                ], 0),
            ],
        },
        {
            'key': 't4c', 'title': "Oddiy chatbot yaratish", 'start_page': 12, 'end_page': 12,
            'explanation': {
                'goals': [
                    "Chatbot yaratishning asosiy tamoyillarini tushunish",
                    "\"System prompt\" (tizim ko'rsatmasi) tushunchasini bilish",
                    "Oddiy chatbot loyihasini rejalashtirish",
                ],
                'blocks': [
                    block(
                        "Chatbot qanday quriladi?",
                        "Zamonaviy chatbot yaratish uchun kompleks kod yozish shart emas - asosiy "
                        "g'oya: LLM (masalan Claude yoki GPT) API'siga ulanib, unga ==maxsus \"tizim "
                        "ko'rsatmasi\" (system prompt) berish==. Bu ko'rsatma botning \"shaxsiyati\" va "
                        "vazifasini belgilaydi.\n\n"
                        "Masalan: \"Sen 'TechDo'kon' onlayn do'konining yordamchisisan. Faqat mahsulot, "
                        "yetkazib berish va qaytarish haqida savollarga javob ber. Boshqa mavzularda "
                        "'Kechirasiz, men faqat do'kon savollariga yordam bera olaman' deb javob ber.\"",
                    ),
                    block(
                        "System prompt yozish tamoyillari",
                        "Yaxshi system prompt quyidagilarni o'z ichiga oladi:\n\n"
                        "1. **Rol** - bot kim: \"Sen ... yordamchisisan\"\n"
                        "2. **Vazifa chegarasi** - nima haqida javob berishi, nima haqida bermasligi kerak\n"
                        "3. **Ohang/uslub** - rasmiy, do'stona, qisqa yoki batafsil\n"
                        "4. **Maxsus qoidalar** - masalan, \"narxlarni hech qachon o'zgartirma\", \"agar "
                        "bilmasang, insonga murojaat qilishni tavsiya qil\"\n\n"
                        "Bu aynan 2-bo'limda o'rgangan **prompt yozish qoidalari**ning maxsus holati - "
                        "farqi shundaki, bu ko'rsatma ==har bir suhbatda doimiy qo'llaniladi==.",
                    ),
                    block(
                        "Chatbot loyihasini rejalashtirish",
                        "O'z chatbotingizni yaratishni boshlash uchun:\n\n"
                        "1. **Maqsadni aniqlang**: chatbot nima uchun kerak? (mijozlarga yordam, "
                        "ta'lim, o'yin-kulgi)\n"
                        "2. **Bilim chegarasini belgilang**: bot qanday savollarga javob berishi kerak\n"
                        "3. **System prompt yozing**: yuqoridagi tamoyillar asosida\n"
                        "4. **Sinab ko'ring**: turli savollar bering, botning \"chegaradan chiqib\" "
                        "ketmasligini tekshiring\n"
                        "5. **Yaxshilang**: kamchiliklarni ko'rib, system promptni to'g'rilang\n\n"
                        "Bu ko'nikma - keyingi bo'limda ko'radigan **\"AI bilan pul topish\"** "
                        "imkoniyatlarining asosiy vositalaridan biri, chunki ko'plab kichik "
                        "bizneslarga shunday chatbotlar kerak.",
                    ),
                ],
                'key_facts': [
                    fact("System prompt - chatbotning \"shaxsiyati\" va vazifa chegarasini belgilaydigan ko'rsatma."),
                    fact("Yaxshi system prompt: rol, vazifa chegarasi, ohang, maxsus qoidalarni o'z ichiga oladi."),
                    fact("Chatbot yaratish: maqsad, bilim chegarasi, system prompt, sinov, yaxshilash bosqichlari."),
                ],
                'summary': "Chatbot = LLM + **system prompt** (rol + chegara + ohang + qoidalar). "
                           "Buni yaxshi yozish - foydali va xavfsiz botning kaliti.",
            },
            'test': [
                mcq("\"System prompt\" nima?", [
                    "Botning shaxsiyati va vazifasini belgilaydigan doimiy ko'rsatma",
                    "Foydalanuvchi yozadigan har bir xabar",
                    "Kompyuter operatsion tizimi",
                    "Internet provayderi",
                ], 0),
                mcq("Yaxshi system prompt nimalarni o'z ichiga olishi kerak?", [
                    "Rol, vazifa chegarasi, ohang, maxsus qoidalar",
                    "Faqat botning nomi", "Faqat rang sxemasi", "Faqat narx",
                ], 0),
                mcq("System prompt oddiy prompt'dan nimasi bilan farq qiladi?", [
                    "Har bir suhbatda doimiy qo'llaniladi",
                    "Faqat bir marta ishlatiladi va yo'qoladi",
                    "Hech qanday farqi yo'q",
                    "Faqat rasm uchun ishlatiladi",
                ], 0),
                mcq("Chatbot loyihasini rejalashtirishning birinchi qadami nima?", [
                    "Maqsadni aniqlash - chatbot nima uchun kerak",
                    "Darhol kod yozishni boshlash", "Narxni belgilash",
                    "Reklama qilish",
                ], 0),
                mcq("Nega botga \"bilmasang, insonga murojaat qil\" qoidasini qo'shish foydali?", [
                    "Bot bilmagan narsani to'qib chiqarmasligi (hallucination) uchun",
                    "Botni sekinlashtirish uchun", "Botni qimmatlashtirish uchun",
                    "Hech qanday foyda yo'q",
                ], 0),
            ],
        },
    ],
})

# ============================================================
# BO'LIM 5: AI BILAN PUL TOPISH
# ============================================================
sections.append({
    'key': 's5', 'title': "5-BO'LIM. AI bilan pul topish",
    'topics': [
        {
            'key': 't5a', 'title': "Frilanser sifatida AI xizmatlari ko'rsatish", 'start_page': 13, 'end_page': 13,
            'explanation': {
                'goals': [
                    "AI ko'nikmalari orqali frilanser sifatida ishlashning yo'llarini bilish",
                    "Qaysi xizmatlarga talab borligini aniqlash",
                    "Portfolio va birinchi mijozni topish strategiyasini tushunish",
                ],
                'blocks': [
                    block(
                        "AI ko'nikmalari - talab yuqori bozor",
                        "Bugungi kunda ko'plab kompaniya va shaxslar AI'dan foydalanishni xohlaydi, "
                        "lekin ==buni qanday to'g'ri qilishni bilishmaydi==. Bu sizga katta imkoniyat "
                        "yaratadi - siz bu bo'limda o'rgangan bilimlar (prompt yozish, chatbot yaratish, "
                        "avtomatlashtirish) allaqachon ko'plab odamlardan ustunroq.\n\n"
                        "Frilanser platformalarida (Upwork, Fiverr, mahalliy bozorlarda Telegram "
                        "guruhlari orqali ham) AI bilan bog'liq xizmatlarga talab tobora oshib bormoqda.",
                    ),
                    block(
                        "Qanday xizmatlar taklif qilish mumkin",
                        "- **Chatbot yaratish**: kichik bizneslar uchun mijozlarga xizmat ko'rsatuvchi bot\n"
                        "- **Avtomatlashtirish sozlash**: Zapier/Make orqali ish jarayonlarini avtomatlashtirish\n"
                        "- **Kontent yaratishda yordam**: AI yordamida ijtimoiy tarmoq postlari, "
                        "reklama matnlari yozish\n"
                        "- **Prompt yozish maslahati**: kompaniyalarga o'z ichki AI vositalarini "
                        "samarali ishlatishni o'rgatish\n"
                        "- **AI yordamida kichik veb-sahifa/dastur yaratish**: 3-bo'limda o'rgangan "
                        "ko'nikmalar asosida\n\n"
                        "Boshlash uchun ==katta mijozlar emas, kichik, oddiy vazifalar bilan boshlang== - "
                        "tajriba va sharhlar (review) to'plash birinchi qadam.",
                    ),
                    block(
                        "Portfolio va birinchi mijozni topish",
                        "Hech qanday tajribangiz bo'lmasa ham boshlash mumkin:\n\n"
                        "1. **O'zingiz uchun 2-3 ta намуна loyiha yarating** (masalan, o'zingiz uchun "
                        "chatbot, do'stingiz biznesiga oddiy avtomatlashtirish) - bu portfolio bo'ladi\n"
                        "2. **Ijtimoiy tarmoqlarda ko'rsating**: qanday muammoni yechganingizni tushuntirib, "
                        "natijani ulashing\n"
                        "3. **Arzon yoki bepul birinchi loyiha taklif qiling**: sharh olish uchun\n"
                        "4. **Sharhlar asosida narxni oshirib boring**: tajriba oshgani sari o'z "
                        "narxingizni oqilona oshiring\n\n"
                        "**Muhim**: mijozga va'da berganingizda ==real, tekshirilgan natijalar== "
                        "va'da bering - AI'ning cheklovlarini (hallucination, xato ehtimoli) mijozga "
                        "ham tushuntiring, bu ishonchni oshiradi.",
                    ),
                ],
                'key_facts': [
                    fact("AI ko'nikmalariga bo'lgan talab tobora oshib bormoqda."),
                    fact("Boshlash uchun kichik, oddiy vazifalar va o'z-portfolio loyihalari foydali."),
                    fact("Mijozga real natijalar va'da berish, AI cheklovlarini tushuntirish ishonch yaratadi."),
                ],
                'summary': "AI ko'nikmalari orqali frilanser sifatida ishlash uchun: **kichik boshlang, "
                           "portfolio yig'ing, halol bo'ling** - talab yuqori, imkoniyat katta.",
            },
            'test': [
                mcq("Nega AI ko'nikmalari bilan frilanser ishlash imkoniyati katta?", [
                    "Talab yuqori, lekin ko'p odam AI'dan to'g'ri foydalanishni bilmaydi",
                    "Chunki hech kimga AI kerak emas", "Chunki bu qonun bilan taqiqlangan",
                    "Chunki AI mavjud emas",
                ], 0),
                mcq("Tajribasiz odam qanday boshlashi mumkin?", [
                    "O'zi uchun namuna loyihalar yaratib, portfolio to'plash",
                    "Darhol eng qimmat xizmatni taklif qilish",
                    "Hech qachon boshlamaslik",
                    "Faqat katta kompaniyalarga murojaat qilish",
                ], 0),
                mcq("Quyidagilardan qaysi biri AI bilan bog'liq frilanser xizmatiga misol?", [
                    "Kichik biznes uchun chatbot yaratish", "Faqat futbol o'ynash",
                    "Faqat kitob o'qish", "Faqat uxlash",
                ], 0),
                mcq("Mijozga nima haqida halol bo'lish tavsiya etiladi?", [
                    "AI'ning cheklovlari (xato ehtimoli) haqida",
                    "Narxni doim yashirish haqida",
                    "Hech qachon natija ko'rsatmaslik haqida",
                    "Faqat o'zining shaxsiy hayoti haqida",
                ], 0),
                mcq("Tajriba oshgani sari narx bilan nima qilish tavsiya etiladi?", [
                    "Oqilona oshirib borish", "Har doim bepul qilib qoldirish",
                    "Darhol juda qimmat qilish", "Narxni hech qachon o'zgartirmaslik",
                ], 0),
            ],
        },
        {
            'key': 't5b', 'title': "AI yordamida kontent biznesi", 'start_page': 14, 'end_page': 14,
            'explanation': {
                'goals': [
                    "AI yordamida kontent yaratish orqali daromad olish yo'llarini bilish",
                    "Kontent sifatini saqlash muhimligini tushunish",
                    "Turli platformalar uchun kontent strategiyasini aniqlash",
                ],
                'blocks': [
                    block(
                        "Kontent yaratish - AI bilan tezlashadi",
                        "AI yordamida kontent yaratish (blog maqolalari, ijtimoiy tarmoq postlari, "
                        "video skriptlari) ==vaqtni sezilarli qisqartiradi==, lekin bu \"AI hammasini "
                        "qiladi, men hech narsa qilmayman\" degani emas.\n\n"
                        "Eng samarali yondashuv: siz **g'oya va tajribangizni** qo'shasiz, AI esa "
                        "**tezlik va strukturani** ta'minlaydi. Masalan, siz kulinariya bo'yicha "
                        "tajribangiz bor - AI sizga retsept tavsiflarini tezroq yozishga, turli "
                        "tillarga tarjima qilishga yordam beradi.",
                    ),
                    block(
                        "Daromad manbalari",
                        "- **Blog/YouTube**: reklama daromadi, sponsorlik - AI kontent yozish/skript "
                        "tayyorlashda yordam beradi\n"
                        "- **Ijtimoiy tarmoq menejmenti**: kichik bizneslar uchun Instagram/Telegram "
                        "kontentini AI yordamida tezroq, ko'proq ishlab chiqarish\n"
                        "- **Elektron kitob/kurs yaratish**: bilimingizni AI yordamida tezroq "
                        "tuzilgan formatga keltirish\n"
                        "- **Tarjima xizmatlari**: AI yordamida tezroq, lekin **inson tomonidan "
                        "tekshirilgan** sifatli tarjima\n\n"
                        "==Barcha holatlarda muvaffaqiyat kaliti - AI tezligini o'z bilim/tajribangiz "
                        "bilan birlashtirish==, shunchaki AI matnini o'zgartirmasdan sotish emas.",
                    ),
                    block(
                        "Sifatni saqlash - uzoq muddatli muvaffaqiyat kaliti",
                        "Ko'p odamlar AI'dan foydalanib, tekshirmasdan, o'zgartirmasdan ko'p miqdorda "
                        "past sifatli kontent chiqaradi - bu qisqa muddatda ishlashi mumkin, lekin "
                        "==uzoq muddatda obro'ga zarar yetkazadi==. Auditoriya asta-sekin \"AI "
                        "kontenti\" va \"chin dildan yozilgan kontent\"ni farqlashni o'rganmoqda.\n\n"
                        "Shuning uchun: AI'dan **qoralama va tezlik** uchun foydalaning, lekin "
                        "yakuniy natijani **o'zingiz tekshiring, shaxsiylashtiring, haqiqiy fikringizni "
                        "qo'shing**. Bu sizni boshqa \"faqat AI'ga nusxa qo'ygan\" raqobatchilardan "
                        "ajratib turadi.",
                    ),
                ],
                'key_facts': [
                    fact("AI kontent yaratishda vaqtni tezlashtiradi, lekin g'oya va sifatni inson qo'shadi."),
                    fact("Daromad manbalari: blog/YouTube, ijtimoiy tarmoq menejmenti, kurs/kitob, tarjima."),
                    fact("Sifatsiz, tekshirilmagan AI-kontent uzoq muddatda obro'ga zarar yetkazadi."),
                ],
                'summary': "AI kontent biznesida **tezlik** beradi, siz esa **g'oya, tajriba va sifat "
                           "nazorati** qo'shasiz - ==ikkalasi birga== muvaffaqiyat keltiradi.",
            },
            'test': [
                mcq("AI kontent yaratishda eng samarali yondashuv qanday?", [
                    "O'z g'oya/tajribangizni AI tezligi bilan birlashtirish",
                    "AI yozganini hech qanday o'zgartirmasdan ishlatish",
                    "AI'dan umuman foydalanmaslik",
                    "Faqat AI'ga ishonib, o'zi hech narsa qilmaslik",
                ], 0),
                mcq("Nega tekshirilmagan, past sifatli AI-kontent xavfli?", [
                    "Uzoq muddatda obro'ga zarar yetkazishi mumkin",
                    "Chunki bu texnik jihatdan imkonsiz",
                    "Chunki bu juda qimmat", "Hech qanday xavfi yo'q",
                ], 0),
                mcq("Quyidagilardan qaysi biri AI yordamidagi kontent-daromad manbai EMAS?", [
                    "Kompyuterni jismonan ta'mirlash", "Blog/YouTube reklama daromadi",
                    "Elektron kitob/kurs sotish", "Ijtimoiy tarmoq menejmenti xizmati",
                ], 0),
                mcq("Yakuniy kontentni chop etishdan oldin nima qilish tavsiya etiladi?", [
                    "O'zingiz tekshirish va shaxsiylashtirish",
                    "Hech narsa qilmasdan darhol chop etish",
                    "Faqat boshqa AI'dan tekshirtirish",
                    "Uzoq vaqt kutish",
                ], 0),
                mcq("AI kontent biznesida sizni raqobatchilardan nima ajratib turadi?", [
                    "Haqiqiy fikr va sifat nazoratini qo'shishingiz",
                    "Faqat tezroq ishlashingiz",
                    "Faqat arzonroq narx qo'yishingiz",
                    "Hech narsa, hamma bir xil",
                ], 0),
            ],
        },
        {
            'key': 't5c', 'title': "AI asosidagi startap g'oyalari", 'start_page': 15, 'end_page': 15,
            'explanation': {
                'goals': [
                    "AI asosidagi mahsulot g'oyasini qanday topishni bilish",
                    "Kichik AI mahsulotini sinab ko'rish (MVP) tamoyilini tushunish",
                    "Real muammoni yechishning ahamiyatini anglash",
                ],
                'blocks': [
                    block(
                        "Yaxshi startap g'oyasi qayerdan keladi?",
                        "Eng yaxshi AI-startap g'oyalari odatda ==\"AI ajoyib, nimadir qilaman\" emas, "
                        "balki \"men (yoki atrofimdagilar) shu muammoni doim boshdan kechiramiz\" "
                        "degan kuzatishdan boshlanadi==.\n\n"
                        "Misol: agar siz kichik do'kon egasi bo'lib, har kuni mijozlarning bir xil "
                        "savollariga (\"ish vaqti qachon?\", \"yetkazib berish bormi?\") javob berishdan "
                        "charchagan bo'lsangiz - bu AI chatbot uchun aniq, real muammo.",
                    ),
                    block(
                        "MVP - Minimal ishlaydigan mahsulot",
                        "Startap boshlaganda ==darhol mukammal, katta mahsulot qurishga urinmang==. "
                        "**MVP (Minimum Viable Product)** - eng oddiy, faqat asosiy muammoni "
                        "yechadigan versiya yaratish tamoyili:\n\n"
                        "1. Bitta aniq muammoni tanlang\n"
                        "2. Eng oddiy yechimni yarating (masalan, oddiy chatbot, 3-4 bo'limdagi "
                        "vositalar bilan)\n"
                        "3. Haqiqiy foydalanuvchilarga bering, fikr-mulohaza (feedback) yig'ing\n"
                        "4. Fikr-mulohaza asosida yaxshilang\n\n"
                        "Bu yondashuv vaqt va pulni behuda sarflashning oldini oladi - avval "
                        "\"odamlarga bu kerakmi?\" ni tekshirib, keyin murakkablashtirasiz.",
                    ),
                    block(
                        "AI-startap g'oyalariga misollar",
                        "- Mahalliy tilda (o'zbek tilida) ishlaydigan mijozlar bilan muloqot boti\n"
                        "- Kichik ta'lim markazlari uchun avtomatik uy vazifasi tekshirish tizimi\n"
                        "- Fermerlar uchun AI orqali o'simlik kasalliklarini rasm bo'yicha aniqlash\n"
                        "- Kichik bizneslar uchun avtomatik hisobot va statistika tahlili\n\n"
                        "Muhim: ==bu g'oyalarning barchasi \"AI\" so'zidan emas, balki real, kundalik "
                        "muammodan boshlanadi== - texnologiya vosita, muammo esa boshlang'ich nuqta.",
                    ),
                ],
                'key_facts': [
                    fact("Yaxshi startap g'oyasi real, kuzatilgan muammodan boshlanadi."),
                    fact("MVP - eng oddiy, faqat asosiy muammoni yechadigan birinchi versiya."),
                    fact("Avval fikr-mulohaza yig'ish, keyin murakkablashtirish tavsiya etiladi."),
                ],
                'summary': "Yaxshi AI-startap = **real muammo** + **oddiy MVP** + **foydalanuvchi "
                           "fikr-mulohazasi**. ==Texnologiya emas, muammo boshlang'ich nuqta==.",
            },
            'test': [
                mcq("Eng yaxshi startap g'oyalari odatda qayerdan kelib chiqadi?", [
                    "Real, kuzatilgan muammodan", "Faqat \"AI zo'r\" degan fikrdan",
                    "Tasodifiy tanlovdan", "Boshqalarni taqlid qilishdan",
                ], 0),
                mcq("\"MVP\" nimani anglatadi?", [
                    "Minimal ishlaydigan mahsulot - eng oddiy birinchi versiya",
                    "Eng qimmat mahsulot", "Eng murakkab mahsulot",
                    "Mahsulotni sotib bo'lmasligi",
                ], 0),
                mcq("MVP yaratishning maqsadi nima?", [
                    "Vaqt va pulni behuda sarflamasdan, g'oyani tekshirish",
                    "Darhol mukammal mahsulot qurish",
                    "Hech qachon mahsulot chiqarmaslik",
                    "Faqat reklama qilish",
                ], 0),
                mcq("MVP dan keyingi qadam nima bo'lishi kerak?", [
                    "Foydalanuvchi fikr-mulohazasini yig'ib, yaxshilash",
                    "Darhol yopib qo'yish", "Hech narsa o'zgartirmaslik",
                    "Narxni oshirib, kutish",
                ], 0),
                mcq("AI-startap g'oyalarida texnologiya (AI) qanday rol o'ynaydi?", [
                    "Vosita - asosiy narsa hal qilinayotgan muammo",
                    "Yagona muhim narsa, muammo ahamiyatsiz",
                    "Hech qanday rol o'ynamaydi",
                    "Faqat marketing uchun kerak",
                ], 0),
            ],
        },
    ],
})

# ============================================================
# BO'LIM 6: AI XAVFSIZLIGI, ETIKASI VA KELAJAGI
# ============================================================
sections.append({
    'key': 's6', 'title': "6-BO'LIM. AI xavfsizligi, etikasi va kelajagi",
    'topics': [
        {
            'key': 't6a', 'title': "AI xatolarini tekshirish va ishonchli foydalanish", 'start_page': 16, 'end_page': 16,
            'explanation': {
                'goals': [
                    "Hallucinationni qanday aniqlash va oldini olishni chuqurroq o'rganish",
                    "AI javobini tekshirish usullarini bilish",
                    "Muhim qarorlarda AI'ga qanchalik ishonish mumkinligini tushunish",
                ],
                'blocks': [
                    block(
                        "Hallucinationni qanday aniqlash mumkin",
                        "1-bo'limda hallucination haqida o'rgangan edik. Endi uni ==qanday aniqlash va "
                        "kamaytirish== mumkinligini ko'ramiz:\n\n"
                        "- **Aniq raqam, sana, ism** aytilsa - shubhalaning, alohida tekshiring\n"
                        "- **\"Manba ko'rsat\"** deb so'rang - agar AI aniq manba keltira olmasa, "
                        "ehtiyot bo'ling\n"
                        "- **Bir xil savolni boshqacha shaklda qayta bering** - agar javob keskin "
                        "o'zgarsa, bu ishonchsizlik belgisi\n"
                        "- **\"Bunga qanchalik ishonchingiz komil?\"** deb so'rash ham foydali, lekin "
                        "AI bu savolga ham noto'g'ri baho berishi mumkinligini unutmang",
                    ),
                    block(
                        "Tekshirish darajasi vaziyatga bog'liq",
                        "Har bir AI javobini bir xil darajada tekshirish shart emas - ==xavf qanchalik "
                        "yuqori bo'lsa, tekshirish shunchalik chuqur bo'lishi kerak==:\n\n"
                        "- **Past xavf** (ijodiy g'oya, qoralama matn): tekshirmasdan ishlatish mumkin\n"
                        "- **O'rta xavf** (o'quv materiali, umumiy ma'lumot): asosiy faktlarni tez "
                        "tekshirish tavsiya etiladi\n"
                        "- **Yuqori xavf** (tibbiy, huquqiy, moliyaviy qaror, dastur kodi productionda "
                        "ishlatiladigan): **albatta mutaxassis yoki ishonchli manba bilan tasdiqlash shart**\n\n"
                        "Bu \"xavf darajasiga qarab tekshirish\" - AI bilan ishlashning eng muhim "
                        "amaliy ko'nikmalaridan biri.",
                    ),
                    block(
                        "AI - kuchli vosita, yakuniy javobgarlik insonda",
                        "Qanchalik rivojlangan bo'lmasin, ==yakuniy qarorlar va ularning oqibati uchun "
                        "javobgarlik insonda qoladi==. AI shifokor emas, huquqshunos emas, moliyaviy "
                        "maslahatchi emas - u faqat **yordamchi vosita**.\n\n"
                        "Amaliy qoida: AI javobini \"aqlli do'stning fikri\" sifatida qabul qiling - "
                        "foydali, ko'pincha to'g'ri, lekin **har doim so'nggi so'z sizniki va "
                        "tekshirish sizning zimmangizda**.",
                    ),
                ],
                'key_facts': [
                    fact("Aniq raqam/sana/ism kabi faktlarni alohida tekshirish kerak."),
                    fact("Tekshirish chuqurligi vaziyat xavfiga bog'liq bo'lishi kerak."),
                    fact("Yakuniy qaror va javobgarlik har doim insonda qoladi, AI'da emas."),
                ],
                'summary': "AI javobini ==xavf darajasiga qarab== tekshiring - past xavfda erkin, yuqori "
                           "xavfda (tibbiy, huquqiy, moliyaviy) albatta mutaxassis bilan tasdiqlang.",
            },
            'test': [
                mcq("Hallucinationni aniqlashning bir usuli qanday?", [
                    "AI'dan aniq manba ko'rsatishni so'rash", "Hech qachon savol bermaslik",
                    "Faqat bitta marta so'rab, boshqa tekshirmaslik", "AI'ni butunlay o'chirib qo'yish",
                ], 0),
                mcq("Yuqori xavfli qarorlarda (tibbiy, huquqiy) nima qilish kerak?", [
                    "Albatta mutaxassis yoki ishonchli manba bilan tasdiqlash",
                    "Faqat AI javobiga to'liq ishonish", "Hech qanday tekshiruv shart emas",
                    "Qarorni tasodifan qabul qilish",
                ], 0),
                mcq("Past xavfli vazifalarga (ijodiy g'oya) misol qaysi?", [
                    "Qoralama matn yozish", "Dori dozasini belgilash",
                    "Sud qarorini chiqarish", "Bank kreditini tasdiqlash",
                ], 0),
                mcq("Yakuniy qaror va javobgarlik kim zimmasida qoladi?", [
                    "Insonda", "To'liq AI'da", "Internet provayderida", "Kompyuter ishlab chiqaruvchisida",
                ], 0),
                mcq("Bir xil savolni boshqacha shaklda qayta berish nima uchun foydali?", [
                    "Javob keskin o'zgarsa, bu ishonchsizlik belgisi bo'lishi mumkin",
                    "Bu AI'ni charchatish uchun",
                    "Bu hech qanday foyda bermaydi",
                    "Bu faqat vaqtni behuda sarflaydi",
                ], 0),
            ],
        },
        {
            'key': 't6b', 'title': "AI etikasi va maxfiylik", 'start_page': 17, 'end_page': 17,
            'explanation': {
                'goals': [
                    "AI'ga shaxsiy/maxfiy ma'lumot berishda ehtiyotkorlikni tushunish",
                    "AI'dan noto'g'ri/zararli maqsadda foydalanish xavfini bilish",
                    "Mualliflik huquqi masalasini oddiy tushunish",
                ],
                'blocks': [
                    block(
                        "Maxfiylik: nimani AI'ga yozmaslik kerak",
                        "AI xizmatlariga yozgan xabarlaringiz ==kompaniya serverlariga yuboriladi== - "
                        "shuning uchun quyidagilarni yozishdan saqlaning (agar xizmat aniq maxfiylik "
                        "kafolati bermasa):\n\n"
                        "- Parollar, bank karta raqamlari, shaxsiy hujjat raqamlari\n"
                        "- Boshqa odamlarning ruxsatisiz shaxsiy ma'lumotlari\n"
                        "- Kompaniyangizning maxfiy biznes ma'lumotlari (agar ish joyingiz buni "
                        "taqiqlagan bo'lsa)\n\n"
                        "Oddiy qoida: **\"agar bu ma'lumotni notanish odamga aytishga tayyor "
                        "bo'lmasangiz, AI chatiga ham yozmang\"**.",
                    ),
                    block(
                        "Noto'g'ri foydalanish xavfi",
                        "AI kuchli vosita bo'lgani uchun, ==uni yomon niyatda ishlatish ham mumkin==: "
                        "soxta yangiliklar yaratish, boshqa odamning ovozi/qiyofasini ruxsatsiz "
                        "nusxalash (deepfake), maktab/universitet ishlarini butunlay AI'ga yozdirib, "
                        "o'zining bilim sifatida topshirish.\n\n"
                        "Bu kurs davomida biz doim ta'kidlagan narsa - **AI yordamchi, o'rinbosar "
                        "emas** - aynan shu sabab bilan muhim: yolg'on ma'lumot yoki firibgarlik uchun "
                        "ishlatilgan AI jamiyatga zarar keltiradi va ko'p mamlakatlarda jinoiy "
                        "javobgarlikka sabab bo'lishi mumkin.",
                    ),
                    block(
                        "Mualliflik huquqi haqida oddiy tushuncha",
                        "AI yaratgan matn, rasm yoki musiqaning mualliflik huquqi murakkab va hali "
                        "=juridik jihatdan to'liq aniq bo'lmagan== mavzu. Amaliy tavsiyalar:\n\n"
                        "- AI yaratgan kontentni tijorat maqsadida ishlatishdan oldin, ishlatayotgan "
                        "AI xizmatining foydalanish shartlarini (terms of service) o'qing\n"
                        "- Boshqa muallifning uslubini \"aynan nusxalash\" so'rovi bilan AI'dan "
                        "foydalanishdan saqlaning\n"
                        "- Agar kontent muhim/tijorat maqsadida bo'lsa, huquqshunosdan maslahat olish "
                        "foydali bo'lishi mumkin",
                    ),
                ],
                'key_facts': [
                    fact("Parol, karta raqami kabi maxfiy ma'lumotlarni AI chatiga yozmaslik kerak."),
                    fact("AI'ni firibgarlik yoki yolg'on ma'lumot yaratish uchun ishlatish jinoiy javobgarlikka sabab bo'lishi mumkin."),
                    fact("AI kontentining mualliflik huquqi hali to'liq aniqlanmagan, foydalanish shartlarini o'qish kerak."),
                ],
                'summary': "AI'ga **maxfiy ma'lumot yozmang**, uni **yolg'on/firibgarlik uchun "
                           "ishlatmang**, va tijorat kontentida ==mualliflik huquqi shartlarini tekshiring==.",
            },
            'test': [
                mcq("AI chatiga qanday ma'lumotlarni yozmaslik kerak?", [
                    "Parollar, bank karta raqamlari, maxfiy hujjatlar",
                    "Ob-havo haqidagi savollar", "Umumiy bilim savollari",
                    "Kitob mavzusi haqida savollar",
                ], 0),
                mcq("AI'ni yolg'on yangilik yoki firibgarlik uchun ishlatish nima bilan tugashi mumkin?", [
                    "Jinoiy javobgarlik", "Hech qanday oqibat", "Faqat maqtov",
                    "Avtomatik mukofot",
                ], 0),
                mcq("Oddiy maxfiylik qoidasi qanday shakllantiriladi?", [
                    "Notanish odamga aytishga tayyor bo'lmagan narsani AI'ga ham yozmaslik",
                    "Hamma narsani AI'ga yozish mumkin",
                    "Faqat parolni yozmaslik, boshqasi muhim emas",
                    "AI hech qachon ma'lumotni saqlamaydi",
                ], 0),
                mcq("AI kontentining mualliflik huquqi haqida nima deyish to'g'ri?", [
                    "Bu hali to'liq aniq bo'lmagan, murakkab mavzu",
                    "Bu masala butunlay hal qilingan va aniq",
                    "AI kontenti hech qachon ishlatilmasligi kerak",
                    "Mualliflik huquqi umuman mavjud emas",
                ], 0),
                mcq("Tijorat maqsadida AI kontent ishlatishdan oldin nima qilish tavsiya etiladi?", [
                    "Xizmatning foydalanish shartlarini o'qish",
                    "Hech narsa tekshirmasdan ishlatish",
                    "Faqat narxni tekshirish",
                    "Boshqa hech kimga aytmaslik",
                ], 0),
            ],
        },
        {
            'key': 't6c', 'title': "AI kelajagi va doimiy o'rganish", 'start_page': 18, 'end_page': 18,
            'explanation': {
                'goals': [
                    "AI sohasi tez o'zgarishini va doimiy o'rganish zarurligini tushunish",
                    "Kelajakda qaysi ko'nikmalar qadrli bo'lishini bilish",
                    "Kursdan keyingi o'rganish yo'lini rejalashtirish",
                ],
                'blocks': [
                    block(
                        "AI juda tez rivojlanmoqda",
                        "Siz shu kursda o'rgangan vositalar (ChatGPT, Claude, Gemini) bir necha yil "
                        "oldin mavjud emas edi, va ==keyingi bir necha yilda yana ancha o'zgaradi==. "
                        "Shuning uchun bu kursning eng muhim natijasi aniq bir vosita nomini "
                        "yodlash emas, balki **tamoyillarni tushunish**:\n\n"
                        "- Prompt yozish mantig'i\n"
                        "- Agent va avtomatlashtirish g'oyasi\n"
                        "- Tekshirish va tanqidiy fikrlash odati\n\n"
                        "Bu tamoyillar yangi vositalar chiqqanda ham amal qiladi.",
                    ),
                    block(
                        "Kelajakda qaysi ko'nikmalar qadrli bo'ladi",
                        "AI ko'plab oddiy, takrorlanuvchi vazifalarni avtomatlashtirgani sari, "
                        "==inson uchun quyidagi ko'nikmalar tobora qadrli bo'lib boradi==:\n\n"
                        "- **Tanqidiy fikrlash** - AI javobini baholash, xatoni topish\n"
                        "- **Ijodkorlik va original g'oyalar** - AI mavjud naqshlarni takrorlaydi, "
                        "haqiqiy yangilikni inson yaratadi\n"
                        "- **Muloqot va hissiy aql** - odamlar bilan ishonch o'rnatish, jamoada ishlash\n"
                        "- **Murakkab muammoni to'g'ri qo'yish** - AI'ga \"nima kerakligini\" aniq "
                        "tushuntira olish (bu butun kurs davomida o'rgangan narsangiz!)\n\n"
                        "Qiziq paradoks: ==AI qanchalik kuchli bo'lsa, \"inson\" ko'nikmalar shunchalik "
                        "muhimroq bo'lib boradi==.",
                    ),
                    block(
                        "Kursdan keyin nima qilish kerak",
                        "Bu kurs - **boshlang'ich nuqta**, yakuni emas. Davom etish uchun tavsiyalar:\n\n"
                        "1. **Har kuni amaliyot qiling**: haqiqiy vazifalaringizda AI'dan foydalaning "
                        "(o'qish, ish, shaxsiy loyihalar)\n"
                        "2. **Yangiliklarni kuzating**: yangi AI vositalari chiqqanda, ularning nima "
                        "o'zgacha qilishini tushunishga harakat qiling\n"
                        "3. **Kichik loyihalar yarating**: har oy bitta yangi narsa - chatbot, "
                        "avtomatlashtirish, veb-sahifa\n"
                        "4. **Jamiyatga qo'shiling**: onlayn forumlar, Telegram guruhlari orqali "
                        "boshqa o'rganuvchilar bilan tajriba almashing\n\n"
                        "**Yodda tuting**: bu kursni tugatgan bo'lsangiz, siz allaqachon ko'pchilikdan "
                        "oldinda turibsiz - endi shu bilimni **amalda qo'llash va chuqurlashtirish** "
                        "vaqti keldi.",
                    ),
                ],
                'key_facts': [
                    fact("AI vositalari tez o'zgaradi - tamoyillarni tushunish vosita nomidan muhimroq."),
                    fact("Tanqidiy fikrlash, ijodkorlik, muloqot - AI davrida tobora qadrli inson ko'nikmalari."),
                    fact("Kursdan keyin doimiy amaliyot va kichik loyihalar orqali o'rganishni davom ettirish kerak."),
                ],
                'summary': "AI tez o'zgaradi, lekin ==tamoyillar (prompt, tekshirish, tanqidiy fikrlash) "
                           "doim amal qiladi==. Bu - **boshlang'ich nuqta**, davomi amaliyotda.",
            },
            'test': [
                mcq("Kursning eng muhim natijasi nima bo'lishi kerak?", [
                    "Tamoyillarni tushunish, aniq vosita nomini yodlash emas",
                    "Faqat ChatGPT nomini yodlab olish", "Hech narsa, kurs foydasiz",
                    "Faqat imtihondan o'tish",
                ], 0),
                mcq("AI rivojlangani sari qaysi inson ko'nikmalari tobora qadrli bo'ladi?", [
                    "Tanqidiy fikrlash, ijodkorlik, muloqot",
                    "Faqat tez yozish tezligi", "Faqat xotira kuchi",
                    "Hech qanday ko'nikma kerak emas",
                ], 0),
                mcq("Kursdan keyin nima qilish tavsiya etiladi?", [
                    "Doimiy amaliyot qilish va kichik loyihalar yaratish",
                    "Hech qachon AI ishlatmaslik", "Faqat nazariy bilimni yetarli deb hisoblash",
                    "Kursni butunlay unutish",
                ], 0),
                mcq("Nega \"tamoyillarni tushunish\" vosita nomidan muhimroq?", [
                    "Vositalar tez o'zgaradi, lekin tamoyillar amal qilaveradi",
                    "Chunki vositalar hech qachon o'zgarmaydi",
                    "Chunki tamoyillar oson unutiladi",
                    "Hech qanday farqi yo'q",
                ], 0),
                mcq("\"Qiziq paradoks\" deb aytilgan narsa nima?", [
                    "AI qanchalik kuchli bo'lsa, inson ko'nikmalari shunchalik muhimroq bo'lishi",
                    "AI hech qachon ishlamasligi",
                    "Inson hech qachon AI'siz ishlay olmasligi",
                    "AI insonlardan aqlliroq bo'lishi",
                ], 0),
            ],
        },
    ],
})

# ============================================================
# YAKUNIY YIG'ISH VA YOZISH
# ============================================================
book_data = {
    'format_version': FORMAT_VERSION,
    'book': {
        'key': 'suniy_intellekt',
        'title': "Sun'iy intellekt: noldan ekspertgacha",
        'description': "AI nima ekanidan tortib, uni kundalik hayotda, dasturlashda va pul topishda "
                       "qanday qo'llashgacha - to'liq, sodda tilda yozilgan amaliy kurs.",
        'subject': 'suniy-intellekt',
        'subject_title': "Sun'iy intellekt",
    },
    'sections': sections,
}

import os
os.makedirs('backend/content/ai', exist_ok=True)
with open('backend/content/ai/book.json', 'w', encoding='utf-8') as f:
    json.dump(book_data, f, ensure_ascii=False, indent=2)
    f.write('\n')

n_topics = sum(len(s['topics']) for s in sections)
n_questions = sum(len(t['test']) for s in sections for t in s['topics'])
print(f"Tayyor: {len(sections)} bo'lim, {n_topics} mavzu, {n_questions} test savoli")
