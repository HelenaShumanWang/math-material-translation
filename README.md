# mathtrans — layout-preserving translation of math learning materials

[中文说明 / Chinese README](README.zh-CN.md)

`mathtrans` translates math textbooks and worksheets (PDF) between **Chinese, English, Portuguese, Spanish, Japanese and Korean**. It keeps the original page layout, images, colours and styling, replaces **every piece of text on the page — including text embedded in raster images** — with the translation, runs a mandatory **multi-round automatic QA loop**, and only then exports an **editable PDF** (optionally also a Word document and a bilingual side-by-side version).

| Source (Chinese textbook, page 1) | Output (English, layout / images / in-image text preserved) |
|---|---|
| ![source](docs/sample-zh-source-page1.png) | ![translated](docs/sample-zh-en-page1.png) |

Web UI (bilingual labels):

![web ui](docs/screenshot-web-ui.png)

> The pictures above were produced by the built-in **offline mock translator** (word-by-word substitution used for demos and tests). With an `ANTHROPIC_API_KEY` configured, translation and semantic review are done by Claude.

---

## Feature matrix

| Requirement | Status | How it is implemented |
|---|---|---|
| Upload source files (zh / en / pt / es / ja / ko) | ✅ | Web upload, REST API and CLI; the source language is auto-detected (`languages.detect_language`) or set explicitly |
| Free choice of target language | ✅ | Any of the six languages (source ≠ target) |
| Layout, images and styling preserved | ✅ | Only the original text objects are erased (PyMuPDF redaction keeps images, rules and background fills); the translation is re-inserted into the original text box with the original font size, colour, weight and alignment, shrinking, tightening line height or growing into free space (never across a column gutter) when it does not fit |
| Text inside images translated | ✅ | RapidOCR (offline) or Claude vision detects text in raster images → translation → background fill / inpainting → redraw in a target-language font → the image object is replaced (same pixel size and placement) |
| Editable PDF | ✅ | Translated text consists of real text objects with embedded fonts; it can be edited in Acrobat, Illustrator, etc. (`--subset-fonts` trades editability for a much smaller file) |
| Automatic QA (mandatory) | ✅ | 10 rule checks + Claude semantic review + layout-fit checks + output-file checks, run in a loop (failing segments are re-translated with the QA feedback); files are exported only after QA passes — a failing job is marked `qa_failed` and its downloads are refused unless forced |
| Batch upload | ✅ | Upload several PDFs at once; one project per file under a shared `batch_id`, executed by a background queue |
| Word export | ✅ | `--docx` / "Export DOCX" (LibreOffice conversion; python-docx rebuild when LibreOffice is unavailable) |
| Fixed terminology (glossary) | ✅ | 90+ built-in six-language math terms; custom CSV/JSON glossaries (upload or paste) take precedence; QA verifies that the glossary was followed |
| Projects are saved | ✅ | Every project lives in `data/projects/<id>/` with the source file, the outputs of every run, the QA report and the segment JSON; re-translate with another target language or glossary while keeping the history |
| Preview | ✅ | PNG previews of every page are generated after translation (`/api/projects/{id}/preview/{page}`); download when satisfied |
| Bilingual side-by-side version | ✅ | `--bilingual` / "Bilingual side-by-side PDF": original page on the left, translation on the right |
| Skip pages | ✅ | `--skip-pages 2` / "Skip pages" leaves selected pages untouched (e.g. a page with a QR code or legal notice) |
| Scanned textbooks | ✅ | Pages without a text layer go through OCR; by default (`--scanned-mode overlay`) the recognised text is erased from the page image and the translation is placed as real, editable text (OCR lines are grouped into paragraphs so sentences are translated in context); `--scanned-mode repaint` draws it into the image instead |

---

## Quick start

```bash
git clone https://github.com/HelenaShumanWang/math-material-translation
cd math-material-translation
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"                     # or: pip install -r requirements.txt
cp .env.example .env                       # put your ANTHROPIC_API_KEY here
python scripts/fetch_fonts.py              # optional: Noto Sans SC/JP/KR for nicer typography
```

