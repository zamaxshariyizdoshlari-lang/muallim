# -*- coding: utf-8 -*-
from dsl import F, W, P, ORD

EXTRAS = {}

EXTRAS['m5a'] = dict(
    formulas=[F("Tekislik aniqlanishi", "bir to'g'ri chiziqda yotmagan 3 nuqta", ""),
              F("Chiziqlar", "kesishadi / parallel / ayqash", ""),
              F("Perpendikulyar va og'ma", "og'ma² = perpendikulyar² + proyeksiya²", "Pifagor teoremasi"),
              F("Perpendikulyarlik alomati", "tekislikdagi ikki kesishuvchi chiziqqa perpendikulyar", "")],
    worked_examples=[
        W("Nuqtadan tekislikka og'ma 13, uning proyeksiyasi 5. Nuqtadan tekislikkacha masofa?", ["Perpendikulyar, og'ma va proyeksiya to'g'ri burchakli uchburchak tashkil etadi", "h² = 13² − 5² = 169 − 25 = 144", "h = 12"], "12"),
        W("Kubning bitta qirrasiga nechta qirra ayqash?", ["Kubda 12 qirra", "Berilgan qirraga parallel: 3; kesishuvchi: 4 (har uchida 2 tadan, jami 4)", "Qolgan: 12 − 1 − 3 − 4 = 4"], "4")],
    problems=[
        P("Nuqtadan tekislikka og'ma 13, uning proyeksiyasi 5. Perpendikulyar uzunligi?", "12", "Pifagor", "√(169 − 25) = 12"),
        P("Nuqta tekislikdan 4 sm masofada, og'ma 5 sm. Proyeksiya uzunligi?", "3", "", "√(25 − 16) = 3", unit="sm"),
        P("Kubning bitta qirrasiga nechta qirra ayqash?", "4", "12 − 1 − parallel − kesishuvchi", "4"),
        P("Bir tekislikda yotmaydigan 4 nuqtadan (har uchtasi to'g'ri chiziqda emas) nechta tekislik o'tkazish mumkin (uchtalab)?", "4", "C(4, 3)", "4 ta"),
        P("Parallel tekisliklar orasidagi masofa 6. Ularni kesuvchi 10 uzunlikdagi kesma bir tekislikdagi proyeksiyasi?", "8", "√(100 − 36)", "8"),
        P("Uchta o'zaro perpendikulyar tekislik fazoni nechta qismga bo'ladi?", "8", "Koordinata oktantlari", "8")],
    sentence_practice=[ORD("Og'ma, proyeksiya va perpendikulyar masalasini yechish", ["Perpendikulyar, og'ma va proyeksiya — to'g'ri burchakli uchburchak", "h² = 13² − 5²", "h² = 144", "h = 12"])],
)

EXTRAS['m5b'] = dict(
    formulas=[F("Prizma hajmi", "V = S_asos · H", ""),
              F("Piramida hajmi", "V = ⅓ S_asos · H", ""),
              F("To'g'ri burchakli parallelepiped", "V = abc; d = √(a² + b² + c²)", "S = 2(ab + bc + ca)"),
              F("Kub", "V = a³; S = 6a²; d = a√3", "")],
    worked_examples=[
        W("Asosi 6×6 kvadrat, balandligi 4 bo'lgan piramida hajmi?", ["S_asos = 36", "V = ⅓ · 36 · 4", "V = 48"], "48"),
        W("O'lchamlari 3, 4, 12 bo'lgan parallelepiped diagonalini toping", ["d² = 3² + 4² + 12²", "= 9 + 16 + 144 = 169", "d = 13"], "13")],
    problems=[
        P("Asos yuzi 20, balandligi 7 bo'lgan prizma hajmi?", "140", "", "20 · 7"),
        P("Asos yuzi 30, balandligi 9 bo'lgan piramida hajmi?", "90", "⅓·S·H", "30·9/3 = 90"),
        P("Qirrasi 5 bo'lgan kubning to'la sirti?", "150", "6a²", "6 · 25"),
        P("O'lchamlari 2, 3, 6 bo'lgan to'g'ri burchakli parallelepiped diagonali?", "7", "√(4 + 9 + 36)", "√49 = 7"),
        P("Muntazam to'rtburchakli piramida asos tomoni 6, apofemasi 5. Yon sirti?", "60", "½ · P · l", "½ · 24 · 5 = 60"),
        P("Qirrasi 3 bo'lgan kubning hajmi?", "27", "a³", "27")],
    sentence_practice=[ORD("Piramida hajmini topish tartibi", ["S_asos = 6 · 6 = 36", "V = ⅓ · S_asos · H", "V = ⅓ · 36 · 4", "V = 48"])],
)

