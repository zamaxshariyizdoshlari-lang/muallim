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
            'blocks': [{'heading': h, 'pages': [n], 'text': x} for h, x in blocks],
            'key_facts': [{'fact': f} for f in facts],
            'summary': summary,
        },
        'test': [mcq(q) for q in test],
    }
    return t, b
