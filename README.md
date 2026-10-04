# mathtrans — layout-preserving translation of math learning materials

[中文说明 / Chinese README](README.zh-CN.md)

`mathtrans` translates math textbooks and worksheets (PDF) between **Chinese, English, Portuguese, Spanish, Japanese and Korean**. It keeps the original page layout, images, colours and styling, replaces **every piece of text on the page — including text embedded in raster images** — with the translation, runs a mandatory **multi-round automatic QA loop**, and only then exports an **editable PDF** (optionally also a Word document and a bilingual side-by-side version).

| Source (Chinese textbook, page 1) | Output (English, layout / images / in-image text preserved) |
|---|---|
| ![source](docs/sample-zh-source-page1.png) | ![translated](docs/sample-zh-en-page1.png) |

Web UI (bilingual labels):

![web ui](docs/screenshot-web-ui.png)

> The pictures above were produced by the built-in **offline mock translator** (word-by-word substitution used for demos and tests). With an `ANTHROPIC_API_KEY` configured, translation and semantic review are done by Claude; with a `DEEPSEEK_API_KEY` they are done by DeepSeek.

---

## Feature matrix

| Requirement | Status | How it is implemented |
|---|---|---|
| Upload source files (zh / en / pt / es / ja / ko) | ✅ | Web upload, REST API and CLI; the source language is auto-detected (`languages.detect_language`) or set explicitly |
| Free choice of target language | ✅ | Any of the six languages (source ≠ target) |
| Layout, images and styling preserved | ✅ | Only the original text objects are erased (PyMuPDF redaction keeps images, rules and background fills); the translation is re-inserted into the original text box with the original font size, colour, weight and alignment, shrinking, tightening line height or growing into free space (never across a column gutter) when it does not fit. Ruled tables are recognised from their rules and translated cell by cell (each translation stays inside its cell); side-by-side text on one line (running head + page number, borderless table rows) is kept in place as separate pieces |
| Text inside images translated | ✅ | RapidOCR (offline) or Claude vision detects text in raster images → translation → background fill / inpainting → redraw in a target-language font → the image object is replaced (same pixel size and placement) |
| Editable PDF | ✅ | Translated text consists of real text objects with embedded fonts; it can be edited in Acrobat, Illustrator, etc. (`--subset-fonts` trades editability for a much smaller file) |
| Automatic QA (mandatory) | ✅ | 10 rule checks + Claude semantic review + layout-fit checks + output-file checks, run in a loop (failing segments are re-translated with the QA feedback); files are exported only after QA passes — a failing job is marked `qa_failed` and its downloads are refused unless forced (the web UI asks for a confirmation and labels such downloads "forced") |
| Batch upload | ✅ | Upload several PDFs at once; one project per file under a shared `batch_id`, executed by a background queue |
| Word export | ✅ | `--docx` / "Export DOCX" (LibreOffice conversion; python-docx rebuild when LibreOffice is unavailable) |
| Fixed terminology (glossary) | ✅ | 90+ built-in six-language math terms; custom CSV/JSON glossaries (upload or paste) take precedence; QA verifies that the glossary was followed |
| Projects are saved | ✅ | Every project lives in `data/projects/<id>/` with the source file, the outputs of every run, the QA report and the segment JSON; re-translate with another target language or glossary while keeping the history — every previous run stays viewable and downloadable (history links in the UI, `?run=<run_id>` in the API) |
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
mathtrans serve                      # http://127.0.0.1:8000 (loopback only)
# open http://localhost:8000
```

The UI offers multi-file upload, source/target language selection, glossaries (pick an existing one, paste CSV or upload a file), options (in-image text, bilingual version, Word export, QA rounds, skip pages), a project table with live progress, the QA report, page previews, downloads (a confirmed, explicitly "forced" download when QA failed), re-translation into another language and, for every previous run, links to its outputs, previews and QA report.

**Deployment and access control.** There are no user accounts: every client that can reach the port sees, creates, re-translates and deletes every project and glossary. By default the service listens on the loopback interface only. Bind to `0.0.0.0` (or publish the Docker port) only behind an authenticating reverse proxy, or set `MATHTRANS_API_TOKEN`: every `/api/*` request (except `GET /api/languages`) then needs `Authorization: Bearer <token>` or `X-API-Key: <token>` (the web UI asks for the token and stores it in the browser). Independently of the token, state-changing requests that a browser marks as cross-site (`Sec-Fetch-Site: cross-site`, or an `Origin` that does not match the host) are refused with 403, so a web page open in the operator's browser cannot plant projects or glossaries (CSRF).

```bash
MATHTRANS_API_TOKEN=change-me mathtrans serve --host 0.0.0.0 --port 8000
curl -H 'Authorization: Bearer change-me' http://host:8000/api/projects
```

| Method | Path | Purpose |
|---|---|---|
| GET | `/api/languages` | Supported languages |
| GET / POST | `/api/glossaries` | List / upload glossaries (CSV/JSON file or a `text` field) |
| GET | `/api/glossaries/template` | CSV glossary template |
| POST | `/api/projects` | Create projects (multipart: `files`×N, `target_lang`; optional `source_lang`, `glossary_id`, `translate_images`, `bilingual`, `export_docx`, `max_qa_rounds`, `require_qa_pass`, `subset_fonts`, `pages`, `skip_pages`, `ocr_engine`); 413 when a file exceeds `MATHTRANS_MAX_UPLOAD_MB` or `MATHTRANS_MAX_PAGES` |
| GET | `/api/projects`, `/api/projects/{id}` | List / detail (status, progress, result, QA summary) |
| POST | `/api/projects/{id}/retranslate` | New run with another target language / glossary / options (history kept: the previous run stays on disk and is listed in `history` with its `run_id`, `outputs` and `preview_pages`) |
| GET | `/api/projects/{id}/qa` | QA report (`?format=md` for Markdown; `&run=<run_id>` for a previous run) |
| GET | `/api/projects/{id}/preview/{page}` | PNG preview of page N (`?run=<run_id>` for a previous run) |
| GET | `/api/projects/{id}/download?format=pdf\|bilingual\|docx\|segments` | Download (409 while QA has not passed; add `&force=1` to override; `&run=<run_id>` downloads the output of a previous run, judged by that run's status) |
| DELETE | `/api/projects/{id}` | Delete a project |

### Glossary format

CSV with language codes as header (an optional `note` column; any two or more languages suffice) or JSON:

```csv
zh,en,pt,es,ja,ko,note
勾股定理,Pythagorean theorem,Teorema de Pitágoras,Teorema de Pitágoras,三平方の定理,피타고라스 정리,
斜边,hypotenuse,hipotenusa,hipotenusa,斜辺,빗변,
```

The built-in glossary is `mathtrans/data/default_glossary.csv`; custom entries override it. A custom glossary may hold up to 20,000 entries with terms of up to 200 characters (the QA glossary check scans every pair for every segment); longer lists should be split by subject.

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
| `ANTHROPIC_API_KEY` | — | Claude API key (translation, review, vision OCR). Without any key the offline mock translator is used (demo only) |
| `DEEPSEEK_API_KEY` | — | DeepSeek API key (translation and review through the OpenAI-compatible chat endpoint in JSON mode). Used when no Anthropic key is set, or with `MATHTRANS_TRANSLATOR=deepseek` / `--translator deepseek`; OCR of text inside images stays with RapidOCR |
| `MATHTRANS_DEEPSEEK_MODEL` | `deepseek-chat` | DeepSeek model (e.g. `deepseek-v4-pro`, `deepseek-flash`); per job: `--model` |
| `MATHTRANS_DEEPSEEK_BASE_URL` | `https://api.deepseek.com` | DeepSeek endpoint (any OpenAI-compatible `/chat/completions` server with JSON mode) |
| `MATHTRANS_CLAUDE_MODEL` | `claude-opus-5-5` | Model for translation and review |
| `MATHTRANS_CLAUDE_EFFORT` | `medium` | Reasoning effort: low / medium / high / xhigh / max |
| `MATHTRANS_ENABLE_FALLBACKS` | `true` | Server-side refusal fallbacks (`fallbacks: "default"`) |
| `MATHTRANS_TRANSLATOR` | `auto` | `auto` / `claude` / `deepseek` / `mock`. `auto` = Claude if `ANTHROPIC_API_KEY` is set, else DeepSeek if `DEEPSEEK_API_KEY` is set, else mock |
| `MATHTRANS_OCR_ENGINE` | `auto` | `auto` / `rapid` / `claude` / `none`. `auto` = offline RapidOCR for zh/en/pt/es sources; Claude vision for ja/ko sources when an API key is configured (RapidOCR reads kana / hangul unreliably — without a key it is still used and every translated image label gets a QA warning). Per job: `--ocr-engine` / form field `ocr_engine` |
| `MATHTRANS_OCR_THREADS` | `0` | Threads per RapidOCR model (`0` = all cores). Set `1` when several documents are translated side by side |
| `MATHTRANS_OCR_CACHE_DIR` | — | When set, OCR results are cached per image in this directory, so re-running a document (after a crash or a change further down the pipeline) skips recognition |
| `MATHTRANS_MAX_IMAGE_MEGAPIXELS` | `50` | Embedded images with more pixels are neither decoded nor OCR'd (memory budget; a 600 dpi A4 scan is ~35 MP) |
| `MATHTRANS_DATA_DIR` | `data` | Where projects and outputs are stored |
| `MATHTRANS_FONTS_DIR` | — | Extra fonts directory |
| `MATHTRANS_MAX_QA_ROUNDS` | `3` | Maximum QA rounds |
| `MATHTRANS_REQUIRE_QA_PASS` | `true` | Refuse downloads while QA has not passed |
| `MATHTRANS_MAX_UPLOAD_MB` | `100` | Per-file upload limit of the web service (also bounds glossary uploads) |
| `MATHTRANS_MAX_PAGES` | `500` | Page limit per document: web uploads / re-translations of longer PDFs are refused (413) and the CLI refuses to translate more pages than this (`--pages` counts); memory grows with every rendered page, so raise it only on hosts with enough RAM |
| `MATHTRANS_RENDER_CHECKPOINT_PAGES` | `25` | The layout stage saves and reopens the PDF every N rendered pages, which keeps memory flat for long documents (`0` disables) |
| `MATHTRANS_MAX_WORKERS` | `2` | Concurrent translation jobs in the web service |
| `MATHTRANS_API_TOKEN` | — | Shared secret required on every `/api/*` request when set (`Authorization: Bearer`, `X-API-Key` or the UI's cookie); recommended whenever the service is reachable from other machines |

---

## Development

```bash
pip install -e ".[dev]"
python -m pytest -q      # fully offline: mock translator + generated sample PDFs, no API key needed
```

The module layout is described in `ARCHITECTURE.md`: `extract` (text extraction), `protect` (formula protection), `ocr` / `images` (text inside images), `translate` (Claude / DeepSeek / mock backends), `qa` (checks and loop), `layout` / `export` (re-layout and exports), `pipeline` (orchestration), `projects` / `api` / `cli` / `web` (service and UI).

A `Dockerfile` is included (`docker build -t mathtrans . && docker run -p 8000:8000 -e ANTHROPIC_API_KEY=... -e MATHTRANS_API_TOKEN=... -v $PWD/data:/data mathtrans`); the container listens on `0.0.0.0`, so set `MATHTRANS_API_TOKEN` or publish the port only to a reverse proxy (see "Deployment and access control").

### Known limitations

* **Scanned PDFs** (each page is one image, no text layer) are handled through OCR. The default `overlay` mode groups OCR lines into paragraphs (headings, table cells, labels, answer blanks and equations stay separate), erases only the glyphs of the recognised text, places editable text and lets it grow into plain background around the box (never over pictures); what still does not fit is shrunk and listed in the QA report. `--scanned-mode repaint` draws the translation into the page image instead. Slanted decorative text and the publisher watermark (learnt from its slanted fragments) are left untouched; OCR noise such as single low-confidence characters stays in the picture.
* RapidOCR ships Chinese + English recognition models; kana and hangul inside images are often misread as look-alike Han characters, and Portuguese / Spanish accents may be dropped. With an API key, `auto` therefore uses the Claude vision OCR for Japanese and Korean sources (or force it with `--ocr-engine claude` / `MATHTRANS_OCR_ENGINE=claude`). Without a key, RapidOCR is still used for ja/ko: Korean lines read as Han-only text are left untouched (`unreliable OCR`), and the QA report carries an `image_text` warning for every translated image label so the figures get checked in the preview. Superscripts inside images may be recognised as plain digits.
* When the Claude vision OCR cannot serve any request (bad API key, unknown model), the job stops with status `error` and the reason; a transient failure on individual images (rate limit, 5xx) skips those images and is reported in the QA report (`OCR failed on N of M image(s)`; an error that blocks the download when no image could be read at all).
* Vertical (Japanese) writing is treated as rotated text; complex vertical layouts may need manual touch-up.
* The offline mock translator only demonstrates the pipeline; it is not a real translation.
