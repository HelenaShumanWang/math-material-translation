# QA report

**Result:** QA FAILED after 3 rounds: 241 errors, 161 warnings (1929.5 s); proofread: 769 corrections applied; output file checks: 0 error(s)

**Document:** 数 (zh → en, 109 page(s), 1777 translatable segment(s))

**Checks run:** `completeness`, `placeholders`, `numbers`, `untranslated`, `target_script`, `glossary`, `length_ratio`, `formatting`, `layout_fit`, `image_text`, `llm_review`, `output_checks`

## Rounds

| Round | Errors | Warnings | Re-translated | Passed | Duration |
|---|---|---|---|---|---|
| 1 | 385 | 280 | 355 segment(s) | no | 497.1 s |
| 2 | 306 | 286 | 268 segment(s) | no | 472.1 s |
| 3 | 288 | 332 | 0 segment(s) | no | 182.5 s |

- Round 1: llm_review ×504, layout_fit ×106, formatting ×26, completeness ×9, glossary ×5, numbers ×5, untranslated ×3, image_text ×2, length_ratio ×2, target_script ×2, placeholders ×1
- Round 2: llm_review ×485, layout_fit ×71, untranslated ×12, target_script ×8, formatting ×7, glossary ×4, image_text ×2, length_ratio ×2, completeness ×1
- Round 3: llm_review ×507, layout_fit ×87, formatting ×12, length_ratio ×4, completeness ×3, image_text ×2, target_script ×2, untranslated ×2, glossary ×1

## Final issues (402)

### `completeness` — 9 errors, 0 warnings

| Severity | Page | Segment | Message | Source | Translation |
|---|---|---|---|---|---|
| error | 21 | p20_s14 | The translation "," contains no words; translate the complete source text | 面， | , |
| error | 29 | p28_s20 | The translation "." contains no words; translate the complete source text | 千五百年。 | . |
| error | 29 | p28_s21 | The translation "." contains no words; translate the complete source text | 百七十年。 | . |
| error | 36 | p35_s21 | The translation "()" contains no words; translate the complete source text | （）个 | () |
| error | 72 | p71_s17 | The translation "□" contains no words; translate the complete source text | 〇个 | □ |
| error | 72 | p71_s18 | The translation "□" contains no words; translate the complete source text | 〇个 | □ |
| error | 91 | p90_s10 | The translation "() () ()" contains no words; translate the complete source text | ）个（）个（）个 | () () () |
| error | 91 | p90_s14 | The translation ")," contains no words; translate the complete source text | ）个， | ), |
| error | 93 | p92_s13 | The translation ")." contains no words; translate the complete source text | ）的 | ). |

### `formatting` — 46 errors, 6 warnings

