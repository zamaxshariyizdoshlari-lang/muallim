# -*- coding: utf-8 -*-
"""Geografiya uchun sxematik SVG rasmlar generatori (hammasi original, tashqi manbasiz)."""
import math
from xml.sax.saxutils import escape

W, H = 720, 400
INK, MUTED, LINE = '#1f2937', '#64748b', '#cbd5e1'
PAL = ['#60a5fa', '#34d399', '#fbbf24', '#f87171', '#a78bfa', '#fb923c', '#2dd4bf', '#f472b6', '#94a3b8', '#84cc16']
LAND, SEA = '#d9e8c4', '#dbeafe'


def tint(hexcol, a=0.3):
    h = hexcol.lstrip('#')[:6]
    r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
    f = lambda c: int(255 - (255 - c) * a)
    return f'#{f(r):02x}{f(g):02x}{f(b):02x}'


def svg(title, body, w=W, h=H, bg='#f8fafc'):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" role="img" aria-label="{escape(title)}" '
            f'font-family="system-ui, -apple-system, Segoe UI, Roboto, sans-serif">'
            f'<rect width="{w}" height="{h}" rx="14" fill="{bg}"/>'
            f'<text x="{w/2}" y="28" text-anchor="middle" font-size="17" font-weight="700" fill="{INK}">{escape(title)}</text>'
            f'{body}</svg>')


def T(x, y, s, size=13, fill=INK, anchor='middle', weight='400', rot=0, italic=False):
    r = f' transform="rotate({rot} {x} {y})"' if rot else ''
    it = ' font-style="italic"' if italic else ''
    return f'<text x="{x:.1f}" y="{y:.1f}" text-anchor="{anchor}" font-size="{size}" font-weight="{weight}" fill="{fill}"{it}{r}>{escape(str(s))}</text>'


def box(x, y, w, h, fill, stroke='none', rx=8, sw=1):
    return f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'


def line(x1, y1, x2, y2, stroke=INK, sw=2, dash='', arrow=False):
    d = f' stroke-dasharray="{dash}"' if dash else ''
    out = f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{stroke}" stroke-width="{sw}"{d}/>'
    if arrow:
        a = math.atan2(y2 - y1, x2 - x1)
        L = 8 + sw * 1.5
        p1 = (x2 - L * math.cos(a - 0.45), y2 - L * math.sin(a - 0.45))
        p2 = (x2 - L * math.cos(a + 0.45), y2 - L * math.sin(a + 0.45))
        out += f'<path d="M{x2:.1f} {y2:.1f} L{p1[0]:.1f} {p1[1]:.1f} L{p2[0]:.1f} {p2[1]:.1f}Z" fill="{stroke}"/>'
    return out


ARROW_DEF = ('<defs><marker id="ar" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
             '<path d="M0 0L10 5L0 10z" fill="#334155"/></marker></defs>')


def circle(x, y, r, fill, stroke='none', sw=1):
    return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'


def poly(pts, fill, stroke='none', sw=1, close=True):
    d = 'M' + ' L'.join(f'{x:.1f} {y:.1f}' for x, y in pts) + ('Z' if close else '')
    f = fill if close else 'none'
    return f'<path d="{d}" fill="{f}" stroke="{stroke}" stroke-width="{sw}" stroke-linejoin="round"/>'


def layers(title, items, note=''):
    """items: [(nom, izoh, rang, nisbiy_balandlik)] yuqoridan pastga."""
    tot = sum(i[3] for i in items)
    top, hh = 50, H - 85
    out = []
    y = top
    for name, sub, col, rel in items:
        h = hh * rel / tot
        out.append(box(40, y, 320, h, col, '#ffffff', rx=4, sw=2))
        out.append(T(200, y + h / 2 + 5, name, 15, INK, weight='700'))
        out.append(T(375, y + h / 2 + 5, sub, 13, INK, anchor='start'))
        y += h
    if note:
        out.append(T(W / 2, H - 14, note, 12, MUTED))
    return svg(title, ''.join(out))


