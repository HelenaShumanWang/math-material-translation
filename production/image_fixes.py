"""Pixel corrections applied to the erased source before the layout: {"restore": [x0, y0, x1, y1], "page": N}
puts the source scan's pixels back in the box (an answer box or bubble outline an erase damaged); {"paint": [x0, y0,
x1, y1], "page": N, "colour": [r, g, b] | "border"} fills the box flat ("border": the median colour of the box's
one-point border ring - a sign's plate, a disc). Boxes in page points, page = the index in segment ids."""
import numpy as np
import pymupdf

from mathtrans.images import encode_image, load_image, replace_image

MAX_SHARE = 0.12  # a fix covers at most this share of the page


def check(c, page_count, page_rects):
    """None when the fix is valid, else why not."""
    try:
        page = int(c.get("page"))
        x0, y0, x1, y1 = (float(v) for v in (c.get("restore") or c.get("paint")))
    except Exception:  # noqa: BLE001
        return "a restore or paint needs page and box"
    if not 0 <= page < page_count:
        return "no such page"
    r = page_rects[page]
    if x1 <= x0 or y1 <= y0 or x0 < 0 or y0 < 0 or x1 > r.width or y1 > r.height:
        return "box off the page"
    if (x1 - x0) * (y1 - y0) > MAX_SHARE * r.width * r.height:
        return "box larger than a picture detail"
    if c.get("paint") is not None:
        col = c.get("colour", "border")
        if col != "border" and not (isinstance(col, list) and len(col) == 3 and all(0 <= int(v) <= 255 for v in col)):
            return "colour must be [r, g, b] or 'border'"
    return None


def apply(erased_doc: pymupdf.Document, source_path: str, fixes: list) -> int:
    """Apply ``fixes`` to the page images of ``erased_doc`` (in order); returns how many were applied."""
    src = pymupdf.open(source_path)
    done = 0
    by_page = {}
    for c in fixes:
        by_page.setdefault(int(c["page"]), []).append(c)
    for page_index, items in by_page.items():
        page = erased_doc[page_index]
        infos = page.get_image_info(xrefs=True)
        if not infos:
            continue
        info = max(infos, key=lambda i: (i["bbox"][2] - i["bbox"][0]) * (i["bbox"][3] - i["bbox"][1]))
        xref = info["xref"]
        bx0, by0, bx1, by1 = info["bbox"]
        loaded = load_image(erased_doc, xref)
        canvas = np.array(loaded.rgb, copy=True)
        sxref = src[page_index].get_image_info(xrefs=True)
        original = None
        if sxref:
            sinfo = max(sxref, key=lambda i: (i["bbox"][2] - i["bbox"][0]) * (i["bbox"][3] - i["bbox"][1]))
            original = np.asarray(load_image(src, sinfo["xref"]).rgb)
        sx, sy = loaded.width / (bx1 - bx0), loaded.height / (by1 - by0)
        for c in items:
            x0, y0, x1, y1 = (float(v) for v in (c.get("restore") or c.get("paint")))
            px0, py0 = max(0, int((x0 - bx0) * sx)), max(0, int((y0 - by0) * sy))
            px1, py1 = min(loaded.width, int(np.ceil((x1 - bx0) * sx))), min(loaded.height, int(np.ceil((y1 - by0) * sy)))
            if px1 <= px0 or py1 <= py0:
                continue
            if c.get("restore") is not None:
                if original is None or original.shape != canvas.shape:
                    continue
                canvas[py0:py1, px0:px1] = original[py0:py1, px0:px1]
            else:
                col = c.get("colour", "border")
                if col == "border":
                    ring = max(1, int(round(sx)))
                    edge = np.concatenate([canvas[py0:py0 + ring, px0:px1].reshape(-1, 3),
                                           canvas[py1 - ring:py1, px0:px1].reshape(-1, 3),
                                           canvas[py0:py1, px0:px0 + ring].reshape(-1, 3),
                                           canvas[py0:py1, px1 - ring:px1].reshape(-1, 3)])
                    colour = np.median(edge, axis=0).astype(np.uint8)
                else:
                    colour = np.array([int(v) for v in col], dtype=np.uint8)
                canvas[py0:py1, px0:px1] = colour
            done += 1
        alpha = np.array(loaded.alpha, copy=True) if loaded.alpha is not None else None
        stream = encode_image(canvas, alpha, loaded.ext, qtables=loaded.jpeg_qtables, subsampling=loaded.jpeg_subsampling)
        replace_image(page, xref, stream)
    return done
