# -*- coding: utf-8 -*-
"""Turk tili B2 uchun yordamchi: ixcham yozuvni book.json/exam_bank.json formatiga aylantiradi.

Savollarda BIRINCHI variant - to'g'ri javob; qurilishda aralashtiriladi (deterministik).
"""
import random
import zlib


def mcq(q, opts):
    opts = list(opts)
    rng = random.Random(zlib.crc32(q.encode('utf-8')))
    order = list(range(len(opts)))
    rng.shuffle(order)
    return {'question': q, 'options': [opts[i] for i in order], 'correct_index': order.index(0)}


def topic(key, title, sp, ep, goals, blocks, facts, vocab, reading, listening, practice,
          writing, speaking, test, bank):
    practice_out = []
    for p in practice:
        if p[0] == 'c':
            m = mcq(p[1], p[2])
            practice_out.append({'type': 'choice', 'prompt': m['question'], 'options': m['options'],
                                 'correct_index': m['correct_index']})
        else:
            practice_out.append({'type': 'order', 'prompt': p[1], 'words': p[2]})
    t = {
        'key': key, 'title': title, 'start_page': sp, 'end_page': ep,
        'explanation': {
            'goals': goals,
            'blocks': [{'heading': h, 'text': x} for h, x in blocks],
            'key_facts': [{'fact': f} for f in facts],
            'vocabulary': [
                {'tr': v[0], 'uz': v[1], 'example_tr': v[2], 'example_uz': v[3]} for v in vocab
            ],
            'reading': {'title': reading[0], 'text': reading[1],
                        'questions': [mcq(q, o) for q, o in reading[2]]},
            'listening': {'dialogue': [{'speaker': s, 'text': x} for s, x in listening[0]],
                          'questions': [mcq(q, o) for q, o in listening[1]]},
            'sentence_practice': practice_out,
            'writing_prompt': {'instruction': writing[0], 'sample_answer': writing[1]},
            'speaking_prompt': {'sentences': speaking},
        },
        'test': [mcq(q, o) for q, o in test],
    }
    return t, [mcq(q, o) for q, o in bank]
