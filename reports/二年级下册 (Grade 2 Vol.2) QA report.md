# QA report

**Result:** QA FAILED after 3 rounds: 212 errors, 140 warnings (1979.3 s); proofread: 518 corrections applied; output file checks: 0 error(s)

**Document:** 数 (zh → en, 109 page(s), 1780 translatable segment(s))

**Checks run:** `completeness`, `placeholders`, `numbers`, `untranslated`, `target_script`, `glossary`, `length_ratio`, `formatting`, `layout_fit`, `image_text`, `llm_review`, `output_checks`

## Rounds

| Round | Errors | Warnings | Re-translated | Passed | Duration |
|---|---|---|---|---|---|
| 1 | 324 | 257 | 294 segment(s) | no | 478.9 s |
| 2 | 282 | 297 | 254 segment(s) | no | 442.7 s |
| 3 | 308 | 344 | 0 segment(s) | no | 185.5 s |

- Round 1: llm_review ×411, layout_fit ×117, formatting ×31, glossary ×6, image_text ×5, completeness ×4, numbers ×2, placeholders ×2, target_script ×2, untranslated ×1
- Round 2: llm_review ×457, layout_fit ×93, formatting ×10, untranslated ×6, image_text ×5, completeness ×3, glossary ×2, placeholders ×2, target_script ×1
- Round 3: llm_review ×523, layout_fit ×83, formatting ×19, untranslated ×7, image_text ×5, placeholders ×4, completeness ×3, numbers ×3, target_script ×3, length_ratio ×2

