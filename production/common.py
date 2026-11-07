"""Shared settings of the production run that translates the twelve 北师大版 primary maths volumes into English.

Everything a run makes lives under WORK (env BNU_WORK, default /tmp/piptest/real):
  books/<code>.pdf              the scanned Chinese source (from the owner's Google Drive)
  books/out_<code>/             stage-1 pipeline output: segments_base.json (pristine), segments.json (corrected),
                                output.pdf (current render), final.pdf (page 2 left out, English afterword)
  proof/<code>/                 corrections (corr_*.json, applied in file-time order, the latest wins), proof pack
  afterword/                    the typeset English afterword pages
  previews/                     preview and try renders
  deliver/                      compact copies for chat delivery
The corrections are the valuable part: save_state.sh pushes proof/ to the work-state branch."""
import os
from pathlib import Path

WORK = Path(os.environ.get("BNU_WORK", "/tmp/piptest/real"))
BOOKS = WORK / "books"
PROOF = WORK / "proof"
PREVIEWS = WORK / "previews"
DELIVER = WORK / "deliver"
AFTERWORD = WORK / "afterword"
REPO = Path(__file__).resolve().parent.parent

CODES = ["g1_1", "g1_2", "g2_1", "g2_2", "g3_1", "g3_2", "g4_1", "g4_2", "g5_1", "g5_2", "g6_1", "g6_2"]
TITLES = {"g1_1": "一年级上册", "g1_2": "一年级下册", "g2_1": "二年级上册", "g2_2": "二年级下册",
          "g3_1": "三年级上册", "g3_2": "三年级下册", "g4_1": "四年级上册", "g4_2": "四年级下册",
          "g5_1": "五年级上册", "g5_2": "五年级下册", "g6_1": "六年级上册", "g6_2": "六年级下册"}
DRIVE_IDS = {"g1_1": "1Rk5A_5MSypSedvlO2i31J3ILtYSr0UY3", "g1_2": "1D6-Oz_SX37HWbVhkuE4lCEYkV2uNAqll",
             "g2_1": "1xsKpujM5vcaMDAT-fY2C75MHuCBzETc7", "g2_2": "1n-heogAyybBKHP9NDyIWVOAh1oMhF79q",
             "g3_1": "1HxSxZ658silqD8Lby4SLvk3khCRZrheZ", "g3_2": "1Q8EKKMoDigQHSp1x8AV7Y_VhK4UOaaDb",
             "g4_1": "1duCvbEEmSmdIg8HRA5WfYkNY1MIj1V4m", "g4_2": "1J2aKufbQnrBqD2qcLAzVBJjANeLs6zms",
             "g5_1": "1-w38TFZ3YNj5HqRQAAKGHy26XaxE5kSb", "g5_2": "1Bjc_bRzIvkA7T9O3_4j7d8oc3XR2GwZG",
             "g6_1": "1b5yv6axrw4TlWtDRr8errDdEtYRBrReO", "g6_2": "1wKmoE4JdWQF0HNRNHuau0gQdJ2EJeb-U"}


def grade_volume(code: str) -> tuple[int, int]:
    return int(code[1]), int(code[3])


def pdf_name(code: str) -> str:
    g, v = grade_volume(code)
    return f"Mathematics Grade {g} Volume {v}.pdf"


def report_name(code: str) -> str:
    g, v = grade_volume(code)
    return f"Mathematics Grade {g} Volume {v} - QA report.md"


def out_dir(code: str) -> Path:
    return BOOKS / f"out_{code}"


def proof_dir(code: str) -> Path:
    return PROOF / code


def source_pdf(code: str) -> Path:
    return BOOKS / f"{code}.pdf"


def final_page_of(source_index: int) -> int | None:
    """Index in the delivered book of a source page (page 2, index 1, is left out of the English book)."""
    if source_index == 1:
        return None
    return source_index if source_index == 0 else source_index - 1


def reading_order(items: list, box) -> list:
    """``items`` in reading order: rows from the top (lines whose centres lie within half a line height of each
    other are one row), left to right within a row. ``box(item)`` gives (x0, y0, x1, y1). Used both for the lines a
    proof pack lists and for the lines a split sets its texts on, so the two always agree."""
    rows: list[list] = []
    for it in sorted(items, key=lambda i: (box(i)[1] + box(i)[3]) / 2):
        x0, y0, x1, y1 = box(it)
        c, h = (y0 + y1) / 2, y1 - y0
        if rows:
            r0, r1 = box(rows[-1][0])[1], box(rows[-1][0])[3]
            if abs(c - (r0 + r1) / 2) <= 0.5 * min(h, r1 - r0):
                rows[-1].append(it)
                continue
        rows.append([it])
    return [it for row in rows for it in sorted(row, key=lambda i: box(i)[0])]
