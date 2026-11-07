# QA report

**Result:** QA FAILED after 3 rounds: 2 errors, 505 warnings (1303.3 s); proofread: 2129 corrections applied; output file checks: 0 error(s)

**Document:** 数学 (zh → en, 109 page(s), 1240 translatable segment(s))

**Checks run:** `completeness`, `placeholders`, `numbers`, `untranslated`, `target_script`, `glossary`, `length_ratio`, `formatting`, `layout_fit`, `image_text`, `llm_review`, `output_checks`

## Rounds

| Round | Errors | Warnings | Re-translated | Passed | Duration |
|---|---|---|---|---|---|
| 1 | 237 | 205 | 208 segment(s) | no | 308.9 s |
| 2 | 186 | 239 | 169 segment(s) | no | 323.2 s |
| 3 | 186 | 192 | 0 segment(s) | no | 109.8 s |

- Round 1: llm_review ×287, layout_fit ×85, glossary ×37, formatting ×23, image_text ×8, completeness ×1, numbers ×1
- Round 2: llm_review ×328, layout_fit ×78, image_text ×8, formatting ×6, glossary ×3, placeholders ×2
- Round 3: llm_review ×274, layout_fit ×76, glossary ×10, image_text ×8, formatting ×5, completeness ×2, length_ratio ×1, placeholders ×1, untranslated ×1

## Final issues (507)

### `layout_fit` — 2 errors, 6 warnings

| Severity | Page | Segment | Message | Source | Translation |
|---|---|---|---|---|---|
| error | 99 | p98_s10 | Shorten the translation to at most 5 characters so it fits the original box (the current translation of 8 characters overflows its box; the minimum allowed size is 55%) | 饼干 | Biscuits |
| error | 99 | p98_s10 | Shorten the translation to at most 5 characters so it fits the original box (the current translation of 8 characters overflows its box; the minimum allowed size is 55%) | 饼干 | Biscuits |
| warning | 9 | p8_s5 | Reviewed by the proofreader: Shorten the translation to at most 6 characters so it fits the original box (the current translation of 8 characters overflows its box; the minimum allowed size is 55%) | 练一缘 | Practice |
| warning | 9 | p8_s5 | Reviewed by the proofreader: Shorten the translation to at most 6 characters so it fits the original box (the current translation of 8 characters overflows its box; the minimum allowed size is 55%) | 练一缘 | Practice |
| warning | 26 | p25_s2 | Reviewed by the proofreader: Shorten the translation to at most 19 characters so it fits the original box (the current translation of 26 characters overflows its box; the minimum allowed size is 55%) | 100.2.l比100.2.0重 | is heavier than the tiger. |
| warning | 26 | p25_s2 | Reviewed by the proofreader: Shorten the translation to at most 19 characters so it fits the original box (the current translation of 26 characters overflows its box; the minimum allowed size is 55%) | 100.2.l比100.2.0重 | is heavier than the tiger. |
| warning | 26 | p25_s5_k0 | Reviewed by the proofreader: Shorten the translation to at most 10 characters so it fits the original box (the current translation of 12 characters overflows its box; the minimum allowed size is 55%) | 最重， | is heaviest, |
| warning | 26 | p25_s5_k0 | Reviewed by the proofreader: Shorten the translation to at most 10 characters so it fits the original box (the current translation of 12 characters overflows its box; the minimum allowed size is 55%) | 最重， | is heaviest, |

### `completeness` — 0 errors, 121 warnings

