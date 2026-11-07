"""strip_page2.py <code>: the English book from the render: out_<code>/output.pdf without page 2 (the QR page of the
Chinese edition is left out) and with the last page (the afterword, vector outlines the pipeline cannot read)
replaced by its typeset English page afterword/final_<code>.pdf when there is one. Writes out_<code>/final.pdf."""
import sys
from pathlib import Path

import pymupdf

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import AFTERWORD, out_dir  # noqa: E402

code = sys.argv[1]
src = pymupdf.open(str(out_dir(code) / "output.pdf"))
n = src.page_count
out = pymupdf.open()
out.insert_pdf(src, from_page=0, to_page=0)
aw = AFTERWORD / f"final_{code}.pdf"
last = n - 2 if aw.exists() else n - 1
out.insert_pdf(src, from_page=2, to_page=last)
if aw.exists():
    out.insert_pdf(pymupdf.open(str(aw)))
out.save(str(out_dir(code) / "final.pdf"), garbage=3, deflate=True)
print(f"final.pdf: {out.page_count} pages (page 2 removed from {n}" + ("; English afterword)" if aw.exists() else ")"))