def cycle(title, nodes, center=''):
    cx, cy, rx, ry = W / 2, 220, 255, 125
    n = len(nodes)
    pts = []
    for i in range(n):
        a = -math.pi / 2 + 2 * math.pi * i / n
        pts.append((cx + rx * math.cos(a), cy + ry * math.sin(a)))
    out = [ARROW_DEF]
    for i, (name, sub) in enumerate(nodes):
        x, y = pts[i]
        out.append(box(x - 62, y - 24, 124, 48, tint(PAL[i % len(PAL)], 0.35), PAL[i % len(PAL)], rx=12, sw=2))
        out.append(T(x, y - 3, name, 13, INK, weight='700'))
        if sub:
            out.append(T(x, y + 13, sub, 11, MUTED))
    for i in range(n):
        x1, y1 = pts[i]
        x2, y2 = pts[(i + 1) % n]
        dx, dy = x2 - x1, y2 - y1
        L = math.hypot(dx, dy) or 1
        ux, uy = dx / L, dy / L
        t = min(62 / abs(ux) if abs(ux) > 1e-6 else 1e9, 24 / abs(uy) if abs(uy) > 1e-6 else 1e9) + 6
        out.append(line(x1 + ux * t, y1 + uy * t, x2 - ux * t, y2 - uy * t, '#334155', 2.5, arrow=True))
    if center:
        out.append(T(cx, cy + 4, center, 15, MUTED, weight='700'))
    return svg(title, ''.join(out))


def flow(title, steps, note=''):
    n = len(steps)
    gap = 30
    bw = (W - 40 - gap * (n - 1)) / n
    out = [ARROW_DEF]
    for i, (name, sub) in enumerate(steps):
        x = 20 + i * (bw + gap)
        col = PAL[i % len(PAL)]
        out.append(box(x, 120, bw, 160, tint(col, 0.28), col, rx=12, sw=2))
        out.append(T(x + bw / 2, 155, str(i + 1), 22, col, weight='800'))
        words = name.split(' ')
        if len(name) > 11 and len(words) > 1:
            half = len(words) // 2 or 1
            out.append(T(x + bw / 2, 188, ' '.join(words[:half]), 13, INK, weight='700'))
            out.append(T(x + bw / 2, 204, ' '.join(words[half:]), 13, INK, weight='700'))
        else:
            out.append(T(x + bw / 2, 194, name, 13, INK, weight='700'))
        out.append(T(x + bw / 2, 240, sub, 11, MUTED))
        if i < n - 1:
            out.append(line(x + bw + 1, 200, x + bw + gap - 1, 200, '#334155', 2, arrow=True))
    if note:
        out.append(T(W / 2, H - 20, note, 12, MUTED))
    return svg(title, ''.join(out))


def bars(title, data, unit='', maxv=None, note=''):
    maxv = maxv or max(v for _, v in data)
    out = []
    top, rowh = 55, (H - 105) / len(data)
    for i, (name, v) in enumerate(data):
        y = top + i * rowh
        bw = (W - 300) * v / maxv
        out.append(T(190, y + rowh / 2 + 4, name, 13, INK, anchor='end'))
        out.append(box(200, y + 4, max(bw, 2), rowh - 10, PAL[i % len(PAL)], rx=4))
        out.append(T(208 + bw, y + rowh / 2 + 4, f'{v:g} {unit}', 12, INK, anchor='start', weight='700'))
    if note:
        out.append(T(W / 2, H - 14, note, 12, MUTED))
    return svg(title, ''.join(out))


def pie(title, data, note=''):
    tot = sum(v for _, v in data)
    cx, cy, r = 210, 215, 135
    a = -math.pi / 2
    out = []
    for i, (name, v) in enumerate(data):
        b = a + 2 * math.pi * v / tot
        x1, y1 = cx + r * math.cos(a), cy + r * math.sin(a)
        x2, y2 = cx + r * math.cos(b), cy + r * math.sin(b)
        large = 1 if b - a > math.pi else 0
        out.append(f'<path d="M{cx} {cy} L{x1:.1f} {y1:.1f} A{r} {r} 0 {large} 1 {x2:.1f} {y2:.1f}Z" fill="{PAL[i % len(PAL)]}" stroke="#fff" stroke-width="2"/>')
        a = b
    for i, (name, v) in enumerate(data):
        y = 95 + i * 30
        out.append(box(400, y - 12, 18, 18, PAL[i % len(PAL)], rx=4))
        out.append(T(428, y + 2, f'{name} — {v:g}%', 14, INK, anchor='start'))
    if note:
        out.append(T(W / 2, H - 14, note, 12, MUTED))
    return svg(title, ''.join(out))


