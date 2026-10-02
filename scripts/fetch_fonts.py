"""Download Noto Sans SC / JP / KR / Latin from Google Fonts into ./fonts (optional, nicer typography)."""
import re
import sys
import urllib.request
from pathlib import Path

FAMILIES = {"NotoSansSC": "Noto+Sans+SC", "NotoSansJP": "Noto+Sans+JP", "NotoSansKR": "Noto+Sans+KR", "NotoSans": "Noto+Sans"}
OUT = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent / "fonts"
OUT.mkdir(parents=True, exist_ok=True)
for name, fam in FAMILIES.items():
    target = OUT / f"{name}-Regular.ttf"
    if target.exists():
        print("exists", target)
        continue
    req = urllib.request.Request(f"https://fonts.googleapis.com/css2?family={fam}&display=swap",
                                 headers={"User-Agent": "Mozilla/5.0"})
    css = urllib.request.urlopen(req, timeout=30).read().decode()
    m = re.search(r"https://fonts\.gstatic\.com[^)]+", css)
    if not m:
        print("no url for", name)
        continue
    data = urllib.request.urlopen(m.group(0), timeout=120).read()
    target.write_bytes(data)
    print("saved", target, len(data))
