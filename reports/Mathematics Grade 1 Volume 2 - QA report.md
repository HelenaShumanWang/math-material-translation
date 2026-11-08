# QA report

**Result:** QA FAILED after 3 rounds: 14 errors, 640 warnings (2820.3 s); proofread: 1616 corrections applied; output file checks: 0 error(s)

**Document:** 数 (zh → en, 99 page(s), 1365 translatable segment(s))

**Checks run:** `completeness`, `placeholders`, `numbers`, `untranslated`, `target_script`, `glossary`, `length_ratio`, `formatting`, `layout_fit`, `image_text`, `llm_review`, `output_checks`

## Rounds

| Round | Errors | Warnings | Re-translated | Passed | Duration |
|---|---|---|---|---|---|
| 1 | 286 | 152 | 230 segment(s) | no | 330.2 s |
| 2 | 136 | 203 | 124 segment(s) | no | 310.0 s |
| 3 | 140 | 139 | 0 segment(s) | no | 94.0 s |

- Round 1: llm_review ×273, glossary ×81, layout_fit ×63, formatting ×7, image_text ×6, untranslated ×5, completeness ×3
- Round 2: llm_review ×293, layout_fit ×31, glossary ×7, image_text ×6, completeness ×1, placeholders ×1
- Round 3: llm_review ×211, layout_fit ×41, glossary ×17, image_text ×6, formatting ×3, untranslated ×1

## Final issues (654)

### `layout_fit` — 14 errors, 4 warnings

| Severity | Page | Segment | Message | Source | Translation |
|---|---|---|---|---|---|
| error | 72 | p71_s15 | Shorten the translation to at most 7 characters so it fits the original box (the current translation of 16 characters overflows its box; the minimum allowed size is 55%) | 童话世 | Fairy Tale World |
| error | 72 | p71_s15 | Shorten the translation to at most 7 characters so it fits the original box (the current translation of 16 characters overflows its box; the minimum allowed size is 55%) | 童话世 | Fairy Tale World |
| error | 72 | p71_s16 | Shorten the translation to at most 9 characters so it fits the original box (the current translation of 12 characters overflows its box; the minimum allowed size is 55%) | 丛林世界 | Jungle World |
| error | 72 | p71_s16 | Shorten the translation to at most 9 characters so it fits the original box (the current translation of 12 characters overflows its box; the minimum allowed size is 55%) | 丛林世界 | Jungle World |
| error | 72 | p71_s30 | Shorten the translation to at most 11 characters so it fits the original box (the current translation of 16 characters overflows its box; the minimum allowed size is 55%) | 童活世 | Fairy Tale World |
| error | 72 | p71_s30 | Shorten the translation to at most 11 characters so it fits the original box (the current translation of 16 characters overflows its box; the minimum allowed size is 55%) | 童活世 | Fairy Tale World |
| error | 72 | p71_s31 | Shorten the translation to at most 8 characters so it fits the original box (the current translation of 11 characters overflows its box; the minimum allowed size is 55%) | 满底世界 | Ocean World |
| error | 72 | p71_s31 | Shorten the translation to at most 8 characters so it fits the original box (the current translation of 11 characters overflows its box; the minimum allowed size is 55%) | 满底世界 | Ocean World |
| error | 72 | p71_s4 | Shorten the translation to at most 11 characters so it fits the original box (the current translation of 16 characters overflows its box; the minimum allowed size is 55%) | 童话世 | Fairy Tale World |
| error | 72 | p71_s4 | Shorten the translation to at most 11 characters so it fits the original box (the current translation of 16 characters overflows its box; the minimum allowed size is 55%) | 童话世 | Fairy Tale World |
| error | 72 | p71_s5 | Shorten the translation to at most 9 characters so it fits the original box (the current translation of 12 characters overflows its box; the minimum allowed size is 55%) | 以林世界 | Jungle World |
| error | 72 | p71_s5 | Shorten the translation to at most 9 characters so it fits the original box (the current translation of 12 characters overflows its box; the minimum allowed size is 55%) | 以林世界 | Jungle World |
| error | 72 | p71_s8 | Shorten the translation to at most 12 characters so it fits the original box (the current translation of 16 characters overflows its box; the minimum allowed size is 55%) | 室话世泵 | Fairy Tale World |
| error | 72 | p71_s8 | Shorten the translation to at most 12 characters so it fits the original box (the current translation of 16 characters overflows its box; the minimum allowed size is 55%) | 室话世泵 | Fairy Tale World |
| warning | 16 | p15_s2 | Reviewed by the proofreader: Shorten the translation to at most 37 characters so it fits the original box (the current translation of 42 characters overflows its box; the minimum allowed size is 55%) | 64.6.l比64.6.0少64.6.1 | 64.6.l has 64.6.1 fewer than 64.6.0. |
| warning | 16 | p15_s2 | Reviewed by the proofreader: Shorten the translation to at most 37 characters so it fits the original box (the current translation of 42 characters overflows its box; the minimum allowed size is 55%) | 64.6.l比64.6.0少64.6.1 | 64.6.l has 64.6.1 fewer than 64.6.0. |
| warning | 82 | p81_s18 | The translation overflows its box and was rendered at 51% of the original size; even a much shorter text would not fit, check this box in the preview | 个位十位 | T O |
| warning | 82 | p81_s18 | The translation overflows its box and was rendered at 51% of the original size; even a much shorter text would not fit, check this box in the preview | 个位十位 | T O |

### `completeness` — 0 errors, 87 warnings

