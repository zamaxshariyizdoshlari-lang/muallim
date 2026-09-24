from pypdf import PdfReader


class NoTextLayerError(Exception):
    """PDF skan qilingan (matn qatlami yo'q) bo'lsa ko'tariladi."""


def extract_pages(file_path):
    """PDF faylni bet-bet o'qib, [(page_number, text), ...] qaytaradi.

    Matn qatlami umuman topilmasa NoTextLayerError ko'taradi, chunki bunday
    hollarda foydalanuvchiga OCR kerakligini alohida aytish kerak.
    """
    reader = PdfReader(file_path)
    pages = []
    has_any_text = False

    for i, page in enumerate(reader.pages, start=1):
        text = (page.extract_text() or '').strip()
        if text:
            has_any_text = True
        pages.append((i, text))

    if not has_any_text:
        raise NoTextLayerError(
            "Ushbu PDF'da matn qatlami topilmadi (skan qilingan hujjat bo'lishi mumkin). "
            "Iltimos, matnli PDF yuklang."
        )

    return pages
