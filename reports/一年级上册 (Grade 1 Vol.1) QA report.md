# QA report

**Result:** QA FAILED after 3 rounds: 182 errors, 150 warnings (1811.1 s); proofread: 484 corrections applied; output file checks: 0 error(s)

**Document:** 数学 (zh → en, 109 page(s), 1077 translatable segment(s))

**Checks run:** `completeness`, `placeholders`, `numbers`, `untranslated`, `target_script`, `glossary`, `length_ratio`, `formatting`, `layout_fit`, `image_text`, `llm_review`, `output_checks`

## Rounds

| Round | Errors | Warnings | Re-translated | Passed | Duration |
|---|---|---|---|---|---|
| 1 | 262 | 183 | 245 segment(s) | no | 418.7 s |
| 2 | 235 | 214 | 217 segment(s) | no | 296.5 s |
| 3 | 175 | 177 | 0 segment(s) | no | 74.1 s |

- Round 1: llm_review ×298, layout_fit ×104, formatting ×16, image_text ×11, glossary ×9, untranslated ×4, completeness ×3
- Round 2: llm_review ×341, layout_fit ×85, image_text ×11, formatting ×7, glossary ×2, placeholders ×2, untranslated ×1
- Round 3: llm_review ×229, layout_fit ×89, image_text ×11, glossary ×9, formatting ×6, untranslated ×4, placeholders ×3, completeness ×1

## Final issues (332)

### `completeness` — 3 errors, 0 warnings

| Severity | Page | Segment | Message | Source | Translation |
|---|---|---|---|---|---|
| error | 19 | p18_s3 | The translation "." contains no words; translate the complete source text | 一样多。 | . |
| error | 25 | p24_s11 | The translation "→" contains no words; translate the complete source text | 号→ | → |
| error | 97 | p96_s5 | The translation "____" contains no words; translate the complete source text | 场 | ____ |

### `formatting` — 12 errors, 3 warnings

