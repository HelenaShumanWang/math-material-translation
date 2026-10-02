# Architecture & module contract

`mathtrans` translates math learning materials (PDF) between zh / en / pt / es / ja / ko while
preserving the page layout, replacing text that is embedded in raster images, producing an
editable PDF and running a multi-round automatic QA loop before anything is exported.

```
upload ─► extract (text segments + protection) ─► OCR images (image_text segments)
       ─► translate (Claude, glossary) ─► QA loop [rule checks + LLM review → re-translate]
       ─► layout (redact + re-insert text, preserve images/graphics) ─► image text replacement
       ─► output checks (page count, geometry, leftovers, fonts) ─► exports (PDF / bilingual / DOCX)
       ─► previews (PNG per page)
```

## Shared modules (already implemented — do not change their public API without updating all users)

| module | purpose |
|---|---|
| `mathtrans/models.py` | All pydantic models: `Lang`, `BBox`, `TextSpan`, `SegmentStyle`, `ImageRef`, `RenderInfo`, `TextSegment`, `Glossary`, `TranslationItem/Result`, `ReviewItem/Finding`, `OcrResult`, `QAIssue/QARound/QAReport`, `PageInfo`, `TranslatedDocument`, `PipelineOptions`, `PipelineStats`, `PipelineResult`; placeholder helpers (`make_placeholder`, `PLACEHOLDER_RE`, `restore_placeholders`). |
| `mathtrans/languages.py` | `LANGUAGES` table, `detect_language(text)`, `script_profile`, `letters_of_script`, `foreign_letters`, `script_ratio`, `is_cjk`, `normalize_for_compare`. |
| `mathtrans/protect.py` | `protect_text(text, src_lang, extra_fragments) -> (protected_text, fragments)`, `is_fully_protected`, `verify_placeholders(protected_text, translated_raw) -> problems`. |
| `mathtrans/glossary.py` | `default_glossary()`, `effective_glossary(custom, use_default)`, `load_glossary`, `parse_glossary_text`, `save_glossary`, `glossary_prompt_block(pairs)`, `missing_glossary_terms(...)`, `apply_glossary_literal`, `glossary_template_csv`. |
| `mathtrans/fonts.py` | `find_font_file(lang, bold)`, `pil_font(lang, size)`, `html_font_setup(lang) -> (css, archive, family)`, `text_width`, `wrap_lines`, `fit_font_size`. |
| `mathtrans/config.py` | `Settings` (env `MATHTRANS_*`, `ANTHROPIC_API_KEY`), `get_settings()`, `reset_settings()`. |
| `mathtrans/interfaces.py` | Protocols `Translator`, `Reviewer`, `OcrEngine`, `QACheck`; `ProgressCallback`; exceptions `TranslationError`, `TranslationRefused`. |
| `mathtrans/samples.py` | `make_sample_pdf(path, lang)` two-page sample textbook with images containing text (fixtures `sample_pdf_zh`, `sample_pdf_en` in `tests/conftest.py`). |

Conventions: page coordinates are PyMuPDF points (top-left origin); pages are 0-based;
segment ids are `p{page}_b{n}` for text and `p{page}_i{xref}_{n}` for image text; the
translator only ever sees `protected_text` (placeholders `⟦n⟧`), `translation_raw` keeps the
placeholders, `translated_text` has them restored. Never import `pipeline`/`api` from a
lower-level module. Log through `logging.getLogger("mathtrans.<module>")`. Everything must
work offline with the mock translator so the test-suite never needs network or an API key.

## Modules to implement

