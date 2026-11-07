export const meta = {
  name: 'leftover-chinese-pass',
  description: 'Targeted pass over the Chinese still visible in a translated textbook volume: agents translate what carries meaning and keep only decoration, writing corrections to files',
  phases: [{ title: 'Review', detail: 'one agent per batch of pages with leftover Chinese' }],
}
// args: { volumes: [{ code, title, items: {"12": [{"text", "box", "how", "ids"}...], ...} }], batch: 6 }
// (items built by production/leftover_items.py from the OCR of the rendered pages, the dropped paragraphs and the smaller instructions)
const BATCH = (args && args.batch) || 6

const RESULT_SCHEMA = {
  type: 'object',
  properties: {
    code: { type: 'string' }, pages: { type: 'string' },
    corrections_written: { type: 'integer' }, kept: { type: 'integer' }, file: { type: 'string' },
    flags: { type: 'array', items: { type: 'object', properties: {
      page: { type: 'integer' }, issue: { type: 'string' } }, required: ['page', 'issue'] } },
    summary: { type: 'string' },
  },
  required: ['code', 'pages', 'corrections_written', 'kept', 'file', 'flags', 'summary'],
}

function prompt(v, pages, items, file) {
  const dir = `/tmp/piptest/real/proof/${v.code}`
  const S = '/home/user/math-material-translation/production'
  return `You check an English translation of a Chinese primary-school mathematics textbook (北师大版 ${v.title}) for Chinese that is
STILL VISIBLE on the translated pages, and you remove every piece of it that a reader of the English book needs, using the
correction tools below. The book was translated automatically (OCR of scanned pages, machine translation, English set over the
cleaned page images) and proofread twice; what is left is Chinese the pipeline did not translate, or that a proofreader DROPped
(kept in the picture) when it would not fit - the layout has since improved (bubbles, side labels set up the side, more room).

Your pages (1-based, as in the files): ${pages.join(', ')}. For each page P (three digits):
- ${dir}/pP_src.png and ${dir}/pP_out.png: the Chinese page and the translated page as rendered now (75 dpi; look at both).
- ${dir}/pP.json: the page's paragraphs (id, source, translation, box in PDF points, note) and chinese_left_in_picture (OCR lines
  the pipeline left untranslated, each with its "id", "why" and "box").
- THE ITEMS TO DECIDE (Chinese still visible on the rendered page, found by OCR of the output, plus paragraphs a proofreader
  dropped), page by page; "box" is in PDF points; "ids" are the paragraphs or OCR lines under it:
${items}

For EACH item decide, looking at the pictures, one of:
- KEEP: the Chinese is decoration that an English edition would keep as printed - the publisher's diagonal watermark
  (北京师范大学出版社, often misread as 帅/版社/服社/师莎), a Chinese character shown as a shape (symmetric characters like 王 中 田 囍,
  the 正 tally marks the lesson teaches), calligraphy or 福 decorations, coin and banknote inscriptions, a pupil's handwritten
  working that is maths only, a stray OCR misreading of a line, a dot or a picture part. Count it in "kept"; write nothing.
- TRANSLATE: anything with meaning for the reader - a sign or banner (终点 = "Finish", 火车站 = "Station", 欢迎新同学 = "Welcome,
  new classmates!"), a label on an object in an exercise (牙膏 = "toothpaste", 语文/数学 on book covers = "Chinese"/"Maths"), a name
  tag (小秀 = "Xiaoxiu"), a word in a sentence or bubble, a unit (米 = "m"), a lesson or unit title, a question or instruction. Use
  the tool that fits:
  * a dropped or empty paragraph (its id is a paragraph "pN_sK"): {"segment_id": "p65_s16", "translation": "Station", "reason": "..."}
    (add "box": [x0, y0, x1, y1] to give it more room inside the same sign, cell or bubble when it would be too small);
  * an OCR line left in the picture (its id is "pN_iM_K"): {"line": "p66_i264_10", "translation": "...", "force": true, "reason": "..."};
    when that line is part of a sentence whose other part is a paragraph, then also merge, in this order:
    {"merge": ["p66_s9", "p66_i264_10_t"], "translation": "the whole sentence", "reason": "..."};
  * a line mixing words with pictures or printed blanks (🐰比🐥（多，少）, □◯□ boxes): translate only its words in place, each in the
    x-range (PDF points) it occupies, the pictures and blanks staying: {"line": "p20_i80_3", "pieces": [[291, 309, "vs"],
    [332, 417, "(more, fewer)"]], "reason": "..."} ("BLANK" erases a piece and sets nothing, e.g. a Chinese full stop; a piece
    may give its own height: [x0, x1, "text", y0, y1]); 比 between two pictures reads "vs";
  * Chinese with no paragraph or line under it ("ids" empty): {"add": "p65_a1", "page": 65, "box": [74, 220, 92, 230],
    "translation": "Finish", "source": "终点", "reason": "..."} - the page number in "add"/"page" is the N of the page's paragraph ids
    (pN_...), which is the file's page number minus 1; the box is erased exactly and the English set there (centred, sized to the box;
    give a box a little wider than the Chinese when the English is longer and there is plain room around it);
  * a label written top to bottom (one character under another): translate it normally - it is set up the side automatically.
  To read exact positions you may run: python3 ${S}/ruler.py ${v.code} <page index> x0 y0 x1 y1
  <out.png> 3 (page index = file page number minus 1; the png has point rulers on the top and left) and look at the png.
- SMALLER items (their "how" starts with SMALLER) are not Chinese: a numbered instruction set smaller than the other
  numbered instructions of its page, because its English did not fit where it stands. The same kind of text must have the
  same size; a new line is better than shrinking. Make it fit at the page's size (look at the page; "how" gives the size
  and how wide the English is at that size):
  * when the line runs into a picture or the next row, reword it shorter with exactly the same meaning and maths (no
    word of the task lost: "2. What is the largest number that fits in (   )?" -> "2. Fill in the largest possible number.");
  * when there is free paper below or beside it, break it with "\n" where a second line fits, or give it a "box" over the
    free paper (never over a picture, a table or other text);
  * {"segment_id": "p16_s6", "translation": "...", "box": [x0, y0, x1, y1], "reason": "..."} (box optional).
  If nothing fits without harming the page, leave it and count it in "kept".
- FLAG: something you cannot fix with these tools (the Chinese sits on a busy picture so erasing would damage it, no room at all).

A one-character label on a geometry figure that is "left in source language" (no room for a word) takes the standard letter of
English diagrams: 高 = "h" (height), 底 = "b" (base), 长 = "l", 宽 = "w"; a map label that does not fit gets a "box" over the free
paper next to it (never over another label or the coast line).
Rules: English must be correct, natural and short enough for its place; character names in pinyin (淘气 Taoqi, 笑笑 Xiaoxiao, 奇思 Qisi,
妙想 Miaoxiang, 智慧老人 Wise Old Man, 机灵狗 Clever Dog); yuan as ¥3; metric units as "2 m". Never translate the same text twice
(check the page's paragraphs: a line may already be covered by a paragraph's English - then the leftover Chinese is a remnant: give it
"BLANK" via its line or an add with "BLANK"). Do not touch anything that is not in your items.

Write ONE file ${file} (use the Write tool) with exactly this shape:
{"corrections": [ ...entries as above... ], "kept": [{"page": 12, "text": "福", "why": "decoration"}],
 "flags": [{"page": 12, "issue": "..."}]}
Write the file even when everything is kept. Then return the structured summary.`
}

