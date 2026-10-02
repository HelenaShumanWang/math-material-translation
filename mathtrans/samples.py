"""Generate small but realistic sample textbooks (used by tests, demos and the CLI)."""
from __future__ import annotations

import io
from pathlib import Path

from PIL import Image, ImageDraw

from .fonts import pil_font
from .models import Lang

_TEXTS = {
    "zh": {
        "title": "第一章 勾股定理",
        "section": "1.1 探索勾股定理",
        "para1": "在直角三角形中，两条直角边的平方和等于斜边的平方。如果直角三角形的两条直角边长分别为 a 和 b，斜边长为 c，那么 a²+b²=c²。这就是著名的勾股定理。",
        "caption": "图 1-1 直角三角形中的边长关系",
        "example": "例题 1 已知直角三角形的两条直角边分别为 3 cm 和 4 cm，求斜边的长度。",
        "solution": "解：由勾股定理得 c² = 3² + 4² = 9 + 16 = 25，所以 c = 5 cm。",
        "theorem": "定理：直角三角形两直角边的平方和等于斜边的平方。",
        "exercises": "练习 1.1",
        "ex1": "1. 在 Rt△ABC 中，∠C = 90°，AC = 6，BC = 8，求 AB 的长。",
        "ex2": "2. 一个直角三角形的斜边长为 13，一条直角边长为 5，求另一条直角边的长。",
        "ex3": "3. 判断：边长为 7、24、25 的三角形是直角三角形吗？",
        "think": "思考：如图所示，用四个全等的直角三角形可以拼成一个大正方形，中间留下一个小正方形。请利用面积关系证明勾股定理。",
        "img_label": "斜边 c",
        "img_title": "图 1-1",
        "img2_label": "面积 = c²",
        "img2_title": "小正方形",
        "footer": "第 2 页",
    },
    "en": {
        "title": "Chapter 1 The Pythagorean Theorem",
        "section": "1.1 Exploring the Pythagorean Theorem",
        "para1": "In a right triangle, the sum of the squares of the two legs equals the square of the hypotenuse. If the legs have lengths a and b and the hypotenuse has length c, then a²+b²=c². This is the famous Pythagorean theorem.",
        "caption": "Figure 1-1 Side lengths in a right triangle",
        "example": "Example 1 The legs of a right triangle are 3 cm and 4 cm. Find the length of the hypotenuse.",
        "solution": "Solution: By the Pythagorean theorem, c² = 3² + 4² = 9 + 16 = 25, so c = 5 cm.",
        "theorem": "Theorem: In a right triangle the sum of the squares of the legs equals the square of the hypotenuse.",
        "exercises": "Exercises 1.1",
        "ex1": "1. In right triangle ABC, ∠C = 90°, AC = 6 and BC = 8. Find AB.",
        "ex2": "2. The hypotenuse of a right triangle is 13 and one leg is 5. Find the other leg.",
        "ex3": "3. Decide: is a triangle with sides 7, 24 and 25 a right triangle?",
        "think": "Think: as shown in the figure, four congruent right triangles form a large square with a small square in the middle. Use areas to prove the Pythagorean theorem.",
        "img_label": "hypotenuse c",
        "img_title": "Figure 1-1",
        "img2_label": "Area = c²",
        "img2_title": "small square",
        "footer": "Page 2",
    },
}