Optional system dependency: **LibreOffice** (`soffice`) for high-fidelity Word export; without it the Word file is rebuilt with python-docx.

### Command line

```bash
# Write a two-page sample textbook (Chinese, with text inside the figures)
mathtrans sample examples/sample_zh.pdf --lang zh

# Chinese textbook → English: layout preserved, in-image text translated, automatic QA,
# editable PDF + bilingual version + Word document
mathtrans translate examples/sample_zh.pdf --to en --bilingual --docx --out output/zh_en

# Explicit source language, custom glossary, up to 4 QA rounds, page 2 left untouched
mathtrans translate book.pdf --from zh --to pt --glossary my_terms.csv --max-rounds 4 --skip-pages 2

# Without an API key the offline mock translator exercises the whole pipeline
# (demo / testing only — it is not a real translation)
mathtrans translate examples/sample_zh.pdf --to en --translator mock

# Scanned textbook (default overlay mode: editable text); --scanned-mode repaint paints into the page image
mathtrans translate scanned_book.pdf --to en --skip-pages 2

# Pick a model and subset the embedded fonts (smaller file; editors can only reuse embedded glyphs)
mathtrans translate book.pdf --to ja --model claude-opus-5-5 --subset-fonts
```

Exit codes: `0` completed with QA passed, `2` QA failed (the output files are still written for inspection), `1` error.
`examples/` contains sample textbooks in all six languages, generated with `mathtrans sample`.

### Web UI and REST API

```bash
mathtrans serve --host 0.0.0.0 --port 8000
# open http://localhost:8000
```

The UI offers multi-file upload, source/target language selection, glossaries (pick an existing one, paste CSV or upload a file), options (in-image text, bilingual version, Word export, QA rounds, skip pages), a project table with live progress, the QA report, page previews, downloads and re-translation into another language.

| Method | Path | Purpose |
|---|---|---|
| GET | `/api/languages` | Supported languages |
| GET / POST | `/api/glossaries` | List / upload glossaries (CSV/JSON file or a `text` field) |
| GET | `/api/glossaries/template` | CSV glossary template |
| POST | `/api/projects` | Create projects (multipart: `files`×N, `target_lang`; optional `source_lang`, `glossary_id`, `translate_images`, `bilingual`, `export_docx`, `max_qa_rounds`, `require_qa_pass`, `subset_fonts`, `pages`, `skip_pages`) |
| GET | `/api/projects`, `/api/projects/{id}` | List / detail (status, progress, result, QA summary) |
| POST | `/api/projects/{id}/retranslate` | New run with another target language / glossary / options (history kept) |
| GET | `/api/projects/{id}/qa` | QA report (`?format=md` for Markdown) |
| GET | `/api/projects/{id}/preview/{page}` | PNG preview of page N |
| GET | `/api/projects/{id}/download?format=pdf\|bilingual\|docx\|segments` | Download (409 while QA has not passed; add `&force=1` to override) |
| DELETE | `/api/projects/{id}` | Delete a project |

### Glossary format

CSV with language codes as header (an optional `note` column; any two or more languages suffice) or JSON:

```csv
zh,en,pt,es,ja,ko,note
勾股定理,Pythagorean theorem,Teorema de Pitágoras,Teorema de Pitágoras,三平方の定理,피타고라스 정리,
斜边,hypotenuse,hipotenusa,hipotenusa,斜辺,빗변,
```

The built-in glossary is `mathtrans/data/default_glossary.csv`; custom entries override it.

---

## Pipeline

```
PDF ─► extract text blocks (size / colour / alignment / role) + protect formulas and numbers with placeholders
    ─► OCR text inside images (RapidOCR offline, or Claude vision)
    ─► translate with Claude (glossary injected, structured JSON output, placeholder verification)
    ─► QA loop: rule checks + Claude semantic review + layout-fit checks → failing segments re-translated with feedback
       → until everything passes or the round limit is reached
    ─► re-layout (erase original text, insert translation in the original style, keep images/graphics) ─► replace in-image text
    ─► output-file checks (page count / page size / image placement / leftovers / embedded fonts)
    ─► exports: editable PDF, bilingual PDF, Word, segment JSON, QA report (JSON + Markdown), PNG previews
```