### `mathtrans/extract.py` (text extraction)
```python
def extract_document(pdf_path, *, target_lang: Lang, source_lang: Lang | None = None,
                     pages: list[int] | None = None) -> TranslatedDocument
def detect_document_language(pdf_path_or_doc) -> Lang            # over all text, via languages.detect_language
def build_page_segments(page: pymupdf.Page, page_index: int, source_lang: Lang) -> list[TextSegment]
```
* Use `page.get_text("dict")` (TEXTFLAGS_DICT without TEXT_PRESERVE_IMAGES); one segment per text block (a block =
  paragraph). Join lines: CJK sources join with "" (keep an explicit "\n" only where a line ends
  with sentence punctuation and the next line starts a list item / looks like a new paragraph);
  Latin sources join with " " and de-hyphenate `word-\nword`. Keep list markers (`1.`, `(1)`, `①`, `•`).
* Spans typeset in math fonts (name contains `CMMI`, `CMSY`, `CMEX`, `Symbol`, `Math`, `MTExtra`,
  `Euclid`, `MT-`, `Cambria Math`, `Asana`, `XITS`, `STIX` …) or single-letter italic spans are
  `is_math=True` and passed to `protect_text(..., extra_fragments=[span texts])`.
* `translate=False` with a `skip_reason` for segments that are empty, pure numbers/formulas
  (`is_fully_protected`), or have no letters of the source script *and* no Latin letters.
* `style`: dominant (by character count) font size/colour/bold/italic/serif; `align` from the
  line boxes (centred if lines are symmetric within the block, right if right-aligned, justify if
  >=3 lines and all but the last line end within 2pt of the block right edge); `role` heuristic
  (heading = size >= 1.25 × page median size or bold & <= 2 lines; caption = starts with
  图/表/Figure/Fig./Figura/Tabela/Tabla/図/表/그림/표; list = starts with list marker; label = <= 3
  words and small box).
* `PageInfo.image_bboxes` from `page.get_image_info(xrefs=True)` (deduplicated, inside the page).
* Rotated/vertical text: detect via `line["dir"]`; set `style.rotation` to the PyMuPDF `rotate` value
  (90 = text runs upward, 270 = downward, 180 = upside down) and `is_vertical` for CJK vertical writing
  (dir == (0, 1)/(0,-1)); these segments are still translated.

### `mathtrans/layout.py` (re-rendering translated text into the PDF)
```python
def render_document(src_pdf, doc: TranslatedDocument, out_pdf, *, min_font_scale=0.55,
                    fonts_dir=None, pages: list[int] | None = None) -> list[RenderInfo]
def render_page_previews(pdf, out_dir, dpi=110, pages=None) -> list[str]   # PNG per page, "page-001.png"
def segment_html(seg: TextSegment, text: str) -> str                         # HTML for insert_htmlbox
```
* Per page: add one redaction per TEXT segment that has a translation (`seg.bbox` shrunk by 0.3pt),
  `page.apply_redactions(images=pymupdf.PDF_REDACT_IMAGE_NONE, graphics=pymupdf.PDF_REDACT_LINE_ART_NONE)`
  so images, rules, table borders and backgrounds survive; then `page.insert_htmlbox(rect, html,
  css=..., scale_low=min_font_scale, archive=..., rotate=seg.style.rotation)` with the original
  font size, colour (`#rrggbb`), weight, italic, alignment and line-height. `insert_htmlbox` returns
  `(spare_height, scale)`; store them in `seg.render`. If `scale == 0` / the text does not fit even at
  `scale_low`: the implemented attempt order is (1) original box at full size, (2) the box grown into
  free space at full size (downward ≤ 1.5 × height, sideways within the column: a wide text block to
  one side acts as a column wall), (3) the grown box shrunk down to `min_font_scale`, (4) the same with
  the tighter line height 1.1, (5) otherwise unlimited shrinking (PyMuPDF writes nothing when the text
  does not fit at `scale_low > 0`) with `render.overflow=True` (QA reports it and asks for a shorter text).
* Image-text segments are *not* rendered here (see `images.render_image_segments`).
* Use `fonts.html_font_setup(doc.target_lang, fonts_dir)` for CSS/Archive; built-ins already cover all
  six languages. Translated text must stay real, extractable text (editable PDF) — never rasterise.
