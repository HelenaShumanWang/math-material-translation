"""han_left.py <code> [--pages a,b] [--dpi N]: OCR the rendered English pages (out_<code>/output.pdf) and list the
Chinese still visible (lines that are only the publisher's watermark left out). One line per finding:
page (1-based), box in points, text, confidence."""
import re
import sys
import time
from pathlib import Path

import numpy as np
import pymupdf

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import out_dir  # noqa: E402

from mathtrans.ocr import RapidOcrEngine  # noqa: E402

WATERMARK = set("北京师范大学出版社")
HAN = re.compile(r"[㐀-鿿]")
code = sys.argv[1]
dpi = int(sys.argv[sys.argv.index("--dpi") + 1]) if "--dpi" in sys.argv else 150
doc = pymupdf.open(str(out_dir(code) / "output.pdf"))
pages = [int(p) - 1 for p in sys.argv[sys.argv.index("--pages") + 1].split(",")] if "--pages" in sys.argv \
    else list(range(doc.page_count))
eng = RapidOcrEngine()
t0, found, hit = time.time(), 0, set()
for i in pages:
    pix = doc[i].get_pixmap(dpi=dpi)
    a = np.frombuffer(pix.samples, np.uint8).reshape(pix.height, pix.width, pix.n)[:, :, :3]
    k = 72.0 / dpi
    for r in eng.recognize(np.ascontiguousarray(a)):
        han = HAN.findall(r.text)
        if not han or all(c in WATERMARK for c in han):
            continue
        xs, ys = [p[0] for p in r.polygon], [p[1] for p in r.polygon]
        box = [round(min(xs) * k), round(min(ys) * k), round(max(xs) * k), round(max(ys) * k)]
        print(f"page {i + 1} {box} '{r.text}' {r.confidence:.2f}", flush=True)
        found += 1
        hit.add(i)
print(f"{found} Chinese lines on {len(hit)} pages in {time.time() - t0:.0f}s")