### QA dimensions

| Check | Level | What it verifies |
|---|---|---|
| completeness | error | Every translatable segment has a translation |
| placeholders | error | Formula / number placeholders are all present exactly once |
| numbers | error | Every number of the source (incl. full-width digits) appears in the translation |
| untranslated | error | No source-language text remains in the translation |
| target_script | error | The translation is written in the target language's script |
| glossary | error | Glossary terms were used (inflection-aware for Latin languages) |
| formatting | error | List markers, line breaks and sentence-final punctuation preserved; no stray quotes or JSON |
| layout_fit | error | The translation fits its original box (no shrinking below 55 %), otherwise a shorter translation is requested |
| image_text | error / warning | Text inside images was repainted and did not overflow |
| length_ratio | warning | Translation length ratio is plausible |
| LLM review | error / warning | Claude compares source and translation: meaning errors, omissions, number/formula mismatches, terminology, grammar |
| output_* | error | Output PDF has the same page count, page sizes and image placements as the source; translated text is extractable; no leftovers; fonts embedded |

The report is written as `qa_report.json` / `qa_report.md` and shown in the web UI.

---

## Configuration

Environment variables (or `.env`):

| Variable | Default | Meaning |
|---|---|---|
| `ANTHROPIC_API_KEY` | — | Claude API key (translation, review, vision OCR). Without it the offline mock translator is used (demo only) |
| `MATHTRANS_CLAUDE_MODEL` | `claude-opus-5-5` | Model for translation and review |
| `MATHTRANS_CLAUDE_EFFORT` | `high` | Reasoning effort: low / medium / high / xhigh / max |
| `MATHTRANS_ENABLE_FALLBACKS` | `true` | Server-side refusal fallbacks (`fallbacks: "default"`) |
| `MATHTRANS_TRANSLATOR` | `auto` | `auto` / `claude` / `mock` |
| `MATHTRANS_OCR_ENGINE` | `auto` | `auto` / `rapid` / `claude` / `none` |
| `MATHTRANS_DATA_DIR` | `data` | Where projects and outputs are stored |
| `MATHTRANS_FONTS_DIR` | — | Extra fonts directory |
| `MATHTRANS_MAX_QA_ROUNDS` | `3` | Maximum QA rounds |
| `MATHTRANS_REQUIRE_QA_PASS` | `true` | Refuse downloads while QA has not passed |
| `MATHTRANS_MAX_UPLOAD_MB` | `100` | Per-file upload limit of the web service |
| `MATHTRANS_MAX_WORKERS` | `2` | Concurrent translation jobs in the web service |

---

## Development

```bash
pip install -e ".[dev]"
python -m pytest -q      # fully offline: mock translator + generated sample PDFs, no API key needed
```

The module layout is described in `ARCHITECTURE.md`: `extract` (text extraction), `protect` (formula protection), `ocr` / `images` (text inside images), `translate` (Claude / mock backends), `qa` (checks and loop), `layout` / `export` (re-layout and exports), `pipeline` (orchestration), `projects` / `api` / `cli` / `web` (service and UI).

A `Dockerfile` is included (`docker build -t mathtrans . && docker run -p 8000:8000 -e ANTHROPIC_API_KEY=... -v $PWD/data:/data mathtrans`).

### Known limitations

* **Scanned PDFs** (each page is one image, no text layer) are handled through OCR. The default `overlay` mode erases the recognised text and places editable text; because the boxes are as tight as the scan, long translations are shrunk (the QA report lists them). `--scanned-mode repaint` draws the translation into the page image instead (picture-based result). Slanted decorative text and watermarks are left untouched.
* RapidOCR ships Chinese + English recognition models; for Japanese, Korean, Portuguese or Spanish text inside images use the Claude vision OCR (`MATHTRANS_OCR_ENGINE=claude`) for best results. Superscripts inside images may be recognised as plain digits.
* Vertical (Japanese) writing is treated as rotated text; complex vertical layouts may need manual touch-up.
* The offline mock translator only demonstrates the pipeline; it is not a real translation.