_TEXTS["ja"] = dict(_TEXTS["zh"], **{
    "title": "第1章 三平方の定理", "section": "1.1 三平方の定理を調べよう",
    "para1": "直角三角形では、直角をはさむ二辺の平方の和は斜辺の平方に等しい。二辺の長さを a と b、斜辺の長さを c とすると、a²+b²=c² が成り立つ。これが三平方の定理である。",
    "caption": "図 1-1 直角三角形の辺の関係", "example": "例題 1 直角三角形の二辺が 3 cm と 4 cm のとき、斜辺の長さを求めよ。",
    "solution": "解：三平方の定理より c² = 3² + 4² = 25、よって c = 5 cm。",
    "theorem": "定理：直角三角形の二辺の平方の和は斜辺の平方に等しい。", "exercises": "練習 1.1",
    "ex1": "1. 直角三角形 ABC で ∠C = 90°、AC = 6、BC = 8 のとき AB を求めよ。",
    "ex2": "2. 斜辺が 13、一辺が 5 の直角三角形のもう一辺を求めよ。", "ex3": "3. 辺が 7、24、25 の三角形は直角三角形か。",
    "think": "考えよう：図のように 4 つの合同な直角三角形で大きな正方形を作ると、中央に小さな正方形ができる。面積を使って三平方の定理を証明しなさい。",
    "img_label": "斜辺 c", "img_title": "図 1-1", "img2_label": "面積 = c²", "img2_title": "小さな正方形", "footer": "2 ページ",
})
_TEXTS["ko"] = dict(_TEXTS["zh"], **{
    "title": "제1장 피타고라스 정리", "section": "1.1 피타고라스 정리 탐구",
    "para1": "직각삼각형에서 두 변의 제곱의 합은 빗변의 제곱과 같다. 두 변의 길이를 a와 b, 빗변의 길이를 c라 하면 a²+b²=c²이다. 이것이 피타고라스 정리이다.",
    "caption": "그림 1-1 직각삼각형의 변의 길이", "example": "예제 1 직각삼각형의 두 변이 3 cm, 4 cm일 때 빗변의 길이를 구하시오.",
    "solution": "풀이: 피타고라스 정리에 의해 c² = 3² + 4² = 25, 따라서 c = 5 cm이다.",
    "theorem": "정리: 직각삼각형에서 두 변의 제곱의 합은 빗변의 제곱과 같다.", "exercises": "연습 1.1",
    "ex1": "1. 직각삼각형 ABC에서 ∠C = 90°, AC = 6, BC = 8일 때 AB를 구하시오.",
    "ex2": "2. 빗변이 13, 한 변이 5인 직각삼각형의 다른 변을 구하시오.", "ex3": "3. 변이 7, 24, 25인 삼각형은 직각삼각형인가?",
    "think": "생각해 보기: 그림과 같이 합동인 직각삼각형 4개로 큰 정사각형을 만들면 가운데에 작은 정사각형이 생긴다. 넓이를 이용하여 피타고라스 정리를 증명하시오.",
    "img_label": "빗변 c", "img_title": "그림 1-1", "img2_label": "넓이 = c²", "img2_title": "작은 정사각형", "footer": "2쪽",
})
_TEXTS["es"] = dict(_TEXTS["en"], **{
    "title": "Capítulo 1 El teorema de Pitágoras", "section": "1.1 Explorando el teorema de Pitágoras",
    "para1": "En un triángulo rectángulo, la suma de los cuadrados de los catetos es igual al cuadrado de la hipotenusa. Si los catetos miden a y b y la hipotenusa mide c, entonces a²+b²=c². Este es el famoso teorema de Pitágoras.",
    "caption": "Figura 1-1 Longitudes de los lados de un triángulo rectángulo",
    "example": "Ejemplo 1 Los catetos de un triángulo rectángulo miden 3 cm y 4 cm. Calcula la longitud de la hipotenusa.",
    "solution": "Solución: Por el teorema de Pitágoras, c² = 3² + 4² = 9 + 16 = 25, así que c = 5 cm.",
    "theorem": "Teorema: En un triángulo rectángulo la suma de los cuadrados de los catetos es igual al cuadrado de la hipotenusa.",
    "exercises": "Ejercicios 1.1", "ex1": "1. En el triángulo rectángulo ABC, ∠C = 90°, AC = 6 y BC = 8. Calcula AB.",
    "ex2": "2. La hipotenusa de un triángulo rectángulo mide 13 y un cateto mide 5. Calcula el otro cateto.",
    "ex3": "3. Decide: ¿es un triángulo de lados 7, 24 y 25 un triángulo rectángulo?",
    "think": "Piensa: como muestra la figura, cuatro triángulos rectángulos congruentes forman un cuadrado grande con un cuadrado pequeño en el centro. Usa las áreas para demostrar el teorema de Pitágoras.",
    "img_label": "hipotenusa c", "img_title": "Figura 1-1", "img2_label": "Área = c²", "img2_title": "cuadrado pequeño", "footer": "Página 2",
})
_TEXTS["pt"] = dict(_TEXTS["en"], **{
    "title": "Capítulo 1 O teorema de Pitágoras", "section": "1.1 Explorando o teorema de Pitágoras",
    "para1": "Em um triângulo retângulo, a soma dos quadrados dos catetos é igual ao quadrado da hipotenusa. Se os catetos medem a e b e a hipotenusa mede c, então a²+b²=c². Este é o famoso teorema de Pitágoras.",
    "caption": "Figura 1-1 Comprimentos dos lados de um triângulo retângulo",
    "example": "Exemplo 1 Os catetos de um triângulo retângulo medem 3 cm e 4 cm. Calcule o comprimento da hipotenusa.",
    "solution": "Solução: Pelo teorema de Pitágoras, c² = 3² + 4² = 9 + 16 = 25, logo c = 5 cm.",
    "theorem": "Teorema: Em um triângulo retângulo a soma dos quadrados dos catetos é igual ao quadrado da hipotenusa.",
    "exercises": "Exercícios 1.1", "ex1": "1. No triângulo retângulo ABC, ∠C = 90°, AC = 6 e BC = 8. Calcule AB.",
    "ex2": "2. A hipotenusa de um triângulo retângulo mede 13 e um cateto mede 5. Calcule o outro cateto.",
    "ex3": "3. Decida: um triângulo de lados 7, 24 e 25 é um triângulo retângulo?",
    "think": "Pense: como mostra a figura, quatro triângulos retângulos congruentes formam um quadrado grande com um quadrado pequeno no centro. Use as áreas para demonstrar o teorema de Pitágoras.",
    "img_label": "hipotenusa c", "img_title": "Figura 1-1", "img2_label": "Área = c²", "img2_title": "quadrado pequeno", "footer": "Página 2",
})


