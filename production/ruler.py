"""ruler.py <code> <page index> x0 y0 x1 y1 <out.png> [zoom]: the rendered page's area (PDF points) with point rulers
on the top and left, for reading exact positions (page index = 1-based page number minus 1)."""
import sys
from pathlib import Path

import pymupdf
from PIL import Image, ImageDraw

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import out_dir  # noqa: E402

code, page = sys.argv[1], int(sys.argv[2])
x0, y0, x1, y1 = (float(v) for v in sys.argv[3:7])
out, zoom = sys.argv[7], float(sys.argv[8]) if len(sys.argv) > 8 else 3.0
pdf = pymupdf.open(str(out_dir(code) / "output.pdf"))
pix = pdf[page].get_pixmap(clip=pymupdf.Rect(x0, y0, x1, y1), matrix=pymupdf.Matrix(zoom, zoom))
im = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
m = 30
canvas = Image.new("RGB", (im.width + m, im.height + m), "white")
canvas.paste(im, (m, m))
d = ImageDraw.Draw(canvas)
step = 5 if (x1 - x0) <= 150 else 10
for v in range(int(x0 // step * step), int(x1) + 1, step):
    if v < x0:
        continue
    x = m + (v - x0) * zoom
    d.line([(x, m - (8 if v % (2 * step) == 0 else 4)), (x, m)], fill="red")
    if v % (2 * step) == 0:
        d.text((x - 8, 2), str(v), fill="red")
for v in range(int(y0 // step * step), int(y1) + 1, step):
    if v < y0:
        continue
    y = m + (v - y0) * zoom
    d.line([(m - (8 if v % (2 * step) == 0 else 4), y), (m, y)], fill="blue")
    if v % (2 * step) == 0:
        d.text((1, y - 5), str(v), fill="blue")
canvas.save(out)
print(out)
