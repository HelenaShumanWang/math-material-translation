# QA report

**Result:** QA FAILED after 3 rounds: 169 errors, 66 warnings (1253.6 s); proofread: 367 corrections applied; output file checks: 0 error(s)

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

## Final issues (235)

### `completeness` — 81 errors, 0 warnings

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
| error | 19 | p18_s3 | The translation "." contains no words; translate the complete source text | 一样多。 | . |
| error | 21 | p20_s2 | The segment has no translation; translate the complete source text | （多，少），3（多，少），43 |  |
| error | 21 | p20_s3 | The segment has no translation; translate the complete source text | （多，少），23 |  |
| error | 25 | p24_s10 | The segment has no translation; translate the complete source text | 号→□96.16.0号→□96.16.1号→□96.16.2号 |  |
| error | 25 | p24_s11 | The segment has no translation; translate the complete source text | 号→ |  |
| error | 25 | p24_s12 | The segment has no translation; translate the complete source text | 号 |  |
| error | 26 | p25_s10 | The segment has no translation; translate the complete source text | 轻 |  |
| error | 26 | p25_s11 | The segment has no translation; translate the complete source text | 重 |  |
| error | 26 | p25_s4 | The segment has no translation; translate the complete source text | 100.4.0轻 |  |
| error | 33 | p32_s3 | The segment has no translation; translate the complete source text | 000Og |  |
| error | 37 | p36_s10 | The segment has no translation; translate the complete source text | 三 |  |
| error | 37 | p36_s12 | The segment has no translation; translate the complete source text | 5-5日 |  |
| error | 37 | p36_s6 | The segment has no translation; translate the complete source text | 目5-2日 |  |
| error | 44 | p43_s1 | The segment has no translation; translate the complete source text | Ma |  |
| error | 44 | p43_s5 | The segment has no translation; translate the complete source text | 填巾 |  |
| error | 55 | p54_s21 | The segment has no translation; translate the complete source text | 6一 |  |
| error | 57 | p56_s10 | The segment has no translation; translate the complete source text | 光明小学 |  |
| error | 59 | p58_s5 | The translation ":" contains no words; translate the complete source text | 有 | : |
| error | 59 | p58_s6 | The translation ":" contains no words; translate the complete source text | 有 | : |
| error | 63 | p62_s10 | The segment has no translation; translate the complete source text | 练 |  |
| error | 63 | p62_s11 | The segment has no translation; translate the complete source text | 文 |  |
| error | 63 | p62_s12 | The segment has no translation; translate the complete source text | 语文练习本语文 |  |
| error | 63 | p62_s13 | The segment has no translation; translate the complete source text | 练习木数学练习本语文 |  |
| error | 63 | p62_s16 | The segment has no translation; translate the complete source text | 练习本数学 |  |
| error | 63 | p62_s19 | The segment has no translation; translate the complete source text | 数学练习本数学 |  |
| error | 63 | p62_s20 | The segment has no translation; translate the complete source text | 数学语文 |  |
| error | 63 | p62_s3 | The segment has no translation; translate the complete source text | 数学语文练习本 |  |
| error | 63 | p62_s5 | The segment has no translation; translate the complete source text | 数学药习本 |  |
| error | 63 | p62_s9 | The segment has no translation; translate the complete source text | 语 |  |
| error | 65 | p64_s18 | The segment has no translation; translate the complete source text | 蔬菜 |  |
| error | 65 | p64_s19 | The segment has no translation; translate the complete source text | 水果 |  |
| error | 67 | p66_s16 | The segment has no translation; translate the complete source text | 火车站路广场 |  |
| error | 68 | p67_s10 | The translation ":" contains no words; translate the complete source text | 在 | : |
| error | 68 | p67_s13 | The translation ":" contains no words; translate the complete source text | 在 | : |
| error | 68 | p67_s4 | The translation ":" contains no words; translate the complete source text | 在 | : |
| error | 68 | p67_s5 | The segment has no translation; translate the complete source text | 的 |  |
| error | 68 | p67_s7 | The translation ":" contains no words; translate the complete source text | 在 | : |
| error | 69 | p68_s3 | The segment has no translation; translate the complete source text | 面 |  |
| error | 69 | p68_s4 | The translation ":" contains no words; translate the complete source text | 在 | : |
| error | 70 | p69_s10 | The segment has no translation; translate the complete source text | 是第—个是第个。 |  |
| error | 71 | p70_s15 | The segment has no translation; translate the complete source text | 是第5辆，一 |  |
| error | 72 | p71_s17 | The translation "." contains no words; translate the complete source text | 的下面 | . |
| error | 72 | p71_s2 | The segment has no translation; translate the complete source text | 自284.2.0葬自信自强自立 |  |
| error | 72 | p71_s20 | The segment has no translation; translate the complete source text | 在 |  |
| error | 73 | p72_s16 | The segment has no translation; translate the complete source text | ns. |  |
| error | 74 | p73_s12 | The segment has no translation; translate the complete source text | 茶 |  |
| error | 74 | p73_s2 | The segment has no translation; translate the complete source text | 牙膏 |  |
| error | 74 | p73_s4 | The segment has no translation; translate the complete source text | 茶 |  |
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
| error | 101 | p100_s25 | The segment has no translation; translate the complete source text | C cccecccccccececcececccccc |  |
| error | 104 | p103_s10 | The translation ":" contains no words; translate the complete source text | 有 | : |
| error | 104 | p103_s11 | The translation "." contains no words; translate the complete source text | 个 | . |
| error | 104 | p103_s14 | The translation ": () : () : () : ()" contains no words; translate the complete source text | 有()个有(）个，有个有个 | : () : () : () : () |
| error | 104 | p103_s3 | The translation ":" contains no words; translate the complete source text | 有 | : |
| error | 104 | p103_s4 | The translation "." contains no words; translate the complete source text | 个 | . |
| error | 104 | p103_s5 | The translation ":" contains no words; translate the complete source text | 有 | : |
| error | 104 | p103_s6 | The translation "." contains no words; translate the complete source text | 个 | . |
| error | 104 | p103_s7 | The translation ":" contains no words; translate the complete source text | 有 | : |
| error | 104 | p103_s8 | The translation "." contains no words; translate the complete source text | 个 | . |
| error | 104 | p103_s9 | The segment has no translation; translate the complete source text | 有 |  |

### `formatting` — 20 errors, 3 warnings

| Severity | Page | Segment | Message | Source | Translation |
|---|---|---|---|---|---|
| error | 7 | p6_s0 | Start the translation with the list marker "(2）" exactly as in the source | (2）班 | Class 2 |
| error | 12 | p11_s1 | The source does not end with a question mark; do not end the translation with one | 1.写数。 | 1. How many? |
| error | 19 | p18_s2 | Remove the symbol(s) □: they are not in the source (a picture in the book is not a symbol; leave it out rather than inventing one) | 每，和 | Draw as many □ as |
| error | 19 | p18_s5 | Remove the symbol(s) ○: they are not in the source (a picture in the book is not a symbol; leave it out rather than inventing one) | 画，比多72.6.0。 | Draw more ○ than 72.6.0. |
| error | 22 | p21_s4 | Remove the symbol(s) ✓: they are not in the source (a picture in the book is not a symbol; leave it out rather than inventing one) | ”，最少的画 | "✓", least: |
| error | 35 | p34_s1 | The source does not end with a question mark; do not end the translation with one | 1.还有几个136.1.0 | 1. How many 136.1.0 are left? |
| error | 46 | p45_s5 | The source does not end with a question mark; do not end the translation with one | 3.房子里有几只 | 3. How many inside? |
| error | 68 | p67_s16 | The source ends with a question mark; end the translation with a question mark too | 猜一猜，它是谁？ | Guess who it is. |
| error | 72 | p71_s15 | The source ends with a question mark; end the translation with a question mark too | 猜一猜，说的是什么物品？ | Guess which object is being described. |
| error | 84 | p83_s5 | The source does not end with a question mark; do not end the translation with one | 共有几条业332.7.0 | How many 332.7.0? |
| error | 89 | p88_s2 | The source does not end with a question mark; do not end the translation with one | 在第—级台阶，在第—级台阶，在第—级台阶，在第_在第—级台阶，在第——级台阶，在第_级台阶，只在第_级台阶，站在第9级… | Which step is each person on? Step ___, step ___, step ___,… |
| error | 90 | p89_s27 | The source ends with a question mark; end the translation with a question mark too | 里可以填几？ | be? Think about it. |
| error | 94 | p93_s2 | The source does not end with a question mark; do not end the translation with one | 2人一组做游戏，比一比哪组堆得又快又高。 | Play in groups of 2. Which group stacks fastest and highest? |
| error | 95 | p94_s4 | Keep the line breaks of the source: it has 0 line break(s), the translation has 2 | 结果比10大的就被淘汰结果最大的人获胜结果一样大谁摸的牌少谁获胜。 | If your total is more than 10, you're out. The highest tota… |
| error | 99 | p98_s11 | Remove the symbol(s) □ △ ○: they are not in the source (a picture in the book is not a symbol; leave it out rather than inventing one) | 3.画一画。在画☆，上面画，左边画，下面画 | 3. Draw ☆ to the right of the flower, □ above it, △ to its … |
| error | 99 | p98_s7 | Keep the line breaks of the source: it has 0 line break(s), the translation has 2 | 图形与几何独立思考 | Shapes and Geometry On your own |
| error | 100 | p99_s12 | Keep the line breaks of the source: it has 0 line break(s), the translation has 2 | 15的个位上是18里面有1个十和3个一合起来是 | Ones digit of 15 18 has 1 ten and 3 ones make |
| error | 104 | p103_s14 | Keep the line breaks of the source: it has 0 line break(s), the translation has 3 | 有()个有(）个，有个有个 | : () : () : () : () |
| error | 104 | p103_s2 | Keep the line breaks of the source: it has 0 line break(s), the translation has 3 | 左上图左下图右上图右下图 | Top left Bottom left Top right Bottom right |
| error | 105 | p104_s0 | The source does not end with a question mark; do not end the translation with one | 本学期你学到了什么 | What did you learn this term? |
| warning | 18 | p17_s2 | The source does not end with a exclamation mark; do not end the translation with one | 样多，够了 | Same number. Enough! |
| warning | 67 | p66_s8 | The source does not end with a exclamation mark; do not end the translation with one | 把得数小的排在前面 | Smaller answers go in front! |
| warning | 74 | p73_s17 | The source does not end with a exclamation mark; do not end the translation with one | 嘻嘻，我知道了。 | Hee hee, now I know! |

### `glossary` — 10 errors, 0 warnings

| Severity | Page | Segment | Message | Source | Translation |
|---|---|---|---|---|---|
| error | 14 | p13_s5 | Glossary: translate "填一填" as "Fill in" | 5.看尺子，填一填 | 5. Complete the ruler. |
| error | 54 | p53_s26 | Glossary: translate "算式" as "number sentence" | 你能找出得数是10的加法算式吗？排一排 | Which addition sentences make 10? Arrange them |
| error | 55 | p54_s17 | Glossary: translate "算式" as "number sentence" | 找出6减几的算式，排一排 | Find the sentences that subtract from 6. Arrange them |
| error | 55 | p54_s22 | Glossary: translate "算式" as "number sentence" | 你能找出得数是8的减法算式吗？排一排 | Which subtraction sentences make 8? Arrange them |
| error | 58 | p57_s19 | Glossary: translate "算式" as "number sentence" | 4.写出不同算式。 | 4. Write different sums. |
| error | 63 | p62_s4 | Glossary: translate "练习" as "exercise" | 数学练习本 | Maths |
| error | 71 | p70_s4 | Glossary: translate "练习" as "exercise" | 练习本 | Notes |
| error | 88 | p87_s17 | Glossary: translate "算式" as "number sentence" | 4.把得数是12的算式涂上红色，得数是11的涂上绿色。 | 4. Colour red where the answer is 12 and green where it is … |
| error | 94 | p93_s2 | Glossary: translate "比一比" as "Compare" | 2人一组做游戏，比一比哪组堆得又快又高。 | Play in groups of 2. Which group stacks fastest and highest? |
| error | 100 | p99_s0 | Glossary: translate "练习" as "exercise" | 练习 | Practice |

### `layout_fit` — 40 errors, 16 warnings

| Severity | Page | Segment | Message | Source | Translation |
|---|---|---|---|---|---|
| error | 5 | p4_s2 | Shorten the translation to at most 23 characters so it fits the original box (the current translation of 27 characters overflows its box; the minimum allowed size is 55%) | 七加与减 | Unit 7 Add and Subtract (2) |
| error | 5 | p4_s2 | Shorten the translation to at most 23 characters so it fits the original box (the current translation of 27 characters overflows its box; the minimum allowed size is 55%) | 七加与减 | Unit 7 Add and Subtract (2) |
| error | 8 | p7_s4 | Shorten the translation to at most 6 characters so it fits the original box (the current translation of 8 characters overflows its box; the minimum allowed size is 55%) | 1筐 | 1 basket |
| error | 8 | p7_s4 | Shorten the translation to at most 6 characters so it fits the original box (the current translation of 8 characters overflows its box; the minimum allowed size is 55%) | 1筐 | 1 basket |
| error | 26 | p25_s2 | Shorten the translation to at most 24 characters so it fits the original box (the current translation of 36 characters overflows its box; the minimum allowed size is 55%) | 100.2.l比100.2.0重 | 100.2.l is heavier than 100.2.0. |
| error | 26 | p25_s2 | Shorten the translation to at most 24 characters so it fits the original box (the current translation of 36 characters overflows its box; the minimum allowed size is 55%) | 100.2.l比100.2.0重 | 100.2.l is heavier than 100.2.0. |
| error | 26 | p25_s3 | Shorten the translation to at most 27 characters so it fits the original box (the current translation of 33 characters overflows its box; the minimum allowed size is 55%) | 100.3.l比100.3.r | 100.3.l lighter than 100.3.r. |
| error | 26 | p25_s3 | Shorten the translation to at most 27 characters so it fits the original box (the current translation of 33 characters overflows its box; the minimum allowed size is 55%) | 100.3.l比100.3.r | 100.3.l lighter than 100.3.r. |
| error | 26 | p25_s9 | Shorten the translation to at most 37 characters so it fits the original box (the current translation of 71 characters overflows its box; the minimum allowed size is 55%) | 100.12.l比100.12.r100.14.l比100.14.r | 100.12.l heavier than 100.12.r. 100.14.l lighter than… |
| error | 26 | p25_s9 | Shorten the translation to at most 37 characters so it fits the original box (the current translation of 71 characters overflows its box; the minimum allowed size is 55%) | 100.12.l比100.12.r100.14.l比100.14.r | 100.12.l heavier than 100.12.r. 100.14.l lighter than… |
| error | 28 | p27_s12 | Shorten the translation to at most 7 characters so it fits the original box (the current translation of 9 characters overflows its box; the minimum allowed size is 55%) | 加号 | plus sign |
| error | 28 | p27_s12 | Shorten the translation to at most 7 characters so it fits the original box (the current translation of 9 characters overflows its box; the minimum allowed size is 55%) | 加号 | plus sign |
| error | 31 | p30_s11 | Shorten the translation to at most 8 characters so it fits the original box (the current translation of 10 characters overflows its box; the minimum allowed size is 55%) | 减号 | minus sign |
| error | 31 | p30_s11 | Shorten the translation to at most 8 characters so it fits the original box (the current translation of 10 characters overflows its box; the minimum allowed size is 55%) | 减号 | minus sign |
| error | 40 | p39_s0 | Shorten the translation to at most 14 characters so it fits the original box (the current translation of 17 characters overflows its box; the minimum allowed size is 55%) | 背土豆 | Carrying Potatoes |
| error | 40 | p39_s0 | Shorten the translation to at most 14 characters so it fits the original box (the current translation of 17 characters overflows its box; the minimum allowed size is 55%) | 背土豆 | Carrying Potatoes |
| error | 42 | p41_s0 | Shorten the translation to at most 7 characters so it fits the original box (the current translation of 9 characters overflows its box; the minimum allowed size is 55%) | 跳绳 | Jump Rope |
| error | 42 | p41_s0 | Shorten the translation to at most 7 characters so it fits the original box (the current translation of 9 characters overflows its box; the minimum allowed size is 55%) | 跳绳 | Jump Rope |
| error | 49 | p48_s0 | Shorten the translation to at most 6 characters so it fits the original box (the current translation of 8 characters overflows its box; the minimum allowed size is 55%) | 乘车 | Bus Ride |
| error | 49 | p48_s0 | Shorten the translation to at most 6 characters so it fits the original box (the current translation of 8 characters overflows its box; the minimum allowed size is 55%) | 乘车 | Bus Ride |
| error | 58 | p57_s6 | Shorten the translation to at most 7 characters so it fits the original box (the current translation of 9 characters overflows its box; the minimum allowed size is 55%) | 排第 | is number |
| error | 58 | p57_s6 | Shorten the translation to at most 7 characters so it fits the original box (the current translation of 9 characters overflows its box; the minimum allowed size is 55%) | 排第 | is number |
| error | 61 | p60_s13 | Shorten the translation to at most 6 characters so it fits the original box (the current translation of 9 characters overflows its box; the minimum allowed size is 55%) | 妙想 | Miaoxiang |
| error | 61 | p60_s13 | Shorten the translation to at most 6 characters so it fits the original box (the current translation of 9 characters overflows its box; the minimum allowed size is 55%) | 妙想 | Miaoxiang |
| error | 62 | p61_s7 | Shorten the translation to at most 8 characters so it fits the original box (the current translation of 10 characters overflows its box; the minimum allowed size is 55%) | 文具 | Stationery |
| error | 62 | p61_s7 | Shorten the translation to at most 8 characters so it fits the original box (the current translation of 10 characters overflows its box; the minimum allowed size is 55%) | 文具 | Stationery |
| error | 63 | p62_s14 | Shorten the translation to at most 5 characters so it fits the original box (the current translation of 7 characters overflows its box; the minimum allowed size is 55%) | 语文 | Chinese |
| error | 63 | p62_s14 | Shorten the translation to at most 5 characters so it fits the original box (the current translation of 7 characters overflows its box; the minimum allowed size is 55%) | 语文 | Chinese |
| error | 63 | p62_s17 | Shorten the translation to at most 5 characters so it fits the original box (the current translation of 7 characters overflows its box; the minimum allowed size is 55%) | 语文 | Chinese |
| error | 63 | p62_s17 | Shorten the translation to at most 5 characters so it fits the original box (the current translation of 7 characters overflows its box; the minimum allowed size is 55%) | 语文 | Chinese |
| error | 66 | p65_s1 | Shorten the translation to at most 8 characters so it fits the original box (the current translation of 10 characters overflows its box; the minimum allowed size is 55%) | 前后 | Front/Back |
| error | 66 | p65_s1 | Shorten the translation to at most 8 characters so it fits the original box (the current translation of 10 characters overflows its box; the minimum allowed size is 55%) | 前后 | Front/Back |
| error | 68 | p67_s0 | Shorten the translation to at most 9 characters so it fits the original box (the current translation of 11 characters overflows its box; the minimum allowed size is 55%) | 上下 | Above/Below |
| error | 68 | p67_s0 | Shorten the translation to at most 9 characters so it fits the original box (the current translation of 11 characters overflows its box; the minimum allowed size is 55%) | 上下 | Above/Below |
| error | 70 | p69_s0 | Shorten the translation to at most 8 characters so it fits the original box (the current translation of 10 characters overflows its box; the minimum allowed size is 55%) | 左右 | Left/Right |
| error | 70 | p69_s0 | Shorten the translation to at most 8 characters so it fits the original box (the current translation of 10 characters overflows its box; the minimum allowed size is 55%) | 左右 | Left/Right |
| error | 72 | p71_s11 | Shorten the translation to at most 5 characters so it fits the original box (the current translation of 8 characters overflows its box; the minimum allowed size is 55%) | 小红 | Xiaohong |
| error | 72 | p71_s11 | Shorten the translation to at most 5 characters so it fits the original box (the current translation of 8 characters overflows its box; the minimum allowed size is 55%) | 小红 | Xiaohong |
| error | 78 | p77_s1 | Shorten the translation to at most 13 characters so it fits the original box (the current translation of 16 characters overflows its box; the minimum allowed size is 55%) | 古人计数 | Ancient Counting |
| error | 78 | p77_s1 | Shorten the translation to at most 13 characters so it fits the original box (the current translation of 16 characters overflows its box; the minimum allowed size is 55%) | 古人计数 | Ancient Counting |
| warning | 33 | p32_s6 | The translation overflows its box and was rendered at 48% of the original size; even a much shorter text would not fit, check this box in the preview | 支。 | fewer. |
| warning | 33 | p32_s6 | The translation overflows its box and was rendered at 48% of the original size; even a much shorter text would not fit, check this box in the preview | 支。 | fewer. |
| warning | 56 | p55_s8 | The translation overflows its box and was rendered at 38% of the original size; even a much shorter text would not fit, check this box in the preview | 画 | Draw |
| warning | 56 | p55_s8 | The translation overflows its box and was rendered at 38% of the original size; even a much shorter text would not fit, check this box in the preview | 画 | Draw |
| warning | 63 | p62_s1 | The translation overflows its box and was rendered at 33% of the original size; even a much shorter text would not fit, check this box in the preview | 语 | Chinese |
| warning | 63 | p62_s1 | The translation overflows its box and was rendered at 33% of the original size; even a much shorter text would not fit, check this box in the preview | 语 | Chinese |
| warning | 63 | p62_s15 | The translation overflows its box and was rendered at 48% of the original size; even a much shorter text would not fit, check this box in the preview | 语文 | Chinese |
| warning | 63 | p62_s15 | The translation overflows its box and was rendered at 48% of the original size; even a much shorter text would not fit, check this box in the preview | 语文 | Chinese |
| warning | 63 | p62_s2 | The translation overflows its box and was rendered at 54% of the original size; even a much shorter text would not fit, check this box in the preview | 数学 | Maths |
| warning | 63 | p62_s2 | The translation overflows its box and was rendered at 54% of the original size; even a much shorter text would not fit, check this box in the preview | 数学 | Maths |
| warning | 63 | p62_s6 | The translation overflows its box and was rendered at 28% of the original size; even a much shorter text would not fit, check this box in the preview | 语 | Chinese |
| warning | 63 | p62_s6 | The translation overflows its box and was rendered at 28% of the original size; even a much shorter text would not fit, check this box in the preview | 语 | Chinese |
| warning | 72 | p71_s13 | The translation overflows its box and was rendered at 42% of the original size; even a much shorter text would not fit, check this box in the preview | 小强 | Xiaoqiang |
| warning | 72 | p71_s13 | The translation overflows its box and was rendered at 42% of the original size; even a much shorter text would not fit, check this box in the preview | 小强 | Xiaoqiang |
| warning | 99 | p98_s9 | The translation overflows its box and was rendered at 48% of the original size; even a much shorter text would not fit, check this box in the preview | 饼干 | Cookies |
| warning | 99 | p98_s9 | The translation overflows its box and was rendered at 48% of the original size; even a much shorter text would not fit, check this box in the preview | 饼干 | Cookies |

### `llm_review` — 18 errors, 31 warnings

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
| error | 53 | p52_s14 | Reviewer (meaning): '摆一摆' means to arrange/manipulate objects, but the more natural textbook wording is 'Use objects to represent and calculate' or 'Show and calculate'. Suggested translation: "7. Arrange and calculate." | 7.摆一摆，算一算。 | 7. Arrange and calculate. |
| error | 58 | p57_s4 | Reviewer (omission): '一共有' followed by '只动物' is split across items; the translation 'There are' + 'animals in total' is fine, but '一共有' alone should include the blank/number placeholder if present in source. | 一共有 | There are |
| error | 61 | p60_s11 | Reviewer (omission): The final clause 'they are all' has no completion, and the ellipsis placement differs from the source; the sentence ends with '它们都是' requiring the category word. Suggested translation: "Put the balls, toy cars and ······ together; they are all" | 把球、小汽车和······放在一起它们都是 | Put the balls, toy cars and ······ together; they are all |
| error | 78 | p77_s7 | Reviewer (terminology): '10个一' should be '10 ones' with singular 'one', matching place-value terminology; '10 ones' uses plural incorrectly in this counting sense. Suggested translation: "10 ones" | 10个一 | 10 ones |
| error | 85 | p84_s1 | Reviewer (untranslated): The source "mmhwn" is left untranslated; this is a garbled/placeholder-like fragment but should be rendered or flagged as a placeholder consistently. | mmhwn | mmhwn |
| error | 85 | p84_s2 | Reviewer (untranslated): The source "mmy" is left untranslated; it should be handled as a placeholder rather than kept verbatim. | mmy | mmy |
| error | 92 | p91_s2 | Reviewer (terminology): 'on Taoqi's campus' — 校园 is school campus; 'school' or 'campus' both fine, but 'campus' is not usually used for a primary school. Consider 'at Taoqi's school'. Suggested translation: "Can you find math problems at Taoqi's school?" | 你能找到淘气校园里的数学问题吗？ | Can you find math problems on Taoqi's campus? |
| error | 95 | p94_s8 | Reviewer (meaning): '还摸吗？' means 'Should I/we draw another?' The translation 'Draw again?' is a command, changing the meaning from a question about whether to draw more. Suggested translation: "3, 5. Should I draw another?" | 3，5。还摸吗？ | 3, 5. Draw again? |
| error | 96 | p95_s9 | Reviewer (untranslated): 'ii ip' is a scan artifact. It should probably be a clock-face description or left as a placeholder; keeping it is questionable but it is not translatable text. | ii ip | ii ip |
| warning | 8 | p7_s6 | Reviewer (format): Heading fragment missing final period; also "it" is an addition not present in the source. Suggested translation: "Find and talk about" | 找一找，说一说 | Find and talk about it |
| warning | 11 | p10_s2 | Reviewer (grammar): The sentence is left incomplete in English; it should read naturally as a statement of counting. Suggested translation: "1, 2, 3, 4, there are" | 1，2，3，4，有 | 1, 2, 3, 4, there are |
| warning | 15 | p14_s2 | Reviewer (grammar): Missing the object of "do" relative to the source 做一做; earlier parallel item reads "Think and do it." Suggested translation: "Think and do." | 想一想，做一做 | Think and do. |
| warning | 16 | p15_s2 | Reviewer (grammar): "Find and talk about it" is awkward; use "Find and say." Suggested translation: "Find and say." | 找一找，说一说 | Find and talk about it. |
| warning | 16 | p15_s4 | Reviewer (grammar): "Jump and talk about it" is awkward; use "Jump and say." Suggested translation: "Jump and say." | 跳一跳，说一说。 | Jump and talk about it. |
| warning | 25 | p24_s7 | Reviewer (format): “比一比，填一填” has no final period in the source; the translation adds one. Consistency with other labels is minor. Suggested translation: "Compare and fill in" | 比一比，填一填 | Compare and fill in. |
| warning | 30 | p29_s1 | Reviewer (format): The source '4.说一说。' keeps its period and marker; the translation keeps it correctly, but the numbering convention for this item should match the source exactly. Suggested translation: "4. Talk about it." | 4.说一说。 | 4. Talk about it. |
| warning | 35 | p34_s21 | Reviewer (format): The source '4.说一说。' includes a period; the translation keeps the numbering but the sentence punctuation should match the source. Suggested translation: "4. Talk about it." | 4.说一说。 | 4. Talk about it. |
| warning | 51 | p50_s3 | Reviewer (format): '10 children' is fine; no issue. | 4. 10个小朋友做游戏。 | 4. 10 children are playing a game. |
| warning | 54 | p53_s31 | Reviewer (grammar): 'Taoqi made' is acceptable; more natural: 'Here is the addition table Taoqi made.' | 下面是淘气做的加法表，你能帮他填完整吗？ | Below is the addition table Taoqi made. Can you help him co… |
| warning | 58 | p57_s5 | Reviewer (grammar): 'animals in total.' is fine as a fragment, but 'animals.' with 'in total' in the previous item may be more natural. | 只动物。 | animals in total. |
| warning | 59 | p58_s4 | Reviewer (grammar): Missing end punctuation; also 'fill in' needs an object in textbook style. Suggested translation: "7. Think and fill in the blanks" | 7.想一想，填一填 | 7. Think and fill in |
| warning | 63 | p62_s14 | Reviewer (grammar): Standalone label 'Chinese' is fine but should match the format of other labels; no change needed if the split-label rendering is intentional. | 语文 | Chinese |
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