def linechart(title, xs, ys, xlabel='', ylabel='', labels=None, color='#ef4444', bars_y=None, bar_color='#60a5fa', ylim=None):
    L, R, Tp, B = 70, 55, 55, 70
    cw, ch = W - L - R, H - Tp - B
    lo, hi = ylim or (min(ys), max(ys))
    if not ylim:
        pad = (hi - lo) * 0.15 or 1
        lo, hi = lo - pad, hi + pad
    X = lambda i: L + cw * i / (len(xs) - 1)
    Y = lambda v: Tp + ch * (1 - (v - lo) / (hi - lo))
    out = [line(L, Tp, L, Tp + ch, '#475569', 2), line(L, Tp + ch, L + cw, Tp + ch, '#475569', 2)]
    for k in range(5):
        v = lo + (hi - lo) * k / 4
        out.append(line(L, Y(v), L + cw, Y(v), LINE, 1, '4 4'))
        out.append(T(L - 8, Y(v) + 4, f'{v:.0f}', 11, MUTED, anchor='end'))
    if bars_y:
        bm = max(bars_y)
        for k in range(5):
            out.append(T(L + cw + 6, Y(lo + (hi - lo) * k / 4) + 4, f'{bm * 0.75 * k / 4 / 0.75:.0f}', 10, '#2563eb', anchor='start'))
        out.append(T(W - 10, Tp - 6, "Yog'in (mm)", 10, '#2563eb', anchor='end'))
        for i, v in enumerate(bars_y):
            bh = ch * 0.75 * v / bm
            out.append(box(X(i) - cw / len(xs) * 0.3, Tp + ch - bh, cw / len(xs) * 0.6, bh, tint(bar_color, 0.6), rx=2))
    out.append(poly([(X(i), Y(v)) for i, v in enumerate(ys)], color, color, 3, close=False))
    for i, v in enumerate(ys):
        out.append(circle(X(i), Y(v), 4, color))
        out.append(T(X(i), Tp + ch + 18, xs[i], 11, MUTED))
    out.append(T(W / 2, H - 22, xlabel, 12, MUTED))
    out.append(T(18, Tp + ch / 2, ylabel, 12, MUTED, rot=-90))
    for (i, txt) in (labels or []):
        out.append(T(X(i), Y(ys[i]) - 12, txt, 12, INK, weight='700'))
    return svg(title, ''.join(out))


def profile(title, pts, labels, water=None):
    """pts: [(x 0..100, balandlik 0..100)] ; labels: [(x, y, matn)]"""
    X = lambda x: 40 + (W - 80) * x / 100
    Y = lambda y: H - 60 - (H - 130) * y / 100
    out = [box(40, 45, W - 80, H - 105, '#e0f2fe', rx=6)]
    ground = [(X(x), Y(y)) for x, y in pts]
    out.append(poly([(X(pts[0][0]), Y(0))] + ground + [(X(pts[-1][0]), Y(0))], '#c4a574', '#8b6b3d', 2))
    if water:
        wx0, wx1, wy = water
        out.append(poly([(X(wx0), Y(wy)), (X(wx1), Y(wy)), (X(wx1), Y(wy) + 14), (X(wx0), Y(wy) + 14)], '#60a5fa'))
    for x, y, t in labels:
        out.append(T(X(x), Y(y), t, 13, INK, weight='700'))
    out.append(line(40, Y(0), W - 40, Y(0), '#475569', 2))
    return svg(title, ''.join(out))


