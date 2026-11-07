export const meta = {
  name: 'labels-headings-review',
  description: 'Text review of every heading and label of the translated textbooks: a reviewer proposes real improvements, a skeptic accepts or rejects each, then one standard English per Chinese label across all volumes',
  phases: [
    { title: 'Review', detail: 'one reviewer per chunk of a volume proposes changes' },
    { title: 'Verify', detail: 'a skeptic accepts or rejects each proposal and writes the volume file' },
    { title: 'Consistency', detail: 'the same Chinese label reads the same in every volume' },
    { title: 'Check', detail: 'a skeptic re-checks the consistency changes' },
  ],
}
// args: { chunks: [{ code, title, from, to }] }  (pages 1-based, inclusive; items in /tmp/piptest/real/proof/<code>/labels.json)
const P = '/tmp/piptest/real/proof'

const PROPOSALS = {
  type: 'object',
  properties: {
    proposals: { type: 'array', items: { type: 'object', properties: {
      id: { type: 'string' }, en: { type: 'string' }, was: { type: 'string' },
      kind: { type: 'string', enum: ['wrong', 'unnatural', 'inconsistent', 'too long', 'case'] }, reason: { type: 'string' } },
      required: ['id', 'en', 'was', 'kind', 'reason'] } },
    reviewed: { type: 'integer' },
  },
  required: ['proposals', 'reviewed'],
}
const VERDICTS = {
  type: 'object',
  properties: { file: { type: 'string' }, accepted: { type: 'integer' }, rejected: { type: 'integer' }, summary: { type: 'string' } },
  required: ['file', 'accepted', 'rejected', 'summary'],
}

const RULES = `The English edition is for children at a UK-style primary school; it follows the Chinese book closely.
- Meaning first: the English must say what the Chinese says, in the context of a primary maths lesson ("lesson" is the page's title,
  "near" the English of the nearest paragraph). Maths terms as a UK primary teacher says them: 竖式 column method, 直角 right angle,
  平行四边形 parallelogram, 个位/十位/百位 ones/tens/hundreds, 十分位 tenths, 统计 data/statistics, 估算 estimate, 验算 check.
- Natural, correct English: grammar, articles, plurals; no Chinglish ("School Sizes" for 学校人数 -> "Number of Students").
- Kinds: lesson titles and section headings in Title Case ("Buying Pencils", "Did You Know?", "Try It", "Practice"); labels on
  pictures, signs, tags and table cells as short phrases (sentence case, no full stop unless a sentence); name tags in pinyin
  (淘气 Taoqi, 笑笑 Xiaoxiao, 奇思 Qisi, 妙想 Miaoxiang, 小红 Xiaohong, 智慧老人 Wise Old Man, 机灵狗 Clever Dog); British spelling
  (metre, colour, centre, maths); money as ¥3 / ¥0.50; units "2 m", "5 kg" with a space; numbers as digits.
- Room: "w" is the box width in points, "size" the Chinese size, "set" the size the English was set at (smaller than size = it had
  to shrink). Never make a label noticeably longer unless the current one is wrong; where it shrank, a shorter equivalent with the
  same meaning is an improvement ("too long").
- Leave alone: anything already right (no style churn, no synonyms for taste), the cover's "Mathematics" / "Grade N" / "Volume M"
  lines and the publisher, maths expressions, and text that only repeats numbers or symbols.`

function reviewPrompt(c) {
  return `You review the English of every heading and label (titles, section labels, signs, tags, table cells, picture labels) on
pages ${c.from}-${c.to} of the translated textbook 北师大版 ${c.title} (code ${c.code}). The items are in ${P}/${c.code}/labels.json
(a JSON list; take those whose "page" is between ${c.from} and ${c.to}; fields: id, page, role, zh, en, w, size, set, lesson, near).
Read them all (use python to print them compactly, e.g. one line per item) and judge each against the Chinese.

${RULES}

Propose a change only where the current English is wrong, unnatural, inconsistent with how this volume says the same thing
elsewhere, too long for its room, or in the wrong case for its kind. Give the exact new English ("en"), the old ("was"), the kind
and a short reason. Return the proposals (an empty list is a fine answer) and how many items you reviewed.`
}