* `render_document` must not alter page sizes, page count, image placements or vector graphics.

### `mathtrans/export.py`
```python
def make_bilingual_pdf(src_pdf, translated_pdf, out_path) -> str   # each output page = original | translation side by side (page.show_pdf_page)
def export_docx(translated_pdf, out_path, doc: TranslatedDocument | None = None, timeout=180) -> str
```
* DOCX: use LibreOffice when available (`soffice --headless --infilter="writer_pdf_import" --convert-to docx --outdir ...`);
  fallback: python-docx document built from `doc.segments` in reading order (headings, paragraphs,
  images extracted from the translated PDF). Always produce a file.

### `mathtrans/ocr.py` + `mathtrans/images.py` (text inside images)
```python
class RapidOcrEngine:  name = "rapid";  recognize(image_rgb, hint_langs=None) -> list[OcrResult]
class ClaudeVisionOcrEngine: name = "claude"; __init__(client=None, model=None); recognize(...)   # JSON list of {text, box [x0,y0,x1,y1] in 0-1000 normalised coords}
class NullOcrEngine: name = "none"
def get_ocr_engine(name: str, settings) -> OcrEngine            # auto → rapid if importable else claude if API key else none

def extract_image_segments(pdf_path, doc: TranslatedDocument, engine, *, min_confidence=0.6,
                           min_image_px=40, pages=None) -> list[TextSegment]   # appends nothing; caller extends doc.segments
def render_image_segments(pdf_doc: pymupdf.Document, doc: TranslatedDocument, *, fonts_dir=None) -> int  # images modified in place
```
* Group by xref (an image can be placed on several pages). Skip tiny images, masks (`smask`
  images themselves), and OCR results that are pure numbers / single Latin letters / math only
  (`is_fully_protected`) — those stay as they are.
* Rendering: estimate the background colour from a 2-px ring around the box (median), fill the
  box (or `cv2.inpaint` when the ring is not uniform), estimate the text colour as the box pixel
  colour most distant from the background, draw the translation with `fonts.pil_font` at the
  largest size that fits the box (height first, then shrink for width; allow 2 lines for wide
  boxes), then `page.replace_image(xref, stream=png_bytes)` (keep the original pixel size; keep
  alpha if the source had it). Store what was done in `seg.render`.

### `mathtrans/scanned.py` (scanned pages, overlay mode)
```python
def is_scanned_page(page) -> bool                      # no text layer and one image covering >= 85 % of the page
def scanned_pages(pdf, pages=None) -> set[int]
def group_ocr_lines(lines, page_index, source_lang) -> list[TextSegment]   # IMAGE_TEXT lines -> paragraph TEXT segments (origin="ocr", members=[line ids])
def build_overlay_segments(doc, scanned) -> list[TextSegment]
def erase_merged_lines(pdf_doc, doc) -> int            # erase the merged lines' pixels (flat fill / inpaint) and replace the page images
```
* `PipelineOptions.scanned_mode`: `overlay` (default) groups the OCR lines of scanned pages into homogeneous
  paragraphs (prose only; formula / number lines stay in the picture), marks the lines
  `translate=False, skip_reason="merged into paragraph <id>"`, erases them from the image after the layout stage
  and lets the paragraphs flow through translation, QA and `layout.render_document` like native text
  (editable output). `repaint` keeps the old behaviour (`images.render_image_segments` paints into the image).
* Paragraph style: font size = 0.82 × median line height, line height from the line pitch, centred when every
  line is centred in the union box, role heading / label / body by size and length.

