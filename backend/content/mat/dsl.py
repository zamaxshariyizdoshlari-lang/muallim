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


def topic(n, key, title, goals, blocks, facts, summary, test, bank):
    """blocks: [(sarlavha, matn)], facts: [str], test/bank: [(savol, to'g'ri, xato1, xato2, xato3)]"""
    assert len(test) >= 5, key
    seen, b = {x[0] for x in test}, []
    for q in bank:
        if q[0] in seen:
            continue
        seen.add(q[0])
        b.append(mcq(q))
    t = {
        'key': key, 'title': title, 'start_page': n, 'end_page': n,
        'explanation': {
            'goals': goals,
            'blocks': [{'heading': h, 'pages': [], 'text': x} for h, x in blocks],
            'key_facts': [{'fact': f} for f in facts],
            'summary': summary,
        },
        'test': [mcq(q) for q in test],
    }
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