def zones(title, bands, note=''):
    """bands: [(nom, izoh, rang, lat_from, lat_to)] shimoldan janubga"""
    X0, X1 = 110, W - 40
    Y = lambda lat: 50 + (H - 100) * (90 - lat) / 180
    out = []
    for name, sub, col, a, b in bands:
        out.append(box(X0, Y(a), X1 - X0, Y(b) - Y(a), col, '#fff', rx=2, sw=1.5))
        out.append(T((X0 + X1) / 2, (Y(a) + Y(b)) / 2 + 4, name, 14, INK, weight='700'))
        out.append(T((X0 + X1) / 2, (Y(a) + Y(b)) / 2 + 19, sub, 11, MUTED))
    for lat in (90, 66.5, 23.5, 0, -23.5, -66.5, -90):
        out.append(line(X0 - 8, Y(lat), X0, Y(lat), '#475569', 2))
        suf = '' if lat in (0, 90, -90) else (' Sh' if lat > 0 else ' J')
        out.append(T(X0 - 12, Y(lat) + 4, f'{abs(lat):g}°{suf}', 11, MUTED, anchor='end'))
    if note:
        out.append(T(W / 2, H - 12, note, 12, MUTED))
    return svg(title, ''.join(out))


CONT = {
    'sh_amerika': [(-168, 66), (-156, 71), (-125, 70), (-95, 72), (-80, 70), (-62, 60), (-56, 52), (-66, 45), (-70, 42), (-76, 35), (-81, 31), (-80, 25), (-84, 30), (-90, 29), (-97, 26), (-97, 21), (-88, 21), (-87, 15), (-83, 10), (-79, 9), (-86, 12), (-92, 15), (-105, 20), (-110, 24), (-115, 30), (-118, 34), (-124, 40), (-124, 48), (-135, 58), (-150, 60), (-165, 60)],
    'grenlandiya': [(-73, 78), (-60, 82), (-30, 83), (-20, 75), (-22, 70), (-40, 65), (-48, 61), (-55, 68), (-70, 76)],
    'j_amerika': [(-80, 9), (-72, 12), (-62, 10), (-52, 5), (-50, 0), (-45, -3), (-35, -6), (-39, -14), (-41, -22), (-48, -26), (-53, -34), (-58, -38), (-65, -41), (-66, -47), (-69, -52), (-72, -54), (-74, -48), (-73, -40), (-71, -30), (-70, -18), (-76, -14), (-81, -5), (-80, 2)],
    'yevroosiyo': [(-9, 37), (-9, 43), (-2, 43.5), (-1, 46), (-5, 48), (2, 51), (5, 53), (8, 54), (9, 57), (11, 56), (12, 54), (20, 55), (22, 58), (28, 60), (21, 61), (22, 66), (28, 70), (41, 67), (44, 68), (60, 69), (70, 73), (80, 73), (105, 77), (113, 74), (130, 71), (150, 71), (170, 69), (180, 66), (177, 62), (163, 59), (156, 51), (143, 59), (137, 54), (141, 48), (135, 43), (130, 42), (129, 35), (126, 35), (125, 40), (121, 40), (119, 37), (122, 31), (120, 26), (110, 21), (108, 16), (109, 11), (105, 9), (101, 13), (100, 7), (103, 1), (98, 8), (98, 16), (94, 18), (92, 22), (88, 22), (80, 15), (77, 8), (73, 17), (70, 21), (67, 25), (61, 25), (57, 26), (50, 30), (48, 29), (51, 25), (56, 26), (59, 22), (55, 17), (44, 12), (43, 14), (39, 21), (35, 28), (34, 31), (35, 34), (36, 36), (30, 36), (27, 37), (26, 40), (23, 38), (22, 37), (19, 41), (16, 38), (12, 42), (8, 44), (3, 43), (-1, 38), (-5, 36)],
    'afrika': [(-17, 21), (-16, 28), (-10, 30), (-6, 36), (10, 37), (11, 33), (20, 31), (32, 31), (34, 28), (38, 19), (43, 12), (51, 12), (48, 5), (40, -3), (40, -15), (35, -24), (32, -29), (27, -34), (20, -35), (17, -30), (12, -17), (13, -6), (9, 3), (5, 5), (-8, 4), (-13, 8), (-17, 14)],
    'avstraliya': [(114, -22), (122, -18), (130, -12), (137, -12), (142, -11), (146, -19), (153, -26), (151, -34), (146, -39), (138, -35), (130, -32), (116, -35), (114, -26)],
    'antarktida': [(-180, -70), (-120, -73), (-60, -66), (0, -70), (60, -67), (120, -66), (180, -70), (180, -90), (-180, -90)],
}
ISLANDS = [
    [(-5, 50), (1, 51), (2, 53), (-2, 57), (-5, 58), (-6, 55)],
    [(130, 31), (135, 34), (141, 37), (142, 43), (140, 41), (136, 36)],
    [(44, -25), (47, -25), (50, -15), (49, -12), (44, -17)],
    [(95, 5), (104, -2), (106, -6), (98, 0)],
    [(109, 1), (117, 7), (119, 1), (116, -4), (110, -3)],
    [(131, -1), (141, -3), (150, -10), (141, -9)],
    [(172, -34), (178, -38), (174, -41), (167, -46), (170, -44)],
]