## Final issues (352)

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
| error | 49 | p48_s11 | Start the translation with the list marker "（1）" exactly as in the source | （1）班和(2）班一共····· | Class 1 and Class 2 together… |
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
| error | 79 | p78_s11 | The source ends with a question mark; end the translation with a question mark too | 与同伴说一说，你是怎么认的？ | Tell your partner how you read the time. |
| error | 79 | p78_s4 | The source ends with a question mark; end the translation with a question mark too | 说一说，关于钟面你知道些什么？ | Say what you know about the clock face. |
| error | 81 | p80_s0 | The source does not end with a question mark; do not end the translation with one | 分有多长 | minute: how long? |
| error | 88 | p87_s7 | Remove the symbol(s) √: they are not in the source (a picture in the book is not a symbol; leave it out rather than inventing one) | 花盆的摆放也是有规律的：√√××Vxx··· | The arrangement of the flower pots also follows a pattern: … |
| error | 90 | p89_s14 | Keep the line breaks of the source: it has 0 line break(s), the translation has 2 | 喜欢356.26.0的有（）人，喜欢喜欢356.28.0的有（）人，喜欢的有（）人，可以选（）作为吉祥物。 | () people like 356.26.0, () people like 356.28.0, () pe… |
| error | 90 | p89_s9 | Keep the line breaks of the source: it has 0 line break(s), the translation has 2 | 兔猴鱼 | Rabbit Monkey Fish |
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

### `layout_fit` — 64 errors, 40 warnings

| Severity | Page | Segment | Message | Source | Translation |
|---|---|---|---|---|---|
| error | 3 | p2_s10 | Shorten the translation to at most 23 characters so it fits the original box (the current translation of 27 characters overflows its box; the minimum allowed size is 55%) | 2任何数乘0都为0。 | 2. Any number times 0 is 0. |
| error | 3 | p2_s10 | Shorten the translation to at most 23 characters so it fits the original box (the current translation of 27 characters overflows its box; the minimum allowed size is 55%) | 2任何数乘0都为0。 | 2. Any number times 0 is 0. |
| error | 3 | p2_s7 | Shorten the translation to at most 20 characters so it fits the original box (the current translation of 41 characters overflows its box; the minimum allowed size is 55%) | 1.任何数加减0都没有变化。 | 1. Add or subtract 0 and nothing changes. |
| error | 3 | p2_s7 | Shorten the translation to at most 20 characters so it fits the original box (the current translation of 41 characters overflows its box; the minimum allowed size is 55%) | 1.任何数加减0都没有变化。 | 1. Add or subtract 0 and nothing changes. |
| error | 4 | p3_s5 | Shorten the translation to at most 20 characters so it fits the original box (the current translation of 24 characters overflows its box; the minimum allowed size is 55%) | 12.8.0打谷场 | 12.8.0 Threshing floor |
| error | 4 | p3_s5 | Shorten the translation to at most 20 characters so it fits the original box (the current translation of 24 characters overflows its box; the minimum allowed size is 55%) | 12.8.0打谷场 | 12.8.0 Threshing floor |
| error | 4 | p3_s6 | Shorten the translation to at most 25 characters so it fits the original box (the current translation of 29 characters overflows its box; the minimum allowed size is 55%) | 二 方向与位置 | Unit 2 Direction and Position |
| error | 4 | p3_s6 | Shorten the translation to at most 25 characters so it fits the original box (the current translation of 29 characters overflows its box; the minimum allowed size is 55%) | 二 方向与位置 | Unit 2 Direction and Position |
| error | 6 | p5_s1 | Shorten the translation to at most 12 characters so it fits the original box (the current translation of 14 characters overflows its box; the minimum allowed size is 55%) | 分苹果 | Sharing apples |
| error | 6 | p5_s1 | Shorten the translation to at most 12 characters so it fits the original box (the current translation of 14 characters overflows its box; the minimum allowed size is 55%) | 分苹果 | Sharing apples |
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
| error | 18 | p17_s13 | Shorten the translation to at most 16 characters so it fits the original box (the current translation of 19 characters overflows its box; the minimum allowed size is 55%) | 个，还剩 | dustpans, remainder |
| error | 18 | p17_s13 | Shorten the translation to at most 16 characters so it fits the original box (the current translation of 19 characters overflows its box; the minimum allowed size is 55%) | 个，还剩 | dustpans, remainder |
| error | 19 | p18_s31 | Shorten the translation to at most 7 characters so it fits the original box (the current translation of 10 characters overflows its box; the minimum allowed size is 55%) | 操场 | Playground |
| error | 19 | p18_s31 | Shorten the translation to at most 7 characters so it fits the original box (the current translation of 10 characters overflows its box; the minimum allowed size is 55%) | 操场 | Playground |
| error | 21 | p20_s0 | Shorten the translation to at most 19 characters so it fits the original box (the current translation of 22 characters overflows its box; the minimum allowed size is 55%) | 辨认方向 | Identifying Directions |
| error | 21 | p20_s0 | Shorten the translation to at most 19 characters so it fits the original box (the current translation of 22 characters overflows its box; the minimum allowed size is 55%) | 辨认方向 | Identifying Directions |
| error | 22 | p21_s29 | Shorten the translation to at most 10 characters so it fits the original box (the current translation of 16 characters overflows its box; the minimum allowed size is 55%) | 天津山东 | Tianjin Shandong |
| error | 22 | p21_s29 | Shorten the translation to at most 10 characters so it fits the original box (the current translation of 16 characters overflows its box; the minimum allowed size is 55%) | 天津山东 | Tianjin Shandong |
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
| error | 90 | p89_s9 | Shorten the translation to at most 6 characters so it fits the original box (the current translation of 18 characters overflows its box; the minimum allowed size is 55%) | 兔猴鱼 | Rabbit Monkey Fish |
| error | 90 | p89_s9 | Shorten the translation to at most 6 characters so it fits the original box (the current translation of 18 characters overflows its box; the minimum allowed size is 55%) | 兔猴鱼 | Rabbit Monkey Fish |
| error | 91 | p90_s21 | Shorten the translation to at most 12 characters so it fits the original box (the current translation of 15 characters overflows its box; the minimum allowed size is 55%) | 只爱吃菜 | Vegetables only |
| error | 91 | p90_s21 | Shorten the translation to at most 12 characters so it fits the original box (the current translation of 15 characters overflows its box; the minimum allowed size is 55%) | 只爱吃菜 | Vegetables only |
| error | 91 | p90_s24 | Shorten the translation to at most 6 characters so it fits the original box (the current translation of 8 characters overflows its box; the minimum allowed size is 55%) | 3人 | 3 people |
| error | 91 | p90_s24 | Shorten the translation to at most 6 characters so it fits the original box (the current translation of 8 characters overflows its box; the minimum allowed size is 55%) | 3人 | 3 people |
| error | 100 | p99_s9 | Shorten the translation to at most 15 characters so it fits the original box (the current translation of 20 characters overflows its box; the minimum allowed size is 55%) | 汽车慢速中速快速 | Car Slow Medium Fast |
| error | 100 | p99_s9 | Shorten the translation to at most 15 characters so it fits the original box (the current translation of 20 characters overflows its box; the minimum allowed size is 55%) | 汽车慢速中速快速 | Car Slow Medium Fast |
| warning | 4 | p3_s0 | The translation overflows its box and was rendered at 27% of the original size; even a much shorter text would not fit, check this box in the preview | 录 | Contents |
| warning | 4 | p3_s0 | The translation overflows its box and was rendered at 27% of the original size; even a much shorter text would not fit, check this box in the preview | 录 | Contents |
| warning | 4 | p3_s1 | The translation overflows its box and was rendered at 44% of the original size; even a much shorter text would not fit, check this box in the preview | 目 | Table of |
| warning | 4 | p3_s1 | The translation overflows its box and was rendered at 44% of the original size; even a much shorter text would not fit, check this box in the preview | 目 | Table of |
| warning | 6 | p5_s15 | The translation overflows its box and was rendered at 23% of the original size; even a much shorter text would not fit, check this box in the preview | 十位 | tens |
| warning | 6 | p5_s15 | The translation overflows its box and was rendered at 23% of the original size; even a much shorter text would not fit, check this box in the preview | 十位 | tens |
| warning | 7 | p6_s6 | The translation overflows its box and was rendered at 43% of the original size; even a much shorter text would not fit, check this box in the preview | 烟花 | fireworks |
| warning | 7 | p6_s6 | The translation overflows its box and was rendered at 43% of the original size; even a much shorter text would not fit, check this box in the preview | 烟花 | fireworks |
| warning | 8 | p7_s9 | The translation overflows its box and was rendered at 41% of the original size; even a much shorter text would not fit, check this box in the preview | 余数 | remainder |
| warning | 8 | p7_s9 | The translation overflows its box and was rendered at 41% of the original size; even a much shorter text would not fit, check this box in the preview | 余数 | remainder |
| warning | 15 | p14_s10 | The translation overflows its box and was rendered at 43% of the original size; even a much shorter text would not fit, check this box in the preview | 答 | Answer: |
| warning | 15 | p14_s10 | The translation overflows its box and was rendered at 43% of the original size; even a much shorter text would not fit, check this box in the preview | 答 | Answer: |
| warning | 17 | p16_s10 | The translation overflows its box and was rendered at 24% of the original size; even a much shorter text would not fit, check this box in the preview | 福 | blessing |
| warning | 17 | p16_s10 | The translation overflows its box and was rendered at 24% of the original size; even a much shorter text would not fit, check this box in the preview | 福 | blessing |
| warning | 17 | p16_s11 | The translation overflows its box and was rendered at 24% of the original size; even a much shorter text would not fit, check this box in the preview | 福 | blessing |
| warning | 17 | p16_s11 | The translation overflows its box and was rendered at 24% of the original size; even a much shorter text would not fit, check this box in the preview | 福 | blessing |
| warning | 17 | p16_s12 | The translation overflows its box and was rendered at 24% of the original size; even a much shorter text would not fit, check this box in the preview | 福 | blessing |
| warning | 17 | p16_s12 | The translation overflows its box and was rendered at 24% of the original size; even a much shorter text would not fit, check this box in the preview | 福 | blessing |
| warning | 17 | p16_s13 | The translation overflows its box and was rendered at 21% of the original size; even a much shorter text would not fit, check this box in the preview | 福 | blessing |
| warning | 17 | p16_s13 | The translation overflows its box and was rendered at 21% of the original size; even a much shorter text would not fit, check this box in the preview | 福 | blessing |
| warning | 17 | p16_s7 | The translation overflows its box and was rendered at 20% of the original size; even a much shorter text would not fit, check this box in the preview | 福 | blessing |
| warning | 17 | p16_s7 | The translation overflows its box and was rendered at 20% of the original size; even a much shorter text would not fit, check this box in the preview | 福 | blessing |
| warning | 22 | p21_s22 | The translation overflows its box and was rendered at 19% of the original size; even a much shorter text would not fit, check this box in the preview | 古 | Inner Mongolia |
| warning | 22 | p21_s22 | The translation overflows its box and was rendered at 19% of the original size; even a much shorter text would not fit, check this box in the preview | 古 | Inner Mongolia |
| warning | 22 | p21_s26 | The translation overflows its box and was rendered at 29% of the original size; even a much shorter text would not fit, check this box in the preview | 内 | Inner Mongolia |
| warning | 22 | p21_s26 | The translation overflows its box and was rendered at 29% of the original size; even a much shorter text would not fit, check this box in the preview | 内 | Inner Mongolia |
| warning | 22 | p21_s27 | The translation overflows its box and was rendered at 21% of the original size; even a much shorter text would not fit, check this box in the preview | 陕 | Shaanxi |
| warning | 22 | p21_s27 | The translation overflows its box and was rendered at 21% of the original size; even a much shorter text would not fit, check this box in the preview | 陕 | Shaanxi |
| warning | 22 | p21_s34 | The translation overflows its box and was rendered at 25% of the original size; even a much shorter text would not fit, check this box in the preview | 江 | Jiangsu |
| warning | 22 | p21_s34 | The translation overflows its box and was rendered at 25% of the original size; even a much shorter text would not fit, check this box in the preview | 江 | Jiangsu |
| warning | 22 | p21_s37 | The translation overflows its box and was rendered at 17% of the original size; even a much shorter text would not fit, check this box in the preview | 庆 | Chongqing |
| warning | 22 | p21_s37 | The translation overflows its box and was rendered at 17% of the original size; even a much shorter text would not fit, check this box in the preview | 庆 | Chongqing |
| warning | 31 | p30_s1 | The translation overflows its box and was rendered at 43% of the original size; even a much shorter text would not fit, check this box in the preview | 黄山 | Huangshan |
| warning | 31 | p30_s1 | The translation overflows its box and was rendered at 43% of the original size; even a much shorter text would not fit, check this box in the preview | 黄山 | Huangshan |
| warning | 35 | p34_s10 | The translation overflows its box and was rendered at 39% of the original size; even a much shorter text would not fit, check this box in the preview | 有 | There are |
| warning | 35 | p34_s10 | The translation overflows its box and was rendered at 39% of the original size; even a much shorter text would not fit, check this box in the preview | 有 | There are |
| warning | 71 | p70_s18 | The translation overflows its box and was rendered at 38% of the original size; even a much shorter text would not fit, check this box in the preview | 宽 | width |
| warning | 71 | p70_s18 | The translation overflows its box and was rendered at 38% of the original size; even a much shorter text would not fit, check this box in the preview | 宽 | width |
| warning | 91 | p90_s4 | The translation overflows its box and was rendered at 33% of the original size; even a much shorter text would not fit, check this box in the preview | 相声魔术杂技歌舞 | Comedy Magic Acrobatics Dance |
| warning | 91 | p90_s4 | The translation overflows its box and was rendered at 33% of the original size; even a much shorter text would not fit, check this box in the preview | 相声魔术杂技歌舞 | Comedy Magic Acrobatics Dance |

### `llm_review` — 72 errors, 83 warnings

| Severity | Page | Segment | Message | Source | Translation |
|---|---|---|---|---|---|
| error | 4 | p3_s0 | Reviewer (meaning): "录" alone means "record/list"; in the running head it is the second character of 目录 and must be rendered "of", not "Contents". Suggested translation: "of" | 录 | Contents |
| error | 4 | p3_s1 | Reviewer (meaning): "目" alone is the first character of 目录 and must be rendered "Table", not "Table of". Suggested translation: "Table" | 目 | Table of |
| error | 4 | p3_s3 | Reviewer (meaning): "饲养场" means a livestock/feeding farm; "Farm" loses the meaning and conflicts with the threshing-floor label. Suggested translation: "Livestock farm" | 饲养场 | Farm |
| error | 6 | p5_s17 | Reviewer (meaning): The source is a garbled/overlapping label "位位" (likely "十位 个位"), but the translation adds the words "tens ones" which are not present; more importantly this cannot be verified. The given translation is acceptable if the source truly means the two place-value labels; no change needed. However, since 位位 alone is not meaningful Chinese, flagging is not warranted. | 位位 | tens ones |
| error | 6 | p5_s3 | Reviewer (omission): The measure word "个" is dropped; the context names the counted objects (apples), so it should be "18 (apples)". Suggested translation: "18 (apples)" | 18个 | 18 |
| error | 6 | p5_s8 | Reviewer (meaning): The multiplication-table rhyme "(三)六十八" corresponds to 3 × 6 = 18; the translation "3 × 6 = 18" as written treats 三 as the factor 3, whereas the source reads "(3) 6 × 6 = 18". Suggested translation: "3 × 6 = 18" | (三)六十八。 | 3 × 6 = 18 |
| error | 9 | p8_s11 | Reviewer (meaning): The placeholder is in the middle of the sentence, splitting "Number of sticks" from its verb "made"; the sentence reads ungrammatically and the object (squares) is missing. In the source it is likely a table header. The translation should read naturally. Suggested translation: "Number of sticks ⟦32.18.0⟧ made" | 小棒根数搭成的32.18.0 | Number of sticks 32.18.0 made |
| error | 9 | p8_s13 | Reviewer (meaning): Same issue as p8_s11: the sentence reads "Number of sticks ⟦32.20.0⟧ made", missing the object noun (squares) and ungrammatical. Suggested translation: "Number of sticks ⟦32.20.0⟧ made" | 小棒根数搭成的32.20.0 | Number of sticks 32.20.0 made |
| error | 9 | p8_s19 | Reviewer (number): The source equation 33÷4=8（根）····.1（根） is mathematically incorrect as written (33÷4=8 remainder 1, so units should be 个 but the source says 根), and the translation wrongly renders the first unit as "sticks" (根) while the source has 根 in both places. The translation should keep the source's inconsistency: "33÷4=8 (sticks) ····.1 (stick)", and the doubled spacing/stray period should be cleaned. Suggested translation: "33÷4=8 (sticks) ····1 (stick)" | 33÷4=8（根）····.1（根） | 33÷4=8 (sticks) ····.1 (stick) |
| error | 10 | p9_s10 | Reviewer (meaning): 'Look and say' omits the second verb 说一说 ('say/tell'); 'Look and tell' is closer, though acceptable. Suggested translation: "Look and tell." | 看一看，说一说。 | Look and say. |
| error | 10 | p9_s13 | Reviewer (meaning): '粘成一朵花' means glue together to form one flower; 'are pasted together to make one flower' is acceptable. | 5片树叶粘成一朵花。 | 5 leaves are pasted together to make one flower. |
| error | 11 | p10_s26 | Reviewer (meaning): 'partner.' completes the sentence from previous item; fine. | 伴说一说。 | partner. |
| error | 11 | p10_s4 | Reviewer (meaning): 'building blocks' is fine; source 积木 is blocks. No issue. | 有20块积木。 | There are 20 building blocks. |
| error | 11 | p10_s5 | Reviewer (meaning): 'Using the sharing process' — 结合 means 'in connection with/combined with'; better 'In connection with the sharing process'. Suggested translation: "(2) In connection with the sharing process, tell your partner what each step in the vertical form means." | （2）结合分物过程，和同伴说一说竖式中每一步的意思。 | (2) Using the sharing process, tell your partner what each … |
| error | 12 | p11_s1 | Reviewer (meaning): 'in total' for 一共 is correct per convention (¥/$ not applicable). | 一共55个草莓。 | There are 55 strawberries in total. |
| error | 12 | p11_s14 | Reviewer (meaning): '56 is larger than the dividend!' — 56比被除数大了 = '56 is larger than the dividend!'; correct. | 56比被除数大了！ | 56 is larger than the dividend! |
| error | 12 | p11_s2 | Reviewer (meaning): 'There are 8 plates.' fine. | 有8个盘子。 | There are 8 plates. |
| error | 13 | p12_s1 | Reviewer (meaning): 'Flower arranging.' — 插花 means arranging flowers; fine. | 1.插花。 | 1. Flower arranging. |
| error | 13 | p12_s14 | Reviewer (terminology): 'Calculate in vertical form.' — glossary says 竖式 => vertical form; correct. | 3.用竖式计算。 | 3. Calculate in vertical form. |
| error | 13 | p12_s18 | Reviewer (meaning): 'Forest doctor' — 森林医生 is a known exercise title 'Forest Doctor'; capitalize. Suggested translation: "4. Forest Doctor" | 4.森林医生 | 4. Forest doctor |
| error | 17 | p16_s10 | Reviewer (terminology): Inconsistent rendering of 福: translated as "blessing" while other instances keep 福; identical card labels must match. Suggested translation: "福" | 福 | blessing |
| error | 17 | p16_s11 | Reviewer (terminology): Inconsistent rendering of 福: translated as "blessing" while other instances keep 福; identical card labels must match. Suggested translation: "福" | 福 | blessing |
| error | 17 | p16_s12 | Reviewer (terminology): Inconsistent rendering of 福: translated as "blessing" while other instances keep 福; identical card labels must match. Suggested translation: "福" | 福 | blessing |
| error | 17 | p16_s13 | Reviewer (terminology): Inconsistent rendering of 福: translated as "blessing" while other instances keep 福; identical card labels must match. Suggested translation: "福" | 福 | blessing |
| error | 17 | p16_s21 | Reviewer (omission): The measure word 块 is dropped; the label should read "50 pieces" to name what is counted. Suggested translation: "50 pieces" | 50块 | 50 |
| error | 17 | p16_s7 | Reviewer (untranslated): The character 福 on the cards is left as "blessing" here but as the untranslated 福 elsewhere (p16_s8, s9); these are identical verbatim card labels and must be consistent. Suggested translation: "福" | 福 | blessing |
| error | 18 | p17_s19 | Reviewer (omission): The measure word 只 names the passengers (snow leopards) and must be translated; "Maximum 3" loses the referent. Suggested translation: "Maximum 3 snow leopards" | 限乘3只 | Maximum 3 |
| error | 22 | p21_s25 | Reviewer (untranslated): The source label “丁夏” is likely a scan of 宁夏 (Ningxia); the translation gives “Ningxia” which is a reasonable correction, but the mismatch with the source characters should be flagged. If the source truly reads 丁夏, this is a mistranslation. Suggested translation: "Ningxia" | 丁夏 | Ningxia |
| error | 22 | p21_s31 | Reviewer (untranslated): The source label 春海 is a misread/OCR fragment of 青海 (Qinghai); the translation 'Qinghai' is correct in meaning but the source character 春海 is not 青海. Given the map-label context, 'Qinghai' is the intended rendering, so no change needed beyond noting the source is garbled. Suggested translation: "Qinghai" | 春海 | Qinghai |
| error | 22 | p21_s36 | Reviewer (untranslated): The source label 四三 is a garbled/OCR fragment; context (map of China) suggests 四川 (Sichuan), and the translation 'Sichuan' matches that, but the source has two characters that do not form a province name. The translation should not silently invent a single province from a garbled label without note, but given map context, 'Sichuan' is the likely intended label. Suggested translation: "Sichuan" | 四三 | Sichuan |
| error | 22 | p21_s37 | Reviewer (untranslated): The source label 庆 is a single character; 庆 alone is not a standard province abbreviation (重庆 is abbreviated 渝). Rendering it as 'Chongqing' is likely intended from map context, but the source character does not itself stand for Chongqing. Suggested translation: "Chongqing" | 庆 | Chongqing |
| error | 22 | p21_s41 | Reviewer (meaning): The source lists 广东, 香港, 澳门, 海南 as separate entries (with 二 possibly a separator/OCR artifact). The translation merges them without punctuation, making it read as a single string; the regions should be separated. Suggested translation: "Guangdong, Hong Kong, Macao, Hainan" | 广东二香港澳门海南 | Guangdong Hong Kong Macao Hainan |
| error | 24 | p23_s11 | Reviewer (number): The placeholder ⟦92.15.0⟧ from the source is missing in the translation; it must be kept where it stands. Suggested translation: "2. Say how many ⟦92.15.0⟧ there are." | 2.说一说，有多少个日？92.15.0 | 2. Say how many 92.15.0 there are. |
| error | 26 | p25_s5 | Reviewer (number): The source label '千百十个' must be Th H T O, but the translation omits Th, changing the place-value labels. Suggested translation: "Th H T O" | 千百十个 | Th H T O |
| error | 27 | p26_s8 | Reviewer (number): The source label '千百' is Th H, but the translation adds Th H. Suggested translation: "Th H" | 千百 | Th H |
| error | 28 | p27_s20 | Reviewer (terminology): 写作： here introduces the written form of numbers; "Write:" is acceptable but the source verb is 写作 (write in digits). Consider matching the paired task with the preceding item's wording consistently. Suggested translation: "Write:" | 写作： | Write: |
| error | 30 | p29_s2 | Reviewer (untranslated): The placeholder ⟦0⟧/picture code 116.2.0 is kept but its meaning (a pictured object) is unclear; source has 个 (measure word) requiring the counted noun "How many ... are there?". Suggested translation: "How many 116.2.0 are there?" | 有多少个口116.2.0？ | How many 116.2.0 are there? |
| error | 31 | p30_s9 | Reviewer (terminology): Place-value labels 万千 here should use the standard abbreviations; 万 is ten-thousands (TTh is ten-thousands, so "TTh Th" is correct). No fix needed. | 万千 | TTh Th |
| error | 35 | p34_s10 | Reviewer (omission): 'There are' alone is not a translation of 有 in this label; the source likely has a blank or measure word that was dropped. Suggested translation: "There are ____" | 有 | There are |
| error | 36 | p35_s0 | Reviewer (terminology): 练习二 is 'Exercise 2' per glossary (习题 => exercises); acceptable. | 练习二 | Exercise 2 |
| error | 38 | p37_s9 | Reviewer (meaning): The source heading 找一找，说子说 (likely 找一找，说一说) means "Find and say", not "Find and talk". Suggested translation: "Find and say" | 找一找，说子说 | Find and talk |
| error | 46 | p45_s3 | Reviewer (terminology): 填一填 is glossed as "Fill in", but the glossary term is "Fill in"; the translation omits the blank where students fill in, which the source also lacks, so wording is acceptable but could read "Fill in the blanks" only if the source had 空. No change required. | 11.填一填 | 11. Fill in |
| error | 47 | p46_s0 | Reviewer (number): The source is 五 (five), but the translation says "Unit 5" — actually that matches; however the source "五力" is likely an OCR artifact of "五 加与减" (Unit 5 Addition and Subtraction), and the translation split it into "Unit 5". No change needed. | 五力 | Unit 5 |
| error | 53 | p52_s4 | Reviewer (meaning): The source asks how many more storybooks than comics there are (a difference/comparison question), but the translation asks for the total number of storybooks and comics, changing the meaning. Suggested translation: "How many more storybooks are there than comics?" | 故事书比连环画多多少本？ | How many more storybooks than comics are there? |
| error | 56 | p55_s18 | Reviewer (omission): The source has the adverb 共 (“in total, altogether”); “950 eggs in total” is fine, so only a wording note. | 共950个鸡蛋 | 950 eggs in total |
| error | 57 | p56_s25 | Reviewer (meaning): “他们做得对吗？” asks “Did they do it correctly?”; “Are they right?” is acceptable but less precise. Suggested translation: "Did they do it correctly? Talk with your partner." | 他们做得对吗？和同伴说一说 | Are they right? Talk with your partner. |
| error | 59 | p58_s22 | Reviewer (meaning): “结果分别是多少” asks what each result is, not “What is each result?” singular; acceptable, but could be “What is each result?”. Suggested translation: "What subtraction number sentences can you make with these numbers? What is each result?" | 用这些数可以列出哪些减法算式？结果分别是多少？ | What subtraction number sentences can you make with these n… |
| error | 63 | p62_s12 | Reviewer (terminology): "Sports shoes" is acceptable but "sneakers" or "athletic shoes" is more idiomatic for 运动鞋 in a retail label. Suggested translation: "Sneakers" | 运动鞋 | Sports shoes |
| error | 69 | p68_s5 | Reviewer (terminology): 认一认 is conventionally "Identify" (as on p70_s17); "identify" without an object is fine, but consistency with the other item is preferable. Suggested translation: "Compare and identify." | 比一比，认一认 | Compare and identify |
| error | 72 | p71_s3 | Reviewer (untranslated): Figure reference uses English word 'Figure' instead of keeping the label as in the source. Suggested translation: "⟦0⟧ Which pieces of the tangram can form a rectangle or a square? Try with the tangram in Appendix 3, Fig. 2." | （1）七巧板中哪些板可以拼出长方形或正方形？用附页3图2中的七巧板试一试。 | (1) Which pieces of the tangram can form a rectangle or a s… |
| error | 73 | p72_s8 | Reviewer (meaning): Source '边' (side) singular label; translation 'sides' plural changes meaning. Should be singular 'side'. Suggested translation: "side" | 边 | sides |
| error | 74 | p73_s4 | Reviewer (meaning): Source says '分别找出三种你认识的图形' = find three kinds of shapes you know in the patterns (overall), not three in each pattern. Direction of 'each' changes the task. Suggested translation: "2. Find three kinds of shapes you know from the patterns below." | 2.从下面的图案中分别找出三种你认识的图形。 | 2. Find three shapes you know in each of the patterns below. |
| error | 78 | p77_s4 | Reviewer (meaning): '哪根小棒' is 'which stick' (singular choice among options); 'Which stick can be used' is acceptable but the source implies picking one of several given sticks — consider 'Which stick can make a rectangle?' Suggested translation: "Which stick can make a rectangle?" | 用哪根小棒能拼成一个长方形？ | Which stick can be used to make a rectangle? |
| error | 82 | p81_s12 | Reviewer (terminology): 'One round is 60 minutes' — '走一圈' means 'one lap' or 'going around once'; 'one round' is acceptable but could be clearer. Also uses 'minutes' spelled out while other items use 'min'. Suggested translation: "One lap is 60 minutes, and 30 more minutes is 90 minutes" | 走一圈是60分，再走30分是90分 | One round is 60 minutes, and 30 more minutes is 90 minutes |
| error | 82 | p81_s15 | Reviewer (terminology): '1 hour' spelled out while other labels use 'h'; inconsistent unit abbreviation. Suggested translation: "1 h is 60" | 1时是60 | 1 hour is 60 |
| error | 82 | p81_s23 | Reviewer (number): The source says '跑2米' (run 2 m); this is a short distance, likely a scan/OCR issue, but the number 2 is kept correctly. No issue. Suggested translation: "Running 2 m takes about" | 跑2米大约需要 | Running 2 m takes about |
| error | 83 | p82_s0 | Reviewer (meaning): The source '1时=_分—分秒时—分' contains blanks and dashes indicating separate fill-in items (1 h = ___ min, ___ min ___ s, ___ h ___ min). The translation merges '—分秒时—分' into '___ min ___ s ___ h ___ min', which loses the dash separators and changes the structure of the exercise. Suggested translation: "3. Think and fill in. 1 h = ___ min ___ min ___ s ___ h ___ min" | 3.想一想，填一填1时=_分—分秒时—分 | 3. Think and fill in. 1 h = ___ min ___ min ___ s ___ h ___… |
| error | 83 | p82_s15 | Reviewer (meaning): '4时差5分' means 4 o'clock minus 5 minutes (5 minutes to 4), which is correct. No issue. Suggested translation: "5 minutes to 4" | 4时差5分 | 5 minutes to 4 |
| error | 83 | p82_s30 | Reviewer (terminology): '12 s' uses abbreviation while p82_s27-29 use 'seconds'; inconsistent. Suggested translation: "12 seconds" | 12秒 | 12 s |
| error | 86 | p85_s16 | Reviewer (omission): "再·" (then...) is left as a dangling dot instead of being translated. Suggested translation: "First record the time you leave home, then ..." | 先记录从家里出发时是几时几分，再· | First record the time you leave home, then · |
| error | 87 | p86_s21 | Reviewer (meaning): The source asks "大概用了多长时间？" (about how long does it/does one take), but the translation switches to past tense "did it take?". Suggested translation: "About how long does it take?" | 大概用了多长时间？ | About how long did it take? |
| error | 87 | p86_s22 | Reviewer (omission): The sentence is split; "每天上学路上" is cut off mid-sentence, losing "the time" clause beginning. Suggested translation: "3. Use the record table in Appendix 3 to record your own time to school each day for" | 3.利用附页3中的记录表记录你自己一周内每天上学路上 | 3. Use the record table in Appendix 3 to record your own ti… |
| error | 91 | p90_s15 | Reviewer (meaning): The source expresses that the first item is less than the second; the translation reverses the comparison ("is less than ... by"). Actually it says "is less than" which is correct? Wait: 360.24.l 比 360.24.0 少 means l is less than 0. The translation says l is less than 0, which is correct. No finding. | 360.24.l比口360.24.0少（ | 360.24.l is less than 360.24.0 by ( |
| error | 94 | p93_s0 | Reviewer (terminology): Glossary term 总复习 is rendered 'Final Review', which matches the glossary pair (总复习 => Final Review); no change needed. | 总复习 | Final Review |
| error | 97 | p96_s24 | Reviewer (omission): The source "请你提出一个数学问题，并尝" is split across items; the translation here renders only "并尝" as "and try", which is fine for a split item. However this item ends mid-sentence and p96_s25 completes it — the split is preserved. No omission within this item itself, but "并提出" ideally is "pose a math question" (translation says "Ask a math question"), acceptable. | （2）请你提出一个数学问题，并尝 | (2) Ask a math question and try |
| error | 98 | p97_s1 | Reviewer (omission): The source "做眼保健操大约需要" is an incomplete sentence that continues on the next line (likely with a time unit); the translation ends with "takes about" which preserves the truncation. However, "做眼保健操" means "doing eye exercises" — acceptable. But the line likely continues (e.g. "1分"); since this item is truncated, no fix possible within it. | 做眼保健操大约需要 | Doing eye exercises takes about |
| error | 98 | p97_s42 | Reviewer (number): In the source, the second conversion 2分米=（ ）厘米 is a single complete equation; the translation also shows 60 mm = () cm correctly, but the 2 dm = () cm blank should be present (it is). Verify no blank was added or dropped: the source has four blanks and the translation has four. No change needed if counts match. | 7千米=（）米2分米=（60毫米=（）厘米5厘米=（）毫米 | 7 km = () m 2 dm = () cm 60 mm = () cm 5 cm = () mm |
| error | 98 | p97_s7 | Reviewer (number): The source 5时 (5 hours) uses the time unit 时, but the translation renders it as "5 h"; all time labels in this table use minutes/seconds, so this hour label must be kept as 5 hours (5 h is acceptable only if the 时 unit itself is intended). Suggested translation: "5 h" | 5时 | 5 h |
| error | 99 | p98_s10 | Reviewer (meaning): The source 哪几根小棒可以搭成一个长方形? (plural 根数) asks which sticks (plural) can form a rectangle; "Which of the sticks" is acceptable, but the source uses 小棒 (counting sticks), so "Which sticks can be used to make a rectangle?" is closer. Suggested translation: "Which sticks can be used to make a rectangle?" | 哪几根小棒可以搭成一个长方形？ | Which of the sticks can be used to make a rectangle? |
| error | 99 | p98_s15 | Reviewer (meaning): "Mark three shapes you know" is acceptable, but 标出 means "label/mark out"; "Label three shapes you know in the picture below." is more precise. Suggested translation: "7. Label three shapes you know in the picture below." | 7.在下面的图中标出三个你认识的图形。 | 7. Mark three shapes you know in the picture below. |
| error | 99 | p98_s5 | Reviewer (number): The source ends 在括号里填上适当的单位 ("Fill in the appropriate unit in the brackets"); the translation drops 在括号里 ("in the brackets"). Suggested translation: "4. Fill in the appropriate unit in the brackets." | 4.在括号里填上适当的单位 | 4. Fill in the appropriate unit. |
| error | 100 | p99_s12 | Reviewer (terminology): '中速' is rendered 'medium' here but 'Med' (an invented abbreviation) in p99_s9; the translations are inconsistent and 'Med' is not a full word. Suggested translation: "How many cars are fast? How many are medium-speed? How many are slow?" | 快速的车有多少辆？中速的有多少辆？慢速的有多少辆？ | How many cars are fast? How many are medium? How many are s… |
| warning | 8 | p7_s12 | Reviewer (format): Two column labels run together without separation ("Number of sticks Squares made"); the source also has them adjacent but a line break/space should separate the two headers. Suggested translation: "Number of sticks / Squares made" | 小棒根数搭成的正方形 | Number of sticks Squares made |
| warning | 8 | p7_s14 | Reviewer (grammar): The dotted remainder separator "······" uses middle dots; should be a consistent notation. Suggested translation: "14÷4=3 (squares) ··2 (sticks)" | 14÷4=3（个）····*2（根） | 14÷4=3 (squares)······2 (sticks) |
| warning | 10 | p9_s1 | Reviewer (grammar): The ellipsis "···" uses three middle dots instead of the proper ellipsis; minor style. Suggested translation: "6 sticks make one house…" | 6根小棒搭一个房子··· | 6 sticks make one house··· |
| warning | 10 | p9_s15 | Reviewer (grammar): Comma splice; split into clauses. Suggested translation: "5 leaves make one flower, so 2 flowers can be made and 3 leaves are left." | 5片树叶粘一朵花，可以粘2朵花，还剩3片。 | 5 leaves make one flower, so 2 flowers can be made, with 3 … |
| warning | 11 | p10_s25 | Reviewer (format): Ellipsis rendered as '····' (four dots) instead of '...'. Suggested translation: "5. Think of a problem that can be solved with "10÷4=2...2", and tell your" | 5.想一个可以用“10÷4=2.····2”解决的问题，和同 | 5. Think of a problem that can be solved with "10÷4=2.····2… |
| warning | 11 | p10_s7 | Reviewer (format): Enumerator '(1)' kept; fine. No issue. | (1)填一填。 | (1) Fill in. |
| warning | 12 | p11_s0 | Reviewer (format): Heading 'Sharing Strawberries' — source is '分草莓', acceptable. | 分草莓 | Sharing Strawberries |
| warning | 12 | p11_s12 | Reviewer (format): 'Answer:' correct. | 答： | Answer: |
| warning | 12 | p11_s13 | Reviewer (grammar): 'Think and discuss.' — source 想一想，说一说 = 'Think and tell/say'; 'discuss' is acceptable. Suggested translation: "Are the calculations below correct? Think and tell." | 下面算得对吗？想一想，说一说 | Are the calculations below correct? Think and discuss. |
| warning | 12 | p11_s8 | Reviewer (format): 'Answer:' correct per convention (答 => Answer:). No issue. | 答： | Answer: |
| warning | 13 | p12_s0 | Reviewer (format): Heading 'Practice' correct for 练一练. | 练一练 | Practice |
| warning | 14 | p13_s2 | Reviewer (grammar): 'Max 4 people' — 'Max' is an abbreviation; write 'Maximum 4 people' or 'Up to 4 people'. Suggested translation: "Up to 4 people" | 限乘4人 | Max 4 people |
| warning | 18 | p17_s20 | Reviewer (grammar): "Thread the beads" reads as an imperative instruction; the context is describing the given bead pattern, so a description is more natural. Suggested translation: "The beads are threaded as shown below. Counting from left to right, what color is the 18th bead?" | 按下面的方式穿珠子，从左往右数，第18颗是什么颜色？ | Thread the beads as shown below. Counting from left to righ… |
| warning | 20 | p19_s22 | Reviewer (grammar): "one end always points south and the other end points north" is fine, but the comma splice/run-on rendering is awkward for a textbook; also "will not lose their way" is acceptable. | 指南针是我们的祖先在两千多年前发明的。指南针是辨认方向的能手，不论把它放在地球上的什么地方，它总是一端指南，一端指北。… | The compass was invented by our ancestors more than two tho… |
| warning | 21 | p20_s16 | Reviewer (format): The Chinese ellipsis “···” is rendered as “...”; the truncated sentence is acceptable, but keep the ellipsis style consistent. Suggested translation: "Northeast is between east and north, northwest ..." | 东北方向在东和北之间，西北.··· | Northeast is between east and north, northwest... |
| warning | 21 | p20_s22 | Reviewer (grammar): "look around the playground" is a slight addition for 到操场上看一看 (go to the playground and look), acceptable but could be "go to the playground and look around". Suggested translation: "Make a direction board, go to the playground and look around, record what is in each direction of the school, and then talk about it with a partner." | 制作一个方向板，到操场上看一看，记录校园各个方向有什么，再和同伴说一说。 | Make a direction board, look around the playground, record … |
| warning | 22 | p21_s26 | Reviewer (format): The source is the single-character abbreviation 内 for Inner Mongolia on a map label; the translation expands it, which is acceptable, but it deviates from the source label form. Suggested translation: "Inner Mongolia" | 内 | Inner Mongolia |
| warning | 25 | p24_s5 | Reviewer (format): The source compass label 北 is rendered 'N' here, while the parallel label 北 on p21_s44 is rendered 'North'; consistency of compass labels is preferred (use the same form in both). Suggested translation: "North" | 北 | N |
| warning | 34 | p33_s12 | Reviewer (format): Heading 'Estimate and fill in' is missing the glossary term for 填一填 ('Fill in'). Suggested translation: "Estimate and Fill in" | 估一估，填一填 | Estimate and fill in |
| warning | 34 | p33_s14 | Reviewer (format): The answer blank （） was replaced by '()' instead of keeping the parentheses/blank as in the source. Suggested translation: "There are about （） grains." | 大约有（）粒。 | About () grains. |
| warning | 34 | p33_s9 | Reviewer (grammar): 'talk about it' is vague; the source asks to talk about the estimate. Suggested translation: "Work in groups, estimate, and talk about it." | 小组合作，估一估，说一说。 | Work in groups, estimate and talk about it. |
| warning | 35 | p34_s14 | Reviewer (grammar): 'There are 50 jelly beans.' is fine, but source '有 50颗。' is a label; agreement ok. No change needed. | 有 50颗。 | There are 50 jelly beans. |
| warning | 35 | p34_s16 | Reviewer (format): Source has an empty （） blank; translation inserted '__' that is not in the source. Suggested translation: "There are about （） jelly beans." | 大约有（）颗。 | There are about (__) jelly beans. |
| warning | 36 | p35_s18 | Reviewer (format): 千百 => Th H : standard place-value abbreviations are TTh Th H T O; 千 is thousands = Th, 百 = H, so 'Th H' is acceptable. | 千百 | Th H |
| warning | 36 | p35_s27 | Reviewer (format): Place-value column labels must follow the standard abbreviations; the source runs 千 and 百 together, and the rendered 百 is missing (it appears separately in the next item), so this label should be "Th H". Suggested translation: "Th H" | 千百 | Th H |
| warning | 36 | p35_s30 | Reviewer (format): 百 as a place-value column label should be the standard abbreviation "H", which is correct. Suggested translation: "H" | 百 | H |
| warning | 39 | p38_s3 | Reviewer (format): Table column labels should be capitalised consistently; "Your measurement" is a heading fragment. Suggested translation: "Your measurement" | 你的测量 | Your measurement |
| warning | 39 | p38_s8 | Reviewer (format): Missing full stop after the exercise instruction. Suggested translation: "3. Fill in." | 3.填一填 | 3. Fill in |
| warning | 41 | p40_s25 | Reviewer (format): The continuation fragment should stand as its own line as in the source. Suggested translation: "get home?" | 回到家？ | get home? |
| warning | 42 | p41_s0 | Reviewer (format): This is a unit heading (整理与复习), which should be rendered as a unit heading per the convention. Suggested translation: "Unit Review" | 整理与复习 | Review |
| warning | 42 | p41_s25 | Reviewer (grammar): The word 数位 is rendered as "places", which is acceptable, but the sentence structure "Which places have you learned?" is awkward and the source term is 数位 (place values). Also "分别" (respectively) is not fully conveyed. Suggested translation: "Which place values have you learned? Move the beads on the counting frame and explain what each "2" in the table above represents respectively." | 你学过了哪些数位？在计数器上拨一拨，说说上表数据中的“2”分别表示多少。 | Which places have you learned? Move the beads on the counti… |
| warning | 42 | p41_s26 | Reviewer (grammar): "Organise" is British spelling; also the sentence is a compound imperative that should be joined with a comma and "and" is fine, but capitalization/wording is slightly informal. Minor style only. Suggested translation: "Organize the length units you have learned, and explain how they are related." | 整理一下你学过的长度单位，说说它们之间有什么关系。 | Organise the length units you have learned and explain how … |
| warning | 44 | p43_s20 | Reviewer (format): Label is capitalised 'Residential area', while the same phrase appears lowercase elsewhere; label casing inconsistent. Suggested translation: "Residential area" | 居住区 | Residential area |
| warning | 46 | p45_s6 | Reviewer (format): Missing space before the equal sign after the number; results in "3000 m =" which is acceptable, though consistent spacing is preferred. Suggested translation: "3000 m =" | 3000米= | 3000 m = |
| warning | 50 | p49_s21 | Reviewer (format): Direction labels on diagrams are usually abbreviated (N, E) or written lowercase (north, east); the inconsistent capitalization among the direction labels should be made uniform. Suggested translation: "North" | 北 | North |
| warning | 50 | p49_s23 | Reviewer (format): Direction labels on diagrams are usually abbreviated (N, E) or written lowercase (north, east); the inconsistent capitalization among the direction labels should be made uniform. Suggested translation: "East" | 东 | East |
| warning | 58 | p57_s12 | Reviewer (format): The source “懂吗？和同伴说一说。” is split across items by the scan; the translation keeps the split correctly. No change. | 懂吗？和同伴说一说。 | understand? Talk with your partner. |
| warning | 58 | p57_s16 | Reviewer (format): “拨一拨” is “move the beads on the counting frame”, which is acceptable; no change needed. | 1.画一画，填一填，并在计数器上拨一拨。 | 1. Draw, fill in, and move the beads on the counting frame. |
| warning | 59 | p58_s25 | Reviewer (format): “一年级二年级” is a table row of two column labels; the translation should separate them clearly as two labels. Suggested translation: "Grade 1 Grade 2" | 一年级二年级 | Grade 1 Grade 2 |
| warning | 61 | p60_s19 | Reviewer (grammar): Source ends with a comma; translation replaces it with a period. Minor punctuation deviation. Suggested translation: "1. How many cards did Taoqi and Xiaoxiao collect in total? Calculate and check," | 1.淘气和笑笑一共收集了多少张卡片？计算并验算， | 1. How many cards did Taoqi and Xiaoxiao collect in total? … |
| warning | 64 | p63_s17 | Reviewer (format): The row label "Day" is added before the weekday abbreviations; the source has only 星期一二三四五 (Mon Tue Wed Thu Fri). Suggested translation: "Mon Tue Wed Thu Fri" | 星期一二三四五 | Day Mon Tue Wed Thu Fri |
| warning | 64 | p63_s6 | Reviewer (format): The two prices are run together on one line; a line break (as in the original vertical/figure layout) improves readability. Suggested translation: "Original price: ¥398 Current price: ¥350" | 原价：398元现价：350元 | Original price: ¥398 Current price: ¥350 |
| warning | 64 | p63_s7 | Reviewer (format): The two prices are run together on one line; a line break improves readability. Suggested translation: "Original price: ¥235 Current price: ¥198" | 原价：235元现价：198元 | Original price: ¥235 Current price: ¥198 |
| warning | 64 | p63_s8 | Reviewer (format): The two prices are run together on one line; a line break improves readability. Suggested translation: "Original price: ¥1000 Current price: ¥960" | 原价：1000元现价：960元 | Original price: ¥1000 Current price: ¥960 |
| warning | 66 | p65_s7 | Reviewer (format): The source writes 记作：1 with the angle symbol omitted before 1; the translation adds ∠. The symbol is implied and conventional, so acceptable. Suggested translation: "Written as: ∠1. Read as: angle 1." | 记作：1。读作：角1。 | Written as: ∠1. Read as: angle 1. |
| warning | 68 | p67_s15 | Reviewer (format): The three repeated answer blanks run together without separation; they should be clearly separated, and the blank parentheses are retained but spacing is lost. Suggested translation: "() angles left () angles left () angles left" | 还剩（）个角还剩（）个角还剩（）个角 | () angles left () angles left () angles left |
| warning | 71 | p70_s16 | Reviewer (format): The blank "___" and the fill-in blank "_" are preserved, which is correct; the sentence construction is acceptable but "The four sides of a square ___" leaves the predicate implicit — fine for a fill-in item. Suggested translation: "The four sides of a square ___ and the four angles are all _ angles." | 正方形的四条边___四个角都是_角。 | The four sides of a square ___ and the four angles are all … |
| warning | 71 | p70_s9 | Reviewer (format): The dotted fill-in "····" is preserved, which is correct; but the translation adds a period before the blank dots, changing the visual fill-in line. Keep punctuation style consistent with the source. Suggested translation: "Each angle of a rectangle is ····" | 长方形的每个角都是···· | Each angle of a rectangle is ···· |
| warning | 73 | p72_s4 | Reviewer (grammar): Imperative 'Pull left' is acceptable, but stylistically 'Pull to the left' reads better in textbook instructions. Suggested translation: "Pull to the left" | 向左拉 | Pull left |
| warning | 73 | p72_s5 | Reviewer (grammar): Same stylistic issue as p72_s4. Suggested translation: "Pull to the right" | 向右拉 | Pull right |
| warning | 73 | p72_s6 | Reviewer (grammar): Incomplete phrase; 'Compare their' is fine as a label but could read 'Compare their...' Suggested translation: "Compare their..." | 比一比它们的 | Compare their |
| warning | 73 | p72_s7 | Reviewer (format): Source uses 角··．． (angle with dotted continuation); ellipsis style differs but meaning preserved. Suggested translation: "After pulling, the angles..." | 拉动后，角··．． | After pulling, the angles... |
| warning | 74 | p73_s9 | Reviewer (grammar): 'Read and tell' is acceptable, but 'Read and retell' better renders 讲一讲. Suggested translation: "5. Read and retell." | 5.读一读，讲一讲。 | 5. Read and tell. |
| warning | 75 | p74_s1 | Reviewer (grammar): 'Enjoy the patterns' misrenders 欣赏 (appreciate); use 'Appreciate the patterns below...' Suggested translation: "Appreciate the patterns below and find the shapes you know." | 欣赏下面的图案，找出你认识的图形。 | Enjoy the patterns below and find the shapes you know. |
| warning | 75 | p74_s5 | Reviewer (format): Source ends with '我用正方形和·' (and ...), the trailing ellipsis/dot is dropped. Suggested translation: "I use squares and..." | 我用正方形和· | I use squares and |
| warning | 76 | p75_s13 | Reviewer (format): Fragment ends with 'the' and continues in p75_s14; acceptable split but sentence reads 'trace it on the' + 'grid paper below.' Suggested translation: "4. Choose your favourite pattern designed by your classmates and trace it on the grid paper below." | 4.在全班同学设计的图案中选择一个你最喜欢的，描在下面 | 4. Choose your favourite pattern designed by your classmate… |
| warning | 76 | p75_s5 | Reviewer (format): Source '用4个长方形拼出一' is incomplete continuing to p75_s6 '个新图形社'; translation split awkwardly ('a' + 'new shape'). Suggested translation: "Use 4 rectangles to make a new shape" | 用4个长方形拼出一 | Use 4 rectangles to make a |
| warning | 77 | p76_s3 | Reviewer (format): Fragment is incomplete; continues on next line in source. Translation fine as fragment. Suggested translation: "2. Tell which angles in the figures below are acute angles, which are right angles, and which" | 2.说一说下面各图中的角哪些是锐角，哪些是直角，哪些 | 2. Tell which angles in the figures below are acute angles,… |
| warning | 77 | p76_s4 | Reviewer (grammar): Fragment 'are obtuse angles.' is missing its subject; as a label it reads incompletely. Suggested translation: "are obtuse angles." | 是钝角。 | are obtuse angles. |
| warning | 84 | p83_s1 | Reviewer (grammar): "Fill in and talk about it" is awkward; the standard instruction wording should be used. Suggested translation: "Fill in and say what you find." | 填一填，说一说。 | Fill in and talk about it. |
| warning | 84 | p83_s3 | Reviewer (format): Missing punctuation between the two clauses; the source has no comma but English needs a separator. Suggested translation: "Taoqi gets up at 6:30 and has breakfast at 6:55 ····" | 淘气早上6时30分起床6时55分吃早餐···· | Taoqi gets up at 6:30 and has breakfast at 6:55 ···· |
| warning | 87 | p86_s23 | Reviewer (format): This fragment continues the previous sentence; as a separate translation segment it reads as a dangling label. Suggested translation: "a week." | 用的时间。 | a week. |
| warning | 87 | p86_s6 | Reviewer (format): "Arrival time Time taken on the way" merges two column labels without a separator. Suggested translation: "Arrival time Time taken on the way" | 到校时间路上用的时间 | Arrival time Time taken on the way |
| warning | 88 | p87_s7 | Reviewer (format): Source uses the capital Latin V as part of the pattern (√√××Vxx); the translation changed it to the check-mark-like symbol √. Suggested translation: "The arrangement of the flower pots also follows a pattern: √√××Vxx..." | 花盆的摆放也是有规律的：√√××Vxx··· | The arrangement of the flower pots also follows a pattern: … |
| warning | 91 | p90_s14 | Reviewer (format): The answer blank （ ） before 个 is missing; the measure word indicates the counted noun blank. Suggested translation: "___," | ）个， | ), |
| warning | 91 | p90_s15 | Reviewer (format): The trailing blank/括号 is rendered as a lone "(" without the matching blank; keep the answer blank format as in the source. Suggested translation: "360.24.l is less than 360.24.0 by ( )" | 360.24.l比口360.24.0少（ | 360.24.l is less than 360.24.0 by ( |
| warning | 91 | p90_s19 | Reviewer (grammar): "Below is..." is unnatural for a textbook; use "The following is...". Suggested translation: "The following is Qisi's survey record." | 下面是奇思的调查记录。 | Below is Qisi's survey record. |
| warning | 91 | p90_s27 | Reviewer (format): The answer blank is rendered as "()" rather than an underscore blank. Suggested translation: "(1) Qisi surveyed ____ students." | (1)奇思调查了（）名同学。 | (1) Qisi surveyed () students. |
| warning | 91 | p90_s3 | Reviewer (grammar): “performances” is an addition; the source says 节目 (programmes/shows), and the sentence asks which programme the classmates like best. Suggested translation: "Let's survey which programmes the students like best." | 我们调查一下同学们最喜爱的节目。 | Let's survey which performances the students like best. |
| warning | 91 | p90_s32 | Reviewer (grammar): "Talk about it." is an incomplete translation of 说一说 ("Talk about it") in context; better as "Discuss." Suggested translation: "(3) Discuss: What suggestions do you have about diet?" | （3）说一说，在饮食方面，你有什么建议？ | (3) Talk about it. What suggestions do you have about diet? |
| warning | 91 | p90_s7 | Reviewer (format): The answer blank （ ） must be kept as an answer blank, not as empty parentheses. Suggested translation: "Miaoxiang surveyed ___ students." | 妙想调查了（）名同学。 | Miaoxiang surveyed () students. |
| warning | 92 | p91_s11 | Reviewer (grammar): "·····" ellipsis rendered as "..."; keep the style consistent with the source ellipsis. Suggested translation: "apple, banana, banana, orange, pear……" | 苹果、香蕉、香蕉橘子、梨····· | apple, banana, banana, orange, pear... |
| warning | 92 | p91_s5 | Reviewer (grammar): "which kind less" is elliptical and awkward; supply "of". Suggested translation: "How should we buy the fruit? Which kind should we buy more of, and which kind less of?" | 应该怎么买水果呢？哪一种多买些，哪一种少买些？ | How should we buy the fruit? Which kind should we buy more … |
| warning | 93 | p92_s3 | Reviewer (format): Enumerator "(2)" is followed by no space; the source has a full-width parenthesis and space-style. Suggested translation: "(2) Below are Taoqi's and Xiaoxiao's records. Which do you like?" | （2)下面是淘气和笑笑的记录，你喜欢哪个？ | (2) Below are Taoqi's and Xiaoxiao's records. Which do you … |
| warning | 94 | p93_s19 | Reviewer (format): The place-value column labels 千百十个 should be translated with the standard abbreviations Th H T O (thousands, hundreds, tens, ones), not 'Th H T O' as given... Actually the source has four labels 千 百 十 个 = Th H T O, but the translation gives 'Th H T O' which is correct. No problem. | 千百十个 | Th H T O |
| warning | 97 | p96_s25 | Reviewer (grammar): "to answer it." as a standalone fragment is fine given the split, but the preceding item ended with "and try" — the pair reads "Ask a math question and try to answer it." which is acceptable. No change needed. | 试解答。 | to answer it. |
| warning | 98 | p97_s0 | Reviewer (grammar): "Choose and draw" — the source "选一选，画" is an incomplete instruction (the object of "draw" is on the next line); the translation matches the truncation. Acceptable as-is. | 11.选一选，画 | 11. Choose and draw |
| warning | 98 | p97_s25 | Reviewer (format): Inconsistent capitalization of place-name labels ("Birch Forest", "Zoo", "Lake Center Island"); map labels usually use lowercase except for proper names. Consider "Birch Forest" is fine as a proper name. | 桦树林 | Birch Forest |
| warning | 98 | p97_s4 | Reviewer (format): Source time units 分/时/秒 are abbreviated as min/h/s; the instruction says only standard units (m, km, cm, min, h) are abbreviated, and 秒 (seconds) is conventionally "s" — acceptable, but 时 in p97_s7 conflicts with 小时 usage; keep consistent. | 5分 | 5 min |
| warning | 99 | p98_s1 | Reviewer (format): Fragments ( )厘米 ("() cm") are duplicated across several labels; the source brackets (（）) are rendered as "()", which is fine, but ensure blanks stay where the source has them. | ）厘米 | () cm |
| warning | 99 | p98_s12 | Reviewer (format): The string of measurements 4厘米2厘米3厘米2厘米5厘米4厘米 is run together in the source; the translation separates them with spaces, which is a reasonable reading but the grouping (the sticks) may be lost. | 4厘米2厘米3厘米2厘米5厘米4厘米 | 4 cm 2 cm 3 cm 2 cm 5 cm 4 cm |
| warning | 99 | p98_s13 | Reviewer (format): Two instructions run together in the source (画出一个长方形画出一个正方形); the translation adds a sentence break, which is acceptable but should be consistently separated. Suggested translation: "Draw a rectangle. Draw a square." | 画出一个长方形画出一个正方形 | Draw a rectangle. Draw a square. |
| warning | 100 | p99_s14 | Reviewer (grammar): The semicolon-separated clauses contain comma lists that are ambiguous; each name's list of animals should be separated clearly from the next name. Suggested translation: "Taoqi: rabbit, chicken, bird, tiger and bear; Xiaoxiao: dog, cat, bear and tiger; Qisi: dog, tiger, bear and elephant; Miaoxiang: none; Lele: cat and bear." | 淘气：兔、鸡、鸟、老虎和熊；笑笑：狗、猫、熊和老虎；奇思：狗、老虎、熊和大象；妙想：没有；乐乐：猫和熊。 | Taoqi: rabbit, chicken, bird, tiger and bear; Xiaoxiao: dog… |

### `numbers` — 2 errors, 0 warnings

| Severity | Page | Segment | Message | Source | Translation |
|---|---|---|---|---|---|
| error | 44 | p43_s21 | Number "3" from the source is missing in the translation; keep every number exactly as written in the source | ③试验田在居住区的西北方。 | ⑤ The experimental field is to the northwest of the residen… |
| error | 82 | p81_s6 | Number "5" from the source is missing in the translation; keep every number exactly as written in the source | 5秒 | 15 s |

### `target_script` — 1 error, 0 warnings

| Severity | Page | Segment | Message | Source | Translation |
|---|---|---|---|---|---|
| error | 17 | p16_s9 | Only 0% of the letters in the translation are in the English script; write the whole translation in English (formulas, variable names, units and proper names copied from the source excepted) | 福福福福福福福 | 福福福福福福福 |

### `untranslated` — 7 errors, 0 warnings

| Severity | Page | Segment | Message | Source | Translation |
|---|---|---|---|---|---|
| error | 17 | p16_s14 | 1 letter(s) of the source script remain untranslated ("福"); translate all text into English | 福 | 福 |
| error | 17 | p16_s15 | 2 letter(s) of the source script remain untranslated ("福福"); translate all text into English | 福福 | 福福 |
| error | 17 | p16_s16 | 1 letter(s) of the source script remain untranslated ("福"); translate all text into English | 福 | 福 |
| error | 17 | p16_s9 | 7 letter(s) of the source script remain untranslated ("福福福福福福福"); translate all text into English | 福福福福福福福 | 福福福福福福福 |
| error | 92 | p91_s13 | 1 letter(s) of the source script remain untranslated ("下"); translate all text into English | 下TF正 | 下 TF 正 |
| error | 93 | p92_s6 | 3 letter(s) of the source script remain untranslated ("卌"); translate all text into English | 丰丰丰三 | 卌 卌 卌 \|\|\|\| |
| error | 100 | p99_s6 | 2 letter(s) of the source script remain untranslated ("丰三"); translate all text into English | 丰三 | 丰三 |

### `image_text` — 0 errors, 10 warnings

| Severity | Page | Segment | Message | Source | Translation |
|---|---|---|---|---|---|
| warning | 6 | p5_i20_17 | The text '上面的过程可以用除法竖式表示。认一认，说一说。' was left in the source language (inline pictograms the OCR cannot read (left in the picture)): the line is built around symbols or pictures the OCR could not read - check the page in the preview | 上面的过程可以用除法竖式表示。认一认，说一说。 |  |
| warning | 6 | p5_i20_17 | The text '上面的过程可以用除法竖式表示。认一认，说一说。' was left in the source language (inline pictograms the OCR cannot read (left in the picture)): the line is built around symbols or pictures the OCR could not read - check the page in the preview | 上面的过程可以用除法竖式表示。认一认，说一说。 |  |
| warning | 35 | p34_i136_6 | The text '对比，科学界才初步确定这是一群类似于蜥蜴的早已灭绝的爬行动物。' was left in the source language (inline pictograms the OCR cannot read (left in the picture)): the line is built around symbols or pictures the OCR could not read - check the page in the preview | 对比，科学界才初步确定这是一群类似于蜥蜴的早已灭绝的爬行动物。 |  |
| warning | 35 | p34_i136_6 | The text '对比，科学界才初步确定这是一群类似于蜥蜴的早已灭绝的爬行动物。' was left in the source language (inline pictograms the OCR cannot read (left in the picture)): the line is built around symbols or pictures the OCR could not read - check the page in the preview | 对比，科学界才初步确定这是一群类似于蜥蜴的早已灭绝的爬行动物。 |  |
| warning | 69 | p68_i272_5 | The text '板比比' was left in the source language (inline pictograms the OCR cannot read (left in the picture)): the line is built around symbols or pictures the OCR could not read - check the page in the preview | 板比比 |  |
| warning | 69 | p68_i272_5 | The text '板比比' was left in the source language (inline pictograms the OCR cannot read (left in the picture)): the line is built around symbols or pictures the OCR could not read - check the page in the preview | 板比比 |  |
| warning | 88 | p87_i348_14 | The text '规律的，我是这样表示' was left in the source language (inline pictograms the OCR cannot read (left in the picture)): the line is built around symbols or pictures the OCR could not read - check the page in the preview | 规律的，我是这样表示 |  |
| warning | 88 | p87_i348_14 | The text '规律的，我是这样表示' was left in the source language (inline pictograms the OCR cannot read (left in the picture)): the line is built around symbols or pictures the OCR could not read - check the page in the preview | 规律的，我是这样表示 |  |
| warning | 88 | p87_i348_5 | The text '欢的方式表示。' was left in the source language (inline pictograms the OCR cannot read (left in the picture)): the line is built around symbols or pictures the OCR could not read - check the page in the preview | 欢的方式表示。 |  |
| warning | 88 | p87_i348_5 | The text '欢的方式表示。' was left in the source language (inline pictograms the OCR cannot read (left in the picture)): the line is built around symbols or pictures the OCR could not read - check the page in the preview | 欢的方式表示。 |  |

### `length_ratio` — 0 errors, 1 warning

| Severity | Page | Segment | Message | Source | Translation |
|---|---|---|---|---|---|
| warning | 80 | p79_s12 | The translation looks too short: 17 characters for 19 translatable source characters (ratio 0.89, about 2.60 expected); check that nothing was omitted | 4时12分9时20分6时08分1时30分8时55分 | 4:12, 9:20, 6:08, 1:30, 8:55 |
