"""afterword_en.py <code>...: typeset the English afterword (后记) of each volume, a hand translation: the paragraphs
every volume shares (written once, so all twelve read alike) and each volume's own paragraphs (its chief editors, the
children and teachers who lent their work, the contact details) from afterword_vols.json. The afterword page of the
Chinese edition is vector outlines the pipeline cannot read, so strip_page2.py puts this page in its place.
Writes $BNU_WORK/afterword/final_<code>.pdf, a white page the size of the original, the text at one size relative to
the page in every volume (8.55 pt on a 522 pt page, as delivered)."""
import html
import json
import sys
from pathlib import Path

import pymupdf

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import AFTERWORD, source_pdf  # noqa: E402

from mathtrans.layout import page_css  # noqa: E402
from mathtrans.models import Lang  # noqa: E402

SHARED = [
    "The Compulsory Education Textbooks (Beijing Normal University Edition) were written by many heads and core members "
    "of the groups that drew up the national curriculum standards for basic education, together with subject experts, "
    "education experts, psychologists and master teachers. They rest on solid research and advanced educational ideas, and "
    "offer high-quality writing and professional service. The textbooks strive to reflect the spirit of the national "
    "curriculum standards for basic education, make use of many kinds of information resources, show the latest progress in "
    "each subject where appropriate, and stress the use of knowledge, skills and ways of thinking in real life. They stay "
    "close to students' lives, pay attention to how students learn, meet their different learning needs and promote the "
    "all-round development of every student.",
    "The Compulsory Education Textbooks (Beijing Normal University Edition) · Mathematics (Grades 1–6), also known as the "
    "New Century Primary School Mathematics Textbooks, fully embody the basic ideas of the new century's reform of the "
    "mathematics curriculum, with the healthy growth of children as their fundamental aim. This is the 4th edition of the "
    "New Century Primary School Mathematics Textbooks. Building on the strengths of the first three editions, it has been "
    "fully revised in accordance with the Mathematics Curriculum Standards for Compulsory Education (2011 Edition).",
    "The new edition has the following distinctive features. Its basic form of presentation is “a situation plus a "
    "series of questions”, which seeks to make the unfolding of the content, the students’ learning, the teachers’ "
    "teaching and the reaching of the curriculum goals one whole, good for learning and for teaching, so that students "
    "keep going through the process of thinking a problem through “from beginning to end”. It seeks to give students "
    "realistic, interesting and challenging learning materials, to give them time and space to explore and to share their "
    "ideas, to show how mathematical knowledge is formed and used, and to meet the needs of different students.",
    "The aim is for students to: appreciate the close links between mathematics, nature and human society; gain the basic "
    "knowledge, basic skills, basic ideas and basic experience of activities that they need and that suit their age; develop "
    "the ability to find and pose problems and to analyse and solve them; understand the value of mathematics, become more "
    "interested in learning it and more confident of learning it well; and gain a first sense of innovation and a "
    "scientific attitude.",
    "The chief editors of the New Century Primary School Mathematics Textbooks are Liu Jian, Kong Qiping and Zhang Dan. The "
    "other members of the writing group are Hu Guangti, Liu Keqin, Wang Yong, Tao Wenzhong, Wang Mingming, Zhu Dejiang, "
    "Chen Xiaomei, Zhang Hong, Qian Shouwang, He Fengbo, Hua Yinglong, Huang Lihua, Zhao Yanhui, Li Tie’an, Wei Huinü, "
    "Zhu Yuhong, Ren Jingye and Hou Huiying.",
]
SIGN = "Beijing Normal University Press"
SWAPPED_ORDER = {"g2_1"}  # this volume prints the first six names of the writing group in another order
TEXT_PT_PER_PAGE_PT = 8.55 / 521.57
vols = json.load(open(Path(__file__).resolve().parent / "afterword_vols.json", encoding="utf-8"))


def texts_of(code):
    texts = SHARED + vols[code]
    if code in SWAPPED_ORDER:
        texts = texts[:4] + [texts[4].replace("Hu Guangti, Liu Keqin, Wang Yong, Tao Wenzhong, Wang Mingming, Zhu Dejiang",
                                              "Hu Guangti, Wang Yong, Tao Wenzhong, Liu Keqin, Zhu Dejiang, Wang Mingming")] + texts[5:]
        assert texts[4] != SHARED[4]
    return [t.replace("'", "\u2019") for t in texts]  # one kind of apostrophe throughout


def html_of(texts, f):
    """the page at text size 10.5 pt x f (title, gaps and indents scaled alike)"""
    pt = lambda v: f"{v * f:.2f}pt"  # noqa: E731
    parts = [f'<h1 style="text-align:center;font-size:{pt(20)};font-weight:bold;margin:0 0 {pt(12)} 0">Afterword</h1>']
    parts += [f'<p style="text-indent:2em;text-align:left;margin:0 0 {pt(4.5)} 0;line-height:1.25;font-size:{pt(10.5)}">'
              f'{html.escape(t)}</p>' for t in texts]
    parts.append(f'<p style="text-align:right;margin:{pt(14)} 0 0 0;font-size:{pt(10.5)}">{SIGN}</p>')
    return "".join(parts)


def body_box(rect):
    m = 50 * rect.width / 521.6  # the same margins, relative to the page, on every volume
    return pymupdf.Rect(m, 60 * rect.height / 737, rect.width - m, rect.height - 40 * rect.height / 737)


css, archive = page_css(Lang.EN)
AFTERWORD.mkdir(parents=True, exist_ok=True)
for code in sys.argv[1:]:
    src = pymupdf.open(str(source_pdf(code)))
    rect = src[src.page_count - 1].rect
    out = pymupdf.open()
    page = out.new_page(width=rect.width, height=rect.height)
    f = TEXT_PT_PER_PAGE_PT * rect.width / 10.5
    spare, scale = page.insert_htmlbox(body_box(rect), html_of(texts_of(code), f), css=css, archive=archive, scale_low=1)
    assert spare >= 0 and scale == 1, (code, spare, scale)
    out.save(str(AFTERWORD / f"final_{code}.pdf"), garbage=3, deflate=True)
    print(code, f"text {10.5 * f:.2f}pt on a {rect.width:.0f}pt page, spare {spare:.0f}pt")
