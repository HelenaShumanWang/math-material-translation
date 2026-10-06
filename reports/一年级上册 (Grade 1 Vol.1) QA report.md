# QA report

**Result:** QA FAILED after 3 rounds: 153 errors, 131 warnings (1253.6 s); proofread: 564 corrections applied; output file checks: 0 error(s)

**Document:** 数学 (zh → en, 109 page(s), 1076 translatable segment(s))

**Checks run:** `completeness`, `placeholders`, `numbers`, `untranslated`, `target_script`, `glossary`, `length_ratio`, `formatting`, `layout_fit`, `image_text`, `llm_review`, `output_checks`

## Rounds

| Round | Errors | Warnings | Re-translated | Passed | Duration |
|---|---|---|---|---|---|
| 1 | 244 | 204 | 232 segment(s) | no | 294.2 s |
| 2 | 266 | 223 | 203 segment(s) | no | 298.2 s |
| 3 | 223 | 230 | 0 segment(s) | no | 102.5 s |

- Round 1: llm_review ×319, layout_fit ×102, formatting ×8, image_text ×8, glossary ×6, placeholders ×2, length_ratio ×1, numbers ×1, untranslated ×1
- Round 2: llm_review ×323, layout_fit ×93, formatting ×27, placeholders ×15, glossary ×14, image_text ×8, untranslated ×6, length_ratio ×3
- Round 3: llm_review ×317, layout_fit ×89, formatting ×17, placeholders ×11, image_text ×8, glossary ×5, completeness ×2, untranslated ×2, length_ratio ×1, target_script ×1

## Final issues (284)

### `completeness` — 17 errors, 0 warnings

