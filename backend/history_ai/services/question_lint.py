"""Savol sifati tekshiruvi (lint): test savollaridagi odatiy kamchiliklarni topadi.

Tekshiriladi: to'g'ri javob doim eng uzun variant bo'lib qolishi, "barchasi/hech biri" kabi variantlar,
takroriy savollar, variantlar uzunligidagi keskin farq, javob o'rinlari taqsimoti, daraja taqsimoti va
"Nega?" izohlari qamrovi. Natija kitob bo'yicha umumiy ko'rsatkichlar va mavzu bo'yicha ogohlantirishlar.
"""
import re
from collections import Counter

ALL_OF_THE_ABOVE = re.compile(r"\b(barchasi|hammasi|hech biri|yuqoridagilar|yuqoridagi barcha)\b", re.I)
LONG_BIAS_LIMIT = 0.45  # to'g'ri javob eng uzun variant bo'lgan savollar ulushi shundan oshsa - ogohlantirish
RATIO_LIMIT = 3.0       # eng uzun / eng qisqa variant uzunligi nisbati shundan oshsa - ogohlantirish


def _norm(text):
    return re.sub(r'\W+', ' ', text.lower()).strip()


def lint_questions(topics):
    """topics: [(key, title, [question, ...])]. Qaytaradi: {'summary': {...}, 'warnings': [...]}."""
    warnings = []
    total = 0
    longest_correct = 0
    positions = Counter()
    levels = Counter()
    with_explanation = 0
    seen = {}
    per_topic_long = {}

    for key, _title, questions in topics:
        long_here = 0
        for qi, q in enumerate(questions):
            total += 1
            opts, ci = q['options'], q['correct_index']
            lens = [len(o) for o in opts]
            positions[ci] += 1
            levels[q.get('level') or '-'] += 1
            with_explanation += bool(q.get('explanation'))
            where = f"{key}[{qi}]"

            if lens[ci] == max(lens) and lens.count(max(lens)) == 1:
                longest_correct += 1
                long_here += 1
            if max(lens) / max(1, min(lens)) > RATIO_LIMIT and len(opts) > 2:
                warnings.append((where, f"variantlar uzunligi keskin farq qiladi (x{max(lens) / max(1, min(lens)):.1f})"))
            if any(ALL_OF_THE_ABOVE.search(o) for o in opts):
                warnings.append((where, "'barchasi/hech biri' tipidagi variant bor"))
            norm_q = _norm(q['question'])
            if norm_q in seen:
                warnings.append((where, f"savol takrorlangan ({seen[norm_q]})"))
            seen.setdefault(norm_q, where)
            if not q.get('page') and q.get('level'):
                warnings.append((where, "bet raqami yo'q"))
        per_topic_long[key] = (long_here, len(questions))

    for key, (n, m) in per_topic_long.items():
        if m >= 10 and n / m > LONG_BIAS_LIMIT:
            warnings.append((key, f"to'g'ri javob {n}/{m} savolda eng uzun variant (odatiy bo'lmagan nishon)"))

    n_opts = 4
    summary = {
        'questions': total,
        'longest_correct_share': round(longest_correct / total, 3) if total else 0,
        'answer_positions': {str(k): positions[k] for k in sorted(positions)},
        'levels': dict(levels),
        'explanation_share': round(with_explanation / total, 3) if total else 0,
        'expected_position_share': round(1 / n_opts, 2),
    }
    return {'summary': summary, 'warnings': warnings}