| Severity | Page | Segment | Message | Source | Translation |
|---|---|---|---|---|---|
| error | 5 | p4_s1 | Keep the line breaks of the source: it has 0 line break(s), the translation has 2 | 去年今年集118棵316棵226棵435棵 | Last year This year 118 316 226 435 |
| error | 6 | p5_s6 | Keep the line breaks of the source: it has 0 line break(s), the translation has 2 | 盘：6个2盘：12个3盘：18个 | 1 plate: 6 2 plates: 12 3 plates: 18 |
| error | 7 | p6_s11 | Start the translation with the list marker "(2)" exactly as in the source | (2) 36个气球，每6个绑成一束，可以绑成 | Tie (2) 36 balloons in bunches of 6. You can make |
| error | 14 | p13_s8 | Keep the line breaks of the source: it has 0 line break(s), the translation has 2 | 1条船：4人3条船：12人5条船：20人 | 1 boat: 4 3 boats: 12 5 boats: 20 |
| error | 14 | p13_s9 | Keep the line breaks of the source: it has 0 line break(s), the translation has 2 | 2条船：8人4条船：16人剩2人 | 2 boats: 8 4 boats: 16 2 people left |
| error | 17 | p16_s2 | Keep the line breaks of the source: it has 0 line break(s), the translation has 2 | 21张卡片，平均分给4个小朋友，每人分到张，还剩 | 4 children share 21 cards equally. Each gets cards and |
| error | 17 | p16_s21 | "(pieces)" is not a translation of a measure word: write the plural noun of the counted thing ((apples), (chicks), (sticks)) or, when the exercise does not name it, drop the parentheses | 50块 | 50 (pieces) |
| error | 23 | p22_s13 | The source does not end with a question mark; do not end the translation with one | 这么多，怎么数呀！ | So many! How can we count them? |
| error | 25 | p24_s0 | The source does not end with a question mark; do not end the translation with one | 3.估一估，圈一圈，大约有多少个○96.0.0 | 3. Estimate and circle. About how many 96.0.0 are there? |
| error | 25 | p24_s0 | Keep the symbol(s) ○ of the source in the translation, at the matching position | 3.估一估，圈一圈，大约有多少个○96.0.0 | 3. Estimate and circle. About how many 96.0.0 are there? |
| error | 31 | p30_s17 | Keep the line breaks of the source: it has 0 line break(s), the translation has 2 | 黄山泰山华山 | Huangshan Taishan Huashan |
| error | 34 | p33_s0 | The source does not end with a question mark; do not end the translation with one | 有多少个字 | How Many Words? |
| error | 38 | p37_s1 | The source does not end with a question mark; do not end the translation with one | 铅笔有多长 | How Long Is the Pencil? |
| error | 40 | p39_s0 | The source does not end with a question mark; do not end the translation with one | 千米有多长 | How Long Is a Kilometre? |
| error | 42 | p41_s14 | Keep the line breaks of the source: it has 0 line break(s), the translation has 4 | 光明小学育才小学前进小学胜利小学黄村小学 | Guangming Yucai Qianjin Shengli Huangcun |
| error | 44 | p43_s21 | Keep the list marker "③" at the start of the translation (found "⑤") | ③试验田在居住区的西北方。 | ⑤ The experimental field is to the northwest of the residen… |
| error | 46 | p45_s12 | Keep the line breaks of the source: it has 0 line break(s), the translation has 3 | 我的估计厘米毫米分米 | My estimate cm mm dm |
| error | 46 | p45_s13 | Keep the line breaks of the source: it has 0 line break(s), the translation has 3 | 我的测量—厘米—毫米毫米分米—厘米 | My measurement ____ cm ____ mm ____ mm ____ dm ____ cm |
| error | 46 | p45_s14 | Keep the line breaks of the source: it has 0 line break(s), the translation has 3 | 我的铅笔长我的书厚我的凳子高我喜欢的物品的长度 | Length of my pencil Thickness of my book Height of my stool… |
| error | 46 | p45_s4 | Keep the line breaks of the source: it has 0 line break(s), the translation has 2 | 4分米=6千米=50毫米= | 4 dm = =6 km = =50 mm = |
| error | 46 | p45_s7 | Keep the line breaks of the source: it has 0 line break(s), the translation has 2 | 千米毫米分米 | km mm dm |
| error | 49 | p48_s1 | Keep the line breaks of the source: it has 0 line break(s), the translation has 2 | 回收奖励___二年级回收废电池情况200节废电池奖励10把手电筒240节废电池奖励1个足球 | Recycling rewards Grade 2 battery recycling 200 batteries: … |
| error | 49 | p48_s11 | Start the translation with the list marker "（1）" exactly as in the source | （1）班和(2）班一共····· | Class 1 and Class 2 together····· |
| error | 49 | p48_s13 | Start the translation with the list marker "(3）" exactly as in the source | (3）班一个班就一百四十多了，加上（1班的肯定 | Class 3 alone has over 140, so with Class 1 it will surely … |
| error | 49 | p48_s14 | Start the translation with the list marker "（1）" exactly as in the source | （1）班和（2）班一共回收多少节废电池？ | How many batteries did Class 1 and Class 2 recycle in total? |
| error | 49 | p48_s21 | Start the translation with the list marker "（1）" exactly as in the source | （1）班和（3）班一共回收多少节废电池？ | How many batteries did Class 1 and Class 3 recycle in total? |
| error | 50 | p49_s25 | The source ends with a question mark; end the translation with a question mark too | (2)算一算，从笑笑家到学校要走多少米？ | (2) Work out how many metres it is from Xiaoxiao's home to … |
| error | 50 | p49_s7 | Keep the line breaks of the source: it has 0 line break(s), the translation has 2 | 去年今年118棵316棵226棵435棵 | Last year This year 118 316 226 435 |
| error | 58 | p57_s17 | The source ends with a question mark; end the translation with a question mark too | 和同伴说一说，每228.24.0一步算得都对吗？ | Talk with your partner. Is every step worked out correctly?… |
| error | 69 | p68_s3 | The source ends with a question mark; end the translation with a question mark too | 说一说，下面哪些角是直角？ | Say which of the angles below are right angles. |
| error | 72 | p71_s17 | Remove the symbol(s) □: they are not in the source (a picture in the book is not a symbol; leave it out rather than inventing one) | 〇个 | □ |
| error | 72 | p71_s18 | Remove the symbol(s) □: they are not in the source (a picture in the book is not a symbol; leave it out rather than inventing one) | 〇个 | □ |
| error | 75 | p74_s4 | The source ends with a question mark; end the translation with a question mark too | 说一说，下面的两幅作品是如何设计的？ | Talk about how the two designs below were made. |
| error | 77 | p76_s6 | The source does not end with a question mark; do not end the translation with one | 还有 | Any others? |
| error | 79 | p78_s11 | The source ends with a question mark; end the translation with a question mark too | 与同伴说一说，你是怎么认的？ | Tell your partner how you read the time. |
| error | 79 | p78_s4 | The source ends with a question mark; end the translation with a question mark too | 说一说，关于钟面你知道些什么？ | Say what you know about the clock face. |
| error | 81 | p80_s0 | The source does not end with a question mark; do not end the translation with one | 分有多长 | minute: how long? |
| error | 90 | p89_s14 | Keep the line breaks of the source: it has 0 line break(s), the translation has 2 | 喜欢356.26.0的有（）人，喜欢喜欢356.28.0的有（）人，喜欢的有（）人，可以选（）作为吉祥物。 | () people like 356.26.0, () people like 356.28.0, () pe… |
| error | 91 | p90_s12 | Keep the symbol(s) △ ● of the source in the translation, at the matching position | ）个，比●360.22.0多（）个，比△少360.25.0（） | ) and more than 360.22.0 by ( ) and less than 360.25.0 … |
| error | 91 | p90_s4 | Keep the line breaks of the source: it has 0 line break(s), the translation has 3 | 相声魔术杂技歌舞 | Comedy Magic Acrobatics Dance |
| error | 93 | p92_s10 | Keep the line breaks of the source: it has 0 line break(s), the translation has 3 | 动物园科技馆游乐场公园 | Zoo Science museum Funfair Park |
| error | 93 | p92_s5 | Keep the line breaks of the source: it has 0 line break(s), the translation has 3 | 动物园科技馆游乐场公园 | Zoo Science museum Funfair Park |
| error | 95 | p94_s7 | The source ends with a question mark; end the translation with a question mark too | 说一说正方形、长方形有什么特点，这些特点是怎么得到的？ | say what features a square and a rectangle have and how you… |
| error | 96 | p95_s3 | The source does not end with a question mark; do not end the translation with one | 3.将41个鸡蛋全部放在蛋托里，至少需要蛋托。 | 3. Put all 41 eggs in egg trays. At least how many egg tray… |
| error | 98 | p97_s34 | Start the translation with the list marker "(2)" exactly as in the source | (2)笑笑家在果园的（）方向，动物园在果园 | ((2)) Xiaoxiao's home is to the () of the orchard, and the … |
| error | 101 | p100_s0 | The source does not end with a question mark; do not end the translation with one | 本学期你学到了什么 | What have you learned this term? |
| warning | 13 | p12_s26 | The source ends with a exclamation mark; end the translation with a exclamation mark too | 3个5！ | 3 lots of 5 |
| warning | 15 | p14_s5 | The source does not end with a exclamation mark; do not end the translation with one | 哦，我明白了 | Oh, I see! |
| warning | 23 | p22_s13 | The source ends with a exclamation mark; end the translation with a exclamation mark too | 这么多，怎么数呀！ | So many! How can we count them? |
| warning | 24 | p23_s1 | The source ends with a exclamation mark; end the translation with a exclamation mark too | 想一想，再大致圈出一千个！ | Think first, then circle about one thousand squares. |
| warning | 81 | p80_s8 | The source ends with a exclamation mark; end the translation with a exclamation mark too | 1分大约拍—下。！ | About ___ claps in 1 minute. |
| warning | 86 | p85_s2 | The source does not end with a exclamation mark; do not end the translation with one | 我去上学了，再见 | I'm going to school. Bye! |

### `glossary` — 11 errors, 0 warnings

| Severity | Page | Segment | Message | Source | Translation |
|---|---|---|---|---|---|
| error | 9 | p8_s9 | Glossary: translate "小棒" as "sticks" | 2.用小棒搭 | 2. Build |
| error | 27 | p26_s1 | Glossary: translate "计数器" as "counting frame" | 1.一百一百地数，从八千九百数到一万，并在计数器上拨 | 1. Count by hundreds from eight thousand nine hundred to te… |
| error | 50 | p49_s25 | Glossary: translate "算一算" as "Calculate" | (2)算一算，从笑笑家到学校要走多少米？ | (2) Work out how many metres it is from Xiaoxiao's home to … |
| error | 53 | p52_s21 | Glossary: translate "算式" as "number sentence" | 说一个算式“239一57”育 | Make up a problem that "239 − 57" |
| error | 53 | p52_s22 | Glossary: translate "算一算" as "Calculate" | 能解决的问题，并算一算。 | can solve, and work it out. |
| error | 78 | p77_s7 | Glossary: translate "直角" as "right angle" | 锐角直角钝角 | acute right obtuse |
| error | 78 | p77_s7 | Glossary: translate "钝角" as "obtuse angle" | 锐角直角钝角 | acute right obtuse |
| error | 78 | p77_s7 | Glossary: translate "锐角" as "acute angle" | 锐角直角钝角 | acute right obtuse |
| error | 90 | p89_s4 | Glossary: translate "统计" as "statistics" | 统计最喜欢每种动物的人数，可以让大家举手····· | To count how many people like each animal best, we can ask … |
| error | 95 | p94_s9 | Glossary: translate "比一比" as "Compare" | 长方形四个角都是直角，我是用三角板比一比得到的··· | All four angles of a rectangle are right angles. I checked … |
| error | 98 | p97_s24 | Glossary: translate "笑笑" as "Xiaoxiao" | （1）邮局在果园的（面，书店在笑笑家的 | (1) The post office is to the () of the orchard, and the bo… |

### `layout_fit` — 84 errors, 30 warnings

| Severity | Page | Segment | Message | Source | Translation |
|---|---|---|---|---|---|
| error | 3 | p2_s10 | Shorten the translation to at most 23 characters so it fits the original box (the current translation of 27 characters overflows its box; the minimum allowed size is 55%) | 2任何数乘0都为0。 | 2. Any number times 0 is 0. |
| error | 3 | p2_s10 | Shorten the translation to at most 23 characters so it fits the original box (the current translation of 27 characters overflows its box; the minimum allowed size is 55%) | 2任何数乘0都为0。 | 2. Any number times 0 is 0. |
| error | 3 | p2_s6 | Shorten the translation to at most 13 characters so it fits the original box (the current translation of 15 characters overflows its box; the minimum allowed size is 55%) | 数宇魔法师 | Number Magician |
| error | 3 | p2_s6 | Shorten the translation to at most 13 characters so it fits the original box (the current translation of 15 characters overflows its box; the minimum allowed size is 55%) | 数宇魔法师 | Number Magician |
| error | 3 | p2_s7 | Shorten the translation to at most 20 characters so it fits the original box (the current translation of 41 characters overflows its box; the minimum allowed size is 55%) | 1.任何数加减0都没有变化。 | 1. Add or subtract 0 and nothing changes. |
| error | 3 | p2_s7 | Shorten the translation to at most 20 characters so it fits the original box (the current translation of 41 characters overflows its box; the minimum allowed size is 55%) | 1.任何数加减0都没有变化。 | 1. Add or subtract 0 and nothing changes. |
| error | 4 | p3_s5 | Shorten the translation to at most 20 characters so it fits the original box (the current translation of 24 characters overflows its box; the minimum allowed size is 55%) | 12.8.0打谷场 | 12.8.0 Threshing Floor |
| error | 4 | p3_s5 | Shorten the translation to at most 20 characters so it fits the original box (the current translation of 24 characters overflows its box; the minimum allowed size is 55%) | 12.8.0打谷场 | 12.8.0 Threshing Floor |
| error | 4 | p3_s6 | Shorten the translation to at most 25 characters so it fits the original box (the current translation of 29 characters overflows its box; the minimum allowed size is 55%) | 二 方向与位置 | Unit 2 Direction and Position |
| error | 4 | p3_s6 | Shorten the translation to at most 25 characters so it fits the original box (the current translation of 29 characters overflows its box; the minimum allowed size is 55%) | 二 方向与位置 | Unit 2 Direction and Position |
| error | 6 | p5_s1 | Shorten the translation to at most 12 characters so it fits the original box (the current translation of 14 characters overflows its box; the minimum allowed size is 55%) | 分苹果 | Sharing Apples |
| error | 6 | p5_s1 | Shorten the translation to at most 12 characters so it fits the original box (the current translation of 14 characters overflows its box; the minimum allowed size is 55%) | 分苹果 | Sharing Apples |
| error | 8 | p7_s13 | Shorten the translation to at most 10 characters so it fits the original box (the current translation of 15 characters overflows its box; the minimum allowed size is 55%) | 算式 | Number sentence |
| error | 8 | p7_s13 | Shorten the translation to at most 10 characters so it fits the original box (the current translation of 15 characters overflows its box; the minimum allowed size is 55%) | 算式 | Number sentence |
| error | 9 | p8_s12 | Shorten the translation to at most 12 characters so it fits the original box (the current translation of 15 characters overflows its box; the minimum allowed size is 55%) | 算式人 | Number sentence |
| error | 9 | p8_s12 | Shorten the translation to at most 12 characters so it fits the original box (the current translation of 15 characters overflows its box; the minimum allowed size is 55%) | 算式人 | Number sentence |
| error | 9 | p8_s14 | Shorten the translation to at most 12 characters so it fits the original box (the current translation of 15 characters overflows its box; the minimum allowed size is 55%) | 算式 | Number sentence |
| error | 9 | p8_s14 | Shorten the translation to at most 12 characters so it fits the original box (the current translation of 15 characters overflows its box; the minimum allowed size is 55%) | 算式 | Number sentence |
| error | 12 | p11_s0 | Shorten the translation to at most 16 characters so it fits the original box (the current translation of 20 characters overflows its box; the minimum allowed size is 55%) | 分草莓 | Sharing Strawberries |
| error | 12 | p11_s0 | Shorten the translation to at most 16 characters so it fits the original box (the current translation of 20 characters overflows its box; the minimum allowed size is 55%) | 分草莓 | Sharing Strawberries |
| error | 14 | p13_s4 | Shorten the translation to at most 57 characters so it fits the original box (the current translation of 65 characters overflows its box; the minimum allowed size is 55%) | 说一说，你从图中知道了哪些数学信息？ | Talk about it: what math information can you find in the pi… |
| error | 14 | p13_s4 | Shorten the translation to at most 57 characters so it fits the original box (the current translation of 65 characters overflows its box; the minimum allowed size is 55%) | 说一说，你从图中知道了哪些数学信息？ | Talk about it: what math information can you find in the pi… |
| error | 17 | p16_s21 | Shorten the translation to at most 9 characters so it fits the original box (the current translation of 11 characters overflows its box; the minimum allowed size is 55%) | 50块 | 50 (pieces) |
| error | 17 | p16_s21 | Shorten the translation to at most 9 characters so it fits the original box (the current translation of 11 characters overflows its box; the minimum allowed size is 55%) | 50块 | 50 (pieces) |
| error | 18 | p17_s13 | Shorten the translation to at most 16 characters so it fits the original box (the current translation of 19 characters overflows its box; the minimum allowed size is 55%) | 个，还剩 | dustpans, remainder |
| error | 18 | p17_s13 | Shorten the translation to at most 16 characters so it fits the original box (the current translation of 19 characters overflows its box; the minimum allowed size is 55%) | 个，还剩 | dustpans, remainder |
| error | 19 | p18_s30 | Shorten the translation to at most 6 characters so it fits the original box (the current translation of 10 characters overflows its box; the minimum allowed size is 55%) | 操场 | Playground |
| error | 19 | p18_s30 | Shorten the translation to at most 6 characters so it fits the original box (the current translation of 10 characters overflows its box; the minimum allowed size is 55%) | 操场 | Playground |
| error | 22 | p21_s29 | Shorten the translation to at most 10 characters so it fits the original box (the current translation of 17 characters overflows its box; the minimum allowed size is 55%) | 天津山东 | Tianjin, Shandong |
| error | 22 | p21_s29 | Shorten the translation to at most 10 characters so it fits the original box (the current translation of 17 characters overflows its box; the minimum allowed size is 55%) | 天津山东 | Tianjin, Shandong |
| error | 26 | p25_s9 | Shorten the translation to at most 17 characters so it fits the original box (the current translation of 20 characters overflows its box; the minimum allowed size is 55%) | 千三千、三千 | 1,000, 2,000, 3,000… |
| error | 26 | p25_s9 | Shorten the translation to at most 17 characters so it fits the original box (the current translation of 20 characters overflows its box; the minimum allowed size is 55%) | 千三千、三千 | 1,000, 2,000, 3,000… |
| error | 31 | p30_s11 | Shorten the translation to at most 13 characters so it fits the original box (the current translation of 19 characters overflows its box; the minimum allowed size is 55%) | 黄山香山 | Huangshan Xiangshan |
| error | 31 | p30_s11 | Shorten the translation to at most 13 characters so it fits the original box (the current translation of 19 characters overflows its box; the minimum allowed size is 55%) | 黄山香山 | Huangshan Xiangshan |
| error | 31 | p30_s2 | Shorten the translation to at most 5 characters so it fits the original box (the current translation of 9 characters overflows its box; the minimum allowed size is 55%) | 香山 | Xiangshan |
| error | 31 | p30_s2 | Shorten the translation to at most 5 characters so it fits the original box (the current translation of 9 characters overflows its box; the minimum allowed size is 55%) | 香山 | Xiangshan |
| error | 31 | p30_s24 | Shorten the translation to at most 14 characters so it fits the original box (the current translation of 17 characters overflows its box; the minimum allowed size is 55%) | 黄山泰山 | Huangshan Taishan |
| error | 31 | p30_s24 | Shorten the translation to at most 14 characters so it fits the original box (the current translation of 17 characters overflows its box; the minimum allowed size is 55%) | 黄山泰山 | Huangshan Taishan |
| error | 35 | p34_s11 | Shorten the translation to at most 24 characters so it fits the original box (the current translation of 29 characters overflows its box; the minimum allowed size is 55%) | 136.18.0快下雨了 | 136.18.0 It will rain soon. |
| error | 35 | p34_s11 | Shorten the translation to at most 24 characters so it fits the original box (the current translation of 29 characters overflows its box; the minimum allowed size is 55%) | 136.18.0快下雨了 | 136.18.0 It will rain soon. |
| error | 40 | p39_s0 | Shorten the translation to at most 20 characters so it fits the original box (the current translation of 24 characters overflows its box; the minimum allowed size is 55%) | 千米有多长 | How Long Is a Kilometre? |
| error | 40 | p39_s0 | Shorten the translation to at most 20 characters so it fits the original box (the current translation of 24 characters overflows its box; the minimum allowed size is 55%) | 千米有多长 | How Long Is a Kilometre? |
| error | 47 | p46_s1 | Shorten the translation to at most 21 characters so it fits the original box (the current translation of 24 characters overflows its box; the minimum allowed size is 55%) | 加与减 | Addition and Subtraction |
| error | 47 | p46_s1 | Shorten the translation to at most 21 characters so it fits the original box (the current translation of 24 characters overflows its box; the minimum allowed size is 55%) | 加与减 | Addition and Subtraction |
| error | 47 | p46_s2 | Shorten the translation to at most 14 characters so it fits the original box (the current translation of 17 characters overflows its box; the minimum allowed size is 55%) | 买电器 | Buying Appliances |
| error | 47 | p46_s2 | Shorten the translation to at most 14 characters so it fits the original box (the current translation of 17 characters overflows its box; the minimum allowed size is 55%) | 买电器 | Buying Appliances |
| error | 48 | p47_s15 | Shorten the translation to at most 6 characters so it fits the original box (the current translation of 8 characters overflows its box; the minimum allowed size is 55%) | 周四 | Thursday |
| error | 48 | p47_s15 | Shorten the translation to at most 6 characters so it fits the original box (the current translation of 8 characters overflows its box; the minimum allowed size is 55%) | 周四 | Thursday |
| error | 49 | p48_s0 | Shorten the translation to at most 20 characters so it fits the original box (the current translation of 24 characters overflows its box; the minimum allowed size is 55%) | 回收废电池 | Recycling Used Batteries |
| error | 49 | p48_s0 | Shorten the translation to at most 20 characters so it fits the original box (the current translation of 24 characters overflows its box; the minimum allowed size is 55%) | 回收废电池 | Recycling Used Batteries |
| error | 49 | p48_s22 | Shorten the translation to at most 16 characters so it fits the original box (the current translation of 18 characters overflows its box; the minimum allowed size is 55%) | 满十进1 | Make ten, carry 1. |
| error | 49 | p48_s22 | Shorten the translation to at most 16 characters so it fits the original box (the current translation of 18 characters overflows its box; the minimum allowed size is 55%) | 满十进1 | Make ten, carry 1. |
| error | 52 | p51_s11 | Shorten the translation to at most 48 characters so it fits the original box (the current translation of 56 characters overflows its box; the minimum allowed size is 55%) | （3） 800元可以买哪两件家具？ | (3) Which two pieces of furniture can you buy with ¥800? |
| error | 52 | p51_s11 | Shorten the translation to at most 48 characters so it fits the original box (the current translation of 56 characters overflows its box; the minimum allowed size is 55%) | （3） 800元可以买哪两件家具？ | (3) Which two pieces of furniture can you buy with ¥800? |
| error | 57 | p56_s24 | Shorten the translation to at most 5 characters so it fits the original box (the current translation of 7 characters overflows its box; the minimum allowed size is 55%) | 答： | Answer: |
| error | 57 | p56_s24 | Shorten the translation to at most 5 characters so it fits the original box (the current translation of 7 characters overflows its box; the minimum allowed size is 55%) | 答： | Answer: |
| error | 61 | p60_s23 | Shorten the translation to at most 10 characters so it fits the original box (the current translation of 12 characters overflows its box; the minimum allowed size is 55%) | 水浒卡片 | Water Margin |
| error | 61 | p60_s23 | Shorten the translation to at most 10 characters so it fits the original box (the current translation of 12 characters overflows its box; the minimum allowed size is 55%) | 水浒卡片 | Water Margin |
| error | 69 | p68_s4 | Shorten the translation to at most 26 characters so it fits the original box (the current translation of 31 characters overflows its box; the minimum allowed size is 55%) | 我用三角 | I'll compare with a set square. |
| error | 69 | p68_s4 | Shorten the translation to at most 26 characters so it fits the original box (the current translation of 31 characters overflows its box; the minimum allowed size is 55%) | 我用三角 | I'll compare with a set square. |
| error | 77 | p76_s6 | Shorten the translation to at most 9 characters so it fits the original box (the current translation of 11 characters overflows its box; the minimum allowed size is 55%) | 还有 | Any others? |
| error | 77 | p76_s6 | Shorten the translation to at most 9 characters so it fits the original box (the current translation of 11 characters overflows its box; the minimum allowed size is 55%) | 还有 | Any others? |
| error | 82 | p81_s11 | Shorten the translation to at most 5 characters so it fits the original box (the current translation of 7 characters overflows its box; the minimum allowed size is 55%) | 分 | minutes |
| error | 82 | p81_s11 | Shorten the translation to at most 5 characters so it fits the original box (the current translation of 7 characters overflows its box; the minimum allowed size is 55%) | 分 | minutes |
| error | 82 | p81_s14 | Shorten the translation to at most 8 characters so it fits the original box (the current translation of 10 characters overflows its box; the minimum allowed size is 55%) | 30分 | 30 minutes |
| error | 82 | p81_s14 | Shorten the translation to at most 8 characters so it fits the original box (the current translation of 10 characters overflows its box; the minimum allowed size is 55%) | 30分 | 30 minutes |
| error | 82 | p81_s17 | Shorten the translation to at most 5 characters so it fits the original box (the current translation of 7 characters overflows its box; the minimum allowed size is 55%) | 分 | minutes |
| error | 82 | p81_s17 | Shorten the translation to at most 5 characters so it fits the original box (the current translation of 7 characters overflows its box; the minimum allowed size is 55%) | 分 | minutes |
| error | 82 | p81_s25 | Shorten the translation to at most 6 characters so it fits the original box (the current translation of 9 characters overflows its box; the minimum allowed size is 55%) | 3分 | 3 minutes |
| error | 82 | p81_s25 | Shorten the translation to at most 6 characters so it fits the original box (the current translation of 9 characters overflows its box; the minimum allowed size is 55%) | 3分 | 3 minutes |
| error | 82 | p81_s26 | Shorten the translation to at most 7 characters so it fits the original box (the current translation of 9 characters overflows its box; the minimum allowed size is 55%) | 1分 | 1 minutes |
| error | 82 | p81_s26 | Shorten the translation to at most 7 characters so it fits the original box (the current translation of 9 characters overflows its box; the minimum allowed size is 55%) | 1分 | 1 minutes |
| error | 83 | p82_s2 | Shorten the translation to at most 10 characters so it fits the original box (the current translation of 12 characters overflows its box; the minimum allowed size is 55%) | 90秒= | 90 seconds = |
| error | 83 | p82_s2 | Shorten the translation to at most 10 characters so it fits the original box (the current translation of 12 characters overflows its box; the minimum allowed size is 55%) | 90秒= | 90 seconds = |
| error | 90 | p89_s9 | Shorten the translation to at most 15 characters so it fits the original box (the current translation of 18 characters overflows its box; the minimum allowed size is 55%) | 兔猴鱼 | Rabbit Monkey Fish |
| error | 90 | p89_s9 | Shorten the translation to at most 15 characters so it fits the original box (the current translation of 18 characters overflows its box; the minimum allowed size is 55%) | 兔猴鱼 | Rabbit Monkey Fish |
| error | 91 | p90_s21 | Shorten the translation to at most 12 characters so it fits the original box (the current translation of 15 characters overflows its box; the minimum allowed size is 55%) | 只爱吃菜 | Vegetables only |
| error | 91 | p90_s21 | Shorten the translation to at most 12 characters so it fits the original box (the current translation of 15 characters overflows its box; the minimum allowed size is 55%) | 只爱吃菜 | Vegetables only |
| error | 91 | p90_s24 | Shorten the translation to at most 6 characters so it fits the original box (the current translation of 8 characters overflows its box; the minimum allowed size is 55%) | 3人 | 3 people |
| error | 91 | p90_s24 | Shorten the translation to at most 6 characters so it fits the original box (the current translation of 8 characters overflows its box; the minimum allowed size is 55%) | 3人 | 3 people |
| error | 92 | p91_s4 | Shorten the translation to at most 15 characters so it fits the original box (the current translation of 18 characters overflows its box; the minimum allowed size is 55%) | 怎么办呢？ | What should we do? |
| error | 92 | p91_s4 | Shorten the translation to at most 15 characters so it fits the original box (the current translation of 18 characters overflows its box; the minimum allowed size is 55%) | 怎么办呢？ | What should we do? |
| error | 100 | p99_s9 | Shorten the translation to at most 15 characters so it fits the original box (the current translation of 20 characters overflows its box; the minimum allowed size is 55%) | 汽车慢速中速快速 | Car Slow Medium Fast |
| error | 100 | p99_s9 | Shorten the translation to at most 15 characters so it fits the original box (the current translation of 20 characters overflows its box; the minimum allowed size is 55%) | 汽车慢速中速快速 | Car Slow Medium Fast |
| warning | 4 | p3_s0 | The translation overflows its box and was rendered at 27% of the original size; even a much shorter text would not fit, check this box in the preview | 录 | Contents |
| warning | 4 | p3_s0 | The translation overflows its box and was rendered at 27% of the original size; even a much shorter text would not fit, check this box in the preview | 录 | Contents |
| warning | 4 | p3_s1 | The translation overflows its box and was rendered at 26% of the original size; even a much shorter text would not fit, check this box in the preview | 目 | Contents |
| warning | 4 | p3_s1 | The translation overflows its box and was rendered at 26% of the original size; even a much shorter text would not fit, check this box in the preview | 目 | Contents |
| warning | 4 | p3_s12 | The translation overflows its box and was rendered at 32% of the original size; even a much shorter text would not fit, check this box in the preview | 四 | Unit 4 Measurement |
| warning | 4 | p3_s12 | The translation overflows its box and was rendered at 32% of the original size; even a much shorter text would not fit, check this box in the preview | 四 | Unit 4 Measurement |
| warning | 7 | p6_s6 | The translation overflows its box and was rendered at 43% of the original size; even a much shorter text would not fit, check this box in the preview | 烟花 | fireworks |
| warning | 7 | p6_s6 | The translation overflows its box and was rendered at 43% of the original size; even a much shorter text would not fit, check this box in the preview | 烟花 | fireworks |
| warning | 8 | p7_s9 | The translation overflows its box and was rendered at 41% of the original size; even a much shorter text would not fit, check this box in the preview | 余数 | remainder |
| warning | 8 | p7_s9 | The translation overflows its box and was rendered at 41% of the original size; even a much shorter text would not fit, check this box in the preview | 余数 | remainder |
| warning | 15 | p14_s10 | The translation overflows its box and was rendered at 43% of the original size; even a much shorter text would not fit, check this box in the preview | 答 | Answer: |
| warning | 15 | p14_s10 | The translation overflows its box and was rendered at 43% of the original size; even a much shorter text would not fit, check this box in the preview | 答 | Answer: |
| warning | 22 | p21_s22 | The translation overflows its box and was rendered at 19% of the original size; even a much shorter text would not fit, check this box in the preview | 古 | Inner Mongolia |
| warning | 22 | p21_s22 | The translation overflows its box and was rendered at 19% of the original size; even a much shorter text would not fit, check this box in the preview | 古 | Inner Mongolia |
| warning | 22 | p21_s26 | The translation overflows its box and was rendered at 49% of the original size; even a much shorter text would not fit, check this box in the preview | 内 | Inner |
| warning | 22 | p21_s26 | The translation overflows its box and was rendered at 49% of the original size; even a much shorter text would not fit, check this box in the preview | 内 | Inner |
| warning | 22 | p21_s27 | The translation overflows its box and was rendered at 21% of the original size; even a much shorter text would not fit, check this box in the preview | 陕 | Shaanxi |
| warning | 22 | p21_s27 | The translation overflows its box and was rendered at 21% of the original size; even a much shorter text would not fit, check this box in the preview | 陕 | Shaanxi |
| warning | 22 | p21_s34 | The translation overflows its box and was rendered at 35% of the original size; even a much shorter text would not fit, check this box in the preview | 江 | Jiang |
| warning | 22 | p21_s34 | The translation overflows its box and was rendered at 35% of the original size; even a much shorter text would not fit, check this box in the preview | 江 | Jiang |
| warning | 22 | p21_s37 | The translation overflows its box and was rendered at 17% of the original size; even a much shorter text would not fit, check this box in the preview | 庆 | Chongqing |
| warning | 22 | p21_s37 | The translation overflows its box and was rendered at 17% of the original size; even a much shorter text would not fit, check this box in the preview | 庆 | Chongqing |
| warning | 31 | p30_s1 | The translation overflows its box and was rendered at 43% of the original size; even a much shorter text would not fit, check this box in the preview | 黄山 | Huangshan |
| warning | 31 | p30_s1 | The translation overflows its box and was rendered at 43% of the original size; even a much shorter text would not fit, check this box in the preview | 黄山 | Huangshan |
| warning | 35 | p34_s10 | The translation overflows its box and was rendered at 39% of the original size; even a much shorter text would not fit, check this box in the preview | 有 | There is |
| warning | 35 | p34_s10 | The translation overflows its box and was rendered at 39% of the original size; even a much shorter text would not fit, check this box in the preview | 有 | There is |
| warning | 71 | p70_s18 | The translation overflows its box and was rendered at 38% of the original size; even a much shorter text would not fit, check this box in the preview | 宽 | width |
| warning | 71 | p70_s18 | The translation overflows its box and was rendered at 38% of the original size; even a much shorter text would not fit, check this box in the preview | 宽 | width |
| warning | 91 | p90_s4 | The translation overflows its box and was rendered at 33% of the original size; even a much shorter text would not fit, check this box in the preview | 相声魔术杂技歌舞 | Comedy Magic Acrobatics Dance |
| warning | 91 | p90_s4 | The translation overflows its box and was rendered at 33% of the original size; even a much shorter text would not fit, check this box in the preview | 相声魔术杂技歌舞 | Comedy Magic Acrobatics Dance |

### `llm_review` — 77 errors, 120 warnings

| Severity | Page | Segment | Message | Source | Translation |
|---|---|---|---|---|---|
| error | 1 | p0_s9 | Reviewer (untranslated): The source "北京师范大学出" is truncated but the translation adds "Press" and omits the missing character; more importantly the publisher name is rendered properly, though the source fragment lacks 版. Keep as is; the issue is that the Chinese fragment is incomplete, not the translation. Suggested translation: "Beijing Normal University Press" | 北京师范大学出 | Beijing Normal University Press |
| error | 4 | p3_s12 | Reviewer (omission): The source label 四 is the bare numeral beginning of the unit heading "四 测量"; the translation adds "Measurement" here and repeats it in p3_s13, creating a duplicated heading and dropping the bare numeral form. The unit heading should be "Unit 4 Measurement" once, and p3_s12 should not carry the title alone. Suggested translation: "Unit 4" | 四 | Unit 4 Measurement |
| error | 4 | p3_s5 | Reviewer (untranslated): The placeholder ⟦12.8.0⟧ is retained correctly, but the source has it attached before 打谷场; the translation keeps it attached before the label, which is correct. No change needed. Suggested translation: "⟦12.8.0⟧ Threshing Floor" | 12.8.0打谷场 | 12.8.0 Threshing Floor |
| error | 6 | p5_s8 | Reviewer (meaning): The source "(三)六十八" is a multiplication-table rhyme with a blank for the first factor: "( ) six eighteen" meaning 3 × 6 = 18. Rendering it as a completed fact is acceptable when the blank represents 3, but the blank form should be kept as an exercise if the source has a blank. Suggested translation: "3 × 6 = 18" | (三)六十八。 | 3 × 6 = 18 |
| error | 7 | p6_s0 | Reviewer (terminology): 练一练 is glossed as 'Practice', which matches the glossary; no problem. | 练一练 | Practice |
| error | 7 | p6_s12 | Reviewer (meaning): '束' is 'bunches'; correct. | 束。 | bunches. |
| error | 7 | p6_s2 | Reviewer (meaning): '烟花' means 'fireworks'; '12根烟花' means '12 fireworks', which is fine. | 我买了12根烟花。 | I bought 12 fireworks. |
| error | 7 | p6_s5 | Reviewer (meaning): '提出一个与除法有关的问题' means 'Ask a question related to division'; the translation drops 'related to division' nuance? It says 'a division question', which is acceptable but slightly different. Also '并尝试解答' = 'and try to solve it', not 'answer it'. Suggested translation: "Ask a question related to division and try to solve it." | 提出一个与除法有关的问题，并尝试解答。 | Ask a division question and try to answer it. |
| error | 7 | p6_s6 | Reviewer (terminology): 'fireworks' is fine. | 烟花 | fireworks |
| error | 7 | p6_s9 | Reviewer (meaning): '支' is the measure word for crayons; the translation 'crayons.' is correct. | 支。 | crayons. |
| error | 8 | p7_s13 | Reviewer (terminology): 'Number sentence' is correct for 算式. | 算式 | Number sentence |
| error | 8 | p7_s14 | Reviewer (meaning): The source '14÷4=3（个）····*2（根）' has the measure words 个 (squares) and 根 (sticks). The translation '14÷4=3 (squares)····*2 (sticks)' is correct. | 14÷4=3（个）····*2（根） | 14÷4=3 (squares)····*2 (sticks) |
| error | 8 | p7_s17 | Reviewer (meaning): The source '余数都比除数小为什么？' means 'The remainder is always smaller than the divisor. Why?' The translation adds a period and is correct. | 余数都比除数小为什么？ | The remainder is always smaller than the divisor. Why? |
| error | 8 | p7_s7 | Reviewer (meaning): The source '13÷4=3（个）' has the measure word 个 after the answer, meaning '3 squares' (since the context is squares). The translation '13÷4=3 (squares)' is correct. | 13÷4=3（个） | 13÷4=3 (squares) |
| error | 8 | p7_s9 | Reviewer (terminology): 'remainder' is correct for 余数. | 余数 | remainder |
| error | 9 | p8_s0 | Reviewer (terminology): 'Practice' is correct. | 练一练 | Practice |
| error | 9 | p8_s11 | Reviewer (meaning): The source '小棒根数搭成的32.18.0' contains a placeholder '32.18.0'; the translation keeps it but should render it as ⟦0⟧. Suggested translation: "Number of sticks, squares built ⟦0⟧" | 小棒根数搭成的32.18.0 | Number of sticks, squares built 32.18.0 |
| error | 9 | p8_s12 | Reviewer (meaning): The source '算式人' has an extra character '人'; the translation 'Number sentence' is fine. | 算式人 | Number sentence |
| error | 9 | p8_s13 | Reviewer (meaning): The source '小棒根数搭成的32.20.0' contains a placeholder; the translation keeps it but should render it as ⟦0⟧. Suggested translation: "Number of sticks, squares built ⟦0⟧" | 小棒根数搭成的32.20.0 | Number of sticks, squares built 32.20.0 |
| error | 9 | p8_s14 | Reviewer (terminology): 'Number sentence' is correct. | 算式 | Number sentence |
| error | 9 | p8_s19 | Reviewer (number): The source '33÷4=8（根）····.1（根）' appears to have an error: 33÷4=8 (sticks)····1 (sticks) — but 33÷4=8⅟₄, so the quotient is 8 remainder 1. The translation '33÷4=8 (squares) ····.1 (sticks)' mistranslates the first measure word 根 as 'squares' (should be 'sticks'? But the context is squares; the source says 根, which means sticks). Suggested translation: "33÷4=8 (sticks)····1 (sticks)" | 33÷4=8（根）····.1（根） | 33÷4=8 (squares) ····.1 (sticks) |
| error | 18 | p17_s17 | Reviewer (meaning): "钉" means sew/attach buttons onto jackets ("fasten" implies buttoning up), which changes the action and the answer interpretation. Suggested translation: "(2) With 27 buttons, how many jackets can buttons be sewn onto at most?" | （2） 27粒扣子最多可以钉几件上衣？ | (2) With 27 buttons, how many jackets can be fastened at mo… |
| error | 22 | p21_s25 | Reviewer (untranslated): '丁夏' appears to be mis-scanned '宁夏' (Ningxia). Translating it as 'Dingxia' is not a real place name; it should be 'Ningxia'. Suggested translation: "Ningxia" | 丁夏 | Dingxia |
| error | 22 | p21_s33 | Reviewer (meaning): The source '安苏' (abbreviation for 安徽江苏, Anhui and Jiangsu) names two provinces; the translation keeps only Anhui. Suggested translation: "Anhui Jiangsu" | 安苏 | Anhui |
| error | 22 | p21_s41 | Reviewer (omission): The source list includes 二 (the numeral/punctuation between Guangdong and Hong Kong), which is omitted in the translation. Suggested translation: "Guangdong 2 Hong Kong Macao Hainan" | 广东二香港澳门海南 | Guangdong Hong Kong Macao Hainan |
| error | 23 | p22_s10 | Reviewer (untranslated): The source '白' is left untranslated; it should be rendered. Suggested translation: "White" | 白 | H |
| error | 23 | p22_s19 | Reviewer (omission): The source ellipsis '··' is missing in the translation. Suggested translation: "I count one by one: eight hundred eighty-seven, eight hundred eighty-eight, eight hundred eighty-nine ··" | 我一个一个地数，八百八十七，八百八十八，八百八十九·· | I count one by one: eight hundred eighty-seven, eight hundr… |
| error | 23 | p22_s3 | Reviewer (number): The source ellipsis '·' is dropped; the translation should keep the trailing punctuation. Suggested translation: "9 beads plus 1 more·" | 9个珠子再添上1个.· | 9 beads plus 1 more... |
| error | 27 | p26_s9 | Reviewer (untranslated): The string '104.13.0' is untranslated and appears to be an artifact or incorrect content; the source has a placeholder picture or answer box there. Suggested translation: "2. Talk about it. How many are there?" | 2.说一说，有多少个口？104.13.0 | 2. Talk about it. How many 104.13.0 are there? |
| error | 31 | p30_s16 | Reviewer (untranslated): The single-character place-value label 个 (ones place) must use the standard abbreviation "O", but the translation gives the letter "O" which is fine as the abbreviation — however this is a label of a counting frame and the standard abbreviation for 个 is "O"; the provided translation "O" is correct. No finding. | 个 | O |
| error | 31 | p30_s22 | Reviewer (number): The source lists five column labels 万千百十个; the translation omits the ones-place label and gives only "TTh Th H T", but p30_s16/s23 separately render 个 as "O". This fragment should include all five labels. Suggested translation: "TTh Th H T O" | 万千百十 | TTh Th H T |
| error | 32 | p31_s15 | Reviewer (terminology): Measure word 根 counts corn cobs/stalks; "cobs" is acceptable, but the same measure word must be rendered consistently across p31_s15–s18. Suggested translation: "1503 cobs" | 1503根 | 1503 cobs |
| error | 33 | p32_s7 | Reviewer (omission): "一人想数" means "one person thinks of a number"; the translation drops the object "a number". Suggested translation: "(1) In pairs, one person thinks of a number" | （1）两人一组，一人想数 | (1) In pairs, one person thinks of a number |
| error | 34 | p33_s9 | Reviewer (terminology): 估计 is rendered "estimate" rather than the glossary verb "Estimate" for 估一估. Suggested translation: "Work in groups, estimate and discuss." | 小组合作，估一估，说一说。 | Work in groups, estimate and discuss. |
| error | 35 | p34_s13 | Reviewer (terminology): 糖豆 is "candy beans" but "jelly beans" is acceptable; minor wording preference. Suggested translation: "3. Estimate: how many jelly beans are there?" | 3.估一估，有多少颗糖豆？ | 3. Estimate: how many jelly beans are there? |
| error | 35 | p34_s18 | Reviewer (terminology): 说一说 rendered "talk about it" deviates from the pattern "discuss" used elsewhere. Suggested translation: "Estimate and discuss." | 估一估，说一说。 | Estimate and talk about it. |
| error | 36 | p35_s18 | Reviewer (terminology): 千百 should be abbreviated TTh Th (ten-thousands and thousands), not "Th H". Suggested translation: "TTh Th" | 千百 | Th H |
| error | 36 | p35_s27 | Reviewer (terminology): 千百 should be abbreviated TTh Th, not "Th H". Suggested translation: "TTh Th" | 千百 | Th H |
| error | 36 | p35_s3 | Reviewer (terminology): 千百十个 should be abbreviated TTh Th H T O, not "Th H T O". Suggested translation: "TTh Th H T O" | 千百十个 | Th H T O |
| error | 36 | p35_s4 | Reviewer (terminology): 千百十个 should be abbreviated TTh Th H T O, not "Th H T O". Suggested translation: "TTh Th H T O" | 千百十个 | Th H T O |
| error | 36 | p35_s5 | Reviewer (terminology): 千百十个 should be abbreviated TTh Th H T O, not "Th H T O". Suggested translation: "TTh Th H T O" | 千百十个 | Th H T O |
| error | 42 | p41_s25 | Reviewer (terminology): 数位 glossary says 'ones/tens/...' but here 数位 means place values; 'place values' acceptable. However 计数器 is glossary 'counting frame' — used correctly. No change needed except consistency. | 你学过了哪些数位？在计数器上拨一拨，说说上表数据中的“2”分别表示多少。 | Which place values have you learned? Move the beads on the … |
| error | 46 | p45_s11 | Reviewer (terminology): "tell" is vague; 说一说 in this context is "discuss" or "explain". Suggested translation: "12. Estimate, measure and discuss." | 12.估一估，量一量，说一说。 | 12. Estimate, measure and tell. |
| error | 47 | p46_s0 | Reviewer (untranslated): The source heading is '五 加与减' with the unit number; '五力' here appears to be a mis-segmentation, but the translation 'Unit 5' is correct for the unit number. However the source text '五力' has been rendered as 'Unit 5' while the heading convention requires 'Unit 5', so this is acceptable. No finding if the segmentation is intended. Suggested translation: "Unit 5" | 五力 | Unit 5 |
| error | 48 | p47_s17 | Reviewer (terminology): Number/unit inconsistency: the source is '800米' and the running-record table uses the full unit elsewhere ('metres'/'米' in the exercise); writing 'm' abbreviates the unit inconsistently with the rest of the exercise (cf. p45 items and p47 labels). Suggested translation: "800 m" | 800米 | 800 m |
| error | 48 | p47_s18 | Reviewer (terminology): Unit abbreviated as 'm' while other items in the set write 'metres'; keep the unit style consistent within the exercise. Suggested translation: "820 m" | 820米 | 820 m |
| error | 48 | p47_s19 | Reviewer (terminology): Unit abbreviated as 'm' while other items in the set write 'metres'; keep the unit style consistent within the exercise. Suggested translation: "850 m" | 850米 | 850 m |
| error | 48 | p47_s20 | Reviewer (terminology): Unit abbreviated as 'm' while other items in the set write 'metres'; keep the unit style consistent within the exercise. Suggested translation: "950 m" | 950米 | 950 m |
| error | 48 | p47_s21 | Reviewer (terminology): Unit abbreviated as 'm' while other items in the set write 'metres'; keep the unit style consistent within the exercise. Suggested translation: "1150 m" | 1150米 | 1150 m |
| error | 51 | p50_s19 | Reviewer (terminology): 个 as a single column label should be "O" (ones) per the counting-frame convention; "O" is correct. No finding. | 个 | O |
| error | 51 | p50_s9 | Reviewer (meaning): Source "哪一位相加满十，就向前一位进1" means "Whenever a place sums to ten, carry 1 to the place to its left (the next higher place)"; translation "carry 1 to the next place" is ambiguous/wrong direction. Fix to "carry 1 to the next higher place". Suggested translation: "If a place sums to ten, carry 1 to the next higher place." | 哪一位相加满十，就向前一位进1 | If a place sums to ten, carry 1 to the next place. |
| error | 60 | p59_s14 | Reviewer (omission): The subject 我 (I) is omitted; the source says "I'll try 300 minus 44." Suggested translation: "I'll try 300 minus 44." | 我用300减去44试试 | Try 300 minus 44 |
| error | 63 | p62_s1 | Reviewer (terminology): 计数器 should be translated as "counting frame" per the glossary, not "counting frame" with a different meaning; "move the beads on the counting frame" is acceptable but the term should match. Suggested translation: "1. Draw, fill in, and move the beads on the counting frame." | 1.画一画，填一填，并在计数器上拨一拔。 | 1. Draw, fill in, and move the beads on the counting frame. |
| error | 63 | p62_s21 | Reviewer (terminology): 验算 is the standard term 'check by calculating/verify', 'check' alone is acceptable but the glossary-style term for 验算 in textbooks is 'check by calculating'. Suggested translation: "4. Calculate and check by calculating" | 4.计算并验算 | 4. Calculate and check |
| error | 66 | p65_s7 | Reviewer (number): The angle symbol and numeral: 记作：1 means 'Written as: ∠1' — the source's numeral 1 after the ∠ symbol was lost/or the angle label should be ∠1; translation '∠1' is correct, but the phrase 读作：角1 'Read as: angle 1' is fine. No change needed; checking placeholder integrity. | 记作：1。读作：角1。 | Written as: ∠1. Read as: angle 1. |
| error | 67 | p66_s2 | Reviewer (terminology): 三角板 is more precisely 'triangular set square'; 'set squares' is acceptable but singular/plural consistency matters. Suggested translation: "As shown, compare the sizes of the angles of the two set squares. What do you find?" | 如图，比较两个三角板的角的大小，你发现了什么？ | As shown, compare the sizes of the angles of the two set sq… |
| error | 77 | p76_s2 | Reviewer (omission): The translation "Name the parts." drops the directive of the original ("and point out...") and misstates the verb as "name" instead of "point out". Suggested translation: "and point out the parts of one of the angles." | 部分名称。 | Name the parts. |
| error | 79 | p78_s9 | Reviewer (number): Source has "1时=—分" with a dash placeholder; translation "1 hour = __ minutes" is fine, but the number blank is a single blank and the unit is minutes; the translation is acceptable. No finding. | 1时=—分 | 1 hour = __ minutes |
| error | 80 | p79_s17 | Reviewer (terminology): Glossary pair 读一读 => "Read"; "读一读，说一说" rendered "Read and say." follows it. Correct. | 2.读一读，说一说。 | 2. Read and say. |
| error | 82 | p81_s15 | Reviewer (omission): The source '1时是60' (1 hour is 60 ___) appears to be missing the unit/blank '分'; the translation leaves '60' dangling, which is acceptable only if 'minutes' is implied elsewhere. Suggested translation: "1 hour is 60 minutes" | 1时是60 | 1 hour is 60 |
| error | 83 | p82_s0 | Reviewer (omission): The source contains three items: '1时=__分', '—分秒' and '时—分'. The translation drops the latter two. All blanks must be preserved. Suggested translation: "3. Think and fill in 1 hour = ___ min, ___ min ___ s, ___ hour ___ min" | 3.想一想，填一填1时=_分—分秒时—分 | 3. Think and fill in 1 hour = __ min |
| error | 83 | p82_s6 | Reviewer (untranslated): The digit string '328.11.0' appears to be a placeholder/corrupted marker in the source; it is left in the translation. If it is a placeholder, keep it; otherwise it should not appear. | 328.11.0分，课间休息 | 328.11.0 minutes, break is |
| error | 85 | p84_s12 | Reviewer (number): The source has a dash '—' placeholder before 分, which the translation renders as '___' but also the dash form differs; the blank must be kept as in the source. Suggested translation: "(1) ___ minutes passed." | (1)经过了—分。 | (1) ___ min passed. |
| error | 87 | p86_s22 | Reviewer (omission): Sentence split across source segments; should be joined as one complete sentence. Suggested translation: "3. Use the record table in Appendix 3 to record the time you take each day on the way to school." | 3.利用附页3中的记录表记录你自己一周内每天上学路上 | 3. Use the record table in Appendix 3 to record the time yo… |
| error | 87 | p86_s23 | Reviewer (omission): '用的时间' is a continuation of the previous sentence and should not be treated as a separate label. Suggested translation: "the time used." | 用的时间。 | the time used. |
| error | 88 | p87_s4 | Reviewer (meaning): The source fragment '欢的方式表示' is the continuation of the previous sentence; the translation 'express them in a way you like.' does not match the source's meaning (it means 'express [them] in the way you like'). Suggested translation: "express them in the way you like." | 欢的方式表示。 | express them in a way you like. |
| error | 91 | p90_s15 | Reviewer (meaning): The source "⟦0⟧比口⟦1⟧少（" means "⟦0⟧ is fewer than 口⟦1⟧ (", i.e. the blank follows the comparison; the translation says "⟦0⟧ is less than 口⟦1⟧ (" which reverses the comparison direction (should be "has fewer than"). Suggested translation: "⟦0⟧ has fewer than 口⟦1⟧ (" | 360.24.l比口360.24.0少（ | 360.24.l is less than 口360.24.0 ( |
| error | 91 | p90_s7 | Reviewer (terminology): The glossary lists '妙想' => 'Miaoxiang', but the translation uses 'Miaoxiang' — this is correct. However, the source also contains '妙想' in p90_s2 and p90_s7; the same person's name is rendered 'Miaoxiang' consistently. No error. | 妙想调查了（）名同学。 | Miaoxiang surveyed () classmates. |
| error | 94 | p93_s11 | Reviewer (omission): The source includes 填一填 ("Fill in"), which is missing from the translation; only Draw and the counting-frame action are rendered. Suggested translation: "5. Draw, fill in, and move the beads on the counting frame." | 5.画一画，填一填，并在计数器上拨一拨。 | 5. Draw, fill in, and move the beads on the counting frame. |
| error | 95 | p94_s0 | Reviewer (terminology): 图形 is rendered 'Figures'; the mathematical term is 'Shapes', and the glossary prefers 'square/rectangle' style. 'Figures and Geometry' is acceptable but 'Shapes and Geometry' is more standard. Suggested translation: "Shapes and Geometry" | 图形与几何 | Figures and Geometry |
| error | 98 | p97_s42 | Reviewer (omission): The source's second item is "2分米=（）厘米" (2 dm = () cm); the translation omits the "= () cm" part. Suggested translation: "7 km = () m 2 dm = () cm 60 mm = () cm 5 cm = () mm" | 7千米=（）米2分米=（60毫米=（）厘米5厘米=（）毫米 | 7 km = () m 2 dm = () cm 60 mm = () cm 5 cm = () mm |
| error | 98 | p97_s43 | Reviewer (omission): The source's second item is "30厘米=（）分米" (30 cm = () dm); the translation omits the "= () dm" part. Suggested translation: "4000 m = () km 30 cm = () dm" | 4000米=（）千米30厘米=（）分米 | 4000 m = () km 30 cm = () dm |
| error | 99 | p98_s10 | Reviewer (meaning): "哪几根小棒" is plural: which several sticks can form a rectangle; the translation drops the plural/"several" sense. Suggested translation: "Which of the sticks can be put together to form a rectangle?" | 哪几根小棒可以搭成一个长方形？ | Which sticks can be put together to form a rectangle? |
| error | 99 | p98_s12 | Reviewer (omission): The list "4厘米2厘米3厘米2厘米5厘米4厘米" is a set of segment lengths; the translation has lost the separators/structure by running them together. Suggested translation: "4 cm, 2 cm, 3 cm, 2 cm, 5 cm, 4 cm" | 4厘米2厘米3厘米2厘米5厘米4厘米 | 4 cm 2 cm 3 cm 2 cm 5 cm 4 cm |
| error | 99 | p98_s13 | Reviewer (omission): Two separate instructions "画出一个长方形" and "画出一个正方形" are run together without punctuation/line break. Suggested translation: "Draw a rectangle. Draw a square." | 画出一个长方形画出一个正方形 | Draw a rectangle Draw a square |
| error | 99 | p98_s15 | Reviewer (meaning): "在下面的图中标出三个你认识的图形" = mark three shapes you recognize in the figure below; "three shapes you know" is acceptable, but the translation omits nothing major; still, "know" should be "recognize". Suggested translation: "7. Mark three shapes you recognize in the figure below." | 7.在下面的图中标出三个你认识的图形。 | 7. Mark three shapes you know in the figure below. |
| error | 103 | p102_s7 | Reviewer (untranslated): The garbled source label 'L品' was rendered as 'Lₚ', inventing a subscript that does not appear in the source. Suggested translation: "L品" | L品 | Lₚ |
| warning | 1 | p0_s10 | Reviewer (format): The English source line is already English and matches the translation; no issue. | BEIJING NORMAL UNIVERSITY PRESS | BEIJING NORMAL UNIVERSITY PRESS |
| warning | 1 | p0_s5 | Reviewer (format): Grade labels are conventionally written "Grade 2" rather than spelled out; wording preference only. Suggested translation: "Grade 2" | 二年级 | Grade Two |
| warning | 1 | p0_s6 | Reviewer (grammar): "Volume 2" is acceptable, but the standard rendering of 下册 for a textbook is "Volume 2" / "Second Semester"; no meaning change. Suggested translation: "Volume 2" | 下册 | Volume 2 |
| warning | 3 | p2_s24 | Reviewer (format): This label is the second half of the sentence from p2_s23; as an isolated fragment "together!" is fine but should be considered with the previous line. Suggested translation: "together!" | 发吧！ | together! |
| warning | 3 | p2_s6 | Reviewer (format): Heading should be in Title Case; "Number Magician" is fine. Suggested translation: "Number Magician" | 数宇魔法师 | Number Magician |
| warning | 4 | p3_s10 | Reviewer (format): The counting-frame column labels 百十 are rendered "H T", matching the convention of separate letters; fine. Suggested translation: "H T" | 百十 | H T |
| warning | 4 | p3_s11 | Reviewer (format): 个 alone as a place-value label is "O"; correct per convention. Suggested translation: "O" | 个 | O |
| warning | 4 | p3_s13 | Reviewer (format): This is the continuation of the unit heading 四 测量; as a separate item it duplicates the title. Acceptable if treated as two labels, but better combined. Suggested translation: "Measurement" | 测量 | Measurement |
| warning | 5 | p4_s0 | Reviewer (format): The source has no space between 五 and 加与减; the translation renders it as the unit heading, which is correct. Suggested translation: "Unit 5 Addition and Subtraction" | 五加与减 | Unit 5 Addition and Subtraction |
| warning | 5 | p4_s5 | Reviewer (format): Heading should be in Title Case; "Math Is Fun" is correct per glossary. Suggested translation: "Math Is Fun" | 数学好玩 | Math Is Fun |
| warning | 6 | p5_s12 | Reviewer (grammar): "...shown by division in vertical form" reads awkwardly; the standard phrasing is "shown using the vertical form of division". Suggested translation: "The process above can be shown using the vertical form of division. Look at it and talk about it." | 上面的过程可以用除法竖式表示。认一认，说一说。 | The process above can be shown by division in vertical form… |
| warning | 6 | p5_s18 | Reviewer (format): The source '位位' is two place-value column labels (hundreds and tens? Actually 位位 is not a standard pair); the translation 'T O' uses the abbreviations T (tens) and O (ones), but the source has two identical characters 位位, not 十位个位. The standard abbreviations for place-value column labels are TTh Th H T O; '位位' likely stands for 十位个位, which is 'T O'. This follows the convention, no problem. | 位位 | T O |
| warning | 6 | p5_s22 | Reviewer (grammar): 'talk about it' is unnatural; 'say what you find' or 'discuss' is better. Suggested translation: "Fill in and discuss." | 填一填，说一说。 | Fill in and talk about it. |
| warning | 6 | p5_s3 | Reviewer (format): The source is a bare count label 18个; per convention the counted object should be given when the context names it. "18 apples" is correct. Suggested translation: "18 apples" | 18个 | 18 apples |
| warning | 7 | p6_s1 | Reviewer (grammar): 'I brought 9 apples.' is fine. | 我带来9个苹果。 | I brought 9 apples. |
| warning | 7 | p6_s4 | Reviewer (grammar): '闹元宵' means 'celebrate the Lantern Festival'; 'Lantern Festival' loses the verb 'celebrate'. Suggested translation: "1. Celebrate the Lantern Festival." | 1.闹元宵。 | 1. Lantern Festival. |
| warning | 7 | p6_s7 | Reviewer (grammar): Missing final period; capitalization after the enumerator is fine. 'explain what each step in the vertical form of the division means' is wordy but acceptable. Suggested translation: "2. Circle, fill in, and explain what each step in the vertical form of the division means." | 2.圈一圈，填一填，说说除法竖式中每一步的意思 | 2. Circle, fill in, and explain what each step in the verti… |
| warning | 8 | p7_s0 | Reviewer (format): Heading '搭一搭（一）' should be 'Build (1)'; acceptable. | 搭一搭（一） | Build (1) |
| warning | 8 | p7_s12 | Reviewer (format): The source '小棒根数搭成的正方形' is a table header 'Number of sticks \| Squares made'; the translation adds a '\|' not in the source but acceptable as a table header. | 小棒根数搭成的正方形 | Number of sticks \| Squares made |
| warning | 8 | p7_s16 | Reviewer (grammar): '余数一会儿大一会儿小' means 'the remainder is sometimes large and sometimes small'; 'The remainder is sometimes big, sometimes small; why?' is acceptable. | 余数一会儿大一会儿小，怎么回事？ | The remainder is sometimes big, sometimes small; why? |
| warning | 8 | p7_s2 | Reviewer (grammar): Fine. | 13根小棒可以搭几个正方形，还剩几根？ | How many squares can you make with 13 sticks, and how many … |
| warning | 8 | p7_s5 | Reviewer (format): '答' should be 'Answer:'; correct. | 答 | Answer: |
| warning | 9 | p8_s17 | Reviewer (grammar): Fine. | 4根小棒搭一个正方形，用33根小棒可以搭几个正方形，还剩几根？ | 4 sticks make one square; with 33 sticks, how many squares … |
| warning | 10 | p9_s0 | Reviewer (format): 'Build (2)' is fine. | 搭一搭（二） | Build (2) |
| warning | 10 | p9_s1 | Reviewer (grammar): Fine. | 6根小棒搭一个房子··· | 6 sticks make a house··· |
| warning | 10 | p9_s2 | Reviewer (grammar): Fine. | 16根小棒可以搭几个房子，还剩几根？搭一搭，填一填。 | How many houses can you make with 16 sticks, and how many s… |
| warning | 17 | p16_s20 | Reviewer (grammar): "8 per box" is acceptable, but a full phrase is clearer for a label. Suggested translation: "8 per box" | 每盒8块 | 8 per box |
| warning | 17 | p16_s21 | Reviewer (format): A measure word after a number should be rendered with the counted object when known, otherwise dropped; "(pieces)" is not allowed. Suggested translation: "50 mooncakes" | 50块 | 50 (pieces) |
| warning | 17 | p16_s25 | Reviewer (format): "用竖式计算" is conventionally rendered "Calculate in vertical form." or "Use vertical form to calculate."; wording is acceptable but "Calculate in vertical form" omits 用. Minor. | 3.用竖式计算。 | 3. Calculate in vertical form. |
| warning | 18 | p17_s14 | Reviewer (format): "(brooms)" renders the measure word 把; it may be acceptable as the numbered noun, but if the context does not clearly name brooms it should be dropped. Context indicates brooms; keep. | 24把 | 24 (brooms) |
| warning | 18 | p17_s19 | Reviewer (format): "Seats 3 (cubs)" supplies the counted noun from context; if the exercise's context is sleds, not cubs, this is misleading. Context is snow sleds transporting cubs, so acceptable, but "(cubs)" should be checked against the picture. | 限乘3只 | Seats 3 (cubs) |
| warning | 18 | p17_s20 | Reviewer (grammar): "Counting from left to right" is fine; consider "counting from the left" for natural exercise wording. No meaning change. | 按下面的方式穿珠子，从左往右数，第18颗是什么颜色？ | Thread the beads as shown below. Counting from left to righ… |
| warning | 19 | p18_s27 | Reviewer (grammar): "Some put south at the top, some" is a sentence fragment in English because the source is cut mid-sentence; acceptable as a truncated caption. No change if source truly ends there. | 有的把南面写在上面，有的 | Some put south at the top, some |
| warning | 19 | p18_s28 | Reviewer (grammar): "Recognise and fill in." uses British spelling while the rest of the text uses American forms (color, etc.); keep spelling consistent. Suggested translation: "Recognize and fill in." | 认一认，填一填。 | Recognise and fill in. |
| warning | 22 | p21_s29 | Reviewer (format): Source '天津山东' has no comma between the two province names (it is a map label split by position); translation added a comma. Minor. Suggested translation: "Tianjin Shandong" | 天津山东 | Tianjin, Shandong |
| warning | 28 | p27_s10 | Reviewer (grammar): Number agreement error: '9 thousands' should be '9 thousand'. Suggested translation: "9 thousand, 0 hundreds, 4 tens, 0 ones" | 9个千，0个百，4个十，0个一 | 9 thousands, 0 hundreds, 4 tens, 0 ones |
| warning | 28 | p27_s21 | Reviewer (format): The single-character place-value row 万千百十个 is missing the ones-place O; the source has five labels (TTh Th H T O), but the translation shows only four. Suggested translation: "TTh Th H T O" | 万千百十个 | TTh Th H T O |
| warning | 28 | p27_s22 | Reviewer (format): The single-character place-value row 万千百十个 is missing the ones-place O; the source has five labels (TTh Th H T O), but the translation shows only four. Suggested translation: "TTh Th H T O" | 万千百十个 | TTh Th H T O |
| warning | 28 | p27_s23 | Reviewer (format): The single-character place-value row 万千百十个 is missing the ones-place O; the source has five labels (TTh Th H T O), but the translation shows only four. Suggested translation: "TTh Th H T O" | 万千百十个 | TTh Th H T O |
| warning | 28 | p27_s9 | Reviewer (grammar): Number agreement error: '2 thousands' should be '2 thousand', and '2 ones' should be '2 ones' (the latter is acceptable but inconsistent). Use singular 'thousand' with numerals. Suggested translation: "2 thousand, 9 hundreds, 3 tens, 2 ones" | 2个千，9个百，3个十，2个一 | 2 thousands, 9 hundreds, 3 tens, 2 ones |
| warning | 32 | p31_s11 | Reviewer (format): Exercise titles are not normally in Title Case mid-exercise; more importantly 收玉米 means "Harvesting corn" (sentence case). Suggested translation: "1. Harvesting corn" | 1.收玉米 | 1. Harvesting Corn |
| warning | 32 | p31_s8 | Reviewer (format): A currency label should not end with a period; the source period is likely punctuation of the sentence, but as a label it is odd. Keep consistent with the other amount labels. Suggested translation: "¥3200" | 3200元。 | ¥3200. |
| warning | 33 | p32_s10 | Reviewer (grammar): Missing final period. Suggested translation: "and the person thinking of the number may only answer "yes" or "no"." | 想数的人只能回答“对”或“不对” | and the person thinking of the number may only answer "yes"… |
| warning | 33 | p32_s5 | Reviewer (grammar): Missing final period. Suggested translation: "The winning number is greater than 3000, less than 4000, and close to 3500." | 获奖号码大于3000，小于4000，接近3500 | The winning number is greater than 3000, less than 4000, an… |
| warning | 33 | p32_s9 | Reviewer (format): Item is labelled a heading but is a list item continuing (1); casing/format inconsistent. Suggested translation: "(2) The guesser asks questions," | （2）猜数的人提问， | (2) The guesser asks questions, |
| warning | 34 | p33_s13 | Reviewer (format): The answer blank parenthesis is left open and unclosed; the source intends an answer blank. Suggested translation: "About (___)" | 大约有（ | About ( |
| warning | 34 | p33_s2 | Reviewer (format): The string of C's is a decorative placeholder in the source; keeping it verbatim is acceptable, but it is not a heading in English. | CCCCCCCCCCCCCCC | CCCCCCCCCCCCCCC |
| warning | 35 | p34_s14 | Reviewer (format): "50 beans" drops the explicit "颗" classifier noun; the counted noun should be consistent with 糖豆 (beans). Suggested translation: "There are 50 beans." | 有 50颗。 | There are 50 beans. |
| warning | 36 | p35_s35 | Reviewer (format): The colon suggests a label following; the source '写作：' likely means 'Writing:' as a section heading. Suggested translation: "Writing:" | 写作： | Write: |
| warning | 37 | p36_s0 | Reviewer (grammar): 'Think and talk.' is somewhat terse; 'Think and discuss.' is more natural for a textbook instruction. Suggested translation: "7. Think and discuss." | 7.想一想，说一说。 | 7. Think and talk. |
| warning | 38 | p37_s12 | Reviewer (grammar): 'Fill in and think.' is terse; 'Fill in and think about it.' is more natural. Suggested translation: "Find 1 mm, 1 cm, and 1 dm on the ruler. Fill in and think about it." | 在尺子上找出1毫米、1厘米、1分米。填一填，想一想。 | Find 1 mm, 1 cm and 1 dm on the ruler. Fill in and think. |
| warning | 38 | p37_s14 | Reviewer (grammar): 'Fill in and talk.' is terse; 'Fill in and say.' is more natural. Suggested translation: "Fill in and say." | 填一填，说一说。 | Fill in and talk. |
| warning | 38 | p37_s9 | Reviewer (format): As a heading '找一找，说子说' should be in Title Case: 'Find and Talk'. Suggested translation: "Find and Talk" | 找一找，说子说 | Find and Talk |
| warning | 39 | p38_s10 | Reviewer (format): Unit label; should be 'dm'. Suggested translation: "dm" | 分米 | dm |
| warning | 39 | p38_s15 | Reviewer (format): Unit label; should be 'cm'. Suggested translation: "cm" | 厘米 | cm |
| warning | 39 | p38_s18 | Reviewer (style): 'Read and do.' is terse; 'Read and do it.' is more natural. Suggested translation: "5. Read and do it." | 5.读一读，做一做。 | 5. Read and do. |
| warning | 39 | p38_s19 | Reviewer (grammar): The sentence joins two independent actions with a comma ('...apart, then walk...'); this comma splice is not natural textbook prose. Suggested translation: "The narrowest hutong in Beijing is Qianshi Hutong. It is 55 m long in total and 7 dm wide on average. With a partner, pull two desks apart so that they are 7 dm apart, and then walk between them together." | 北京最窄的胡同是钱市胡同。全长55米，平均宽7分米。和同伴一起把两张课桌拉开，使它们中间相隔7分米，然后，两个人同时在… | The narrowest hutong in Beijing is Qianshi Hutong. It is 55… |
| warning | 39 | p38_s5 | Reviewer (style): 'Big Dipper' is the usual term; '北斗星' can be 'Big Dipper' or 'Northern Dipper'. Suggested translation: "2. This is a diagram of the Big Dipper." | 2.这是北斗星的示意图。 | 2. This is a diagram of the Big Dipper. |
| warning | 39 | p38_s6 | Reviewer (format): Missing spaces around parentheses and units. Suggested translation: "Measure on the diagram: from star 1 to star 2 is ( ) mm, from star 6 to star 7 is ( ) cm" | 在图上量一量，第1颗星到第2颗星是（）毫米，第6颗星到第7颗星是（）厘米 | Measure on the diagram: from star 1 to star 2 is () mm, fro… |
| warning | 39 | p38_s7 | Reviewer (format): Incomplete fragment; likely ' ) mm' is part of a larger item. Suggested translation: ") mm" | ）毫米 | ) mm |
| warning | 39 | p38_s8 | Reviewer (grammar): 'Fill in' is terse; 'Fill in the blanks.' is more natural. Suggested translation: "3. Fill in the blanks." | 3.填一填 | 3. Fill in |
| warning | 39 | p38_s9 | Reviewer (format): Missing space after '='; should be '7 m = '. Suggested translation: "7 m =" | 7米= | 7 m = |
| warning | 46 | p45_s10 | Reviewer (format): Standalone unit label should be abbreviated cm. Suggested translation: "cm" | 厘米 | centimetres |
| warning | 46 | p45_s31 | Reviewer (grammar): Number agreement: '1 kilometres' should be singular '1 kilometre'. Suggested translation: "1 kilometre" | 1千米 | 1 kilometres |
| warning | 46 | p45_s6 | Reviewer (format): 3000米 should use the standard unit abbreviation m. Suggested translation: "3000 m =" | 3000米= | 3000 metres= |
| warning | 46 | p45_s8 | Reviewer (format): Standalone unit label should be abbreviated m. Suggested translation: "m" | 米 | metres |
| warning | 47 | p46_s26 | Reviewer (grammar): Number agreement: '1 electric fans' and '1 refrigerators' should be singular. Suggested translation: "How much cheaper is 1 electric fan than 1 refrigerator?" | 买1台电扇比1台冰箱便宜多少元？ | How much cheaper are 1 electric fans than 1 refrigerators? |
| warning | 49 | p48_s11 | Reviewer (format): Source has (1)班和(2)班; translation "Class 1 and Class 2" drops the parentheses numbering, but that is a formatting choice; acceptable. | （1）班和(2）班一共····· | Class 1 and Class 2 together····· |
| warning | 58 | p57_s16 | Reviewer (grammar): Wording "move the beads on the counting frame" is a reasonable rendering but "move" is less standard than "slide the beads"; acceptable, minor style issue for an instructional verb. | 1.画一画，填一填，并在计数器上拨一拨。 | 1. Draw, fill in, and move the beads on the counting frame. |
| warning | 59 | p58_s25 | Reviewer (format): Source is two labels in one line ("一年级二年级") rendered as two lines; splitting is acceptable for labels but check line-break intent. | 一年级二年级 | Grade 1 Grade 2 |
| warning | 59 | p58_s26 | Reviewer (format): Source has bare "278人"; adding "students" is a reasonable inference but the measure word is a label. Acceptable. | 278人 | 278 students |
| warning | 59 | p58_s27 | Reviewer (format): Source has bare "203人"; "students" added. Acceptable. | 203人 | 203 students |
| warning | 61 | p60_s27 | Reviewer (format): Money amounts must be written in Chinese yuan with the currency symbol before the number, as in the rest of the text (¥300, ¥28). Suggested translation: "(2) Teacher Li paid ¥300 and got ¥28 change. Is that right?" | （2）李老师付了300元，找回28元，对吗？ | (2) Teacher Li paid 300 yuan and got 28 yuan change. Is tha… |
| warning | 63 | p62_s25 | Reviewer (grammar): 'from smallest to largest result' is awkward word order; the natural phrasing places the noun after the adjective. Suggested translation: "5. Arrange these number sentences in one row from smallest to largest result." | 5.把这些算式按得数的大小，从小到大排成一行 | 5. Arrange these number sentences in one row from smallest … |
| warning | 64 | p63_s17 | Reviewer (format): The header 星期一二三四五 combines the column header 'Day' with the weekdays; 'Day Mon Tue Wed Thu Fri' should read 'Weekday' followed by the day abbreviations. Suggested translation: "Weekday Mon Tue Wed Thu Fri" | 星期一二三四五 | Day Mon Tue Wed Thu Fri |
| warning | 64 | p63_s20 | Reviewer (grammar): 'Tickets sold / tickets' is a redundant rendering of 票数/张; the unit label should be 'Number of tickets / tickets'. Suggested translation: "Number of tickets / tickets" | 票数/张 | Tickets sold / tickets |
| warning | 66 | p65_s0 | Reviewer (format): Unit heading: 'Unit 6 Recognizing Shapes' is fine, but the convention places the unit numeral followed by the topic; 'Unit 6 Recognizing Shapes' is acceptable. No change needed. | 六认识图形 | Unit 6 Recognizing Shapes |
| warning | 66 | p65_s10 | Reviewer (grammar): 'mark them' for 标一标 is acceptable but the exercise label convention is 'Mark them'. Minor. Suggested translation: "Find three angles in each figure below and mark them." | 在下面的图中各找出三个角，标一标。 | Find three angles in each figure below and mark them. |
| warning | 68 | p67_s14 | Reviewer (grammar): "4 angles" is unnatural for the corners of a square piece of paper; English uses "4 corners". Suggested translation: "Do it and fill in. A square piece of paper has 4 corners. If you cut off one corner with scissors, how many corners are left?" | 做一做，填一填。一张正方形纸有4个角，如果用剪刀剪去一个角，还剩几个角？ | Do it and fill in. A square piece of paper has 4 angles. If… |
| warning | 68 | p67_s15 | Reviewer (format): The three answer blanks run together; a space between each "() angles left" would match the source layout. Suggested translation: "() angles left () angles left () angles left" | 还剩（）个角还剩（）个角还剩（）个角 | () angles left () angles left () angles left |
| warning | 70 | p69_s11 | Reviewer (grammar): "Fold a circle in half twice" is unclear; the object is a circular piece of paper. Suggested translation: "5. Fold a circle in half twice, then open it. Talk about where the right angles are." | 5.把一个圆片对折两次后打开，说一说哪有直角。 | 5. Fold a circle in half twice, then open it. Discuss where… |
| warning | 70 | p69_s18 | Reviewer (grammar): "make a right angle and an obtuse angle" is acceptable, but "form" better matches 摆出. Suggested translation: "(2) Use two pieces of the tangram in Figure 2 on attached page 3 to form a right angle and an obtuse angle." | （2）利用附页3图2七巧板中的两块板，分别摆出一个直角和一个钝角。 | (2) Use two pieces of the tangram in Figure 2 on attached p… |
| warning | 71 | p70_s14 | Reviewer (format): Ellipsis should be three dots, not "···". Suggested translation: "Each angle of a square ..." | 正方形的每个角··· | Each angle of a square ··· |
| warning | 71 | p70_s15 | Reviewer (format): Ellipsis should be three dots, not "···". Suggested translation: "Each side of a square ..." | 正方形的每条边··· | Each side of a square ··· |
| warning | 71 | p70_s8 | Reviewer (grammar): "The opposite sides of a rectangle are equal." is acceptable but "opposite sides" is the standard term in textbook phrasing. Suggested translation: "The opposite sides of a rectangle are equal." | 长方形对着的边相等。 | The opposite sides of a rectangle are equal. |
| warning | 71 | p70_s9 | Reviewer (format): The ellipsis dots are rendered as "····"; the source uses an ellipsis marking an unfinished sentence. Suggested translation: "Each angle of a rectangle is ..." | 长方形的每个角都是···· | Each angle of a rectangle is ···· |
| warning | 72 | p71_s3 | Reviewer (grammar): "Try with the tangram" is awkward; the Chinese means to try using the tangram pieces. Suggested translation: "(1) Which pieces of the tangram can make a rectangle or a square? Try it with the tangram in Figure 2 on attached page 3." | （1）七巧板中哪些板可以拼出长方形或正方形？用附页3图2中的七巧板试一试。 | (1) Which pieces of the tangram can make a rectangle or a s… |
| warning | 76 | p75_s5 | Reviewer (grammar): The fragment duplicates the continuation belonging to the previous line; the sentence should read naturally when the fragments are joined. As split text, capitalization is inconsistent with the previous fragment. Suggested translation: "Use 4 rectangles to make a" | 用4个长方形拼出一 | use 4 rectangles to make a |
| warning | 79 | p78_s1 | Reviewer (format): The label "Olympic Opening" would read more naturally as "The Olympic Opening Ceremony", though the short form is acceptable as a caption. Suggested translation: "The Olympic Opening Ceremony" | 奥运开幕 | Olympic Opening |
| warning | 82 | p81_s26 | Reviewer (grammar): Number agreement: '1 minutes' should be '1 minute'. Suggested translation: "1 minute" | 1分 | 1 minutes |
| warning | 82 | p81_s27 | Reviewer (format): Seconds are abbreviated as 's' here but written 'seconds' in p81_s29 and elsewhere; inconsistent abbreviation style. Suggested translation: "20 seconds" | 20秒 | 20 s |
| warning | 82 | p81_s29 | Reviewer (format): Inconsistent with p81_s27 and p81_s28 which use 's'; choose one style for seconds. Suggested translation: "3 s" | 3秒 | 3 seconds |
| warning | 82 | p81_s4 | Reviewer (format): Source contains numeric placeholders; translation keeps them. Fine. | 324.4.0分324.4.1秒 | 324.4.0 min 324.4.1 s |
| warning | 82 | p81_s9 | Reviewer (grammar): Missing article before the singular countable noun phrase '1 hour 30 minutes'; textbook English normally writes '1 hour and 30 minutes' (or '1 hour 30 minutes'), but a determiner/article is needed: '1 hour and 30 minutes'. Suggested translation: "A football match took 1 hour and 30 minutes. How many minutes is 1 hour and 30 minutes?" | 踢一场足球比赛用了1时30分。1时30分是多少分？ | A football match took 1 hour 30 minutes. How many minutes i… |
| warning | 84 | p83_s0 | Reviewer (format): Heading casing: 'Daily Schedule' uses Title Case, which is fine; but 'Taoqi's Daily Schedule' — ensure title style consistent. No real issue. | 淘气的作息时间 | Taoqi's Daily Schedule |
| warning | 84 | p83_s19 | Reviewer (grammar): '20 min' should be '20 minutes' in running text. Suggested translation: "It took 20 minutes in total." | 一共花了20分。 | It took 20 min in total. |
| warning | 84 | p83_s3 | Reviewer (format): The trailing ellipsis '····' is preserved but its dots are spaced in the source; translation uses '····'. Use standard ellipsis. Suggested translation: "Taoqi gets up at 6:30 and has breakfast at 6:55…" | 淘气早上6时30分起床6时55分吃早餐···· | Taoqi gets up at 6:30 and has breakfast at 6:55···· |
| warning | 84 | p83_s5 | Reviewer (grammar): Awkward wording; 'How long does it take Taoqi to go from getting up to starting breakfast?' is more natural. Suggested translation: "How long does it take Taoqi to go from getting up to starting eating breakfast? Look and talk about it." | 淘气从起床到开始吃早餐，用了多长时间？看一看，说一说。 | How long does it take Taoqi from getting up to starting bre… |
| warning | 84 | p83_s6 | Reviewer (grammar): Unit 'min' should be written as 'minutes' in running text. Suggested translation: "It took 25 minutes in total." | 一共花了25分。 | It took 25 min in total. |
| warning | 85 | p84_s32 | Reviewer (grammar): Unit 'min' should be written as 'minutes' in running text. Suggested translation: "Played for _ minutes." | 玩了_分。 | Played for _ min. |
| warning | 86 | p85_s2 | Reviewer (grammar): Punctuation: comma splice; use a period or semicolon. Suggested translation: "I'm going to school. Bye!" | 我去上学了，再见 | I'm going to school. Bye! |
| warning | 87 | p86_s6 | Reviewer (format): Two separate column labels merged without separation; should be split. Suggested translation: "Arrival time Time on the way" | 到校时间路上用的时间 | Arrival time Time on the way |
| warning | 90 | p89_s9 | Reviewer (format): The source label '兔猴鱼' is vertical text with no spaces; the translation separates the words with spaces. Preserving the original layout would be preferable for a matching exercise. Suggested translation: "Rabbit Monkey Fish" | 兔猴鱼 | Rabbit Monkey Fish |
| warning | 91 | p90_s14 | Reviewer (format): The trailing comma after the answer blank is kept, but the blank's closing parenthesis is missing in the source only; translation is acceptable. No real problem. | ）个， | ), |
| warning | 91 | p90_s18 | Reviewer (format): Heading/label should be in Title Case per textbook conventions. Suggested translation: "Healthy Eating Day" | 健康饮食日 | Healthy Eating Day |
| warning | 92 | p91_s0 | Reviewer (grammar): British spelling 'Favourite' while other items use 'favorite'; spelling consistency issue. Suggested translation: "Favorite Fruits" | 最喜欢的水果 | Favourite Fruits |
| warning | 93 | p92_s15 | Reviewer (format): Answer blanks in the source are full-width parentheses （）; the translation uses empty half-width parentheses (), which is not the standard blank form and may be confused with punctuation. Suggested translation: "(2) There are （） basketballs, （） footballs and （） volleyballs." | (2)篮球有（）个，足球有（）个，排球有（）个。 | (2) There are () basketballs, () footballs and () volleybal… |
| warning | 94 | p93_s4 | Reviewer (format): The source enumerator "2." starts the item and should remain at the start of the translation; it is present, but "2." should keep the space as in the source. No change needed beyond consistency: the item is fine, but kept for review of the enumerator spacing. | 2.用自己喜欢的方式把下面三个数表示出来。 | 2. Show the three numbers below in your own way. |
| warning | 95 | p94_s22 | Reviewer (format): An unmatched opening quotation mark is carried over, but the 正 tally character should be kept exactly as 正; the stray quote is a formatting artifact. Keep the tally symbol only. Suggested translation: "正" | “正 | "正 |
| warning | 96 | p95_s6 | Reviewer (grammar): 'Write the numbers on the lines' is awkward for 横线上的数 (the numbers written above the line); also 'move them on the abacus' should be 'move the beads on the abacus'. Suggested translation: "4. Write the numbers on the lines and move the beads on the abacus." | 4.写出横线上的数，并在算盘上拨一拨。 | 4. Write the numbers on the lines, and move them on the aba… |
| warning | 97 | p96_s24 | Reviewer (grammar): The sentence is split across two items (s24 "...并尝" and s25 "试解答。"). The translation splits it as "...and try" / "to answer it." This preserves the split, but "Pose a mathematical question and try" is an incomplete sentence in English; since the continuation is in the next item, this is only a style issue. No change required if items are concatenated. | （2）请你提出一个数学问题，并尝 | (2) Pose a mathematical question and try |
| warning | 97 | p96_s25 | Reviewer (grammar): "to answer it." alone is a fragment; when concatenated with s24 it reads correctly. No change required if items are adjacent. | 试解答。 | to answer it. |
| warning | 97 | p96_s7 | Reviewer (grammar): The source parentheses list possible answers (30字、300字、3000字); the translation preserves them, which is good, but the phrasing 'about how many characters there are' is fine. No real issue. | 8.估一估，大约有多少个字？（30字、300字、3000字） | 8. Estimate about how many characters there are. (30 charac… |
| warning | 98 | p97_s0 | Reviewer (format): The source "选一选，画" is a truncated instruction (the object of 画 is cut off in the scan); the translation "Choose and draw" is acceptable but could be "Choose and draw" left as is. No change needed. | 11.选一选，画 | 11. Choose and draw |
| warning | 98 | p97_s1 | Reviewer (grammar): "Doing eye exercises takes about" is a sentence fragment; since the source item is also a fragment ending before the answer blank, this is consistent, but a comma or blank would read better in the final layout. | 做眼保健操大约需要 | Doing eye exercises takes about |
| warning | 98 | p97_s2 | Reviewer (grammar): "Getting dressed takes about" is a sentence fragment matching the source fragment; acceptable but ensure the blank follows. | 穿衣服大约需要 | Getting dressed takes about |
| warning | 98 | p97_s26 | Reviewer (format): Proper place name 通天桥 left in pinyin ("Tongtian Bridge"); standard textbook rendering would translate it. Suggested translation: "Bridge to Heaven" | 通天桥 | Tongtian Bridge |
| warning | 98 | p97_s3 | Reviewer (grammar): "Tying shoelaces takes about" is a sentence fragment matching the source fragment; acceptable but ensure the blank follows. | 系鞋带大约需要 | Tying shoelaces takes about |
| warning | 99 | p98_s0 | Reviewer (format): "3.量一量。" the glossary word 量一量 is "Measure"; the trailing period is dropped, which is a minor formatting inconsistency. Suggested translation: "3. Measure." | 3.量一量。 | 3. Measure. |
| warning | 100 | p99_s13 | Reviewer (grammar): 'The animals liked by 5 children are as follows' is awkward word order for a textbook exercise. Suggested translation: "3. Five children like the following animals." | 3. 5个小朋友喜欢的动物如下。 | 3. The animals liked by 5 children are as follows. |

### `numbers` — 2 errors, 0 warnings

| Severity | Page | Segment | Message | Source | Translation |
|---|---|---|---|---|---|
| error | 44 | p43_s21 | Number "3" from the source is missing in the translation; keep every number exactly as written in the source | ③试验田在居住区的西北方。 | ⑤ The experimental field is to the northwest of the residen… |
| error | 82 | p81_s6 | Number "5" from the source is missing in the translation; keep every number exactly as written in the source | 5秒 | 15 s |

### `untranslated` — 12 errors, 0 warnings

| Severity | Page | Segment | Message | Source | Translation |
|---|---|---|---|---|---|
| error | 17 | p16_s10 | 1 letter(s) of the source script remain untranslated ("福"); translate all text into English | 福 | 福 |
| error | 17 | p16_s11 | 1 letter(s) of the source script remain untranslated ("福"); translate all text into English | 福 | 福 |
| error | 17 | p16_s12 | 1 letter(s) of the source script remain untranslated ("福"); translate all text into English | 福 | 福 |
| error | 17 | p16_s13 | 1 letter(s) of the source script remain untranslated ("福"); translate all text into English | 福 | 福 |
| error | 17 | p16_s14 | 1 letter(s) of the source script remain untranslated ("福"); translate all text into English | 福 | 福 |
| error | 17 | p16_s15 | 2 letter(s) of the source script remain untranslated ("福福"); translate all text into English | 福福 | 福福 |
| error | 17 | p16_s16 | 1 letter(s) of the source script remain untranslated ("福"); translate all text into English | 福 | 福 |
| error | 17 | p16_s7 | 1 letter(s) of the source script remain untranslated ("福"); translate all text into English | 福 | 福 |
| error | 17 | p16_s8 | 2 letter(s) of the source script remain untranslated ("福福"); translate all text into English | 福福 | 福福 |
| error | 91 | p90_s15 | 1 letter(s) of the source script remain untranslated ("口"); translate all text into English | 360.24.l比口360.24.0少（ | 360.24.l is less than 口360.24.0 ( |
| error | 92 | p91_s13 | 1 letter(s) of the source script remain untranslated ("下"); translate all text into English | 下TF正 | 下 TF 正 |
| error | 93 | p92_s6 | 3 letter(s) of the source script remain untranslated ("卌"); translate all text into English | 丰丰丰三 | 卌 卌 卌 \|\|\|\| |

### `image_text` — 0 errors, 4 warnings

| Severity | Page | Segment | Message | Source | Translation |
|---|---|---|---|---|---|
| warning | 35 | p34_i136_6 | The text '对比，科学界才初步确定这是一群类似于蜥蜴的早已灭绝的爬行动物。' was left in the source language (inline pictograms the OCR cannot read (left in the picture)): the line is built around symbols or pictures the OCR could not read - check the page in the preview | 对比，科学界才初步确定这是一群类似于蜥蜴的早已灭绝的爬行动物。 |  |
| warning | 35 | p34_i136_6 | The text '对比，科学界才初步确定这是一群类似于蜥蜴的早已灭绝的爬行动物。' was left in the source language (inline pictograms the OCR cannot read (left in the picture)): the line is built around symbols or pictures the OCR could not read - check the page in the preview | 对比，科学界才初步确定这是一群类似于蜥蜴的早已灭绝的爬行动物。 |  |
| warning | 69 | p68_i272_5 | The text '板比比' was left in the source language (inline pictograms the OCR cannot read (left in the picture)): the line is built around symbols or pictures the OCR could not read - check the page in the preview | 板比比 |  |
| warning | 69 | p68_i272_5 | The text '板比比' was left in the source language (inline pictograms the OCR cannot read (left in the picture)): the line is built around symbols or pictures the OCR could not read - check the page in the preview | 板比比 |  |

### `length_ratio` — 0 errors, 1 warning

| Severity | Page | Segment | Message | Source | Translation |
|---|---|---|---|---|---|
| warning | 80 | p79_s12 | The translation looks too short: 9 characters for 19 translatable source characters (ratio 0.47, about 2.60 expected); check that nothing was omitted | 4时12分9时20分6时08分1时30分8时55分 | 4:12 9:20 6:08 1:30 8:55 |
