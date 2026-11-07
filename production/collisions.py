"""collisions.py <code> [--pages a,b]: words of different text lines that overlap on the rendered page (fragments
set over each other, labels on top of each other). Prints page (1-based), the two words and where."""
import sys
from pathlib import Path

import pymupdf

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import out_dir  # noqa: E402

code = sys.argv[1]
pdf = pymupdf.open(str(out_dir(code) / "output.pdf"))
only = {int(p) - 1 for p in sys.argv[sys.argv.index("--pages") + 1].split(",")} if "--pages" in sys.argv else None
total, pages = 0, 0
for i, page in enumerate(pdf):
    if only is not None and i not in only:
        continue
    words = page.get_text("words")
    hits = []
    for a in range(len(words)):
        wa = words[a]
        for b in range(a + 1, len(words)):
            wb = words[b]
            if (wa[5], wa[6]) == (wb[5], wb[6]):
                continue  # same line
            x0, y0 = max(wa[0], wb[0]), max(wa[1], wb[1])
            x1, y1 = min(wa[2], wb[2]), min(wa[3], wb[3])
            if x1 - x0 > 1.5 and y1 - y0 > 0.4 * min(wa[3] - wa[1], wb[3] - wb[1]):
                hits.append(f"'{wa[4]}'/'{wb[4]}'@[{round(x0)}, {round(y0)}]")
    if hits:
        pages += 1
        total += len(hits)
        print(f"page {i + 1}: " + "; ".join(hits[:6]))
print(f"{total} collisions on {pages} pages")