function verifyPrompt(c, proposals, file) {
  return `You are the skeptical second reader of proposed changes to headings and labels in the translated textbook 北师大版
${c.title} (code ${c.code}, pages ${c.from}-${c.to}). Items (with their Chinese, room and context) are in ${P}/${c.code}/labels.json.
The proposals:
${proposals.map(p => `  - ${p.id}: "${p.was}" -> "${p.en}" [${p.kind}] ${p.reason}`).join('\n') || '  (none)'}

${RULES}

For each proposal look up the item (zh, w, size, set, lesson, near) and try to REFUTE it: is the old English in fact right? Does the
new one change the meaning, lose a word of the task, get longer where there is no room, break the volume's own terms, or only
swap a synonym? Accept a proposal only when it is clearly better; you may amend it (keep it short). Then write ONE file ${file}
with the Write tool, shaped {"corrections": [{"segment_id": "<id>", "translation": "<new English>", "reason": "<kind: why>"} ...]}
holding only the accepted (or amended) changes - write it even when empty. Return the counts and a one-line summary.`
}

function consistencyPrompt(codes) {
  return `The twelve volumes of a translated Chinese primary maths textbook series (北师大版, Grades 1-6, two volumes each: codes
${codes.join(', ')}) must say the same Chinese heading or label the same way in English everywhere. Each volume's headings and labels
are in ${P}/<code>/labels.json (fields id, page, role, zh, en, w, size, set, lesson, near); changes already accepted in a text review
are in ${P}/<code>/corr_tx_<code>.json ({"corrections": [{"segment_id", "translation"}]} - apply them over "en" first).

With python, group all items by their Chinese (zh with spaces and trailing punctuation removed) and list the groups whose English
differs (ignoring case and a trailing full stop only where the kind allows). For each such group decide whether the Chinese means
the same thing in each place (look at role, lesson and near): where it does, choose the one best English (correct, natural, fits the
narrowest "w" of the group, Title Case for headings and section labels) and change the others to it; where the meaning differs by
context, leave them. Recurring section labels must match exactly: 你知道吗 "Did You Know?", 试一试 "Try It", 练一练 "Practice",
数学好玩 "Maths Is Fun", 整理与复习 "Review", 总复习 "Final Review", 做一做 "Do It", 说一说 "Talk About It", 想一想 "Think",
议一议 "Discuss".

${RULES}

Write one file per volume that has changes, ${P}/<code>/corr_tc_<code>.json, shaped {"corrections": [{"segment_id", "translation",
"reason": "consistency: <the standard and why>"}]} (Write tool). Return the files written, the number of changes and the
standards you chose (as a list of "zh -> en").`
}

const CONSIST = {
  type: 'object',
  properties: { files: { type: 'array', items: { type: 'string' } }, changes: { type: 'integer' },
    standards: { type: 'array', items: { type: 'string' } } },
  required: ['files', 'changes', 'standards'],
}

const chunks = args.chunks
phase('Review')
const done = await pipeline(chunks,
  c => agent(reviewPrompt(c), { label: `review:${c.code}:${c.from}-${c.to}`, phase: 'Review', schema: PROPOSALS }),
  (r, c) => agent(verifyPrompt(c, (r && r.proposals) || [], `${P}/${c.code}/corr_tx_${c.code}_${String(c.from).padStart(3, '0')}.json`),
    { label: `verify:${c.code}:${c.from}-${c.to}`, phase: 'Verify', schema: VERDICTS }),
)
const ok = done.filter(Boolean)
log(`text review: ${ok.reduce((n, r) => n + r.accepted, 0)} changes accepted, ${ok.reduce((n, r) => n + r.rejected, 0)} rejected`)

// the per-volume files are merged by the consistency agent: tell it where they are
const codes = [...new Set(chunks.map(c => c.code))]
phase('Consistency')
const cons = await agent(consistencyPrompt(codes).replace(/corr_tx_<code>\.json/g, 'corr_tx_<code>_*.json (one per chunk)'),
  { label: 'consistency', phase: 'Consistency', schema: CONSIST })
phase('Check')
const check = cons && cons.changes > 0 ? await agent(`You are the skeptical second reader of consistency changes made to the
headings and labels of a translated Chinese primary maths textbook series (volumes ${codes.join(', ')}). The changes are in the files
${(cons.files || []).join(', ')}; each volume's items (zh, en, w, size, set, lesson, near) are in ${P}/<code>/labels.json, with
accepted text-review changes in ${P}/<code>/corr_tx_<code>_*.json. Standards chosen: ${(cons.standards || []).join('; ')}.

${RULES}

Check every change: same meaning in that place? fits its "w"? correct English? Remove changes that are wrong for their context
and fix bad standards (rewrite the files with the Write tool; keep their shape). Return the files, the number of changes kept and the
standards.`, { label: 'check:consistency', phase: 'Check', schema: CONSIST }) : null
return { review: ok, consistency: cons, check }
