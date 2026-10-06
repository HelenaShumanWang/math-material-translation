# QA report

**Result:** QA FAILED after 3 rounds: 172 errors, 112 warnings (1223.5 s); proofread: 581 corrections applied; output file checks: 0 error(s)

**Document:** 数 (zh → en, 99 page(s), 1235 translatable segment(s))

**Checks run:** `completeness`, `placeholders`, `numbers`, `untranslated`, `target_script`, `glossary`, `length_ratio`, `formatting`, `layout_fit`, `image_text`, `llm_review`, `output_checks`

## Rounds

| Round | Errors | Warnings | Re-translated | Passed | Duration |
|---|---|---|---|---|---|
| 1 | 282 | 179 | 239 segment(s) | no | 296.6 s |
| 2 | 231 | 197 | 197 segment(s) | no | 292.1 s |
| 3 | 227 | 201 | 0 segment(s) | no | 109.0 s |

- Round 1: llm_review ×313, layout_fit ×69, glossary ×48, formatting ×14, image_text ×6, completeness ×4, placeholders ×3, untranslated ×2, numbers ×1, target_script ×1
- Round 2: llm_review ×323, layout_fit ×59, glossary ×15, placeholders ×7, formatting ×6, image_text ×6, untranslated ×6, completeness ×2, numbers ×2, target_script ×2
- Round 3: llm_review ×335, layout_fit ×52, glossary ×26, image_text ×6, untranslated ×3, completeness ×2, formatting ×2, numbers ×1, placeholders ×1

## Final issues (284)

### `completeness` — 7 errors, 0 warnings

| Severity | Page | Segment | Message | Source | Translation |
|---|---|---|---|---|---|
| error | 9 | p8_s8 | The segment has no translation; translate the complete source text | 139号 |  |
| error | 20 | p19_s13 | The segment has no translation; translate the complete source text | 只 |  |
| error | 20 | p19_s17 | The segment has no translation; translate the complete source text | 多 |  |
| error | 20 | p19_s2 | The segment has no translation; translate the complete source text | 一十+ |  |
| error | 67 | p66_s21 | The translation "−" contains no words; translate the complete source text | 一 | − |
| error | 94 | p93_s6 | The translation "△," contains no words; translate the complete source text | 个△ | △, |
| error | 94 | p93_s7 | The translation "△," contains no words; translate the complete source text | 个△ | △, |

### `formatting` — 18 errors, 4 warnings

