SYSTEM_RULES = """Sen "Tarixchi AI" tizimisan. Faqat quyida berilgan darslik matni asosida ishlaysan.

QATIY QOIDALAR:
- Barcha faktlarni (sana, shaxs, joy, voqea, sabab-oqibat) FAQAT berilgan matndan ol. O'zingdan yangi tarixiy fakt qo'shma.
- Matnda ma'lumot bo'lmasa, uni to'qib chiqarma — shunchaki tushirib qoldir.
- Har bir faktdan keyin uning bet raqamini [bet N] shaklida ko'rsat.
- Faktni oddiy tilda tushuntirish, qisqa o'xshatish yoki misol keltirish mumkin, lekin bu tushuntirish yangi tarixiy fakt kiritmasligi kerak.
- Javobni FAQAT o'zbek tilida yoz.
- Javobni FAQAT quyida ko'rsatilgan JSON formatida qaytar, boshqa hech qanday matn qo'shma.
"""


def _pages_block(pages):
    return '\n\n'.join(f"--- BET {num} ---\n{text}" for num, text in pages if text)


def build_lesson_prompt(topic_title, pages):
    """pages: [(page_number, text), ...] — faqat shu mavzuga tegishli betlar."""
    pages_block = _pages_block(pages)

    return f"""{SYSTEM_RULES}

MAVZU: {topic_title}

DARSLIK MATNI:
{pages_block}

Quyidagi JSON formatida javob ber (boshqa matn qo'shmasdan, faqat JSON):

{{
  "lesson_plan": {{
    "topic": "mavzu nomi",
    "goals": ["dars maqsadi 1", "dars maqsadi 2"],
    "key_facts": [
      {{"fact": "qisqa fakt matni", "page": <bet raqami>}}
    ],
    "explanation": "faktlarni oddiy tilda tushuntirish, o'xshatish/misollar bilan (yangi fakt qo'shmasdan)",
    "summary": "darsning qisqa xulosasi"
  }},
  "quiz": {{
    "questions": [
      {{
        "question": "savol matni",
        "options": ["variant A", "variant B", "variant C", "variant D"],
        "correct_index": 0,
        "page": <javob asoslangan bet raqami>
      }}
    ]
  }}
}}

Kamida 5 ta test savoli tuz. Agar matnda mavzu bo'yicha yetarli ma'lumot bo'lmasa, "key_facts" yoki "questions" ro'yxatini qisqaroq qoldir, lekin hech qachon to'qib yozma.
"""


def build_presentation_prompt(topic_title, pages):
    """Interaktiv taqdimot uchun slaydlar (JSON) tuzadi — frontend buni HTML slaydlar sifatida ko'rsatadi."""
    pages_block = _pages_block(pages)

    return f"""{SYSTEM_RULES}

MAVZU: {topic_title}

DARSLIK MATNI:
{pages_block}

Ushbu mavzu uchun taqdimot slaydlarini tuz. Har bir slayd — bitta kichik g'oya yoki fakt guruhi.
Birinchi slayd sarlavha slaydi bo'lsin (mavzu nomi, "page" maydonisiz).

Quyidagi JSON formatida javob ber (boshqa matn qo'shmasdan, faqat JSON):

{{
  "slides": [
    {{"title": "{topic_title}", "bullets": [], "page": null}},
    {{"title": "Slayd sarlavhasi", "bullets": ["fakt 1", "fakt 2"], "page": <bet raqami>}}
  ]
}}

Kamida 5 ta, ko'pi bilan 10 ta slayd tuz. Har bir "bullets" elementi qisqa (bitta gap) bo'lsin.
"""


def build_timeline_game_prompt(topic_title, pages):
    """Xronologiya tartiblash o'yini uchun to'g'ri tartibdagi voqealar ro'yxatini tuzadi."""
    pages_block = _pages_block(pages)

    return f"""{SYSTEM_RULES}

MAVZU: {topic_title}

DARSLIK MATNI:
{pages_block}

Ushbu mavzudagi voqealarni xronologik (vaqt) tartibida ro'yxatla — bu "voqealarni tartiblash" o'yini uchun ishlatiladi.
Faqat matnda aniq vaqt/tartib ko'rsatilgan voqealarni ol.

Quyidagi JSON formatida javob ber (boshqa matn qo'shmasdan, faqat JSON):

{{
  "items": [
    {{"label": "voqea qisqa tavsifi", "page": <bet raqami>}}
  ]
}}

"items" ro'yxati DARSLIK MATNIDAGI VOQEALARNING TO'G'RI XRONOLOGIK TARTIBIDA bo'lsin (birinchi bo'lib sodir bo'lgani birinchi). Kamida 4, ko'pi bilan 8 ta voqea. Agar matnda yetarlicha tartiblanadigan voqea topilmasa, ro'yxatni qisqaroq qoldir.
"""


def build_matching_game_prompt(topic_title, pages):
    """Moslashtirish o'yini uchun juftliklar (masalan shaxs-voqea, sana-hodisa) tuzadi."""
    pages_block = _pages_block(pages)

    return f"""{SYSTEM_RULES}

MAVZU: {topic_title}

DARSLIK MATNI:
{pages_block}

Ushbu mavzudan "moslashtirish" o'yini uchun juftliklar tuz (masalan: shaxs → uning ishi, sana → voqea, atama → izoh).

Quyidagi JSON formatida javob ber (boshqa matn qo'shmasdan, faqat JSON):

{{
  "pairs": [
    {{"left": "chap tomon (masalan ism yoki sana)", "right": "o'ng tomon (mos javob)", "page": <bet raqami>}}
  ]
}}

Kamida 4, ko'pi bilan 8 ta juftlik tuz. Har bir juftlik faqat matndagi haqiqiy faktga asoslangan bo'lsin.
"""
