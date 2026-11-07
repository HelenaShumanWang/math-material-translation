export const meta = {
  name: 'flagged-defects-fix',
  description: 'Fix the defects earlier passes flagged on a translated textbook volume: one agent fixes and tries each group of pages, a second checks the result independently',
  phases: [
    { title: 'Fix', detail: 'one agent per group of flagged pages, trying each fix before writing it' },
    { title: 'Check', detail: 'an independent agent re-renders the fixes and corrects what is still wrong' },
  ],
}
// args: { volumes: [{ code, title, flags: [{ page, issue }] }], batch: 3 }  (page = 1-based file page)
const BATCH = (args && args.batch) || 3
const S = '/home/user/math-material-translation/production'

const RESULT = {
  type: 'object',
  properties: {
    pages: { type: 'string' }, file: { type: 'string' },
    fixed: { type: 'integer' }, left: { type: 'array', items: { type: 'object', properties: {
      page: { type: 'integer' }, issue: { type: 'string' } }, required: ['page', 'issue'] } },
    summary: { type: 'string' },
  },
  required: ['pages', 'file', 'fixed', 'left', 'summary'],
}

const TOOLS = (code) => `TOOLS (run them with Bash; page numbers 1-based as in the proof files, "page index" in corrections = that minus 1):
- See a page as it renders NOW (all corrections so far applied): python3 ${S}/preview_pages.py ${code} <page>[,<page>...] --dpi 110
  -> /tmp/piptest/real/previews/preview_${code}_<page>.png (source left, English right). Run with PYTHONPATH=/home/user/math-material-translation.
- Try corrections before writing them: put {"corrections": [...]} in a scratch file and run
  python3 ${S}/try_fix.py ${code} <page>[,...] <file> <tag>  -> prints what was applied/rejected and renders
  /tmp/piptest/real/previews/try_<tag>_${code}_<page>.png. Look at the png (crop/zoom with python PIL into your own png when details are small).
- Exact positions: python3 ${S}/ruler.py ${code} <page index> x0 y0 x1 y1 <out.png> 3
  (point rulers on the top and left; NOTE output.pdf is the last full render - use it for positions, the previews for the state).
- The page's paragraphs: /tmp/piptest/real/proof/${code}/pPPP.json (ids, source, translation, boxes in PDF points); the volume's
  current segments: /tmp/piptest/real/books/out_${code}/segments.json (read-only for you).

CORRECTIONS (JSON entries; boxes in PDF points; "page" = page index):
- {"segment_id": "pN_sK", "translation": "...", "reason": "..."}  ("DROP" keeps the Chinese in the picture, "BLANK" erases it and
  sets nothing); add "box": [x0, y0, x1, y1] to lay the paragraph out in another box (free paper of the same sign/cell/bubble).
- {"segment_id": "pN_sK", "erase": [[x0, y0, x1, y1], ...]}: also erase these small areas next to the paragraph (a leftover 。 or 个).
- {"segment_id": "pN_sK", "clip": [x0, y0, x1, y1]}: only the part of the paragraph's OCR lines inside the box is erased.
- {"merge": ["pN_sA", "pN_sB"], "translation": "...", "reason": "..."}: one sentence the OCR split.
- {"split": "pN_sK", "translations": ["...", ...]}: one paragraph per OCR line (cells, separate labels).
- {"line": "pN_iM_K", "translation": "...", "force": true}: an OCR line left in the picture, translated in place.
- {"line": "pN_iM_K", "pieces": [[x0, x1, "text"], [x0, x1, "BLANK", y0, y1], ...]}: only these x-ranges of the line are erased and
  re-set (pictures and printed blanks between them stay).
- {"add": "pN_aK", "page": N, "box": [x0, y0, x1, y1], "translation": "...", "source": "终点", "size": 8, "align": "left|center",
  "color": 2301728}: text the OCR never read; exactly the box is erased and the English set there ("BLANK" = erase only). Use a
  fresh id (pN_a<number not used on the page>).
- {"restore": [x0, y0, x1, y1], "page": N}: put the source scan's pixels back in the box (an answer box, bubble outline or picture
  part an erase damaged) - make sure no Chinese comes back with it, and nothing English is set there.
- {"paint": [x0, y0, x1, y1], "page": N, "colour": "border" | [r, g, b]}: fill the box flat ("border" = the colour of its edge):
  a sign's plate or a disc whose Chinese cannot be erased cleanly, before setting English over it with an add.
Character names in pinyin (淘气 Taoqi, 笑笑 Xiaoxiao, 奇思 Qisi, 妙想 Miaoxiang, 小红 Xiaohong); British spelling; yuan as ¥3;
"2 m" with a space; the same kind of text the same size (a new line rather than shrinking).`