def sample_texts(lang: str) -> dict[str, str]:
    return dict(_TEXTS[Lang.parse(lang).value])


def _triangle_image(t: dict[str, str], lang: str) -> bytes:
    img = Image.new("RGB", (480, 360), "white")
    d = ImageDraw.Draw(img)
    pts = [(60, 300), (420, 300), (60, 60)]
    d.polygon(pts, fill=(214, 228, 255), outline=(31, 58, 147), width=4)
    d.rectangle([60, 270, 90, 300], outline=(31, 58, 147), width=3)
    big = pil_font(lang, 30)
    small = pil_font(lang, 26)
    d.text((40, 305), "A", fill=(0, 0, 0), font=big)
    d.text((420, 305), "B", fill=(0, 0, 0), font=big)
    d.text((40, 25), "C", fill=(0, 0, 0), font=big)
    d.text((250, 150), t["img_label"], fill=(200, 30, 30), font=small)
    d.text((200, 320), "a", fill=(0, 0, 0), font=small)
    d.text((20, 170), "b", fill=(0, 0, 0), font=small)
    d.text((170, 10), t["img_title"], fill=(60, 60, 60), font=small)
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()


def _square_image(t: dict[str, str], lang: str) -> bytes:
    img = Image.new("RGB", (400, 400), "white")
    d = ImageDraw.Draw(img)
    d.rectangle([40, 40, 360, 360], outline=(31, 58, 147), width=4, fill=(255, 246, 213))
    d.polygon([(40, 40), (240, 40), (40, 160)], fill=(214, 228, 255), outline=(31, 58, 147))
    d.polygon([(240, 40), (360, 40), (360, 240)], fill=(214, 228, 255), outline=(31, 58, 147))
    d.polygon([(360, 240), (360, 360), (160, 360)], fill=(214, 228, 255), outline=(31, 58, 147))
    d.polygon([(160, 360), (40, 360), (40, 160)], fill=(214, 228, 255), outline=(31, 58, 147))
    f = pil_font(lang, 24)
    d.text((120, 180), t["img2_label"], fill=(0, 0, 0), font=f)
    d.text((110, 215), t["img2_title"], fill=(200, 30, 30), font=f)
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()


