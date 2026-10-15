# QA report

**Result:** QA FAILED after 3 rounds: 243 errors, 42 warnings (1253.6 s); proofread: 787 corrections applied; output file checks: 0 error(s)

**Document:** 数学 (zh → en, 109 page(s), 1173 translatable segment(s))

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

## Final issues (285)

### `completeness` — 131 errors, 0 warnings

| Severity | Page | Segment | Message | Source | Translation |
|---|---|---|---|---|---|
| error | 1 | p0_s7 | The segment has no translation; translate the complete source text | 米2 |  |
| error | 3 | p2_s7 | The segment has no translation; translate the complete source text | 30元 |  |
| error | 4 | p3_s2 | The segment has no translation; translate the complete source text | 新国 |  |
| error | 6 | p5_s1 | The segment has no translation; translate the complete source text | 迎新同 |  |
| error | 6 | p5_s2 | The segment has no translation; translate the complete source text | 欢 |  |
| error | 6 | p5_s3 | The segment has no translation; translate the complete source text | 学 |  |
| error | 13 | p12_s7 | The segment has no translation; translate the complete source text | mmmmlmm mmka |  |
| error | 16 | p15_s3 | The segment has no translation; translate the complete source text | 亭台六七座八九十枝花 |  |
| error | 19 | p18_s11 | The segment has no translation; translate the complete source text | 3.比一比，最多的画 |  |
| error | 19 | p18_s12 | The segment has no translation; translate the complete source text | ，最少的画 |  |
| error | 19 | p18_s3 | The translation "." contains no words; translate the complete source text | 一样多。 | . |
| error | 21 | p20_i80_10_p1 | The segment has no translation; translate the complete source text | （多，少），23 |  |
| error | 21 | p20_i80_5_p0 | The segment has no translation; translate the complete source text | 2 |  |
| error | 21 | p20_i80_6_p0 | The segment has no translation; translate the complete source text | 4 |  |
| error | 21 | p20_i80_8_p1 | The segment has no translation; translate the complete source text | （多，少），43 |  |
| error | 21 | p20_s4 | The segment has no translation; translate the complete source text | 2.多的画 |  |
| error | 21 | p20_s5 | The segment has no translation; translate the complete source text | “✓”，少的画 |  |
| error | 22 | p21_s3 | The segment has no translation; translate the complete source text | 哪杯装得最多？最多的画 |  |
| error | 22 | p21_s4 | The segment has no translation; translate the complete source text | ”，最少的画 |  |
| error | 23 | p22_s1 | The segment has no translation; translate the complete source text | 1.大的画 |  |
| error | 23 | p22_s2 | The segment has no translation; translate the complete source text | ，小的画 |  |
| error | 23 | p22_s3 | The segment has no translation; translate the complete source text | 2.最大的画 |  |
| error | 23 | p22_s4 | The segment has no translation; translate the complete source text | “✓”，最小的画 |  |
| error | 23 | p22_s5 | The segment has no translation; translate the complete source text | 3.哪个装得多？多的画 |  |
| error | 23 | p22_s6 | The segment has no translation; translate the complete source text | 少的画 |  |
| error | 25 | p24_a2_p0 | The segment has no translation; translate the complete source text | 号 |  |
| error | 25 | p24_a3_p0 | The segment has no translation; translate the complete source text | 号 |  |
| error | 25 | p24_a4_p0 | The segment has no translation; translate the complete source text | 号 |  |
| error | 25 | p24_a5_p0 | The segment has no translation; translate the complete source text | 号 |  |
| error | 25 | p24_a6_p0 | The segment has no translation; translate the complete source text | 号 |  |
| error | 25 | p24_s10 | The segment has no translation; translate the complete source text | 号→□96.16.0号→□96.16.1号→□96.16.2号 |  |
| error | 25 | p24_s11 | The segment has no translation; translate the complete source text | 号→ |  |
| error | 25 | p24_s12 | The segment has no translation; translate the complete source text | 号 |  |
| error | 25 | p24_s9 | The segment has no translation; translate the complete source text | 最长的画最短的画 |  |
| error | 26 | p25_s10 | The segment has no translation; translate the complete source text | 轻 |  |
| error | 26 | p25_s11 | The segment has no translation; translate the complete source text | 重 |  |
| error | 26 | p25_s4 | The segment has no translation; translate the complete source text | 100.4.0轻 |  |
| error | 27 | p26_s1 | The segment has no translation; translate the complete source text | 1.轻的画 |  |
| error | 27 | p26_s2 | The segment has no translation; translate the complete source text | √”，重的画 |  |
| error | 27 | p26_s4 | The segment has no translation; translate the complete source text | 2.最轻的画 |  |
| error | 27 | p26_s6 | The segment has no translation; translate the complete source text | ，最重的画 |  |
| error | 27 | p26_s7 | The segment has no translation; translate the complete source text | 3.在重的一边画 |  |
| error | 27 | p26_s8 | The segment has no translation; translate the complete source text | 最轻的画 |  |
| error | 33 | p32_s3 | The segment has no translation; translate the complete source text | 000Og |  |
| error | 37 | p36_s10 | The segment has no translation; translate the complete source text | 三 |  |
| error | 37 | p36_s12 | The segment has no translation; translate the complete source text | 5-5日 |  |
| error | 37 | p36_s6 | The segment has no translation; translate the complete source text | 目5-2日 |  |
| error | 44 | p43_s1 | The segment has no translation; translate the complete source text | Ma |  |
| error | 44 | p43_s5 | The segment has no translation; translate the complete source text | 填巾 |  |
| error | 55 | p54_i216_20_p0 | The segment has no translation; translate the complete source text | 6一 |  |
| error | 56 | p55_s8 | The segment has no translation; translate the complete source text | 画 |  |
| error | 56 | p55_s9 | The segment has no translation; translate the complete source text | 画 |  |
| error | 57 | p56_i224_23_p0 | The segment has no translation; translate the complete source text | 比 |  |
| error | 58 | p57_s23 | The segment has no translation; translate the complete source text | 5.比一比，重的画 |  |
| error | 58 | p57_s24 | The segment has no translation; translate the complete source text | “✓”，轻的画 |  |
| error | 59 | p58_s1 | The segment has no translation; translate the complete source text | 爬得最高的画最低的画 |  |
| error | 59 | p58_s5 | The translation ":" contains no words; translate the complete source text | 有 | : |
| error | 59 | p58_s6 | The translation ":" contains no words; translate the complete source text | 有 | : |
| error | 63 | p62_a3_p0 | The segment has no translation; translate the complete source text | 习本 |  |
| error | 63 | p62_i248_10_p0 | The segment has no translation; translate the complete source text | 练习本 |  |
| error | 63 | p62_i248_17_p0 | The segment has no translation; translate the complete source text | 练习木 |  |
| error | 63 | p62_i248_18_p0 | The segment has no translation; translate the complete source text | 语文 |  |
| error | 63 | p62_i248_1_p0 | The segment has no translation; translate the complete source text | 语 |  |
| error | 63 | p62_i248_21_p0 | The segment has no translation; translate the complete source text | 数学 |  |
| error | 63 | p62_i248_22_p0 | The segment has no translation; translate the complete source text | 语文 |  |
| error | 63 | p62_i248_23_p0 | The segment has no translation; translate the complete source text | 练习本 |  |
| error | 63 | p62_i248_25_p0 | The segment has no translation; translate the complete source text | 练习本 |  |
| error | 63 | p62_i248_26_p0 | The segment has no translation; translate the complete source text | 练习本 |  |
| error | 63 | p62_i248_27_p0 | The segment has no translation; translate the complete source text | 练习本 |  |
| error | 63 | p62_i248_2_p0 | The segment has no translation; translate the complete source text | 数学 |  |
| error | 63 | p62_i248_32_p0 | The segment has no translation; translate the complete source text | 语文 |  |
| error | 63 | p62_i248_33_p0 | The segment has no translation; translate the complete source text | 语文 |  |
| error | 63 | p62_i248_34_p0 | The segment has no translation; translate the complete source text | 语文 |  |
| error | 63 | p62_i248_3_p0 | The segment has no translation; translate the complete source text | 数学 |  |
| error | 63 | p62_i248_43_p0 | The segment has no translation; translate the complete source text | 学 |  |
| error | 63 | p62_i248_7_p0 | The segment has no translation; translate the complete source text | 语文 |  |
| error | 63 | p62_s10 | The segment has no translation; translate the complete source text | 练 |  |
| error | 63 | p62_s11 | The segment has no translation; translate the complete source text | 文 |  |
| error | 67 | p66_i264_21_p0 | The segment has no translation; translate the complete source text | 路 |  |
| error | 67 | p66_i264_22_p0 | The segment has no translation; translate the complete source text | 广场 |  |
| error | 68 | p67_s10 | The translation ":" contains no words; translate the complete source text | 在 | : |
| error | 68 | p67_s13 | The translation ":" contains no words; translate the complete source text | 在 | : |
| error | 68 | p67_s7 | The translation ":" contains no words; translate the complete source text | 在 | : |
| error | 69 | p68_a2_p0 | The translation "." contains no words; translate the complete source text | 面 | . |
| error | 69 | p68_i272_10_p0 | The segment has no translation; translate the complete source text | 的_ |  |
| error | 69 | p68_i272_3_p0 | The segment has no translation; translate the complete source text | 面 |  |
| error | 69 | p68_i272_4_p0 | The segment has no translation; translate the complete source text | 面 |  |
| error | 69 | p68_i272_5_p0 | The segment has no translation; translate the complete source text | 面 |  |
| error | 69 | p68_i272_6_p0 | The segment has no translation; translate the complete source text | 面 |  |
| error | 69 | p68_i272_9_p0 | The segment has no translation; translate the complete source text | 在 |  |
| error | 70 | p69_s10 | The segment has no translation; translate the complete source text | 是第—个是第个。 |  |
| error | 71 | p70_s15 | The segment has no translation; translate the complete source text | 是第5辆，一 |  |
| error | 72 | p71_s17 | The translation "." contains no words; translate the complete source text | 的下面 | . |
| error | 72 | p71_s2 | The segment has no translation; translate the complete source text | 自284.2.0葬自信自强自立 |  |
| error | 72 | p71_s20 | The segment has no translation; translate the complete source text | 在 |  |
| error | 73 | p72_s16 | The segment has no translation; translate the complete source text | ns. |  |
| error | 80 | p79_i316_9_p1 | The segment has no translation; translate the complete source text | V |  |
| error | 84 | p83_i332_33_p0 | The segment has no translation; translate the complete source text | 只，地上有 |  |
| error | 84 | p83_i332_33_p1 | The segment has no translation; translate the complete source text | 只，地上有 |  |
| error | 84 | p83_i332_36_p0 | The segment has no translation; translate the complete source text | 只 |  |
| error | 84 | p83_i332_38_p0 | The segment has no translation; translate the complete source text | ，一共有 |  |
| error | 84 | p83_i332_42_p0 | The segment has no translation; translate the complete source text | 只 |  |
| error | 84 | p83_i332_42_p1 | The segment has no translation; translate the complete source text | 只 |  |
| error | 84 | p83_s8 | The segment has no translation; translate the complete source text | 8+9元 |  |
| error | 88 | p87_s16 | The segment has no translation; translate the complete source text | 7+8元 |  |
| error | 88 | p87_s42 | The segment has no translation; translate the complete source text | 十+ |  |
| error | 89 | p88_s3 | The segment has no translation; translate the complete source text | 级台阶，从在第 |  |
| error | 89 | p88_s4 | The segment has no translation; translate the complete source text | 级台阶， |  |
| error | 93 | p92_s2 | The segment has no translation; translate the complete source text | 有 |  |
| error | 93 | p92_s5 | The segment has no translation; translate the complete source text | 有 |  |
| error | 97 | p96_s4 | The segment has no translation; translate the complete source text | 农 |  |
| error | 97 | p96_s5 | The segment has no translation; translate the complete source text | 场 |  |
| error | 97 | p96_s6 | The segment has no translation; translate the complete source text | 小 |  |
| error | 97 | p96_s7 | The segment has no translation; translate the complete source text | 学 |  |
| error | 99 | p98_s12 | The segment has no translation; translate the complete source text | 的右边 |  |
| error | 99 | p98_s19 | The segment has no translation; translate the complete source text | 的左边是 |  |
| error | 99 | p98_s2 | The segment has no translation; translate the complete source text | 都 |  |
| error | 101 | p100_a1_p0 | The segment has no translation; translate the complete source text | “>”“<”或“=”。 |  |
| error | 101 | p100_s25 | The segment has no translation; translate the complete source text | C cccecccccccececcececccccc |  |
| error | 103 | p102_s8 | The segment has no translation; translate the complete source text | 17.最重的画 |  |
| error | 103 | p102_s9 | The segment has no translation; translate the complete source text | 最轻的画 |  |
| error | 104 | p103_s10 | The translation ":" contains no words; translate the complete source text | 有 | : |
| error | 104 | p103_s11 | The translation "." contains no words; translate the complete source text | 个 | . |
| error | 104 | p103_s14 | The translation ": ( ) : ( ) : ( ) :…" contains no words; translate the complete source text | 有()个有(）个，有个有个 | : ( ) : ( ) : ( ) : ( ) |
| error | 104 | p103_s3 | The translation ":" contains no words; translate the complete source text | 有 | : |
| error | 104 | p103_s4 | The translation "." contains no words; translate the complete source text | 个 | . |
| error | 104 | p103_s5 | The translation ":" contains no words; translate the complete source text | 有 | : |
| error | 104 | p103_s6 | The translation "." contains no words; translate the complete source text | 个 | . |
| error | 104 | p103_s7 | The translation ":" contains no words; translate the complete source text | 有 | : |
| error | 104 | p103_s8 | The translation "." contains no words; translate the complete source text | 个 | . |
| error | 104 | p103_s9 | The segment has no translation; translate the complete source text | 有 |  |

### `formatting` — 32 errors, 4 warnings

| Severity | Page | Segment | Message | Source | Translation |
|---|---|---|---|---|---|
| error | 7 | p6_s0 | Start the translation with the list marker "(2）" exactly as in the source | (2）班 | Class 2 |
| error | 12 | p11_s1 | The source does not end with a question mark; do not end the translation with one | 1.写数。 | 1. How many? |
| error | 19 | p18_a1_p0 | Remove the symbol(s) ○ ✓: they are not in the source (a picture in the book is not a symbol; leave it out rather than inventing one) | 3.比一比，最多的画，最少的画 | 3. Compare. Draw "✓" for the most and "○" for the fewest. |
| error | 19 | p18_s2 | Remove the symbol(s) □: they are not in the source (a picture in the book is not a symbol; leave it out rather than inventing one) | 每，和 | Draw as many □ as |
| error | 19 | p18_s5 | Remove the symbol(s) ○: they are not in the source (a picture in the book is not a symbol; leave it out rather than inventing one) | 画，比多72.6.0。 | Draw more ○ than 72.6.0. |
| error | 21 | p20_a1_p0 | Remove the symbol(s) ○: they are not in the source (a picture in the book is not a symbol; leave it out rather than inventing one) | 2.多的画“✓”，少的画 | 2. Draw "✓" for the one with more and "○" for the one with … |
| error | 22 | p21_a1_p0 | Remove the symbol(s) ○ ✓: they are not in the source (a picture in the book is not a symbol; leave it out rather than inventing one) | 哪杯装得最多？最多的画”，最少的画 | Which glass holds the most? Draw "✓" for the most and "○" f… |
| error | 23 | p22_a3_p0 | Remove the symbol(s) ○ ✓: they are not in the source (a picture in the book is not a symbol; leave it out rather than inventing one) | 3.哪个装得多？多的画少的画 | 3. Which holds more? Draw "✓" for the one that holds more a… |
| error | 25 | p24_a1_p0 | Remove the symbol(s) ○ ✓: they are not in the source (a picture in the book is not a symbol; leave it out rather than inventing one) | 最长的画最短的画 | Draw "✓" for the longest and "○" for the shortest. |
| error | 27 | p26_a1_p0 | Keep the symbol(s) √ of the source in the translation, at the matching position | 1.轻的画√”，重的画 | 1. Draw "✓" for the lighter one and "○" for the heavier one. |
| error | 27 | p26_a1_p0 | Remove the symbol(s) ○ ✓: they are not in the source (a picture in the book is not a symbol; leave it out rather than inventing one) | 1.轻的画√”，重的画 | 1. Draw "✓" for the lighter one and "○" for the heavier one. |
| error | 27 | p26_a2_p0 | Remove the symbol(s) ○ ✓: they are not in the source (a picture in the book is not a symbol; leave it out rather than inventing one) | 2.最轻的画，最重的画 | 2. Draw "✓" for the lightest and "○" for the heaviest. |
| error | 27 | p26_a3_p0 | Remove the symbol(s) ○ ✓: they are not in the source (a picture in the book is not a symbol; leave it out rather than inventing one) | 最轻的画 | 4. Draw "✓" for the lightest and "○" for the heaviest. |
| error | 35 | p34_s1 | The source does not end with a question mark; do not end the translation with one | 1.还有几个136.1.0 | 1. How many 136.1.0 are left? |
| error | 46 | p45_s5 | The source does not end with a question mark; do not end the translation with one | 3.房子里有几只 | 3. How many inside? |
| error | 58 | p57_a1_p0 | Remove the symbol(s) ○: they are not in the source (a picture in the book is not a symbol; leave it out rather than inventing one) | 5.比一比，重的画“✓”，轻的画 | 5. Compare. Draw "✓" for the heavier one and "○" for the li… |
| error | 59 | p58_a1_p0 | Remove the symbol(s) ○ ✓: they are not in the source (a picture in the book is not a symbol; leave it out rather than inventing one) | 爬得最高的画最低的画 | Draw "✓" for the one that climbed highest and "○" for the l… |
| error | 68 | p67_s16 | The source ends with a question mark; end the translation with a question mark too | 猜一猜，它是谁？ | Guess who it is. |
| error | 69 | p68_s2 | Keep the line breaks of the source: it has 0 line break(s), the translation has 2 | 在馨272.2.0的——面馨在272.8.0一的— | is ___ 272.2.0. is ___ 272.8.0. |
| error | 72 | p71_s15 | The source ends with a question mark; end the translation with a question mark too | 猜一猜，说的是什么物品？ | Guess which object is being described. |
| error | 84 | p83_s5 | The source does not end with a question mark; do not end the translation with one | 共有几条业332.7.0 | How many 332.7.0? |
| error | 89 | p88_s2 | The source does not end with a question mark; do not end the translation with one | 在第—级台阶，在第—级台阶，在第—级台阶，在第_在第—级台阶，在第——级台阶，在第_级台阶，只在第_级台阶，站在第9级… | Which step is each person on? Step ___, step ___, step ___,… |
| error | 90 | p89_s27 | The source ends with a question mark; end the translation with a question mark too | 里可以填几？ | be? Think about it. |
| error | 94 | p93_s2 | The source does not end with a question mark; do not end the translation with one | 2人一组做游戏，比一比哪组堆得又快又高。 | Play in groups of 2. Which group stacks fastest and highest? |
| error | 95 | p94_s4 | Keep the line breaks of the source: it has 0 line break(s), the translation has 2 | 结果比10大的就被淘汰结果最大的人获胜结果一样大谁摸的牌少谁获胜。 | If your total is more than 10, you're out. The highest tota… |
| error | 99 | p98_s11 | Remove the symbol(s) □ △ ○: they are not in the source (a picture in the book is not a symbol; leave it out rather than inventing one) | 3.画一画。在画☆，上面画，左边画，下面画 | 3. Draw ☆ to the right of the flower, □ above it, △ to its … |
| error | 99 | p98_s7 | Keep the line breaks of the source: it has 0 line break(s), the translation has 2 | 图形与几何独立思考 | Shapes and Geometry On your own |
| error | 100 | p99_s12 | Keep the line breaks of the source: it has 0 line break(s), the translation has 2 | 15的个位上是18里面有1个十和3个一合起来是 | Ones digit of 15 18 has 1 ten and 3 ones make |
| error | 103 | p102_a1_p0 | Remove the symbol(s) ○ ✓: they are not in the source (a picture in the book is not a symbol; leave it out rather than inventing one) | 17.最重的画最轻的画 | 17. Draw "✓" for the heaviest and "○" for the lightest. |
| error | 104 | p103_s14 | Keep the line breaks of the source: it has 0 line break(s), the translation has 3 | 有()个有(）个，有个有个 | : ( ) : ( ) : ( ) : ( ) |
| error | 104 | p103_s2 | Keep the line breaks of the source: it has 0 line break(s), the translation has 3 | 左上图左下图右上图右下图 | Top left Bottom left Top right Bottom right |
| error | 105 | p104_s0 | The source does not end with a question mark; do not end the translation with one | 本学期你学到了什么 | What did you learn this term? |
| warning | 6 | p5_a5_p0 | The source does not end with a exclamation mark; do not end the translation with one | 学 | mates! |
| warning | 18 | p17_s2 | The source does not end with a exclamation mark; do not end the translation with one | 样多，够了 | Same number. Enough! |
| warning | 67 | p66_s8 | The source does not end with a exclamation mark; do not end the translation with one | 把得数小的排在前面 | Smaller answers go in front! |
| warning | 74 | p73_s17 | The source does not end with a exclamation mark; do not end the translation with one | 嘻嘻，我知道了。 | Hee hee, now I know! |

### `glossary` — 27 errors, 0 warnings

| Severity | Page | Segment | Message | Source | Translation |
|---|---|---|---|---|---|
| error | 14 | p13_s5 | Glossary: translate "填一填" as "Fill in" | 5.看尺子，填一填 | 5. Complete the ruler. |
| error | 54 | p53_s26 | Glossary: translate "算式" as "number sentence" | 你能找出得数是10的加法算式吗？排一排 | Which addition sentences make 10? Arrange them |
| error | 55 | p54_s17 | Glossary: translate "算式" as "number sentence" | 找出6减几的算式，排一排 | Find the sentences that subtract from 6. Arrange them |
| error | 55 | p54_s22 | Glossary: translate "算式" as "number sentence" | 你能找出得数是8的减法算式吗？排一排 | Which subtraction sentences make 8? Arrange them |
| error | 58 | p57_s19 | Glossary: translate "算式" as "number sentence" | 4.写出不同算式。 | 4. Write different sums. |
| error | 63 | p62_a10_p0 | Glossary: translate "练习" as "exercise" | 语文练习本 | Chinese |
| error | 63 | p62_a12_p0 | Glossary: translate "练习" as "exercise" | 数学练习本 | Maths |
| error | 63 | p62_a2_p0 | Glossary: translate "练习" as "exercise" | 语文练习本 | Chinese |
| error | 63 | p62_s4 | Glossary: translate "练习" as "exercise" | 数学练习本 | Maths |
| error | 71 | p70_s4 | Glossary: translate "练习" as "exercise" | 练习本 | Notes |
| error | 78 | p77_i308_14_p0 | Glossary: translate "个位" as "ones" | 十位个位 | Tens |
| error | 78 | p77_i308_14_p1 | Glossary: translate "十位" as "tens" | 十位个位 | Ones |
| error | 78 | p77_i308_19_p0 | Glossary: translate "十位" as "tens" | 十位个位 | Ones |
| error | 78 | p77_i308_20_p0 | Glossary: translate "个位" as "ones" | 十位个位 | Tens |
| error | 78 | p77_i308_20_p1 | Glossary: translate "十位" as "tens" | 十位个位 | Ones |
| error | 78 | p77_i308_8_p0 | Glossary: translate "个位" as "ones" | 十位个位 | Tens |
| error | 78 | p77_i308_8_p1 | Glossary: translate "十位" as "tens" | 十位个位 | Ones |
| error | 79 | p78_i312_25_p0 | Glossary: translate "个位" as "ones" | 十位个位 | Tens |
| error | 79 | p78_i312_25_p1 | Glossary: translate "十位" as "tens" | 十位个位 | Ones |
| error | 79 | p78_i312_30_p0 | Glossary: translate "个位" as "ones" | 十位个位 | Tens |
| error | 79 | p78_i312_30_p1 | Glossary: translate "十位" as "tens" | 十位个位 | Ones |
| error | 79 | p78_i312_31_p0 | Glossary: translate "个位" as "ones" | 十位个位 | Tens |
| error | 79 | p78_i312_31_p1 | Glossary: translate "十位" as "tens" | 十位个位 | Ones |
| error | 79 | p78_i312_32_p0 | Glossary: translate "个位" as "ones" | 十位个位 | Tens |
| error | 79 | p78_i312_32_p1 | Glossary: translate "十位" as "tens" | 十位个位 | Ones |
| error | 88 | p87_s17 | Glossary: translate "算式" as "number sentence" | 4.把得数是12的算式涂上红色，得数是11的涂上绿色。 | 4. Colour red where the answer is 12 and green where it is … |
| error | 94 | p93_s2 | Glossary: translate "比一比" as "Compare" | 2人一组做游戏，比一比哪组堆得又快又高。 | Play in groups of 2. Which group stacks fastest and highest? |

### `layout_fit` — 10 errors, 6 warnings

| Severity | Page | Segment | Message | Source | Translation |
|---|---|---|---|---|---|
| error | 26 | p25_s2 | Shorten the translation to at most 18 characters so it fits the original box (the current translation of 26 characters overflows its box; the minimum allowed size is 55%) | 100.2.l比100.2.0重 | is heavier than the tiger. |
| error | 26 | p25_s2 | Shorten the translation to at most 18 characters so it fits the original box (the current translation of 26 characters overflows its box; the minimum allowed size is 55%) | 100.2.l比100.2.0重 | is heavier than the tiger. |
| error | 31 | p30_s11 | Shorten the translation to at most 8 characters so it fits the original box (the current translation of 10 characters overflows its box; the minimum allowed size is 55%) | 减号 | minus sign |
| error | 31 | p30_s11 | Shorten the translation to at most 8 characters so it fits the original box (the current translation of 10 characters overflows its box; the minimum allowed size is 55%) | 减号 | minus sign |
| error | 68 | p67_s4 | Shorten the translation to at most 17 characters so it fits the original box (the current translation of 20 characters overflows its box; the minimum allowed size is 55%) | 在的 | : the rabbit is ____ |
| error | 68 | p67_s4 | Shorten the translation to at most 17 characters so it fits the original box (the current translation of 20 characters overflows its box; the minimum allowed size is 55%) | 在的 | : the rabbit is ____ |
| error | 70 | p69_s0 | Shorten the translation to at most 8 characters so it fits the original box (the current translation of 10 characters overflows its box; the minimum allowed size is 55%) | 左右 | Left/Right |
| error | 70 | p69_s0 | Shorten the translation to at most 8 characters so it fits the original box (the current translation of 10 characters overflows its box; the minimum allowed size is 55%) | 左右 | Left/Right |
| error | 99 | p98_s9 | Shorten the translation to at most 5 characters so it fits the original box (the current translation of 8 characters overflows its box; the minimum allowed size is 55%) | 饼干 | Biscuits |
| error | 99 | p98_s9 | Shorten the translation to at most 5 characters so it fits the original box (the current translation of 8 characters overflows its box; the minimum allowed size is 55%) | 饼干 | Biscuits |
| warning | 56 | p55_s10 | The translation overflows its box and was rendered at 48% of the original size; even a much shorter text would not fit, check this box in the preview | 画 | Draw |
| warning | 56 | p55_s10 | The translation overflows its box and was rendered at 48% of the original size; even a much shorter text would not fit, check this box in the preview | 画 | Draw |
| warning | 104 | p103_s17 | The translation overflows its box and was rendered at 54% of the original size; even a much shorter text would not fit, check this box in the preview | 在 | is on |
| warning | 104 | p103_s17 | The translation overflows its box and was rendered at 54% of the original size; even a much shorter text would not fit, check this box in the preview | 在 | is on |
| warning | 104 | p103_s19 | The translation overflows its box and was rendered at 54% of the original size; even a much shorter text would not fit, check this box in the preview | 在 | is on |
| warning | 104 | p103_s19 | The translation overflows its box and was rendered at 54% of the original size; even a much shorter text would not fit, check this box in the preview | 在 | is on |

### `llm_review` — 17 errors, 27 warnings

| Severity | Page | Segment | Message | Source | Translation |
|---|---|---|---|---|---|
| error | 12 | p11_s3 | Reviewer (terminology): British spelling "colour" deviates from the standard textbook spelling "color". Suggested translation: "3. Look at the number and color." | 3.看数涂一涂。 | 3. Look at the number and colour. |
| error | 14 | p13_s4 | Reviewer (terminology): British spelling "colour" deviates from the standard textbook spelling "color". Suggested translation: "4. Color and write." | 4.涂一涂，写一写。 | 4. Colour and write. |
| error | 22 | p21_s6 | Reviewer (meaning): The source label 和 ("and") is translated as "and", which is a possible reading, but in this page context it is the label for a question word; treating it as a plain conjunction changes the label's function. Also, no context is given to confirm. If it is the question word (和 = "sum/and"), the standard rendering on such a page label is "and"; however the more serious issue is the following items. | 和 | and |
| error | 22 | p21_s7 | Reviewer (number): The placeholder ⟦84.9.0⟧ is rendered as plain "84.9.0" instead of being kept as the placeholder ⟦84.9.0⟧; the source has an image/answer-box placeholder that must be preserved. Suggested translation: "⟦84.9.0⟧, which one holds more?" | 84.9.0，哪个装得多？ | 84.9.0, which one holds more? |
| error | 36 | p35_s0 | Reviewer (terminology): The glossary gives 练习 => exercise, but '练习一' as a section title is conventionally 'Exercise 1'; if a heading, it should follow the glossary and be 'Exercise 1'. Suggested translation: "Exercise 1" | 练习一 | Exercise 1 |
| error | 47 | p46_s0 | Reviewer (terminology): Title should match the standard title-case convention and be a natural heading; 'Chicks Eating' is acceptable but 'Chicks Eat Food' closer. No change required beyond title case. Suggested translation: "Chicks Eating Food" | 小鸡吃食 | Chicks Eating |
| error | 48 | p47_s5 | Reviewer (meaning): Source '还有8级！' means '8 steps left/remaining', not '8 steps to go' is close, but 'Come on, 8 steps to go!' is acceptable. Actually '还有8级' = 'there are still 8 levels/steps'. Translation is fine. No finding. Remove this entry if not needed. Suggested translation: "Come on, 8 more steps!" | 加油，还有8级！ | Come on, 8 steps to go! |
| error | 49 | p48_s2 | Reviewer (untranslated): Place name kept in pinyin as a proper noun: correct, no finding. | 三家店 | Sanjiadian |
| error | 52 | p51_s0 | Reviewer (terminology): 练习二 should follow the glossary term 练习 => exercise, and the source numbering is Chinese; 'Exercise 2' is acceptable, but consider consistency. | 练习二 | Exercise 2 |
| error | 58 | p57_s4 | Reviewer (omission): '一共有' followed by '只动物' is split across items; the translation 'There are' + 'animals in total' is fine, but '一共有' alone should include the blank/number placeholder if present in source. | 一共有 | There are |
| error | 61 | p60_s11 | Reviewer (omission): The final clause 'they are all' has no completion, and the ellipsis placement differs from the source; the sentence ends with '它们都是' requiring the category word. Suggested translation: "Put the balls, toy cars and ······ together; they are all" | 把球、小汽车和······放在一起它们都是 | Put the balls, toy cars and ······ together; they are all |
| error | 78 | p77_s7 | Reviewer (terminology): '10个一' should be '10 ones' with singular 'one', matching place-value terminology; '10 ones' uses plural incorrectly in this counting sense. Suggested translation: "10 ones" | 10个一 | 10 ones |
| error | 85 | p84_s1 | Reviewer (untranslated): The source "mmhwn" is left untranslated; this is a garbled/placeholder-like fragment but should be rendered or flagged as a placeholder consistently. | mmhwn | mmhwn |
| error | 85 | p84_s2 | Reviewer (untranslated): The source "mmy" is left untranslated; it should be handled as a placeholder rather than kept verbatim. | mmy | mmy |
| error | 92 | p91_s2 | Reviewer (terminology): 'on Taoqi's campus' — 校园 is school campus; 'school' or 'campus' both fine, but 'campus' is not usually used for a primary school. Consider 'at Taoqi's school'. Suggested translation: "Can you find math problems at Taoqi's school?" | 你能找到淘气校园里的数学问题吗？ | Can you find maths problems on Taoqi's campus? |
| error | 95 | p94_s8 | Reviewer (meaning): '还摸吗？' means 'Should I/we draw another?' The translation 'Draw again?' is a command, changing the meaning from a question about whether to draw more. Suggested translation: "3, 5. Should I draw another?" | 3，5。还摸吗？ | 3, 5. Draw again? |
| error | 96 | p95_s9 | Reviewer (untranslated): 'ii ip' is a scan artifact. It should probably be a clock-face description or left as a placeholder; keeping it is questionable but it is not translatable text. | ii ip | ii ip |
| warning | 11 | p10_s2 | Reviewer (grammar): The sentence is left incomplete in English; it should read naturally as a statement of counting. Suggested translation: "1, 2, 3, 4, there are" | 1，2，3，4，有 | 1, 2, 3, 4, there are |
| warning | 15 | p14_s2 | Reviewer (grammar): Missing the object of "do" relative to the source 做一做; earlier parallel item reads "Think and do it." Suggested translation: "Think and do." | 想一想，做一做 | Think and do. |
| warning | 16 | p15_s2 | Reviewer (grammar): "Find and talk about it" is awkward; use "Find and say." Suggested translation: "Find and say." | 找一找，说一说 | Find and talk about it. |
| warning | 16 | p15_s4 | Reviewer (grammar): "Jump and talk about it" is awkward; use "Jump and say." Suggested translation: "Jump and say." | 跳一跳，说一说。 | Jump and talk about it. |
| warning | 25 | p24_s7 | Reviewer (format): “比一比，填一填” has no final period in the source; the translation adds one. Consistency with other labels is minor. Suggested translation: "Compare and fill in" | 比一比，填一填 | Compare and fill in. |
| warning | 30 | p29_s1 | Reviewer (format): The source '4.说一说。' keeps its period and marker; the translation keeps it correctly, but the numbering convention for this item should match the source exactly. Suggested translation: "4. Talk about it." | 4.说一说。 | 4. Talk about it. |
| warning | 35 | p34_s21 | Reviewer (format): The source '4.说一说。' includes a period; the translation keeps the numbering but the sentence punctuation should match the source. Suggested translation: "4. Talk about it." | 4.说一说。 | 4. Talk about it. |
| warning | 51 | p50_s3 | Reviewer (format): '10 children' is fine; no issue. | 4. 10个小朋友做游戏。 | 4. 10 children are playing a game. |
| warning | 54 | p53_s31 | Reviewer (grammar): 'Taoqi made' is acceptable; more natural: 'Here is the addition table Taoqi made.' | 下面是淘气做的加法表，你能帮他填完整吗？ | Below is the addition table Taoqi made. Can you help him co… |
| warning | 70 | p69_s2 | Reviewer (format): Placeholder should precede the word where the blank belongs; spacing is off. Suggested translation: "⟦276.3.0⟧ The other hand is" | 276.3.0另一只手是 | 276.3.0 The other hand is |
| warning | 71 | p70_s11 | Reviewer (grammar): 'point' needs an object; the natural phrasing is 'point to them'. Suggested translation: "3. Talk about it and point to them." | 3.说一说，指一指。 | 3. Talk about it and point. |
| warning | 74 | p73_s18 | Reviewer (format): The source uses the Chinese ellipsis '····' (four dots); the translation uses three dots. Suggested translation: "It can roll forward and backward...." | 可以前后滚动···· | It can roll forward and backward... |
| warning | 79 | p78_s12 | Reviewer (grammar): "Do it." is unnatural for a textbook instruction; 做一做 is the standard hands-on activity heading. Suggested translation: "2. Try it." | 2.做一做。 | 2. Do it. |
| warning | 80 | p79_s12 | Reviewer (grammar): "Read and tell." is awkward; 讲一讲 means "tell/discuss the story". Suggested translation: "9. Read and discuss. Long ago, people counted by tying knots in a rope. For example, for 3 sheep, they tied 3 knots in the rope." | 9.读一读，讲一讲古时候，人们用在绳子上打结的方法来计数。比如，3只羊，就在绳子上打3个结来表示。 | 9. Read and tell. Long ago, people counted by tying knots i… |
| warning | 82 | p81_s21 | Reviewer (grammar): "Talk about it." is awkward; 说一说 convention is "Discuss." Suggested translation: "5. Discuss. What results can you get?" | 5.说一说，你能得到哪些结果？ | 5. Talk about it. What results can you get? |
| warning | 86 | p85_s4 | Reviewer (grammar): The Chinese commands 圈一圈，算一算 are conventionally rendered with an object or as 'Circle and calculate'; 'Circle and calculate' is acceptable, but 'calculate' alone slightly loses the 'work out the answer' sense. Consider 'Circle and calculate.' is fine; no change needed. However, consistency with the glossary ('算一算' => 'Calculate') is met. | 2.圈一圈，算一算。 | 2. Circle and calculate. |
| warning | 86 | p85_s6 | Reviewer (grammar): 'Look and fill in' is acceptable, but '填一填' is glossed as 'Fill in'; 'Look and fill in' matches. | 3.看一看，填一填。 | 3. Look and fill in. |
| warning | 87 | p86_s0 | Reviewer (format): Heading casing: 'How Many Birds' is in Title Case, which follows the convention for headings. Acceptable. | 有几只小鸟 | How Many Birds |
| warning | 87 | p86_s6 | Reviewer (format): Single-character column labels 十位个位 should use the standard abbreviations T and O rather than 'Tens Ones'. Suggested translation: "T O" | 十位个位 | Tens Ones |
| warning | 87 | p86_s7 | Reviewer (format): Single-character column labels 十位个位 should use the standard abbreviations T and O rather than 'Tens Ones'. Suggested translation: "T O" | 十位个位 | Tens Ones |
| warning | 87 | p86_s8 | Reviewer (format): Single-character column labels 十位个位 should use the standard abbreviations T and O rather than 'Tens Ones'. Suggested translation: "T O" | 十位个位 | Tens Ones |
| warning | 87 | p86_s9 | Reviewer (grammar): Same as p85_s4: 'Circle and calculate' is acceptable. | 圈一圈，算一算。 | Circle and calculate. |
| warning | 93 | p92_s11 | Reviewer (grammar): Missing comma / conjunction between the two clauses: 'many female teachers and few male teachers' is fine but the comma splice should be avoided. Suggested translation: "The school has many female teachers and few male teachers..." | 学校女老师很多男老师很少··· | The school has many female teachers and few male teachers... |
| warning | 93 | p92_s6 | Reviewer (format): '想一想' is a fixed exercise label; the standard rendering is 'Think' but the more idiomatic textbook label is 'Think about it'. Not misleading. Suggested translation: "Think about it" | 想一想 | Think |
| warning | 93 | p92_s8 | Reviewer (format): Ellipsis style: source uses '····' style trailing dots; translation uses '...'. Acceptable but inconsistent with other items. No meaning change. | 我们班有20名男生···· | Our class has 20 boys... |
| warning | 96 | p95_s12 | Reviewer (grammar): 'I say, you set the clock.' is acceptable; clearer is 'I say the time, you set the clock.' Suggested translation: "I say the time, you set the clock." | 我说你拨。 | I say, you set the clock. |
| warning | 97 | p96_s15 | Reviewer (format): '11时半' rendered as '11:30' while p96_s13 uses 'half past 10' and p96_s16 'half past 5'. Inconsistent style; use 'half past 11'. Suggested translation: "half past 11" | 11时半 | 11:30 |

### `numbers` — 15 errors, 0 warnings

| Severity | Page | Segment | Message | Source | Translation |
|---|---|---|---|---|---|
| error | 21 | p20_i80_10_p0 | Number "23" from the source is missing in the translation; keep every number exactly as written in the source | （多，少），23 | (more, fewer) |
| error | 21 | p20_i80_2_p0 | Number "3" from the source is missing in the translation; keep every number exactly as written in the source | （多，少），3 | (more, fewer) |
| error | 21 | p20_i80_3_p0 | Number "3" from the source is missing in the translation; keep every number exactly as written in the source | 比篷（多，少），3 | vs |
| error | 21 | p20_i80_3_p1 | Number "3" from the source is missing in the translation; keep every number exactly as written in the source | 比篷（多，少），3 | (more, fewer) |
| error | 21 | p20_i80_8_p0 | Number "43" from the source is missing in the translation; keep every number exactly as written in the source | （多，少），43 | (more, fewer) |
| error | 26 | p25_s2 | Number "0" from the source is missing in the translation; keep every number exactly as written in the source | 100.2.l比100.2.0重 | is heavier than the tiger. |
| error | 26 | p25_s2 | Number "100" from the source is missing in the translation; keep every number exactly as written in the source | 100.2.l比100.2.0重 | is heavier than the tiger. |
| error | 26 | p25_s2 | Number "2" from the source is missing in the translation; keep every number exactly as written in the source | 100.2.l比100.2.0重 | is heavier than the tiger. |
| error | 26 | p25_s3 | Number "100" from the source is missing in the translation; keep every number exactly as written in the source | 100.3.l比100.3.r | is lighter than the tiger. |
| error | 26 | p25_s3 | Number "3" from the source is missing in the translation; keep every number exactly as written in the source | 100.3.l比100.3.r | is lighter than the tiger. |
| error | 26 | p25_s9 | Number "100" from the source is missing in the translation; keep every number exactly as written in the source | 100.12.l比100.12.r100.14.l比100.14.r | 100.12.l is heavier than the apple. 100.14.l is lighter… |
| error | 26 | p25_s9 | Number "12" from the source is missing in the translation; keep every number exactly as written in the source | 100.12.l比100.12.r100.14.l比100.14.r | 100.12.l is heavier than the apple. 100.14.l is lighter… |
| error | 101 | p100_s13 | Number "0" from the source is missing in the translation; keep every number exactly as written in the source | 6.在400.13.0里填上 | 6. Fill in each ◯ with >, < or =. |
| error | 101 | p100_s13 | Number "13" from the source is missing in the translation; keep every number exactly as written in the source | 6.在400.13.0里填上 | 6. Fill in each ◯ with >, < or =. |
| error | 101 | p100_s13 | Number "400" from the source is missing in the translation; keep every number exactly as written in the source | 6.在400.13.0里填上 | 6. Fill in each ◯ with >, < or =. |

### `placeholders` — 11 errors, 0 warnings

| Severity | Page | Segment | Message | Source | Translation |
|---|---|---|---|---|---|
| error | 10 | p9_s0 | Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "3") | 3.看一看，说一说 | 3. Look and say. |
| error | 25 | p24_s4 | Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "3") | 3.想一想，说一说 | 3. Think and talk. |
| error | 26 | p25_s2 | Placeholder problem: missing placeholders: ⟦0⟧, ⟦1⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "100.2.l", ⟦1⟧ = "100.2.0") | 100.2.l比100.2.0重 | is heavier than the tiger. |
| error | 26 | p25_s3 | Placeholder problem: missing placeholders: ⟦0⟧, ⟦1⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "100.3.l", ⟦1⟧ = "100.3.r") | 100.3.l比100.3.r | is lighter than the tiger. |
| error | 26 | p25_s9 | Placeholder problem: missing placeholders: ⟦1⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦1⟧ = "100.12.r") | 100.12.l比100.12.r100.14.l比100.14.r | 100.12.l is heavier than the apple. 100.14.l is lighter… |
| error | 50 | p49_s9 | Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "2") | 2.说一说，算一算。 | 2. Talk about it and calculate. |
| error | 73 | p72_s1 | Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "1") | 1.看图回答问题 | 1. Look at the picture and answer. |
| error | 75 | p74_s4 | Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "3") | 3.搭一搭。 | 3. Build it. |
| error | 79 | p78_s10 | Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "1") | 1.看图写数 | 1. Write the numbers. |
| error | 101 | p100_s13 | Placeholder problem: missing placeholders: ⟦1⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦1⟧ = "400.13.0") | 6.在400.13.0里填上 | 6. Fill in each ◯ with >, < or =. |
| error | 101 | p100_s20 | Placeholder problem: missing placeholders: ⟦0⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦0⟧ = "7") | 7.填一填 | 7. Fill in. |

