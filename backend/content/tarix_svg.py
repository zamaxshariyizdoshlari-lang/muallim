# -*- coding: utf-8 -*-
"""Tarix kurslari uchun original SVG rasmlar: vaqt chizig'i, taqqoslash, sxema. Barchasi o'zimiz chizgan."""
import json, os, sys, textwrap
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'geo'))
from svglib import svg, T, box, line, circle, tint, PAL, INK, MUTED, ARROW_DEF, W, H, flow, layers, cycle, bars


def wrap(s, n):
    return textwrap.wrap(s, n) or ['']


def timeline(title, events):
    """events: [(sana, matn)] — 3..6 ta, tepa/pastga navbatma-navbat."""
    n = len(events)
    out = [line(30, 215, W - 30, 215, '#94a3b8', 4)]
    step = (W - 100) / max(n - 1, 1)
    for i, (d, s) in enumerate(events):
        x = 50 + i * step
        col = PAL[i % len(PAL)]
        up = i % 2 == 0
        out.append(line(x, 215, x, 160 if up else 270, col, 2))
        out.append(circle(x, 215, 9, col, '#fff', 2))
        lines = wrap(s, 22)
        bh = 24 + 16 * len(lines)
        by = 160 - bh if up else 270
        bw = 150
        bx = min(max(x - bw / 2, 8), W - bw - 8)
        out.append(box(bx, by, bw, bh, tint(col, 0.28), col, rx=10, sw=2))
        out.append(T(bx + bw / 2, by + 18, d, 13, INK, weight='800'))
        for j, ln in enumerate(lines):
            out.append(T(bx + bw / 2, by + 36 + 16 * j, ln, 11.5, INK))
    return svg(title, ''.join(out))


def compare(title, lt, litems, rt, ritems):
    out = []
    for k, (head, items) in enumerate(((lt, litems), (rt, ritems))):
        col = PAL[k * 3 % len(PAL)] if k == 0 else PAL[3]
        x = 20 + k * 350
        out.append(box(x, 50, 330, 330, tint(col, 0.2), col, rx=14, sw=2))
        out.append(box(x, 50, 330, 40, col, rx=14))
        out.append(T(x + 165, 76, head, 15, '#fff', weight='800'))
        y = 112
        for it in items:
            ls = wrap(it, 38)
            out.append(circle(x + 22, y - 4, 4, col))
            for j, ln in enumerate(ls):
                out.append(T(x + 36, y + 16 * j, ln, 12.5, INK, anchor='start'))
            y += 16 * len(ls) + 14
    return svg(title, ''.join(out))


def tree(title, root, kids):
    """root: matn, kids: [(nom, izoh)] — markazdagi tushuncha va shoxlar."""
    n = len(kids)
    out = [ARROW_DEF]
    bw = (W - 40 - 14 * (n - 1)) / n
    out.append(box(W / 2 - 120, 55, 240, 44, '#1f2937', rx=12))
    out.append(T(W / 2, 83, root, 15, '#fff', weight='800'))
    for i, (nm, sub) in enumerate(kids):
        x = 20 + i * (bw + 14)
        col = PAL[i % len(PAL)]
        out.append(line(W / 2, 99, x + bw / 2, 150, '#64748b', 2, arrow=True))
        out.append(box(x, 150, bw, 220, tint(col, 0.25), col, rx=12, sw=2))
        out.append(T(x + bw / 2, 176, nm, 13, INK, weight='800'))
        cap = max(int(bw / 7.2), 8)
        for j, ln in enumerate(wrap(sub, cap)[:9]):
            out.append(T(x + bw / 2, 204 + 16 * j, ln, 11.5, MUTED))
    return svg(title, ''.join(out))


def inject(course, imgs):
    """imgs: {topic_key: [(fayl, sarlavha, svg_matn)]} — SVG yoziladi, JSON'larga explanation.images qo'shiladi."""
    root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    pub = os.path.join(root, 'frontend', 'public', course)
    os.makedirs(pub, exist_ok=True)
    meta = {k: [{'src': f'/{course}/{f}.svg', 'caption': c} for f, c, _ in v] for k, v in imgs.items()}
    for k, v in imgs.items():
        for f, c, s in v:
            open(os.path.join(pub, f + '.svg'), 'w', encoding='utf-8').write(s)

    def patch(d):
        if d.get('key') in meta:
            d['explanation']['images'] = meta[d['key']]
            return 1
        return 0
    base = os.path.join(root, 'backend', 'content', course)
    n = 0
    bp = os.path.join(base, 'book.json')
    b = json.load(open(bp, encoding='utf-8'))
    for s in b['sections']:
        for t in s['topics']:
            n += patch(t)
    json.dump(b, open(bp, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    td = os.path.join(base, 'topics')
    for fn in os.listdir(td):
        p = os.path.join(td, fn)
        d = json.load(open(p, encoding='utf-8'))
        if patch(d):
            json.dump(d, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print(f'{course}: {sum(len(v) for v in imgs.values())} rasm, {n} mavzu yangilandi')


def adder(pref, I):
    def add(k, tl, tle, f2, t2, s2):
        I[k] = [(f'{pref}_{k}_vaqt', tl + ': vaqt chizig\'i', timeline(tl, tle)), (f'{pref}_{k}_{f2}', t2, s2)]
    return add
