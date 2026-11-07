export const meta = {
  name: 'proofread-volumes-pass-n',
  description: 'Further proofreading pass (args.pass) on the corrected rendering of a translated textbook volume: agents compare source and output pages and write the remaining corrections to files',
  phases: [{ title: 'Proofread', detail: 'one agent per batch of pages' }, { title: 'Check', detail: 'an independent agent renders each batch of corrections and repairs what is wrong' }],
}
// args: { volumes: [{ code, title, pages: [n, ...] }], batch: 8 }
const BATCH = (args && args.batch) || 8
const T = '/home/user/math-material-translation/production'  // the production tools
const W = '/tmp/piptest/real'  // the work folder (BNU_WORK)
const PASS = (args && args.pass) || 3

const RESULT_SCHEMA = {
  type: 'object',
  properties: {
    code: { type: 'string' }, pages: { type: 'string' },
    corrections_written: { type: 'integer' }, file: { type: 'string' },
    flags: { type: 'array', items: { type: 'object', properties: {
      page: { type: 'integer' }, issue: { type: 'string' } }, required: ['page', 'issue'] } },
    summary: { type: 'string' },
  },
  required: ['code', 'pages', 'corrections_written', 'file', 'flags', 'summary'],
}

function prompt(v, pages, file) {
  const dir = `${W}/proof/${v.code}`
  return `You are the final proofreader of an English translation of a Chinese primary-school mathematics textbook
(北师大版 ${v.title}). The translation was produced automatically: OCR of scanned pages, machine translation, and English
text laid over the cleaned page images. Your job: make every translated text on your pages correct, natural, child-appropriate
English that a native-speaking maths teacher would accept, consistent with what the picture shows.

${PASS === 1 ? `THIS IS THE FIRST PASS OF THE REBUILD: the English is a fresh machine translation, with the English of the checked
edition carried over where it could be matched to a paragraph. What you see is the current state of the book. `
  : `THIS IS PROOFREADING PASS ${PASS}. Your pages were already proofread ${PASS - 1} time${PASS === 2 ? '' : 's'} and those corrections have been applied: what you see
is the current state of the book. `}Report only what is STILL wrong. Look especially for: (a) paragraphs whose note says
"left in source language" or that were shrunk (scale under 0.7) - supply a shorter English that keeps the meaning so the text
can be set; (b) English that does not match what the picture shows (counted nouns, who speaks, what is compared);
(c) grammar, number agreement and unnatural phrasing; (d) a translation that is wrong or incomplete for its fragment;
(e) OCR noise set as text (restore the picture with DROP) and a line printed twice (erase the duplicate with BLANK).
Two special translations are allowed: "DROP" restores the original picture for that paragraph (OCR noise, hand lettering,
decorative text, a label that must not be printed outside its cell) and "BLANK" erases it and prints nothing (a duplicate
read of a line that is printed elsewhere). Leave good translations alone; do not re-request layout changes.

Your pages (1-based): ${pages.join(', ')}. For each page P (three-digit, e.g. 007):
- ${dir}/pP_src.png  the original Chinese page (look at it with the Read tool)
- ${dir}/pP_out.png  the translated page as rendered now (look at it too)
- ${dir}/pP.json     the page's translated paragraphs: id, role, source (Chinese, "[picture]" marks an inline picture),
  protected (the text sent to the translator: ⟦n⟧ placeholders stand for verbatim fragments - numbers, formulas,
  answer blanks - and for inline pictures), translation (current English WITH the same ⟦n⟧ placeholders), shown (what is printed,
  placeholders restored), scale/note (layout: "left in source language" means the English did not fit and the Chinese was kept),
  "lines" (for a paragraph made of several OCR lines: the Chinese of each line, in reading order), and
  chinese_left_in_picture (Chinese lines the pipeline deliberately did not translate).

For every paragraph whose English is wrong or poor, write a corrected translation. Fix: mistranslations and changed meaning;
omissions or additions; unnatural or non-idiomatic English; grammar (number agreement 1 apple / 2 apples, articles, tense);
terminology (standard UK primary maths terms, British spelling - metre, colour, centre, maths: number sentence, column method (竖式), tens/ones, counting frame, sticks, more/fewer,
"How many more ... than ...?"); character names in pinyin (淘气 Taoqi, 笑笑 Xiaoxiao, 奇思 Qisi, 妙想 Miaoxiang, 智慧老人 Wise Old Man,
机灵狗 Clever Dog); measure words in brackets after an answer blank (use the counted noun from the picture or the exercise, e.g.
"(apples)", or drop the brackets; never "(pieces)", "(items)", "(count)"); multiplication-table rhymes as facts (三七二十一 =
"3 × 7 = 21"); yuan amounts as ¥3; keep list enumerators (1. (2) ①) at the start. Use the pictures to decide what is counted or
compared, who speaks, and what an inline [picture] is (put its placeholder where that word belongs in English).
Fragments: OCR sometimes splits one sentence into several paragraphs (look at the pages); translate each fragment so the pieces read
correctly together in their positions. Numbers written in Chinese words (七十七) become English words ("seventy-seven") when the exercise
is about reading or writing numbers, digits otherwise. A lone measure word after an answer blank (个, 只) becomes the counted noun
from the picture ("apples"), never "(items)". Place-value labels (十位/个位 over a column-method sum or a counting frame) are "Tens"/"Ones" (T/O where a cell is too narrow); 答： is "Answer:"; single-character
column labels of a counting frame (万 千 百 十 个) are the standard abbreviations TTh Th H T O (they must fit one-character cells). For paragraphs with note "left in source language", write a SHORTER English that keeps the
meaning (labels: 1-3 words) so it can fit.

HARD RULES for each corrected translation:
- Start from the "protected" text and keep EVERY ⟦n⟧ placeholder of it exactly once, unchanged (you may move them).
  Never write the placeholder's content instead of the placeholder; never invent new ⟦n⟧. Two exceptions, checked
  against the page image: a placeholder that stands for OCR noise (an inline [picture] that is a crop of a stray Chinese
  character, of a bubble outline or of a dotted pattern; an enumerator read twice) is LEFT OUT; a placeholder whose
  fragment is a misread number (the image says 96, the fragment says 9) is replaced by the correct number written out.
  Say which in the reason ("dropped ⟦2⟧: OCR crop of 示").
- Keep it about as long as the current one (shorter is better when the note says it was shrunk or left in Chinese),
  but never abbreviate ("Ans:", "Qty", "ea." are wrong): shorten by dropping optional words instead.
- Measure-word labels right after an answer box (□（个）) are erased on purpose (English books write "13 − 9 = □");
  do not ask for them back.
- Only correct real problems; leave good translations alone. Do not touch ids that are not in the JSON.

FIVE STRUCTURAL FIXES are also allowed, each as its own entry in "corrections":
- BOX: when a translation is set too small (scale under 0.7) or wraps badly because its box is tight while free room lies
  right next to it (the rest of a banner, ribbon, bubble or cell; blank paper), give it a new box in PDF points:
  {"segment_id": "p40_s24", "box": [100, 456, 180, 479], "reason": "..."}. The new box must overlap the old one, stay
  inside the same banner, bubble or cell, cover no other text or important part of the picture, and be at most six
  times the old area.
- TRANSLATE A LINE that the pipeline left in Chinese in the picture (an entry of chinese_left_in_picture, by its "id"):
  {"line": "p9_i36_14", "translation": "TM", "reason": "..."}. It is erased and the English is set in its place. Only for
  lines whose box holds nothing but that text - a column or place-value label, a unit label (60米 = "60 m"), a lone
  character label (图 = "Figure"), a whole line of text; lines whose "why" says slanted text or watermark are refused.
  A line whose "why" says "inline pictograms" is often a FALSE ALARM: the pipeline takes every line with 比 ("ratio",
  "compare": 比的认识, 写出比, 比值是, 百分比, 对比) or ending in 的面 for a sentence whose little pictures were dropped. Look at
  the page image: when the line's box holds only Chinese text (no little pictures between the characters), translate it
  with "force": {"line": "p72_i288_1", "translation": "Understanding Ratios", "force": true, "reason": "..."}. When such a
  line is only part of a sentence whose other part is a paragraph (the line before or after it), translate the line AND
  then merge the two, in this order, using the new paragraph id "<line id>_t":
  {"line": "p30_i120_21", "translation": "saved", "force": true, ...}, {"merge": ["p30_s9", "p30_i120_21_t"],
  "translation": "the whole sentence", ...}. Real pictogram lines (pictures inside the box) stay refused: flag them.
- SPLIT a paragraph that joins lines which are NOT one text (the cells of a table column printed as one run of prose,
  labels of different pictures, two questions): {"split": "p104_s19", "translations": ["Item", "Original class fund", ...],
  "reason": "..."} with exactly one English text per entry of its "lines" list in pP.json, in that order ("DROP" or "BLANK"
  allowed for a line). Each line is then set on its own place. A paragraph of ONE line that runs over several table cells
  ("三（1）班三（2）班" over two header cells) is cut at x positions in PDF points (the cell borders):
  {"split": "p64_s29", "at": [204], "translations": ["Class 3 (1)", "Class 3 (2)"], "reason": "..."} - one more text than cuts.
- MERGE the fragments of ONE sentence or question that the OCR split into separate paragraphs (they print at different
  sizes, overlap, or wrap badly): {"merge": ["p38_s17", "p38_s18", "p38_s19"], "translation": "the whole English text,
  written out in full with its numbers (no ⟦n⟧ placeholders)", "reason": "..."}. The first id keeps the paragraph, set over
  all their boxes. Only for pieces that stand together (one under the other, or side by side on one row) and read as one
  text; never merge the cells of a table, the labels of different pictures, or two different speakers.
- ERASE Chinese that a paragraph's OCR box left in the picture beside it (a character before or after the line, a full stop,
  the rest of the line): {"segment_id": "p48_s10", "erase": [[x0, y0, x1, y1]], "reason": "..."}. Coordinates are PDF points
  like the "box" of each paragraph in pP.json; the png images are 75 dpi, so points = pixels x 0.96. Each box must be small
  (at most about four line heights tall), lie on the same picture right next to that paragraph, and hold only the leftover
  Chinese: the dark glyphs inside it are erased. Add "translation" to the same entry when the English must now also say what
  the erased words said.

A one-character label on a geometry figure that is "left in source language" (no room for a word) takes the standard letter of
English diagrams: 高 = "h" (height), 底 = "b" (base), 长 = "l", 宽 = "w"; a map label that does not fit gets a "box" over the free
paper next to it (never over another label or the coast line).

SAME SIZE: a page's pP.json may list "smaller_than_siblings" - numbered instructions set smaller than the other numbered
instructions of the page because their English did not fit where it stands ("how" gives the page's size and how wide the
English is at that size). Same kind of text, same size; a new line is better than shrinking. Where the line runs into a picture
or the next row, reword it shorter with exactly the same meaning and maths ("2. What is the largest number that fits in (   )?"
-> "2. Fill in the largest possible number."); where there is free paper below or beside it, break it with "\n" or give it a
"box" over that free paper (never over a picture, a table or other text). Leave it when nothing fits without harming the page.

CHINESE STILL VISIBLE: a page's pP.json may list "chinese_visible_on_output" - Chinese found by OCR on the rendered page, or a
paragraph a proofreader DROPped (kept in the picture), each with "text", "box" (PDF points), "how" and "ids" (the paragraphs or OCR
lines under it). Decide each one. KEEP (write nothing) what an English edition keeps as printed: the publisher's diagonal watermark
(北京师范大学出版社, often misread as 帅/版社/服社), a Chinese character shown as a shape (王 中 田 囍, the 正 tally marks the lesson
teaches), 福 and calligraphy decorations, coin and banknote inscriptions, a pupil's handwritten working that is maths only, an OCR
misreading of a line or a picture part. TRANSLATE everything with meaning (a sign, banner, label on an object, name tag, unit, title,
a word in a sentence or bubble) with the tool that fits: a dropped paragraph by its id ({"segment_id": ..., "translation": ...},
with a "box" for more room inside the same sign or bubble); an OCR line by "line" with "force": true (and MERGE with its
sentence's paragraph if it is part of one); a line mixing words and pictures or printed blanks by "pieces" - each word in the
x-range it occupies: {"line": "p20_i80_3", "pieces": [[291, 309, "vs"], [332, 417, "(more, fewer)"]], "reason": "..."}
("BLANK" erases a piece and sets nothing; 比 between two pictures reads "vs"); text with no id under it by ADD:
{"add": "p65_a1", "page": 65, "box": [74, 220, 92, 230], "translation": "Finish", "source": "终点", "reason": "..."} where the page
is the N of the page's paragraph ids (pN_...) and the box is erased exactly and the English set there. Flag what cannot be fixed.

THE CHECKED EDITION: this volume was proofread before, page by page, and that checked English edition was delivered; the work
files behind it were lost, so the book is being rebuilt from a fresh machine translation. A page's pP.json names
"old_checked_edition": pP_old.png shows that page of the checked edition. Compare it with pP_out.png: carry over every fix it shows
that the current page lacks (its English wording, sentences joined or split, Chinese translated or erased, labels set in place,
sizes) with the tools below - unless the current page is already right. The checked edition is not perfect: never copy a flaw of
it (Chinese left, overlap, text too small, a wrong translation). Many paragraphs already carry its English (corr_000_recovered).

SEE AND TRY BEFORE YOU WRITE (run with Bash; PYTHONPATH=/home/user/math-material-translation): the pP_out.png pictures show the
last full render. To see a page as it renders now: python3 ${T}/preview_pages.py ${v.code} <page>[,<page>] --dpi 110 (-> ${W}/previews/preview_${v.code}_<page>.png,
source left, English right). To try corrections before writing them, put {"corrections": [...]} in a scratch file of your own (name it after
your volume and first page, e.g. /tmp/try_${v.code}_${pages[0]}.json: other agents run at the same time) and run
python3 ${T}/try_fix.py ${v.code} <page>[,...] <file> <tag> (prints applied/rejected, renders ${W}/previews/try_<tag>_${v.code}_<page>.png);
zoom into details with python PIL. Try every structural fix (box, line, pieces, add, erase, restore, paint) and look at the result.
Two pixel fixes are also allowed: {"restore": [x0, y0, x1, y1], "page": N} puts the source scan's pixels back in the box (an outline,
answer box or picture part an erase damaged - no Chinese may come back with it); {"paint": [x0, y0, x1, y1], "page": N, "colour":
"border" | [r, g, b]} fills the box flat (a plate whose Chinese cannot be erased cleanly, before an add sets English on it).
Text with no paragraph or line under it is set with an ADD: {"add": "pN_aK", "page": N, "box": [x0, y0, x1, y1], "translation":
"...", "source": "终点", "size": 9, "align": "left", "reason": "..."} (N = the page index of the page's ids; the box is erased
exactly and the English set there). A line mixing words with pictures or printed blanks takes "pieces":
{"line": "pN_iM_K", "pieces": [[x0, x1, "words"], [x0, x1, "BLANK"]], "reason": "..."}.

Write ONE file ${file} (use the Write tool) with exactly this JSON shape:
{"corrections": [{"segment_id": "p12_s3", "translation": "English with ⟦0⟧ placeholders", "reason": "short reason"},
                 {"merge": ["p12_s7", "p12_s8"], "translation": "...", "reason": "..."},
                 {"segment_id": "p12_s9", "erase": [[230, 380, 300, 396]], "reason": "..."},
                 {"split": "p12_s11", "translations": ["...", "..."], "reason": "..."},
                 {"line": "p12_i48_20", "translation": "...", "reason": "..."},
                 {"line": "p12_i48_21", "translation": "...", "force": true, "reason": "only text in the box, no pictures"}],
 "flags": [{"page": 12, "issue": "a problem you cannot fix by text, line, split, merge, erase or box (erased picture, overlap, missing
translation of a line kept in Chinese, text too small)"}]}
Write the file even when there are no corrections ({"corrections": [], "flags": [...]}). Then return the structured summary.`
}