EXTRAS['m5c'] = dict(
    formulas=[F("Silindr", "V = πr²H; S_yon = 2πrH", ""),
              F("Konus", "V = ⅓πr²H; l² = r² + H²; S_yon = πrl", ""),
              F("Shar", "V = 4/3 πR³; S_sfera = 4πR²", ""),
              F("Arximed nisbati", "konus : shar : silindr = 1 : 2 : 3", "r = R, H = 2R")],
    worked_examples=[
        W("r = 3, H = 4 bo'lgan konusning yasovchisi va hajmini toping", ["l² = 3² + 4² = 25 ⇒ l = 5", "V = ⅓ π r² H = ⅓ π · 9 · 4", "V = 12π"], "l = 5; V = 12π"),
        W("R = 3 bo'lgan shar hajmini toping", ["V = 4/3 · π · R³", "= 4/3 · π · 27", "= 36π"], "36π")],
    problems=[
        P("R = 3 bo'lgan shar hajmi π ning necha barobari?", "36", "", "4/3 · 27 = 36"),
        P("R = 5 bo'lgan sfera sirti π ning necha barobari?", "100", "4πR²", "4 · 25 = 100"),
        P("r = 4, H = 5 bo'lgan silindrning yon sirti π ning necha barobari?", "40", "2πrH", "2 · 4 · 5 = 40"),
        P("Konus yasovchisi 13, asos radiusi 5. Balandligi?", "12", "H² = l² − r²", "H² = 169 − 25 = 144 ⇒ H = 12"),
        P("r = 6, H = 5 bo'lgan konus hajmi π ning necha barobari?", "60", "⅓ r² H", "⅓ · 36 · 5 = 60"),
        P("Shar radiusi 2 marta oshsa, hajmi necha marta oshadi?", "8", "k³", "2³ = 8")],
    sentence_practice=[ORD("Konus hajmini topish tartibi", ["l² = r² + H² = 9 + 16 = 25", "V = ⅓ π r² H", "V = ⅓ π · 9 · 4", "V = 12π"])],
)

EXTRAS['m5d'] = dict(
    formulas=[F("Eyler formulasi", "U − Q + Y = 2", "uchlar − qirralar + yoqlar"),
              F("Kubga chizilgan shar", "ichki r = a/2; tashqi R = a√3/2", ""),
              F("Zichlik", "m = ρ · V", ""),
              F("Hajm birliklari", "1 m³ = 1000 l; 1 l = 1 dm³", "")],
    worked_examples=[
        W("Dodekaedrning 20 uchi va 30 qirrasi bor. Nechta yog'i bor?", ["Eyler: U − Q + Y = 2", "20 − 30 + Y = 2", "Y = 12"], "12"),
        W("Qirrasi 8 bo'lgan kubga ichki chizilgan sharning radiusi?", ["Ichki shar kubning har yog'iga urinadi", "Diametr = qirra = 8", "r = 4"], "4")],
    problems=[
        P("Dodekaedrning 20 uchi va 30 qirrasi bor. Yoqlari soni?", "12", "U − Q + Y = 2", "Y = 2 − 20 + 30 = 12"),
        P("Ikosaedrning 12 uchi va 30 qirrasi bor. Yoqlari soni?", "20", "Eyler formulasi", "2 − 12 + 30 = 20"),
        P("Qirrasi 8 bo'lgan kubga ichki chizilgan shar radiusi?", "4", "a/2", "4"),
        P("Qirrasi 6 bo'lgan kubga tashqi chizilgan shar radiusi √3 ning necha barobari?", "3", "R = a√3/2", "6√3/2 = 3√3"),
        P("Tubi 20×30 sm, suv balandligi 10 sm bo'lgan idishda necha litr suv bor?", "6", "V = 20·30·10 sm³", "6000 sm³ = 6 l", unit="litr"),
        P("Hajmi 150 sm³, zichligi 2 g/sm³ bo'lgan jism massasi?", "300", "m = ρV", "2 · 150 = 300", unit="g")],
    sentence_practice=[ORD("Dodekaedr yoqlari sonini topish tartibi", ["Eyler: U − Q + Y = 2", "20 − 30 + Y = 2", "Y = 2 − 20 + 30", "Y = 12"])],
)