| Severity | Page | Segment | Message | Source | Translation |
|---|---|---|---|---|---|
| error | 7 | p6_s0 | Start the translation with the list marker "(2）" exactly as in the source | (2）班 | Class 2 |
| error | 19 | p18_s2 | The translation still contains the raw placeholder "⟦0⟧"; use only the ⟦n⟧ placeholders that occur in the source, each exactly once | 每，和 | each ⟦0⟧, and ⟦0⟧ |
| error | 19 | p18_s5 | Remove the symbol(s) ○: they are not in the source (a picture in the book is not a symbol; leave it out rather than inventing one) | 画，比多72.6.0。 | Draw more ○ than 72.6.0. |
| error | 22 | p21_s5 | Remove the symbol(s) ✓: they are not in the source (a picture in the book is not a symbol; leave it out rather than inventing one) | ”，最少的画 | "✓", the least with |
| error | 25 | p24_s10 | Keep the symbol(s) □×3 of the source in the translation, at the matching position | 号→□96.16.0号→□96.16.1号→□96.16.2号 | → 96.16.0 → 96.16.1 → 96.16.2 |
| error | 35 | p34_s1 | The source does not end with a question mark; do not end the translation with one | 1.还有几个136.1.0 | 1. How many 136.1.0 are left? |
| error | 46 | p45_s5 | The source does not end with a question mark; do not end the translation with one | 3.房子里有几只 | 3. How many are in the house? |
| error | 59 | p58_s1 | Remove the symbol(s) ○ ✓: they are not in the source (a picture in the book is not a symbol; leave it out rather than inventing one) | 爬得最高的画最低的画 | Draw ✓ for the highest climber and ○ for the lowest. |
| error | 84 | p83_s5 | The source does not end with a question mark; do not end the translation with one | 共有几条业332.7.0 | Altogether, how many 332.7.0? |
| error | 89 | p88_s2 | The source does not end with a question mark; do not end the translation with one | 在第—级台阶，在第—级台阶，在第—级台阶，在第_在第—级台阶，在第——级台阶，在第_级台阶，只在第_级台阶，站在第9级… | Which step is each person on? Step ___, step ___, step ___,… |
| error | 99 | p98_s11 | Remove the symbol(s) □ △ ○: they are not in the source (a picture in the book is not a symbol; leave it out rather than inventing one) | 3.画一画。在画☆，上面画，左边画，下面画 | 3. Draw. Draw ☆ to the right of the flower, □ above it, △ t… |
| error | 105 | p104_s0 | The source does not end with a question mark; do not end the translation with one | 本学期你学到了什么 | What did you learn this term? |
| warning | 18 | p17_s2 | The source does not end with a exclamation mark; do not end the translation with one | 样多，够了 | The same number. Enough! |
| warning | 67 | p66_s8 | The source does not end with a exclamation mark; do not end the translation with one | 把得数小的排在前面 | Smaller answers go in front! |
| warning | 74 | p73_s17 | The source does not end with a exclamation mark; do not end the translation with one | 嘻嘻，我知道了。 | Hee hee, now I know! |

### `glossary` — 17 errors, 0 warnings

| Severity | Page | Segment | Message | Source | Translation |
|---|---|---|---|---|---|
| error | 10 | p9_s7 | Glossary: translate "找一找" as "Find" | 5.找一找生活中的数。 | 5. Look for numbers in everyday life. |
| error | 36 | p35_s0 | Glossary: translate "练习" as "exercise" | 练习一 | Practice 1 |
| error | 61 | p60_s13 | Glossary: translate "妙想" as "Miaoxiang" | 妙想 | Miaox. |
| error | 63 | p62_s12 | Glossary: translate "练习" as "exercise" | 语文练习本语文 | Chinese workbook; Chinese |
| error | 63 | p62_s13 | Glossary: translate "练习" as "exercise" | 练习木数学练习本语文 | workbook; Maths workbook; Chinese |
| error | 63 | p62_s16 | Glossary: translate "练习" as "exercise" | 练习本数学 | workbook; Maths |
| error | 63 | p62_s19 | Glossary: translate "练习" as "exercise" | 数学练习本数学 | Maths workbook; Maths |
| error | 63 | p62_s3 | Glossary: translate "练习" as "exercise" | 数学语文练习本 | Maths; Chinese workbook |
| error | 63 | p62_s4 | Glossary: translate "练习" as "exercise" | 数学练习本 | Maths workbook |
| error | 71 | p70_s4 | Glossary: translate "练习" as "exercise" | 练习本 | workbook |
| error | 87 | p86_s6 | Glossary: translate "个位" as "ones" | 十位个位 | T O |
| error | 87 | p86_s6 | Glossary: translate "十位" as "tens" | 十位个位 | T O |
| error | 87 | p86_s7 | Glossary: translate "个位" as "ones" | 十位个位 | T O |
| error | 87 | p86_s7 | Glossary: translate "十位" as "tens" | 十位个位 | T O |
| error | 87 | p86_s8 | Glossary: translate "个位" as "ones" | 十位个位 | T O |
| error | 87 | p86_s8 | Glossary: translate "十位" as "tens" | 十位个位 | T O |
| error | 94 | p93_s2 | Glossary: translate "比一比" as "Compare" | 2人一组做游戏，比一比哪组堆得又快又高。 | Play in groups of 2. See which group can stack the fastest … |

### `layout_fit` — 114 errors, 68 warnings

| Severity | Page | Segment | Message | Source | Translation |
|---|---|---|---|---|---|
| error | 3 | p2_s17 | Shorten the translation to at most 24 characters so it fits the original box (the current translation of 29 characters overflows its box; the minimum allowed size is 55%) | 编者大朋友 | Your big friends, the editors |
| error | 3 | p2_s17 | Shorten the translation to at most 24 characters so it fits the original box (the current translation of 29 characters overflows its box; the minimum allowed size is 55%) | 编者大朋友 | Your big friends, the editors |
| error | 5 | p4_s2 | Shorten the translation to at most 26 characters so it fits the original box (the current translation of 31 characters overflows its box; the minimum allowed size is 55%) | 七加与减 | Unit 7 Addition and Subtraction |
| error | 5 | p4_s2 | Shorten the translation to at most 26 characters so it fits the original box (the current translation of 31 characters overflows its box; the minimum allowed size is 55%) | 七加与减 | Unit 7 Addition and Subtraction |
| error | 8 | p7_s4 | Shorten the translation to at most 6 characters so it fits the original box (the current translation of 8 characters overflows its box; the minimum allowed size is 55%) | 1筐 | 1 basket |
| error | 8 | p7_s4 | Shorten the translation to at most 6 characters so it fits the original box (the current translation of 8 characters overflows its box; the minimum allowed size is 55%) | 1筐 | 1 basket |
| error | 13 | p12_s3 | Shorten the translation to at most 25 characters so it fits the original box (the current translation of 31 characters overflows its box; the minimum allowed size is 55%) | 一条鱼也没有 | No fish at all is written as 0. |
| error | 13 | p12_s3 | Shorten the translation to at most 25 characters so it fits the original box (the current translation of 31 characters overflows its box; the minimum allowed size is 55%) | 一条鱼也没有 | No fish at all is written as 0. |
| error | 15 | p14_s0 | Shorten the translation to at most 5 characters so it fits the original box (the current translation of 10 characters overflows its box; the minimum allowed size is 55%) | 文具 | Stationery |
| error | 15 | p14_s0 | Shorten the translation to at most 5 characters so it fits the original box (the current translation of 10 characters overflows its box; the minimum allowed size is 55%) | 文具 | Stationery |
| error | 20 | p19_s1 | Shorten the translation to at most 9 characters so it fits the original box (the current translation of 11 characters overflows its box; the minimum allowed size is 55%) | 动物乐园 | Animal Park |
| error | 20 | p19_s1 | Shorten the translation to at most 9 characters so it fits the original box (the current translation of 11 characters overflows its box; the minimum allowed size is 55%) | 动物乐园 | Animal Park |
| error | 25 | p24_s5 | Shorten the translation to at most 27 characters so it fits the original box (the current translation of 32 characters overflows its box; the minimum allowed size is 55%) | 桥下通过吗？ | Can the car go under the bridge? |
| error | 25 | p24_s5 | Shorten the translation to at most 27 characters so it fits the original box (the current translation of 32 characters overflows its box; the minimum allowed size is 55%) | 桥下通过吗？ | Can the car go under the bridge? |
| error | 26 | p25_s10 | Shorten the translation to at most 5 characters so it fits the original box (the current translation of 8 characters overflows its box; the minimum allowed size is 55%) | 轻 | lighter. |
| error | 26 | p25_s10 | Shorten the translation to at most 5 characters so it fits the original box (the current translation of 8 characters overflows its box; the minimum allowed size is 55%) | 轻 | lighter. |
| error | 26 | p25_s11 | Shorten the translation to at most 5 characters so it fits the original box (the current translation of 8 characters overflows its box; the minimum allowed size is 55%) | 重 | heavier. |
| error | 26 | p25_s11 | Shorten the translation to at most 5 characters so it fits the original box (the current translation of 8 characters overflows its box; the minimum allowed size is 55%) | 重 | heavier. |
| error | 26 | p25_s2 | Shorten the translation to at most 24 characters so it fits the original box (the current translation of 36 characters overflows its box; the minimum allowed size is 55%) | 100.2.l比100.2.0重 | 100.2.l is heavier than 100.2.0. |
| error | 26 | p25_s2 | Shorten the translation to at most 24 characters so it fits the original box (the current translation of 36 characters overflows its box; the minimum allowed size is 55%) | 100.2.l比100.2.0重 | 100.2.l is heavier than 100.2.0. |
| error | 26 | p25_s3 | Shorten the translation to at most 8 characters so it fits the original box (the current translation of 21 characters overflows its box; the minimum allowed size is 55%) | 100.3.l比100.3.r | 100.3.l100.3.r is |
| error | 26 | p25_s3 | Shorten the translation to at most 8 characters so it fits the original box (the current translation of 21 characters overflows its box; the minimum allowed size is 55%) | 100.3.l比100.3.r | 100.3.l100.3.r is |
| error | 26 | p25_s4 | Shorten the translation to at most 17 characters so it fits the original box (the current translation of 23 characters overflows its box; the minimum allowed size is 55%) | 100.4.0轻 | lighter than 100.4.0. |
| error | 26 | p25_s4 | Shorten the translation to at most 17 characters so it fits the original box (the current translation of 23 characters overflows its box; the minimum allowed size is 55%) | 100.4.0轻 | lighter than 100.4.0. |
| error | 26 | p25_s9 | Shorten the translation to at most 32 characters so it fits the original box (the current translation of 79 characters overflows its box; the minimum allowed size is 55%) | 100.12.l比100.12.r100.14.l比100.14.r | Compared with 100.12.r, 100.12.l is Compared with 100.… |
| error | 26 | p25_s9 | Shorten the translation to at most 32 characters so it fits the original box (the current translation of 79 characters overflows its box; the minimum allowed size is 55%) | 100.12.l比100.12.r100.14.l比100.14.r | Compared with 100.12.r, 100.12.l is Compared with 100.… |
| error | 28 | p27_s12 | Shorten the translation to at most 7 characters so it fits the original box (the current translation of 9 characters overflows its box; the minimum allowed size is 55%) | 加号 | plus sign |
| error | 28 | p27_s12 | Shorten the translation to at most 7 characters so it fits the original box (the current translation of 9 characters overflows its box; the minimum allowed size is 55%) | 加号 | plus sign |
| error | 28 | p27_s13 | Shorten the translation to at most 23 characters so it fits the original box (the current translation of 27 characters overflows its box; the minimum allowed size is 55%) | 读作：3加2等于5。 | Read as: 3 plus 2 equals 5. |
| error | 28 | p27_s13 | Shorten the translation to at most 23 characters so it fits the original box (the current translation of 27 characters overflows its box; the minimum allowed size is 55%) | 读作：3加2等于5。 | Read as: 3 plus 2 equals 5. |
| error | 30 | p29_s4 | Shorten the translation to at most 10 characters so it fits the original box (the current translation of 12 characters overflows its box; the minimum allowed size is 55%) | 个。 | more apples. |
| error | 30 | p29_s4 | Shorten the translation to at most 10 characters so it fits the original box (the current translation of 12 characters overflows its box; the minimum allowed size is 55%) | 个。 | more apples. |
| error | 31 | p30_s11 | Shorten the translation to at most 8 characters so it fits the original box (the current translation of 10 characters overflows its box; the minimum allowed size is 55%) | 减号 | minus sign |
| error | 31 | p30_s11 | Shorten the translation to at most 8 characters so it fits the original box (the current translation of 10 characters overflows its box; the minimum allowed size is 55%) | 减号 | minus sign |
| error | 31 | p30_s12 | Shorten the translation to at most 24 characters so it fits the original box (the current translation of 28 characters overflows its box; the minimum allowed size is 55%) | 读作：5减2等于3。 | Read as: 5 minus 2 equals 3. |
| error | 31 | p30_s12 | Shorten the translation to at most 24 characters so it fits the original box (the current translation of 28 characters overflows its box; the minimum allowed size is 55%) | 读作：5减2等于3。 | Read as: 5 minus 2 equals 3. |
| error | 33 | p32_s6 | Shorten the translation to at most 6 characters so it fits the original box (the current translation of 14 characters overflows its box; the minimum allowed size is 55%) | 支。 | fewer pencils. |
| error | 33 | p32_s6 | Shorten the translation to at most 6 characters so it fits the original box (the current translation of 14 characters overflows its box; the minimum allowed size is 55%) | 支。 | fewer pencils. |
| error | 40 | p39_s0 | Shorten the translation to at most 10 characters so it fits the original box (the current translation of 12 characters overflows its box; the minimum allowed size is 55%) | 背土豆 | Potato Carry |
| error | 40 | p39_s0 | Shorten the translation to at most 10 characters so it fits the original box (the current translation of 12 characters overflows its box; the minimum allowed size is 55%) | 背土豆 | Potato Carry |
| error | 42 | p41_s0 | Shorten the translation to at most 11 characters so it fits the original box (the current translation of 13 characters overflows its box; the minimum allowed size is 55%) | 跳绳 | Rope Skipping |
| error | 42 | p41_s0 | Shorten the translation to at most 11 characters so it fits the original box (the current translation of 13 characters overflows its box; the minimum allowed size is 55%) | 跳绳 | Rope Skipping |
| error | 47 | p46_s0 | Shorten the translation to at most 15 characters so it fits the original box (the current translation of 18 characters overflows its box; the minimum allowed size is 55%) | 小鸡吃食 | Chicks Eating Food |
| error | 47 | p46_s0 | Shorten the translation to at most 15 characters so it fits the original box (the current translation of 18 characters overflows its box; the minimum allowed size is 55%) | 小鸡吃食 | Chicks Eating Food |
| error | 49 | p48_s0 | Shorten the translation to at most 6 characters so it fits the original box (the current translation of 8 characters overflows its box; the minimum allowed size is 55%) | 乘车 | Bus Ride |
| error | 49 | p48_s0 | Shorten the translation to at most 6 characters so it fits the original box (the current translation of 8 characters overflows its box; the minimum allowed size is 55%) | 乘车 | Bus Ride |
| error | 50 | p49_s7 | Shorten the translation to at most 20 characters so it fits the original box (the current translation of 24 characters overflows its box; the minimum allowed size is 55%) | （1）一共有几个 | (1) Altogether, how many |
| error | 50 | p49_s7 | Shorten the translation to at most 20 characters so it fits the original box (the current translation of 24 characters overflows its box; the minimum allowed size is 55%) | （1）一共有几个 | (1) Altogether, how many |
| error | 54 | p53_s0 | Shorten the translation to at most 18 characters so it fits the original box (the current translation of 22 characters overflows its box; the minimum allowed size is 55%) | 做个加法表 | Make an Addition Table |
| error | 54 | p53_s0 | Shorten the translation to at most 18 characters so it fits the original box (the current translation of 22 characters overflows its box; the minimum allowed size is 55%) | 做个加法表 | Make an Addition Table |
| error | 58 | p57_s6 | Shorten the translation to at most 7 characters so it fits the original box (the current translation of 9 characters overflows its box; the minimum allowed size is 55%) | 排第 | is number |
| error | 58 | p57_s6 | Shorten the translation to at most 7 characters so it fits the original box (the current translation of 9 characters overflows its box; the minimum allowed size is 55%) | 排第 | is number |
| error | 59 | p58_s5 | Shorten the translation to at most 6 characters so it fits the original box (the current translation of 8 characters overflows its box; the minimum allowed size is 55%) | 有 | has ____ |
| error | 59 | p58_s5 | Shorten the translation to at most 6 characters so it fits the original box (the current translation of 8 characters overflows its box; the minimum allowed size is 55%) | 有 | has ____ |
| error | 63 | p62_s12 | Shorten the translation to at most 14 characters so it fits the original box (the current translation of 25 characters overflows its box; the minimum allowed size is 55%) | 语文练习本语文 | Chinese workbook; Chinese |
| error | 63 | p62_s12 | Shorten the translation to at most 14 characters so it fits the original box (the current translation of 25 characters overflows its box; the minimum allowed size is 55%) | 语文练习本语文 | Chinese workbook; Chinese |
| error | 63 | p62_s13 | Shorten the translation to at most 19 characters so it fits the original box (the current translation of 33 characters overflows its box; the minimum allowed size is 55%) | 练习木数学练习本语文 | workbook; Maths workbook; Chinese |
| error | 63 | p62_s13 | Shorten the translation to at most 19 characters so it fits the original box (the current translation of 33 characters overflows its box; the minimum allowed size is 55%) | 练习木数学练习本语文 | workbook; Maths workbook; Chinese |
| error | 63 | p62_s16 | Shorten the translation to at most 8 characters so it fits the original box (the current translation of 15 characters overflows its box; the minimum allowed size is 55%) | 练习本数学 | workbook; Maths |
| error | 63 | p62_s16 | Shorten the translation to at most 8 characters so it fits the original box (the current translation of 15 characters overflows its box; the minimum allowed size is 55%) | 练习本数学 | workbook; Maths |
| error | 63 | p62_s19 | Shorten the translation to at most 14 characters so it fits the original box (the current translation of 21 characters overflows its box; the minimum allowed size is 55%) | 数学练习本数学 | Maths workbook; Maths |
| error | 63 | p62_s19 | Shorten the translation to at most 14 characters so it fits the original box (the current translation of 21 characters overflows its box; the minimum allowed size is 55%) | 数学练习本数学 | Maths workbook; Maths |
| error | 63 | p62_s20 | Shorten the translation to at most 10 characters so it fits the original box (the current translation of 14 characters overflows its box; the minimum allowed size is 55%) | 数学语文 | Maths; Chinese |
| error | 63 | p62_s20 | Shorten the translation to at most 10 characters so it fits the original box (the current translation of 14 characters overflows its box; the minimum allowed size is 55%) | 数学语文 | Maths; Chinese |
| error | 63 | p62_s4 | Shorten the translation to at most 11 characters so it fits the original box (the current translation of 14 characters overflows its box; the minimum allowed size is 55%) | 数学练习本 | Maths workbook |
| error | 63 | p62_s4 | Shorten the translation to at most 11 characters so it fits the original box (the current translation of 14 characters overflows its box; the minimum allowed size is 55%) | 数学练习本 | Maths workbook |
| error | 63 | p62_s5 | Shorten the translation to at most 8 characters so it fits the original box (the current translation of 14 characters overflows its box; the minimum allowed size is 55%) | 数学药习本 | Maths workbook |
| error | 63 | p62_s5 | Shorten the translation to at most 8 characters so it fits the original box (the current translation of 14 characters overflows its box; the minimum allowed size is 55%) | 数学药习本 | Maths workbook |
| error | 65 | p64_s20 | Shorten the translation to at most 7 characters so it fits the original box (the current translation of 9 characters overflows its box; the minimum allowed size is 55%) | 可回收物 | Recycling |
| error | 65 | p64_s20 | Shorten the translation to at most 7 characters so it fits the original box (the current translation of 9 characters overflows its box; the minimum allowed size is 55%) | 可回收物 | Recycling |
| error | 66 | p65_s1 | Shorten the translation to at most 8 characters so it fits the original box (the current translation of 10 characters overflows its box; the minimum allowed size is 55%) | 前后 | Front/Back |
| error | 66 | p65_s1 | Shorten the translation to at most 8 characters so it fits the original box (the current translation of 10 characters overflows its box; the minimum allowed size is 55%) | 前后 | Front/Back |
| error | 68 | p67_s0 | Shorten the translation to at most 6 characters so it fits the original box (the current translation of 7 characters overflows its box; the minimum allowed size is 55%) | 上下 | Up/Down |
| error | 68 | p67_s0 | Shorten the translation to at most 6 characters so it fits the original box (the current translation of 7 characters overflows its box; the minimum allowed size is 55%) | 上下 | Up/Down |
| error | 70 | p69_s0 | Shorten the translation to at most 8 characters so it fits the original box (the current translation of 10 characters overflows its box; the minimum allowed size is 55%) | 左右 | Left/Right |
| error | 70 | p69_s0 | Shorten the translation to at most 8 characters so it fits the original box (the current translation of 10 characters overflows its box; the minimum allowed size is 55%) | 左右 | Left/Right |
| error | 70 | p69_s11 | Shorten the translation to at most 5 characters so it fits the original box (the current translation of 7 characters overflows its box; the minimum allowed size is 55%) | 在 | Next to |
| error | 70 | p69_s11 | Shorten the translation to at most 5 characters so it fits the original box (the current translation of 7 characters overflows its box; the minimum allowed size is 55%) | 在 | Next to |
| error | 71 | p70_s4 | Shorten the translation to at most 6 characters so it fits the original box (the current translation of 8 characters overflows its box; the minimum allowed size is 55%) | 练习本 | workbook |
| error | 71 | p70_s4 | Shorten the translation to at most 6 characters so it fits the original box (the current translation of 8 characters overflows its box; the minimum allowed size is 55%) | 练习本 | workbook |
| error | 72 | p71_s2 | Shorten the translation to at most 40 characters so it fits the original box (the current translation of 56 characters overflows its box; the minimum allowed size is 55%) | 自284.2.0葬自信自强自立 | self284.2.0confidence, self-reliance, self-improvement |
| error | 72 | p71_s2 | Shorten the translation to at most 40 characters so it fits the original box (the current translation of 56 characters overflows its box; the minimum allowed size is 55%) | 自284.2.0葬自信自强自立 | self284.2.0confidence, self-reliance, self-improvement |
| error | 73 | p72_s11 | Shorten the translation to at most 10 characters so it fits the original box (the current translation of 13 characters overflows its box; the minimum allowed size is 55%) | 火车站 | Train station |
| error | 73 | p72_s11 | Shorten the translation to at most 10 characters so it fits the original box (the current translation of 13 characters overflows its box; the minimum allowed size is 55%) | 火车站 | Train station |
| error | 74 | p73_s1 | Shorten the translation to at most 15 characters so it fits the original box (the current translation of 18 characters overflows its box; the minimum allowed size is 55%) | 认识图形 | Recognizing Shapes |
| error | 74 | p73_s1 | Shorten the translation to at most 15 characters so it fits the original box (the current translation of 18 characters overflows its box; the minimum allowed size is 55%) | 认识图形 | Recognizing Shapes |
| error | 76 | p75_s9 | Shorten the translation to at most 11 characters so it fits the original box (the current translation of 13 characters overflows its box; the minimum allowed size is 55%) | 对了！ | That's right! |
| error | 76 | p75_s9 | Shorten the translation to at most 11 characters so it fits the original box (the current translation of 13 characters overflows its box; the minimum allowed size is 55%) | 对了！ | That's right! |
| error | 78 | p77_s1 | Shorten the translation to at most 13 characters so it fits the original box (the current translation of 16 characters overflows its box; the minimum allowed size is 55%) | 古人计数 | Ancient Counting |
| error | 78 | p77_s1 | Shorten the translation to at most 13 characters so it fits the original box (the current translation of 16 characters overflows its box; the minimum allowed size is 55%) | 古人计数 | Ancient Counting |
| error | 82 | p81_s2 | Shorten the translation to at most 8 characters so it fits the original box (the current translation of 10 characters overflows its box; the minimum allowed size is 55%) | 12支 | 12 markers |
| error | 82 | p81_s2 | Shorten the translation to at most 8 characters so it fits the original box (the current translation of 10 characters overflows its box; the minimum allowed size is 55%) | 12支 | 12 markers |
| error | 84 | p83_s26 | Shorten the translation to at most 17 characters so it fits the original box (the current translation of 20 characters overflows its box; the minimum allowed size is 55%) | 只，地上有 | birds, on the ground |
| error | 84 | p83_s26 | Shorten the translation to at most 17 characters so it fits the original box (the current translation of 20 characters overflows its box; the minimum allowed size is 55%) | 只，地上有 | birds, on the ground |
| error | 97 | p96_s14 | Shorten the translation to at most 7 characters so it fits the original box (the current translation of 9 characters overflows its box; the minimum allowed size is 55%) | 3时 | 3 o'clock |
| error | 97 | p96_s14 | Shorten the translation to at most 7 characters so it fits the original box (the current translation of 9 characters overflows its box; the minimum allowed size is 55%) | 3时 | 3 o'clock |
| error | 97 | p96_s15 | Shorten the translation to at most 10 characters so it fits the original box (the current translation of 12 characters overflows its box; the minimum allowed size is 55%) | 11时半 | half past 11 |
| error | 97 | p96_s15 | Shorten the translation to at most 10 characters so it fits the original box (the current translation of 12 characters overflows its box; the minimum allowed size is 55%) | 11时半 | half past 11 |
| error | 99 | p98_s9 | Shorten the translation to at most 5 characters so it fits the original box (the current translation of 8 characters overflows its box; the minimum allowed size is 55%) | 饼干 | Biscuits |
| error | 99 | p98_s9 | Shorten the translation to at most 5 characters so it fits the original box (the current translation of 8 characters overflows its box; the minimum allowed size is 55%) | 饼干 | Biscuits |
| error | 103 | p102_s8 | Shorten the translation to at most 22 characters so it fits the original box (the current translation of 26 characters overflows its box; the minimum allowed size is 55%) | 17.最重的画 | 17. Mark the heaviest with |
| error | 103 | p102_s8 | Shorten the translation to at most 22 characters so it fits the original box (the current translation of 26 characters overflows its box; the minimum allowed size is 55%) | 17.最重的画 | 17. Mark the heaviest with |
| error | 104 | p103_s11 | Shorten the translation to at most 5 characters so it fits the original box (the current translation of 8 characters overflows its box; the minimum allowed size is 55%) | 个 | in line. |
| error | 104 | p103_s11 | Shorten the translation to at most 5 characters so it fits the original box (the current translation of 8 characters overflows its box; the minimum allowed size is 55%) | 个 | in line. |
| error | 104 | p103_s17 | Shorten the translation to at most 6 characters so it fits the original box (the current translation of 7 characters overflows its box; the minimum allowed size is 55%) | 在 | Next to |
| error | 104 | p103_s17 | Shorten the translation to at most 6 characters so it fits the original box (the current translation of 7 characters overflows its box; the minimum allowed size is 55%) | 在 | Next to |
| error | 104 | p103_s19 | Shorten the translation to at most 6 characters so it fits the original box (the current translation of 7 characters overflows its box; the minimum allowed size is 55%) | 在 | Next to |
| error | 104 | p103_s19 | Shorten the translation to at most 6 characters so it fits the original box (the current translation of 7 characters overflows its box; the minimum allowed size is 55%) | 在 | Next to |
| error | 104 | p103_s20 | Shorten the translation to at most 6 characters so it fits the original box (the current translation of 7 characters overflows its box; the minimum allowed size is 55%) | 在 | Next to |
| error | 104 | p103_s20 | Shorten the translation to at most 6 characters so it fits the original box (the current translation of 7 characters overflows its box; the minimum allowed size is 55%) | 在 | Next to |
| error | 104 | p103_s5 | Shorten the translation to at most 6 characters so it fits the original box (the current translation of 8 characters overflows its box; the minimum allowed size is 55%) | 有 | has ____ |
| error | 104 | p103_s5 | Shorten the translation to at most 6 characters so it fits the original box (the current translation of 8 characters overflows its box; the minimum allowed size is 55%) | 有 | has ____ |
| error | 104 | p103_s6 | Shorten the translation to at most 5 characters so it fits the original box (the current translation of 8 characters overflows its box; the minimum allowed size is 55%) | 个 | in line. |
| error | 104 | p103_s6 | Shorten the translation to at most 5 characters so it fits the original box (the current translation of 8 characters overflows its box; the minimum allowed size is 55%) | 个 | in line. |
| warning | 37 | p36_s10 | The translation overflows its box and was rendered at 42% of the original size; even a much shorter text would not fit, check this box in the preview | 三 | Unit 3 |
| warning | 37 | p36_s10 | The translation overflows its box and was rendered at 42% of the original size; even a much shorter text would not fit, check this box in the preview | 三 | Unit 3 |
| warning | 42 | p41_s8 | The translation overflows its box and was rendered at 34% of the original size; even a much shorter text would not fit, check this box in the preview | 穿 | wearing |
| warning | 42 | p41_s8 | The translation overflows its box and was rendered at 34% of the original size; even a much shorter text would not fit, check this box in the preview | 穿 | wearing |
| warning | 56 | p55_s8 | The translation overflows its box and was rendered at 38% of the original size; even a much shorter text would not fit, check this box in the preview | 画 | Draw |
| warning | 56 | p55_s8 | The translation overflows its box and was rendered at 38% of the original size; even a much shorter text would not fit, check this box in the preview | 画 | Draw |
| warning | 59 | p58_s6 | The translation overflows its box and was rendered at 42% of the original size; even a much shorter text would not fit, check this box in the preview | 有 | has ____ |
| warning | 59 | p58_s6 | The translation overflows its box and was rendered at 42% of the original size; even a much shorter text would not fit, check this box in the preview | 有 | has ____ |
| warning | 63 | p62_s1 | The translation overflows its box and was rendered at 33% of the original size; even a much shorter text would not fit, check this box in the preview | 语 | Chinese |
| warning | 63 | p62_s1 | The translation overflows its box and was rendered at 33% of the original size; even a much shorter text would not fit, check this box in the preview | 语 | Chinese |
| warning | 63 | p62_s10 | The translation overflows its box and was rendered at 24% of the original size; even a much shorter text would not fit, check this box in the preview | 练 | Exercise |
| warning | 63 | p62_s10 | The translation overflows its box and was rendered at 24% of the original size; even a much shorter text would not fit, check this box in the preview | 练 | Exercise |
| warning | 63 | p62_s11 | The translation overflows its box and was rendered at 30% of the original size; even a much shorter text would not fit, check this box in the preview | 文 | Chinese |
| warning | 63 | p62_s11 | The translation overflows its box and was rendered at 30% of the original size; even a much shorter text would not fit, check this box in the preview | 文 | Chinese |
| warning | 63 | p62_s15 | The translation overflows its box and was rendered at 48% of the original size; even a much shorter text would not fit, check this box in the preview | 语文 | Chinese |
| warning | 63 | p62_s15 | The translation overflows its box and was rendered at 48% of the original size; even a much shorter text would not fit, check this box in the preview | 语文 | Chinese |
| warning | 63 | p62_s2 | The translation overflows its box and was rendered at 52% of the original size; even a much shorter text would not fit, check this box in the preview | 数学 | maths |
| warning | 63 | p62_s2 | The translation overflows its box and was rendered at 52% of the original size; even a much shorter text would not fit, check this box in the preview | 数学 | maths |
| warning | 63 | p62_s6 | The translation overflows its box and was rendered at 28% of the original size; even a much shorter text would not fit, check this box in the preview | 语 | Chinese |
| warning | 63 | p62_s6 | The translation overflows its box and was rendered at 28% of the original size; even a much shorter text would not fit, check this box in the preview | 语 | Chinese |
| warning | 63 | p62_s9 | The translation overflows its box and was rendered at 29% of the original size; even a much shorter text would not fit, check this box in the preview | 语 | Chinese |
| warning | 63 | p62_s9 | The translation overflows its box and was rendered at 29% of the original size; even a much shorter text would not fit, check this box in the preview | 语 | Chinese |
| warning | 65 | p64_s18 | The translation overflows its box and was rendered at 40% of the original size; even a much shorter text would not fit, check this box in the preview | 蔬菜 | Vegetables |
| warning | 65 | p64_s18 | The translation overflows its box and was rendered at 40% of the original size; even a much shorter text would not fit, check this box in the preview | 蔬菜 | Vegetables |
| warning | 67 | p66_s16 | The translation overflows its box and was rendered at 29% of the original size; even a much shorter text would not fit, check this box in the preview | 火车站路广场 | Railway Station, Road, Square |
| warning | 67 | p66_s16 | The translation overflows its box and was rendered at 29% of the original size; even a much shorter text would not fit, check this box in the preview | 火车站路广场 | Railway Station, Road, Square |
| warning | 68 | p67_s13 | The translation overflows its box and was rendered at 40% of the original size; even a much shorter text would not fit, check this box in the preview | 在 | Next to |
| warning | 68 | p67_s13 | The translation overflows its box and was rendered at 40% of the original size; even a much shorter text would not fit, check this box in the preview | 在 | Next to |
| warning | 68 | p67_s4 | The translation overflows its box and was rendered at 40% of the original size; even a much shorter text would not fit, check this box in the preview | 在 | Next to |
| warning | 68 | p67_s4 | The translation overflows its box and was rendered at 40% of the original size; even a much shorter text would not fit, check this box in the preview | 在 | Next to |
| warning | 68 | p67_s7 | The translation overflows its box and was rendered at 40% of the original size; even a much shorter text would not fit, check this box in the preview | 在 | Next to |
| warning | 68 | p67_s7 | The translation overflows its box and was rendered at 40% of the original size; even a much shorter text would not fit, check this box in the preview | 在 | Next to |
| warning | 68 | p67_s9 | The translation overflows its box and was rendered at 48% of the original size; even a much shorter text would not fit, check this box in the preview | 面 | bottom |
| warning | 68 | p67_s9 | The translation overflows its box and was rendered at 48% of the original size; even a much shorter text would not fit, check this box in the preview | 面 | bottom |
| warning | 69 | p68_s3 | The translation overflows its box and was rendered at 48% of the original size; even a much shorter text would not fit, check this box in the preview | 面 | side |
| warning | 69 | p68_s3 | The translation overflows its box and was rendered at 48% of the original size; even a much shorter text would not fit, check this box in the preview | 面 | side |
| warning | 69 | p68_s4 | The translation overflows its box and was rendered at 19% of the original size; even a much shorter text would not fit, check this box in the preview | 在 | Next to |
| warning | 69 | p68_s4 | The translation overflows its box and was rendered at 19% of the original size; even a much shorter text would not fit, check this box in the preview | 在 | Next to |
| warning | 69 | p68_s8 | The translation overflows its box and was rendered at 49% of the original size; even a much shorter text would not fit, check this box in the preview | 面 | side |
| warning | 69 | p68_s8 | The translation overflows its box and was rendered at 49% of the original size; even a much shorter text would not fit, check this box in the preview | 面 | side |
| warning | 72 | p71_s0 | The translation overflows its box and was rendered at 42% of the original size; even a much shorter text would not fit, check this box in the preview | 教室 | Classroom |
| warning | 72 | p71_s0 | The translation overflows its box and was rendered at 42% of the original size; even a much shorter text would not fit, check this box in the preview | 教室 | Classroom |
| warning | 72 | p71_s13 | The translation overflows its box and was rendered at 42% of the original size; even a much shorter text would not fit, check this box in the preview | 小强 | Xiaoqiang |
| warning | 72 | p71_s13 | The translation overflows its box and was rendered at 42% of the original size; even a much shorter text would not fit, check this box in the preview | 小强 | Xiaoqiang |
| warning | 74 | p73_s12 | The translation overflows its box and was rendered at 52% of the original size; even a much shorter text would not fit, check this box in the preview | 茶 | Tea |
| warning | 74 | p73_s12 | The translation overflows its box and was rendered at 52% of the original size; even a much shorter text would not fit, check this box in the preview | 茶 | Tea |
| warning | 74 | p73_s13 | The translation overflows its box and was rendered at 33% of the original size; even a much shorter text would not fit, check this box in the preview | 球 | sphere |
| warning | 74 | p73_s13 | The translation overflows its box and was rendered at 33% of the original size; even a much shorter text would not fit, check this box in the preview | 球 | sphere |
| warning | 74 | p73_s2 | The translation overflows its box and was rendered at 33% of the original size; even a much shorter text would not fit, check this box in the preview | 牙膏 | Toothpaste |
| warning | 74 | p73_s2 | The translation overflows its box and was rendered at 33% of the original size; even a much shorter text would not fit, check this box in the preview | 牙膏 | Toothpaste |
| warning | 74 | p73_s4 | The translation overflows its box and was rendered at 47% of the original size; even a much shorter text would not fit, check this box in the preview | 茶 | Tea |
| warning | 74 | p73_s4 | The translation overflows its box and was rendered at 47% of the original size; even a much shorter text would not fit, check this box in the preview | 茶 | Tea |
| warning | 88 | p87_s42 | The translation overflows its box and was rendered at 40% of the original size; even a much shorter text would not fit, check this box in the preview | 十+ | 10 + |
| warning | 88 | p87_s42 | The translation overflows its box and was rendered at 40% of the original size; even a much shorter text would not fit, check this box in the preview | 十+ | 10 + |
| warning | 93 | p92_s2 | The translation overflows its box and was rendered at 45% of the original size; even a much shorter text would not fit, check this box in the preview | 有 | has ____ |
| warning | 93 | p92_s2 | The translation overflows its box and was rendered at 45% of the original size; even a much shorter text would not fit, check this box in the preview | 有 | has ____ |
| warning | 93 | p92_s5 | The translation overflows its box and was rendered at 45% of the original size; even a much shorter text would not fit, check this box in the preview | 有 | has ____ |
| warning | 93 | p92_s5 | The translation overflows its box and was rendered at 45% of the original size; even a much shorter text would not fit, check this box in the preview | 有 | has ____ |
| warning | 97 | p96_s4 | The translation overflows its box and was rendered at 41% of the original size; even a much shorter text would not fit, check this box in the preview | 农 | Farm |
| warning | 97 | p96_s4 | The translation overflows its box and was rendered at 41% of the original size; even a much shorter text would not fit, check this box in the preview | 农 | Farm |
| warning | 97 | p96_s6 | The translation overflows its box and was rendered at 29% of the original size; even a much shorter text would not fit, check this box in the preview | 小 | Primary |
| warning | 97 | p96_s6 | The translation overflows its box and was rendered at 29% of the original size; even a much shorter text would not fit, check this box in the preview | 小 | Primary |
| warning | 97 | p96_s7 | The translation overflows its box and was rendered at 53% of the original size; even a much shorter text would not fit, check this box in the preview | 学 | pils |
| warning | 97 | p96_s7 | The translation overflows its box and was rendered at 53% of the original size; even a much shorter text would not fit, check this box in the preview | 学 | pils |
| warning | 104 | p103_s10 | The translation overflows its box and was rendered at 43% of the original size; even a much shorter text would not fit, check this box in the preview | 有 | has ____ |
| warning | 104 | p103_s10 | The translation overflows its box and was rendered at 43% of the original size; even a much shorter text would not fit, check this box in the preview | 有 | has ____ |
| warning | 104 | p103_s7 | The translation overflows its box and was rendered at 43% of the original size; even a much shorter text would not fit, check this box in the preview | 有 | has ____ |
| warning | 104 | p103_s7 | The translation overflows its box and was rendered at 43% of the original size; even a much shorter text would not fit, check this box in the preview | 有 | has ____ |

### `llm_review` — 32 errors, 56 warnings

| Severity | Page | Segment | Message | Source | Translation |
|---|---|---|---|---|---|
| error | 1 | p0_s5 | Reviewer (meaning): The source reads "及上册", which is incomplete/garbled; "and Volume 1" drops the character 及 and adds "and". The source should be rendered faithfully, e.g. "Volume 1 (First Semester)" / simply "Volume 1". Suggested translation: "Volume 1" | 及上册 | and Volume 1 |
| error | 1 | p0_s7 | Reviewer (number): The source "米2" is a unit label (m²); the translation "m2" uses a digit instead of the superscript/number formatting and could be read as "m2" (metres two). Use the unit with superscript: m². Suggested translation: "m²" | 米2 | m2 |
| error | 4 | p3_s2 | Reviewer (meaning): The source "新国" appears to be a garbled/abbreviated label; it should not be translated as "New Term" (新学期) since that changes the meaning and invents content. Suggested translation: "New Term" | 新国 | New Term |
| error | 6 | p5_s1 | Reviewer (meaning): The source "迎新同" is garbled; the translation "Welcome," drops the 同 and splits the phrase oddly. The heading should read as a welcome to new students, keeping the source content. Suggested translation: "Welcome," | 迎新同 | Welcome, |
| error | 13 | p12_s7 | Reviewer (untranslated): The source 'mmmmlmm mmka' appears to be garbled or placeholder text and is left as is; acceptable if represents an image. | mmmmlmm mmka | mmmmlmm mmka |
| error | 19 | p18_s2 | Reviewer (meaning): The placeholder ⟦0⟧ is used twice for two different objects; source reads '每 ⟦0⟧ 和 ⟦0⟧'. Suggested translation: "each ⟦0⟧ and ⟦0⟧" | 每，和 | each ⟦0⟧, and ⟦0⟧ |
| error | 28 | p27_s0 | Reviewer (omission): The heading ends with an isolated Chinese character 一 (part of the unit title pattern) that is dropped in the translation; the heading should read 'Unit 3 Addition and Subtraction (1)', not 'Unit 3 Addition and Subtraction (1)' — the '一' after 加减 belongs to the title. Suggested translation: "Unit 3 Addition and Subtraction (1) 108.1.0 108.1.1" | 三加与减（一108.1.0）108.1.1 | Unit 3 Addition and Subtraction (1) 108.1.0108.1.1 |
| error | 28 | p27_s7 | Reviewer (omission): The measure word 只 is not rendered; the counted objects (pandas) should be named: 'There are 3 pandas eating bamboo'. Suggested translation: "There are 3 pandas eating bamboo" | 有3只在吃竹子 | There are 3 eating bamboo |
| error | 34 | p33_s5 | Reviewer (omission): The measure word 条 is translated as 'fish.' with a period, but the source label 条。 is a fragment to complete a sentence (…还剩 __ 条). The period inside the fragment is fine; however the object 'fish' is supplied from context (小猫吃鱼) which is acceptable. No issue. | 条。 | fish. |
| error | 34 | p33_s7 | Reviewer (terminology): 拨一拨 refers to moving beads on a counting frame; 'Move and fill in' is acceptable, but 'Move the beads and fill in' would be clearer in context. Minor. | 拨一拨，填一填 | Move and fill in |
| error | 37 | p36_s12 | Reviewer (meaning): The source '5-5日' contains the character 日 (day) which is dropped in the translation. Suggested translation: "5-5日" | 5-5日 | 5-5 |
| error | 37 | p36_s6 | Reviewer (meaning): The source '目5-2日' contains a Chinese character 日 (day) and 目 (eye/marker) around the number; the translation drops these characters, changing the label. Suggested translation: "目5-2日" | 目5-2日 | 5-2 |
| error | 41 | p40_s3 | Reviewer (omission): The source '，可以怎么分？' asks 'how can you divide them?'; the translation says 'share them' and drops the object 只 (the animals), changing the meaning. Suggested translation: ", how can you divide them?" | ，可以怎么分？ | . How can you share them? |
| error | 44 | p43_s5 | Reviewer (untranslated): Source text "填巾" appears garbled; translation "Fill in" omits the second character. If source is a garbled "填一填", the glossary term is "Fill in". Suggested translation: "Fill in" | 填巾 | Fill in |
| error | 46 | p45_s6 | Reviewer (omission): The counted noun is dropped after the numeral; the context counts chicks. Suggested translation: "There are 7 chicks in total" | 一共有7只 | There are 7 in total |
| error | 48 | p47_s18 | Reviewer (untranslated): Garbled source fragment "188.29.0" plus "中" is translated as "into." losing the meaning "into the ...". Suggested translation: "into 188.29.0." | 188.29.0中。 | 188.29.0 into. |
| error | 48 | p47_s5 | Reviewer (omission): "8级" refers to 8 remaining steps/levels; translation says "8 steps left" which is acceptable but the number refers to steps remaining — fine. No problem. | 加油，还有8级！ | Come on, 8 steps left! |
| error | 61 | p60_s13 | Reviewer (untranslated): The name 妙想 is abbreviated as 'Miaox.'; names are written in full pinyin and must not be abbreviated. Suggested translation: "Miaoxiang" | 妙想 | Miaox. |
| error | 62 | p61_s7 | Reviewer (meaning): 文具 means 'stationery' (school supplies overall), not 'Pens', which narrows the category wrongly. Suggested translation: "Stationery" | 文具 | Pens |
| error | 63 | p62_s17 | Reviewer (untranslated): 语文 is abbreviated as 'Chi.'; it should be written in full as 'Chinese'. Suggested translation: "Chinese" | 语文 | Chi. |
| error | 68 | p67_s12 | Reviewer (meaning): 面 as "top" is a mistranslation of the combined location word (上面 = above/on top). | 面 | top |
| error | 68 | p67_s6 | Reviewer (meaning): 面 alone is part of the location phrase (上面 = above/on top, 下面 = below/under) and cannot stand alone as "top". Rendering it as a bare noun misleads the student about the intended sentence. | 面 | top |
| error | 68 | p67_s9 | Reviewer (meaning): 面 rendered alone as "bottom" does not convey the location phrase 下面 (below/under) and results in a wrong sentence meaning. | 面 | bottom |
| error | 71 | p70_s6 | Reviewer (untranslated): 载学 is an OCR-garbled 数学 ('mathematics') left untranslated; render it as 'mathematics'. Suggested translation: "mathematics" | 载学 | 载学 |
| error | 72 | p71_s11 | Reviewer (untranslated): The name '小红' is left untranslated; it should be written in pinyin as 'Xiaohong'. Suggested translation: "Xiaohong" | 小红 | 小红 |
| error | 72 | p71_s2 | Reviewer (untranslated): The source fragment is garbled ('自284.2.0葬自信自强自立'); the translation drops the leading 'self' duplication but partially keeps garbled content. It should read as the full phrase 'confidence, self-reliance, self-improvement' without the stray fragment. Suggested translation: "confidence, self-reliance, self-improvement" | 自284.2.0葬自信自强自立 | self284.2.0confidence, self-reliance, self-improvement |
| error | 73 | p72_s16 | Reviewer (untranslated): The source fragment 'ns.' is a stray abbreviation left untranslated and does not constitute meaningful text; it should be removed or rendered as a full word if it stands for 'minutes'/'items'. | ns. | ns. |
| error | 78 | p77_s3 | Reviewer (meaning): "比10多1，是" means "1 more than 10 is", but the translation inserts an extra "1" ("is 1") and changes the meaning. Suggested translation: "1 more than 10 is" | 比10多1，是 | 1 more than 10 is 1, it is |
| error | 84 | p83_s8 | Reviewer (meaning): The amount is split incorrectly: source is 8 yuan plus 9, i.e. ¥8 + 9 (or 8元+9), not ¥8+9. Suggested translation: "¥8 + 9" | 8+9元 | ¥8+9 |
| error | 96 | p95_s0 | Reviewer (number): Source '八' is the unit number (Unit 8); translation keeps 'Unit 8' correct, but the placeholder content '380.1.0' is preserved. No change needed. However '认识钟表' is 'Telling Time'. OK. | 八 380.1.0认识钟表 | Unit 8 380.1.0 Telling Time |
| error | 101 | p100_s25 | Reviewer (untranslated): Row of characters/glyph-like string left as-is; if this is a counting/tally or symbol string it should be preserved, but as-is it appears untranslated. | C cccecccccccececcececccccc | C cccecccccccececcececccccc |
| error | 104 | p103_s14 | Reviewer (meaning): "有()个有(）个，有个有个" means "There are ( ) ___ , there are ( ) ___, ..." — the measure words (counted nouns) and blanks are lost; translation omits the nouns after the blanks. Suggested translation: "There are ( ) ___, there are ( ) ___, there are ( ) ___, there are ( ) ___" | 有()个有(）个，有个有个 | There are () There are (), There are () There are () |
| warning | 10 | p9_s3 | Reviewer (grammar): The source uses 人 and translation uses people, though consistent with appearance, this item is fine; no change needed. | 有几个人？ | How many people are there? |
| warning | 17 | p16_s7 | Reviewer (grammar): Missing final punctuation; source has no period either, but sentence should end with a period for textbook style; also 'colour' vs 'color' consistency is style only. Suggested translation: "6. Look at the number and colour." | 6.看数涂一涂 | 6. Look at the number and colour |
| warning | 31 | p30_s12 | Reviewer (grammar): Inconsistent with p27_s13 ('Read:'); the standard formula-reading prompt is 'Read as:'. Minor consistency issue. | 读作：5减2等于3。 | Read as: 5 minus 2 equals 3. |
| warning | 31 | p30_s13 | Reviewer (format): 画一画 is glossed 'Draw' in the glossary; 'Draw and calculate' is correct. No issue. | 画一画，算一算。 | Draw and calculate. |
| warning | 33 | p32_s1 | Reviewer (grammar): Duplicate of p29_s1 pattern; fine. No issue. | 4.说一说。 | 4. Talk about it. |
| warning | 34 | p33_s3 | Reviewer (wording): 'On the plate there are' is fine as a sentence fragment. No issue. | 盘子里有 | On the plate there are |
| warning | 42 | p41_s12 | Reviewer (grammar): The source ends with a full stop '。'; the translation keeps it, which is fine, but the wording 'Talk about it.' is acceptable. Suggested translation: "Talk about it." | 说一说。 | Talk about it. |
| warning | 44 | p43_s0 | Reviewer (grammar): "Make 9" is awkward; the exercise is about making pairs that sum to 9. Suggested translation: "3. Make 9." | 3.凑成9。 | 3. Make 9. |
| warning | 46 | p45_s3 | Reviewer (grammar): "Talk about it" is a bare verb phrase; an object is preferable. Suggested translation: "2. Talk about it" | 2.说一说 | 2. Talk about it |
| warning | 47 | p46_s0 | Reviewer (grammar): "Chicks Eating Food" is an unnatural title; a noun phrase reads better. Suggested translation: "Chicks Eating" | 小鸡吃食 | Chicks Eating Food |
| warning | 47 | p46_s4 | Reviewer (grammar): Missing sentence-final punctuation after the instruction. Suggested translation: "Move the beads and fill in." | 拨一拨，填一填 | Move the beads and fill in |
| warning | 51 | p50_s4 | Reviewer (grammar): Missing sentence-final punctuation. Suggested translation: "The rest are hiding here." | 剩下的人藏在这里 | The rest are hiding here |
| warning | 51 | p50_s6 | Reviewer (grammar): Missing sentence-final punctuation. Suggested translation: "Pose a math question and try to solve it." | 提出一个数学问题，并尝试解答 | Pose a math question and try to solve it |
| warning | 53 | p52_s3 | Reviewer (grammar): "in all" is acceptable, but the more natural textbook wording is "altogether". Suggested translation: "There are 6 people altogether." | 一共有6人。 | There are 6 people in all. |
| warning | 54 | p53_s52 | Reviewer (grammar): The wording is unnatural for a textbook; a more idiomatic phrasing is preferable. Suggested translation: "Look at it vertically, horizontally, and diagonally: what pattern do you find?" | 坚着看，横着看，斜着看，你发现了什么规律？ | Look vertically, horizontally and diagonally: what pattern … |
| warning | 55 | p54_s1 | Reviewer (grammar): "start with 6 minus something" is awkward for a subtraction exercise; "6 minus a number" is more standard. Suggested translation: "These number sentences are all 6 minus a number." | 这几个算式都是6减几的 | These number sentences all start with 6 minus something |
| warning | 55 | p54_s17 | Reviewer (grammar): "6 minus something" is informal; "6 minus a number" is preferable. Suggested translation: "Find the number sentences that are 6 minus a number and arrange them." | 找出6减几的算式，排一排 | Find the number sentences that start with 6 minus something… |
| warning | 55 | p54_s50 | Reviewer (grammar): The wording is unnatural; a more idiomatic phrasing is preferable. Suggested translation: "Look at it vertically, horizontally, and diagonally: what pattern do you find?" | 竖着看，横着看，斜着看，你发现了什么规律？ | Look vertically, horizontally and diagonally: what pattern … |
| warning | 60 | p59_s10 | Reviewer (grammar): 'respectively into' is awkward; 'Fill 2, 3, 4 and 5 into' reads naturally. Suggested translation: "Fill 2, 3, 4 and 5 into" | 在每个式子里每个数只能用一次。 | Each number can be used only once in each number sentence. |
| warning | 62 | p61_s9 | Reviewer (grammar): 'how you tidied it' changes the present-tense prompt; 'how you tidy it' matches the source tense. Suggested translation: "Tidy your schoolbag and talk about how you tidy it." | 整理自己的书包，说一说你是怎么整理的。 | Tidy your schoolbag and talk about how you tidied it. |
| warning | 68 | p67_s11 | Reviewer (grammar): The 's fragment is not natural English for the sentence frame. | 的 | 's |
| warning | 68 | p67_s14 | Reviewer (grammar): 's is an incomplete possessive fragment; in this counting-book context the label 的 after an object means 'of' or belongs to a noun phrase. Consider 'of'. Suggested translation: "of" | 的 | 's |
| warning | 68 | p67_s16 | Reviewer (grammar): A question with 'Guess who it is' should end with a period or be rephrased; word order is not natural for a question. Suggested translation: "Guess who it is." | 猜一猜，它是谁？ | Guess who it is? |
| warning | 68 | p67_s5 | Reviewer (grammar): The possessive 's fragment is awkward; the frame requires a phrase like "the ... of" or placing the object before the location word. | 的 | 's |
| warning | 68 | p67_s8 | Reviewer (grammar): Possessive 's fragment is unnatural in the sentence frame. | 的 | 's |
| warning | 69 | p68_s18 | Reviewer (format): The source ends with a single '·' (an incomplete sentence), which the translation keeps as '·' with a space; keep it attached as in the source. Suggested translation: "I know the treasure is in·" | 我知道了宝物在· | I know the treasure is in · |
| warning | 69 | p68_s2 | Reviewer (format): The placeholders ⟦272.2.0⟧ and ⟦272.8.0⟧ are preserved, but the source has a dash label 的——面 and the translation drops the second dash/blank and the closing label, leaving '—' unbalanced. Suggested translation: "⟦272.2.0⟧ is on the — side; ⟦272.8.0⟧ is on the —" | 在馨272.2.0的——面馨在272.8.0一的— | 272.2.0 is on the — side, 272.8.0 is on the — |
| warning | 69 | p68_s7 | Reviewer (grammar): 'is on ⟦272.11.0⟧'s' is an unnatural fragment; the source is a vertical label meaning 'to the ___ of ⟦272.11.0⟧'. Suggested translation: "is on ⟦272.11.0⟧'s" | 在272.11.0的 | is on 272.11.0's |
| warning | 70 | p69_s3 | Reviewer (grammar): 'I say, you do.' is telegraphic. A natural textbook rendering is 'I say it, you do it.' Suggested translation: "I say it, you do it." | 我说你做。 | I say, you do. |
| warning | 72 | p71_s0 | Reviewer (format): The source heading '教室' is a unit heading that begins with a bare Chinese numeral '六' (in the merged fragment '六认识图形'); per convention it should be rendered as a unit heading with 'Unit 6'. | 教室 | Classroom |
| warning | 73 | p72_s13 | Reviewer (format): Inconsistent capitalization: 'Store' is lowercase while parallel place labels are capitalized; it should be 'Store' or 'Shop' consistently with 'Cinema', 'Stadium', etc. Suggested translation: "Store" | 商店 | Store |
| warning | 74 | p73_s0 | Reviewer (format): Unit heading '六认识图形' should follow the unit-heading convention: 'Unit 6 Recognizing Shapes' (the placeholder should remain attached correctly). Suggested translation: "Unit 6 Recognizing Shapes" | 六292.0.0认识图形 | Unit 6 Recognizing Shapes292.0.0 |
| warning | 79 | p78_s11 | Reviewer (format): Per the convention, single-character column labels of a place-value chart use the standard abbreviations TTh Th H T O; "十位个位" should be "T O", not "Tens Ones". Suggested translation: "T O" | 十位个位 | Tens Ones |
| warning | 79 | p78_s13 | Reviewer (format): Place-value column labels should use the standard abbreviations "T O". Suggested translation: "T O" | 十位个位 | Tens Ones |
| warning | 79 | p78_s14 | Reviewer (format): Place-value column labels should use the standard abbreviations "T O". Suggested translation: "T O" | 十位个位 | Tens Ones |
| warning | 79 | p78_s15 | Reviewer (format): Place-value column labels should use the standard abbreviations "T O". Suggested translation: "T O" | 十位个位 | Tens Ones |
| warning | 79 | p78_s16 | Reviewer (format): Place-value column label should use the standard abbreviation "T". Suggested translation: "T" | 十位 | Tens |
| warning | 79 | p78_s17 | Reviewer (format): Place-value column label should use the standard abbreviation "O". Suggested translation: "O" | 个位 | Ones |
| warning | 81 | p80_s17 | Reviewer (format): Place-value column labels should use the standard abbreviations "T O". Suggested translation: "T O" | 十位个位 | Tens Ones |
| warning | 81 | p80_s7 | Reviewer (format): Place-value column labels should use the standard abbreviations "T O". Suggested translation: "T O" | 十位个位 | Tens Ones |
| warning | 83 | p82_s11 | Reviewer (format): Place-value column labels should use the standard abbreviations "T O". Suggested translation: "T O" | 十位个位 | Tens Ones |
| warning | 83 | p82_s12 | Reviewer (format): Place-value column labels should use the standard abbreviations "T O". Suggested translation: "T O" | 十位个位 | Tens Ones |
| warning | 83 | p82_s13 | Reviewer (format): Place-value column labels should use the standard abbreviations "T O". Suggested translation: "T O" | 十位个位 | Tens Ones |
| warning | 85 | p84_s0 | Reviewer (format): Heading punctuation: the source is a question; ending with a question mark is preferable for a heading question. Suggested translation: "How many trees?" | 有几棵树 | How many trees |
| warning | 86 | p85_s1 | Reviewer (grammar): "Arrange" is not idiomatic for 摆一摆 in a primary maths exercise; children move objects/pictures around. Suggested translation: "1. Move the objects and calculate." | 1.摆一摆，算一算。 | 1. Arrange and calculate. |
| warning | 92 | p91_s1 | Reviewer (grammar): "Taoqi's School" misrepresents 校园 (campus); the title refers to the campus. Suggested translation: "Taoqi's Campus" | 淘气的校园 | Taoqi's School |
| warning | 93 | p92_s8 | Reviewer (format): Source uses spaced dots '····' as ellipsis; translation uses four dots '....'. Minor punctuation style. Suggested translation: "Our class has 20 boys..." | 我们班有20名男生···· | Our class has 20 boys.... |
| warning | 95 | p94_s12 | Reviewer (format): Source ellipsis '..··' rendered as '...'; acceptable but punctuation style differs. Suggested translation: "It's 10..." | 是10..·· | It's 10... |
| warning | 97 | p96_s16 | Reviewer (grammar): Inconsistent clock style: 'half past 5' avoids a colon, while other times in the same set use '12:00'/'8:00'. For a textbook, write the time with digits consistently. Suggested translation: "5:30" | 5时半 | half past 5 |
| warning | 97 | p96_s4 | Reviewer (format): Single characters 农 and 场 are likely part of a split word '农场' (farm); 'Farm' and '____' split is acceptable. 小 and 学 split as 'Primary'/'School' is odd; should be 'Primary School'. | 农 | Farm |
| warning | 97 | p96_s5 | Reviewer (format): '场' rendered as a blank; if it is an answer blank, keeping '____' is correct. Fine. | 场 | ____ |
| warning | 97 | p96_s6 | Reviewer (format): Split characters '小'/'学' render as 'Primary'/'School', which wrongly reads as two separate labels. Suggested translation: "Primary" | 小 | Primary |
| warning | 100 | p99_s0 | Reviewer (format): Heading is lowercased; a section heading should be capitalised. Suggested translation: "Exercise" | 练习 | exercise |
| warning | 102 | p101_s0 | Reviewer (grammar): "Colour" spelling inconsistent with "color"; also missing period is acceptable in a label. Suggested translation: "10. Color and fill in" | 10.涂一涂，填一填 | 10. Colour and fill in |
| warning | 104 | p103_s21 | Reviewer (format): "的（" is an incomplete fragment "of (" split across items; acceptable as fragment but punctuation spacing inconsistent. Suggested translation: "of (" | 的（ | of ( |
| warning | 104 | p103_s23 | Reviewer (format): Incomplete fragment "of (" — consistent with source fragment; no change needed. Suggested translation: "of (" | 的（ | of ( |

### `placeholders` — 2 errors, 0 warnings

| Severity | Page | Segment | Message | Source | Translation |
|---|---|---|---|---|---|
| error | 19 | p18_s2 | Placeholder problem: unknown placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position | 每，和 | each ⟦0⟧, and ⟦0⟧ |
| error | 19 | p18_s2 | Placeholder problem: duplicated placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position | 每，和 | each ⟦0⟧, and ⟦0⟧ |

### `untranslated` — 2 errors, 0 warnings

| Severity | Page | Segment | Message | Source | Translation |
|---|---|---|---|---|---|
| error | 71 | p70_s6 | 2 letter(s) of the source script remain untranslated ("载学"); translate all text into English | 载学 | 载学 |
| error | 72 | p71_s11 | 2 letter(s) of the source script remain untranslated ("小红"); translate all text into English | 小红 | 小红 |

### `image_text` — 0 errors, 22 warnings

| Severity | Page | Segment | Message | Source | Translation |
|---|---|---|---|---|---|
| warning | 13 | p12_i48_5 | The text '用\ue00048.5.0\ue0010表示。' was left in the source language (inline pictograms the OCR cannot read (left in the picture)): the line is built around symbols or pictures the OCR could not read - check the page in the preview | 用48.5.00表示。 |  |
| warning | 13 | p12_i48_5 | The text '用\ue00048.5.0\ue0010表示。' was left in the source language (inline pictograms the OCR cannot read (left in the picture)): the line is built around symbols or pictures the OCR could not read - check the page in the preview | 用48.5.00表示。 |  |
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
| warning | 80 | p79_i316_35 | The text '子上打3个结来表示。' was left in the source language (inline pictograms the OCR cannot read (left in the picture)): the line is built around symbols or pictures the OCR could not read - check the page in the preview | 子上打3个结来表示。 |  |
| warning | 80 | p79_i316_35 | The text '子上打3个结来表示。' was left in the source language (inline pictograms the OCR cannot read (left in the picture)): the line is built around symbols or pictures the OCR could not read - check the page in the preview | 子上打3个结来表示。 |  |
| warning | 98 | p97_i388_10 | The text '个方法表示' was left in the source language (inline pictograms the OCR cannot read (left in the picture)): the line is built around symbols or pictures the OCR could not read - check the page in the preview | 个方法表示 |  |
| warning | 98 | p97_i388_10 | The text '个方法表示' was left in the source language (inline pictograms the OCR cannot read (left in the picture)): the line is built around symbols or pictures the OCR could not read - check the page in the preview | 个方法表示 |  |
| warning | 99 | p98_i392_5 | The text '比' was left in the source language (inline pictograms the OCR cannot read (left in the picture)): the line is built around symbols or pictures the OCR could not read - check the page in the preview | 比 |  |
| warning | 99 | p98_i392_5 | The text '比' was left in the source language (inline pictograms the OCR cannot read (left in the picture)): the line is built around symbols or pictures the OCR could not read - check the page in the preview | 比 |  |

### `length_ratio` — 0 errors, 1 warning

| Severity | Page | Segment | Message | Source | Translation |
|---|---|---|---|---|---|
| warning | 25 | p24_s10 | The translation looks too short: 5 characters for 13 translatable source characters (ratio 0.38, about 2.60 expected); check that nothing was omitted | 号→□96.16.0号→□96.16.1号→□96.16.2号 | → 96.16.0 → 96.16.1 → 96.16.2 |
