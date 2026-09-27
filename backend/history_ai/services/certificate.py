from fpdf import FPDF


def _latin1(text):
    """Standart PDF shriftlari faqat latin-1 ni qo'llaydi: o'zbekcha ʻ/ʼ/’ ni oddiy ' ga almashtiramiz."""
    for ch in ('ʻ', 'ʼ', '’', '‘', '`'):
        text = text.replace(ch, "'")
    return text.encode('latin-1', 'replace').decode('latin-1')


def build_certificate_pdf(student_name, book_title, issued_date, verify_url=None):
    """Sertifikat PDF (landshaft A4) baytlarini qaytaradi.

    `verify_url` berilsa, pastki qismga sertifikatni tekshirish havolasi yoziladi.
    """
    pdf = FPDF(orientation='L', unit='mm', format='A4')
    pdf.add_page()
    pdf.set_auto_page_break(False)

    pdf.set_draw_color(79, 70, 229)
    pdf.set_line_width(2)
    pdf.rect(10, 10, 277, 190)
    pdf.set_line_width(0.5)
    pdf.rect(15, 15, 267, 180)

    pdf.set_text_color(79, 70, 229)
    pdf.set_font('Helvetica', 'B', 40)
    pdf.set_xy(0, 40)
    pdf.cell(297, 20, 'SERTIFIKAT', align='C')

    pdf.set_text_color(60, 60, 60)
    pdf.set_font('Helvetica', '', 16)
    pdf.set_xy(0, 75)
    pdf.cell(297, 10, 'Ushbu sertifikat quyidagi shaxsga beriladi:', align='C')

    pdf.set_text_color(20, 20, 20)
    pdf.set_font('Helvetica', 'B', 32)
    pdf.set_xy(0, 95)
    pdf.cell(297, 16, _latin1(student_name), align='C')

    pdf.set_text_color(60, 60, 60)
    pdf.set_font('Helvetica', '', 16)
    pdf.set_xy(20, 125)
    pdf.multi_cell(257, 9, _latin1(
        f"\"{book_title}\" darsligini to'liq o'zlashtirib, barcha mavzu testlari va "
        "yakuniy imtihonni muvaffaqiyatli topshirgani uchun."
    ), align='C')

    pdf.set_font('Helvetica', '', 14)
    pdf.set_xy(0, 170)
    footer = f"Sana: {issued_date:%d.%m.%Y}   |   Muallim"
    pdf.cell(297, 10, _latin1(footer), align='C')

    if verify_url:
        pdf.set_font('Helvetica', '', 10)
        pdf.set_text_color(120, 120, 120)
        pdf.set_xy(0, 180)
        pdf.cell(297, 8, _latin1(f"Sertifikatni tekshirish: {verify_url}"), align='C')

    return bytes(pdf.output())
