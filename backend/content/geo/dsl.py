# -*- coding: utf-8 -*-
import zlib


def _h(s):
    return zlib.crc32(s.encode('utf-8'))


def mcq(q):
    text, right, *wrong = q
    assert len(wrong) == 3 and len({right, *wrong}) == 4, text
    ci = _h(text) % 4
    opts = list(wrong)
    opts.insert(ci, right)
    return {'question': text, 'options': opts, 'correct_index': ci}


def topic(n, key, title, goals, blocks, facts, summary, test, bank, gallery=None, extra=None):
    """blocks: [(sarlavha, matn)] yoki [(sarlavha, matn, rasm_nomi, izoh)]; gallery: [(rasm_nomi, izoh, savol_tuple)]"""
    assert len(test) >= 5, key
    seen, b = {x[0] for x in test}, []
    for q in bank:
        if q[0] in seen:
            continue
        seen.add(q[0])
        b.append(mcq(q))
    bl = []
    for it in blocks:
        d = {'heading': it[0], 'pages': [], 'text': it[1]}
        if len(it) > 3 and it[2]:
            d['image'] = {'src': f'/geo/{it[2]}.svg', 'caption': it[3]}
        bl.append(d)
    expl = {'layout': 'geo', 'goals': goals, 'blocks': bl, 'key_facts': [{'fact': f} for f in facts], 'summary': summary}
    if gallery:
        expl['gallery'] = [{'src': f'/geo/{g[0]}.svg', 'caption': g[1], **({'question': mcq(g[2])} if len(g) > 2 and g[2] else {})} for g in gallery]
    if extra:
        expl.update(extra)
    t = {'key': key, 'title': title, 'start_page': n, 'end_page': n, 'explanation': expl, 'test': [mcq(q) for q in test]}
    return t, b


# ---- fanga xos mashqlar uchun yordamchilar (units/<bo'lim>_x.py ichida ishlatiladi) ----
def F(name, formula, note=''):
    return {'name': name, 'formula': formula, **({'note': note} if note else {})}


def W(problem, steps, answer=''):
    return {'problem': problem, 'steps': steps, **({'answer': answer} if answer else {})}


def P(question, answer, hint='', solution='', unit='', fmt=''):
    d = {'question': question, 'answer': answer}
    for k, v in (('hint', hint), ('solution', solution), ('unit', unit), ('format', fmt)):
        if v:
            d[k] = v
    return d


def ORD(prompt, lines, mono=False):
    return {'type': 'order', 'prompt': prompt, 'words': lines, **({'mono': True} if mono else {})}


def TR(code, question, answer, explanation='', title='', lines=1):
    d = {'code': code, 'question': question, 'answer': answer}
    for k, v in (('explanation', explanation), ('title', title)):
        if v:
            d[k] = v
    if lines > 1:
        d['lines'] = lines
    return d


def MT(*pairs):
    return [{'left': a, 'right': b} for a, b in pairs]
