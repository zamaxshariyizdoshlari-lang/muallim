# -*- coding: utf-8 -*-
"""Tarix kurslari uchun original SVG rasmlar: vaqt chizig'i, taqqoslash, sxema. Barchasi o'zimiz chizgan."""
import json, os, sys, textwrap
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'geo'))
from svglib import svg, T, box, line, circle, poly, tint, PAL, INK, MUTED, ARROW_DEF, W, H, flow, layers, cycle, bars


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
    for fn in (os.listdir(td) if os.path.isdir(td) else []):
        p = os.path.join(td, fn)
        d = json.load(open(p, encoding='utf-8'))
        if patch(d):
            json.dump(d, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print(f'{course}: {sum(len(v) for v in imgs.values())} rasm, {n} mavzu yangilandi')


def adder1(pref, I):
    def add(k, cap, svgtext):
        I[k] = [(f'{pref}_{k}', cap, svgtext)]
    return add


class P:
    """Koordinata tekisligi: matematik koordinatalardan piksellarga."""
    def __init__(self, xr, yr, box=(70, 55, 650, 365)):
        self.xr, self.yr, self.b = xr, yr, box
        self.o = []

    def X(self, x):
        a, b, c, d = self.b
        return a + (x - self.xr[0]) / (self.xr[1] - self.xr[0]) * (c - a)

    def Y(self, y):
        a, b, c, d = self.b
        return d - (y - self.yr[0]) / (self.yr[1] - self.yr[0]) * (d - b)

    def axes(self, grid=True, xs=None, ys=None):
        import math as _m
        a, b, c, d = self.b
        xs = xs if xs is not None else range(int(_m.ceil(self.xr[0])), int(_m.floor(self.xr[1])) + 1)
        ys = ys if ys is not None else range(int(_m.ceil(self.yr[0])), int(_m.floor(self.yr[1])) + 1)
        for x in xs:
            if grid:
                self.o.append(line(self.X(x), b, self.X(x), d, '#e2e8f0', 1))
            if x != 0:
                self.o.append(T(self.X(x), self.Y(0) + 15, x, 10.5, MUTED))
        for y in ys:
            if grid:
                self.o.append(line(a, self.Y(y), c, self.Y(y), '#e2e8f0', 1))
            if y != 0:
                self.o.append(T(self.X(0) - 6, self.Y(y) + 4, y, 10.5, MUTED, anchor='end'))
        self.o.append(line(a, self.Y(0), c, self.Y(0), '#334155', 2, arrow=True))
        self.o.append(line(self.X(0), d, self.X(0), b, '#334155', 2, arrow=True))
        self.o.append(T(c + 2, self.Y(0) - 6, 'x', 12, INK, anchor='end', italic=True))
        self.o.append(T(self.X(0) + 10, b + 4, 'y', 12, INK, anchor='start', italic=True))
        return self

    def curve(self, f, color='#ef4444', x0=None, x1=None, n=160, sw=3):
        x0 = self.xr[0] if x0 is None else x0
        x1 = self.xr[1] if x1 is None else x1
        pts = []
        for i in range(n + 1):
            x = x0 + (x1 - x0) * i / n
            try:
                y = f(x)
            except Exception:
                pts.append(None)
                continue
            if y is None or y < self.yr[0] - 0.3 or y > self.yr[1] + 0.3:
                pts.append(None)
            else:
                pts.append((self.X(x), self.Y(y)))
        seg = []
        for q in pts + [None]:
            if q is None:
                if len(seg) > 1:
                    self.o.append('<polyline fill="none" stroke="%s" stroke-width="%s" points="%s"/>' % (color, sw, ' '.join('%.1f,%.1f' % t for t in seg)))
                seg = []
            else:
                seg.append(q)
        return self

    def pt(self, x, y, label='', color='#1f2937', dx=8, dy=-8, r=5):
        self.o.append(circle(self.X(x), self.Y(y), r, color, '#fff', 2))
        if label:
            self.o.append(T(self.X(x) + dx, self.Y(y) + dy, label, 12, INK, anchor='start', weight='700'))
        return self

    def text(self, x, y, s, size=12, color=INK, anchor='start', weight='400'):
        self.o.append(T(self.X(x), self.Y(y), s, size, color, anchor=anchor, weight=weight))
        return self

    def seg(self, x1, y1, x2, y2, color='#334155', sw=2, dash='', arrow=False):
        self.o.append(line(self.X(x1), self.Y(y1), self.X(x2), self.Y(y2), color, sw, dash, arrow))
        return self

    def raw(self, s):
        self.o.append(s)
        return self

    def done(self, title):
        return svg(title, ''.join([ARROW_DEF] + self.o))


def adder(pref, I):
    def add(k, tl, tle, f2, t2, s2):
        I[k] = [(f'{pref}_{k}_vaqt', tl + ': vaqt chizig\'i', timeline(tl, tle)), (f'{pref}_{k}_{f2}', t2, s2)]
    return add