const jobs = []
for (const v of args.volumes) {
  const data = { pages: v.items }
  const pages = Object.keys(data.pages).map(Number).sort((a, b) => a - b)
  for (let i = 0; i < pages.length; i += BATCH) {
    const chunk = pages.slice(i, i + BATCH)
    const items = chunk.map(p => `  page ${String(p).padStart(3, '0')}:\n` + data.pages[String(p)].map(it =>
      `    - ${JSON.stringify(it)}`).join('\n')).join('\n')
    const tags = chunk.map(n => String(n).padStart(3, '0'))
    jobs.push({ v, pages: tags, items, file: `/tmp/piptest/real/proof/${v.code}/corr_lc_${tags[0]}.json` })
  }
}
log(`${jobs.length} leftover-Chinese batches over ${args.volumes.length} volume(s)`)
phase('Review')
const results = await parallel(jobs.map(j => () => agent(prompt(j.v, j.pages, j.items, j.file),
  { label: `lc:${j.v.code}:${j.pages[0]}-${j.pages[j.pages.length - 1]}`, phase: 'Review', schema: RESULT_SCHEMA })))
const ok = results.filter(Boolean)
const failed = jobs.filter((j, i) => !results[i]).map(j => `${j.v.code}:${j.pages[0]}`)
log(`${ok.length}/${jobs.length} batches done; corrections: ${ok.reduce((n, r) => n + (r.corrections_written || 0), 0)}, kept: ${ok.reduce((n, r) => n + (r.kept || 0), 0)}`)
return { done: ok.length, failed, corrections: ok.reduce((n, r) => n + (r.corrections_written || 0), 0),
  kept: ok.reduce((n, r) => n + (r.kept || 0), 0),
  flags: ok.flatMap(r => r.flags.map(f => ({ code: r.code, ...f }))).slice(0, 300) }
