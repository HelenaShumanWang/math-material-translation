"""size_outliers.py <code>...: numbered instructions ("3. ...", "(2) ...") set smaller than the other numbered
instructions of their page (same kind of text, same size). Prints page (1-based), id, size vs the page's size."""
import json, re, statistics, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import out_dir  # noqa: E402
ITEM = re.compile(r"^\s*(\d{1,2}\.\s|\(\d{1,2}\)\s|[①-⑩])")
tot = 0
for code in sys.argv[1:]:
    segs = json.load(open(out_dir(code) / "segments.json"))["segments"]
    pages = {}
    for s in segs:
        r = s.get("render") or {}
        if s["kind"] != "text" or not r.get("font_size") or not ITEM.match(s.get("translated_text") or ""):
            continue
        pages.setdefault(s["page"], []).append(s)
    n = 0
    for p, ss in sorted(pages.items()):
        if len(ss) < 2:
            continue
        top = max(statistics.median(x["render"]["font_size"] for x in ss), 0)
        for s in ss:
            f = s["render"]["font_size"]
            if f < 0.9 * top:
                n += 1
                if "-v" in sys.argv:
                    print(f"  {code} page {p + 1} {s['id']} {f:.1f} vs {top:.1f} {s['render'].get('notes', '')[:60]!r} {(s.get('translated_text') or '')[:50]!r}")
    tot += n
    print(code, n, "numbered instructions smaller than their page's")
print("total", tot)