| Severity | Page | Segment | Message | Source | Translation |
|---|---|---|---|---|---|
| error | 19 | p18_s3 | The translation "." contains no words; translate the complete source text | 一样多。 | . |
| error | 25 | p24_s11 | The translation "→" contains no words; translate the complete source text | 号→ | → |
| error | 25 | p24_s12 | The translation "." contains no words; translate the complete source text | 号 | . |
| error | 59 | p58_s5 | The translation ":" contains no words; translate the complete source text | 有 | : |
| error | 59 | p58_s6 | The translation ":" contains no words; translate the complete source text | 有 | : |
| error | 93 | p92_s2 | The translation ":" contains no words; translate the complete source text | 有 | : |
| error | 93 | p92_s5 | The translation ":" contains no words; translate the complete source text | 有 | : |
| error | 104 | p103_s10 | The translation ":" contains no words; translate the complete source text | 有 | : |
| error | 104 | p103_s11 | The translation "." contains no words; translate the complete source text | 个 | . |
| error | 104 | p103_s14 | The translation ": () : () : () : ()" contains no words; translate the complete source text | 有()个有(）个，有个有个 | : () : () : () : () |
| error | 104 | p103_s3 | The translation ":" contains no words; translate the complete source text | 有 | : |
| error | 104 | p103_s4 | The translation "." contains no words; translate the complete source text | 个 | . |
| error | 104 | p103_s5 | The translation ":" contains no words; translate the complete source text | 有 | : |
| error | 104 | p103_s6 | The translation "." contains no words; translate the complete source text | 个 | . |
| error | 104 | p103_s7 | The translation ":" contains no words; translate the complete source text | 有 | : |
| error | 104 | p103_s8 | The translation "." contains no words; translate the complete source text | 个 | . |
| error | 104 | p103_s9 | The translation ":" contains no words; translate the complete source text | 有 | : |

### `formatting` — 18 errors, 3 warnings

| Severity | Page | Segment | Message | Source | Translation |
|---|---|---|---|---|---|
| error | 19 | p18_s2 | Remove the symbol(s) □: they are not in the source (a picture in the book is not a symbol; leave it out rather than inventing one) | 每，和 | Draw as many □ as |
| error | 19 | p18_s5 | Remove the symbol(s) ○: they are not in the source (a picture in the book is not a symbol; leave it out rather than inventing one) | 画，比多72.6.0。 | Draw more ○ than 72.6.0. |
| error | 22 | p21_s4 | Remove the symbol(s) ✓: they are not in the source (a picture in the book is not a symbol; leave it out rather than inventing one) | ”，最少的画 | "✓", the least with |
| error | 25 | p24_s10 | Keep the symbol(s) □×3 of the source in the translation, at the matching position | 号→□96.16.0号→□96.16.1号→□96.16.2号 | → 96.16.0 → 96.16.1 → 96.16.2 |
| error | 35 | p34_s1 | The source does not end with a question mark; do not end the translation with one | 1.还有几个136.1.0 | 1. How many 136.1.0 are left? |
| error | 46 | p45_s5 | The source does not end with a question mark; do not end the translation with one | 3.房子里有几只 | 3. How many in the house? |
| error | 68 | p67_s16 | The source ends with a question mark; end the translation with a question mark too | 猜一猜，它是谁？ | Guess who it is. |
| error | 72 | p71_s15 | The source ends with a question mark; end the translation with a question mark too | 猜一猜，说的是什么物品？ | Guess which object is being described. |
| error | 84 | p83_s5 | The source does not end with a question mark; do not end the translation with one | 共有几条业332.7.0 | How many 332.7.0 in all? |
| error | 89 | p88_s2 | The source does not end with a question mark; do not end the translation with one | 在第—级台阶，在第—级台阶，在第—级台阶，在第_在第—级台阶，在第——级台阶，在第_级台阶，只在第_级台阶，站在第9级… | Which step is each person on? Step ___, step ___, step ___,… |
| error | 90 | p89_s27 | The source ends with a question mark; end the translation with a question mark too | 里可以填几？ | be? Think about it. |
| error | 95 | p94_s4 | Keep the line breaks of the source: it has 0 line break(s), the translation has 2 | 结果比10大的就被淘汰结果最大的人获胜结果一样大谁摸的牌少谁获胜。 | If your total is more than 10, you're out. The highest tota… |
| error | 99 | p98_s11 | Remove the symbol(s) □ △ ○: they are not in the source (a picture in the book is not a symbol; leave it out rather than inventing one) | 3.画一画。在画☆，上面画，左边画，下面画 | 3. Draw ☆ to the right of the flower, □ above it, △ to its … |
| error | 99 | p98_s7 | Keep the line breaks of the source: it has 0 line break(s), the translation has 2 | 图形与几何独立思考 | Shapes and Geometry On your own |
| error | 100 | p99_s12 | Keep the line breaks of the source: it has 0 line break(s), the translation has 2 | 15的个位上是18里面有1个十和3个一合起来是 | The ones digit of 15 18 has 1 ten and 3 ones make |
| error | 104 | p103_s14 | Keep the line breaks of the source: it has 0 line break(s), the translation has 3 | 有()个有(）个，有个有个 | : () : () : () : () |
| error | 104 | p103_s2 | Keep the line breaks of the source: it has 0 line break(s), the translation has 3 | 左上图左下图右上图右下图 | Top left Bottom left Top right Bottom right |
| error | 105 | p104_s0 | The source does not end with a question mark; do not end the translation with one | 本学期你学到了什么 | What did you learn this term? |
| warning | 18 | p17_s2 | The source does not end with a exclamation mark; do not end the translation with one | 样多，够了 | The same number. Enough! |
| warning | 67 | p66_s8 | The source does not end with a exclamation mark; do not end the translation with one | 把得数小的排在前面 | Smaller answers go in front! |
| warning | 74 | p73_s17 | The source does not end with a exclamation mark; do not end the translation with one | 嘻嘻，我知道了。 | Hee hee, now I know! |

### `glossary` — 9 errors, 0 warnings

| Severity | Page | Segment | Message | Source | Translation |
|---|---|---|---|---|---|
| error | 63 | p62_s12 | Glossary: translate "练习" as "exercise" | 语文练习本语文 | Chinese workbook; Chinese |
| error | 63 | p62_s13 | Glossary: translate "练习" as "exercise" | 练习木数学练习本语文 | workbook; Maths workbook; Chinese |
| error | 63 | p62_s16 | Glossary: translate "练习" as "exercise" | 练习本数学 | workbook; Maths |
| error | 63 | p62_s19 | Glossary: translate "练习" as "exercise" | 数学练习本数学 | Maths workbook; Maths |
| error | 63 | p62_s3 | Glossary: translate "练习" as "exercise" | 数学语文练习本 | Maths; Chinese workbook |
| error | 63 | p62_s4 | Glossary: translate "练习" as "exercise" | 数学练习本 | Maths workbook |
| error | 71 | p70_s4 | Glossary: translate "练习" as "exercise" | 练习本 | Notes |
| error | 94 | p93_s2 | Glossary: translate "比一比" as "Compare" | 2人一组做游戏，比一比哪组堆得又快又高。 | Play in groups of 2. See which group can stack the fastest … |
| error | 100 | p99_s0 | Glossary: translate "练习" as "exercise" | 练习 | Practice |

### `layout_fit` — 76 errors, 58 warnings

| Severity | Page | Segment | Message | Source | Translation |
|---|---|---|---|---|---|
| error | 5 | p4_s2 | Shorten the translation to at most 30 characters so it fits the original box (the current translation of 35 characters overflows its box; the minimum allowed size is 55%) | 七加与减 | Unit 7 Addition and Subtraction (2) |
| error | 5 | p4_s2 | Shorten the translation to at most 30 characters so it fits the original box (the current translation of 35 characters overflows its box; the minimum allowed size is 55%) | 七加与减 | Unit 7 Addition and Subtraction (2) |
| error | 15 | p14_s0 | Shorten the translation to at most 5 characters so it fits the original box (the current translation of 10 characters overflows its box; the minimum allowed size is 55%) | 文具 | Stationery |
| error | 15 | p14_s0 | Shorten the translation to at most 5 characters so it fits the original box (the current translation of 10 characters overflows its box; the minimum allowed size is 55%) | 文具 | Stationery |
| error | 25 | p24_s5 | Shorten the translation to at most 27 characters so it fits the original box (the current translation of 32 characters overflows its box; the minimum allowed size is 55%) | 桥下通过吗？ | Can the car go under the bridge? |
| error | 25 | p24_s5 | Shorten the translation to at most 27 characters so it fits the original box (the current translation of 32 characters overflows its box; the minimum allowed size is 55%) | 桥下通过吗？ | Can the car go under the bridge? |
| error | 26 | p25_s10 | Shorten the translation to at most 5 characters so it fits the original box (the current translation of 8 characters overflows its box; the minimum allowed size is 55%) | 轻 | lighter. |
| error | 26 | p25_s10 | Shorten the translation to at most 5 characters so it fits the original box (the current translation of 8 characters overflows its box; the minimum allowed size is 55%) | 轻 | lighter. |
| error | 26 | p25_s11 | Shorten the translation to at most 5 characters so it fits the original box (the current translation of 8 characters overflows its box; the minimum allowed size is 55%) | 重 | heavier. |
| error | 26 | p25_s11 | Shorten the translation to at most 5 characters so it fits the original box (the current translation of 8 characters overflows its box; the minimum allowed size is 55%) | 重 | heavier. |
| error | 26 | p25_s2 | Shorten the translation to at most 24 characters so it fits the original box (the current translation of 36 characters overflows its box; the minimum allowed size is 55%) | 100.2.l比100.2.0重 | 100.2.l is heavier than 100.2.0. |
| error | 26 | p25_s2 | Shorten the translation to at most 24 characters so it fits the original box (the current translation of 36 characters overflows its box; the minimum allowed size is 55%) | 100.2.l比100.2.0重 | 100.2.l is heavier than 100.2.0. |
| error | 26 | p25_s4 | Shorten the translation to at most 15 characters so it fits the original box (the current translation of 21 characters overflows its box; the minimum allowed size is 55%) | 100.4.0轻 | 100.4.0 is heavier. |
| error | 26 | p25_s4 | Shorten the translation to at most 15 characters so it fits the original box (the current translation of 21 characters overflows its box; the minimum allowed size is 55%) | 100.4.0轻 | 100.4.0 is heavier. |
| error | 26 | p25_s9 | Shorten the translation to at most 32 characters so it fits the original box (the current translation of 79 characters overflows its box; the minimum allowed size is 55%) | 100.12.l比100.12.r100.14.l比100.14.r | Compared with 100.12.r, 100.12.l is Compared with 100.… |
| error | 26 | p25_s9 | Shorten the translation to at most 32 characters so it fits the original box (the current translation of 79 characters overflows its box; the minimum allowed size is 55%) | 100.12.l比100.12.r100.14.l比100.14.r | Compared with 100.12.r, 100.12.l is Compared with 100.… |
| error | 28 | p27_s12 | Shorten the translation to at most 7 characters so it fits the original box (the current translation of 9 characters overflows its box; the minimum allowed size is 55%) | 加号 | plus sign |
| error | 28 | p27_s12 | Shorten the translation to at most 7 characters so it fits the original box (the current translation of 9 characters overflows its box; the minimum allowed size is 55%) | 加号 | plus sign |
| error | 28 | p27_s13 | Shorten the translation to at most 23 characters so it fits the original box (the current translation of 27 characters overflows its box; the minimum allowed size is 55%) | 读作：3加2等于5。 | Read as: 3 plus 2 equals 5. |
| error | 28 | p27_s13 | Shorten the translation to at most 23 characters so it fits the original box (the current translation of 27 characters overflows its box; the minimum allowed size is 55%) | 读作：3加2等于5。 | Read as: 3 plus 2 equals 5. |
| error | 31 | p30_s11 | Shorten the translation to at most 8 characters so it fits the original box (the current translation of 10 characters overflows its box; the minimum allowed size is 55%) | 减号 | minus sign |
| error | 31 | p30_s11 | Shorten the translation to at most 8 characters so it fits the original box (the current translation of 10 characters overflows its box; the minimum allowed size is 55%) | 减号 | minus sign |
| error | 31 | p30_s12 | Shorten the translation to at most 24 characters so it fits the original box (the current translation of 28 characters overflows its box; the minimum allowed size is 55%) | 读作：5减2等于3。 | Read as: 5 minus 2 equals 3. |
| error | 31 | p30_s12 | Shorten the translation to at most 24 characters so it fits the original box (the current translation of 28 characters overflows its box; the minimum allowed size is 55%) | 读作：5减2等于3。 | Read as: 5 minus 2 equals 3. |
| error | 40 | p39_s0 | Shorten the translation to at most 14 characters so it fits the original box (the current translation of 17 characters overflows its box; the minimum allowed size is 55%) | 背土豆 | Carrying Potatoes |
| error | 40 | p39_s0 | Shorten the translation to at most 14 characters so it fits the original box (the current translation of 17 characters overflows its box; the minimum allowed size is 55%) | 背土豆 | Carrying Potatoes |
| error | 42 | p41_s0 | Shorten the translation to at most 7 characters so it fits the original box (the current translation of 9 characters overflows its box; the minimum allowed size is 55%) | 跳绳 | Jump Rope |
| error | 42 | p41_s0 | Shorten the translation to at most 7 characters so it fits the original box (the current translation of 9 characters overflows its box; the minimum allowed size is 55%) | 跳绳 | Jump Rope |
| error | 49 | p48_s0 | Shorten the translation to at most 6 characters so it fits the original box (the current translation of 8 characters overflows its box; the minimum allowed size is 55%) | 乘车 | Bus Ride |
| error | 49 | p48_s0 | Shorten the translation to at most 6 characters so it fits the original box (the current translation of 8 characters overflows its box; the minimum allowed size is 55%) | 乘车 | Bus Ride |
| error | 50 | p49_s7 | Shorten the translation to at most 20 characters so it fits the original box (the current translation of 24 characters overflows its box; the minimum allowed size is 55%) | （1）一共有几个 | (1) Altogether, how many |
| error | 50 | p49_s7 | Shorten the translation to at most 20 characters so it fits the original box (the current translation of 24 characters overflows its box; the minimum allowed size is 55%) | （1）一共有几个 | (1) Altogether, how many |
| error | 58 | p57_s0 | Shorten the translation to at most 17 characters so it fits the original box (the current translation of 21 characters overflows its box; the minimum allowed size is 55%) | 巩固应用 | Consolidate and Apply |
| error | 58 | p57_s0 | Shorten the translation to at most 17 characters so it fits the original box (the current translation of 21 characters overflows its box; the minimum allowed size is 55%) | 巩固应用 | Consolidate and Apply |
| error | 58 | p57_s6 | Shorten the translation to at most 7 characters so it fits the original box (the current translation of 9 characters overflows its box; the minimum allowed size is 55%) | 排第 | is number |
| error | 58 | p57_s6 | Shorten the translation to at most 7 characters so it fits the original box (the current translation of 9 characters overflows its box; the minimum allowed size is 55%) | 排第 | is number |
| error | 61 | p60_s13 | Shorten the translation to at most 6 characters so it fits the original box (the current translation of 9 characters overflows its box; the minimum allowed size is 55%) | 妙想 | Miaoxiang |
| error | 61 | p60_s13 | Shorten the translation to at most 6 characters so it fits the original box (the current translation of 9 characters overflows its box; the minimum allowed size is 55%) | 妙想 | Miaoxiang |
| error | 62 | p61_s7 | Shorten the translation to at most 8 characters so it fits the original box (the current translation of 10 characters overflows its box; the minimum allowed size is 55%) | 文具 | Stationery |
| error | 62 | p61_s7 | Shorten the translation to at most 8 characters so it fits the original box (the current translation of 10 characters overflows its box; the minimum allowed size is 55%) | 文具 | Stationery |
| error | 63 | p62_s12 | Shorten the translation to at most 14 characters so it fits the original box (the current translation of 25 characters overflows its box; the minimum allowed size is 55%) | 语文练习本语文 | Chinese workbook; Chinese |
| error | 63 | p62_s12 | Shorten the translation to at most 14 characters so it fits the original box (the current translation of 25 characters overflows its box; the minimum allowed size is 55%) | 语文练习本语文 | Chinese workbook; Chinese |
| error | 63 | p62_s13 | Shorten the translation to at most 19 characters so it fits the original box (the current translation of 33 characters overflows its box; the minimum allowed size is 55%) | 练习木数学练习本语文 | workbook; Maths workbook; Chinese |
| error | 63 | p62_s13 | Shorten the translation to at most 19 characters so it fits the original box (the current translation of 33 characters overflows its box; the minimum allowed size is 55%) | 练习木数学练习本语文 | workbook; Maths workbook; Chinese |
| error | 63 | p62_s14 | Shorten the translation to at most 5 characters so it fits the original box (the current translation of 7 characters overflows its box; the minimum allowed size is 55%) | 语文 | Chinese |
| error | 63 | p62_s14 | Shorten the translation to at most 5 characters so it fits the original box (the current translation of 7 characters overflows its box; the minimum allowed size is 55%) | 语文 | Chinese |
| error | 63 | p62_s16 | Shorten the translation to at most 8 characters so it fits the original box (the current translation of 15 characters overflows its box; the minimum allowed size is 55%) | 练习本数学 | workbook; Maths |
| error | 63 | p62_s16 | Shorten the translation to at most 8 characters so it fits the original box (the current translation of 15 characters overflows its box; the minimum allowed size is 55%) | 练习本数学 | workbook; Maths |
| error | 63 | p62_s17 | Shorten the translation to at most 5 characters so it fits the original box (the current translation of 7 characters overflows its box; the minimum allowed size is 55%) | 语文 | Chinese |
| error | 63 | p62_s17 | Shorten the translation to at most 5 characters so it fits the original box (the current translation of 7 characters overflows its box; the minimum allowed size is 55%) | 语文 | Chinese |
| error | 63 | p62_s19 | Shorten the translation to at most 14 characters so it fits the original box (the current translation of 21 characters overflows its box; the minimum allowed size is 55%) | 数学练习本数学 | Maths workbook; Maths |
| error | 63 | p62_s19 | Shorten the translation to at most 14 characters so it fits the original box (the current translation of 21 characters overflows its box; the minimum allowed size is 55%) | 数学练习本数学 | Maths workbook; Maths |
| error | 63 | p62_s20 | Shorten the translation to at most 10 characters so it fits the original box (the current translation of 14 characters overflows its box; the minimum allowed size is 55%) | 数学语文 | Maths; Chinese |
| error | 63 | p62_s20 | Shorten the translation to at most 10 characters so it fits the original box (the current translation of 14 characters overflows its box; the minimum allowed size is 55%) | 数学语文 | Maths; Chinese |
| error | 63 | p62_s4 | Shorten the translation to at most 11 characters so it fits the original box (the current translation of 14 characters overflows its box; the minimum allowed size is 55%) | 数学练习本 | Maths workbook |
| error | 63 | p62_s4 | Shorten the translation to at most 11 characters so it fits the original box (the current translation of 14 characters overflows its box; the minimum allowed size is 55%) | 数学练习本 | Maths workbook |
| error | 63 | p62_s5 | Shorten the translation to at most 8 characters so it fits the original box (the current translation of 14 characters overflows its box; the minimum allowed size is 55%) | 数学药习本 | Maths workbook |
| error | 63 | p62_s5 | Shorten the translation to at most 8 characters so it fits the original box (the current translation of 14 characters overflows its box; the minimum allowed size is 55%) | 数学药习本 | Maths workbook |
| error | 66 | p65_s1 | Shorten the translation to at most 12 characters so it fits the original box (the current translation of 14 characters overflows its box; the minimum allowed size is 55%) | 前后 | Front and Back |
| error | 66 | p65_s1 | Shorten the translation to at most 12 characters so it fits the original box (the current translation of 14 characters overflows its box; the minimum allowed size is 55%) | 前后 | Front and Back |
| error | 67 | p66_s16 | Shorten the translation to at most 8 characters so it fits the original box (the current translation of 21 characters overflows its box; the minimum allowed size is 55%) | 火车站路广场 | Station, Road, Square |
| error | 67 | p66_s16 | Shorten the translation to at most 8 characters so it fits the original box (the current translation of 21 characters overflows its box; the minimum allowed size is 55%) | 火车站路广场 | Station, Road, Square |
| error | 68 | p67_s0 | Shorten the translation to at most 9 characters so it fits the original box (the current translation of 11 characters overflows its box; the minimum allowed size is 55%) | 上下 | Above/Below |
| error | 68 | p67_s0 | Shorten the translation to at most 9 characters so it fits the original box (the current translation of 11 characters overflows its box; the minimum allowed size is 55%) | 上下 | Above/Below |
| error | 70 | p69_s0 | Shorten the translation to at most 11 characters so it fits the original box (the current translation of 14 characters overflows its box; the minimum allowed size is 55%) | 左右 | Left and Right |
| error | 70 | p69_s0 | Shorten the translation to at most 11 characters so it fits the original box (the current translation of 14 characters overflows its box; the minimum allowed size is 55%) | 左右 | Left and Right |
| error | 71 | p70_s15 | Shorten the translation to at most 20 characters so it fits the original box (the current translation of 23 characters overflows its box; the minimum allowed size is 55%) | 是第5辆，一 | the bus is the 5th car, |
| error | 71 | p70_s15 | Shorten the translation to at most 20 characters so it fits the original box (the current translation of 23 characters overflows its box; the minimum allowed size is 55%) | 是第5辆，一 | the bus is the 5th car, |
| error | 72 | p71_s11 | Shorten the translation to at most 5 characters so it fits the original box (the current translation of 8 characters overflows its box; the minimum allowed size is 55%) | 小红 | Xiaohong |
| error | 72 | p71_s11 | Shorten the translation to at most 5 characters so it fits the original box (the current translation of 8 characters overflows its box; the minimum allowed size is 55%) | 小红 | Xiaohong |
| error | 72 | p71_s2 | Shorten the translation to at most 46 characters so it fits the original box (the current translation of 58 characters overflows its box; the minimum allowed size is 55%) | 自284.2.0葬自信自强自立 | 284.2.0 Self-respect, Confidence, Strength, Independence |
| error | 72 | p71_s2 | Shorten the translation to at most 46 characters so it fits the original box (the current translation of 58 characters overflows its box; the minimum allowed size is 55%) | 自284.2.0葬自信自强自立 | 284.2.0 Self-respect, Confidence, Strength, Independence |
| error | 74 | p73_s1 | Shorten the translation to at most 15 characters so it fits the original box (the current translation of 18 characters overflows its box; the minimum allowed size is 55%) | 认识图形 | Recognizing Shapes |
| error | 74 | p73_s1 | Shorten the translation to at most 15 characters so it fits the original box (the current translation of 18 characters overflows its box; the minimum allowed size is 55%) | 认识图形 | Recognizing Shapes |
| error | 78 | p77_s1 | Shorten the translation to at most 17 characters so it fits the original box (the current translation of 20 characters overflows its box; the minimum allowed size is 55%) | 古人计数 | How Ancients Counted |
| error | 78 | p77_s1 | Shorten the translation to at most 17 characters so it fits the original box (the current translation of 20 characters overflows its box; the minimum allowed size is 55%) | 古人计数 | How Ancients Counted |
| warning | 6 | p5_s2 | The translation overflows its box and was rendered at 28% of the original size; even a much shorter text would not fit, check this box in the preview | 欢 | Welcome |
| warning | 6 | p5_s2 | The translation overflows its box and was rendered at 28% of the original size; even a much shorter text would not fit, check this box in the preview | 欢 | Welcome |
| warning | 6 | p5_s3 | The translation overflows its box and was rendered at 30% of the original size; even a much shorter text would not fit, check this box in the preview | 学 | School |
| warning | 6 | p5_s3 | The translation overflows its box and was rendered at 30% of the original size; even a much shorter text would not fit, check this box in the preview | 学 | School |
| warning | 26 | p25_s3 | The translation overflows its box and was rendered at 31% of the original size; even a much shorter text would not fit, check this box in the preview | 100.3.l比100.3.r | 100.3.l is lighter than 100.3.r. |
| warning | 26 | p25_s3 | The translation overflows its box and was rendered at 31% of the original size; even a much shorter text would not fit, check this box in the preview | 100.3.l比100.3.r | 100.3.l is lighter than 100.3.r. |
| warning | 33 | p32_s6 | The translation overflows its box and was rendered at 48% of the original size; even a much shorter text would not fit, check this box in the preview | 支。 | fewer. |
| warning | 33 | p32_s6 | The translation overflows its box and was rendered at 48% of the original size; even a much shorter text would not fit, check this box in the preview | 支。 | fewer. |
| warning | 37 | p36_s10 | The translation overflows its box and was rendered at 42% of the original size; even a much shorter text would not fit, check this box in the preview | 三 | Unit 3 |
| warning | 37 | p36_s10 | The translation overflows its box and was rendered at 42% of the original size; even a much shorter text would not fit, check this box in the preview | 三 | Unit 3 |
| warning | 56 | p55_s8 | The translation overflows its box and was rendered at 38% of the original size; even a much shorter text would not fit, check this box in the preview | 画 | Draw |
| warning | 56 | p55_s8 | The translation overflows its box and was rendered at 38% of the original size; even a much shorter text would not fit, check this box in the preview | 画 | Draw |
| warning | 63 | p62_s1 | The translation overflows its box and was rendered at 33% of the original size; even a much shorter text would not fit, check this box in the preview | 语 | Chinese |
| warning | 63 | p62_s1 | The translation overflows its box and was rendered at 33% of the original size; even a much shorter text would not fit, check this box in the preview | 语 | Chinese |
| warning | 63 | p62_s10 | The translation overflows its box and was rendered at 33% of the original size; even a much shorter text would not fit, check this box in the preview | 练 | ercise |
| warning | 63 | p62_s10 | The translation overflows its box and was rendered at 33% of the original size; even a much shorter text would not fit, check this box in the preview | 练 | ercise |
| warning | 63 | p62_s11 | The translation overflows its box and was rendered at 39% of the original size; even a much shorter text would not fit, check this box in the preview | 文 | ercise |
| warning | 63 | p62_s11 | The translation overflows its box and was rendered at 39% of the original size; even a much shorter text would not fit, check this box in the preview | 文 | ercise |
| warning | 63 | p62_s15 | The translation overflows its box and was rendered at 48% of the original size; even a much shorter text would not fit, check this box in the preview | 语文 | Chinese |
| warning | 63 | p62_s15 | The translation overflows its box and was rendered at 48% of the original size; even a much shorter text would not fit, check this box in the preview | 语文 | Chinese |
| warning | 63 | p62_s2 | The translation overflows its box and was rendered at 54% of the original size; even a much shorter text would not fit, check this box in the preview | 数学 | Maths |
| warning | 63 | p62_s2 | The translation overflows its box and was rendered at 54% of the original size; even a much shorter text would not fit, check this box in the preview | 数学 | Maths |
| warning | 63 | p62_s6 | The translation overflows its box and was rendered at 28% of the original size; even a much shorter text would not fit, check this box in the preview | 语 | Chinese |
| warning | 63 | p62_s6 | The translation overflows its box and was rendered at 28% of the original size; even a much shorter text would not fit, check this box in the preview | 语 | Chinese |
| warning | 63 | p62_s9 | The translation overflows its box and was rendered at 29% of the original size; even a much shorter text would not fit, check this box in the preview | 语 | Chinese |
| warning | 63 | p62_s9 | The translation overflows its box and was rendered at 29% of the original size; even a much shorter text would not fit, check this box in the preview | 语 | Chinese |
| warning | 65 | p64_s18 | The translation overflows its box and was rendered at 38% of the original size; even a much shorter text would not fit, check this box in the preview | 蔬菜 | Vegetables |
| warning | 65 | p64_s18 | The translation overflows its box and was rendered at 38% of the original size; even a much shorter text would not fit, check this box in the preview | 蔬菜 | Vegetables |
| warning | 68 | p67_s4 | The translation overflows its box and was rendered at 54% of the original size; even a much shorter text would not fit, check this box in the preview | 在 | is on |
| warning | 68 | p67_s4 | The translation overflows its box and was rendered at 54% of the original size; even a much shorter text would not fit, check this box in the preview | 在 | is on |
| warning | 68 | p67_s7 | The translation overflows its box and was rendered at 54% of the original size; even a much shorter text would not fit, check this box in the preview | 在 | is on |
| warning | 68 | p67_s7 | The translation overflows its box and was rendered at 54% of the original size; even a much shorter text would not fit, check this box in the preview | 在 | is on |
| warning | 69 | p68_s4 | The translation overflows its box and was rendered at 34% of the original size; even a much shorter text would not fit, check this box in the preview | 在 | is on |
| warning | 69 | p68_s4 | The translation overflows its box and was rendered at 34% of the original size; even a much shorter text would not fit, check this box in the preview | 在 | is on |
| warning | 72 | p71_s0 | The translation overflows its box and was rendered at 42% of the original size; even a much shorter text would not fit, check this box in the preview | 教室 | Classroom |
| warning | 72 | p71_s0 | The translation overflows its box and was rendered at 42% of the original size; even a much shorter text would not fit, check this box in the preview | 教室 | Classroom |
| warning | 72 | p71_s13 | The translation overflows its box and was rendered at 42% of the original size; even a much shorter text would not fit, check this box in the preview | 小强 | Xiaoqiang |
| warning | 72 | p71_s13 | The translation overflows its box and was rendered at 42% of the original size; even a much shorter text would not fit, check this box in the preview | 小强 | Xiaoqiang |
| warning | 74 | p73_s12 | The translation overflows its box and was rendered at 52% of the original size; even a much shorter text would not fit, check this box in the preview | 茶 | Tea |
| warning | 74 | p73_s12 | The translation overflows its box and was rendered at 52% of the original size; even a much shorter text would not fit, check this box in the preview | 茶 | Tea |
| warning | 74 | p73_s2 | The translation overflows its box and was rendered at 33% of the original size; even a much shorter text would not fit, check this box in the preview | 牙膏 | Toothpaste |
| warning | 74 | p73_s2 | The translation overflows its box and was rendered at 33% of the original size; even a much shorter text would not fit, check this box in the preview | 牙膏 | Toothpaste |
| warning | 74 | p73_s4 | The translation overflows its box and was rendered at 47% of the original size; even a much shorter text would not fit, check this box in the preview | 茶 | Tea |
| warning | 74 | p73_s4 | The translation overflows its box and was rendered at 47% of the original size; even a much shorter text would not fit, check this box in the preview | 茶 | Tea |
| warning | 88 | p87_s42 | The translation overflows its box and was rendered at 50% of the original size; even a much shorter text would not fit, check this box in the preview | 十+ | T + |
| warning | 88 | p87_s42 | The translation overflows its box and was rendered at 50% of the original size; even a much shorter text would not fit, check this box in the preview | 十+ | T + |
| warning | 97 | p96_s4 | The translation overflows its box and was rendered at 41% of the original size; even a much shorter text would not fit, check this box in the preview | 农 | Farm |
| warning | 97 | p96_s4 | The translation overflows its box and was rendered at 41% of the original size; even a much shorter text would not fit, check this box in the preview | 农 | Farm |
| warning | 97 | p96_s5 | The translation overflows its box and was rendered at 32% of the original size; even a much shorter text would not fit, check this box in the preview | 场 | Farm Primary School |
| warning | 97 | p96_s5 | The translation overflows its box and was rendered at 32% of the original size; even a much shorter text would not fit, check this box in the preview | 场 | Farm Primary School |
| warning | 97 | p96_s6 | The translation overflows its box and was rendered at 21% of the original size; even a much shorter text would not fit, check this box in the preview | 小 | Primary |
| warning | 97 | p96_s6 | The translation overflows its box and was rendered at 21% of the original size; even a much shorter text would not fit, check this box in the preview | 小 | Primary |
| warning | 97 | p96_s7 | The translation overflows its box and was rendered at 22% of the original size; even a much shorter text would not fit, check this box in the preview | 学 | School |
| warning | 97 | p96_s7 | The translation overflows its box and was rendered at 22% of the original size; even a much shorter text would not fit, check this box in the preview | 学 | School |
| warning | 99 | p98_s9 | The translation overflows its box and was rendered at 48% of the original size; even a much shorter text would not fit, check this box in the preview | 饼干 | Cookies |
| warning | 99 | p98_s9 | The translation overflows its box and was rendered at 48% of the original size; even a much shorter text would not fit, check this box in the preview | 饼干 | Cookies |
| warning | 104 | p103_s19 | The translation overflows its box and was rendered at 55% of the original size; even a much shorter text would not fit, check this box in the preview | 在 | is on |
| warning | 104 | p103_s19 | The translation overflows its box and was rendered at 55% of the original size; even a much shorter text would not fit, check this box in the preview | 在 | is on |

### `llm_review` — 32 errors, 53 warnings

| Severity | Page | Segment | Message | Source | Translation |
|---|---|---|---|---|---|
| error | 6 | p5_s2 | Reviewer (omission): The single character 欢 is part of the split heading 欢迎新同学; translating it separately as "Welcome" and 学 as "Pupils" duplicates/misplaces the heading fragments. Suggested translation: "Welcome" | 欢 | Welcome |
| error | 12 | p11_s3 | Reviewer (terminology): British spelling "colour" deviates from the standard textbook spelling "color". Suggested translation: "3. Look at the number and color." | 3.看数涂一涂。 | 3. Look at the number and colour. |
| error | 13 | p12_s3 | Reviewer (untranslated): The sentence "一条鱼也没有用0表示" is broken by an untranslated section marker "第48.5.0节" and reads ungrammatically; it should state that no fish is shown by 0. Suggested translation: "No fish at all is shown by 0." | 一条鱼也没有用48.5.00表示。 | No fish at all is shown by 48.5.00. |
| error | 13 | p12_s7 | Reviewer (untranslated): The source fragment "mmmmlmm mmka" is gibberish/OCR noise that should not appear as a heading; it is untranslated English-like filler. | mmmmlmm mmka | mmmmlmm mmka |
| error | 14 | p13_s4 | Reviewer (terminology): British spelling "colour" deviates from the standard textbook spelling "color". Suggested translation: "4. Color and write." | 4.涂一涂，写一写。 | 4. Colour and write. |
| error | 22 | p21_s6 | Reviewer (meaning): The source label 和 ("and") is translated as "and", which is a possible reading, but in this page context it is the label for a question word; treating it as a plain conjunction changes the label's function. Also, no context is given to confirm. If it is the question word (和 = "sum/and"), the standard rendering on such a page label is "and"; however the more serious issue is the following items. | 和 | and |
| error | 22 | p21_s7 | Reviewer (number): The placeholder ⟦84.9.0⟧ is rendered as plain "84.9.0" instead of being kept as the placeholder ⟦84.9.0⟧; the source has an image/answer-box placeholder that must be preserved. Suggested translation: "⟦84.9.0⟧, which one holds more?" | 84.9.0，哪个装得多？ | 84.9.0, which one holds more? |
| error | 33 | p32_s3 | Reviewer (untranslated): '000Og' appears to be a scan artifact and is unchanged from the source; no translation issue if it is a placeholder, but it is not English text. Suggested translation: "000Og" | 000Og | 000Og |
| error | 36 | p35_s0 | Reviewer (terminology): The glossary gives 练习 => exercise, but '练习一' as a section title is conventionally 'Exercise 1'; if a heading, it should follow the glossary and be 'Exercise 1'. Suggested translation: "Exercise 1" | 练习一 | Exercise 1 |
| error | 37 | p36_s12 | Reviewer (meaning): Source '5-5日' has the trailing 日 dropped, losing part of the source content. | 5-5日 | 5-5 |
| error | 37 | p36_s6 | Reviewer (meaning): The source '目5-2日' contains OCR-garbled characters (目...日) that are dropped; the translation only keeps '5-2'. | 目5-2日 | 5-2 |
| error | 47 | p46_s0 | Reviewer (terminology): Title should match the standard title-case convention and be a natural heading; 'Chicks Eating' is acceptable but 'Chicks Eat Food' closer. No change required beyond title case. Suggested translation: "Chicks Eating Food" | 小鸡吃食 | Chicks Eating |
| error | 48 | p47_s5 | Reviewer (meaning): Source '还有8级！' means '8 steps left/remaining', not '8 steps to go' is close, but 'Come on, 8 steps to go!' is acceptable. Actually '还有8级' = 'there are still 8 levels/steps'. Translation is fine. No finding. Remove this entry if not needed. Suggested translation: "Come on, 8 more steps!" | 加油，还有8级！ | Come on, 8 steps to go! |
| error | 49 | p48_s2 | Reviewer (untranslated): Place name kept in pinyin as a proper noun: correct, no finding. | 三家店 | Sanjiadian |
| error | 52 | p51_s0 | Reviewer (terminology): 练习二 should follow the glossary term 练习 => exercise, and the source numbering is Chinese; 'Exercise 2' is acceptable, but consider consistency. | 练习二 | Exercise 2 |
| error | 53 | p52_s14 | Reviewer (meaning): '摆一摆' means to arrange/manipulate objects, but the more natural textbook wording is 'Use objects to represent and calculate' or 'Show and calculate'. Suggested translation: "7. Arrange and calculate." | 7.摆一摆，算一算。 | 7. Arrange and calculate. |
| error | 56 | p55_s20 | Reviewer (untranslated): The source has '3十7' and '9一1' with Chinese characters 十 and 一; the translation keeps the Chinese characters 十 and 一, which should be plus/minus or full equations. Suggested translation: "Think about it. What problems can 3 + 7 solve? What about 9 - 1?" | 想一想，3十7可以解决什么问题？9一1呢？ | Think about it. What problems can 3十7 solve? What about 9一1? |
| error | 57 | p56_s10 | Reviewer (untranslated): 光明小学 is a proper name; 'Guangming School' is acceptable, but 'Guangming Primary School' is more precise. Suggested translation: "Guangming Primary School" | 光明小学 | Guangming School |
| error | 58 | p57_s4 | Reviewer (omission): '一共有' followed by '只动物' is split across items; the translation 'There are' + 'animals in total' is fine, but '一共有' alone should include the blank/number placeholder if present in source. | 一共有 | There are |
| error | 61 | p60_s11 | Reviewer (omission): The final clause 'they are all' has no completion, and the ellipsis placement differs from the source; the sentence ends with '它们都是' requiring the category word. Suggested translation: "Put the balls, toy cars and ······ together; they are all" | 把球、小汽车和······放在一起它们都是 | Put the balls, toy cars and ······ together; they are all |
| error | 63 | p62_s10 | Reviewer (untranslated): The fragment 'ercise' is a broken piece of an English word and is not a translation of 练; the source character is part of a split label '练习'. Suggested translation: "Practice" | 练 | ercise |
| error | 63 | p62_s11 | Reviewer (untranslated): The fragment 'ercise' is a broken piece of an English word and is not a translation of 文; the source character is part of a split label '语文'. Suggested translation: "Chinese" | 文 | ercise |
| error | 78 | p77_s7 | Reviewer (terminology): '10个一' should be '10 ones' with singular 'one', matching place-value terminology; '10 ones' uses plural incorrectly in this counting sense. Suggested translation: "10 ones" | 10个一 | 10 ones |
| error | 85 | p84_s1 | Reviewer (untranslated): The source "mmhwn" is left untranslated; this is a garbled/placeholder-like fragment but should be rendered or flagged as a placeholder consistently. | mmhwn | mmhwn |
| error | 85 | p84_s2 | Reviewer (untranslated): The source "mmy" is left untranslated; it should be handled as a placeholder rather than kept verbatim. | mmy | mmy |
| error | 92 | p91_s2 | Reviewer (terminology): 'on Taoqi's campus' — 校园 is school campus; 'school' or 'campus' both fine, but 'campus' is not usually used for a primary school. Consider 'at Taoqi's school'. Suggested translation: "Can you find math problems at Taoqi's school?" | 你能找到淘气校园里的数学问题吗？ | Can you find math problems on Taoqi's campus? |
| error | 95 | p94_s8 | Reviewer (meaning): '还摸吗？' means 'Should I/we draw another?' The translation 'Draw again?' is a command, changing the meaning from a question about whether to draw more. Suggested translation: "3, 5. Should I draw another?" | 3，5。还摸吗？ | 3, 5. Draw again? |
| error | 96 | p95_s0 | Reviewer (number): The heading is '八 380.1.0 认识钟表'. The translation keeps '380.1.0', which is a garbled scan artifact (likely '8' and a page/section number). The unit heading should be 'Unit 8 Understanding Clocks'. The '380.1.0' should not appear in the English. Suggested translation: "Unit 8 Understanding Clocks" | 八 380.1.0认识钟表 | Unit 8 380.1.0 Understanding Clocks |
| error | 96 | p95_s9 | Reviewer (untranslated): 'ii ip' is a scan artifact. It should probably be a clock-face description or left as a placeholder; keeping it is questionable but it is not translatable text. | ii ip | ii ip |
| error | 97 | p96_s14 | Reviewer (number): '3时' should be '3 o'clock', not '3 h' (inconsistent with p96_s12 '1 o'clock'). Suggested translation: "3 o'clock" | 3时 | 3 h |
| error | 97 | p96_s4 | Reviewer (meaning): '农' and '场' are separate characters split across two items (p96_s4 and p96_s5) that form the word 农场 'farm'. Translating '农' as 'Farm' and '场' as 'yard' splits the word and produces nonsense ('Farm' + 'yard'). They belong together as 'Farm' or the split should be preserved as characters. | 农 | Farm |
| error | 97 | p96_s6 | Reviewer (meaning): '小' and '学' (p96_s6 '小' => 'Primary', p96_s7 '学' => 'School') are split characters of 小学 'primary school'. Translating them separately as 'Primary' and 'School' is misleading; they form one word. | 小 | Primary |
| warning | 7 | p6_s0 | Reviewer (format): Class label formatting: Chinese convention is "Class 2"; "(2) Class" reverses the standard order. Suggested translation: "Class 2" | (2）班 | (2) Class |
| warning | 8 | p7_s6 | Reviewer (format): Heading fragment missing final period; also "it" is an addition not present in the source. Suggested translation: "Find and talk about" | 找一找，说一说 | Find and talk about it |
| warning | 10 | p9_s0 | Reviewer (grammar): "talk about it" is awkward for 说一说 in an exercise instruction; a natural rendering is "look and say". Suggested translation: "3. Look and say." | 3.看一看，说一说 | 3. Look and talk about it |
| warning | 11 | p10_s1 | Reviewer (grammar): "Count and talk about it" is unnatural; use "Count and say". Suggested translation: "Count and say" | 数一数，说一说 | Count and talk about it |
| warning | 11 | p10_s2 | Reviewer (grammar): The sentence is left incomplete in English; it should read naturally as a statement of counting. Suggested translation: "1, 2, 3, 4, there are" | 1，2，3，4，有 | 1, 2, 3, 4, there are |
| warning | 15 | p14_s2 | Reviewer (grammar): Missing the object of "do" relative to the source 做一做; earlier parallel item reads "Think and do it." Suggested translation: "Think and do." | 想一想，做一做 | Think and do. |
| warning | 16 | p15_s2 | Reviewer (grammar): "Find and talk about it" is awkward; use "Find and say." Suggested translation: "Find and say." | 找一找，说一说 | Find and talk about it. |
| warning | 16 | p15_s4 | Reviewer (grammar): "Jump and talk about it" is awkward; use "Jump and say." Suggested translation: "Jump and say." | 跳一跳，说一说。 | Jump and talk about it. |
| warning | 25 | p24_s7 | Reviewer (format): “比一比，填一填” has no final period in the source; the translation adds one. Consistency with other labels is minor. Suggested translation: "Compare and fill in" | 比一比，填一填 | Compare and fill in. |
| warning | 30 | p29_s1 | Reviewer (format): The source '4.说一说。' keeps its period and marker; the translation keeps it correctly, but the numbering convention for this item should match the source exactly. Suggested translation: "4. Talk about it." | 4.说一说。 | 4. Talk about it. |
| warning | 34 | p33_s7 | Reviewer (format): '拨一拨' is literally 'move/slide the beads' on a counting frame; 'Move the beads' is acceptable but should be consistent with the counting-frame terminology. Suggested translation: "Move the beads and fill in" | 拨一拨，填一填 | Move the beads and fill in |
| warning | 35 | p34_s21 | Reviewer (format): The source '4.说一说。' includes a period; the translation keeps the numbering but the sentence punctuation should match the source. Suggested translation: "4. Talk about it." | 4.说一说。 | 4. Talk about it. |
| warning | 43 | p42_s1 | Reviewer (grammar): 'Colour' is British spelling; for consistency with textbook convention use 'Color'. Suggested translation: "Color and fill in" | 涂一涂，填一填 | Colour and fill in |
| warning | 44 | p43_s5 | Reviewer (format): Heading is rendered without title case; headings should use Title Case. Suggested translation: "Fill In" | 填巾 | Fill in |
| warning | 50 | p49_s9 | Reviewer (format): Unnecessary capital 'C' in 'Calculate' mid-sentence. Suggested translation: "2. Talk about it, then calculate." | 2.说一说，算一算。 | 2. Talk about it, then Calculate. |
| warning | 51 | p50_s3 | Reviewer (format): '10 children' is fine; no issue. | 4. 10个小朋友做游戏。 | 4. 10 children are playing a game. |
| warning | 54 | p53_s31 | Reviewer (grammar): 'Taoqi made' is acceptable; more natural: 'Here is the addition table Taoqi made.' | 下面是淘气做的加法表，你能帮他填完整吗？ | Below is the addition table Taoqi made. Can you help him co… |
| warning | 55 | p54_s21 | Reviewer (format): '6 -' is a label fragment; keeping it as '6 −' or '6 minus' may be clearer, but it preserves the source. | 6一 | 6 - |
| warning | 58 | p57_s5 | Reviewer (grammar): 'animals in total.' is fine as a fragment, but 'animals.' with 'in total' in the previous item may be more natural. | 只动物。 | animals in total. |
| warning | 59 | p58_s4 | Reviewer (grammar): Missing end punctuation; also 'fill in' needs an object in textbook style. Suggested translation: "7. Think and fill in the blanks" | 7.想一想，填一填 | 7. Think and fill in |
| warning | 63 | p62_s14 | Reviewer (grammar): Standalone label 'Chinese' is fine but should match the format of other labels; no change needed if the split-label rendering is intentional. | 语文 | Chinese |
| warning | 70 | p69_s2 | Reviewer (format): Placeholder should precede the word where the blank belongs; spacing is off. Suggested translation: "⟦276.3.0⟧ The other hand is" | 276.3.0另一只手是 | 276.3.0 The other hand is |
| warning | 71 | p70_s11 | Reviewer (grammar): 'point' needs an object; the natural phrasing is 'point to them'. Suggested translation: "3. Talk about it and point to them." | 3.说一说，指一指。 | 3. Talk about it and point. |
| warning | 71 | p70_s14 | Reviewer (format): The answer blank is empty parentheses '()'; it should be kept with a blank, not shown as '() cars' with nothing inside. Suggested translation: "4. Counting from the right, there are ( ) cars in total. Try drawing a picture." | 4.从右数，共有(）辆车。请画图试一试。 | 4. Counting from the right, there are () cars in total. Try… |
| warning | 74 | p73_s0 | Reviewer (format): The placeholder ⟦0⟧ (page/scan artifact) is missing from the translation; the source has it and it must be reproduced. Suggested translation: "Unit 6 Recognizing ⟦0⟧ Shapes" | 六292.0.0认识图形 | Unit 6 Recognizing 292.0.0 Shapes |
| warning | 74 | p73_s18 | Reviewer (format): The source uses the Chinese ellipsis '····' (four dots); the translation uses three dots. Suggested translation: "It can roll forward and backward...." | 可以前后滚动···· | It can roll forward and backward... |
| warning | 78 | p77_s1 | Reviewer (format): Heading 'How Ancients Counted' does not use Title Case as required for headings. Suggested translation: "How the Ancients Counted" | 古人计数 | How Ancients Counted |
| warning | 78 | p77_s8 | Reviewer (grammar): '1个十' is translated '1 tens' — number agreement is wrong; should be '1 ten'. Suggested translation: "1 ten" | 1个十 | 1 tens |
| warning | 79 | p78_s12 | Reviewer (grammar): "Do it." is unnatural for a textbook instruction; 做一做 is the standard hands-on activity heading. Suggested translation: "2. Try it." | 2.做一做。 | 2. Do it. |
| warning | 80 | p79_s12 | Reviewer (grammar): "Read and tell." is awkward; 讲一讲 means "tell/discuss the story". Suggested translation: "9. Read and discuss. Long ago, people counted by tying knots in a rope. For example, for 3 sheep, they tied 3 knots in the rope." | 9.读一读，讲一讲古时候，人们用在绳子上打结的方法来计数。比如，3只羊，就在绳子上打3个结来表示。 | 9. Read and tell. Long ago, people counted by tying knots i… |
| warning | 80 | p79_s9 | Reviewer (grammar): "Talk." is not idiomatic for 说一说; textbook convention is "Discuss." or "Say and share." Suggested translation: "8. Discuss." | 8.说一说。 | 8. Talk. |
| warning | 81 | p80_s0 | Reviewer (format): Heading 搭积木 is a title and, per instructions, headings use Title Case; "Building Blocks" is acceptable but 搭积木 more precisely means "Building with Blocks". Suggested translation: "Building with Blocks" | 搭积木 | Building Blocks |
| warning | 82 | p81_s21 | Reviewer (grammar): "Talk about it." is awkward; 说一说 convention is "Discuss." Suggested translation: "5. Discuss. What results can you get?" | 5.说一说，你能得到哪些结果？ | 5. Talk about it. What results can you get? |
| warning | 84 | p83_s7 | Reviewer (grammar): "Climb the mountain." is a literal rendering of 登山; in this exercise context it means "mountain climbing" as an activity title. Suggested translation: "3. Mountain Climbing." | 3.登山。 | 3. Climb the mountain. |
| warning | 86 | p85_s1 | Reviewer (grammar): "Arrange and calculate" for 摆一摆，算一算 is not idiomatic; 摆一摆 involves using counters. Suggested translation: "1. Use counters and calculate." | 1.摆一摆，算一算。 | 1. Arrange and calculate. |
| warning | 86 | p85_s4 | Reviewer (grammar): The Chinese commands 圈一圈，算一算 are conventionally rendered with an object or as 'Circle and calculate'; 'Circle and calculate' is acceptable, but 'calculate' alone slightly loses the 'work out the answer' sense. Consider 'Circle and calculate.' is fine; no change needed. However, consistency with the glossary ('算一算' => 'Calculate') is met. | 2.圈一圈，算一算。 | 2. Circle and calculate. |
| warning | 86 | p85_s6 | Reviewer (grammar): 'Look and fill in' is acceptable, but '填一填' is glossed as 'Fill in'; 'Look and fill in' matches. | 3.看一看，填一填。 | 3. Look and fill in. |
| warning | 87 | p86_s0 | Reviewer (format): Heading casing: 'How Many Birds' is in Title Case, which follows the convention for headings. Acceptable. | 有几只小鸟 | How Many Birds |
| warning | 87 | p86_s6 | Reviewer (format): Single-character column labels 十位个位 should use the standard abbreviations T and O rather than 'Tens Ones'. Suggested translation: "T O" | 十位个位 | Tens Ones |
| warning | 87 | p86_s7 | Reviewer (format): Single-character column labels 十位个位 should use the standard abbreviations T and O rather than 'Tens Ones'. Suggested translation: "T O" | 十位个位 | Tens Ones |
| warning | 87 | p86_s8 | Reviewer (format): Single-character column labels 十位个位 should use the standard abbreviations T and O rather than 'Tens Ones'. Suggested translation: "T O" | 十位个位 | Tens Ones |
| warning | 87 | p86_s9 | Reviewer (grammar): Same as p85_s4: 'Circle and calculate' is acceptable. | 圈一圈，算一算。 | Circle and calculate. |
| warning | 88 | p87_s42 | Reviewer (format): The source '十+' is a column label for the tens place with a plus sign (place-value chart); translating it as 'T +' loses the '十' column label, which should be 'T' with the plus: 'T +'. Actually '十' as a column label is 'T', so 'T +' is correct per place-value conventions. | 十+ | T + |
| warning | 93 | p92_s11 | Reviewer (grammar): Missing comma / conjunction between the two clauses: 'many female teachers and few male teachers' is fine but the comma splice should be avoided. Suggested translation: "The school has many female teachers and few male teachers..." | 学校女老师很多男老师很少··· | The school has many female teachers and few male teachers... |
| warning | 93 | p92_s6 | Reviewer (format): '想一想' is a fixed exercise label; the standard rendering is 'Think' but the more idiomatic textbook label is 'Think about it'. Not misleading. Suggested translation: "Think about it" | 想一想 | Think |
| warning | 93 | p92_s7 | Reviewer (grammar): 'in your campus' is unnatural English; 'on your campus' or 'at your school' is standard. Suggested translation: "What math information is there on your campus? What math questions can you ask?" | 你的校园里有哪些数学信息？你能提出哪些数学问题？ | What math information is there in your campus? What math qu… |
| warning | 93 | p92_s8 | Reviewer (format): Ellipsis style: source uses '····' style trailing dots; translation uses '...'. Acceptable but inconsistent with other items. No meaning change. | 我们班有20名男生···· | Our class has 20 boys... |
| warning | 96 | p95_s12 | Reviewer (grammar): 'I say, you set the clock.' is acceptable; clearer is 'I say the time, you set the clock.' Suggested translation: "I say the time, you set the clock." | 我说你拨。 | I say, you set the clock. |
| warning | 97 | p96_s12 | Reviewer (format): Inconsistent clock-time style: '1 o'clock' here vs '3 h' in p96_s14. Should all be 'o'clock'. Suggested translation: "1 o'clock" | 1时 | 1 o'clock |
| warning | 97 | p96_s13 | Reviewer (format): Inconsistent with p96_s15 '11:30'; should be 'half past 10' consistently, or '10:30'. Suggested translation: "half past 10" | 10时半 | half past 10 |
| warning | 97 | p96_s15 | Reviewer (format): '11时半' rendered as '11:30' while p96_s13 uses 'half past 10' and p96_s16 'half past 5'. Inconsistent style; use 'half past 11'. Suggested translation: "half past 11" | 11时半 | 11:30 |
| warning | 97 | p96_s16 | Reviewer (format): Consistent with p96_s13. No change needed. | 5时半 | half past 5 |
| warning | 97 | p96_s9 | Reviewer (grammar): Missing final period after 'Match' (source has no period either, but the label '连一连' is conventionally 'Match.'). Minor. Suggested translation: "2. Match." | 2.连一连 | 2. Match |

### `untranslated` — 1 error, 0 warnings

| Severity | Page | Segment | Message | Source | Translation |
|---|---|---|---|---|---|
| error | 56 | p55_s20 | 2 letter(s) of the source script remain untranslated ("十", "一"); translate all text into English | 想一想，3十7可以解决什么问题？9一1呢？ | Think about it. What problems can 3十7 solve? What about 9一1? |

### `image_text` — 0 errors, 16 warnings

| Severity | Page | Segment | Message | Source | Translation |
|---|---|---|---|---|---|
| warning | 20 | p19_i76_13 | The text '比（多，少），姓比' was left in the source language (inline pictograms the OCR cannot read (left in the picture)): the line is built around symbols or pictures the OCR could not read - check the page in the preview | 比（多，少），姓比 |  |
| warning | 20 | p19_i76_13 | The text '比（多，少），姓比' was left in the source language (inline pictograms the OCR cannot read (left in the picture)): the line is built around symbols or pictures the OCR could not read - check the page in the preview | 比（多，少），姓比 |  |
| warning | 21 | p20_i80_3 | The text '比篷（多，少），3' was left in the source language (inline pictograms the OCR cannot read (left in the picture)): the line is built around symbols or pictures the OCR could not read - check the page in the preview | 比篷（多，少），3 |  |
| warning | 21 | p20_i80_3 | The text '比篷（多，少），3' was left in the source language (inline pictograms the OCR cannot read (left in the picture)): the line is built around symbols or pictures the OCR could not read - check the page in the preview | 比篷（多，少），3 |  |
| warning | 21 | p20_i80_4 | The text '比' was left in the source language (inline pictograms the OCR cannot read (left in the picture)): the line is built around symbols or pictures the OCR could not read - check the page in the preview | 比 |  |
| warning | 21 | p20_i80_4 | The text '比' was left in the source language (inline pictograms the OCR cannot read (left in the picture)): the line is built around symbols or pictures the OCR could not read - check the page in the preview | 比 |  |
| warning | 21 | p20_i80_7 | The text '比' was left in the source language (inline pictograms the OCR cannot read (left in the picture)): the line is built around symbols or pictures the OCR could not read - check the page in the preview | 比 |  |
| warning | 21 | p20_i80_7 | The text '比' was left in the source language (inline pictograms the OCR cannot read (left in the picture)): the line is built around symbols or pictures the OCR could not read - check the page in the preview | 比 |  |
| warning | 21 | p20_i80_9 | The text '比' was left in the source language (inline pictograms the OCR cannot read (left in the picture)): the line is built around symbols or pictures the OCR could not read - check the page in the preview | 比 |  |
| warning | 21 | p20_i80_9 | The text '比' was left in the source language (inline pictograms the OCR cannot read (left in the picture)): the line is built around symbols or pictures the OCR could not read - check the page in the preview | 比 |  |
| warning | 27 | p26_i104_19 | The text '，最重的画“”' was left in the source language (unreadable symbol in quotes (left in the picture)): the line is built around symbols or pictures the OCR could not read - check the page in the preview | ，最重的画“” |  |
| warning | 27 | p26_i104_19 | The text '，最重的画“”' was left in the source language (unreadable symbol in quotes (left in the picture)): the line is built around symbols or pictures the OCR could not read - check the page in the preview | ，最重的画“” |  |
| warning | 57 | p56_i224_23 | The text '比' was left in the source language (inline pictograms the OCR cannot read (left in the picture)): the line is built around symbols or pictures the OCR could not read - check the page in the preview | 比 |  |
| warning | 57 | p56_i224_23 | The text '比' was left in the source language (inline pictograms the OCR cannot read (left in the picture)): the line is built around symbols or pictures the OCR could not read - check the page in the preview | 比 |  |
| warning | 99 | p98_i392_5 | The text '比' was left in the source language (inline pictograms the OCR cannot read (left in the picture)): the line is built around symbols or pictures the OCR could not read - check the page in the preview | 比 |  |
| warning | 99 | p98_i392_5 | The text '比' was left in the source language (inline pictograms the OCR cannot read (left in the picture)): the line is built around symbols or pictures the OCR could not read - check the page in the preview | 比 |  |

### `length_ratio` — 0 errors, 1 warning

| Severity | Page | Segment | Message | Source | Translation |
|---|---|---|---|---|---|
| warning | 25 | p24_s10 | The translation looks too short: 5 characters for 13 translatable source characters (ratio 0.38, about 2.60 expected); check that nothing was omitted | 号→□96.16.0号→□96.16.1号→□96.16.2号 | → 96.16.0 → 96.16.1 → 96.16.2 |