UZB = [(56, 45.1), (58.5, 45.5), (61.2, 44.6), (62.5, 43.5), (64.8, 43.2), (66, 42.1), (68, 41.2), (69.5, 42.2), (71.2, 42.8), (72.6, 41.5), (73.1, 40.8), (71.6, 40.2), (70.6, 40.2), (70.7, 39.6), (69.2, 39.5), (68, 38.3), (67.8, 37.2), (66.5, 37.4), (65.5, 37.6), (64.5, 38.8), (62.7, 39.9), (61.4, 41.3), (60, 41.3), (56.8, 41.3), (55.9, 43.5)]


def world(title, overlay=None, bbox=(-180, 180, -90, 90), hl=None, labels=None, points=None, grid=False, legend=None, uzb=None, w=W, h=H):
    """Sxematik xarita. hl: {'afrika': rang}; labels: [(lon, lat, matn)]; points: [(lon, lat, matn)];
    overlay: P(lon, lat) -> (x, y) funksiyasini qabul qiluvchi funksiya."""
    x0, x1, y0, y1 = bbox
    pw, ph = w - 30, h - 80
    sc = min(pw / (x1 - x0), ph / (y1 - y0))
    ow, oh = (x1 - x0) * sc, (y1 - y0) * sc
    ox, oy = (w - ow) / 2, 44 + (ph - oh) / 2
    P = lambda lon, lat: (ox + (lon - x0) * sc, oy + (y1 - lat) * sc)
    out = [f'<clipPath id="cp"><rect x="{ox:.1f}" y="{oy:.1f}" width="{ow:.1f}" height="{oh:.1f}" rx="8"/></clipPath>', ARROW_DEF,
           f'<rect x="{ox:.1f}" y="{oy:.1f}" width="{ow:.1f}" height="{oh:.1f}" rx="8" fill="{SEA}"/>', '<g clip-path="url(#cp)">']
    if grid:
        for lat in range(-60, 90, 30):
            a, b = P(x0, lat), P(x1, lat)
            out.append(line(a[0], a[1], b[0], b[1], '#ffffff', 1, '3 3'))
        for lon in range(-150, 180, 30):
            a, b = P(lon, y0), P(lon, y1)
            out.append(line(a[0], a[1], b[0], b[1], '#ffffff', 1, '3 3'))
    for name, pts in CONT.items():
        out.append(poly([P(*p) for p in pts], (hl or {}).get(name, LAND), '#94a68a', 1))
    for pts in ISLANDS:
        out.append(poly([P(*p) for p in pts], LAND, '#94a68a', 1))
    if uzb:
        out.append(poly([P(*p) for p in UZB], uzb, '#166534', 2))
    if overlay:
        out.append(overlay(P))
    out.append('</g>')
    big = ow > 400
    for lon, lat, txt in (labels or []):
        x, y = P(lon, lat)
        out.append(T(x, y, txt, 12 if big else 13, INK, weight='700'))
    for lon, lat, txt in (points or []):
        x, y = P(lon, lat)
        out.append(circle(x, y, 4, '#ef4444', '#fff', 1.5))
        out.append(T(x + 7, y + 4, txt, 11, INK, anchor='start', weight='600'))
    for i, (col, txt) in enumerate(legend or []):
        xx, yy = 30 + i * 160, h - 18
        out.append(box(xx, yy - 10, 14, 14, col, '#94a3b8', rx=3))
        out.append(T(xx + 20, yy + 2, txt, 11, INK, anchor='start'))
    return svg(title, ''.join(out), w, h)


def write(path, s):
    with open(path, 'w', encoding='utf-8') as f:
        f.write(s)
