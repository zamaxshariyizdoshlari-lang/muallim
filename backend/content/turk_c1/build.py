# -*- coding: utf-8 -*-
"""Turk tili C1 (Yedi Iklim Turkce C1 mundarijasi asosida): units/u*.py dan book.json va exam_bank.json quradi."""
import importlib.util
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
UNIT_TITLES = {
    'u1': "1-ünite. Spor (Sport)",
    'u2': "2-ünite. Değişen Dünya (O'zgaruvchan dunyo)",
    'u3': "3-ünite. Kelimelerin Büyülü Dünyası (So'zlarning sehrli olami)",
    'u4': "4-ünite. Canlılar Âlemi (Jonzotlar olami)",
    'u5': "5-ünite. Tarihe Yolculuk (Tarixga sayohat)",
    'u6': "6-ünite. Bilimin Gözüyle (Fan nazari bilan)",
    'u7': "7-ünite. Sayılarla Hayat (Sonlar bilan hayot)",
    'u8': "8-ünite. Kişiler, Kişilikler (Shaxslar, shaxsiyatlar)",
}

sections, bank = [], {}
for uk, title in UNIT_TITLES.items():
    path = os.path.join(HERE, 'units', f'{uk}.py')
    if not os.path.exists(path):
        continue
    spec = importlib.util.spec_from_file_location(uk, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    topics = []
    for t, b in mod.TOPICS:
        topics.append(t)
        bank[t['key']] = b
    sections.append({'key': uk, 'title': title, 'topics': topics})

book = {
    'format_version': 1,
    'book': {
        'key': 'turk_c1', 'title': "Turk tili C1 (Yedi İklim)",
        'description': "Yedi İklim Türkçe C1 darsligi mundarijasi asosida: ilg'or daraja, 8 ünite, "
                       "24 mavzu, o'zbek tilida tushuntirilgan.",
        'subject': 'turk-tili', 'subject_title': "Turk tili",
    },
    'sections': sections,
}
with open(os.path.join(HERE, 'book.json'), 'w', encoding='utf-8') as f:
    json.dump(book, f, ensure_ascii=False, indent=2); f.write('\n')
with open(os.path.join(HERE, 'exam_bank.json'), 'w', encoding='utf-8') as f:
    json.dump(bank, f, ensure_ascii=False, indent=2); f.write('\n')
print(f"{len(sections)} ünite, {sum(len(s['topics']) for s in sections)} mavzu, {sum(len(v) for v in bank.values())} bank savoli")
