# -*- coding: utf-8 -*-
"""Turk tili B2 (Yedi Iklim Turkce B2 mundarijasi asosida): units/u*.py dan book.json va exam_bank.json quradi."""
import importlib.util
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
UNIT_TITLES = {
    'u1': "1-ünite. Mesleğimde İlerliyorum (Kasbimda yuksalaman)",
    'u2': "2-ünite. Değerlerimiz (Qadriyatlarimiz)",
    'u3': "3-ünite. Bir Ömür Böyle Geçti (Umr shunday o'tdi)",
    'u4': "4-ünite. Mutfakta Kim Var? (Oshxonada kim bor?)",
    'u5': "5-ünite. Tercihiniz Nedir? (Tanlovingiz qaysi?)",
    'u6': "6-ünite. Neler Oluyor Hayatta? (Hayotda nimalar bo'lyapti?)",
    'u7': "7-ünite. Öğrendim, Çalıştım, Başardım (O'rgandim, ishladim, uddaladim)",
    'u8': "8-ünite. Misafir Sever misiniz? (Mehmonni yoqtirasizmi?)",
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
        'key': 'turk_b2', 'title': "Turk tili B2 (Yedi İklim)",
        'description': "Yedi İklim Türkçe B2 darsligi mundarijasi asosida: yuqori o'rta daraja, 8 ünite, "
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