const jobs = []
for (const v of args.volumes) {
  for (let i = 0; i < v.pages.length; i += BATCH) {
    const pages = v.pages.slice(i, i + BATCH).map(n => String(n).padStart(3, '0'))
    jobs.push({ v, pages, file: `${W}/proof/${v.code}/corr_p${PASS}_${pages[0]}.json` })
  }
}
log(`${jobs.length} proofreading batches over ${args.volumes.length} volume(s)`)
function checkPrompt(v, pages, file) {
  return `You independently check the corrections another proofreader wrote for pages ${pages.join(', ')} of an English translation of a
Chinese primary-school maths textbook (北师大版 ${v.title}, code ${v.code}). They are in ${file} ({"corrections": [...], "flags": [...]}).
The proof files are in ${W}/proof/${v.code}/ (pPPP_src.png, pPPP_out.png, pPPP_old.png = the checked edition delivered earlier, pPPP.json).

Assume each correction may be wrong (scratch files you make: name them after ${v.code} and page ${pages[0]}; other agents run at the same
time). Render them (PYTHONPATH=/home/user/math-material-translation python3 ${T}/try_fix.py ${v.code}
<pages> ${file} chk) and compare each changed spot with the Chinese source half of the png and with pPPP_old.png, zooming in with
python PIL. For every entry: is the English correct, natural and complete for the Chinese and the picture (numbers, names, what is
counted)? Did it keep the ⟦n⟧ placeholders of its "protected" text? Did a box, line, pieces, add, erase, restore or paint damage
anything (a picture, an outline, a number, another label), leave Chinese, double a text, or set English too small? Did the page lose a
fix the checked edition had? Remove or repair a bad entry and add what is clearly missing on these pages; try again until the pages
are right. Keep the file's shape; rewrite it with the Write tool only if you change something. Return the structured summary for the
file as it stands after your check.`
}

phase('Proofread')
const results = await pipeline(jobs,
  j => agent(prompt(j.v, j.pages, j.file),
    { label: `proof${PASS}:${j.v.code}:${j.pages[0]}-${j.pages[j.pages.length - 1]}`, phase: 'Proofread', schema: RESULT_SCHEMA }),
  (r, j) => agent(checkPrompt(j.v, j.pages, j.file),
    { label: `check${PASS}:${j.v.code}:${j.pages[0]}-${j.pages[j.pages.length - 1]}`, phase: 'Check', schema: RESULT_SCHEMA }))
const ok = results.filter(Boolean)
const failed = jobs.filter((j, i) => !results[i]).map(j => `${j.v.code}:${j.pages[0]}`)
log(`${ok.length}/${jobs.length} batches done; corrections written: ${ok.reduce((n, r) => n + (r.corrections_written || 0), 0)}`)
return { done: ok.length, failed, corrections: ok.reduce((n, r) => n + (r.corrections_written || 0), 0),
  flags: ok.flatMap(r => r.flags.map(f => ({ code: r.code, ...f }))).slice(0, 400) }