### `mathtrans/translate/` (translation backends)
```python
# translate/base.py
class BaseTranslator: name; translate(items, src, tgt, glossary_pairs, doc_context="") -> list[TranslationResult]
def chunk_items(items, max_chars) -> list[list[TranslationItem]]
# translate/claude.py
class ClaudeTranslator(BaseTranslator): __init__(client=None, model=None, effort=None, enable_fallbacks=None, settings=None, max_chars=None)
class ClaudeReviewer: __init__(client=None, model=None, settings=None); review(items, src, tgt, glossary_pairs) -> list[ReviewFinding]
def make_client(settings) -> anthropic.Anthropic
# translate/mock.py
class MockTranslator(BaseTranslator): deterministic offline translator (glossary + built-in mini dictionary + pseudo-translation in the target script); options to inject faults for QA tests (e.g. drop_placeholders=True, leave_untranslated=True)
class MockReviewer: returns no findings (or findings for texts containing "[[BAD]]")
# translate/__init__.py
def get_translator(name, settings, model=None) -> BaseTranslator
def get_reviewer(name, settings, model=None) -> Reviewer | None
def translate_segments(doc: TranslatedDocument, translator, *, max_chars, doc_context="", only_ids=None, progress=None) -> None
    # builds TranslationItems from seg.protected_text (+ context, feedback, previous), calls translator in chunks,
    # fills translation_raw / translated_text (restore_placeholders), increments attempts, clears feedback
```
* Claude backend: official `anthropic` SDK (>= 1.0). Model from settings (`claude-opus-5-5`), adaptive
  thinking (omit `thinking`), `output_config={"effort": settings.claude_effort, "format": {json_schema}}`,
  `max_tokens` 16000, structured JSON output `{"translations": [{"id", "text"}]}`; stable cached system
  prompt (`cache_control` ephemeral) with the rules: keep every `⟦n⟧` placeholder exactly once and in a
  sensible position, never translate inside placeholders, keep list markers / numbering / line breaks,
  follow the glossary pairs, keep length close to the original (space-constrained labels get `max_chars`),
  textbook register, no explanations, output JSON only. Enable server-side refusal fallbacks by
  default (`client.beta.messages.create(..., betas=["server-side-fallback-2026-07-01"], fallbacks="default")`)
  when `settings.enable_fallbacks`; otherwise `client.messages.create`. Handle `stop_reason == "refusal"`
  → `TranslationRefused`, `max_tokens` → split the chunk and retry, missing ids → retry those ids once,
  placeholder problems → retry once with feedback, typed SDK errors (`anthropic.RateLimitError`,
  `APIStatusError`, `APIConnectionError`) → `TranslationError` with a clear message. Never call the
  network in tests: unit-test with a fake client object exposing the same `.messages.create` /
  `.beta.messages.create` surface.

### `mathtrans/qa/` (automatic multi-dimensional QA)
```python
# qa/checks.py — each check: (doc, options) -> list[QAIssue]; names are stable identifiers
completeness, placeholders, numbers, untranslated, target_script, glossary, length_ratio, formatting, layout_fit, image_text
def rule_checks(doc, options, pairs) -> list[QAIssue]
def output_checks(out_pdf, src_pdf, doc) -> list[QAIssue]       # page count/sizes, image bboxes unchanged (±1pt), translated text extractable on each page, no source-script leftovers outside protected fragments, fonts embedded
# qa/loop.py
def run_qa_loop(doc, options, *, glossary_pairs, retranslate: Callable[[list[str]], None], reviewer=None,
                render_check: Callable[[TranslatedDocument], list[QAIssue]] | None = None, progress=None) -> QAReport
    # round r: issues = rule_checks + reviewer findings (as QAIssues; meaning/omission/number/terminology/untranslated → error, else warning)
    #          + render_check(doc) (layout issues, when provided); passed when no "error" issues
    #          else: fixable segment ids ← append feedback to seg.feedback (issue messages + for layout: "shorten to <= N chars"),
    #          call retranslate(ids) (the pipeline wires this to translate_segments(only_ids=ids)), next round; stop at options.max_qa_rounds
    #          The loop never imports mathtrans.translate — it only uses the callback.
# qa/report.py
def report_markdown(report: QAReport, doc) -> str
def summarize(report) -> str
```
* `numbers`: multiset of digit sequences in `source_text` must appear in `translated_text` (CJK
  numerals 一二三 and placeholders restored count as present). `untranslated`: `foreign_letters`
  (letters of the source script that are not valid in the target script) outside protected fragments
  must be 0, with an allowance of <= 2 characters for tiny labels. `target_script`: `script_ratio`
  >= 0.6 for segments with >= 4 letters. `length_ratio`: warning outside [0.35, 3.0] × expected
  `length_vs_zh` ratio. `formatting`: list marker preserved, no "Translation:" / JSON / quotes
  wrapping, no raw `⟦` left in `translated_text`, terminal punctuation class preserved for sentences.
  `layout_fit`: `seg.render.overflow` or `scale < min_font_scale` → error with a `max_chars` hint.