def make_sample_pdf(path: str | Path, lang: str = "zh") -> Path:
    """Write a two-page sample textbook in ``lang`` to ``path`` and return the path."""
    import pymupdf

    lang = Lang.parse(lang).value
    t = sample_texts(lang)
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    doc = pymupdf.open()
    css_base = "* {font-family: sans-serif;} p {margin: 0;}"

    def html(rect, text, size=11, color="#000000", bold=False, align="left", lh=1.3):
        weight = "bold" if bold else "normal"
        page.insert_htmlbox(
            rect,
            f'<p style="font-size:{size}px;color:{color};font-weight:{weight};text-align:{align};line-height:{lh}">{text}</p>',
            css=css_base,
        )

    # ---------------- page 1 ----------------
    page = doc.new_page(width=595, height=842)
    html(pymupdf.Rect(60, 50, 535, 90), t["title"], size=22, color="#1f3a93", bold=True)
    html(pymupdf.Rect(60, 100, 535, 125), t["section"], size=15, color="#1f3a93", bold=True)
    html(pymupdf.Rect(60, 135, 535, 215), t["para1"], size=11)
    page.insert_image(pymupdf.Rect(80, 225, 320, 405), stream=_triangle_image(t, lang))
    html(pymupdf.Rect(80, 410, 320, 430), t["caption"], size=9, color="#555555", align="center")
    # a formula set in a Latin base font, like many textbooks do
    page.insert_text(pymupdf.Point(340, 300), "a² + b² = c²", fontsize=16, fontname="helv", color=(0.12, 0.23, 0.58))
    # example box with background
    page.draw_rect(pymupdf.Rect(60, 445, 535, 530), color=(0.95, 0.80, 0.30), fill=(1, 0.965, 0.835), width=1)
    html(pymupdf.Rect(70, 452, 525, 490), t["example"], size=11, bold=True)
    html(pymupdf.Rect(70, 492, 525, 525), t["solution"], size=11)
    # theorem box
    page.draw_rect(pymupdf.Rect(60, 550, 535, 600), color=(0.12, 0.23, 0.58), width=1.5)
    html(pymupdf.Rect(70, 558, 525, 595), t["theorem"], size=12, color="#1f3a93", bold=True)
    html(pymupdf.Rect(60, 790, 535, 810), "1", size=9, color="#888888", align="center")

    # ---------------- page 2 (two columns) ----------------
    page = doc.new_page(width=595, height=842)
    html(pymupdf.Rect(60, 50, 535, 80), t["exercises"], size=16, color="#1f3a93", bold=True)
    html(pymupdf.Rect(60, 95, 290, 145), t["ex1"], size=11)
    html(pymupdf.Rect(60, 150, 290, 200), t["ex2"], size=11)
    html(pymupdf.Rect(60, 205, 290, 255), t["ex3"], size=11)
    html(pymupdf.Rect(310, 95, 535, 190), t["think"], size=11)
    page.insert_image(pymupdf.Rect(330, 200, 510, 380), stream=_square_image(t, lang))
    html(pymupdf.Rect(60, 790, 535, 810), t["footer"], size=9, color="#888888", align="center")

    # Each insert_htmlbox call embeds its fonts again; subset and deduplicate them so
    # the sample is as small as a real textbook (about 110 KB instead of 22 MB).
    doc.subset_fonts()
    doc.save(str(path), garbage=4, deflate=True)
    doc.close()
    return path