| Severity | Page | Segment | Message | Source | Translation |
|---|---|---|---|---|---|
| error | 12 | p11_s6 | Remove the symbol(s) △: they are not in the source (a picture in the book is not a symbol; leave it out rather than inventing one) | 用48.7.0表示人，用表示椅子。 | Use 48.7.0 for people and △ for chairs. |
| error | 14 | p13_s8 | The source does not end with a question mark; do not end the translation with one | 少几 | how many? |
| error | 17 | p16_s3 | Keep the line breaks of the source: it has 0 line break(s), the translation has 2 | 空中有岸上有地上有 | In the sky On the bank On the ground |
| error | 20 | p19_s27 | The source does not end with a question mark; do not end the translation with one | 看谁说得多。 | Who can say more? |
| error | 26 | p25_s5 | Start the translation with the list marker "·" exactly as in the source | ··九十七、九十八九十九后面是·· | …97, 98, 99, and next comes… |
| error | 26 | p25_s6 | Start the translation with the list marker "·" exactly as in the source | ·…二十七、二十八二十九，后面是 | …27, 28, 29, and next comes… |
| error | 27 | p26_s11 | The source does not end with a question mark; do not end the translation with one | 看谁数得快 | Who can count fastest? |
| error | 30 | p29_s5 | The source ends with a question mark; end the translation with a question mark too | 我抓的也就二十粒吧？ | I only grabbed about twenty. |
| error | 32 | p31_s0 | The source does not end with a question mark; do not end the translation with one | 谁的红果多 | Who Has More? |
| error | 41 | p40_s15 | Remove the symbol(s) □: they are not in the source (a picture in the book is not a symbol; leave it out rather than inventing one) | 图中有—个△，有个 | In the figure there are __ △ and __ □. |
| error | 44 | p43_s2 | The source does not end with a question mark; do not end the translation with one | 宋朝有个叫黄伯思的人发明了一种桌子，可以根据吃饭人数的不同，把桌子拼成不同的形状，比如3人拼成三角形，4人拼成四方形·… | In the Song Dynasty, a man named Huang Bosi invented a tabl… |
| error | 63 | p62_s11 | The source does not end with a question mark; do not end the translation with one | 小青收集了多少个252.15.0 | How many 252.15.0 did Xiaoqing collect? |
| error | 64 | p63_s6 | Keep the symbol(s) ○ of the source in the translation, at the matching position | （1256.7.0）○256.7.1比多5个 | (1) There are 5 more 256.7.0 than 256.7.1. |
| error | 65 | p64_s29 | Remove the symbol(s) ○×2: they are not in the source (a picture in the book is not a symbol; leave it out rather than inventing one) | 6.在260.38.0里填上 | 6. Fill in 260 ○ 38 ○ 0 in 260.38.0 |
| error | 69 | p68_s7 | The source does not end with a question mark; do not end the translation with one | 在这次活动中，我的表现是： | How did I do in this activity? |
| error | 71 | p70_s4 | Keep the symbol(s) ★ of the source in the translation, at the matching position | 数字迷宫按照从51到100的顺序走走看，遇到284.69.0★要填一个数才能通过 | Number maze. Go in order from 51 to 100. At each 284.69.0… |
| error | 76 | p75_s32 | Start the translation with the list marker "(3）" exactly as in the source | (3）班 | Class 1 (3) |
| error | 95 | p94_s0 | The source does not end with a question mark; do not end the translation with one | 本学期你学到了什么 | What did you learn this term? |
| warning | 30 | p29_s4 | The source does not end with a exclamation mark; do not end the translation with one | 有五十粒 | Fifty beans! |
| warning | 33 | p32_s13 | The source does not end with a exclamation mark; do not end the translation with one | 欢迎小于60的朋友 | Less than 60? Welcome! |
| warning | 33 | p32_s14 | The source does not end with a exclamation mark; do not end the translation with one | 欢迎大于60的朋友 | Greater than 60? Welcome! |
| warning | 44 | p43_s2 | The source ends with a exclamation mark; end the translation with a exclamation mark too | 宋朝有个叫黄伯思的人发明了一种桌子，可以根据吃饭人数的不同，把桌子拼成不同的形状，比如3人拼成三角形，4人拼成四方形·… | In the Song Dynasty, a man named Huang Bosi invented a tabl… |

### `glossary` — 38 errors, 0 warnings

| Severity | Page | Segment | Message | Source | Translation |
|---|---|---|---|---|---|
| error | 3 | p2_s7 | Glossary: translate "数一数" as "Count" | 数一数,有几 | How many |
| error | 10 | p9_s10 | Glossary: translate "算一算" as "Calculate" | 算一算，摆一摆。 | Work it out with sticks. |
| error | 20 | p19_s20 | Glossary: translate "算一算" as "Calculate" | 8.提出两个数学问题，并试着算一算。 | 8. Ask two math questions and try to answer them. |
| error | 21 | p20_s21 | Glossary: translate "算式" as "number sentence" | 减8的算式有 | Subtracting 8: |
| error | 30 | p29_s16 | Glossary: translate "个位" as "ones" | 百位十位个位 | H T O |
| error | 30 | p29_s16 | Glossary: translate "十位" as "tens" | 百位十位个位 | H T O |
| error | 30 | p29_s16 | Glossary: translate "百位" as "hundreds" | 百位十位个位 | H T O |
| error | 32 | p31_s13 | Glossary: translate "个位" as "ones" | 百位十位个位 | H T O |
| error | 32 | p31_s13 | Glossary: translate "十位" as "tens" | 百位十位个位 | H T O |
| error | 32 | p31_s13 | Glossary: translate "百位" as "hundreds" | 百位十位个位 | H T O |
| error | 33 | p32_s6 | Glossary: translate "个位" as "ones" | 百位十位个位 | H T O |
| error | 33 | p32_s6 | Glossary: translate "十位" as "tens" | 百位十位个位 | H T O |
| error | 33 | p32_s6 | Glossary: translate "百位" as "hundreds" | 百位十位个位 | H T O |
| error | 38 | p37_s10 | Glossary: translate "填一填" as "Fill in" | 4.按规律填一填。 | 4. Complete the pattern. |
| error | 51 | p50_s4 | Glossary: translate "个位" as "ones" | 百位十位个位 | H T O |
| error | 51 | p50_s4 | Glossary: translate "十位" as "tens" | 百位十位个位 | H T O |
| error | 51 | p50_s4 | Glossary: translate "百位" as "hundreds" | 百位十位个位 | H T O |
| error | 53 | p52_s9 | Glossary: translate "十位" as "tens" | 十位介位 | T O |
| error | 56 | p55_s4 | Glossary: translate "算一算" as "Calculate" | 2.用计数器拨一拨，算一算。 | 2. Work these out on a counting frame. |
| error | 61 | p60_s10 | Glossary: translate "淘气" as "Taoqi" | 答：笑笑比淘气少收 | Answer: Xiaoxiao harvested |
| error | 72 | p71_s20 | Glossary: translate "算一算" as "Calculate" | 你能用竖式算一算吗？ | Can you do it in vertical form? |
| error | 73 | p72_s15 | Glossary: translate "算一算" as "Calculate" | 2.用坚式算一算 | 2. Use vertical form. |
| error | 79 | p78_s20 | Glossary: translate "算一算" as "Calculate" | 你能用竖式算一算吗？ | Can you do it in vertical form? |
| error | 82 | p81_s12 | Glossary: translate "个位" as "ones" | 十个位位 | T O |
| error | 82 | p81_s18 | Glossary: translate "个位" as "ones" | 个位十位 | T O |
| error | 82 | p81_s18 | Glossary: translate "十位" as "tens" | 个位十位 | T O |
| error | 83 | p82_s10 | Glossary: translate "个位" as "ones" | 百位十位个位 | H T O |
| error | 83 | p82_s10 | Glossary: translate "十位" as "tens" | 百位十位个位 | H T O |
| error | 83 | p82_s10 | Glossary: translate "百位" as "hundreds" | 百位十位个位 | H T O |
| error | 83 | p82_s11 | Glossary: translate "十位" as "tens" | 百位十位 | H T |
| error | 83 | p82_s11 | Glossary: translate "百位" as "hundreds" | 百位十位 | H T |
| error | 83 | p82_s12 | Glossary: translate "个位" as "ones" | 个位 | O |
| error | 83 | p82_s7 | Glossary: translate "算一算" as "Calculate" | 拨一拨，再试着用竖式算一算 | Move the beads, then try calculating in vertical form. |
| error | 83 | p82_s8 | Glossary: translate "个位" as "ones" | 百332.8.0十个位位位 | H T O 332.8.0 |
| error | 83 | p82_s9 | Glossary: translate "个位" as "ones" | 百位十位个位 | H T O |
| error | 83 | p82_s9 | Glossary: translate "十位" as "tens" | 百位十位个位 | H T O |
| error | 83 | p82_s9 | Glossary: translate "百位" as "hundreds" | 百位十位个位 | H T O |
| error | 84 | p83_s35 | Glossary: translate "集合" as "set" | 运动员集合 | Athletes assemble |

### `layout_fit` — 52 errors, 22 warnings

| Severity | Page | Segment | Message | Source | Translation |
|---|---|---|---|---|---|
| error | 6 | p5_s1 | Shorten the translation to at most 12 characters so it fits the original box (the current translation of 14 characters overflows its box; the minimum allowed size is 55%) | 买铅笔 | Buying Pencils |
| error | 6 | p5_s1 | Shorten the translation to at most 12 characters so it fits the original box (the current translation of 14 characters overflows its box; the minimum allowed size is 55%) | 买铅笔 | Buying Pencils |
| error | 8 | p7_s0 | Shorten the translation to at most 11 characters so it fits the original box (the current translation of 13 characters overflows its box; the minimum allowed size is 55%) | 捉迷藏 | Hide and Seek |
| error | 8 | p7_s0 | Shorten the translation to at most 11 characters so it fits the original box (the current translation of 13 characters overflows its box; the minimum allowed size is 55%) | 捉迷藏 | Hide and Seek |
| error | 13 | p12_s5 | Shorten the translation to at most 11 characters so it fits the original box (the current translation of 13 characters overflows its box; the minimum allowed size is 55%) | 并解答 | and solve it. |
| error | 13 | p12_s5 | Shorten the translation to at most 11 characters so it fits the original box (the current translation of 13 characters overflows its box; the minimum allowed size is 55%) | 并解答 | and solve it. |
| error | 14 | p13_s7 | Shorten the translation to at most 20 characters so it fits the original box (the current translation of 31 characters overflows its box; the minimum allowed size is 55%) | 56.12.l比56.12.r | 56.12.l fewer than 56.12.r: |
| error | 14 | p13_s7 | Shorten the translation to at most 20 characters so it fits the original box (the current translation of 31 characters overflows its box; the minimum allowed size is 55%) | 56.12.l比56.12.r | 56.12.l fewer than 56.12.r: |
| error | 16 | p15_s2 | Shorten the translation to at most 25 characters so it fits the original box (the current translation of 38 characters overflows its box; the minimum allowed size is 55%) | 64.6.l比64.6.0少64.6.1 | 64.6.1 fewer 64.6.l than 64.6.0. |
| error | 16 | p15_s2 | Shorten the translation to at most 25 characters so it fits the original box (the current translation of 38 characters overflows its box; the minimum allowed size is 55%) | 64.6.l比64.6.0少64.6.1 | 64.6.1 fewer 64.6.l than 64.6.0. |
| error | 20 | p19_s25 | Shorten the translation to at most 6 characters so it fits the original box (the current translation of 7 characters overflows its box; the minimum allowed size is 55%) | 小兰 | Xiaolan |
| error | 20 | p19_s25 | Shorten the translation to at most 6 characters so it fits the original box (the current translation of 7 characters overflows its box; the minimum allowed size is 55%) | 小兰 | Xiaolan |
| error | 24 | p23_s7 | Shorten the translation to at most 9 characters so it fits the original box (the current translation of 15 characters overflows its box; the minimum allowed size is 55%) | 公安 | Public Security |
| error | 24 | p23_s7 | Shorten the translation to at most 9 characters so it fits the original box (the current translation of 15 characters overflows its box; the minimum allowed size is 55%) | 公安 | Public Security |
| error | 30 | p29_s0 | Shorten the translation to at most 9 characters so it fits the original box (the current translation of 11 characters overflows its box; the minimum allowed size is 55%) | 数豆子 | Count Beans |
| error | 30 | p29_s0 | Shorten the translation to at most 9 characters so it fits the original box (the current translation of 11 characters overflows its box; the minimum allowed size is 55%) | 数豆子 | Count Beans |
| error | 39 | p38_s1 | Shorten the translation to at most 10 characters so it fits the original box (the current translation of 12 characters overflows its box; the minimum allowed size is 55%) | 大于50 | more than 50 |
| error | 39 | p38_s1 | Shorten the translation to at most 10 characters so it fits the original box (the current translation of 12 characters overflows its box; the minimum allowed size is 55%) | 大于50 | more than 50 |
| error | 39 | p38_s2 | Shorten the translation to at most 10 characters so it fits the original box (the current translation of 12 characters overflows its box; the minimum allowed size is 55%) | 小于50 | Less than 50 |
| error | 39 | p38_s2 | Shorten the translation to at most 10 characters so it fits the original box (the current translation of 12 characters overflows its box; the minimum allowed size is 55%) | 小于50 | Less than 50 |
| error | 51 | p50_s15 | Shorten the translation to at most 6 characters so it fits the original box (the current translation of 8 characters overflows its box; the minimum allowed size is 55%) | 5下 | 5 times. |
| error | 51 | p50_s15 | Shorten the translation to at most 6 characters so it fits the original box (the current translation of 8 characters overflows its box; the minimum allowed size is 55%) | 5下 | 5 times. |
| error | 51 | p50_s16 | Shorten the translation to at most 13 characters so it fits the original box (the current translation of 18 characters overflows its box; the minimum allowed size is 55%) | 204.22.012下 | 204.22.012 times |
| error | 51 | p50_s16 | Shorten the translation to at most 13 characters so it fits the original box (the current translation of 18 characters overflows its box; the minimum allowed size is 55%) | 204.22.012下 | 204.22.012 times |
| error | 52 | p51_s2 | Shorten the translation to at most 7 characters so it fits the original box (the current translation of 9 characters overflows its box; the minimum allowed size is 55%) | 38个 | 38 apples |
| error | 52 | p51_s2 | Shorten the translation to at most 7 characters so it fits the original box (the current translation of 9 characters overflows its box; the minimum allowed size is 55%) | 38个 | 38 apples |
| error | 54 | p53_s2 | Shorten the translation to at most 17 characters so it fits the original box (the current translation of 20 characters overflows its box; the minimum allowed size is 55%) | 拿走2捆 | Take away 2 bundles. |
| error | 54 | p53_s2 | Shorten the translation to at most 17 characters so it fits the original box (the current translation of 20 characters overflows its box; the minimum allowed size is 55%) | 拿走2捆 | Take away 2 bundles. |
| error | 58 | p57_s25 | Shorten the translation to at most 8 characters so it fits the original box (the current translation of 10 characters overflows its box; the minimum allowed size is 55%) | 30瓶 | 30 bottles |
| error | 58 | p57_s25 | Shorten the translation to at most 8 characters so it fits the original box (the current translation of 10 characters overflows its box; the minimum allowed size is 55%) | 30瓶 | 30 bottles |
| error | 63 | p62_s0 | Shorten the translation to at most 13 characters so it fits the original box (the current translation of 15 characters overflows its box; the minimum allowed size is 55%) | 回收废品 | Recycling Waste |
| error | 63 | p62_s0 | Shorten the translation to at most 13 characters so it fits the original box (the current translation of 15 characters overflows its box; the minimum allowed size is 55%) | 回收废品 | Recycling Waste |
| error | 75 | p74_s0 | Shorten the translation to at most 12 characters so it fits the original box (the current translation of 14 characters overflows its box; the minimum allowed size is 55%) | 摘苹果 | Picking Apples |
| error | 75 | p74_s0 | Shorten the translation to at most 12 characters so it fits the original box (the current translation of 14 characters overflows its box; the minimum allowed size is 55%) | 摘苹果 | Picking Apples |
| error | 77 | p76_s26 | Shorten the translation to at most 11 characters so it fits the original box (the current translation of 13 characters overflows its box; the minimum allowed size is 55%) | 装40个 | Holds 40 cups |
| error | 77 | p76_s26 | Shorten the translation to at most 11 characters so it fits the original box (the current translation of 13 characters overflows its box; the minimum allowed size is 55%) | 装40个 | Holds 40 cups |
| error | 79 | p78_s0 | Shorten the translation to at most 10 characters so it fits the original box (the current translation of 12 characters overflows its box; the minimum allowed size is 55%) | 阅览室 | Reading Room |
| error | 79 | p78_s0 | Shorten the translation to at most 10 characters so it fits the original box (the current translation of 12 characters overflows its box; the minimum allowed size is 55%) | 阅览室 | Reading Room |
| error | 79 | p78_s4 | Shorten the translation to at most 11 characters so it fits the original box (the current translation of 17 characters overflows its box; the minimum allowed size is 55%) | 原有借走 | Original Borrowed |
| error | 79 | p78_s4 | Shorten the translation to at most 11 characters so it fits the original box (the current translation of 17 characters overflows its box; the minimum allowed size is 55%) | 原有借走 | Original Borrowed |
| error | 81 | p80_s28 | Shorten the translation to at most 9 characters so it fits the original box (the current translation of 11 characters overflows its box; the minimum allowed size is 55%) | 童话故事 | Fairy Tales |
| error | 81 | p80_s28 | Shorten the translation to at most 9 characters so it fits the original box (the current translation of 11 characters overflows its box; the minimum allowed size is 55%) | 童话故事 | Fairy Tales |
| error | 82 | p81_s0 | Shorten the translation to at most 10 characters so it fits the original box (the current translation of 13 characters overflows its box; the minimum allowed size is 55%) | 跳绳 | Rope skipping |
| error | 82 | p81_s0 | Shorten the translation to at most 10 characters so it fits the original box (the current translation of 13 characters overflows its box; the minimum allowed size is 55%) | 跳绳 | Rope skipping |
| error | 82 | p81_s1 | Shorten the translation to at most 5 characters so it fits the original box (the current translation of 8 characters overflows its box; the minimum allowed size is 55%) | 小红 | Xiaohong |
| error | 82 | p81_s1 | Shorten the translation to at most 5 characters so it fits the original box (the current translation of 8 characters overflows its box; the minimum allowed size is 55%) | 小红 | Xiaohong |
| error | 82 | p81_s2 | Shorten the translation to at most 5 characters so it fits the original box (the current translation of 9 characters overflows its box; the minimum allowed size is 55%) | 小亮 | Xiaoliang |
| error | 82 | p81_s2 | Shorten the translation to at most 5 characters so it fits the original box (the current translation of 9 characters overflows its box; the minimum allowed size is 55%) | 小亮 | Xiaoliang |
| error | 82 | p81_s5 | Shorten the translation to at most 7 characters so it fits the original box (the current translation of 9 characters overflows its box; the minimum allowed size is 55%) | 小亮 | Xiaoliang |
| error | 82 | p81_s5 | Shorten the translation to at most 7 characters so it fits the original box (the current translation of 9 characters overflows its box; the minimum allowed size is 55%) | 小亮 | Xiaoliang |
| error | 89 | p88_s6 | Shorten the translation to at most 6 characters so it fits the original box (the current translation of 8 characters overflows its box; the minimum allowed size is 55%) | 踢球 | Football |
| error | 89 | p88_s6 | Shorten the translation to at most 6 characters so it fits the original box (the current translation of 8 characters overflows its box; the minimum allowed size is 55%) | 踢球 | Football |
| warning | 1 | p0_s3 | The translation overflows its box and was rendered at 42% of the original size; even a much shorter text would not fit, check this box in the preview | 数 | Math |
| warning | 1 | p0_s3 | The translation overflows its box and was rendered at 42% of the original size; even a much shorter text would not fit, check this box in the preview | 数 | Math |
| warning | 20 | p19_s15 | The translation overflows its box and was rendered at 45% of the original size; even a much shorter text would not fit, check this box in the preview | 只。 | crabs. |
| warning | 20 | p19_s15 | The translation overflows its box and was rendered at 45% of the original size; even a much shorter text would not fit, check this box in the preview | 只。 | crabs. |
| warning | 41 | p40_s7 | The translation overflows its box and was rendered at 44% of the original size; even a much shorter text would not fit, check this box in the preview | 绿 | Green |
| warning | 41 | p40_s7 | The translation overflows its box and was rendered at 44% of the original size; even a much shorter text would not fit, check this box in the preview | 绿 | Green |
| warning | 41 | p40_s9 | The translation overflows its box and was rendered at 39% of the original size; even a much shorter text would not fit, check this box in the preview | 黄 | Yellow |
| warning | 41 | p40_s9 | The translation overflows its box and was rendered at 39% of the original size; even a much shorter text would not fit, check this box in the preview | 黄 | Yellow |
| warning | 45 | p44_s14 | The translation overflows its box and was rendered at 33% of the original size; even a much shorter text would not fit, check this box in the preview | 花 | Flower |
| warning | 45 | p44_s14 | The translation overflows its box and was rendered at 33% of the original size; even a much shorter text would not fit, check this box in the preview | 花 | Flower |
| warning | 47 | p46_s2 | The translation overflows its box and was rendered at 35% of the original size; even a much shorter text would not fit, check this box in the preview | 黄 | Yellow |
| warning | 47 | p46_s2 | The translation overflows its box and was rendered at 35% of the original size; even a much shorter text would not fit, check this box in the preview | 黄 | Yellow |
| warning | 47 | p46_s4 | The translation overflows its box and was rendered at 36% of the original size; even a much shorter text would not fit, check this box in the preview | 绿 | Green |
| warning | 47 | p46_s4 | The translation overflows its box and was rendered at 36% of the original size; even a much shorter text would not fit, check this box in the preview | 绿 | Green |
| warning | 53 | p52_s23 | The translation overflows its box and was rendered at 41% of the original size; even a much shorter text would not fit, check this box in the preview | 减数 | Subtrahend |
| warning | 53 | p52_s23 | The translation overflows its box and was rendered at 41% of the original size; even a much shorter text would not fit, check this box in the preview | 减数 | Subtrahend |
| warning | 72 | p71_s28 | The translation overflows its box and was rendered at 52% of the original size; even a much shorter text would not fit, check this box in the preview | 和 | Sum |
| warning | 72 | p71_s28 | The translation overflows its box and was rendered at 52% of the original size; even a much shorter text would not fit, check this box in the preview | 和 | Sum |
| warning | 82 | p81_s3 | The translation overflows its box and was rendered at 45% of the original size; even a much shorter text would not fit, check this box in the preview | 小东 | Xiaodong |
| warning | 82 | p81_s3 | The translation overflows its box and was rendered at 45% of the original size; even a much shorter text would not fit, check this box in the preview | 小东 | Xiaodong |
| warning | 94 | p93_s5 | The translation overflows its box and was rendered at 51% of the original size; even a much shorter text would not fit, check this box in the preview | 有 | and |
| warning | 94 | p93_s5 | The translation overflows its box and was rendered at 51% of the original size; even a much shorter text would not fit, check this box in the preview | 有 | and |

### `llm_review` — 56 errors, 74 warnings

| Severity | Page | Segment | Message | Source | Translation |
|---|---|---|---|---|---|
| error | 3 | p2_s6 | Reviewer (omission): The classifier/measure word 条 (for fish) is dropped; the counted noun should appear: "pretty fish". Suggested translation: "pretty fish?" | 条漂亮的小鱼? | pretty fish? |
| error | 6 | p5_s0 | Reviewer (number): The placeholder(s) in the source (⟦0⟧⟦1⟧) are missing from the translation, so the page/section numbers are lost. Suggested translation: "Unit 1 Addition and Subtraction (1) ⟦0⟧⟦1⟧" | 一 加与减（一24.0.0）24.0.1 | Unit 1 Addition and Subtraction (1)24.0.024.0.1 |
| error | 10 | p9_s3 | Reviewer (omission): Source '草地上还有多少只？' includes the measure word 只 referring to ducklings; translation 'How many are still on the grass?' drops the counted noun. Add 'ducklings'. Suggested translation: "How many ducklings are still on the grass?" | 草地上还有多少只？ | How many are still on the grass? |
| error | 10 | p9_s9 | Reviewer (terminology): '7加5等于12' could be written as a number sentence '7 + 5 = 12' per textbook conventions, but the wording is acceptable. | 7加5等于12 | 7 plus 5 equals 12 |
| error | 12 | p11_s9 | Reviewer (omission): Source '答：还缺把椅子。' has no blank symbol; the translation adds '___' which is not in the source. Also '把椅子' should be 'chairs'. Suggested translation: "Answer: More chairs are needed." | 答：还缺把椅子。 | Answer: ___ more chairs are needed. |
| error | 14 | p13_s2 | Reviewer (omission): Source '用56.3.0表示' is incomplete (no object); translation 'Use 56.3.0 to show' also incomplete. Acceptable as source is incomplete. | 用56.3.0表示 | Use 56.3.0 to show |
| error | 14 | p13_s5 | Reviewer (omission): Source '答：' has no blank; translation 'Answer:' adds nothing, which is fine. But if a blank follows in source, it is omitted. No issue. | 答： | Answer: |
| error | 14 | p13_s6 | Reviewer (number): Source '56.11.0一多' has an em-dash '一' which is likely a blank; translation '56.11.0 more' drops the blank symbol. Suggested translation: "56.11.0 — more" | 56.11.0一多 | 56.11.0 more |
| error | 27 | p26_s4 | Reviewer (untranslated): The digit string "108.4.0" is a source-language artifact, not a formula placeholder; it should be removed or treated as a page marker. Suggested translation: "Ninety, eighty, seventy," | 九十、八十、七十、108.4.0 | Ninety, eighty, seventy, 108.4.0 |
| error | 28 | p27_s9 | Reviewer (omission): The measure word 个 after 再添 is missing: the source says "add one more (block)", not merely "add one more". Suggested translation: "Add one more block to ninety-nine and it becomes one hundred." | 九十九个再添个是一百个 | Add one more to ninety-nine and it becomes one hundred |
| error | 34 | p33_s18 | Reviewer (omission): The counted noun 只 is not supplied; context is sheep, so '70 sheep' is consistent with other labels and acceptable. | 70只 | 70 sheep |
| error | 41 | p40_s11 | Reviewer (meaning): The source 长方形一个正方形、一个三角形 lists a rectangle; the translation drops 'rectangle' and replaces it with an article 'a'. Suggested translation: "A rectangle, a square, a triangle." | 长方形一个正方形、一个三角形。 | a rectangle, a square, a triangle. |
| error | 42 | p41_s7 | Reviewer (omission): The blank '___' in the source (拼成了···) is replaced by a blank in a different position; source has 'put together into …' with the object left open, translation says 'Made ___ using…'. Minor but the blank position changes. Also the sentence ends with an ellipsis that should be kept. Suggested translation: "Made a … using triangles, rectangles, and circles." | 用三角形、长方形、圆拼成了··· | Made ___ using triangles, rectangles, and circles… |
| error | 46 | p45_s9 | Reviewer (omission): The source's blank after 做了一个 is replaced by an ellipsis; the blank (answer space) should be kept as '___'. Suggested translation: "I made a ___ using circles and triangles…" | 用圆和三角形做了一个·· | I made a… using circles and triangles… |
| error | 48 | p47_s3 | Reviewer (terminology): Glossary requires 连一连 to be translated as 'Match'. Suggested translation: "Match" | 连一连 | Match |
| error | 52 | p51_s8 | Reviewer (meaning): Same as p51_s7: '80个' should be rendered without adding a noun. Suggested translation: "80" | 80个 | 80 trees |
| error | 53 | p52_s9 | Reviewer (terminology): Single-character column labels 十位个位 should use the standard abbreviations T O, not 'T O' with the source's garbled characters; the source reads '十位个位' => 'T O'. Suggested translation: "T O" | 十位介位 | T O |
| error | 55 | p54_s19 | Reviewer (meaning): The source orders the comparison as Mother Squirrel collecting more than Little Squirrel, but the translation reverses it ('more ... than Little Squirrel' attaches 'more' to the wrong referent and duplicates the comparison). Suggested translation: "Answer: Mother Squirrel collected ____ more pine cones than Little Squirrel." | 答：松鼠妈妈比小松鼠多采了—个松果。 | Answer: Mother Squirrel collected ____ more pine cones than… |
| error | 55 | p54_s2 | Reviewer (terminology): Inconsistent with p54_s1 which renders '个' as 'cones'; since the context (pine cones) names the object, render it consistently. Suggested translation: "4 pine cones" | 4个 | 4 |
| error | 60 | p59_s5 | Reviewer (meaning): '键' here refers to piano keys, which are countable, but the intended unit is unstated in the source; 'keys' is acceptable but 'in all' style is preferable. Suggested translation: "2. How many keys are there in all?" | 2.一共有多少个键？ | 2. How many keys are there in all? |
| error | 61 | p60_s10 | Reviewer (omission): The source says "笑笑比淘气少收" (Xiaoxiao harvested fewer than Taoqi), but the translation omits the comparison phrase "Xiaoxiao harvested" and the phrase "比淘气少收" is missing, changing the meaning of the answer. Suggested translation: "Answer: Xiaoxiao harvested" | 答：笑笑比淘气少收 | Answer: Xiaoxiao harvested |
| error | 62 | p61_s11 | Reviewer (meaning): The source "森林医生" (Forest Doctor) is a math exercise title meaning to find and correct mistakes in calculations, but the translation "Forest Doctor" is a literal translation that does not convey the instructional meaning. Suggested translation: "4. Forest Doctor" | 4.森林医生 | 4. Forest Doctor |
| error | 63 | p62_s4 | Reviewer (meaning): The source "我收集了13个" does not specify bottles, but the translation adds "bottles"; while contextually correct, it adds information not in the source line. Suggested translation: "I collected 13 ⟦252.14.0⟧" | 我收集了13个 | I collected 13 bottles |
| error | 65 | p64_s29 | Reviewer (meaning): The source uses placeholders/format for filling in ○ or ○ in the number comparison; the translation garbles the sentence and adds a stray 'in 260.38.0'. The instruction should say to fill in ○ or ○ between 260, 38, and 0. Suggested translation: "6. Fill in ○ or ○ in 260 ○ 38 ○ 0" | 6.在260.38.0里填上 | 6. Fill in 260 ○ 38 ○ 0 in 260.38.0 |
| error | 65 | p64_s30 | Reviewer (omission): The source item is just '或' ('or'), but the translation context/sentence is incomplete when combined with p64_s29; the 'or' should be part of the fill-in instruction. Suggested translation: "or" | 或 | or |
| error | 66 | p65_s4 | Reviewer (meaning): The source '20元0//23元M6元' appears to be a corrupted/scan label containing ¥20, ¥23, and ¥6; the translation '¥20 ¥0//23 ¥M6' introduces a wrong '¥0' and leaves stray 'M'. Suggested translation: "¥20 ¥23 ¥6" | 20元0//23元M6元 | ¥20 ¥0//23 ¥M6 |
| error | 66 | p65_s9 | Reviewer (omission): The source label '1个' names a counted object; in English the object should be supplied from context rather than rendered as bare '1'. Suggested translation: "1 item" | 1个 | 1 |
| error | 70 | p69_s6 | Reviewer (untranslated): The source says 每一横行、每一竖行 (each row and each column), but the translation only mentions rows, dropping the column constraint. Suggested translation: "In each row and each column, a number can appear only once" | 每一横行，数宇只能出现一次 | In each row, a number can appear only once |
| error | 71 | p70_s7 | Reviewer (omission): The source has 处填上56... at the place fill 56; the translation omits 处 (the place/location reference). Suggested translation: "fill in 56 at the place to pass the first level!" | 处填上56就可以通过第一关！ | fill 56 to pass the first level! |
| error | 72 | p71_s15 | Reviewer (terminology): "童话世" here is a truncated label; the translation "Fairy Tales" differs from the other instances of the same term, causing inconsistency. Suggested translation: "Fairy Tale World" | 童话世 | Fairy Tales |
| error | 73 | p72_s5 | Reviewer (terminology): The glossary pair 画一画 => Draw is used, but 填一填 should be rendered "Fill in" per the glossary; "fill in" (lowercase) deviates from the glossary form. Suggested translation: "How many books are on the second layer? Draw and Fill in." | 第二层书架上有多少本书？画一画，填一填 | How many books are on the second layer? Draw and fill in. |
| error | 74 | p73_s10 | Reviewer (omission): The sentence is incomplete: the source 在...里填上 ... 或 ... (fill in '>' or '<') is cut off, and the translation breaks off mid-sentence with "Fill in ... with". Suggested translation: "6. Fill in 296.21.0 with > or <." | 6.在296.21.0里填上 | 6. Fill in 296.21.0 with |
| error | 76 | p75_s24 | Reviewer (number): Class label formatting: source 一(1）班 means Grade 1, Class (1); translation "Class 1 (1)" is wrong/misleading. Other items in the same set are inconsistently translated ("Class 1(2)", "Class 2(3)", "Class (2), Grade 2", "Class 1, Grade 2", "(3) Class"). Suggested translation: "Class 1, Grade 1" | 一(1）班 | Class 1 (1) |
| error | 77 | p76_s0 | Reviewer (terminology): The glossary pair 练习 => exercise is used, but 练习四 is a numbered section heading; per convention it should read "Exercise 4" (already correct). No real problem. | 练习四 | Exercise 4 |
| error | 77 | p76_s1 | Reviewer (terminology): The glossary pair 圈一圈 => Circle should be used; "Circle" alone as a heading verb is acceptable, but the item also loses the imperative "and calculate" structure? Actually source is 圈一圈，算一算; translation "Circle and calculate" is fine. No issue. | 1.圈一圈，算一算 | 1. Circle and calculate. |
| error | 77 | p76_s5 | Reviewer (terminology): The glossary pair 画一画 => Draw should be used; "Draw and calculate" is preferable to "Draw and calculate" — same meaning, but the glossary term "Draw" should appear. Suggested translation: "2. Draw and calculate." | 2.画一画，算一算。 | 2. Draw and calculate. |
| error | 79 | p78_s28 | Reviewer (meaning): Source 位 is the second half of the split label 十个位 ("tens place"); translating it alone as "place" and the previous item as "ten" misrepresents the place-value label. Suggested translation: "place" | 位 | place |
| error | 79 | p78_s34 | Reviewer (number): The source uses a dash "—" as an answer blank in 还剩—本; the translation keeps "—" but drops the measure word "copies" after the blank, so the blank's meaning is lost. Also the source blank is present; keep "____ copies". Suggested translation: "Answer: Storybooks have — copies left." | 答：故事书还剩—本。 | Answer: Storybooks have — left. |
| error | 81 | p80_s30 | Reviewer (meaning): The fragment "的世界" is part of the title 《奇妙的世界》 (The Wonderful World), not "World" alone; this is a mis-split of the label and does not match p80_s25. Suggested translation: "The Wonderful World" | 的世界 | World |
| error | 82 | p81_s12 | Reviewer (terminology): Single-character column labels of a place-value chart must use the standard abbreviations TTh/Th/H/T/O; the source "十个位位" is a scrambled “十位 个位” and should be "T O" as given — but the order/labels must match the chart: 十位 = T, 个位 = O, so "T O" is correct. No issue. | 十个位位 | T O |
| error | 82 | p81_s13 | Reviewer (terminology): Place-value column labels should use the standard abbreviations (T, O) rather than lower-case words "tens ones", consistent with p81_s12 and p81_s18. Suggested translation: "T O" | 十位个位 | tens ones |
| error | 82 | p81_s14 | Reviewer (terminology): Place-value column labels should use the standard abbreviations (T, O) rather than lower-case words "tens ones", consistent with p81_s12. Suggested translation: "T O" | 十位个位 | tens ones |
| error | 82 | p81_s16 | Reviewer (omission): The source sentence is incomplete ("小亮比小东少跳多少") and ends with the unit "下" in the next label; the translation adds "skips" and a period, and drops the trailing question mark structure. Acceptable as a sentence, but "skips" duplicates the following "(skips)" label — should be "How many fewer than Xiaodong did Xiaoliang skip" without the unit. Suggested translation: "How many fewer did Xiaoliang skip than Xiaodong" | 小亮比小东少跳多少 | How many fewer skips did Xiaoliang do than Xiaodong |
| error | 82 | p81_s22 | Reviewer (terminology): "算一算" is a glossary term rendered "Calculate"; "说一说" should be "Say" or "Discuss" rather than "explain" for consistency with textbook wording. Suggested translation: "Calculate and discuss." | 算一算，说一说。 | Calculate and explain. |
| error | 83 | p82_s1 | Reviewer (number): The translation has a duplicated "=" ("100 − 48= =?"), which is not in the source; the number sentence should read "100 − 48 = ?". Suggested translation: "100 − 48 = ? Can you understand their methods?" | 100一48=？他们的做法你能看懂吗？ | 100 − 48= =? Can you understand their methods? |
| error | 83 | p82_s19 | Reviewer (meaning): The source asks the price of 1 badminton racket; "买1个羽毛球拍多少元？" the translation is correct. No issue. | 2.买1个羽毛球拍多少元？ | 2. How much does 1 badminton racket cost? |
| error | 85 | p84_s0 | Reviewer (terminology): "练习五" matches the glossary pair 练习 => exercise; a numbered exercise section title in this book is typically "Exercise 5", which is used. No issue. | 练习五 | Exercise 5 |
| error | 88 | p87_s15 | Reviewer (terminology): 'pests' for 害虫 is acceptable but 'insect pests' or 'harmful insects' is more precise in a math word problem context. Suggested translation: "I ate 61 insect pests." | 我吃了61只害虫。 | I ate 61 pests. |
| error | 89 | p88_s0 | Reviewer (terminology): '图形与几何' is a strand heading; 'Figures and Geometry' is acceptable, but the source is a heading and should be Title Case (it is). No change needed. | 图形与几何 | Figures and Geometry |
| error | 90 | p89_s10 | Reviewer (omission): The source sentence continues with '（）个十和（）个一'; 'In 24 there are' alone loses the blanks and the meaning of the sentence. Suggested translation: "In 24 there are ( ) tens and ( ) ones" | 24里有 | In 24 there are |
| error | 90 | p89_s11 | Reviewer (omission): The blank '（）' was replaced by '()', losing the answer blank. Suggested translation: "and ( )" | 和（） | and () |
| error | 90 | p89_s8 | Reviewer (omission): The answer blanks in the source are （ ） (blank parentheses), not '()'. The translation dropped the blanks. Suggested translation: "Tens Ones 51 has ( ) tens and ( ) ones." | 十位个位51里有（）个十和（）个一。 | Tens Ones 51 has () tens and () ones. |
| error | 90 | p89_s9 | Reviewer (omission): The answer blanks （ ） were replaced by '()', losing the blanks. Suggested translation: "37 has ( ) tens and ( ) ones" | 37里有（）个十和（）个一 | 37 has () tens and () ones |
| error | 91 | p90_s6 | Reviewer (omission): The source has a blank/answer box '364.6.0' with a space and the instruction 'fill in ... with < or >'; the translation keeps '364.6.0' but the item is truncated and the comparison sign is missing. Suggested translation: "6. Fill in 364.6.0 with < or >" | 6.在364.6.0里填上 | 6. Fill in 364.6.0 with |
| error | 92 | p91_s11 | Reviewer (untranslated): The trailing character '付' in the source is a scan artifact; the translation adds 'them' which is not in the source. Minor addition. Suggested translation: "and try to solve" | 并试着解答付 | and try to solve them |
| error | 92 | p91_s13 | Reviewer (number): '34根' — '根' is a measure word for logs, so '34 logs' is correct. No error. | 34根 | 34 logs |
| warning | 1 | p0_s4 | Reviewer (format): The book title 数学 on a cover must be "Mathematics"; splitting it into "MATHE" and "MATICS" across headings is wrong and the casing is not Title Case. Suggested translation: "Mathematics" | 学 | MATICS |
| warning | 4 | p3_s2 | Reviewer (format): The source has no unit number here (it is the title line of Unit 2); adding "Unit 2" duplicates the number given in the preceding item. Suggested translation: "Observing Objects" | 观察物体 | Unit 2 Observing Objects |
| warning | 4 | p3_s5 | Reviewer (format): The source has no unit number on this line; "Unit 4" duplicates the number already supplied by the preceding item. Suggested translation: "Interesting Shapes" | 有趣的图形 | Unit 4 Interesting Shapes |
| warning | 8 | p7_s0 | Reviewer (format): Heading '捉迷藏' should be in Title Case; 'Hide and Seek' is acceptable but as a heading it is fine. No real issue. | 捉迷藏 | Hide and Seek |
| warning | 9 | p8_s4 | Reviewer (grammar): '2. Draw and fill in.' is acceptable; source has no period but it does not matter. No real issue. | 2.画一画，填一填。 | 2. Draw and fill in. |
| warning | 9 | p8_s7 | Reviewer (grammar): Source '还剩8个' has a measure word 个; translation '8 are left' drops the noun, which is acceptable when no noun is named. Fine. | 还剩8个 | 8 are left |
| warning | 13 | p12_s4 | Reviewer (grammar): Source '(2）再提出一个数学问题，' uses a full-width parenthesis ')'; translation uses '(2)' which is fine. No real issue. | (2）再提出一个数学问题， | (2) Ask another math question, |
| warning | 14 | p13_s3 | Reviewer (grammar): Source '多8个' means '8 more'; translation '8 more' is acceptable. | 多8个 | 8 more |
| warning | 17 | p16_s10 | Reviewer (format): The source uses a dash (—) as an answer blank; 'there are ___' adds a blank not present in the source, though it represents the same dash. Acceptable, but the sentence structure differs slightly. Suggested translation: "Answer: there are ___ fewer birds in the tree than in the sky." | 答：树上的小鸟比空中的少—只。 | Answer: there are ___ fewer birds in the tree than in the s… |
| warning | 18 | p17_s0 | Reviewer (format): The source context is 'label' but this matches the heading '练一练' (Practice); casing is fine. No change needed. | 练一练 | Practice |
| warning | 18 | p17_s4 | Reviewer (grammar): The measure word '只' is dropped before 'squirrels'; since the exercise counts squirrels, the noun is given, which is acceptable. | 只小松鼠，72.3.0 | squirrels, 72.3.0 |
| warning | 18 | p17_s6 | Reviewer (format): The source '只小鸭。' has the measure word attached; the English drops it, which is acceptable per conventions since the noun is given. | 只小鸭。 | ducks. |
| warning | 20 | p19_i80_17 | Reviewer (format): The source fragment "有" ("there are") is rendered as a full sentence; as a label inside a figure it is acceptable, but the wording should match the textbook style. Suggested translation: "There are" | 有 | There are |
| warning | 20 | p19_s0 | Reviewer (grammar): After the enumerator "6." the sentence should start with a capital letter. Suggested translation: "6. Write number sentences." | 6.写算式。 | 6. Write number sentences. |
| warning | 21 | p20_s49 | Reviewer (grammar): "Discuss: what pattern do you find?" is informal; textbook style prefers "Talk about it: what pattern do you find?" Suggested translation: "Talk about it: what pattern do you find?" | 说一说，你发现了什么规律？ | Discuss: what pattern do you find? |
| warning | 22 | p21_s1 | Reviewer (format): Section title uses (1) but the unit convention for such labels is (一)/(二) rendered as (1)/(2); acceptable, but keep consistent with p23_s0 "Look (2)". | 看一看（一） | Look (1) |
| warning | 22 | p21_s9 | Reviewer (grammar): "Which picture Xiaoxia sees" is a question fragment without a question mark or auxiliary. Suggested translation: "Which picture does Xiaoxia see?" | 小霞看到的是哪幅图 | Which picture Xiaoxia sees |
| warning | 23 | p22_s1 | Reviewer (format): Quotation marks around the check mark are unnecessary; the standard instruction is (Draw "✓"). Suggested translation: "1. Which picture below does Taoqi see? (Draw "✓")" | 1.下面哪幅图是淘气看到的？（画“✓”） | 1. Which picture below does Taoqi see? (Draw "✓") |
| warning | 25 | p24_s3 | Reviewer (format): Fragment "see?" is stranded at the start of a new item; it belongs to the preceding question. Suggested translation: "see?" | 笑看到的？ | see? |
| warning | 26 | p25_s11 | Reviewer (format): "Count again another way" suggests repeating the previous count; the source means count using a different method. Suggested translation: "Count using another method." | 换一种方法数一数 | Count again another way. |
| warning | 29 | p28_s1 | Reviewer (grammar): Three clauses joined by "and" are ungrammatical; use commas or separate sentences. Suggested translation: "1. Circle, count: how many sticks are there?" | 1.圈一圈，数一数，有多少根小棒？ | 1. Circle, count, and how many sticks are there? |
| warning | 29 | p28_s2 | Reviewer (grammar): Three clauses joined by "and" are ungrammatical. Suggested translation: "2. Circle, count: how many small blocks are there?" | 2.圈一圈，数一数，有多少个小方块？ | 2. Circle, count, and how many small blocks are there? |
| warning | 29 | p28_s3 | Reviewer (grammar): Three clauses joined by "and" are ungrammatical. Suggested translation: "3. Circle, count: how many eggs are there?" | 3.圈一圈，数一数，有多少个鸡蛋？ | 3. Circle, count, and how many eggs are there? |
| warning | 30 | p29_s10 | Reviewer (format): Place-value column labels should use the standard abbreviations "T O". Suggested translation: "T O" | 十位个位 | tens ones |
| warning | 30 | p29_s9 | Reviewer (format): Place-value column labels should use the standard abbreviations "T O". Suggested translation: "T O" | 十位个位 | tens ones |
| warning | 34 | p33_s0 | Reviewer (format): Heading should be in Title Case. Suggested translation: "A Little Farm" | 小小养殖场 | A Little Farm |
| warning | 35 | p34_s3 | Reviewer (grammar): 'a few fewer people skipping rope' is awkward; 'a few fewer' should modify people. Suggested translation: "There are a few fewer people skipping rope than running." | 跳绳的比跑步的少一些。 | There are a few fewer people skipping rope than running. |
| warning | 38 | p37_s0 | Reviewer (format): Heading '练习二' rendered 'Exercise 2' is consistent with the glossary; no issue. | 练习二 | Exercise 2 |
| warning | 39 | p38_s21 | Reviewer (format): Place-value column labels should be 'T O'. Suggested translation: "T O" | 十位个位 | tens ones |
| warning | 39 | p38_s22 | Reviewer (format): Place-value column labels should be 'T O'. Suggested translation: "T O" | 十位个位 | tens ones |
| warning | 39 | p38_s23 | Reviewer (format): Place-value column labels should be 'T O'. Suggested translation: "T O" | 十位个位 | tens ones |
| warning | 39 | p38_s24 | Reviewer (format): Place-value column labels should be 'T O'. Suggested translation: "T O" | 十位个位 | tens ones |
| warning | 39 | p38_s25 | Reviewer (format): Place-value column labels should be 'T O'. Suggested translation: "T O" | 十位个位 | tens ones |
| warning | 41 | p40_s5 | Reviewer (grammar): 'Colour in.' uses British spelling and the trailing preposition is awkward for a textbook instruction; use 'Colour.' Suggested translation: "2. Colour." | 2.涂一涂。 | 2. Colour in. |
| warning | 42 | p41_s0 | Reviewer (format): Heading wording; 'Hands-on (1)' should follow the heading style used for section titles. Suggested translation: "Hands-On (1)" | 动手做（一） | Hands-on (1) |
| warning | 43 | p42_s5 | Reviewer (grammar): Number agreement: 'four triangles of the same size' is fine, but 'these triangles' should be 'these triangles' (ok); no real issue. However wording 'make with these triangles' is fine. Suggested translation: "4. Cut a square piece of paper into four triangles of the same size. What shapes can you make with these triangles?" | 4.将一张正方形的纸剪成四个一样大小的三角形，用这些三角形可以拼出哪些图形？ | 4. Cut a square piece of paper into four triangles of the s… |
| warning | 44 | p43_s0 | Reviewer (format): Heading casing should be 'Hands-On (2)'. Suggested translation: "Hands-On (2)" | 动手做（二） | Hands-on (2) |
| warning | 44 | p43_s3 | Reviewer (grammar): Missing period at the end of the sentence. Suggested translation: "Later, this table evolved into a toy that is very clever and fun. People call it the "tangram"." | 后来，这种桌子演变成了一种玩具，它十分巧妙好玩，人们叫它“七巧板” | Later, this table evolved into a toy that is very clever an… |
| warning | 46 | p45_s0 | Reviewer (format): Heading casing should be 'Hands-On (3)'. Suggested translation: "Hands-On (3)" | 动手做（三） | Hands-on (3) |
| warning | 46 | p45_s10 | Reviewer (grammar): Missing period; source meaning '4 identical triangles' is fine. Suggested translation: "This pinwheel uses 4 identical triangles." | 这个风车用了4个模一样的三角形 | This pinwheel uses 4 identical triangles. |
| warning | 47 | p46_s2 | Reviewer (format): Label casing: sentence-style labels in the source are consistently capitalized; 'Yellow' is acceptable but consistency across the color labels is required. | 黄 | Yellow |
| warning | 48 | p47_s11 | Reviewer (grammar): Missing sentence-final period; the source ends with a period. Suggested translation: "10 tens." | 10个十。 | 10 tens |
| warning | 48 | p47_s12 | Reviewer (grammar): Missing sentence-final period; the source ends with a period. Suggested translation: "1 more than 99." | 比99多1 | 1 more than 99 |
| warning | 48 | p47_s14 | Reviewer (grammar): Missing sentence-final period; the source ends with a period. Suggested translation: "100 ones." | 100个一 | 100 ones |
| warning | 48 | p47_s7 | Reviewer (grammar): 'look at it from different directions, and talk about it' is acceptable but 'talk about what you see' better matches the source's 说一说 in this context. Suggested translation: "Choose your favorite toy, look at it from different directions, and talk about what you see." | 选你喜欢的玩具，从不同方向看一看，说一说。 | Choose your favorite toy, look at it from different directi… |
| warning | 49 | p48_s5 | Reviewer (format): "我提出的问题" is singular ("the question I raised"); the translation makes it plural "My Questions". Suggested translation: "My Question" | 我提出的问题 | My Questions |
| warning | 51 | p50_s13 | Reviewer (grammar): Incomplete English sentence fragment; the source "我踢了" ends without the number, so a natural rendering is "I kicked it". Suggested translation: "I kicked it" | 我踢了 | I kicked it |
| warning | 51 | p50_s16 | Reviewer (format): The translated label has no spaces around the number; "12 times" needs a space. Suggested translation: "204.22.0 12 times" | 204.22.012下 | 204.22.012 times |
| warning | 51 | p50_s17 | Reviewer (grammar): Incomplete English sentence fragment; the source "我踢了" ends without the number, so a natural rendering is "I kicked it". Suggested translation: "I kicked it" | 我踢了 | I kicked it |
| warning | 51 | p50_s5 | Reviewer (grammar): "8. What do they each see? Match." is a statement sentence; it would read more naturally as an instruction with punctuation matching the source. Suggested translation: "8. What does each of them see? Match them." | 8.他们分别看到的是什么？连一连。 | 8. What do they each see? Match. |
| warning | 52 | p51_s4 | Reviewer (grammar): "我收集的比你的多一些" means "I collected a bit more than you (did)"; the translation "I collected a bit more than you" missing a verb is acceptable but "I collected a few more than you" is more natural. Suggested translation: "I collected a few more than you." | 我收集的比你的多一些。 | I collected a bit more than you. |
| warning | 57 | p56_s3 | Reviewer (grammar): Passive 'were eaten in all' is unnatural for a textbook question; active voice is preferable. Suggested translation: "How many insects did they eat in all?" | 一共吃了多少只虫子？ | How many insects were eaten in all? |
| warning | 58 | p57_s4 | Reviewer (grammar): Passive construction is awkward; active voice is more natural. Suggested translation: "(1) How many insects did they eat in all?" | （1）一共吃了多少条虫子？ | (1) How many insects were eaten in all? |
| warning | 66 | p65_s0 | Reviewer (format): The section title '森林医生' is a playful heading meaning 'Forest Doctor'; capitalized as a title is fine, but the trailing period is not necessary in English headings. Suggested translation: "7. Forest Doctor" | 7.森林医生。 | 7. Forest Doctor. |
| warning | 66 | p65_s8 | Reviewer (grammar): The translation 'To buy 1' is missing the object (the item/picture), which makes the sentence unnatural in English. Suggested translation: "I have ¥20. If I buy 1, how much more do I need?" | 我有20元买1个还差多少元？ | I have ¥20. To buy 1, how many more yuan do I need? |
| warning | 67 | p66_s6 | Reviewer (format): The source '顽皮的小狗' is a heading/title; in English title case is preferred without a stray period unless the source has one. Suggested translation: "The Naughty Dog" | 顽皮的小狗。 | The Naughty Dog. |
| warning | 67 | p66_s9 | Reviewer (format): The source '神奇的算式' is a heading; title case is fine, but the translation should not add a period if the source has none. Suggested translation: "Magical Number Sentences" | 神奇的算式。 | Magical Number Sentences. |
| warning | 68 | p67_s7 | Reviewer (format): The source '做一做' is a section label; 'Do It' is fine but title case should be consistent. Suggested translation: "Do It" | 做一做 | Do It |
| warning | 70 | p69_s4 | Reviewer (format): The enumerator is immediately followed by the sentence without a space after the closing parenthesis. Suggested translation: "(1) Can you understand the rules of the game? Talk about them." | （1）你能看懂游戏规则吗？说一说。 | (1)Can you understand the rules of the game? Talk about the… |
| warning | 74 | p73_s5 | Reviewer (grammar): "Forest Doctor" is an unnatural English rendering of 森林医生 (a common error-spotting exercise title). Suggested translation: "5. Forest Doctor" | 5.森林医生。 | 5. Forest Doctor. |
| warning | 75 | p74_s0 | Reviewer (format): Heading 摘苹果 should be in Title Case per convention. Suggested translation: "Picking Apples" | 摘苹果 | Picking Apples |
| warning | 78 | p77_s12 | Reviewer (format): Heading/casing: headings and titles should be in Title Case, so "Math game" should be "Math Game". Suggested translation: "8. Math Game" | 8.数学游戏 | 8. Math game |
| warning | 80 | p79_s2 | Reviewer (grammar): Missing final punctuation; sentence should end with a period. Suggested translation: "I harvested 35 ears of corn." | 我收了35个玉米 | I harvested 35 ears of corn |
| warning | 81 | p80_s0 | Reviewer (format): Heading/title casing: "Forest doctor" should be in Title Case, "Forest Doctor". Suggested translation: "4. Forest Doctor" | 4.森林医生 | 4. Forest doctor |
| warning | 81 | p80_s28 | Reviewer (format): The same label "童话故事" is rendered "Fairy Tales" in the vertical label and again as a heading; heading should be in Title Case, which it is. No issue. | 童话故事 | Fairy Tales |
| warning | 82 | p81_s11 | Reviewer (format): A bare measure word after an answer blank should be the counted noun in parentheses with the plural noun; "(skips)" is acceptable but an answer blank is missing — the source has "（下)" which is a unit label, so "(skips)" is fine. No issue. | （下) | (skips) |
| warning | 84 | p83_s35 | Reviewer (format): A label should keep sentence-style capitalization typical of figure labels; "Athletes assemble" is fine but may be Title Case consistent with other labels. Suggested translation: "Athletes Assemble" | 运动员集合 | Athletes assemble |
| warning | 85 | p84_s5 | Reviewer (format): "森林医生" is a recurring feature title in these books, conventionally "Forest Doctor" in Title Case, not "Forest doctor". Suggested translation: "2. Forest Doctor." | 2.森林医生。 | 2. Forest doctor. |
| warning | 87 | p86_s25 | Reviewer (grammar): Missing final period. Suggested translation: "If you add 20 to me, you get 52." | 我加上20就是52 | If you add 20 to me, you get 52 |
| warning | 88 | p87_s16 | Reviewer (grammar): Sentence is fine but 'pests' consistency with s15. Suggested translation: "I ate 18 fewer insect pests than you." | 我比你少吃了18只害虫。 | I ate 18 fewer pests than you. |
| warning | 91 | p90_s5 | Reviewer (format): The stray quotation mark rendering of '<"' is likely a scan artifact; '<' or '>' would be the mathematical comparison sign. | <”或 | <" or |
| warning | 92 | p91_s19 | Reviewer (format): '合计' in a table should be 'Total' — acceptable; no change needed. | 合计 | Total |
| warning | 93 | p92_s0 | Reviewer (format): Heading casing: 'Ring toss game' should be in Title Case as a title. Suggested translation: "13. Ring Toss Game." | 13.套圈游戏。 | 13. Ring toss game. |
| warning | 94 | p93_s9 | Reviewer (grammar): '下面每幅图分别是谁看到的？' asks who (which person) sees each picture; the translation 'Who sees each picture below?' loses the '分别' (respectively/each) sense, though acceptable. However 'Who sees each picture below?' is student-confusing because it inverts subject/object. Better: 'Who sees each picture below?'. This is a wording issue (warning). Suggested translation: "2. Who sees each picture below? Match." | 2.下面每幅图分别是谁看到的？连一连 | 2. Who sees each picture below? Match. |

### `numbers` — 1 error, 0 warnings

| Severity | Page | Segment | Message | Source | Translation |
|---|---|---|---|---|---|
| error | 29 | p28_s8 | Number "3" from the source is missing in the translation; keep every number exactly as written in the source | 如图是人们发现的大约3万年前的狼骨，你能看懂古人是怎么计数的吗？ | Here is a wolf bone people found that is about 30,000 years… |

### `image_text` — 0 errors, 12 warnings

| Severity | Page | Segment | Message | Source | Translation |
|---|---|---|---|---|---|
| warning | 14 | p13_i56_4 | The text '，\ue00056.4.0\ue001用表示\ue00056.4.r\ue001' was left in the source language (inline pictograms the OCR cannot read (left in the picture)): the line is built around symbols or pictures the OCR could not read - check the page in the preview | ，56.4.0用表示56.4.r |  |
| warning | 14 | p13_i56_4 | The text '，\ue00056.4.0\ue001用表示\ue00056.4.r\ue001' was left in the source language (inline pictograms the OCR cannot read (left in the picture)): the line is built around symbols or pictures the OCR could not read - check the page in the preview | ，56.4.0用表示56.4.r |  |
| warning | 20 | p19_i80_26 | The text '比\ue00080.26.r\ue001' was left in the source language (inline pictograms the OCR cannot read (left in the picture)): the line is built around symbols or pictures the OCR could not read - check the page in the preview | 比80.26.r |  |
| warning | 20 | p19_i80_26 | The text '比\ue00080.26.r\ue001' was left in the source language (inline pictograms the OCR cannot read (left in the picture)): the line is built around symbols or pictures the OCR could not read - check the page in the preview | 比80.26.r |  |
| warning | 38 | p37_i152_9 | The text '3.谁吃的虫子最多？（画“”）谁吃的虫子最少？（画“”）' was left in the source language (unreadable symbol in quotes (left in the picture)): the line is built around symbols or pictures the OCR could not read - check the page in the preview | 3.谁吃的虫子最多？（画“”）谁吃的虫子最少？（画“”） |  |
| warning | 38 | p37_i152_9 | The text '3.谁吃的虫子最多？（画“”）谁吃的虫子最少？（画“”）' was left in the source language (unreadable symbol in quotes (left in the picture)): the line is built around symbols or pictures the OCR could not read - check the page in the preview | 3.谁吃的虫子最多？（画“”）谁吃的虫子最少？（画“”） |  |
| warning | 63 | p62_i252_18 | The text '比小林多3个' was left in the source language (inline pictograms the OCR cannot read (left in the picture)): the line is built around symbols or pictures the OCR could not read - check the page in the preview | 比小林多3个 |  |
| warning | 63 | p62_i252_18 | The text '比小林多3个' was left in the source language (inline pictograms the OCR cannot read (left in the picture)): the line is built around symbols or pictures the OCR could not read - check the page in the preview | 比小林多3个 |  |
| warning | 73 | p72_i292_3 | The text '比第一层多8本' was left in the source language (inline pictograms the OCR cannot read (left in the picture)): the line is built around symbols or pictures the OCR could not read - check the page in the preview | 比第一层多8本 |  |
| warning | 73 | p72_i292_3 | The text '比第一层多8本' was left in the source language (inline pictograms the OCR cannot read (left in the picture)): the line is built around symbols or pictures the OCR could not read - check the page in the preview | 比第一层多8本 |  |
| warning | 73 | p72_i292_5 | The text '比第一层多9本' was left in the source language (inline pictograms the OCR cannot read (left in the picture)): the line is built around symbols or pictures the OCR could not read - check the page in the preview | 比第一层多9本 |  |
| warning | 73 | p72_i292_5 | The text '比第一层多9本' was left in the source language (inline pictograms the OCR cannot read (left in the picture)): the line is built around symbols or pictures the OCR could not read - check the page in the preview | 比第一层多9本 |  |