### `mathtrans/pipeline.py` (integration — written by the integrator)
```python
def run_pipeline(source_pdf, out_dir, options: PipelineOptions, settings=None, progress: ProgressCallback | None = None,
                 *, translator=None, reviewer=None, ocr_engine=None) -> PipelineResult   # keyword-only backend overrides (tests)
```
Stages/percent: extract 5 → ocr 15 → translate 45 → qa 70 → layout 85 → output checks 90 → exports 97 → previews 100.
Writes `out_dir/output.pdf`, `segments.json`, `qa_report.json`, optional `bilingual.pdf`, `output.docx`,
`previews/page-001.png`. `status="qa_failed"` when `require_qa_pass` and the report did not pass:
the output files are still written for inspection but the API refuses to serve them unless `force=1`.

### `mathtrans/projects.py`, `mathtrans/api.py`, `mathtrans/cli.py`, `mathtrans/web/index.html`
```python
class Project(BaseModel): id, name, created_at, updated_at, source_file, source_lang, target_lang, options (dict), glossary_id,
                          batch_id, status: queued|running|completed|qa_failed|error, progress {stage,message,percent}, result: PipelineResult|None, error, history: list[dict]
# the API stores `glossary_id` on the project and rebuilds PipelineOptions.glossary from data/glossaries/<id>.json at run time
class ProjectStore: __init__(data_dir); create(name, pdf_bytes, options, glossary_id=None, batch_id=None) -> Project; get(id); list(batch_id=None);
                    update(project); delete(id); project_dir(id); save_glossary(glossary) / get_glossary(id) / list_glossaries()
def create_app(settings=None, runner=None) -> FastAPI   # runner defaults to pipeline.run_pipeline (injected in tests)
```
REST: `GET /api/languages`, `POST /api/glossaries` (file or text), `GET /api/glossaries`, `GET /api/glossaries/template`,
`POST /api/projects` (multipart: one or more `files`, `target_lang`, optional `source_lang`, `glossary_id`,
`translate_images`, `bilingual`, `export_docx`, `max_qa_rounds`, `require_qa_pass`) → creates one project per
file (shared `batch_id`) and queues them; `GET /api/projects`, `GET /api/projects/{id}`, `POST /api/projects/{id}/retranslate`
(new target_lang / glossary → new run, history kept), `GET /api/projects/{id}/qa` (JSON + `?format=md`),
`GET /api/projects/{id}/preview/{page}` (PNG), `GET /api/projects/{id}/download?format=pdf|bilingual|docx|segments[&force=1]`,
`DELETE /api/projects/{id}`, `GET /` serves `web/index.html` (vanilla JS: upload multiple files, choose languages,
paste/upload glossary, toggle options, project table with live status, QA report panel, preview strip, downloads).
CLI (`python -m mathtrans.cli` / `mathtrans`): `translate IN.pdf --to en [--from zh] [--glossary g.csv] [--out DIR]
[--bilingual] [--docx] [--no-images] [--translator mock|claude] [--max-rounds N] [--no-require-qa]`, `serve [--host] [--port]`,
`sample OUT.pdf [--lang zh]`, `glossary-template OUT.csv`.