| Severity | Page | Segment | Message | Source | Translation |
|---|---|---|---|---|---|
| warning | 5 | p4_s2 | Reviewed by the proofreader: The segment has no translation; translate the complete source text | eo. |  |
| warning | 8 | p7_a1_p0 | Reviewed by the proofreader: The segment has no translation; translate the complete source text | （个） |  |
| warning | 9 | p8_s8 | Reviewed by the proofreader: The segment has no translation; translate the complete source text | 139号 |  |
| warning | 10 | p9_a1_p0 | Reviewed by the proofreader: The segment has no translation; translate the complete source text | （只） |  |
| warning | 14 | p13_s14 | Reviewed by the proofreader: The segment has no translation; translate the complete source text | 连环画 |  |
| warning | 14 | p13_s15 | Reviewed by the proofreader: The segment has no translation; translate the complete source text | 连环画 |  |
| warning | 14 | p13_s16 | Reviewed by the proofreader: The segment has no translation; translate the complete source text | 连环画 |  |
| warning | 14 | p13_s17 | Reviewed by the proofreader: The segment has no translation; translate the complete source text | 连仔面 |  |
| warning | 14 | p13_s18 | Reviewed by the proofreader: The segment has no translation; translate the complete source text | 连环面 |  |
| warning | 14 | p13_s5 | Reviewed by the proofreader: The segment has no translation; translate the complete source text | 答：56.11.0一多 |  |
| warning | 14 | p13_s7 | Reviewed by the proofreader: The segment has no translation; translate the complete source text | 56.12.l比56.12.r少几 |  |
| warning | 16 | p15_s3 | Reviewed by the proofreader: The segment has no translation; translate the complete source text | 个 |  |
| warning | 16 | p15_s5 | Reviewed by the proofreader: The segment has no translation; translate the complete source text | 个 |  |
| warning | 17 | p16_a1_p0 | Reviewed by the proofreader: The segment has no translation; translate the complete source text | 只 |  |
| warning | 17 | p16_a2_p0 | Reviewed by the proofreader: The segment has no translation; translate the complete source text | 只 |  |
| warning | 17 | p16_s6 | Reviewed by the proofreader: The segment has no translation; translate the complete source text | 只。 |  |
| warning | 19 | p18_s16 | Reviewed by the proofreader: The segment has no translation; translate the complete source text | Mz |  |
| warning | 20 | p19_a1_p0 | Reviewed by the proofreader: The translation ":" contains no words; translate the complete source text | 有 | : |
| warning | 20 | p19_s11 | Reviewed by the proofreader: The translation "," contains no words; translate the complete source text | 只 | , |
| warning | 20 | p19_s12 | Reviewed by the proofreader: The translation ":" contains no words; translate the complete source text | 有 | : |
| warning | 20 | p19_s13 | Reviewed by the proofreader: The translation "," contains no words; translate the complete source text | 只 | , |
| warning | 20 | p19_s14 | Reviewed by the proofreader: The translation ":" contains no words; translate the complete source text | 有 | : |
| warning | 20 | p19_s15 | Reviewed by the proofreader: The translation "." contains no words; translate the complete source text | 只。 | . |
| warning | 20 | p19_s17 | Reviewed by the proofreader: The segment has no translation; translate the complete source text | 多 |  |
| warning | 20 | p19_s19_k0 | Reviewed by the proofreader: The segment has no translation; translate the complete source text | 和共有 |  |
| warning | 20 | p19_s19_k2 | Reviewed by the proofreader: The segment has no translation; translate the complete source text | 和共有 |  |
| warning | 20 | p19_s2 | Reviewed by the proofreader: The segment has no translation; translate the complete source text | 一十+ |  |
| warning | 22 | p21_s10 | Reviewed by the proofreader: The segment has no translation; translate the complete source text | 画 |  |
| warning | 27 | p26_s8_k1 | Reviewed by the proofreader: The segment has no translation; translate the complete source text | 二十三五十六 |  |
| warning | 39 | p38_s27 | Reviewed by the proofreader: The segment has no translation; translate the complete source text | 用2 |  |
| warning | 41 | p40_s8 | Reviewed by the proofreader: The segment has no translation; translate the complete source text | 蓝 |  |
| warning | 41 | p40_s9 | Reviewed by the proofreader: The segment has no translation; translate the complete source text | 黄 |  |
| warning | 47 | p46_s2 | Reviewed by the proofreader: The segment has no translation; translate the complete source text | 黄 |  |
| warning | 47 | p46_s3 | Reviewed by the proofreader: The segment has no translation; translate the complete source text | 红 |  |
| warning | 47 | p46_s4 | Reviewed by the proofreader: The segment has no translation; translate the complete source text | 绿 |  |
| warning | 50 | p49_s27 | Reviewed by the proofreader: The segment has no translation; translate the complete source text | 12-9元 |  |
| warning | 52 | p51_s11 | Reviewed by the proofreader: The segment has no translation; translate the complete source text | 或 |  |
| warning | 53 | p52_s18 | Reviewed by the proofreader: The segment has no translation; translate the complete source text | =40 (个) |  |
| warning | 53 | p52_s19 | Reviewed by the proofreader: The segment has no translation; translate the complete source text | 加数 |  |
| warning | 53 | p52_s20 | Reviewed by the proofreader: The segment has no translation; translate the complete source text | 加数 |  |
| warning | 53 | p52_s21 | Reviewed by the proofreader: The segment has no translation; translate the complete source text | 和 |  |
| warning | 53 | p52_s22 | Reviewed by the proofreader: The segment has no translation; translate the complete source text | 被减数 |  |
| warning | 53 | p52_s23 | Reviewed by the proofreader: The segment has no translation; translate the complete source text | 减数 |  |
| warning | 53 | p52_s24 | Reviewed by the proofreader: The segment has no translation; translate the complete source text | 差 |  |
| warning | 56 | p55_a1_p0 | Reviewed by the proofreader: The segment has no translation; translate the complete source text | （个） |  |
| warning | 58 | p57_s24 | Reviewed by the proofreader: The segment has no translation; translate the complete source text | 42人 |  |
| warning | 58 | p57_s25 | Reviewed by the proofreader: The segment has no translation; translate the complete source text | 30瓶 |  |
| warning | 63 | p62_s14 | Reviewed by the proofreader: The segment has no translation; translate the complete source text | 小林：0000000000000小红：0000000000000 |  |
| warning | 63 | p62_s8 | Reviewed by the proofreader: The segment has no translation; translate the complete source text | 你能提出哪些数学问题？ |  |
| warning | 64 | p63_a1_p0 | Reviewed by the proofreader: The segment has no translation; translate the complete source text | （个） |  |
| warning | 66 | p65_s3 | Reviewed by the proofreader: The segment has no translation; translate the complete source text | 22元 |  |
| warning | 66 | p65_s4 | Reviewed by the proofreader: The segment has no translation; translate the complete source text | 20元0//23元M6元 |  |
| warning | 67 | p66_s21 | Reviewed by the proofreader: The segment has no translation; translate the complete source text | 一 |  |
| warning | 70 | p69_s3 | Reviewed by the proofreader: The segment has no translation; translate the complete source text | 每个空格中只能填1，2，3中的一个每一横行、每一竖行的数字不能重复。 |  |
| warning | 72 | p71_s27 | Reviewed by the proofreader: The segment has no translation; translate the complete source text | 登话世 |  |
| warning | 72 | p71_s32 | Reviewed by the proofreader: The segment has no translation; translate the complete source text | 答： |  |
| warning | 73 | p72_a1_p0 | Reviewed by the proofreader: The segment has no translation; translate the complete source text | （本） |  |
| warning | 73 | p72_s9 | Reviewed by the proofreader: The segment has no translation; translate the complete source text | 292.16.0OO292.16.1O-G（本) |  |
| warning | 74 | p73_s21 | Reviewed by the proofreader: The segment has no translation; translate the complete source text | 人 |  |
| warning | 77 | p76_a1_p0 | Reviewed by the proofreader: The segment has no translation; translate the complete source text | ） |  |
| warning | 78 | p77_s16 | Reviewed by the proofreader: The segment has no translation; translate the complete source text | 于100。 |  |
| warning | 79 | p78_s28 | Reviewed by the proofreader: The segment has no translation; translate the complete source text | 位 |  |
| warning | 81 | p80_s28 | Reviewed by the proofreader: The segment has no translation; translate the complete source text | 童话故事 |  |
| warning | 83 | p82_s10_k0 | Reviewed by the proofreader: The segment has no translation; translate the complete source text | 百位十位个位 |  |
| warning | 83 | p82_s10_k1 | Reviewed by the proofreader: The segment has no translation; translate the complete source text | 百位十位个位 |  |
| warning | 83 | p82_s10_k2 | Reviewed by the proofreader: The segment has no translation; translate the complete source text | 百位十位个位 |  |
| warning | 83 | p82_s11_k0 | Reviewed by the proofreader: The segment has no translation; translate the complete source text | 百位十位 |  |
| warning | 83 | p82_s11_k1 | Reviewed by the proofreader: The segment has no translation; translate the complete source text | 百位十位 |  |
| warning | 83 | p82_s12 | Reviewed by the proofreader: The segment has no translation; translate the complete source text | 个位 |  |
| warning | 83 | p82_s9_k0 | Reviewed by the proofreader: The segment has no translation; translate the complete source text | 百位十位个位 |  |
| warning | 83 | p82_s9_k1 | Reviewed by the proofreader: The segment has no translation; translate the complete source text | 百位十位个位 |  |
| warning | 83 | p82_s9_k2 | Reviewed by the proofreader: The segment has no translation; translate the complete source text | 百位十位个位 |  |
| warning | 86 | p85_s25 | Reviewed by the proofreader: The segment has no translation; translate the complete source text | 晶晶 |  |
| warning | 90 | p89_s8_k0 | Reviewed by the proofreader: The segment has no translation; translate the complete source text | 十位个位 |  |
| warning | 91 | p90_s5 | Reviewed by the proofreader: The segment has no translation; translate the complete source text | <”或 |  |
| warning | 93 | p92_s1_k0 | Reviewed by the proofreader: The segment has no translation; translate the complete source text | 奇思笑笑妙想 |  |
| warning | 93 | p92_s1_k1 | Reviewed by the proofreader: The segment has no translation; translate the complete source text | 奇思笑笑妙想 |  |
| warning | 93 | p92_s1_k2 | Reviewed by the proofreader: The segment has no translation; translate the complete source text | 奇思笑笑妙想 |  |
| warning | 94 | p93_a1_p0 | Reviewed by the proofreader: The segment has no translation; translate the complete source text | 有___个○。 |  |
| warning | 94 | p93_s2 | Reviewed by the proofreader: The segment has no translation; translate the complete source text | 图中有个 |  |
| warning | 94 | p93_s3_k0 | Reviewed by the proofreader: The segment has no translation; translate the complete source text | 图中有个[ |  |
| warning | 94 | p93_s3_k1 | Reviewed by the proofreader: The segment has no translation; translate the complete source text | 有—个 |  |
| warning | 94 | p93_s4 | Reviewed by the proofreader: The segment has no translation; translate the complete source text | 有 |  |
| warning | 94 | p93_s5 | Reviewed by the proofreader: The segment has no translation; translate the complete source text | 有 |  |
| warning | 94 | p93_s6 | Reviewed by the proofreader: The segment has no translation; translate the complete source text | 个△ |  |
| warning | 94 | p93_s7 | Reviewed by the proofreader: The segment has no translation; translate the complete source text | 个△ |  |
| warning | 94 | p93_s8 | Reviewed by the proofreader: The segment has no translation; translate the complete source text | 有 |  |

### `formatting` — 0 errors, 29 warnings

| Severity | Page | Segment | Message | Source | Translation |
|---|---|---|---|---|---|
| warning | 12 | p11_s6 | Reviewed by the proofreader: Remove the symbol(s) △: they are not in the source (a picture in the book is not a symbol; leave it out rather than inventing one) | 用48.7.0表示人，用表示椅子。 | Use 48.7.0 for people and △ for chairs. |
| warning | 22 | p21_s9 | Reviewed by the proofreader: Remove the symbol(s) ✓: they are not in the source (a picture in the book is not a symbol; leave it out rather than inventing one) | 小霞看到的是哪幅图 | Which picture does Xiaoxia see? (Draw “✓”) |
| warning | 26 | p25_s5 | Reviewed by the proofreader: Start the translation with the list marker "·" exactly as in the source | ··九十七、九十八九十九后面是·· | 97, 98, 99, and next comes… |
| warning | 26 | p25_s6 | Reviewed by the proofreader: Start the translation with the list marker "·" exactly as in the source | ·…二十七、二十八二十九，后面是 | 27, 28, 29, and next comes… |
| warning | 27 | p26_s11 | Reviewed by the proofreader: The source does not end with a question mark; do not end the translation with one | 看谁数得快 | Who counts fastest? |
| warning | 30 | p29_s4 | The source does not end with a exclamation mark; do not end the translation with one | 有五十粒 | Fifty beans! |
| warning | 30 | p29_s5 | Reviewed by the proofreader: The source ends with a question mark; end the translation with a question mark too | 我抓的也就二十粒吧？ | I only grabbed about twenty. |
| warning | 32 | p31_s0 | Reviewed by the proofreader: The source does not end with a question mark; do not end the translation with one | 谁的红果多 | Who Has More? |
| warning | 33 | p32_s13 | The source does not end with a exclamation mark; do not end the translation with one | 欢迎小于60的朋友 | Under 60? Welcome! |
| warning | 33 | p32_s14 | The source does not end with a exclamation mark; do not end the translation with one | 欢迎大于60的朋友 | Over 60? Welcome! |
| warning | 35 | p34_s17 | Reviewed by the proofreader: Remove the symbol(s) ✓: they are not in the source (a picture in the book is not a symbol; leave it out rather than inventing one) | 在你认为合适的答案下面画 | Draw "✓" under the answer you think is right. |
| warning | 35 | p34_s4 | Reviewed by the proofreader: Remove the symbol(s) ✓: they are not in the source (a picture in the book is not a symbol; leave it out rather than inventing one) | 跳远的可能有多少人？（画“○”）跳绳的可能有多少人？（画 | How many might do the long jump? (Draw "○") How many might … |
| warning | 38 | p37_i152_9_t | Reviewed by the proofreader: Remove the symbol(s) ○ ✓: they are not in the source (a picture in the book is not a symbol; leave it out rather than inventing one) | 3.谁吃的虫子最多？（画“”）谁吃的虫子最少？（画“”） | 3. Who ate the most bugs? (Draw "○") The fewest? (Draw "✓") |
| warning | 39 | p38_s3 | Reviewed by the proofreader: Remove the symbol(s) ○: they are not in the source (a picture in the book is not a symbol; leave it out rather than inventing one) | 6.在你认为合适的答案下面画 | 6. Draw "○" under the answer you think is right. |
| warning | 41 | p40_s15 | Reviewed by the proofreader: Remove the symbol(s) □: they are not in the source (a picture in the book is not a symbol; leave it out rather than inventing one) | 图中有—个△，有个 | The figure has __ △ and __ □. |
| warning | 44 | p43_s2 | Reviewed by the proofreader: The source does not end with a question mark; do not end the translation with one | 宋朝有个叫黄伯思的人发明了一种桌子，可以根据吃饭人数的不同，把桌子拼成不同的形状，比如3人拼成三角形，4人拼成四方形·… | In the Song Dynasty, a man named Huang Bosi invented a tabl… |
| warning | 44 | p43_s2 | The source ends with a exclamation mark; end the translation with a exclamation mark too | 宋朝有个叫黄伯思的人发明了一种桌子，可以根据吃饭人数的不同，把桌子拼成不同的形状，比如3人拼成三角形，4人拼成四方形·… | In the Song Dynasty, a man named Huang Bosi invented a tabl… |
| warning | 47 | p46_s5 | Reviewed by the proofreader: The source does not end with a question mark; do not end the translation with one | 2.在点子图上用学过的图形设计一个图案，说一说用到了哪些图形。 | 2. Design a pattern on the dot grid with shapes you know. W… |
| warning | 52 | p51_s15_k0 | Reviewed by the proofreader: Keep the symbol(s) ✓ of the source in the translation, at the matching position | 柳树可能有多少棵？（画“✓” | How many willow trees might there be? (Tick one.) |
| warning | 52 | p51_s5 | Reviewed by the proofreader: Keep the symbol(s) ✓ of the source in the translation, at the matching position | 淘气可能收集了多少个？（画“✓” | How many bottles might Taoqi have collected? (Tick one.) |
| warning | 63 | p62_s10 | Reviewed by the proofreader: The source does not end with a question mark; do not end the translation with one | 小青收集了多少个252.15.0 | How many bottles did Xiaoqing collect? |
| warning | 64 | p63_s6 | Reviewed by the proofreader: Keep the symbol(s) ○ of the source in the translation, at the matching position | （1256.7.0）○256.7.1比多5个 | (1) 5 more 256.7.0 than 256.7.1. |
| warning | 65 | p64_s29 | Reviewed by the proofreader: Remove the symbol(s) ○: they are not in the source (a picture in the book is not a symbol; leave it out rather than inventing one) | 6.在260.38.0里填上或 | 6. Fill in each ○ with >, < or =. |
| warning | 66 | p65_s8 | Reviewed by the proofreader: The source ends with a question mark; end the translation with a question mark too | 我有20元买1个还差多少元？ | I have ¥20. To buy 1 |
| warning | 71 | p70_s4 | Reviewed by the proofreader: Keep the symbol(s) ★ of the source in the translation, at the matching position | 数字迷宫按照从51到100的顺序走走看，遇到284.69.0★要填一个数才能通过 | Number maze: go from 51 to 100 in order. At each 284.69.0… |
| warning | 76 | p75_s32 | Reviewed by the proofreader: Start the translation with the list marker "(3）" exactly as in the source | (3）班 | Class 1 (3) |
| warning | 82 | p81_s16 | Reviewed by the proofreader: The source does not end with a question mark; do not end the translation with one | 小亮比小东少跳多少 | How many fewer skips did Xiaoliang do than Xiaodong? |
| warning | 84 | p83_s35 | The source does not end with a exclamation mark; do not end the translation with one | 运动员集合 | Athletes, line up! |
| warning | 95 | p94_s0 | Reviewed by the proofreader: The source does not end with a question mark; do not end the translation with one | 本学期你学到了什么 | What did you learn this term? |

### `glossary` — 0 errors, 169 warnings

| Severity | Page | Segment | Message | Source | Translation |
|---|---|---|---|---|---|
| warning | 3 | p2_s7 | Reviewed by the proofreader: Glossary: translate "数一数" as "Count" | 数一数,有几条漂亮的小鱼? | How many pretty fish? |
| warning | 10 | p9_s10 | Reviewed by the proofreader: Glossary: translate "算一算" as "Calculate" | 算一算，摆一摆。 | Work it out with sticks. |
| warning | 20 | p19_s20 | Reviewed by the proofreader: Glossary: translate "算一算" as "Calculate" | 8.提出两个数学问题，并试着算一算。 | 8. Ask two maths questions and try to answer them. |
| warning | 21 | p20_s21 | Reviewed by the proofreader: Glossary: translate "算式" as "number sentence" | 减8的算式有 | Subtracting 8: |
| warning | 30 | p29_s10_k0 | Reviewed by the proofreader: Glossary: translate "个位" as "ones" | 十位个位 | Tens |
| warning | 30 | p29_s10_k1 | Reviewed by the proofreader: Glossary: translate "十位" as "tens" | 十位个位 | Ones |
| warning | 30 | p29_s13_k0 | Reviewed by the proofreader: Glossary: translate "个位" as "ones" | 十位个位 | Tens |
| warning | 30 | p29_s13_k1 | Reviewed by the proofreader: Glossary: translate "十位" as "tens" | 十位个位 | Ones |
| warning | 30 | p29_s14_k0 | Reviewed by the proofreader: Glossary: translate "个位" as "ones" | 十位个位 | Tens |
| warning | 30 | p29_s14_k1 | Reviewed by the proofreader: Glossary: translate "十位" as "tens" | 十位个位 | Ones |
| warning | 30 | p29_s15_k0 | Reviewed by the proofreader: Glossary: translate "个位" as "ones" | 十位个位 | Tens |
| warning | 30 | p29_s15_k1 | Reviewed by the proofreader: Glossary: translate "十位" as "tens" | 十位个位 | Ones |
| warning | 30 | p29_s16_k0 | Reviewed by the proofreader: Glossary: translate "个位" as "ones" | 百位十位个位 | H |
| warning | 30 | p29_s16_k0 | Reviewed by the proofreader: Glossary: translate "十位" as "tens" | 百位十位个位 | H |
| warning | 30 | p29_s16_k0 | Reviewed by the proofreader: Glossary: translate "百位" as "hundreds" | 百位十位个位 | H |
| warning | 30 | p29_s16_k1 | Reviewed by the proofreader: Glossary: translate "个位" as "ones" | 百位十位个位 | T |
| warning | 30 | p29_s16_k1 | Reviewed by the proofreader: Glossary: translate "十位" as "tens" | 百位十位个位 | T |
| warning | 30 | p29_s16_k1 | Reviewed by the proofreader: Glossary: translate "百位" as "hundreds" | 百位十位个位 | T |
| warning | 30 | p29_s16_k2 | Reviewed by the proofreader: Glossary: translate "个位" as "ones" | 百位十位个位 | O |
| warning | 30 | p29_s16_k2 | Reviewed by the proofreader: Glossary: translate "十位" as "tens" | 百位十位个位 | O |
| warning | 30 | p29_s16_k2 | Reviewed by the proofreader: Glossary: translate "百位" as "hundreds" | 百位十位个位 | O |
| warning | 30 | p29_s9_k0 | Reviewed by the proofreader: Glossary: translate "个位" as "ones" | 十位个位 | Tens |
| warning | 30 | p29_s9_k1 | Reviewed by the proofreader: Glossary: translate "十位" as "tens" | 十位个位 | Ones |
| warning | 31 | p30_s12_k0 | Reviewed by the proofreader: Glossary: translate "个位" as "ones" | 十位个位 | Tens |
| warning | 31 | p30_s12_k1 | Reviewed by the proofreader: Glossary: translate "十位" as "tens" | 十位个位 | Ones |
| warning | 31 | p30_s13_k0 | Reviewed by the proofreader: Glossary: translate "个位" as "ones" | 十位个位 | Tens |
| warning | 31 | p30_s13_k1 | Reviewed by the proofreader: Glossary: translate "十位" as "tens" | 十位个位 | Ones |
| warning | 31 | p30_s14_k0 | Reviewed by the proofreader: Glossary: translate "个位" as "ones" | 十位个位 | Tens |
| warning | 31 | p30_s14_k1 | Reviewed by the proofreader: Glossary: translate "十位" as "tens" | 十位个位 | Ones |
| warning | 31 | p30_s15_k0 | Reviewed by the proofreader: Glossary: translate "个位" as "ones" | 十位个位 | Tens |
| warning | 31 | p30_s15_k1 | Reviewed by the proofreader: Glossary: translate "十位" as "tens" | 十位个位 | Ones |
| warning | 31 | p30_s17_k0 | Reviewed by the proofreader: Glossary: translate "个位" as "ones" | 十位个位 | Tens |
| warning | 31 | p30_s17_k1 | Reviewed by the proofreader: Glossary: translate "十位" as "tens" | 十位个位 | Ones |
| warning | 31 | p30_s4_k0 | Reviewed by the proofreader: Glossary: translate "个位" as "ones" | 十位个位 | Tens |
| warning | 31 | p30_s4_k1 | Reviewed by the proofreader: Glossary: translate "十位" as "tens" | 十位个位 | Ones |
| warning | 32 | p31_s11_k0 | Reviewed by the proofreader: Glossary: translate "个位" as "ones" | 十位个位 | Tens |
| warning | 32 | p31_s11_k1 | Reviewed by the proofreader: Glossary: translate "十位" as "tens" | 十位个位 | Ones |
| warning | 32 | p31_s12_k0 | Reviewed by the proofreader: Glossary: translate "个位" as "ones" | 十位个位 | Tens |
| warning | 32 | p31_s12_k1 | Reviewed by the proofreader: Glossary: translate "十位" as "tens" | 十位个位 | Ones |
| warning | 32 | p31_s13_k0 | Reviewed by the proofreader: Glossary: translate "个位" as "ones" | 百位十位个位 | H |
| warning | 32 | p31_s13_k0 | Reviewed by the proofreader: Glossary: translate "十位" as "tens" | 百位十位个位 | H |
| warning | 32 | p31_s13_k0 | Reviewed by the proofreader: Glossary: translate "百位" as "hundreds" | 百位十位个位 | H |
| warning | 32 | p31_s13_k1 | Reviewed by the proofreader: Glossary: translate "个位" as "ones" | 百位十位个位 | T |
| warning | 32 | p31_s13_k1 | Reviewed by the proofreader: Glossary: translate "十位" as "tens" | 百位十位个位 | T |
| warning | 32 | p31_s13_k1 | Reviewed by the proofreader: Glossary: translate "百位" as "hundreds" | 百位十位个位 | T |
| warning | 32 | p31_s13_k2 | Reviewed by the proofreader: Glossary: translate "个位" as "ones" | 百位十位个位 | O |
| warning | 32 | p31_s13_k2 | Reviewed by the proofreader: Glossary: translate "十位" as "tens" | 百位十位个位 | O |
| warning | 32 | p31_s13_k2 | Reviewed by the proofreader: Glossary: translate "百位" as "hundreds" | 百位十位个位 | O |
| warning | 32 | p31_s14_k0 | Reviewed by the proofreader: Glossary: translate "个位" as "ones" | 十位个位 | Tens |
| warning | 32 | p31_s14_k1 | Reviewed by the proofreader: Glossary: translate "十位" as "tens" | 十位个位 | Ones |
| warning | 32 | p31_s8_k0 | Reviewed by the proofreader: Glossary: translate "个位" as "ones" | 十位个位 | Tens |
| warning | 32 | p31_s8_k1 | Reviewed by the proofreader: Glossary: translate "十位" as "tens" | 十位个位 | Ones |
| warning | 32 | p31_s9_k0 | Reviewed by the proofreader: Glossary: translate "个位" as "ones" | 十位个位 | Tens |
| warning | 32 | p31_s9_k1 | Reviewed by the proofreader: Glossary: translate "十位" as "tens" | 十位个位 | Ones |
| warning | 33 | p32_s2_k0 | Reviewed by the proofreader: Glossary: translate "个位" as "ones" | 十位个位 | Tens |
| warning | 33 | p32_s2_k1 | Reviewed by the proofreader: Glossary: translate "十位" as "tens" | 十位个位 | Ones |
| warning | 33 | p32_s3_k0 | Reviewed by the proofreader: Glossary: translate "个位" as "ones" | 十位个位 | Tens |
| warning | 33 | p32_s3_k1 | Reviewed by the proofreader: Glossary: translate "十位" as "tens" | 十位个位 | Ones |
| warning | 33 | p32_s4_k0 | Reviewed by the proofreader: Glossary: translate "个位" as "ones" | 十位个位 | Tens |
| warning | 33 | p32_s4_k1 | Reviewed by the proofreader: Glossary: translate "十位" as "tens" | 十位个位 | Ones |
| warning | 33 | p32_s5_k0 | Reviewed by the proofreader: Glossary: translate "个位" as "ones" | 十位个位 | Tens |
| warning | 33 | p32_s5_k1 | Reviewed by the proofreader: Glossary: translate "十位" as "tens" | 十位个位 | Ones |
| warning | 33 | p32_s6_k0 | Reviewed by the proofreader: Glossary: translate "个位" as "ones" | 百位十位个位 | H |
| warning | 33 | p32_s6_k0 | Reviewed by the proofreader: Glossary: translate "十位" as "tens" | 百位十位个位 | H |
| warning | 33 | p32_s6_k0 | Reviewed by the proofreader: Glossary: translate "百位" as "hundreds" | 百位十位个位 | H |
| warning | 33 | p32_s6_k1 | Reviewed by the proofreader: Glossary: translate "个位" as "ones" | 百位十位个位 | T |
| warning | 33 | p32_s6_k1 | Reviewed by the proofreader: Glossary: translate "十位" as "tens" | 百位十位个位 | T |
| warning | 33 | p32_s6_k1 | Reviewed by the proofreader: Glossary: translate "百位" as "hundreds" | 百位十位个位 | T |
| warning | 33 | p32_s6_k2 | Reviewed by the proofreader: Glossary: translate "个位" as "ones" | 百位十位个位 | O |
| warning | 33 | p32_s6_k2 | Reviewed by the proofreader: Glossary: translate "十位" as "tens" | 百位十位个位 | O |
| warning | 33 | p32_s6_k2 | Reviewed by the proofreader: Glossary: translate "百位" as "hundreds" | 百位十位个位 | O |
| warning | 33 | p32_s7_k0 | Reviewed by the proofreader: Glossary: translate "个位" as "ones" | 十位个位 | Tens |
| warning | 33 | p32_s7_k1 | Reviewed by the proofreader: Glossary: translate "十位" as "tens" | 十位个位 | Ones |
| warning | 37 | p36_s4 | Reviewed by the proofreader: Glossary: translate "个位" as "ones" | （3）把个位和十位上的数相同的涂上黄色。 | (3) Colour yellow the numbers whose two digits are the same. |
| warning | 37 | p36_s4 | Reviewed by the proofreader: Glossary: translate "十位" as "tens" | （3）把个位和十位上的数相同的涂上黄色。 | (3) Colour yellow the numbers whose two digits are the same. |
| warning | 38 | p37_s10 | Reviewed by the proofreader: Glossary: translate "填一填" as "Fill in" | 4.按规律填一填。 | 4. Complete the pattern. |
| warning | 38 | p37_s3_k0 | Reviewed by the proofreader: Glossary: translate "个位" as "ones" | 十位个位 | Tens |
| warning | 38 | p37_s3_k1 | Reviewed by the proofreader: Glossary: translate "十位" as "tens" | 十位个位 | Ones |
| warning | 38 | p37_s6_k0 | Reviewed by the proofreader: Glossary: translate "个位" as "ones" | 十位个位 | Tens |
| warning | 38 | p37_s6_k1 | Reviewed by the proofreader: Glossary: translate "十位" as "tens" | 十位个位 | Ones |
| warning | 39 | p38_s21_k0 | Reviewed by the proofreader: Glossary: translate "个位" as "ones" | 十位个位 | Tens |
| warning | 39 | p38_s21_k1 | Reviewed by the proofreader: Glossary: translate "十位" as "tens" | 十位个位 | Ones |
| warning | 39 | p38_s22_k0 | Reviewed by the proofreader: Glossary: translate "个位" as "ones" | 十位个位 | Tens |
| warning | 39 | p38_s22_k1 | Reviewed by the proofreader: Glossary: translate "十位" as "tens" | 十位个位 | Ones |
| warning | 39 | p38_s23_k0 | Reviewed by the proofreader: Glossary: translate "个位" as "ones" | 十位个位 | Tens |
| warning | 39 | p38_s23_k1 | Reviewed by the proofreader: Glossary: translate "十位" as "tens" | 十位个位 | Ones |
| warning | 39 | p38_s24_k0 | Reviewed by the proofreader: Glossary: translate "个位" as "ones" | 十位个位 | Tens |
| warning | 39 | p38_s24_k1 | Reviewed by the proofreader: Glossary: translate "十位" as "tens" | 十位个位 | Ones |
| warning | 39 | p38_s25_k0 | Reviewed by the proofreader: Glossary: translate "个位" as "ones" | 十位个位 | Tens |
| warning | 39 | p38_s25_k1 | Reviewed by the proofreader: Glossary: translate "十位" as "tens" | 十位个位 | Ones |
| warning | 48 | p47_s6 | Reviewed by the proofreader: Glossary: translate "算一算" as "Calculate" | 算一算，和同伴说说你的计算过程。 | Work it out and tell your partner how you did it. |
| warning | 51 | p50_s1_k0 | Reviewed by the proofreader: Glossary: translate "个位" as "ones" | 十位个位 | T |
| warning | 51 | p50_s1_k0 | Reviewed by the proofreader: Glossary: translate "十位" as "tens" | 十位个位 | T |
| warning | 51 | p50_s1_k1 | Reviewed by the proofreader: Glossary: translate "个位" as "ones" | 十位个位 | O |
| warning | 51 | p50_s1_k1 | Reviewed by the proofreader: Glossary: translate "十位" as "tens" | 十位个位 | O |
| warning | 51 | p50_s2_k0 | Reviewed by the proofreader: Glossary: translate "个位" as "ones" | 十位个位 | T |
| warning | 51 | p50_s2_k0 | Reviewed by the proofreader: Glossary: translate "十位" as "tens" | 十位个位 | T |
| warning | 51 | p50_s2_k1 | Reviewed by the proofreader: Glossary: translate "个位" as "ones" | 十位个位 | O |
| warning | 51 | p50_s2_k1 | Reviewed by the proofreader: Glossary: translate "十位" as "tens" | 十位个位 | O |
| warning | 51 | p50_s3_k0 | Reviewed by the proofreader: Glossary: translate "个位" as "ones" | 十位个位 | T |
| warning | 51 | p50_s3_k0 | Reviewed by the proofreader: Glossary: translate "十位" as "tens" | 十位个位 | T |
| warning | 51 | p50_s3_k1 | Reviewed by the proofreader: Glossary: translate "个位" as "ones" | 十位个位 | O |
| warning | 51 | p50_s3_k1 | Reviewed by the proofreader: Glossary: translate "十位" as "tens" | 十位个位 | O |
| warning | 51 | p50_s4_k0 | Reviewed by the proofreader: Glossary: translate "个位" as "ones" | 百位十位个位 | H |
| warning | 51 | p50_s4_k0 | Reviewed by the proofreader: Glossary: translate "十位" as "tens" | 百位十位个位 | H |
| warning | 51 | p50_s4_k0 | Reviewed by the proofreader: Glossary: translate "百位" as "hundreds" | 百位十位个位 | H |
| warning | 51 | p50_s4_k1 | Reviewed by the proofreader: Glossary: translate "个位" as "ones" | 百位十位个位 | T |
| warning | 51 | p50_s4_k1 | Reviewed by the proofreader: Glossary: translate "十位" as "tens" | 百位十位个位 | T |
| warning | 51 | p50_s4_k1 | Reviewed by the proofreader: Glossary: translate "百位" as "hundreds" | 百位十位个位 | T |
| warning | 51 | p50_s4_k2 | Reviewed by the proofreader: Glossary: translate "个位" as "ones" | 百位十位个位 | O |
| warning | 51 | p50_s4_k2 | Reviewed by the proofreader: Glossary: translate "十位" as "tens" | 百位十位个位 | O |
| warning | 51 | p50_s4_k2 | Reviewed by the proofreader: Glossary: translate "百位" as "hundreds" | 百位十位个位 | O |
| warning | 53 | p52_s15_k0 | Reviewed by the proofreader: Glossary: translate "个位" as "ones" | 十位个位 | Tens |
| warning | 53 | p52_s15_k1 | Reviewed by the proofreader: Glossary: translate "十位" as "tens" | 十位个位 | Ones |
| warning | 53 | p52_s9_k1 | Reviewed by the proofreader: Glossary: translate "十位" as "tens" | 十位介位 | Ones |
| warning | 55 | p54_s11_k0 | Reviewed by the proofreader: Glossary: translate "个位" as "ones" | 十位个位 | Tens |
| warning | 55 | p54_s11_k1 | Reviewed by the proofreader: Glossary: translate "十位" as "tens" | 十位个位 | Ones |
| warning | 55 | p54_s18_k0 | Reviewed by the proofreader: Glossary: translate "个位" as "ones" | 十位个位 | Tens |
| warning | 55 | p54_s18_k1 | Reviewed by the proofreader: Glossary: translate "十位" as "tens" | 十位个位 | Ones |
| warning | 56 | p55_s4 | Reviewed by the proofreader: Glossary: translate "算一算" as "Calculate" | 2.用计数器拨一拨，算一算。 | 2. Work these out on a counting frame. |
| warning | 57 | p56_s13_k0 | Reviewed by the proofreader: Glossary: translate "个位" as "ones" | 十位个位 | Tens |
| warning | 57 | p56_s13_k1 | Reviewed by the proofreader: Glossary: translate "十位" as "tens" | 十位个位 | Ones |
| warning | 57 | p56_s7_k0 | Reviewed by the proofreader: Glossary: translate "个位" as "ones" | 十位个位 | Tens |
| warning | 57 | p56_s7_k1 | Reviewed by the proofreader: Glossary: translate "十位" as "tens" | 十位个位 | Ones |
| warning | 59 | p58_s14 | Reviewed by the proofreader: Glossary: translate "竖式" as "vertical form" | 学习竖式计算啦！ | Let's learn the column method! |
| warning | 59 | p58_s21 | Reviewed by the proofreader: Glossary: translate "竖式" as "vertical form" | 用竖式计算。 | Use the column method. |
| warning | 60 | p59_s8 | Reviewed by the proofreader: Glossary: translate "竖式" as "vertical form" | 3.用竖式计算。 | 3. Use the column method. |
| warning | 61 | p60_s10 | Reviewed by the proofreader: Glossary: translate "淘气" as "Taoqi" | 答：笑笑比淘气少收 | Answer: Xiaoxiao picked |
| warning | 61 | p60_s12 | Reviewed by the proofreader: Glossary: translate "算一算" as "Calculate" | 你能用竖式算一算吗？想一想，填一填。 | Can you use the column method? Think and fill in. |
| warning | 61 | p60_s12 | Reviewed by the proofreader: Glossary: translate "竖式" as "vertical form" | 你能用竖式算一算吗？想一想，填一填。 | Can you use the column method? Think and fill in. |
| warning | 62 | p61_s8 | Reviewed by the proofreader: Glossary: translate "竖式" as "vertical form" | 3.用竖式计算。 | 3. Use the column method. |
| warning | 72 | p71_s20 | Reviewed by the proofreader: Glossary: translate "算一算" as "Calculate" | 你能用竖式算一算吗？ | Can you use the column method? |
| warning | 72 | p71_s20 | Reviewed by the proofreader: Glossary: translate "竖式" as "vertical form" | 你能用竖式算一算吗？ | Can you use the column method? |
| warning | 72 | p71_s24_k0 | Reviewed by the proofreader: Glossary: translate "个位" as "ones" | 十位个位 | Tens |
| warning | 72 | p71_s24_k1 | Reviewed by the proofreader: Glossary: translate "十位" as "tens" | 十位个位 | Ones |
| warning | 72 | p71_s25_k0 | Reviewed by the proofreader: Glossary: translate "个位" as "ones" | 十位个位 | Tens |
| warning | 72 | p71_s25_k1 | Reviewed by the proofreader: Glossary: translate "十位" as "tens" | 十位个位 | Ones |
| warning | 72 | p71_s26_k0 | Reviewed by the proofreader: Glossary: translate "个位" as "ones" | 十位个位 | Tens |
| warning | 72 | p71_s26_k1 | Reviewed by the proofreader: Glossary: translate "十位" as "tens" | 十位个位 | Ones |
| warning | 73 | p72_s15 | Reviewed by the proofreader: Glossary: translate "算一算" as "Calculate" | 2.用坚式算一算 | 2. Use the column method. |
| warning | 76 | p75_s11 | Reviewed by the proofreader: Glossary: translate "竖式" as "vertical form" | 3.用竖式计算。 | 3. Use the column method. |
| warning | 77 | p76_s18 | Reviewed by the proofreader: Glossary: translate "竖式" as "vertical form" | 4.用竖式计算。 | 4. Use the column method. |
| warning | 79 | p78_s20 | Reviewed by the proofreader: Glossary: translate "算一算" as "Calculate" | 你能用竖式算一算吗？ | Can you use the column method? |
| warning | 79 | p78_s20 | Reviewed by the proofreader: Glossary: translate "竖式" as "vertical form" | 你能用竖式算一算吗？ | Can you use the column method? |
| warning | 80 | p79_s23 | Reviewed by the proofreader: Glossary: translate "竖式" as "vertical form" | 3.用竖式计算。 | 3. Use the column method. |
| warning | 82 | p81_s12 | Reviewed by the proofreader: Glossary: translate "个位" as "ones" | 十个位位 | T O |
| warning | 82 | p81_s18 | Reviewed by the proofreader: Glossary: translate "个位" as "ones" | 个位十位 | T O |
| warning | 82 | p81_s18 | Reviewed by the proofreader: Glossary: translate "十位" as "tens" | 个位十位 | T O |
| warning | 83 | p82_a1_p0 | Reviewed by the proofreader: Glossary: translate "百位" as "hundreds" | 百位 | H |
| warning | 83 | p82_a2_p0 | Reviewed by the proofreader: Glossary: translate "十位" as "tens" | 十位 | T |
| warning | 83 | p82_a3_p0 | Reviewed by the proofreader: Glossary: translate "个位" as "ones" | 个位 | O |
| warning | 83 | p82_a4_p0 | Reviewed by the proofreader: Glossary: translate "百位" as "hundreds" | 百位 | H |
| warning | 83 | p82_a5_p0 | Reviewed by the proofreader: Glossary: translate "十位" as "tens" | 十位 | T |
| warning | 83 | p82_a6_p0 | Reviewed by the proofreader: Glossary: translate "个位" as "ones" | 个位 | O |
| warning | 83 | p82_a7_p0 | Reviewed by the proofreader: Glossary: translate "百位" as "hundreds" | 百位 | H |
| warning | 83 | p82_a8_p0 | Reviewed by the proofreader: Glossary: translate "十位" as "tens" | 十位 | T |
| warning | 83 | p82_a9_p0 | Reviewed by the proofreader: Glossary: translate "个位" as "ones" | 个位 | O |
| warning | 83 | p82_s14 | Reviewed by the proofreader: Glossary: translate "算一算" as "Calculate" | 1.用小棒或计数器做一做，再用竖式算一算。 | 1. Use sticks or a counting frame, then use the column meth… |
| warning | 83 | p82_s14 | Reviewed by the proofreader: Glossary: translate "竖式" as "vertical form" | 1.用小棒或计数器做一做，再用竖式算一算。 | 1. Use sticks or a counting frame, then use the column meth… |
| warning | 83 | p82_s7 | Reviewed by the proofreader: Glossary: translate "算一算" as "Calculate" | 拨一拨，再试着用竖式算一算 | Move the beads, then try using the column method. |
| warning | 83 | p82_s7 | Reviewed by the proofreader: Glossary: translate "竖式" as "vertical form" | 拨一拨，再试着用竖式算一算 | Move the beads, then try using the column method. |
| warning | 83 | p82_s8 | Reviewed by the proofreader: Glossary: translate "个位" as "ones" | 百332.8.0十个位位位 | H T O |
| warning | 84 | p83_s35 | Reviewed by the proofreader: Glossary: translate "集合" as "set" | 运动员集合 | Athletes, line up! |
| warning | 85 | p84_s1 | Reviewed by the proofreader: Glossary: translate "算一算" as "Calculate" | 1.用小棒或计数器做一做，再用竖式算一算。 | 1. Use sticks or a counting frame, then use the column meth… |
| warning | 85 | p84_s1 | Reviewed by the proofreader: Glossary: translate "竖式" as "vertical form" | 1.用小棒或计数器做一做，再用竖式算一算。 | 1. Use sticks or a counting frame, then use the column meth… |
| warning | 88 | p87_s22_k0 | Reviewed by the proofreader: Glossary: translate "个位" as "ones" | 十位个位 | Tens |
| warning | 88 | p87_s22_k1 | Reviewed by the proofreader: Glossary: translate "十位" as "tens" | 十位个位 | Ones |
| warning | 88 | p87_s6 | Reviewed by the proofreader: Glossary: translate "竖式" as "vertical form" | 4.用竖式计算，并利用小棒或计数器说说你是怎么计算的。 | 4. Use the column method, then explain how with sticks or a… |
| warning | 91 | p90_s0 | Reviewed by the proofreader: Glossary: translate "竖式" as "vertical form" | 5.用竖式计算。 | 5. Use the column method. |

### `image_text` — 0 errors, 2 warnings

| Severity | Page | Segment | Message | Source | Translation |
|---|---|---|---|---|---|
| warning | 20 | p19_i80_26 | The text '比\ue00080.26.r\ue001' was left in the source language (inline pictograms the OCR cannot read (left in the picture)): the line is built around symbols or pictures the OCR could not read - check the page in the preview | 比80.26.r |  |
| warning | 20 | p19_i80_26 | The text '比\ue00080.26.r\ue001' was left in the source language (inline pictograms the OCR cannot read (left in the picture)): the line is built around symbols or pictures the OCR could not read - check the page in the preview | 比80.26.r |  |

### `length_ratio` — 0 errors, 3 warnings

| Severity | Page | Segment | Message | Source | Translation |
|---|---|---|---|---|---|
| warning | 52 | p51_s15_k2_k0 | The translation looks too short: 2 characters for 9 translatable source characters (ratio 0.22, about 2.60 expected); check that nothing was omitted | 42棵81棵15棵 | 42 |
| warning | 52 | p51_s15_k2_k1 | The translation looks too short: 2 characters for 9 translatable source characters (ratio 0.22, about 2.60 expected); check that nothing was omitted | 42棵81棵15棵 | 81 |
| warning | 52 | p51_s15_k2_k2 | The translation looks too short: 2 characters for 9 translatable source characters (ratio 0.22, about 2.60 expected); check that nothing was omitted | 42棵81棵15棵 | 15 |

### `llm_review` — 0 errors, 15 warnings

| Severity | Page | Segment | Message | Source | Translation |
|---|---|---|---|---|---|
| warning | 1 | p0_s4 | Earlier automatic review, text kept by the proofreading: Reviewer (meaning): The source '学' is the second half of 数学; it should not be rendered as a separate 'Mathematics' but combined with the previous heading into one title. |  |  |
| warning | 14 | p13_s1 | Reviewer (grammar): Word order 'How many more X than Y?' is awkward; better 'How many more are there of X than of Y?' or 'How many more X are there than Y?' Suggested translation: "How many more 56.1.l are there than 56.1.0?" | 56.1.l比56.1.0多几个？ | How many more 56.1.l than 56.1.0? |
| warning | 18 | p17_s6 | Earlier automatic review, text kept by the proofreading: Reviewer (omission): The measure word '只' is dropped; when the context names the animal, write the plural noun. Suggested translation: "ducks." | 只小鸭。 | ducks. |
| warning | 20 | p19_i80_17 | Earlier automatic review, text kept by the proofreading: Reviewer (meaning): A single figure label '有' ('has/there are'); 'Has' is acceptable but 'There are' may fit a figure label better. Context is limited. | 有 | Has |
| warning | 34 | p33_s16 | Reviewer (grammar): 'how many sheep might there be' is acceptable; but 'Think:' punctuation differs from other items — minor consistency only. No change needed. | 想一想，羊可能有多少只？（画“✓”） | Think: how many sheep might there be? (Draw "✓") |
| warning | 48 | p47_s14 | Reviewer (grammar): "100 ones" reads unnaturally as a place-value label; the counted thing (ones) should be written naturally. Suggested translation: "100 ones" | 100个一 | 100 ones |
| warning | 48 | p47_s5 | Earlier automatic review, text kept by the proofreading: Reviewer (meaning): The source label is simply "15个" (15 items); adding "plates" invents a noun not present in the source, and the context does not establish the object here. Suggested translation: "15" | 15个 | 15 plates |
| warning | 51 | p50_s16 | Earlier automatic review, text kept by the proofreading: Reviewer (number): The trailing measure word 下 was dropped from the label; keep the kicks unit. Suggested translation: "204.22.012 kicks" |  |  |
| warning | 66 | p65_s6 | Reviewer (grammar): "Buy 1" is incomplete; the counted object (batteries) should be supplied, and a numeral should agree with its noun. Suggested translation: "Buy 1 battery" | 买1个 | Buy 1 |
| warning | 66 | p65_s9 | Reviewer (grammar): The measure word 个 names the counted object; writing just "1" drops it. Suggested translation: "1 battery" | 1个 | 1 |
| warning | 77 | p76_s26 | Earlier automatic review, text kept by the proofreading: Reviewer (omission): The counted object after 40 is dropped; a heading label should keep the noun (e.g. 'Holds 40'). Suggested translation: "Holds 40 items" | 装40个 | Holds 40 |
| warning | 80 | p79_s3 | Earlier automatic review, text kept by the proofreading: Reviewer (omission): Subject placeholder ⟦0⟧ (a picture/character) is missing from the translation. Suggested translation: "How many ears of corn did ⟦0⟧ pick?" | 320.4.0收了多少个玉米？ | How many ears of corn did 320.4.0 pick? |
| warning | 90 | p89_s6 | Earlier automatic review, text kept by the proofreading: Reviewer (omission): Measure word 支 names the counted objects (pencils, presumably); dropping it loses the unit. Following the convention, write the object when context gives it; otherwise keep as "10 (pencils)" or "10 each". The bare "10" drops the measure word entirely. Suggested translation: "10 (pencils)" | 10支 | 10 |
| warning | 90 | p89_s7 | Earlier automatic review, text kept by the proofreading: Reviewer (omission): Same as p89_s6: 支 measure word dropped; should name the counted objects. Suggested translation: "10 (pencils)" | 10支 | 10 |
| warning | 93 | p92_s14 | Earlier automatic review, text kept by the proofreading: Reviewer (terminology): 76下 means 76 skips (jumps); consistent, fine. No issue. | 76下 | 76 skips |

### `numbers` — 0 errors, 45 warnings

| Severity | Page | Segment | Message | Source | Translation |
|---|---|---|---|---|---|
| warning | 1 | p0_s0 | Reviewed by the proofreader: Number "0" from the source is missing in the translation; keep every number exactly as written in the source | 教育部632.0.0审定 | Ministry Approved |
| warning | 1 | p0_s0 | Reviewed by the proofreader: Number "632" from the source is missing in the translation; keep every number exactly as written in the source | 教育部632.0.0审定 | Ministry Approved |
| warning | 6 | p5_s0 | Reviewed by the proofreader: Number "0" from the source is missing in the translation; keep every number exactly as written in the source | 一 加与减（一24.0.0）24.0.1 | Unit 1 Addition and Subtraction (1) |
| warning | 6 | p5_s0 | Reviewed by the proofreader: Number "24" from the source is missing in the translation; keep every number exactly as written in the source | 一 加与减（一24.0.0）24.0.1 | Unit 1 Addition and Subtraction (1) |
| warning | 14 | p13_s10 | Reviewed by the proofreader: Number "14" from the source is missing in the translation; keep every number exactly as written in the source | 56.14.0比56.14.156.14.2一少几个也就是56.16.0比56.16.1多几个 | How many fewer 56.14.0 than 56.14.1 is the same as how … |
| warning | 14 | p13_s10 | Reviewed by the proofreader: Number "2" from the source is missing in the translation; keep every number exactly as written in the source | 56.14.0比56.14.156.14.2一少几个也就是56.16.0比56.16.1多几个 | How many fewer 56.14.0 than 56.14.1 is the same as how … |
| warning | 14 | p13_s10 | Reviewed by the proofreader: Number "56" from the source is missing in the translation; keep every number exactly as written in the source | 56.14.0比56.14.156.14.2一少几个也就是56.16.0比56.16.1多几个 | How many fewer 56.14.0 than 56.14.1 is the same as how … |
| warning | 27 | p26_s4 | Reviewed by the proofreader: Number "0" from the source is missing in the translation; keep every number exactly as written in the source | 九十、八十、七十、108.4.0 | Ninety, eighty, seventy, |
| warning | 27 | p26_s4 | Reviewed by the proofreader: Number "108" from the source is missing in the translation; keep every number exactly as written in the source | 九十、八十、七十、108.4.0 | Ninety, eighty, seventy, |
| warning | 27 | p26_s4 | Reviewed by the proofreader: Number "4" from the source is missing in the translation; keep every number exactly as written in the source | 九十、八十、七十、108.4.0 | Ninety, eighty, seventy, |
| warning | 29 | p28_s8 | Reviewed by the proofreader: Number "3" from the source is missing in the translation; keep every number exactly as written in the source | 如图是人们发现的大约3万年前的狼骨，你能看懂古人是怎么计数的吗？ | People found this wolf bone. It is about 30,000 years old. … |
| warning | 29 | p28_s9_k0 | Reviewed by the proofreader: Number "25" from the source is missing in the translation; keep every number exactly as written in the source | 第二组30道痕第一组25道痕 | Group 2: 30 marks |
| warning | 29 | p28_s9_k1 | Reviewed by the proofreader: Number "30" from the source is missing in the translation; keep every number exactly as written in the source | 第二组30道痕第一组25道痕 | Group 1: 25 marks |
| warning | 39 | p38_s15 | Reviewed by the proofreader: Number "0" from the source is missing in the translation; keep every number exactly as written in the source | 有90本吗？156.22.0 | Are there 90? |
| warning | 39 | p38_s15 | Reviewed by the proofreader: Number "156" from the source is missing in the translation; keep every number exactly as written in the source | 有90本吗？156.22.0 | Are there 90? |
| warning | 39 | p38_s15 | Reviewed by the proofreader: Number "22" from the source is missing in the translation; keep every number exactly as written in the source | 有90本吗？156.22.0 | Are there 90? |
| warning | 48 | p47_s13 | Reviewed by the proofreader: Number "50" from the source is missing in the translation; keep every number exactly as written in the source | 2个50 | 2 fifties |
| warning | 51 | p50_s17 | Reviewed by the proofreader: Number "0" from the source is missing in the translation; keep every number exactly as written in the source | 我踢了204.22.012下 | I did 12 kicks. |
| warning | 51 | p50_s17 | Reviewed by the proofreader: Number "204" from the source is missing in the translation; keep every number exactly as written in the source | 我踢了204.22.012下 | I did 12 kicks. |
| warning | 51 | p50_s17 | Reviewed by the proofreader: Number "22" from the source is missing in the translation; keep every number exactly as written in the source | 我踢了204.22.012下 | I did 12 kicks. |
| warning | 52 | p51_s10 | Reviewed by the proofreader: Number "0" from the source is missing in the translation; keep every number exactly as written in the source | 13.在208.11.00里填上 | 13. Fill in each 208.11.0 with >, < or =. |
| warning | 52 | p51_s15_k2_k0 | Reviewed by the proofreader: Number "15" from the source is missing in the translation; keep every number exactly as written in the source | 42棵81棵15棵 | 42 |
| warning | 52 | p51_s15_k2_k0 | Reviewed by the proofreader: Number "81" from the source is missing in the translation; keep every number exactly as written in the source | 42棵81棵15棵 | 42 |
| warning | 52 | p51_s15_k2_k1 | Reviewed by the proofreader: Number "15" from the source is missing in the translation; keep every number exactly as written in the source | 42棵81棵15棵 | 81 |
| warning | 52 | p51_s15_k2_k1 | Reviewed by the proofreader: Number "42" from the source is missing in the translation; keep every number exactly as written in the source | 42棵81棵15棵 | 81 |
| warning | 52 | p51_s15_k2_k2 | Reviewed by the proofreader: Number "42" from the source is missing in the translation; keep every number exactly as written in the source | 42棵81棵15棵 | 15 |
| warning | 52 | p51_s15_k2_k2 | Reviewed by the proofreader: Number "81" from the source is missing in the translation; keep every number exactly as written in the source | 42棵81棵15棵 | 15 |
| warning | 53 | p52_s0 | Reviewed by the proofreader: Number "0" from the source is missing in the translation; keep every number exactly as written in the source | 五加与减（二）212.0.0 | Unit 5 Addition and Subtraction (2) |
| warning | 53 | p52_s0 | Reviewed by the proofreader: Number "212" from the source is missing in the translation; keep every number exactly as written in the source | 五加与减（二）212.0.0 | Unit 5 Addition and Subtraction (2) |
| warning | 63 | p62_s10 | Reviewed by the proofreader: Number "0" from the source is missing in the translation; keep every number exactly as written in the source | 小青收集了多少个252.15.0 | How many bottles did Xiaoqing collect? |
| warning | 63 | p62_s10 | Reviewed by the proofreader: Number "15" from the source is missing in the translation; keep every number exactly as written in the source | 小青收集了多少个252.15.0 | How many bottles did Xiaoqing collect? |
| warning | 63 | p62_s10 | Reviewed by the proofreader: Number "252" from the source is missing in the translation; keep every number exactly as written in the source | 小青收集了多少个252.15.0 | How many bottles did Xiaoqing collect? |
| warning | 63 | p62_s9 | Reviewed by the proofreader: Number "0" from the source is missing in the translation; keep every number exactly as written in the source | 小红收集了多少个？252.14.0 | How many bottles did Xiaohong collect? |
| warning | 63 | p62_s9 | Reviewed by the proofreader: Number "14" from the source is missing in the translation; keep every number exactly as written in the source | 小红收集了多少个？252.14.0 | How many bottles did Xiaohong collect? |
| warning | 63 | p62_s9 | Reviewed by the proofreader: Number "252" from the source is missing in the translation; keep every number exactly as written in the source | 小红收集了多少个？252.14.0 | How many bottles did Xiaohong collect? |
| warning | 64 | p63_s7 | Reviewed by the proofreader: Number "0" from the source is missing in the translation; keep every number exactly as written in the source | (2）256.8.0比256.8.10少7个 | (2) 7 fewer 256.8.0 than 256.8.1. |
| warning | 65 | p64_s29 | Reviewed by the proofreader: Number "0" from the source is missing in the translation; keep every number exactly as written in the source | 6.在260.38.0里填上或 | 6. Fill in each ○ with >, < or =. |
| warning | 65 | p64_s29 | Reviewed by the proofreader: Number "260" from the source is missing in the translation; keep every number exactly as written in the source | 6.在260.38.0里填上或 | 6. Fill in each ○ with >, < or =. |
| warning | 65 | p64_s29 | Reviewed by the proofreader: Number "38" from the source is missing in the translation; keep every number exactly as written in the source | 6.在260.38.0里填上或 | 6. Fill in each ○ with >, < or =. |
| warning | 72 | p71_s0 | Reviewed by the proofreader: Number "0" from the source is missing in the translation; keep every number exactly as written in the source | 六加与减（三）288.0.0288.0.1 | Unit 6 Addition and Subtraction (3) |
| warning | 72 | p71_s0 | Reviewed by the proofreader: Number "1" from the source is missing in the translation; keep every number exactly as written in the source | 六加与减（三）288.0.0288.0.1 | Unit 6 Addition and Subtraction (3) |
| warning | 72 | p71_s0 | Reviewed by the proofreader: Number "288" from the source is missing in the translation; keep every number exactly as written in the source | 六加与减（三）288.0.0288.0.1 | Unit 6 Addition and Subtraction (3) |
| warning | 83 | p82_s8 | Reviewed by the proofreader: Number "0" from the source is missing in the translation; keep every number exactly as written in the source | 百332.8.0十个位位位 | H T O |
| warning | 83 | p82_s8 | Reviewed by the proofreader: Number "332" from the source is missing in the translation; keep every number exactly as written in the source | 百332.8.0十个位位位 | H T O |
| warning | 83 | p82_s8 | Reviewed by the proofreader: Number "8" from the source is missing in the translation; keep every number exactly as written in the source | 百332.8.0十个位位位 | H T O |

### `placeholders` — 0 errors, 286 warnings

| Severity | Page | Segment | Message | Source | Translation |
|---|---|---|---|---|---|
| warning | 1 | p0_s0 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "632.0.0") | 教育部632.0.0审定 | Ministry Approved |
| warning | 6 | p5_s0 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧, ⟦1⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "24.0.0", ⟦1⟧ = "24.0.1") | 一 加与减（一24.0.0）24.0.1 | Unit 1 Addition and Subtraction (1) |
| warning | 6 | p5_s12 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧, ⟦1⟧, ⟦2⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "9", ⟦1⟧ = "6", ⟦2⟧ = "15") | 9再添上6就是15了， | 9 and 6 more makes 15. |
| warning | 6 | p5_s3 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "9") | 我买9支铅笔 | I'll buy 9 pencils. |
| warning | 7 | p6_s1 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "1") | 1.用小棒或计数器做一做，算一算。 | 1. Use sticks or a counting frame, then calculate. |
| warning | 7 | p6_s19 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "5") | 5.说一说，算一算。 | 5. Talk about it, then calculate. |
| warning | 7 | p6_s20 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "9") | 只剩9个松果 | Only 9 pine cones left. |
| warning | 7 | p6_s21 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "17") | 我有17个松果 | I have 17 pine cones. |
| warning | 7 | p6_s4 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "2") | 2.圈一圈，算一算。 | 2. Circle and calculate. |
| warning | 8 | p7_s1 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "13") | 我们一共来了13个人.·· | There are 13 of us altogether… |
| warning | 8 | p7_s14 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "3") | 一3 | −3 |
| warning | 9 | p8_s1 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "1") | 1.用小棒或计数器做一做，算一算。 | 1. Use sticks or a counting frame, then calculate. |
| warning | 9 | p8_s4 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "2") | 2.画一画，填一填。 | 2. Draw and fill in. |
| warning | 9 | p8_s7 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "8") | 还剩8个 | 8 left |
| warning | 10 | p9_s1 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "7") | 7只到河里游泳了。 | 7 went swimming in the river. |
| warning | 10 | p9_s9 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧, ⟦1⟧, ⟦2⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "7", ⟦1⟧ = "5", ⟦2⟧ = "12") | 7加5等于12 | 7 plus 5 equals 12 |
| warning | 11 | p10_s1 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "1") | 1.算一算，用小棒或计数器说明你的计算过程。 | 1. Calculate. Use sticks or a counting frame to show how yo… |
| warning | 11 | p10_s17 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "5") | 5.小熊射门。 | 5. Little Bear shoots at goal. |
| warning | 11 | p10_s4 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "2") | 2.画一画，填一填 | 2. Draw and fill in. |
| warning | 12 | p11_s2 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "7") | 只有7把椅子 | Only 7 chairs |
| warning | 12 | p11_s3 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "1") | 每人坐1把椅子，够吗？ | If each person sits on 1 chair, are there enough chairs? |
| warning | 12 | p11_s7 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "4") | 还缺4把椅子 | We need 4 more chairs. |
| warning | 13 | p12_s3 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧, ⟦1⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "1", ⟦1⟧ = "1") | （1）每个小动物1个苹果，还缺多少个苹果？ | (1) If each animal gets 1 apple, how many more apples are n… |
| warning | 13 | p12_s4 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "2") | (2）再提出一个数学问题，并解答 | (2) Ask another maths question and solve it. |
| warning | 14 | p13_s10 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦2⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦2⟧ = "56.14.2") | 56.14.0比56.14.156.14.2一少几个也就是56.16.0比56.16.1多几个 | How many fewer 56.14.0 than 56.14.1 is the same as how … |
| warning | 15 | p14_s11 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "7") | 我摘了7个桃子 | I picked 7 peaches. |
| warning | 15 | p14_s12 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "16") | 我摘了16个桃子 | I picked 16 peaches. |
| warning | 15 | p14_s2 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧, ⟦1⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "11", ⟦1⟧ = "5") | 昨天生了11个蛋今天只生了5个蛋 | The hens laid 11 eggs yesterday, but only 5 today. |
| warning | 16 | p15_s0 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "3") | 3.谁多？多几只？ | 3. Which group has more? How many more? |
| warning | 16 | p15_s16 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "6") | 6.说一说 | 6. Talk about it. |
| warning | 18 | p17_s12 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "12") | 共有12支 | 12 in total |
| warning | 18 | p17_s13 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "11") | 共有11本 | 11 in total |
| warning | 18 | p17_s7 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "2") | (2）小鹿比小松鼠多几只？ | (2) How many more deer than squirrels? |
| warning | 18 | p17_s8 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "3") | (3）下面列式解决的是什么问题？ | (3) What problem does this number sentence solve? |
| warning | 19 | p18_s1 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "1") | 1.圈一圈，算一算 | 1. Circle and calculate. |
| warning | 19 | p18_s15 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "4") | 4.谁钓得多？ | 4. Who caught more? |
| warning | 19 | p18_s28 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧, ⟦1⟧, ⟦2⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "5", ⟦1⟧ = "1", ⟦2⟧ = "1") | 5. 1把椅子配1张桌子，还缺几张桌子？ | 5. 1 chair goes with 1 table. How many more tables are need… |
| warning | 19 | p18_s4 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "2") | 2.画一画，填一填。 | 2. Draw and fill in. |
| warning | 20 | p19_s21 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "5") | 我踢了5下 | I did 5 kicks. |
| warning | 20 | p19_s22 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "7") | 我踢了7下 | I did 7 kicks. |
| warning | 20 | p19_s24 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "13") | 我踢了13下 | I did 13 kicks. |
| warning | 21 | p20_s1 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "9") | 都是减去9 | All subtract 9. |
| warning | 21 | p20_s18 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "8") | 8的·· | equal 8… |
| warning | 21 | p20_s2 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "12") | 都是12减几 | All start with 12. |
| warning | 21 | p20_s21 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "8") | 减8的算式有 | Subtracting 8: |
| warning | 21 | p20_s3 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "7") | 咦！得数都是7 | Hey! They all equal 7. |
| warning | 23 | p22_s1 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "1") | 1.下面哪幅图是淘气看到的？（画“✓”） | 1. Which picture below does Taoqi see? (Draw "✓") |
| warning | 25 | p24_s2 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "2") | 2.看一看，说一说，下面哪幅图是淘气看到的？哪幅图是笑笑看到的？ | 2. Look and talk. Which picture below does Taoqi see? Which… |
| warning | 25 | p24_s5 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "3") | 3.连一连，说一说 | 3. Match and talk. |
| warning | 27 | p26_s1 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "1") | 1.一个一个地数，数出三十六个花生。 | 1. Count out 36 peanuts one by one. |
| warning | 27 | p26_s4 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "108.4.0") | 九十、八十、七十、108.4.0 | Ninety, eighty, seventy, |
| warning | 27 | p26_s9 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "4") | 4.圈一圈，数一数 | 4. Circle and count. |
| warning | 28 | p27_s3 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧, ⟦1⟧, ⟦2⟧, ⟦3⟧, ⟦4⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "10", ⟦1⟧ = "1", ⟦2⟧ = "1", ⟦3⟧ = "2", ⟦4⟧ = "10") | 10根1捆，1个十、2个十····有10个十 | 10 sticks make 1 bundle. 1 ten, 2 tens… There are 10 tens. |
| warning | 28 | p27_s5 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "10") | 10个十是一百 | 10 tens make 100. |
| warning | 28 | p27_s7 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "10") | 10个小方块是一条。 | 10 small blocks make one strip. |
| warning | 29 | p28_s1 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "1") | 1.圈一圈，数一数，有多少根小棒？ | 1. Circle and count. How many sticks are there? |
| warning | 29 | p28_s2 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "2") | 2.圈一圈，数一数，有多少个小方块？ | 2. Circle and count. How many small blocks are there? |
| warning | 29 | p28_s3 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "3") | 3.圈一圈，数一数，有多少个鸡蛋？ | 3. Circle and count. How many eggs are there? |
| warning | 29 | p28_s4 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "4") | 4.数一数，再添多少就变成一百了？ | 4. Count. How many more are needed to make one hundred? |
| warning | 29 | p28_s8 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "3") | 如图是人们发现的大约3万年前的狼骨，你能看懂古人是怎么计数的吗？ | People found this wolf bone. It is about 30,000 years old. … |
| warning | 30 | p29_s7 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "2") | 有2个十，在十位上拨·· | There are 2 tens, so in the tens place I put… |
| warning | 31 | p30_s1 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "1") | 1.做一做，填一填 | 1. Try it and fill in the blanks. |
| warning | 31 | p30_s18 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧, ⟦1⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "5", ⟦1⟧ = "100") | 5.找找生活中的100 | 5. Find 100 in daily life. |
| warning | 31 | p30_s2 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "2") | 十位上拨2个珠子···· | Put 2 beads in the tens place… |
| warning | 31 | p30_s21 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "100") | 我家住在人民路100号。 | I live at 100 Renmin Road. |
| warning | 31 | p30_s3 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧, ⟦1⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "10", ⟦1⟧ = "2") | 每捆10根，摆2捆，再摆·.· | 10 sticks in each bundle. Put down 2 bundles, then… |
| warning | 31 | p30_s5 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "26") | （）个十和（）个一是26 | ( ) tens and ( ) ones make 26. |
| warning | 32 | p31_s1 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "18") | 我有18个红果 | I have 18 red fruits. |
| warning | 32 | p31_s2 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "21") | 我有21个红果 | I have 21 red fruits. |
| warning | 32 | p31_s5 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧, ⟦1⟧, ⟦2⟧, ⟦3⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "21", ⟦1⟧ = "20", ⟦2⟧ = "18", ⟦3⟧ = "20") | 21比20多18还不到20呢，愚的多 | 21 is more than 20, but 18 is less than 20. So the bear has… |
| warning | 33 | p32_s1 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "1") | 1.比大小 | 1. Compare. |
| warning | 33 | p32_s12 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "3") | 3.连一连 | 3. Match. |
| warning | 33 | p32_s13 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "60") | 欢迎小于60的朋友 | Under 60? Welcome! |
| warning | 33 | p32_s14 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "60") | 欢迎大于60的朋友 | Over 60? Welcome! |
| warning | 33 | p32_s16 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "5") | 5.学校一年级有多少个班？哪个班人数最多？哪个班人数最少？ | 5. How many Grade 1 classes are in your school? Which class… |
| warning | 34 | p33_s10 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧, ⟦1⟧, ⟦2⟧, ⟦3⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "18", ⟦1⟧ = "90", ⟦2⟧ = "97", ⟦3⟧ = "90") | 比18多得多的数有90，97，是90吗？ | 90 and 97 are much more than 18. Is it 90? |
| warning | 34 | p33_s8 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧, ⟦1⟧, ⟦2⟧, ⟦3⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "18", ⟦1⟧ = "26", ⟦2⟧ = "90", ⟦3⟧ = "97") | 18，26，90，97四个数中，有一个是兔子的只数，猜一猜。 | One of the four numbers 18, 26, 90 and 97 is the number of … |
| warning | 34 | p33_s9 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "18") | 比18多得多 | Much more than 18. |
| warning | 35 | p34_s1 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧, ⟦1⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "1", ⟦1⟧ = "86") | 1.跑步的有86人。 | 1. 86 people are running. |
| warning | 35 | p34_s10 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "37") | 我爸爸今年37岁。 | My father is 37 years old this year. |
| warning | 35 | p34_s16 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "28") | 这罐松果有28个。 | This jar has 28 pine cones. |
| warning | 37 | p36_s1 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "1") | 1.在填好的百数表上涂一涂，看一看，和同伴说一说你发现了什么。 | 1. Colour in the completed hundred chart, look at it, and t… |
| warning | 37 | p36_s2 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧, ⟦1⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "1", ⟦1⟧ = "0") | （1）把个位上的数是“0”的涂上绿色。 | (1) Colour green the numbers whose ones digit is "0". |
| warning | 37 | p36_s3 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧, ⟦1⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "2", ⟦1⟧ = "7") | （2）把个位上的数是“7”的涂上蓝色。 | (2) Colour blue the numbers whose ones digit is "7". |
| warning | 37 | p36_s6 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "2") | 2.小熊写门牌号。 | 2. Little Bear writes the house numbers. |
| warning | 37 | p36_s7 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "3") | 3.看一看，填一填 | 3. Look and fill in. |
| warning | 37 | p36_s8 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "4") | 4.想一想，填一填 | 4. Think and fill in. |
| warning | 38 | p37_s1 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "1") | 1.填一填 | 1. Fill in the blanks. |
| warning | 38 | p37_s10 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "4") | 4.按规律填一填。 | 4. Complete the pattern. |
| warning | 38 | p37_s7 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "80") | 我吃了80条 | I ate 80 bugs. |
| warning | 38 | p37_s8 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "64") | 我吃了64条 | I ate 64 bugs. |
| warning | 38 | p37_s9 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "48") | 我吃了48条 | I ate 48 bugs. |
| warning | 39 | p38_s0 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "5") | 5.小鸟回家（连线） | 5. Birds Go Home (Match) |
| warning | 39 | p38_s1 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "50") | 大于50 | Over 50 |
| warning | 39 | p38_s15 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦1⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦1⟧ = "156.22.0") | 有90本吗？156.22.0 | Are there 90? |
| warning | 39 | p38_s17 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "90") | 比90本少一些 | A few fewer than 90. |
| warning | 39 | p38_s2 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "50") | 小于50 | Under 50 |
| warning | 39 | p38_s5 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "38") | 我摘了38个桃子 | I picked 38 peaches. |
| warning | 41 | p40_s12 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "4") | 4.想一想，请你接着画下去。 | 4. Think about it, then continue the pattern. |
| warning | 41 | p40_s5 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "2") | 2.涂一涂。 | 2. Colour in. |
| warning | 42 | p41_s3 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "2") | 把附页图2中的长方形、三角形、圆形的纸分别折成一样的两部分，怎么折？剪一剪，比一比。 | Fold the paper rectangle, triangle and circle in Figure 2 o… |
| warning | 43 | p42_s4 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "3") | 3.你能用一张长方形的纸，折出一个正方形吗？试一试。 | 3. Can you fold a rectangular piece of paper to make a squa… |
| warning | 44 | p43_s2 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧, ⟦1⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "3", ⟦1⟧ = "4") | 宋朝有个叫黄伯思的人发明了一种桌子，可以根据吃饭人数的不同，把桌子拼成不同的形状，比如3人拼成三角形，4人拼成四方形·… | In the Song Dynasty, a man named Huang Bosi invented a tabl… |
| warning | 44 | p43_s4 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧, ⟦1⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "1", ⟦1⟧ = "4") | 说一说，填一填七巧板由种图形组成，其中有—个三角形。1号和号图形、4号和—号图形是完全一样的。 | Talk about it and fill in. The tangram has ___ kinds of sha… |
| warning | 45 | p44_s1 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "1") | 1.拼一拼，想一想，拼出的图形像什么？ | 1. Make these pictures. What does each one look like? |
| warning | 45 | p44_s12 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "4") | 4.发挥你的想象力，用七巧板拼出一个你最喜欢的图形，并展示给同学。 | 4. Use your imagination to make your favourite picture with… |
| warning | 46 | p45_s6 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "8") | 风车的图案是由8个三角形组成的···· | The pinwheel pattern is made of 8 triangles… |
| warning | 47 | p46_s5 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "2") | 2.在点子图上用学过的图形设计一个图案，说一说用到了哪些图形。 | 2. Design a pattern on the dot grid with shapes you know. W… |
| warning | 48 | p47_s11 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "10") | 10个十。 | 10 tens |
| warning | 48 | p47_s13 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧, ⟦1⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "2", ⟦1⟧ = "50") | 2个50 | 2 fifties |
| warning | 48 | p47_s15 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "20") | 找一个比20大的数，像这样说一说。 | Find a number greater than 20 and describe it like this. |
| warning | 49 | p48_s1 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "5") | 我花了很长时间用七巧板中的5块板拼出了一个正方形。 | It took me a long time to make a square with 5 tangram piec… |
| warning | 49 | p48_s9 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧, ⟦1⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "0", ⟦1⟧ = "0") | 妈妈说还有负数，负数是比0还小吗？那怎么可能呢？要这样的数有什么用呢？我怎么也写不出比0小的数。 | Mum says there are also negative numbers. Is a negative num… |
| warning | 50 | p49_s1 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "1") | 1.用小棒或计数器做一做，说说你是怎么算的。 | 1. Work these out with sticks or a counting frame, and say … |
| warning | 50 | p49_s34 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "7") | 吃了7个 | ate 7 cherries |
| warning | 50 | p49_s35 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "7") | 吃了7个 | ate 7 cherries |
| warning | 50 | p49_s6 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "2") | 2.画一画，填一填。 | 2. Draw and fill in. |
| warning | 51 | p50_s0 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "7") | 7.画一画，拨一拨， | 7. Draw and move the beads. |
| warning | 51 | p50_s10 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "10") | 10.踢键子 | 10. Kicking the shuttlecock |
| warning | 51 | p50_s5 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "8") | 8.他们分别看到的是什么？连一连。 | 8. What do they each see? Match. |
| warning | 51 | p50_s6 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "9") | 9.你能用学过的图形拼一个漂亮的图案吗？如果觉得有困难，可以仿照下面的图案拼一个 | 9. Can you make a pretty picture with the shapes you have l… |
| warning | 52 | p51_s0 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧, ⟦1⟧, ⟦2⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "11", ⟦1⟧ = "23", ⟦2⟧ = "32") | 11.笑笑用下面的图表示23，你能用同样的方法表示32吗？ | 11. Xiaoxiao uses the picture below to show 23. Can you sho… |
| warning | 52 | p51_s10 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦2⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦2⟧ = "0") | 13.在208.11.00里填上 | 13. Fill in each 208.11.0 with >, < or =. |
| warning | 52 | p51_s14 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "16") | 有 16 棵杨树 | 16 poplar trees |
| warning | 53 | p52_s0 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "212.0.0") | 五加与减（二）212.0.0 | Unit 5 Addition and Subtraction (2) |
| warning | 53 | p52_s11 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧, ⟦1⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "50", ⟦1⟧ = "40") | 数一数，50，40 | Count: 50, 40. |
| warning | 53 | p52_s12 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧, ⟦1⟧, ⟦2⟧, ⟦3⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "5", ⟦1⟧ = "1", ⟦2⟧ = "4", ⟦3⟧ = "40") | 5个十减1个十得4个十，是40。 | 5 tens minus 1 ten is 4 tens, which is 40. |
| warning | 53 | p52_s5 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧, ⟦1⟧, ⟦2⟧, ⟦3⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "2", ⟦1⟧ = "3", ⟦2⟧ = "5", ⟦3⟧ = "50") | 2个十加3个十得5个十，是50。 | 2 tens and 3 tens make 5 tens, which is 50. |
| warning | 54 | p53_s26 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "5") | 5.提出一个数学问题，并解答 | 5. Make up a maths problem and solve it. |
| warning | 54 | p53_s29 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "40") | 梨40个。 | 40 pears |
| warning | 54 | p53_s5 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "2") | 2.看一看，填一填 | 2. Look and fill in. |
| warning | 55 | p54_s15 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "4") | 个位上拨走4个珠子。 | Take 4 beads off the ones rod. |
| warning | 55 | p54_s8 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "4") | 个位上再拨4个珠子 | Move 4 more beads onto the ones rod. |
| warning | 56 | p55_s1 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "1") | 1.提出一个数学问题，并解答。 | 1. Make up a maths problem and solve it. |
| warning | 56 | p55_s11 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "19") | 原来有19个 | 19 at first |
| warning | 56 | p55_s12 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "2") | 身长2米 | 2 m long |
| warning | 56 | p55_s13 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "25") | 身长25米 | 25 m long |
| warning | 56 | p55_s22 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "5") | 5.想一想，填一填 | 5. Think and fill in. |
| warning | 56 | p55_s4 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "2") | 2.用计数器拨一拨，算一算。 | 2. Work these out on a counting frame. |
| warning | 57 | p56_s10 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "3") | 十位上拨走3个珠子 | Take 3 beads off the tens rod. |
| warning | 57 | p56_s4 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "3") | 十位上再拨3个珠子 | Move 3 more beads onto the tens rod. |
| warning | 58 | p57_s23 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧, ⟦1⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "6", ⟦1⟧ = "1") | 6.每人1瓶水，还差多少瓶水？ | 6. Each person gets 1 bottle of water. How many more bottle… |
| warning | 58 | p57_s6 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "2") | 2.用小棒摆一摆，算一算。 | 2. Show it with sticks, then calculate. |
| warning | 58 | p57_s9 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "3") | 3.看一看，填一填。 | 3. Look and fill in. |
| warning | 59 | p58_s1 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "36") | 我拔了36个萝卜 | I pulled up 36 radishes. |
| warning | 59 | p58_s2 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "23") | 我拔了23个萝卜。 | I pulled up 23 radishes. |
| warning | 60 | p59_s1 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "1") | 1.用计数器拨一拨，算一算。 | 1. Move the beads on a counting frame and calculate. |
| warning | 60 | p59_s12 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "4") | 4.一共有多少只天鹅？ | 4. How many swans are there in total? |
| warning | 60 | p59_s13 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "55") | 有55只天鹅 | 55 swans here. |
| warning | 60 | p59_s14 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "14") | 又飞来14只 | 14 more fly in. |
| warning | 60 | p59_s8 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "3") | 3.用竖式计算。 | 3. Use the column method. |
| warning | 62 | p61_s1 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "1") | 1.用计数器拨一拨，算一算。 | 1. Move the beads on a counting frame and calculate. |
| warning | 62 | p61_s15 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "35") | 我摘了35个桃子 | I picked 35 peaches. |
| warning | 62 | p61_s16 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "47") | 树上原有47个桃子 | The tree had 47 peaches. |
| warning | 62 | p61_s5 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "2") | 2.还有多少个气球没有吹？ | 2. How many balloons haven't been blown up yet? |
| warning | 62 | p61_s7 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "22") | 已经吹好了22个 | 22 already blown up. |
| warning | 62 | p61_s8 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "3") | 3.用竖式计算。 | 3. Use the column method. |
| warning | 63 | p62_s10 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "252.15.0") | 小青收集了多少个252.15.0 | How many bottles did Xiaoqing collect? |
| warning | 63 | p62_s2 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "3") | 我收集的比小林多3个。 | I collected 3 more than Xiaolin. |
| warning | 63 | p62_s3 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "13") | 我收集了13个 | I collected 13 bottles. |
| warning | 63 | p62_s4 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "4") | 我收集的比小林少4个。 | I collected 4 fewer than Xiaolin. |
| warning | 63 | p62_s9 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "252.14.0") | 小红收集了多少个？252.14.0 | How many bottles did Xiaohong collect? |
| warning | 64 | p63_s12 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "47") | 我们班捐了47本书 | Our class donated 47 books. |
| warning | 64 | p63_s3 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "7") | 我比梅花鹿小7岁。 | I'm 7 years younger than the deer. |
| warning | 64 | p63_s4 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "12") | 我今年12岁 | I'm 12 years old. |
| warning | 64 | p63_s5 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "2") | 2.画一画，算一算 | 2. Draw and calculate. |
| warning | 64 | p63_s7 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦3⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦3⟧ = "0") | (2）256.8.0比256.8.10少7个 | (2) 7 fewer 256.8.0 than 256.8.1. |
| warning | 64 | p63_s8 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "3") | 3.笑笑折了多少颗？ | 3. How many stars did Xiaoxiao fold? |
| warning | 65 | p64_s1 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "1") | 1.用计数器拨一拨，算一算。 | 1. Move the beads on a counting frame and calculate. |
| warning | 65 | p64_s6 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "2") | 2.看一看，填一填 | 2. Look and fill in. |
| warning | 66 | p65_s0 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "7") | 7.森林医生。 | 7. Forest Doctor |
| warning | 66 | p65_s12 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "9") | 9.回收废电池 | 9. Recycling used batteries |
| warning | 66 | p65_s13 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "36") | 我的比亮亮多36节 | I have 36 more than Liangliang. |
| warning | 66 | p65_s14 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "12") | 我的比亮亮少12节。 | I have 12 fewer than Liangliang. |
| warning | 66 | p65_s15 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "22") | 我有22节 | I have 22. |
| warning | 66 | p65_s16 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "1") | （1）丽丽回收了多少节？ | (1) How many did Lili recycle? |
| warning | 66 | p65_s18 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "2") | (2）小军回收了多少节？ | (2) How many did Xiaojun recycle? |
| warning | 66 | p65_s21 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧, ⟦1⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "10", ⟦1⟧ = "3") | 10.再写3个算式 | 10. Write 3 more number sentences. |
| warning | 66 | p65_s8 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧, ⟦1⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "20", ⟦1⟧ = "1") | 我有20元买1个还差多少元？ | I have ¥20. To buy 1 |
| warning | 67 | p66_s0 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧, ⟦1⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "11", ⟦1⟧ = "100") | 11.妈妈有100元钱，要买一套衣服，可以怎么买？应付多少元？请你想出一种买法。 | 11. Mum has ¥100 and wants to buy an outfit. What could she… |
| warning | 68 | p67_s9 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "2") | 2.与同伴交流，你有什么新的想法？ | 2. Talk with your partner. What new ideas do you have? |
| warning | 69 | p68_s2 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "1") | 1.比较淘气和笑笑分的结果，你有什么发现？ | 1. Compare how Taoqi and Xiaoxiao sorted. What do you notic… |
| warning | 70 | p69_s10 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "1") | 可以从第三横行开始做，只有1个空格。 | We can start with the third row, which has only 1 blank. |
| warning | 70 | p69_s11 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "3") | （3）接着做下去，说说你是怎么想的。 | (3) Keep going and explain your thinking. |
| warning | 70 | p69_s12 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "3") | 每个数字只能出现一次，这个空格填3。 | Each number can appear only once, so write 3 in this blank. |
| warning | 70 | p69_s4 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "1") | （1）你能看懂游戏规则吗？说一说。 | (1) Can you understand the rules? Explain them. |
| warning | 70 | p69_s5 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧, ⟦1⟧, ⟦2⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "1", ⟦1⟧ = "2", ⟦2⟧ = "3") | 空格里能填1填2、填3。 | Each blank can be 1, 2 or 3. |
| warning | 70 | p69_s9 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "2") | 第一横行有2个空格，怎么填呀？ | The first row has 2 blanks. How do we fill them? |
| warning | 71 | p70_s1 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧, ⟦1⟧, ⟦2⟧, ⟦3⟧, ⟦4⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "1", ⟦1⟧ = "2", ⟦2⟧ = "3", ⟦3⟧ = "4", ⟦4⟧ = "5") | 规则和上面一样，只是空格里可以填1，2，3，4，5中的一个 | Same rules as above, but each blank can be one of 1, 2, 3, … |
| warning | 71 | p70_s2 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦3⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦3⟧ = "2··") | 第一横行第三个格只能填2和4，但第三竖行有4了，所以只能填2·· | The third cell in the first row can only be 2 or 4, but the… |
| warning | 71 | p70_s7 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "56") | 处填上56就可以通过第一关！ | write 56 to pass the first level! |
| warning | 72 | p71_s0 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧, ⟦1⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "288.0.0", ⟦1⟧ = "288.0.1") | 六加与减（三）288.0.0288.0.1 | Unit 6 Addition and Subtraction (3) |
| warning | 72 | p71_s23 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "1") | 满十进1 | Make ten, carry 1. |
| warning | 73 | p72_s15 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "2") | 2.用坚式算一算 | 2. Use the column method. |
| warning | 74 | p73_s2 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "8") | 我比妹妹多摘了8个 | I picked 8 more than my sister. |
| warning | 74 | p73_s20 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "7") | 7.这一排共有 | 7. This row has |
| warning | 74 | p73_s5 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "5") | 5.森林医生。 | 5. Forest Doctor. |
| warning | 75 | p74_s25 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "1") | 个位满十，向十位进1，十位满十·· | When the ones reach ten, carry 1 to the tens; when the tens… |
| warning | 75 | p74_s5 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧, ⟦1⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "38", ⟦1⟧ = "40") | 把38看作40 | Think of 38 as 40. |
| warning | 75 | p74_s7 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦3⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦3⟧ = "20 40+20=60") | 把38看作40，17看作20 40+20=60，装得下。 | Think of 38 as 40 and 17 as 20. 40+20=60, so they fit. |
| warning | 76 | p75_s19 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "4") | 4.森林医生 | 4. Forest Doctor |
| warning | 76 | p75_s2 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "70") | 70颗珠子能穿一条项链。 | 70 beads can make one necklace. |
| warning | 76 | p75_s23 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "60") | 每辆车最多能坐60人，哪两个班合坐一辆车最合适？ | Each bus holds at most 60 people. Which two classes best fi… |
| warning | 76 | p75_s24 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "1") | 一(1）班 | Class 1 (1) |
| warning | 76 | p75_s26 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "(2)") | 一(2)班 | Class 1 (2) |
| warning | 76 | p75_s28 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "(3)") | 二(3)班 | Class 2 (3) |
| warning | 76 | p75_s29 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "(2)") | 二(2)班 | Class 2 (2) |
| warning | 76 | p75_s30 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "1") | 二（1）班 | Class 2 (1) |
| warning | 76 | p75_s31 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "33") | 33人 | 33 students |
| warning | 76 | p75_s34 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "30") | 30人 | 30 students |
| warning | 77 | p76_s1 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "1") | 1.圈一圈，算一算 | 1. Circle and calculate. |
| warning | 77 | p76_s23 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "5") | 5.把茶杯全部放进纸箱里，能装得下吗？ | 5. Will all the teacups fit into the carton? |
| warning | 77 | p76_s4 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "i39+41=") | （根）i39+41= | 39+41= |
| warning | 78 | p77_s12 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "8") | 8.数学游戏 | 8. Maths game |
| warning | 78 | p77_s15 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "1") | （1）每人每次拿两张卡片，将卡片上的数相加，结果要小 | (1) On each turn, take two cards and add the numbers. The s… |
| warning | 78 | p77_s17 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "2") | （2）填表并比较两人每次的得数，把大的得数“圈”起来。 | (2) Fill in the table; each round, circle the larger of the… |
| warning | 78 | p77_s18 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧, ⟦1⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "3", ⟦1⟧ = "5") | （3）连续玩5次，注意拿过的卡片不能再用。谁的“圈”多谁就获胜。 | (3) Play 5 rounds without reusing cards. Whoever has more c… |
| warning | 79 | p78_s13 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧, ⟦1⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "1", ⟦1⟧ = "10") | 十位上1个珠子相当于个位上10个珠子 | 1 bead in the tens place equals 10 beads in the ones place. |
| warning | 80 | p79_s1 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "8") | 我比你少收8个 | I picked 8 fewer than you. |
| warning | 80 | p79_s13 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "2") | 2.想一想，算一算 | 2. Think and calculate. |
| warning | 80 | p79_s2 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "35") | 我收了35个玉米 | I picked 35 ears of corn. |
| warning | 80 | p79_s9 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "1") | 1.用小棒或计数器做一做，算一算。 | 1. Use sticks or a counting frame, then calculate. |
| warning | 81 | p80_s26 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧, ⟦1⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "9", ⟦1⟧ = "1") | 我只有9元钱，要买1本《童话故事》，还差多少元？ | I only have ¥9. I want to buy 1 copy of Fairy Tales. How mu… |
| warning | 82 | p81_s23 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "1") | 个位不够减，向十位借1 | Not enough ones? Borrow 1 ten. |
| warning | 83 | p82_s1 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧, ⟦1⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "100", ⟦1⟧ = "48=") | 100一48=？他们的做法你能看懂吗？ | 100 − 48=? Can you understand their methods? |
| warning | 83 | p82_s14 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "1") | 1.用小棒或计数器做一做，再用竖式算一算。 | 1. Use sticks or a counting frame, then use the column meth… |
| warning | 83 | p82_s19 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧, ⟦1⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "2", ⟦1⟧ = "1") | 2.买1个羽毛球拍多少元？ | 2. How much does 1 badminton racket cost? |
| warning | 83 | p82_s20 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "29") | 找你29元 | ¥29 change. |
| warning | 83 | p82_s21 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "50") | 给您50元 | Here is ¥50. |
| warning | 83 | p82_s8 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "332.8.0") | 百332.8.0十个位位位 | H T O |
| warning | 84 | p83_s0 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "3") | 3.算一算，并说说你的方法。 | 3. Calculate, and explain your method. |
| warning | 84 | p83_s38 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "50") | 最多坐50名乘客 | Up to 50 passengers |
| warning | 84 | p83_s41 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "34") | 我们队有34名运动员 | Our team has 34 athletes. |
| warning | 85 | p84_s1 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "1") | 1.用小棒或计数器做一做，再用竖式算一算。 | 1. Use sticks or a counting frame, then use the column meth… |
| warning | 85 | p84_s5 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "2") | 2.森林医生。 | 2. Forest Doctor. |
| warning | 86 | p85_s1 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "25") | 我已经吃了25个 | I've already eaten 25. |
| warning | 86 | p85_s17 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "100") | 我有100张 | I have 100. |
| warning | 86 | p85_s18 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "16") | 我比欢欢少16张 | I have 16 fewer than Huanhuan. |
| warning | 86 | p85_s19 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "9") | 我比乐乐多9张 | I have 9 more than Lele. |
| warning | 86 | p85_s2 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "42") | 原来有42个 | 42 at first |
| warning | 86 | p85_s4 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "24") | 我今年24岁 | I'm 24 years old. |
| warning | 86 | p85_s5 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "9") | 我今年9岁。 | I'm 9 years old. |
| warning | 86 | p85_s7 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "6") | 6.画出晓跷板。 | 6. Draw the seesaws. |
| warning | 87 | p86_s0 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "8") | 8.得数排队 | 8. Order the answers |
| warning | 87 | p86_s16 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧, ⟦1⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "1", ⟦1⟧ = "50") | （1）小明有50元钱，可以买哪三个玩具？把这三个玩具圈起来尔 | (1) Xiaoming has ¥50. Which three toys can he buy? Circle t… |
| warning | 87 | p86_s17 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "2") | （2）一辆小汽车比一个布娃娃贵多少元？ | (2) How much more does a toy car cost than a doll? |
| warning | 87 | p86_s18 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧, ⟦1⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "3", ⟦1⟧ = "64") | （3）小亮买了一辆小汽车，售货员找回64元，他给了售货员多少元？ | (3) Xiaoliang bought a toy car and got ¥64 change. How much… |
| warning | 87 | p86_s19 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "4") | （4）再提出一个数学问题，并解答 | (4) Ask another maths question and solve it. |
| warning | 88 | p87_s11 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "5") | 5.把你经常出错的题目写下来，说一说计算中应该注意什么。 | 5. List problems you often get wrong and say what to watch … |
| warning | 88 | p87_s13 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "7") | 7.提出一个数学问题，并解答。 | 7. Pose a maths problem and solve it. |
| warning | 88 | p87_s15 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "61") | 我吃了61只害虫。 | I ate 61 pests. |
| warning | 88 | p87_s16 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "18") | 我比你少吃了18只害虫。 | I ate 18 fewer pests than you. |
| warning | 88 | p87_s18 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "32") | 我会这样表示32。 | I can show 32 like this. |
| warning | 88 | p87_s19 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "100") | 我认识了100，还能两个两个地 | I know numbers up to 100 and can count |
| warning | 88 | p87_s20 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧, ⟦1⟧, ⟦2⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "2", ⟦1⟧ = "4", ⟦2⟧ = "6") | 数，2，4，6， | by twos: 2, 4, 6, |
| warning | 88 | p87_s3 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "1") | 1.你认识了哪些数？能按顺序数一数吗？ | 1. What numbers do you know? Can you count them in order? |
| warning | 88 | p87_s4 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧, ⟦1⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "2", ⟦1⟧ = "32") | 2.你能用几种不同的方法表示32这个数？ | 2. How many different ways can you show the number 32? |
| warning | 88 | p87_s5 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "3") | 3.怎样比较两个数的大小？举例说一说。 | 3. How do you compare two numbers? Give an example. |
| warning | 88 | p87_s6 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "4") | 4.用竖式计算，并利用小棒或计数器说说你是怎么计算的。 | 4. Use the column method, then explain how with sticks or a… |
| warning | 89 | p88_s2 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "1") | 1.这学期你学过哪些图形？用自己的语言说一说，你学过的图形都是什么样子的？并试着画一画。 | 1. Which shapes have you learned this term? Describe them i… |
| warning | 89 | p88_s3 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "2") | 2.下面的图案分别是由哪些图形组成的？你能设计出一幅有趣的图案吗？ | 2. Which shapes make up each pattern below? Can you design … |
| warning | 90 | p89_s12 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "3") | 3.连一连 | 3. Match. |
| warning | 90 | p89_s13 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧, ⟦1⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "1", ⟦1⟧ = "30") | 1~30的数 | 1 to 30 |
| warning | 90 | p89_s14 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧, ⟦1⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "31", ⟦1⟧ = "60") | 31~60的数 | 31 to 60 |
| warning | 90 | p89_s15 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧, ⟦1⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "61", ⟦1⟧ = "100") | 61~100的数 | 61 to 100 |
| warning | 90 | p89_s2 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "1") | 1.填一填 | 1. Fill in the blanks. |
| warning | 90 | p89_s5 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "2") | 2.看一看，填一填 | 2. Look and fill in. |
| warning | 91 | p90_s16 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧, ⟦1⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "27", ⟦1⟧ = "15") | 河里有一群鸭，小鸭有27只，大鸭比小鸭少15只，大鸭有多少只？ | A group of ducks is on the river. There are 27 ducklings, a… |
| warning | 91 | p90_s17 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "8") | 8.算一算，说一说 | 8. Calculate and discuss. |
| warning | 92 | p91_s0 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧, ⟦1⟧, ⟦2⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "9", ⟦1⟧ = "3", ⟦2⟧ = "50") | 9.少年宫组织两队同学参加夏令营，每队有3位老师，每辆车可坐50名乘客。 | 9. Two groups go to summer camp. Each group has 3 teachers,… |
| warning | 92 | p91_s11 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "11") | 11.运木头。 | 11. Moving logs. |
| warning | 92 | p91_s13 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "1") | （1）一共运了多少根？ | (1) How many logs in all? |
| warning | 92 | p91_s19 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "23") | 23张 | 23 cards |
| warning | 92 | p91_s20 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "38") | 38张 | 38 cards |
| warning | 92 | p91_s21 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "92") | 92张 | 92 cards |
| warning | 92 | p91_s27 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "3") | (3）再提出一个数学问题，并试着解答。 | (3) Ask another maths question and try to answer it. |
| warning | 93 | p92_s0 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "13") | 13.套圈游戏。 | 13. Ring toss game. |
| warning | 93 | p92_s20 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "2") | (2）最多的跳—下，最少的跳—下，相差—下。 | (2) Most: ___ skips. Fewest: ___ skips. Difference: ___. |
| warning | 93 | p92_s23 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "4") | （4）第四名再跳—下，就和第三名同样多。 | (4) Fourth place needs ___ more skips to match third place. |
| warning | 93 | p92_s24 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "5") | （5）再提出一个数学问题，并试着解答。 | (5) Ask another maths question and try to answer it. |
| warning | 93 | p92_s6 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "2") | (2）妙想可能套中哪两个？ | (2) Which two could Miaoxiang have ringed? |
| warning | 94 | p93_s1 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "1") | 1.找一找。 | 1. Find and count. |
| warning | 94 | p93_s10 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧, ⟦1⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "3", ⟦1⟧ = "4") | 3.用附页图4中的长方形纸折一折。 | 3. Fold the paper rectangle in Figure 4 of the appendix. |
| warning | 94 | p93_s13 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "3") | （3）把它分成一个正方形和一个长方形。 | (3) Divide it into one square and one rectangle. |
| warning | 94 | p93_s14 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "4") | 4.你能仿照下图用学过的平面图形拼图吗？ | 4. Can you make a picture like the one below with the flat … |
| warning | 94 | p93_s9 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "2") | 2.下面每幅图分别是谁看到的？连一连 | 2. Who sees each picture below? Match. |