| Severity | Page | Segment | Message | Source | Translation |
|---|---|---|---|---|---|
| warning | 1 | p0_s7 | Reviewed by the proofreader: The segment has no translation; translate the complete source text | 米2 |  |
| warning | 3 | p2_s7 | Reviewed by the proofreader: The segment has no translation; translate the complete source text | 30元 |  |
| warning | 4 | p3_s2 | Reviewed by the proofreader: The segment has no translation; translate the complete source text | 新国 |  |
| warning | 6 | p5_s1 | Reviewed by the proofreader: The segment has no translation; translate the complete source text | 迎新同 |  |
| warning | 6 | p5_s2 | Reviewed by the proofreader: The segment has no translation; translate the complete source text | 欢 |  |
| warning | 6 | p5_s3 | Reviewed by the proofreader: The segment has no translation; translate the complete source text | 学 |  |
| warning | 12 | p11_s5 | Reviewed by the proofreader: The segment has no translation; translate the complete source text | 第44.11.0节第44.11.1节第44.11.2节第44.11.3节第44.11.4节 |  |
| warning | 13 | p12_s7 | Reviewed by the proofreader: The segment has no translation; translate the complete source text | mmmmlmm mmka |  |
| warning | 16 | p15_s3 | Reviewed by the proofreader: The segment has no translation; translate the complete source text | 亭台六七座八九十枝花 |  |
| warning | 19 | p18_s17 | Reviewed by the proofreader: The segment has no translation; translate the complete source text | 的少 |  |
| warning | 19 | p18_s3 | Reviewed by the proofreader: The translation "." contains no words; translate the complete source text | 一样多。 | . |
| warning | 25 | p24_s12 | Reviewed by the proofreader: The segment has no translation; translate the complete source text | 号 |  |
| warning | 25 | p24_s9 | Reviewed by the proofreader: The segment has no translation; translate the complete source text | 最长的画最短的画 |  |
| warning | 26 | p25_s10 | Reviewed by the proofreader: The segment has no translation; translate the complete source text | 轻 |  |
| warning | 26 | p25_s11 | Reviewed by the proofreader: The segment has no translation; translate the complete source text | 重 |  |
| warning | 26 | p25_s4 | Reviewed by the proofreader: The segment has no translation; translate the complete source text | 100.4.0轻 |  |
| warning | 33 | p32_s3 | Reviewed by the proofreader: The segment has no translation; translate the complete source text | 000Og |  |
| warning | 34 | p33_s5 | Reviewed by the proofreader: The segment has no translation; translate the complete source text | 条。 |  |
| warning | 37 | p36_s10 | Reviewed by the proofreader: The segment has no translation; translate the complete source text | 三 |  |
| warning | 37 | p36_s12 | Reviewed by the proofreader: The segment has no translation; translate the complete source text | 5-5日 |  |
| warning | 37 | p36_s6 | Reviewed by the proofreader: The segment has no translation; translate the complete source text | 目5-2日 |  |
| warning | 39 | p38_s4 | Reviewed by the proofreader: The segment has no translation; translate the complete source text | 放在2个盘子里，可以怎么放？ |  |
| warning | 41 | p40_s3 | Reviewed by the proofreader: The segment has no translation; translate the complete source text | ，可以怎么分？ |  |
| warning | 44 | p43_s1 | Reviewed by the proofreader: The segment has no translation; translate the complete source text | Ma |  |
| warning | 55 | p54_s21 | Reviewed by the proofreader: The segment has no translation; translate the complete source text | 6一 |  |
| warning | 56 | p55_s9 | Reviewed by the proofreader: The segment has no translation; translate the complete source text | 画 |  |
| warning | 58 | p57_a2_p0 | Reviewed by the proofreader: The segment has no translation; translate the complete source text | 。 |  |
| warning | 59 | p58_s5 | Reviewed by the proofreader: The translation ":" contains no words; translate the complete source text | 有 | : |
| warning | 59 | p58_s6 | Reviewed by the proofreader: The translation ":" contains no words; translate the complete source text | 有 | : |
| warning | 60 | p59_s1 | Reviewed by the proofreader: The segment has no translation; translate the complete source text | 能跳到哪个上236.1.0？ |  |
| warning | 63 | p62_a17_p0 | Reviewed by the proofreader: The segment has no translation; translate the complete source text | 文 |  |
| warning | 63 | p62_a18_p0 | Reviewed by the proofreader: The segment has no translation; translate the complete source text | 文 |  |
| warning | 63 | p62_a19_p0 | Reviewed by the proofreader: The segment has no translation; translate the complete source text | 学 |  |
| warning | 63 | p62_a20_p0 | Reviewed by the proofreader: The segment has no translation; translate the complete source text | 学 |  |
| warning | 63 | p62_a21_p0 | Reviewed by the proofreader: The segment has no translation; translate the complete source text | 习本 |  |
| warning | 67 | p66_s15 | Reviewed by the proofreader: The segment has no translation; translate the complete source text | 动物园 |  |
| warning | 67 | p66_s16_k1 | Reviewed by the proofreader: The segment has no translation; translate the complete source text | 路 |  |
| warning | 67 | p66_s16_k2 | Reviewed by the proofreader: The segment has no translation; translate the complete source text | 广场 |  |
| warning | 67 | p66_s17 | Reviewed by the proofreader: The segment has no translation; translate the complete source text | 公园 |  |
| warning | 68 | p67_a2_p0 | Reviewed by the proofreader: The translation "." contains no words; translate the complete source text | 的___面， | . |
| warning | 68 | p67_a4_p0 | Reviewed by the proofreader: The translation "." contains no words; translate the complete source text | 的___面， | . |
| warning | 68 | p67_a6_p0 | Reviewed by the proofreader: The translation "." contains no words; translate the complete source text | 的___面， | . |
| warning | 68 | p67_a8_p0 | Reviewed by the proofreader: The translation "." contains no words; translate the complete source text | 的___面， | . |
| warning | 68 | p67_s10 | Reviewed by the proofreader: The segment has no translation; translate the complete source text | 面 |  |
| warning | 68 | p67_s11 | Reviewed by the proofreader: The segment has no translation; translate the complete source text | 在 |  |
| warning | 68 | p67_s12 | Reviewed by the proofreader: The segment has no translation; translate the complete source text | 的 |  |
| warning | 68 | p67_s13 | Reviewed by the proofreader: The segment has no translation; translate the complete source text | 面 |  |
| warning | 68 | p67_s4 | Reviewed by the proofreader: The segment has no translation; translate the complete source text | 在的面 |  |
| warning | 68 | p67_s5 | Reviewed by the proofreader: The segment has no translation; translate the complete source text | 在 |  |
| warning | 68 | p67_s6 | Reviewed by the proofreader: The segment has no translation; translate the complete source text | 的 |  |
| warning | 68 | p67_s7 | Reviewed by the proofreader: The segment has no translation; translate the complete source text | 面 |  |
| warning | 68 | p67_s8 | Reviewed by the proofreader: The segment has no translation; translate the complete source text | 在 |  |
| warning | 68 | p67_s9 | Reviewed by the proofreader: The segment has no translation; translate the complete source text | 的 |  |
| warning | 69 | p68_a2_p0 | Reviewed by the proofreader: The translation "." contains no words; translate the complete source text | 的___面， | . |
| warning | 69 | p68_a4_p0 | Reviewed by the proofreader: The translation "." contains no words; translate the complete source text | 的___面， | . |
| warning | 69 | p68_a6_p0 | Reviewed by the proofreader: The translation "." contains no words; translate the complete source text | 的___面， | . |
| warning | 69 | p68_a8_p0 | Reviewed by the proofreader: The translation "." contains no words; translate the complete source text | 的___面， | . |
| warning | 69 | p68_s2 | Reviewed by the proofreader: The segment has no translation; translate the complete source text | 在馨272.2.0的——面馨在272.8.0一的— |  |
| warning | 69 | p68_s3 | Reviewed by the proofreader: The segment has no translation; translate the complete source text | 面 |  |
| warning | 69 | p68_s4 | Reviewed by the proofreader: The segment has no translation; translate the complete source text | 在 |  |
| warning | 69 | p68_s5 | Reviewed by the proofreader: The segment has no translation; translate the complete source text | 的_ |  |
| warning | 69 | p68_s6 | Reviewed by the proofreader: The segment has no translation; translate the complete source text | 面 |  |
| warning | 69 | p68_s7 | Reviewed by the proofreader: The segment has no translation; translate the complete source text | 在272.11.0的 |  |
| warning | 69 | p68_s8 | Reviewed by the proofreader: The segment has no translation; translate the complete source text | 面 |  |
| warning | 71 | p70_a8_p0 | Reviewed by the proofreader: The translation "." contains no words; translate the complete source text | 的右边。 | . |
| warning | 71 | p70_s14 | Reviewed by the proofreader: The segment has no translation; translate the complete source text | 4.从右数，共有(）辆车。请画图试一试。 |  |
| warning | 71 | p70_s15 | Reviewed by the proofreader: The segment has no translation; translate the complete source text | 是第5辆，一 |  |
| warning | 71 | p70_s3 | Reviewed by the proofreader: The segment has no translation; translate the complete source text | 把在 |  |
| warning | 71 | p70_s5 | Reviewed by the proofreader: The segment has no translation; translate the complete source text | 放在的右边。 |  |
| warning | 71 | p70_s7 | Reviewed by the proofreader: The segment has no translation; translate the complete source text | 的下面，把放在 |  |
| warning | 71 | p70_s9 | Reviewed by the proofreader: The segment has no translation; translate the complete source text | 的左边，把一280.9.0放 |  |
| warning | 72 | p71_s17 | Reviewed by the proofreader: The translation "." contains no words; translate the complete source text | 的下面 | . |
| warning | 72 | p71_s2 | Reviewed by the proofreader: The segment has no translation; translate the complete source text | 自284.2.0葬自信自强自立 |  |
| warning | 72 | p71_s20 | Reviewed by the proofreader: The segment has no translation; translate the complete source text | 在 |  |
| warning | 73 | p72_s16 | Reviewed by the proofreader: The segment has no translation; translate the complete source text | ns. |  |
| warning | 84 | p83_s8 | Reviewed by the proofreader: The segment has no translation; translate the complete source text | 8+9元 |  |
| warning | 85 | p84_s1 | Reviewed by the proofreader: The segment has no translation; translate the complete source text | mmhwn |  |
| warning | 85 | p84_s2 | Reviewed by the proofreader: The segment has no translation; translate the complete source text | mmy |  |
| warning | 88 | p87_s16 | Reviewed by the proofreader: The segment has no translation; translate the complete source text | 7+8元 |  |
| warning | 88 | p87_s42 | Reviewed by the proofreader: The segment has no translation; translate the complete source text | 十+ |  |
| warning | 89 | p88_a10_p0 | Reviewed by the proofreader: The translation "," contains no words; translate the complete source text | 级台阶， | , |
| warning | 89 | p88_a12_p0 | Reviewed by the proofreader: The translation "," contains no words; translate the complete source text | 级台阶， | , |
| warning | 89 | p88_a14_p0 | Reviewed by the proofreader: The translation "," contains no words; translate the complete source text | 级台阶， | , |
| warning | 89 | p88_a16_p0 | Reviewed by the proofreader: The translation "," contains no words; translate the complete source text | 级台阶， | , |
| warning | 89 | p88_a18_p0 | Reviewed by the proofreader: The translation "," contains no words; translate the complete source text | 级 | , |
| warning | 89 | p88_a2_p0 | Reviewed by the proofreader: The translation "," contains no words; translate the complete source text | 级台阶， | , |
| warning | 89 | p88_a4_p0 | Reviewed by the proofreader: The translation "," contains no words; translate the complete source text | 级台阶， | , |
| warning | 89 | p88_a6_p0 | Reviewed by the proofreader: The translation "," contains no words; translate the complete source text | 级台阶， | , |
| warning | 89 | p88_a8_p0 | Reviewed by the proofreader: The translation "," contains no words; translate the complete source text | 级台阶， | , |
| warning | 89 | p88_s2 | Reviewed by the proofreader: The segment has no translation; translate the complete source text | 在第—级台阶，在第—级台阶，在第—级台阶，在第_在第—级台阶，在第——级台阶，在第_级台阶，只在第_级台阶，站在第9级… |  |
| warning | 89 | p88_s3 | Reviewed by the proofreader: The segment has no translation; translate the complete source text | 级台阶，从在第 |  |
| warning | 89 | p88_s4 | Reviewed by the proofreader: The segment has no translation; translate the complete source text | 级台阶， |  |
| warning | 93 | p92_s2 | Reviewed by the proofreader: The segment has no translation; translate the complete source text | 有 |  |
| warning | 93 | p92_s5 | Reviewed by the proofreader: The segment has no translation; translate the complete source text | 有 |  |
| warning | 94 | p93_s5 | Reviewed by the proofreader: The segment has no translation; translate the complete source text | 10个物体都要用上。堆出的作品要有创意。 |  |
| warning | 96 | p95_s9 | Reviewed by the proofreader: The segment has no translation; translate the complete source text | ii ip |  |
| warning | 97 | p96_s4 | Reviewed by the proofreader: The segment has no translation; translate the complete source text | 农 |  |
| warning | 97 | p96_s5 | Reviewed by the proofreader: The segment has no translation; translate the complete source text | 场小 |  |
| warning | 97 | p96_s6 | Reviewed by the proofreader: The segment has no translation; translate the complete source text | 学 |  |
| warning | 99 | p98_s13 | Reviewed by the proofreader: The translation "." contains no words; translate the complete source text | 的右边 | . |
| warning | 99 | p98_s22 | Reviewed by the proofreader: The segment has no translation; translate the complete source text | 的左边是 |  |
| warning | 99 | p98_s3 | Reviewed by the proofreader: The segment has no translation; translate the complete source text | 都 |  |
| warning | 99 | p98_s8_k2 | Reviewed by the proofreader: The segment has no translation; translate the complete source text | 思考 |  |
| warning | 100 | p99_a1_p0 | Reviewed by the proofreader: The translation "." contains no words; translate the complete source text | 个。 | . |
| warning | 100 | p99_s7 | Reviewed by the proofreader: The segment has no translation; translate the complete source text | 数， |  |
| warning | 101 | p100_s25 | Reviewed by the proofreader: The segment has no translation; translate the complete source text | C cccecccccccececcececccccc |  |
| warning | 104 | p103_a2_p0 | Reviewed by the proofreader: The translation ": ( )." contains no words; translate the complete source text | 有( )个， | : ( ). |
| warning | 104 | p103_s10 | Reviewed by the proofreader: The translation ":" contains no words; translate the complete source text | 有 | : |
| warning | 104 | p103_s11 | Reviewed by the proofreader: The translation "." contains no words; translate the complete source text | 个 | . |
| warning | 104 | p103_s14_k0 | Reviewed by the proofreader: The translation ": ( )." contains no words; translate the complete source text | 有()个 | : ( ). |
| warning | 104 | p103_s14_k1 | Reviewed by the proofreader: The translation ": ( )." contains no words; translate the complete source text | 有(）个， | : ( ). |
| warning | 104 | p103_s15_k0 | Reviewed by the proofreader: The segment has no translation; translate the complete source text | 有 |  |
| warning | 104 | p103_s15_k1 | Reviewed by the proofreader: The segment has no translation; translate the complete source text | 不 |  |
| warning | 104 | p103_s16 | Reviewed by the proofreader: The translation ": ( )." contains no words; translate the complete source text | 有个 | : ( ). |
| warning | 104 | p103_s3 | Reviewed by the proofreader: The translation ":" contains no words; translate the complete source text | 有 | : |
| warning | 104 | p103_s4 | Reviewed by the proofreader: The translation "." contains no words; translate the complete source text | 个 | . |
| warning | 104 | p103_s5 | Reviewed by the proofreader: The translation ":" contains no words; translate the complete source text | 有 | : |
| warning | 104 | p103_s6 | Reviewed by the proofreader: The translation "." contains no words; translate the complete source text | 个 | . |
| warning | 104 | p103_s7 | Reviewed by the proofreader: The translation ":" contains no words; translate the complete source text | 有 | : |
| warning | 104 | p103_s8 | Reviewed by the proofreader: The translation "." contains no words; translate the complete source text | 个 | . |
| warning | 104 | p103_s9 | Reviewed by the proofreader: The segment has no translation; translate the complete source text | 有 |  |

### `formatting` — 0 errors, 41 warnings

| Severity | Page | Segment | Message | Source | Translation |
|---|---|---|---|---|---|
| warning | 6 | p5_a4_p0 | The source does not end with a exclamation mark; do not end the translation with one | 学 | mates! |
| warning | 7 | p6_s0 | Reviewed by the proofreader: Start the translation with the list marker "(2）" exactly as in the source | (2）班 | Class 2 |
| warning | 12 | p11_s1 | Reviewed by the proofreader: The source does not end with a question mark; do not end the translation with one | 1.写数。 | 1. How many? |
| warning | 18 | p17_s2 | The source does not end with a exclamation mark; do not end the translation with one | 样多，够了 | Just enough! |
| warning | 19 | p18_a1_p0 | Reviewed by the proofreader: Keep the symbol(s) ○ of the source in the translation, at the matching position | 画○，○比 | Draw more ○ than |
| warning | 19 | p18_s11 | Reviewed by the proofreader: Remove the symbol(s) ○ ✓: they are not in the source (a picture in the book is not a symbol; leave it out rather than inventing one) | 3.比一比，最多的画，最少的画 | 3. Compare. Draw "✓" for the most and "○" for the fewest. |
| warning | 19 | p18_s2 | Reviewed by the proofreader: Remove the symbol(s) □: they are not in the source (a picture in the book is not a symbol; leave it out rather than inventing one) | 每，和 | Draw as many □ as |
| warning | 19 | p18_s7 | Reviewed by the proofreader: Remove the symbol(s) ✓: they are not in the source (a picture in the book is not a symbol; leave it out rather than inventing one) | 2.哪一堆正合适？画 | 2. Which pile is just right? Draw "✓". |
| warning | 21 | p20_s4 | Reviewed by the proofreader: Remove the symbol(s) ○: they are not in the source (a picture in the book is not a symbol; leave it out rather than inventing one) | 2.多的画“✓”，少的画 | 2. Draw "✓" for the one with more and "○" for the one with … |
| warning | 22 | p21_s3 | Reviewed by the proofreader: Remove the symbol(s) ○ ✓: they are not in the source (a picture in the book is not a symbol; leave it out rather than inventing one) | 哪杯装得最多？最多的画”，最少的画 | Which glass holds the most? Draw "✓" for the most and "○" f… |
| warning | 23 | p22_s1 | Reviewed by the proofreader: Remove the symbol(s) ○ ✓: they are not in the source (a picture in the book is not a symbol; leave it out rather than inventing one) | 1.大的画，小的画 | 1. Draw "✓" for the bigger one and "○" for the smaller one. |
| warning | 23 | p22_s3 | Reviewed by the proofreader: Remove the symbol(s) ○: they are not in the source (a picture in the book is not a symbol; leave it out rather than inventing one) | 2.最大的画“✓”，最小的画 | 2. Draw "✓" for the biggest one and "○" for the smallest on… |
| warning | 23 | p22_s5 | Reviewed by the proofreader: Remove the symbol(s) ○ ✓: they are not in the source (a picture in the book is not a symbol; leave it out rather than inventing one) | 3.哪个装得多？多的画少的画 | 3. Which holds more? Draw "✓" for more and "○" for less. |
| warning | 23 | p22_s8 | Reviewed by the proofreader: Remove the symbol(s) ✓: they are not in the source (a picture in the book is not a symbol; leave it out rather than inventing one) | 5.想一想，把方糖放进杯子后，哪杯水最甜？画 | 5. Think: with the sugar cubes in, which glass is the sweet… |
| warning | 25 | p24_s2 | Reviewed by the proofreader: Remove the symbol(s) ✓: they are not in the source (a picture in the book is not a symbol; leave it out rather than inventing one) | 2.哪根绳子最长？画 | 2. Which rope is the longest? Draw "✓". |
| warning | 27 | p26_s1 | Reviewed by the proofreader: Keep the symbol(s) √ of the source in the translation, at the matching position | 1.轻的画√”，重的画 | 1. Draw "✓" for the lighter one and "○" for the heavier one. |
| warning | 27 | p26_s1 | Reviewed by the proofreader: Remove the symbol(s) ○ ✓: they are not in the source (a picture in the book is not a symbol; leave it out rather than inventing one) | 1.轻的画√”，重的画 | 1. Draw "✓" for the lighter one and "○" for the heavier one. |
| warning | 27 | p26_s4 | Reviewed by the proofreader: Remove the symbol(s) ○ ✓: they are not in the source (a picture in the book is not a symbol; leave it out rather than inventing one) | 2.最轻的画，最重的画 | 2. Draw "✓" for the lightest and "○" for the heaviest. |
| warning | 27 | p26_s7 | Reviewed by the proofreader: Remove the symbol(s) ✓: they are not in the source (a picture in the book is not a symbol; leave it out rather than inventing one) | 3.在重的一边画 | 3. Draw "✓" on the heavier side. |
| warning | 27 | p26_s8 | Reviewed by the proofreader: Remove the symbol(s) ○ ✓: they are not in the source (a picture in the book is not a symbol; leave it out rather than inventing one) | 最轻的画”，最重的画“” | Draw "✓" for the lightest and "○" for the heaviest. |
| warning | 35 | p34_s1 | Reviewed by the proofreader: The source does not end with a question mark; do not end the translation with one | 1.还有几个136.1.0 | 1. How many 136.1.0 are left? |
| warning | 46 | p45_s5 | Reviewed by the proofreader: The source does not end with a question mark; do not end the translation with one | 3.房子里有几只 | 3. How many rabbits are inside? |
| warning | 56 | p55_s11 | Reviewed by the proofreader: The source ends with a question mark; end the translation with a question mark too | 说一说，3在生活中可以表示什么？0呢？ | Talk about it. What can 3 mean in everyday life? What about… |
| warning | 58 | p57_s23 | Reviewed by the proofreader: Remove the symbol(s) ○: they are not in the source (a picture in the book is not a symbol; leave it out rather than inventing one) | 5.比一比，重的画“✓”，轻的画 | 5. Compare. Draw "✓" for the heavier one and "○" for the li… |
| warning | 59 | p58_s1 | Reviewed by the proofreader: Remove the symbol(s) ○ ✓: they are not in the source (a picture in the book is not a symbol; leave it out rather than inventing one) | 爬得最高的画最低的画 | Draw "✓" for the one that climbed highest and "○" for the l… |
| warning | 59 | p58_s9 | Reviewed by the proofreader: Remove the symbol(s) ○: they are not in the source (a picture in the book is not a symbol; leave it out rather than inventing one) | 还剩几个？ | How many ○ left? |
| warning | 60 | p59_s0 | Reviewed by the proofreader: The source does not end with a question mark; do not end the translation with one | 9.画一画，心236.0.0 | 9. Draw. Which lily pad can each frog jump onto? |
| warning | 62 | p61_s2 | Reviewed by the proofreader: Remove the symbol(s) ○ ✓: they are not in the source (a picture in the book is not a symbol; leave it out rather than inventing one) | 2.在水果下面画，蔬菜下面画 | 2. Draw "✓" under the fruit and "○" under the vegetables. |
| warning | 67 | p66_s8 | The source does not end with a exclamation mark; do not end the translation with one | 把得数小的排在前面 | Smaller answers go in front! |
| warning | 68 | p67_s14 | Reviewed by the proofreader: The source ends with a question mark; end the translation with a question mark too | 猜一猜，它是谁？ | Guess who it is. |
| warning | 70 | p69_i276_19_p0 | Reviewed by the proofreader: The source does not end with a question mark; do not end the translation with one |  | What is on its left? And on its right? |
| warning | 72 | p71_s15 | Reviewed by the proofreader: The source ends with a question mark; end the translation with a question mark too | 猜一猜，说的是什么物品？ | Guess which object is being described. |
| warning | 74 | p73_s17 | The source does not end with a exclamation mark; do not end the translation with one | 嘻嘻，我知道了。 | Hee hee, now I know! |
| warning | 74 | p73_s19 | The source does not end with a exclamation mark; do not end the translation with one | 滚不动呀 | It won't roll! |
| warning | 90 | p89_s27 | Reviewed by the proofreader: The source ends with a question mark; end the translation with a question mark too | 里可以填几？ | be? Think about it. |
| warning | 94 | p93_s2 | Reviewed by the proofreader: The source does not end with a question mark; do not end the translation with one | 2人一组做游戏，比一比哪组堆得又快又高。 | Play in groups of 2. Which group stacks fastest and highest? |
| warning | 99 | p98_s12_k1 | Reviewed by the proofreader: Remove the symbol(s) □: they are not in the source (a picture in the book is not a symbol; leave it out rather than inventing one) | 画☆，上面画，左 | Draw ☆ to its right, □ above it, |
| warning | 99 | p98_s12_k2 | Reviewed by the proofreader: Remove the symbol(s) △ ○: they are not in the source (a picture in the book is not a symbol; leave it out rather than inventing one) | 边画，下面画 | △ to its left and ○ below it. |
| warning | 101 | p100_s13 | Reviewed by the proofreader: Remove the symbol(s) ○: they are not in the source (a picture in the book is not a symbol; leave it out rather than inventing one) | 6.在400.13.0里填上 | 6. Fill in each ○ with >, < or =. |
| warning | 103 | p102_s8 | Reviewed by the proofreader: Remove the symbol(s) ○ ✓: they are not in the source (a picture in the book is not a symbol; leave it out rather than inventing one) | 17.最重的画最轻的画 | 17. Draw ✓ for the heaviest and ○ for the lightest. |
| warning | 105 | p104_s0 | Reviewed by the proofreader: The source does not end with a question mark; do not end the translation with one | 本学期你学到了什么 | What did you learn this term? |

### `glossary` — 0 errors, 61 warnings

| Severity | Page | Segment | Message | Source | Translation |
|---|---|---|---|---|---|
| warning | 14 | p13_s5 | Reviewed by the proofreader: Glossary: translate "填一填" as "Fill in" | 5.看尺子，填一填 | 5. Complete the ruler. |
| warning | 54 | p53_s17 | Reviewed by the proofreader: Glossary: translate "算式" as "number sentence" | 找出得数是3的加法算式，排一排 | Find the addition sentences that make 3. Arrange them. |
| warning | 54 | p53_s2 | Reviewed by the proofreader: Glossary: translate "算式" as "number sentence" | 这几个加法算式里都有5 | These addition sentences all have a 5. |
| warning | 54 | p53_s26 | Reviewed by the proofreader: Glossary: translate "算式" as "number sentence" | 你能找出得数是10的加法算式吗？排一排 | Which addition sentences make 10? Arrange them. |
| warning | 55 | p54_s1 | Reviewed by the proofreader: Glossary: translate "算式" as "number sentence" | 这几个算式都是6减几的 | These are all 6 minus a number. |
| warning | 55 | p54_s17 | Reviewed by the proofreader: Glossary: translate "算式" as "number sentence" | 找出6减几的算式，排一排 | Find the subtraction sentences that start with 6. Arrange t… |
| warning | 55 | p54_s22 | Reviewed by the proofreader: Glossary: translate "算式" as "number sentence" | 你能找出得数是8的减法算式吗？排一排 | Which subtraction sentences make 8? Arrange them. |
| warning | 63 | p62_a10_p0 | Reviewed by the proofreader: Glossary: translate "练习" as "exercise" | 语文练习本 | Chinese |
| warning | 63 | p62_a12_p0 | Reviewed by the proofreader: Glossary: translate "练习" as "exercise" | 数学练习本 | Maths |
| warning | 63 | p62_a15_p0 | Reviewed by the proofreader: Glossary: translate "练习" as "exercise" | 数学练习本 | Maths |
| warning | 63 | p62_a16_p0 | Reviewed by the proofreader: Glossary: translate "练习" as "exercise" | 语文练习本 | Chinese |
| warning | 63 | p62_a5_p0 | Reviewed by the proofreader: Glossary: translate "练习" as "exercise" | 语文练习本 | Chinese |
| warning | 63 | p62_a6_p0 | Reviewed by the proofreader: Glossary: translate "练习" as "exercise" | 语文练习本 | Chinese |
| warning | 63 | p62_a7_p0 | Reviewed by the proofreader: Glossary: translate "练习" as "exercise" | 语文练习本 | Chinese |
| warning | 63 | p62_a8_p0 | Reviewed by the proofreader: Glossary: translate "练习" as "exercise" | 语文练习本 | Chinese |
| warning | 63 | p62_s16 | Reviewed by the proofreader: Glossary: translate "练习" as "exercise" | 练习本数学 | Maths |
| warning | 63 | p62_s4 | Reviewed by the proofreader: Glossary: translate "练习" as "exercise" | 数学练习本 | Maths |
| warning | 71 | p70_s4 | Reviewed by the proofreader: Glossary: translate "练习" as "exercise" | 练习本 | Notes |
| warning | 78 | p77_s11_k0 | Reviewed by the proofreader: Glossary: translate "个位" as "ones" | 十位个位 | Tens |
| warning | 78 | p77_s11_k1 | Reviewed by the proofreader: Glossary: translate "十位" as "tens" | 十位个位 | Ones |
| warning | 78 | p77_s15_k0 | Reviewed by the proofreader: Glossary: translate "个位" as "ones" | 十位个位 | Tens |
| warning | 78 | p77_s15_k1 | Reviewed by the proofreader: Glossary: translate "十位" as "tens" | 十位个位 | Ones |
| warning | 78 | p77_s17_k0 | Reviewed by the proofreader: Glossary: translate "个位" as "ones" | 十位个位 | Tens |
| warning | 78 | p77_s17_k1 | Reviewed by the proofreader: Glossary: translate "十位" as "tens" | 十位个位 | Ones |
| warning | 78 | p77_s9_k0 | Reviewed by the proofreader: Glossary: translate "个位" as "ones" | 十位个位 | Tens |
| warning | 78 | p77_s9_k1 | Reviewed by the proofreader: Glossary: translate "十位" as "tens" | 十位个位 | Ones |
| warning | 79 | p78_s11_k0 | Reviewed by the proofreader: Glossary: translate "个位" as "ones" | 十位个位 | Tens |
| warning | 79 | p78_s11_k1 | Reviewed by the proofreader: Glossary: translate "十位" as "tens" | 十位个位 | Ones |
| warning | 79 | p78_s13_k0 | Reviewed by the proofreader: Glossary: translate "个位" as "ones" | 十位个位 | Tens |
| warning | 79 | p78_s13_k1 | Reviewed by the proofreader: Glossary: translate "十位" as "tens" | 十位个位 | Ones |
| warning | 79 | p78_s14_k0 | Reviewed by the proofreader: Glossary: translate "个位" as "ones" | 十位个位 | Tens |
| warning | 79 | p78_s14_k1 | Reviewed by the proofreader: Glossary: translate "十位" as "tens" | 十位个位 | Ones |
| warning | 79 | p78_s15_k0 | Reviewed by the proofreader: Glossary: translate "个位" as "ones" | 十位个位 | Tens |
| warning | 79 | p78_s15_k1 | Reviewed by the proofreader: Glossary: translate "十位" as "tens" | 十位个位 | Ones |
| warning | 81 | p80_s17_k0 | Reviewed by the proofreader: Glossary: translate "个位" as "ones" | 十位个位 | Tens |
| warning | 81 | p80_s17_k1 | Reviewed by the proofreader: Glossary: translate "十位" as "tens" | 十位个位 | Ones |
| warning | 81 | p80_s7_k0 | Reviewed by the proofreader: Glossary: translate "个位" as "ones" | 十位个位 | Tens |
| warning | 81 | p80_s7_k1 | Reviewed by the proofreader: Glossary: translate "十位" as "tens" | 十位个位 | Ones |
| warning | 83 | p82_s11_k0 | Reviewed by the proofreader: Glossary: translate "个位" as "ones" | 十位个位 | Tens |
| warning | 83 | p82_s11_k1 | Reviewed by the proofreader: Glossary: translate "十位" as "tens" | 十位个位 | Ones |
| warning | 83 | p82_s12_k0 | Reviewed by the proofreader: Glossary: translate "个位" as "ones" | 十位个位 | Tens |
| warning | 83 | p82_s12_k1 | Reviewed by the proofreader: Glossary: translate "十位" as "tens" | 十位个位 | Ones |
| warning | 83 | p82_s13_k0 | Reviewed by the proofreader: Glossary: translate "个位" as "ones" | 十位个位 | Tens |
| warning | 83 | p82_s13_k1 | Reviewed by the proofreader: Glossary: translate "十位" as "tens" | 十位个位 | Ones |
| warning | 87 | p86_s6_k0 | Reviewed by the proofreader: Glossary: translate "个位" as "ones" | 十位个位 | Tens |
| warning | 87 | p86_s6_k1 | Reviewed by the proofreader: Glossary: translate "十位" as "tens" | 十位个位 | Ones |
| warning | 87 | p86_s7_k0 | Reviewed by the proofreader: Glossary: translate "个位" as "ones" | 十位个位 | Tens |
| warning | 87 | p86_s7_k1 | Reviewed by the proofreader: Glossary: translate "十位" as "tens" | 十位个位 | Ones |
| warning | 87 | p86_s8_k0 | Reviewed by the proofreader: Glossary: translate "个位" as "ones" | 十位个位 | Tens |
| warning | 87 | p86_s8_k1 | Reviewed by the proofreader: Glossary: translate "十位" as "tens" | 十位个位 | Ones |
| warning | 88 | p87_s17 | Reviewed by the proofreader: Glossary: translate "算式" as "number sentence" | 4.把得数是12的算式涂上红色，得数是11的涂上绿色。 | 4. Colour red where the answer is 12 and green where it is … |
| warning | 94 | p93_s2 | Reviewed by the proofreader: Glossary: translate "比一比" as "Compare" | 2人一组做游戏，比一比哪组堆得又快又高。 | Play in groups of 2. Which group stacks fastest and highest? |
| warning | 98 | p97_a30_p0 | Reviewed by the proofreader: Glossary: translate "十位" as "tens" | 十位 | T |
| warning | 98 | p97_a31_p0 | Reviewed by the proofreader: Glossary: translate "个位" as "ones" | 个位 | O |
| warning | 99 | p98_s12_k0 | Reviewed by the proofreader: Glossary: translate "画一画" as "Draw" | 3.画一画。在 | 3. Look at the |
| warning | 100 | p99_s15_k0 | Reviewed by the proofreader: Glossary: translate "个位" as "ones" | 十位个位 | Tens |
| warning | 100 | p99_s15_k1 | Reviewed by the proofreader: Glossary: translate "十位" as "tens" | 十位个位 | Ones |
| warning | 100 | p99_s16_k0 | Reviewed by the proofreader: Glossary: translate "个位" as "ones" | 十位个位 | Tens |
| warning | 100 | p99_s16_k1 | Reviewed by the proofreader: Glossary: translate "十位" as "tens" | 十位个位 | Ones |
| warning | 100 | p99_s17_k0 | Reviewed by the proofreader: Glossary: translate "个位" as "ones" | 十位个位 | Tens |
| warning | 100 | p99_s17_k1 | Reviewed by the proofreader: Glossary: translate "十位" as "tens" | 十位个位 | Ones |

### `image_text` — 0 errors, 2 warnings

| Severity | Page | Segment | Message | Source | Translation |
|---|---|---|---|---|---|
| warning | 57 | p56_i224_23 | The text '比' was left in the source language (inline pictograms the OCR cannot read (left in the picture)): the line is built around symbols or pictures the OCR could not read - check the page in the preview | 比 |  |
| warning | 57 | p56_i224_23 | The text '比' was left in the source language (inline pictograms the OCR cannot read (left in the picture)): the line is built around symbols or pictures the OCR could not read - check the page in the preview | 比 |  |

### `llm_review` — 0 errors, 35 warnings

| Severity | Page | Segment | Message | Source | Translation |
|---|---|---|---|---|---|
| warning | 5 | p4_s3 | Earlier automatic review, text kept by the proofreading: Reviewer (terminology): Glossary requires "Math Is Fun", not "Maths Is Fun". Suggested translation: "Math Is Fun" | 数学好玩 | Maths Is Fun |
| warning | 19 | p18_s14 | Earlier automatic review, text kept by the proofreading: Reviewer (omission): The plural measure word 个 is omitted; context shows the objects are mushrooms, so the counted noun should be supplied. Suggested translation: "I picked 5 mushrooms ⟦0⟧" | 我采了5个72.20.0 | I picked 5 72.20.0 |
| warning | 19 | p18_s15 | Earlier automatic review, text kept by the proofreading: Reviewer (omission): The measure word 个 is omitted; the counted noun (mushrooms) should be written out. Suggested translation: "I picked 8 mushrooms ⟦0⟧" | 我采了8个72.21.0 | I picked 8 72.21.0 |
| warning | 22 | p21_s4 | Reviewer (format): Opening quote mark is missing; the source begins with a closing quote of the answer symbol instruction and should keep the paired quotation. Suggested translation: "“, draw for the least" |  |  |
| warning | 22 | p21_s6 | Earlier automatic review, text kept by the proofreading: Reviewer (terminology): “和” is used as a conjunction here, but it could also be the mathematical term “sum”; “and” is acceptable but context is unclear. | 和 | and |
| warning | 23 | p22_s4 | Earlier automatic review, text kept by the proofreading: Reviewer (meaning): Source says draw "✓" for the largest and for the smallest, but translation says “for the largest” first then “✓ for the smallest”, duplicating ✓ and changing which mark goes with which. Suggested translation: "Draw "✓" for the largest, and draw "✓" for the smallest" |  |  |
| warning | 23 | p22_s6 | Earlier automatic review, text kept by the proofreading: Reviewer (omission): Source ends with a 画 (draw) followed by a blank/mark that is missing in translation. Suggested translation: "and draw for less" |  |  |
| warning | 25 | p24_s10 | Earlier automatic review, text kept by the proofreading: Reviewer (number): Translation adds “No.” where source has only 号 as a suffix (e.g., ①号); also “No.” placement is wrong and turns suffix into prefix. Suggested translation: "→ □ → □ → □" |  |  |
| warning | 25 | p24_s11 | Earlier automatic review, text kept by the proofreading: Reviewer (meaning): “号→” is a suffix label meaning “No. →” attached to a preceding number; translating it as standalone “No. →” changes meaning. Suggested translation: "→" |  |  |
| warning | 27 | p26_s2 | Reviewer (format): Duplicated quote mark before “✓”; source has closing quote only. Suggested translation: ""✓" and draw ✓ for the heavy one" |  |  |
| warning | 27 | p26_s6 | Earlier automatic review, text kept by the proofreading: Reviewer (omission): Source begins with a comma and 画 without the ✓ explicitly in this fragment; translation adds ✓ which is fine by context but the leading comma is odd. Suggested translation: ", and draw ✓ for the heaviest" |  |  |
| warning | 35 | p34_s22 | Reviewer (grammar): '差几把' — '把' names the counted objects (chairs/brooms); the bare 'How many short' drops the noun and is unnatural. Suggested translation: "How many ⟦136.24.0⟧ short? How many short" |  |  |
| warning | 40 | p39_s0 | Earlier automatic review, text kept by the proofreading: Reviewer (meaning): "背土豆" as a story title; "Carrying Potatoes" is a reasonable rendering but the pinyin-title-like convention optional; no change needed for meaning. | 背土豆 | Carrying Potatoes |
| warning | 51 | p50_s3 | Reviewer (format): The enumerator "4." is kept but the rest of the source sentence is translated; the item should reflect the same numbering style as the other items (fine), however the sentence lacks the final source period style consistency — minor: ensure period retained (it is). No change needed beyond consistency. | 4. 10个小朋友做游戏。 | 4. 10 children are playing a game. |
| warning | 52 | p51_s0 | Reviewer (format): Heading should be in Title Case per convention (headings and titles in Title Case); also the glossary pairs 练习 => exercise. Suggested translation: "Exercise 2" | 练习二 | Exercise 2 |
| warning | 52 | p51_s11 | Reviewer (format): Source has no period after 连一连; adding one is a minor format deviation. Also 连一连 gloss is Match. Suggested translation: "4. Match" | 4.连一连 | 4. Match. |
| warning | 57 | p56_s10 | Earlier automatic review, text kept by the proofreading: Reviewer (untranslated): 光明小学 is a school name; pinyin 'Guangming School' is acceptable, but 'Primary School' would be more precise for 小学. Warning only. Suggested translation: "Guangming Primary School" | 光明小学 | Guangming School |
| warning | 58 | p57_s7 | Earlier automatic review, text kept by the proofreading: Reviewer (number): Source contains reference string 228.7.0; translation keeps it but adds a blank not in source. Also should keep the reference and not add '___'. Suggested translation: "228.7.0 is in place" |  |  |
| warning | 63 | p62_s10 | Earlier automatic review, text kept by the proofreading: Reviewer (untranslated): “练”是源文中的单个字，可能是“练习本”的一部分；译为“exercise book”在上下文中可能可以，但丢失了原标签的单字形式。 Suggested translation: "Practice" |  |  |
| warning | 63 | p62_s11 | Earlier automatic review, text kept by the proofreading: Reviewer (meaning): “文”是“语文”的片段；同样译为“Chinese”可以，但原文单字标签被合并了。 Suggested translation: "Chinese" |  |  |
| warning | 63 | p62_s13 | Earlier automatic review, text kept by the proofreading: Reviewer (terminology): “数学”译为“maths”，与同页“Mathematics”不一致；“练习木”疑为“练习本”，译文拼写或漏译。 Suggested translation: "Exercise book, Mathematics exercise book, Chinese" |  |  |
| warning | 63 | p62_s6 | Earlier automatic review, text kept by the proofreading: Reviewer (meaning): “语”作为学科书标签的缩写，最好译为“Chinese (language)”。 Suggested translation: "Chinese (language)" |  |  |
| warning | 63 | p62_s9 | Earlier automatic review, text kept by the proofreading: Reviewer (meaning): “语”是课程标签的缩写，直接译成“Chinese”可能不够明确。 Suggested translation: "Chinese (language)" |  |  |
| warning | 70 | p69_s10 | Reviewer (format): Answer blank written as '____'; the source blank at the end should be rendered as a blank; wording 'is the ____' is acceptable but the first clause is missing a blank for the subject. Suggested translation: "____ is the first, ____ is the ____." |  |  |
| warning | 70 | p69_s11 | Earlier automatic review, text kept by the proofreading: Reviewer (meaning): 在 with a following 的 left/right phrase means 'to the left of / on the right of', not 'at'. Suggested translation: "to the left of" |  |  |
| warning | 73 | p72_s13 | Reviewer (format): Label should be in Title Case. Suggested translation: "Shop" | 商店 | Shop |
| warning | 74 | p73_s1 | Reviewer (format): Heading should follow Title Case convention; 'Recognising Shapes' is acceptable but consistency with source heading style is preferred (e.g. 'Recognizing Shapes'). Suggested translation: "Recognizing Shapes" | 认识图形 | Recognising Shapes |
| warning | 78 | p77_s7 | Reviewer (grammar): '10 ones' is correct, but pairing with '1 ten' keeps consistency. Suggested translation: "10 ones" | 10个一 | 10 ones |
| warning | 87 | p86_s0 | Reviewer (format): Headings and labels are written in Title Case; 'How Many Birds' follows that, but the label is a question and the convention is fine — no change needed if Title Case is intended. Optional question mark for consistency with other question labels. Suggested translation: "How Many Birds?" | 有几只小鸟 | How Many Birds |
| warning | 92 | p91_s0 | Earlier automatic review, text kept by the proofreading: Reviewer (terminology): Glossary requires 'Math Is Fun', not 'Maths Is Fun'. Suggested translation: "Math Is Fun" | 数学好玩 | Maths Is Fun |
| warning | 92 | p91_s7 | Reviewer (format): Stray dots '·.·' from the scan are carried over; drop or represent as an ellipsis. Suggested translation: "6 people…" |  |  |
| warning | 95 | p94_s8 | Earlier automatic review, text kept by the proofreading: Reviewer (meaning): 还摸吗？ means "Shall I/we draw another?" - "Draw again?" loses the question subject slightly but acceptable; better "Shall we draw another?" Suggested translation: "3, 5. Shall we draw another?" | 3，5。还摸吗？ | 3, 5. Draw again? |
| warning | 96 | p95_s12 | Earlier automatic review, text kept by the proofreading: Reviewer (meaning): 拨 means "turn/set the hands" of the clock; "set the clock" is fine. No change needed, but "I say, you move the hands" is more precise. Suggested translation: "I say it, you move the hands." | 我说你拨。 | I say, you set the clock. |
| warning | 104 | p103_s26 | Reviewer (format): Section heading '统计与概率' rendered in Title Case correctly; no issue. | 统计与概率 | Statistics and Probability |
| warning | 104 | p103_s29 | Reviewer (grammar): Missing punctuation/space: '三类因为' → 'three groups because'. Suggested translation: "I sorted them into three groups because..." | 我分成三类因为··· | I sorted them into three groups because… |

### `numbers` — 0 errors, 34 warnings

| Severity | Page | Segment | Message | Source | Translation |
|---|---|---|---|---|---|
| warning | 13 | p12_s3 | Reviewed by the proofreader: Number "0" from the source is missing in the translation; keep every number exactly as written in the source | 一条鱼也没有用48.5.00表示。 | No fish at all: we write 48.5.0. |
| warning | 19 | p18_s16 | Reviewed by the proofreader: Number "23" from the source is missing in the translation; keep every number exactly as written in the source | 我采的72.22.0比的多，比72.23.r | I picked more 72.22.0 than the white rabbit, but fewer th… |
| warning | 19 | p18_s16 | Reviewed by the proofreader: Number "72" from the source is missing in the translation; keep every number exactly as written in the source | 我采的72.22.0比的多，比72.23.r | I picked more 72.22.0 than the white rabbit, but fewer th… |
| warning | 26 | p25_s2 | Reviewed by the proofreader: Number "0" from the source is missing in the translation; keep every number exactly as written in the source | 100.2.l比100.2.0重 | is heavier than the tiger. |
| warning | 26 | p25_s2 | Reviewed by the proofreader: Number "100" from the source is missing in the translation; keep every number exactly as written in the source | 100.2.l比100.2.0重 | is heavier than the tiger. |
| warning | 26 | p25_s2 | Reviewed by the proofreader: Number "2" from the source is missing in the translation; keep every number exactly as written in the source | 100.2.l比100.2.0重 | is heavier than the tiger. |
| warning | 26 | p25_s3 | Reviewed by the proofreader: Number "100" from the source is missing in the translation; keep every number exactly as written in the source | 100.3.l比100.3.r | is lighter than the tiger. |
| warning | 26 | p25_s3 | Reviewed by the proofreader: Number "3" from the source is missing in the translation; keep every number exactly as written in the source | 100.3.l比100.3.r | is lighter than the tiger. |
| warning | 26 | p25_s9 | Reviewed by the proofreader: Number "100" from the source is missing in the translation; keep every number exactly as written in the source | 100.12.l比100.12.r100.14.l比100.14.r | is heavier than the apple, is lighter than the pear. |
| warning | 26 | p25_s9 | Reviewed by the proofreader: Number "12" from the source is missing in the translation; keep every number exactly as written in the source | 100.12.l比100.12.r100.14.l比100.14.r | is heavier than the apple, is lighter than the pear. |
| warning | 26 | p25_s9 | Reviewed by the proofreader: Number "14" from the source is missing in the translation; keep every number exactly as written in the source | 100.12.l比100.12.r100.14.l比100.14.r | is heavier than the apple, is lighter than the pear. |
| warning | 28 | p27_s0 | Reviewed by the proofreader: Number "0" from the source is missing in the translation; keep every number exactly as written in the source | 三加与减（一108.1.0）108.1.1 | Unit 3 Addition and Subtraction (1) |
| warning | 28 | p27_s0 | Reviewed by the proofreader: Number "1" from the source is missing in the translation; keep every number exactly as written in the source | 三加与减（一108.1.0）108.1.1 | Unit 3 Addition and Subtraction (1) |
| warning | 28 | p27_s0 | Reviewed by the proofreader: Number "108" from the source is missing in the translation; keep every number exactly as written in the source | 三加与减（一108.1.0）108.1.1 | Unit 3 Addition and Subtraction (1) |
| warning | 58 | p57_s3_k1 | Reviewed by the proofreader: Number "1" from the source is missing in the translation; keep every number exactly as written in the source | 我排第1 | I'm first. |
| warning | 60 | p59_s0 | Reviewed by the proofreader: Number "0" from the source is missing in the translation; keep every number exactly as written in the source | 9.画一画，心236.0.0 | 9. Draw. Which lily pad can each frog jump onto? |
| warning | 60 | p59_s0 | Reviewed by the proofreader: Number "236" from the source is missing in the translation; keep every number exactly as written in the source | 9.画一画，心236.0.0 | 9. Draw. Which lily pad can each frog jump onto? |
| warning | 74 | p73_s0 | Reviewed by the proofreader: Number "0" from the source is missing in the translation; keep every number exactly as written in the source | 六292.0.0认识图形 | Unit 6 Recognising Shapes |
| warning | 74 | p73_s0 | Reviewed by the proofreader: Number "292" from the source is missing in the translation; keep every number exactly as written in the source | 六292.0.0认识图形 | Unit 6 Recognising Shapes |
| warning | 77 | p76_s9 | Reviewed by the proofreader: Number "3" from the source is missing in the translation; keep every number exactly as written in the source | 3下面每幅图中各有几个小正方体？说一说你是怎么想的。 | How many small cubes are in each? Say how you know. |
| warning | 78 | p77_s0 | Reviewed by the proofreader: Number "0" from the source is missing in the translation; keep every number exactly as written in the source | 七加与减（二308.0.0）308.0.1 | Unit 7 Addition and Subtraction (2) |
| warning | 78 | p77_s0 | Reviewed by the proofreader: Number "1" from the source is missing in the translation; keep every number exactly as written in the source | 七加与减（二308.0.0）308.0.1 | Unit 7 Addition and Subtraction (2) |
| warning | 78 | p77_s0 | Reviewed by the proofreader: Number "308" from the source is missing in the translation; keep every number exactly as written in the source | 七加与减（二308.0.0）308.0.1 | Unit 7 Addition and Subtraction (2) |
| warning | 84 | p83_s5 | Reviewed by the proofreader: Number "0" from the source is missing in the translation; keep every number exactly as written in the source | 共有几条业332.8.0 | How many |
| warning | 84 | p83_s5 | Reviewed by the proofreader: Number "332" from the source is missing in the translation; keep every number exactly as written in the source | 共有几条业332.8.0 | How many |
| warning | 84 | p83_s5 | Reviewed by the proofreader: Number "8" from the source is missing in the translation; keep every number exactly as written in the source | 共有几条业332.8.0 | How many |
| warning | 96 | p95_s0 | Reviewed by the proofreader: Number "0" from the source is missing in the translation; keep every number exactly as written in the source | 八 380.1.0认识钟表 | Unit 8 Telling the Time |
| warning | 96 | p95_s0 | Reviewed by the proofreader: Number "1" from the source is missing in the translation; keep every number exactly as written in the source | 八 380.1.0认识钟表 | Unit 8 Telling the Time |
| warning | 96 | p95_s0 | Reviewed by the proofreader: Number "380" from the source is missing in the translation; keep every number exactly as written in the source | 八 380.1.0认识钟表 | Unit 8 Telling the Time |
| warning | 99 | p98_s2 | Reviewed by the proofreader: Number "392" from the source is missing in the translation; keep every number exactly as written in the source | 1个392.2.0和1筐可以用1表示392.4.r。 | 1 392.2.0 and 1 basket can both be shown by 1. |
| warning | 99 | p98_s2 | Reviewed by the proofreader: Number "4" from the source is missing in the translation; keep every number exactly as written in the source | 1个392.2.0和1筐可以用1表示392.4.r。 | 1 392.2.0 and 1 basket can both be shown by 1. |
| warning | 101 | p100_s13 | Reviewed by the proofreader: Number "0" from the source is missing in the translation; keep every number exactly as written in the source | 6.在400.13.0里填上 | 6. Fill in each ○ with >, < or =. |
| warning | 101 | p100_s13 | Reviewed by the proofreader: Number "13" from the source is missing in the translation; keep every number exactly as written in the source | 6.在400.13.0里填上 | 6. Fill in each ○ with >, < or =. |
| warning | 101 | p100_s13 | Reviewed by the proofreader: Number "400" from the source is missing in the translation; keep every number exactly as written in the source | 6.在400.13.0里填上 | 6. Fill in each ○ with >, < or =. |

### `placeholders` — 0 errors, 205 warnings

| Severity | Page | Segment | Message | Source | Translation |
|---|---|---|---|---|---|
| warning | 3 | p2_s11 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "24") | 我认为“数学”是页码，是24支彩笔，是各种各样的形状···· | I think "mathematics" is page numbers, 24 coloured pens, al… |
| warning | 7 | p6_s0 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "2") | (2）班 | Class 2 |
| warning | 7 | p6_s1 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "1") | 一(1）班 | Class 1 |
| warning | 9 | p8_s2 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "5") | 河里一共有5只鸭子。 | There are 5 ducks in all. |
| warning | 9 | p8_s3 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "2") | 排在第2 | is 2nd in line. |
| warning | 10 | p9_s7 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "5") | 5.找一找生活中的数。 | 5. Find numbers around you. |
| warning | 12 | p11_s1 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "1") | 1.写数。 | 1. How many? |
| warning | 12 | p11_s2 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "2") | 2.数一数，画一画，写一写。 | 2. Count, draw, and write. |
| warning | 12 | p11_s3 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "3") | 3.看数涂一涂。 | 3. Look at the number and colour. |
| warning | 12 | p11_s4 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "4") | 4.数一数，填一填 | 4. Count and fill in. |
| warning | 13 | p12_s10 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "0") | 尺子上有0 | 0 on the ruler. |
| warning | 13 | p12_s3 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦1⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦1⟧ = "0") | 一条鱼也没有用48.5.00表示。 | No fish at all: we write 48.5.0. |
| warning | 13 | p12_s5 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "0") | 说一说，哪里有“0”？ | Talk about it: where can you find "0"? |
| warning | 13 | p12_s6 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "0") | 开关上有0 | 0 on the dial. |
| warning | 13 | p12_s8 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "0") | 电话机上有0 | 0 on the phone. |
| warning | 13 | p12_s9 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "0") | 温度计上有0 | 0 on the thermometer. |
| warning | 14 | p13_s1 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "1") | 1.数一数，有几朵 | 1. Count. How many |
| warning | 14 | p13_s2 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "2") | 2.读一读，写一写 | 2. Read and write. |
| warning | 14 | p13_s3 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "3") | 3.数一数，有几个 | 3. Count. How many |
| warning | 14 | p13_s5 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "5") | 5.看尺子，填一填 | 5. Complete the ruler. |
| warning | 16 | p15_s1 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "10") | 这两句诗共有10个字。 | In Chinese, these two lines have 10 characters. |
| warning | 16 | p15_s10 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "2") | 2.看数接着画。 | 2. Look at the number and draw the rest. |
| warning | 16 | p15_s9 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "1") | 1.画一画，写一写 | 1. Draw and write. |
| warning | 17 | p16_s4 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "4") | 4.填数。 | 4. Fill in. |
| warning | 17 | p16_s5 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧, ⟦1⟧, ⟦2⟧, ⟦3⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "10", ⟦1⟧ = "9", ⟦2⟧ = "8", ⟦3⟧ = "1") | 10，9，8，·，1，发射！ | 10, 9, 8, …, 1, blast off! |
| warning | 18 | p17_s5 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "1") | 少了1个，不够 | 1 short, not enough |
| warning | 19 | p18_s1 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "1") | 1.画一画 | 1. Draw. |
| warning | 19 | p18_s16 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦1⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦1⟧ = "72.23.r") | 我采的72.22.0比的多，比72.23.r | I picked more 72.22.0 than the white rabbit, but fewer th… |
| warning | 19 | p18_s8 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "1") | 每只小狗1根 | Each puppy gets 1 |
| warning | 20 | p19_s10 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧, ⟦1⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "3", ⟦1⟧ = "2") | 读作：3大于2。 | Say: 3 is greater than 2. |
| warning | 20 | p19_s8 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧, ⟦1⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "4", ⟦1⟧ = "4") | 读作：4等于4。 | Say: 4 equals 4. |
| warning | 20 | p19_s9 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧, ⟦1⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "4", ⟦1⟧ = "5") | 读作：4小于5。 | Say: 4 is less than 5. |
| warning | 21 | p20_s1 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "1") | 1.说一说，填一填 | 1. Talk about it and fill in. |
| warning | 21 | p20_s11 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧, ⟦1⟧, ⟦2⟧, ⟦3⟧, ⟦4⟧, ⟦5⟧, ⟦6⟧, ⟦7⟧, ⟦8⟧, ⟦9⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "4", ⟦1⟧ = "9", ⟦2⟧ = "6", ⟦3⟧ = "4", ⟦4⟧ = "7", ⟦5⟧ = "3", ⟦6⟧ = "5", ⟦7⟧ = "1", ⟦8⟧ = "10", ⟦9⟧ = "4") | 4.在9，6，4，7，3，5，1，10中，把大于4的数写在下面。 | 4. From 9, 6, 4, 7, 3, 5, 1, 10, write the numbers greater … |
| warning | 21 | p20_s12 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧, ⟦1⟧, ⟦2⟧, ⟦3⟧, ⟦4⟧, ⟦5⟧, ⟦6⟧, ⟦7⟧, ⟦8⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "10", ⟦1⟧ = "2", ⟦2⟧ = "0", ⟦3⟧ = "7", ⟦4⟧ = "3", ⟦5⟧ = "5", ⟦6⟧ = "4", ⟦7⟧ = "6", ⟦8⟧ = "6") | 在10，2，0，7，3，5，4，6中，把小于6的数写在下面。 | From 10, 2, 0, 7, 3, 5, 4, 6, write the numbers less than 6… |
| warning | 21 | p20_s6 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "3") | 3.填一填 | 3. Fill in. |
| warning | 23 | p22_s7 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "4") | 4.谁喝得多？ | 4. Who drank more? |
| warning | 25 | p24_s1 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "1") | 1.说一说，谁高？谁矮？ | 1. Talk about it: which is taller? Which is shorter? |
| warning | 25 | p24_s4 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "3") | 3.想一想，说一说 | 3. Think and talk. |
| warning | 26 | p25_s2 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧, ⟦1⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "100.2.l", ⟦1⟧ = "100.2.0") | 100.2.l比100.2.0重 | is heavier than the tiger. |
| warning | 26 | p25_s3 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧, ⟦1⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "100.3.l", ⟦1⟧ = "100.3.r") | 100.3.l比100.3.r | is lighter than the tiger. |
| warning | 26 | p25_s9 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧, ⟦1⟧, ⟦2⟧, ⟦3⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "100.12.l", ⟦1⟧ = "100.12.r", ⟦2⟧ = "100.14.l", ⟦3⟧ = "100.14.r") | 100.12.l比100.12.r100.14.l比100.14.r | is heavier than the apple, is lighter than the pear. |
| warning | 27 | p26_s7 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "3") | 3.在重的一边画 | 3. Draw "✓" on the heavier side. |
| warning | 28 | p27_s0 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧, ⟦1⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "108.1.0", ⟦1⟧ = "108.1.1") | 三加与减（一108.1.0）108.1.1 | Unit 3 Addition and Subtraction (1) |
| warning | 28 | p27_s13 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧, ⟦1⟧, ⟦2⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "3", ⟦1⟧ = "2", ⟦2⟧ = "5") | 读作：3加2等于5。 | Say: 3 plus 2 equals 5. |
| warning | 31 | p30_s12 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧, ⟦1⟧, ⟦2⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "5", ⟦1⟧ = "2", ⟦2⟧ = "3") | 读作：5减2等于3。 | Say: 5 minus 2 equals 3. |
| warning | 31 | p30_s7 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "3") | 还剩3块 | 3 are left. |
| warning | 34 | p33_s2 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "1") | 吃1条，还剩 | It eats 1, leaving |
| warning | 34 | p33_s4 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "1") | 又吃1条，还剩 | It eats 1 more, leaving |
| warning | 34 | p33_s6 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "1") | 再吃1条，还剩 | It eats 1 more, leaving |
| warning | 35 | p34_s7 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "5") | 共有5个气球 | 5 balloons in all |
| warning | 35 | p34_s8 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "1") | 打中了1个 | I hit 1. |
| warning | 36 | p35_s1 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "2") | 2.说一说 | 2. Talk about it. |
| warning | 36 | p35_s17 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "5") | 5.填数。 | 5. Fill in. |
| warning | 37 | p36_s3 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "7") | 7.找家。 | 7. Find the homes. |
| warning | 38 | p37_s4 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧, ⟦1⟧, ⟦2⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "4+1=5", ⟦1⟧ = "1", ⟦2⟧ = "6") | 4+1=5，再添1个就是6。 | 4+1=5, and 1 more makes 6. |
| warning | 39 | p38_s15 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "5") | 5.画一画，填一填 | 5. Draw and fill in. |
| warning | 39 | p38_s24 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "6") | 6.说一说，玩一玩。 | 6. Talk about it and play. |
| warning | 39 | p38_s25 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "1") | 我出1 | I show 1. |
| warning | 39 | p38_s26 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "5") | 我出5 | I show 5. |
| warning | 39 | p38_s3 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧, ⟦1⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "2", ⟦1⟧ = "6") | 2.说一说，6个 | 2. Talk about it. Put 6 |
| warning | 39 | p38_s5 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "3") | 3.说一说 | 3. Talk about it. |
| warning | 40 | p39_s3 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧, ⟦1⟧, ⟦2⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "5+1=6", ⟦1⟧ = "1", ⟦2⟧ = "7") | 5+1=6，再添1个就是7。 | 5+1=6, and 1 more makes 7. |
| warning | 41 | p40_s15 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "5") | 5.说一说，玩一玩 | 5. Talk about it and play. |
| warning | 41 | p40_s16 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "4") | 我出4。 | I show 4. |
| warning | 41 | p40_s4 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "3") | 3.说一说。 | 3. Talk about it. |
| warning | 41 | p40_s6 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "4") | 4.画一画，填一填 | 4. Draw and fill in. |
| warning | 42 | p41_s2 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧, ⟦1⟧, ⟦2⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "6+1=7", ⟦1⟧ = "1", ⟦2⟧ = "8") | 6+1=7，再添1个就是8 | 6+1=7, and 1 more makes 8. |
| warning | 42 | p41_s3 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧, ⟦1⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "6", ⟦1⟧ = "2") | 6个在跳绳，2个在摇绳，一共有··· | 6 are jumping, 2 are turning the rope. In all there are… |
| warning | 42 | p41_s5 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "3") | 3个穿 | 3 in |
| warning | 43 | p42_s10 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "1") | 1.说一说，填一填 | 1. Talk about it and fill in. |
| warning | 43 | p42_s11 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "2") | 2.说一说，填一填。 | 2. Talk about it and fill in. |
| warning | 44 | p43_s2 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "4") | 4.八戒吃瓜。 | 4. Bajie eats watermelon. |
| warning | 45 | p44_s2 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧, ⟦1⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "3", ⟦1⟧ = "5") | 前面有3只，后面有5只，一共有··· | 3 in front and 5 behind, so in all there are… |
| warning | 45 | p44_s3 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "8") | 一共有8只， | 8 penguins in all. |
| warning | 46 | p45_s3 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "2") | 2.说一说 | 2. Talk about it. |
| warning | 46 | p45_s6 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "7") | 一共有7只 | 7 in all. |
| warning | 47 | p46_s2 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧, ⟦1⟧, ⟦2⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "9", ⟦1⟧ = "1", ⟦2⟧ = "10") | 9只，再来1只就是10只 | 9 chicks, and 1 more makes 10. |
| warning | 48 | p47_s14 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "5") | 5.说一说，做一做 | 5. Talk about it and do it. |
| warning | 48 | p47_s15 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "1") | 我说1 | I say 1 |
| warning | 48 | p47_s16 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "9") | 我说9 | I say 9 |
| warning | 48 | p47_s5 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "8") | 加油，还有8级！ | Come on, 8 steps to go! |
| warning | 49 | p48_s1 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "2") | 车上有2人 | 2 on the bus. |
| warning | 49 | p48_s3 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "8") | 车上有8人 | 8 on the bus. |
| warning | 49 | p48_s5 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "9") | 车上有9人 | 9 on the bus. |
| warning | 50 | p49_s11 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "3") | 又飞走了3只 | 3 more flew away. |
| warning | 50 | p49_s7 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "1") | （1）一共有几个 | (1) How many |
| warning | 50 | p49_s8 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "2") | (2）一共有多少人？ | (2) How many people in all? |
| warning | 51 | p50_s1 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "1") | （1）说一说，你发现了哪些数学信息？ | (1) Talk about it: what maths information can you see? |
| warning | 51 | p50_s5 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "3") | 3个人藏在树后。 | 3 are hiding behind the tree. |
| warning | 52 | p51_s1 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "1") | 1.画一画，填一填 | 1. Draw and fill in. |
| warning | 52 | p51_s10 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "3") | 3.打靶比赛。 | 3. Target shooting contest. |
| warning | 52 | p51_s8 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "2") | 2.找朋友。 | 2. Find the pairs. |
| warning | 53 | p52_s14 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "7") | 7.摆一摆，算一算。 | 7. Use counters and calculate. |
| warning | 53 | p52_s3 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "6") | 一共有6人。 | 6 people in all. |
| warning | 54 | p53_s1 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "3") | 这几个算式得数都是3。 | These number sentences all make 3. |
| warning | 54 | p53_s2 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "5") | 这几个加法算式里都有5 | These addition sentences all have a 5. |
| warning | 55 | p54_s1 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "6") | 这几个算式都是6减几的 | These are all 6 minus a number. |
| warning | 55 | p54_s2 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "8") | 这几个算式得数都是8。 | These number sentences all make 8. |
| warning | 56 | p55_s20 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧, ⟦1⟧, ⟦2⟧, ⟦3⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "3", ⟦1⟧ = "7", ⟦2⟧ = "9", ⟦3⟧ = "1") | 想一想，3十7可以解决什么问题？9一1呢？ | Think about it. What problems can 3 + 7 solve? What about 9… |
| warning | 57 | p56_s1 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧, ⟦1⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "3", ⟦1⟧ = "5") | 我会比较大小了！3和5 | I can compare numbers now! Comparing 3 and 5… |
| warning | 57 | p56_s6 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "0") | 0是最小的数吗？生活中的数到底还有多少？是不是有很多呀？ | Is 0 the smallest number? How many numbers are there in eve… |
| warning | 58 | p57_s1 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "1") | 1.把同样多的用线连起来 | 1. Draw lines to join groups of the same number. |
| warning | 59 | p58_s0 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "6") | 6.比一比 | 6. Compare. |
| warning | 59 | p58_s10 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "9") | 一共有9个。 | 9 in all. |
| warning | 59 | p58_s4 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "7") | 7.想一想，填一填 | 7. Think and fill in. |
| warning | 60 | p59_s0 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦1⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦1⟧ = "236.0.0") | 9.画一画，心236.0.0 | 9. Draw. Which lily pad can each frog jump onto? |
| warning | 60 | p59_s7 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "1") | （1）说一说，你发现了哪些数学信息？ | (1) Talk about it: what maths information can you see? |
| warning | 60 | p59_s8 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "2") | （2）提出两个数学问题并列式解答。 | (2) Ask two maths questions and solve them with number sent… |
| warning | 60 | p59_s9 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧, ⟦1⟧, ⟦2⟧, ⟦3⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "2", ⟦1⟧ = "3", ⟦2⟧ = "4", ⟦3⟧ = "5") | 把2，3，4，5分别填入 | Write 2, 3, 4 and 5 in the |
| warning | 62 | p61_s1 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "1") | 1.把会飞的动物涂上颜色 | 1. Colour the animals that can fly. |
| warning | 62 | p61_s5 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "3") | 3.分一分 | 3. Sort. |
| warning | 64 | p63_s6 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "1") | 1.把同类的涂上相同的颜色。 | 1. Colour things of the same kind the same colour. |
| warning | 65 | p64_s0 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "3") | 3.分一分，说一说 | 3. Sort and talk about it. |
| warning | 65 | p64_s16 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "6") | 6.看一看，说一说它们是怎么分类的。 | 6. Look and talk about how they are sorted. |
| warning | 65 | p64_s2 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "4") | 4.按要求分一分，说一说 | 4. Sort as instructed and talk about it. |
| warning | 65 | p64_s5 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "5") | 5.算一算；在得数相同的算式上涂一样的颜色。 | 5. Calculate. Colour number sentences with the same answer … |
| warning | 66 | p65_s7 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧, ⟦1⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "1", ⟦1⟧ = "4") | 在图中，1号车排第—，4号车在—号车的后面，在—号车的前面。 | In the picture, car 1 is in — place. Car 4 is behind car — … |
| warning | 67 | p66_s1 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "1") | 1.你的座位前面是谁？后面是谁？ | 1. Who sits in front of you? Who sits behind you? |
| warning | 67 | p66_s18 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "5") | 5.新龟兔赛跑。 | 5. A new tortoise and hare race. |
| warning | 67 | p66_s2 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "2") | 2.算一算，排一排。 | 2. Calculate and put in order. |
| warning | 69 | p68_s1 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "1") | 1.填一填，说一说 | 1. Fill in and talk about it. |
| warning | 69 | p68_s10 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "1") | （1）谁住在最下面？ | (1) Who lives at the very bottom? |
| warning | 69 | p68_s11 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧, ⟦1⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "2", ⟦1⟧ = "2") | （2）谁住在第2层？它在谁的上面？ | (2) Who lives on floor 2? Who is it above? |
| warning | 69 | p68_s13 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "3") | （3）谁住在最上面？它的下面都有谁？ | (3) Who lives at the top? Who lives below it? |
| warning | 69 | p68_s9 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "2") | 2.分房子。把附页中的动物头像剪下，贴在右图中。想一想，说一说。 | 2. Who lives where? Cut out the animal pictures on the cut-… |
| warning | 70 | p69_s15 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "3") | 先向上走3格，再···· | First go up 3 squares, then… |
| warning | 71 | p70_s1 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "1") | 1.说一说你相邻的同学是谁。 | 1. Say who sits next to you. |
| warning | 71 | p70_s11 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "3") | 3.说一说，指一指。 | 3. Talk about it and point. |
| warning | 71 | p70_s12 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "2") | 右边第2个是什么？ | What is 2nd to its right? |
| warning | 71 | p70_s13 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "3") | 左边第3个是什么？ | What is 3rd to its left? |
| warning | 71 | p70_s16 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "5") | 5.做一做 | 5. Do it. |
| warning | 72 | p71_s4 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "8") | 在黑板的上面、国旗的下面有8个大字···· | Above the blackboard and below the national flag there are … |
| warning | 73 | p72_s1 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "1") | 1.看图回答问题 | 1. Answer from the picture. |
| warning | 73 | p72_s6 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧, ⟦1⟧, ⟦2⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "2", ⟦1⟧ = "1", ⟦2⟧ = "4") | (2）从右往左数，小明排第1，小红排第4 | (2) Counting from right to left, Xiaoming is 1st and Xiaoho… |
| warning | 73 | p72_s9 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧, ⟦1⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "3", ⟦1⟧ = "6") | 3.说一说你的文具盒的上、下、前、后、左、右6个面。 | 3. Talk about the 6 faces of your pencil case: top, bottom,… |
| warning | 74 | p73_s0 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "292.0.0") | 六292.0.0认识图形 | Unit 6 Recognising Shapes |
| warning | 75 | p74_s1 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "1") | 1.找朋友。 | 1. Match each object to its shape. |
| warning | 75 | p74_s4 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "3") | 3.搭一搭。 | 3. Build it. |
| warning | 75 | p74_s5 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "4") | 4.找一找形状是 | 4. Find objects like |
| warning | 77 | p76_s8 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "2") | 2.你能说出图中哪些物体的形状？ | 2. Can you name the shapes of the objects in the picture? |
| warning | 77 | p76_s9 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "3") | 3下面每幅图中各有几个小正方体？说一说你是怎么想的。 | How many small cubes are in each? Say how you know. |
| warning | 78 | p77_s0 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧, ⟦1⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "308.0.0", ⟦1⟧ = "308.0.1") | 七加与减（二308.0.0）308.0.1 | Unit 7 Addition and Subtraction (2) |
| warning | 78 | p77_s10 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧, ⟦1⟧, ⟦2⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "1", ⟦1⟧ = "1", ⟦2⟧ = "11") | 1个十，1个一，是11。 | 1 ten and 1 one make 11. |
| warning | 78 | p77_s16 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧, ⟦1⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "2", ⟦1⟧ = "20") | 2个十，是20。 | 2 tens make 20. |
| warning | 78 | p77_s3 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧, ⟦1⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "10", ⟦1⟧ = "1") | 比10多1，是 | 1 more than 10 is |
| warning | 78 | p77_s8 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "1") | 1个十 | 1 ten |
| warning | 79 | p78_s10 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "1") | 1.看图写数 | 1. Write the numbers. |
| warning | 79 | p78_s7 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧, ⟦1⟧, ⟦2⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "4", ⟦1⟧ = "2", ⟦2⟧ = "14") | 4比2大，14大 | 4 is greater than 2, so 14 is greater. |
| warning | 79 | p78_s8 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧, ⟦1⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "12", ⟦1⟧ = "13") | 古人这样表示12，你能用这样的方式表示13吗？ | People long ago showed 12 like this. Can you show 13 the sa… |
| warning | 80 | p79_s0 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "3") | 3.填一填 | 3. Fill in. |
| warning | 80 | p79_s10 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧, ⟦1⟧, ⟦2⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "1", ⟦1⟧ = "8", ⟦2⟧ = "18") | 1个十和8个一合起来是18 | 1 ten and 8 ones together make 18. |
| warning | 80 | p79_s11 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧, ⟦1⟧, ⟦2⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "1", ⟦1⟧ = "8", ⟦2⟧ = "18") | 十位上是1，个位上是8，这个数是18， | The tens digit is 1, the ones digit is 8, so the number is … |
| warning | 80 | p79_s8 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "7") | 7.数一数，填一填。 | 7. Count and fill in. |
| warning | 80 | p79_s9 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "8") | 8.说一说。 | 8. Talk about it. |
| warning | 81 | p80_s2 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "2") | 再放2块 | Add 2 more. |
| warning | 82 | p81_s6 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧, ⟦1⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "2", ⟦1⟧ = "18") | 2.哪两个数加起来是18？填在算式中 | 2. Which two numbers add up to 18? Fill them in the number … |
| warning | 82 | p81_s7 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "3") | 3.看一看，填一填 | 3. Look and fill in. |
| warning | 84 | p83_s5 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "332.8.0") | 共有几条业332.8.0 | How many |
| warning | 86 | p85_s1 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "1") | 1.摆一摆，算一算。 | 1. Lay out and calculate. |
| warning | 86 | p85_s17 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "5") | 5.连一连 | 5. Match. |
| warning | 86 | p85_s19 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "6") | 6.买哪两盒合适？连一连 | 6. Which two boxes should you buy? Match. |
| warning | 86 | p85_s6 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "3") | 3.看一看，填一填。 | 3. Look and fill in. |
| warning | 88 | p87_s17 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧, ⟦1⟧, ⟦2⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "4", ⟦1⟧ = "12", ⟦2⟧ = "11") | 4.把得数是12的算式涂上红色，得数是11的涂上绿色。 | 4. Colour red where the answer is 12 and green where it is … |
| warning | 88 | p87_s4 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "2") | 2.看一看，填一填。 | 2. Look and fill in. |
| warning | 89 | p88_s20 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "4") | 4.画一画，填一填 | 4. Draw and fill in. |
| warning | 90 | p89_s15 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "8") | 8.说一说，做一做 | 8. Talk about it, then do it. |
| warning | 90 | p89_s17 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "8+5") | 8+5元 | 8+5= |
| warning | 90 | p89_s3 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "6") | 6.一共有几只？ | 6. How many in total? |
| warning | 91 | p90_s2 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "14") | 哦！这几个算式得数都是14。 | Oh! These number sentences all have the answer 14. |
| warning | 91 | p90_s3 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "8") | 这几个算式中都有8 | These number sentences all contain 8. |
| warning | 92 | p91_s11 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "2") | 2.说一说你们小组的发现。 | 2. Share what your group found. |
| warning | 92 | p91_s12 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧, ⟦1⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "2", ⟦1⟧ = "9") | 教学楼是长方体形状的，有2层，我还看见9扇窗户。 | The classroom building is shaped like a rectangular prism. … |
| warning | 93 | p92_s0 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "3") | 3.数一数，填一填 | 3. Count and fill in. |
| warning | 93 | p92_s8 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "20") | 我们班有20名男生···· | Our class has 20 boys… |
| warning | 93 | p92_s9 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧, ⟦1⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "6", ⟦1⟧ = "3") | 我们学校有6个年级每个年级3个班······ | Our school has 6 grades, with 3 classes in each grade… |
| warning | 94 | p93_s2 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "2") | 2人一组做游戏，比一比哪组堆得又快又高。 | Play in groups of 2. Which group stacks fastest and highest? |
| warning | 95 | p94_s10 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "2") | 摸到2，正好 | A 2 makes exactly |
| warning | 95 | p94_s11 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "1") | 摸到1可以吗？ | Would a 1 work? |
| warning | 95 | p94_s12 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "10") | 是10..·· | 10… |
| warning | 96 | p95_s0 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "380.1.0") | 八 380.1.0认识钟表 | Unit 8 Telling the Time |
| warning | 96 | p95_s14 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "9") | 我9时睡觉 | I go to bed at 9. |
| warning | 97 | p96_s1 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "1") | 1.认一认。 | 1. Read the clocks. |
| warning | 97 | p96_s8 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "2") | 2.连一连 | 2. Match. |
| warning | 98 | p97_s11 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧, ⟦1⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "4", ⟦1⟧ = "2") | 4.你能在2分钟之内完成吗？看谁做得又对又好 | 4. Can you finish in 2 minutes? See who does them correctly… |
| warning | 98 | p97_s24 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧, ⟦1⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "7", ⟦1⟧ = "9") | 数学作业得了7颗☆语文作业得了9颗☆。 | I got 7 ☆ for my maths homework and 9 ☆ for my Chinese home… |
| warning | 98 | p97_s27 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "8+6=14") | 你能看懂右图中8+6=14吗？ | Can you understand 8+6=14 in the picture on the right? |
| warning | 98 | p97_s31 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "7") | 7.认一认，连一连 | 7. Read the clocks and match. |
| warning | 98 | p97_s4 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "1") | 1.举例说一说，对于数，你有哪些认识？ | 1. Give examples: what do you know about numbers? |
| warning | 98 | p97_s7 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "1") | 这两个1表示的意思一样吗？ | Do these two 1s mean the same thing? |
| warning | 99 | p98_s17 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "4") | 4.请你说说，排队时，你的前面有谁，后面有谁？ | 4. When you line up, who is in front of you and who is behi… |
| warning | 99 | p98_s2 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦4⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦4⟧ = "392.4.r") | 1个392.2.0和1筐可以用1表示392.4.r。 | 1 392.2.0 and 1 basket can both be shown by 1. |
| warning | 99 | p98_s5 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "7+9=16") | 一共得了多少颗☆？7+9=16，我会解决数学问题啦！ | How many ☆ did I get in all? 7+9=16. I can solve maths prob… |
| warning | 99 | p98_s9 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "1") | 1.把下面的物体分一分，说一说你的理由 | 1. Sort the objects below and explain why. |
| warning | 100 | p99_s18 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧, ⟦1⟧, ⟦2⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "4", ⟦1⟧ = "2", ⟦2⟧ = "5") | 4.涂一涂，从左数第2颗珠子涂成红色，从右数第5颗珠子涂成黑色 | 4. Colour the 2nd bead from the left red and the 5th bead f… |
| warning | 100 | p99_s2 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "1") | 1.数一数，填一填 | 1. Count and fill in. |
| warning | 101 | p100_s0 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "5") | 5.把得数相同的算式连起来 | 5. Match number sentences with the same answer. |
| warning | 101 | p100_s13 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦1⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦1⟧ = "400.13.0") | 6.在400.13.0里填上 | 6. Fill in each ○ with >, < or =. |
| warning | 101 | p100_s20 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "7") | 7.填一填 | 7. Fill in. |
| warning | 101 | p100_s24 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧, ⟦1⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "8", ⟦1⟧ = "15") | 8.把得数是15的算式涂上颜色，你发现了什么？ | 8. Colour the number sentences whose answer is 15. What do … |
| warning | 101 | p100_s55 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "9") | 9.一共有多少只？ | 9. How many tadpoles are there in all? |
| warning | 102 | p101_s5 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "15") | 一共15棵 | 15 in all. |
| warning | 103 | p102_s1 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "9") | 我捡了9个贝壳 | I collected 9 shells. |
| warning | 103 | p102_s7 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "16") | 16.接着画下去。 | 16. Keep drawing. |
| warning | 104 | p103_s1 | Reviewed by the proofreader: Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "1") | 1.数一数，填一填， | 1. Count and fill in. |
