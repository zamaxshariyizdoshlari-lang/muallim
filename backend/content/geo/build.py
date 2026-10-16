# -*- coding: utf-8 -*-
"""Geografiya kursi: units/g*.py dan book.json va exam_bank.json quradi."""
import importlib.util
import json
import os

import sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
SECTION_TITLES = {
    'g1': "1-bo'lim. Yer va xarita",
    'g2': "2-bo'lim. Litosfera va relyef",
    'g3': "3-bo'lim. Atmosfera va iqlim",
    'g4': "4-bo'lim. Gidrosfera",
    'g5': "5-bo'lim. Biosfera, tuproq va tabiat zonalari",
    'g6': "6-bo'lim. Materiklar va okeanlar",
    'g7': "7-bo'lim. Aholi va xo'jalik",
    'g8': "8-bo'lim. O'zbekiston geografiyasi",
    'g9': "9-bo'lim. Global muammolar",
}

sections, bank = [], {}
IMG_OUT = {}
for sk, title in SECTION_TITLES.items():
    path = os.path.join(HERE, 'units', f'{sk}.py')
    if not os.path.exists(path):
        continue
    spec = importlib.util.spec_from_file_location(sk, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    for name, content in getattr(mod, 'IMAGES', {}).items():
        IMG_OUT[name] = content
    extras = {}
    xpath = os.path.join(HERE, 'units', f'{sk}_x.py')
    if os.path.exists(xpath):
        xspec = importlib.util.spec_from_file_location(sk + '_x', xpath)
        xmod = importlib.util.module_from_spec(xspec)
        xspec.loader.exec_module(xmod)
        extras = xmod.EXTRAS
    topics = []
    for t, b in mod.TOPICS:
        t['explanation'].update(extras.get(t['key'], {}))
        topics.append(t)
        bank[t['key']] = b
    sections.append({'key': sk, 'title': title, 'topics': topics})

book = {
    'format_version': 1,
    'book': {
        'key': 'geografiya', 'title': "Geografiya (rasmli kurs)",
        'description': "Geografiya: Yer va xarita, litosfera, atmosfera, gidrosfera, biosfera, materiklar, aholi va xo'jalik, O'zbekiston geografiyasi va global muammolar - ko'plab sxematik rasm va xaritalar bilan.",
        'subject': 'geografiya', 'subject_title': "Geografiya",
    },
    'sections': sections,
}
with open(os.path.join(HERE, 'book.json'), 'w', encoding='utf-8') as f:
    json.dump(book, f, ensure_ascii=False, indent=1)
with open(os.path.join(HERE, 'exam_bank.json'), 'w', encoding='utf-8') as f:
    json.dump(bank, f, ensure_ascii=False, indent=1)
nt = sum(len(t['test']) for s in sections for t in s['topics'])
print(f"{len(sections)} bo'lim, {sum(len(s['topics']) for s in sections)} mavzu, test {nt}, bank {sum(len(v) for v in bank.values())}")

IMG_DIR = os.path.abspath(os.path.join(HERE, '..', '..', '..', 'frontend', 'public', 'geo'))
os.makedirs(IMG_DIR, exist_ok=True)
for name, content in IMG_OUT.items():
    with open(os.path.join(IMG_DIR, name + '.svg'), 'w', encoding='utf-8') as f:
        f.write(content)
print(f"{len(IMG_OUT)} ta rasm yozildi")