function fixPrompt(v, pages, flags, file) {
  return `You fix defects that earlier reviewers flagged on the English translation of a Chinese primary-school maths textbook
(北师大版 ${v.title}, volume code ${v.code}). The English is set over cleaned scans of the Chinese pages; corrections in JSON files
change what is erased and what is set. Your pages (1-based): ${pages.join(', ')}. The flags (written by reviewers who could not fix
them with the tools they had; some name things outside their own items):
${flags.map(f => `  - page ${f.page}: ${f.issue}`).join('\n')}

For each flag: first look at the page as it renders now (preview) - some flags may already be fixed by later corrections; then fix
what is still wrong with the tools below, TRY every fix (try_fix.py) and look at the result closely (zoom), and iterate until the
page is right: no Chinese a reader needs, no damaged outline or box, no doubled text, English correct and natural, sizes matching
their kind. Never fix one thing by damaging another. A flag you cannot fix well stays as it is: list it in "left" with why.

${TOOLS(v.code)}

Write ONE file ${file} (Write tool): {"corrections": [ ...the entries you tried and kept... ], "left": [{"page": .., "issue": ".."}]}
(write it even when empty). Then return the structured summary.`
}

function checkPrompt(v, pages, flags, file) {
  return `You independently check fixes another agent wrote for flagged defects on the English translation of a Chinese
primary-school maths textbook (北师大版 ${v.title}, volume code ${v.code}). Pages (1-based): ${pages.join(', ')}. The flags were:
${flags.map(f => `  - page ${f.page}: ${f.issue}`).join('\n')}
The fixes are in ${file} ("corrections"; "left" = what the fixer could not fix).

Assume the fixes may be wrong. Render them yourself (try_fix.py with that file, then look closely, zooming into each flagged spot
and comparing with the source half of the png): is every fixed flag really fixed? Did any fix damage something else (a picture,
an outline, a number, another label), leave Chinese, double a text, set English too small or wrongly? Is the English correct?
Then correct the file: remove or repair a bad entry, add what is missing, and try again until the pages are right. If a "left" flag
can in fact be fixed well, fix it. Keep the file's shape; rewrite it with the Write tool only if you change something.

${TOOLS(v.code)}

Return the structured summary for the file as it stands after your check ("fixed" = flags now fixed, "left" = still not).`
}

const jobs = []
for (const v of args.volumes) {
  const byPage = {}
  for (const f of v.flags) (byPage[f.page] = byPage[f.page] || []).push(f)
  const pages = Object.keys(byPage).map(Number).sort((a, b) => a - b)
  for (let i = 0; i < pages.length; i += BATCH) {
    const chunk = pages.slice(i, i + BATCH)
    const flags = chunk.flatMap(p => byPage[p])
    const tag = String(chunk[0]).padStart(3, '0')
    jobs.push({ v, pages: chunk, flags, file: `/tmp/piptest/real/proof/${v.code}/corr_fx_${tag}.json` })
  }
}
log(`${jobs.length} groups of flagged pages over ${args.volumes.length} volume(s)`)
const results = await pipeline(jobs,
  j => agent(fixPrompt(j.v, j.pages, j.flags, j.file), { label: `fix:${j.v.code}:${j.pages.join(',')}`, phase: 'Fix', schema: RESULT }),
  (r, j) => agent(checkPrompt(j.v, j.pages, j.flags, j.file), { label: `check:${j.v.code}:${j.pages.join(',')}`, phase: 'Check', schema: RESULT }),
)
const ok = results.filter(Boolean)
return {
  groups: jobs.length, checked: ok.length,
  fixed: ok.reduce((n, r) => n + (r.fixed || 0), 0),
  left: ok.flatMap(r => r.left),
  failed: jobs.filter((j, i) => !results[i]).map(j => `${j.v.code}:${j.pages.join(',')}`),
}
