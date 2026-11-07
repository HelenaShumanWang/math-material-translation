# Production run: the twelve 北师大版 primary maths volumes in English

These tools turn the scanned Chinese volumes (Grades 1–6, two volumes each) into English books with the layout of
the original. `mathtrans` does the first pass (stage 1); everything after it is corrections, written by
proofreading agents or by hand, applied to the pristine stage-1 segments on every run.

Install `requirements.txt` here as well as the project's: the layout was tuned with PyMuPDF 1.28.2, and on Python
3.12+ OCR uses `rapidocr` 3 pinned to the PP-OCRv4 mobile models (see `mathtrans/ocr.py`).

## Folders

Everything a run makes is under `$BNU_WORK` (default `/tmp/piptest/real`), see `common.py`:
`books/<code>.pdf` (sources), `books/out_<code>/` (stage 1 and renders), `proof/<code>/` (corrections and proof
packs), `afterword/`, `previews/`, `deliver/` (compact copies). The earlier checked edition is read from the
`deliveries` branch checked out at `$BNU_DELIVERIES` (default `/tmp/piptest/deliveries`).

**Save the state often** (`save_state.sh`): it pushes every volume's corrections, pristine segments and the OCR cache
to the `work-state` branch. A container that is reset loses `$BNU_WORK`.

## One volume, in order

1. Stage 1: `python -m mathtrans.cli translate books/<code>.pdf --to en --from zh --translator deepseek --skip-pages 2 --out books/out_<code>`
   (`DEEPSEEK_API_KEY`, `MATHTRANS_OCR_CACHE_DIR=$BNU_WORK/ocr_cache`).
2. `recover_english.py <code>`: the checked edition's English for every paragraph it can be matched to.
3. `apply_corrections.py <code>` (re-render), `han_left.py <code> > han.txt`, `leftover_items.py <code> han.txt`,
   `make_proof_pack.py <code>`.
4. Proofreading pass (`workflows/proofread_pass.js`, args `{pass, batch, volumes: [{code, title, pages}]}`): one
   agent per batch of pages writes `corr_p<N>_<page>.json`, a second checks it on a render. Then the flagged
   defects (`workflows/flags_fix.js`) and the headings and labels (`workflows/labels_review.js`).
5. `cycle.sh <code>`: apply, render, the English book with its afterword (`afterword_en.py`), the compact copy, the
   push to `deliveries`, a fresh proof pack and the saved state.

Checks: `collisions.py` (text set over text), `size_outliers.py` (numbered instructions smaller than their page's),
`han_left.py` (Chinese still visible). Agents see a page with `preview_pages.py`, try corrections with `try_fix.py`
and read positions with `ruler.py`. The correction kinds are listed at the top of `apply_corrections.py`.