### `image_text` — 0 errors, 2 warnings

| Severity | Page | Segment | Message | Source | Translation |
|---|---|---|---|---|---|
| warning | 27 | p26_i104_19 | The text '，最重的画“”' was left in the source language (unreadable symbol in quotes (left in the picture)): the line is built around symbols or pictures the OCR could not read - check the page in the preview | ，最重的画“” |  |
| warning | 27 | p26_i104_19 | The text '，最重的画“”' was left in the source language (unreadable symbol in quotes (left in the picture)): the line is built around symbols or pictures the OCR could not read - check the page in the preview | ，最重的画“” |  |

### `length_ratio` — 0 errors, 3 warnings

| Severity | Page | Segment | Message | Source | Translation |
|---|---|---|---|---|---|
| warning | 20 | p19_i76_13_p0 | The translation looks too short: 2 characters for 9 translatable source characters (ratio 0.22, about 2.60 expected); check that nothing was omitted | 比（多，少），姓比 | vs |
| warning | 20 | p19_i76_13_p2 | The translation looks too short: 2 characters for 9 translatable source characters (ratio 0.22, about 2.60 expected); check that nothing was omitted | 比（多，少），姓比 | vs |
| warning | 21 | p20_i80_3_p0 | The translation looks too short: 2 characters for 9 translatable source characters (ratio 0.22, about 2.60 expected); check that nothing was omitted | 比篷（多，少），3 | vs |
