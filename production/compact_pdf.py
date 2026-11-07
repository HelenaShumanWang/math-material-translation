"""compact_pdf.py <in.pdf> <out.pdf> [max MiB]: a copy small enough to send in chat: page images re-encoded at
falling resolution and JPEG quality until the file fits (text and vector graphics untouched)."""
import os
import sys

import pymupdf

src, dst = sys.argv[1], sys.argv[2]
limit = float(sys.argv[3]) if len(sys.argv) > 3 else 29.5
for dpi, quality in ((200, 80), (170, 75), (150, 72), (130, 68), (110, 62), (96, 55)):
    d = pymupdf.open(src)
    d.rewrite_images(dpi_threshold=dpi + 10, dpi_target=dpi, quality=quality, lossy=True, lossless=True, bitonal=True,
                     color=True, gray=True, set_to_gray=False)
    d.save(dst, garbage=4, deflate=True)
    size = os.path.getsize(dst) / 2 ** 20
    if size <= limit:
        break
print(f"wrote {dst}: {size:.1f} MiB (images at {dpi} dpi, quality {quality})")
