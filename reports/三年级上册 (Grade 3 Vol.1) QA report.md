# QA report

**Result:** QA FAILED after 3 rounds: 209 errors, 155 warnings (2243.6 s); proofread: 969 corrections applied; output file checks: 0 error(s)

**Document:** 数学 (zh → en, 111 page(s), 2168 translatable segment(s))

**Checks run:** `completeness`, `placeholders`, `numbers`, `untranslated`, `target_script`, `glossary`, `length_ratio`, `formatting`, `layout_fit`, `image_text`, `llm_review`, `output_checks`

## Rounds

| Round | Errors | Warnings | Re-translated | Passed | Duration |
|---|---|---|---|---|---|
| 1 | 339 | 347 | 317 segment(s) | no | 522.9 s |
| 2 | 251 | 396 | 228 segment(s) | no | 594.6 s |
| 3 | 287 | 346 | 0 segment(s) | no | 168.6 s |

- Round 1: llm_review ×544, layout_fit ×115, formatting ×11, glossary ×6, completeness ×5, untranslated ×3, image_text ×1, placeholders ×1
- Round 2: llm_review ×529, layout_fit ×96, untranslated ×6, formatting ×5, glossary ×4, placeholders ×4, image_text ×1, length_ratio ×1, target_script ×1
- Round 3: llm_review ×526, layout_fit ×88, formatting ×8, glossary ×4, completeness ×2, placeholders ×2, untranslated ×2, image_text ×1

## Final issues (364)

### `completeness` — 8 errors, 0 warnings

| Severity | Page | Segment | Message | Source | Translation |
|---|---|---|---|---|---|
| error | 6 | p5_s18 | The translation "¥?" contains no words; translate the complete source text | ？元 | ¥? |
| error | 7 | p6_s6 | The translation "¥?" contains no words; translate the complete source text | ？元 | ¥? |
| error | 15 | p14_s21 | The translation "¥?" contains no words; translate the complete source text | ？元 | ¥? |
| error | 15 | p14_s25 | The translation "¥?" contains no words; translate the complete source text | ？元 | ¥? |
| error | 25 | p24_s16 | The translation "¥?" contains no words; translate the complete source text | ？元 | ¥? |
| error | 35 | p34_s28 | The translation "?" contains no words; translate the complete source text | ？枝 | ? |
| error | 75 | p74_s24 | The translation "," contains no words; translate the complete source text | 时分开车， | , |
| error | 75 | p74_s9 | The translation "__:__" contains no words; translate the complete source text | 时分 | __:__ |

### `formatting` — 50 errors, 0 warnings

| Severity | Page | Segment | Message | Source | Translation |
|---|---|---|---|---|---|
| error | 13 | p12_s8 | The source does not end with a question mark; do not end the translation with one | 看一看，说一说，用（70一46）÷8还能解决什么问题 | Look and say: what other problems can be solved with (70−46… |
| error | 25 | p24_s0 | The source does not end with a question mark; do not end the translation with one | 节余多少钱 | How Much Is Saved? |
| error | 27 | p26_s11 | The source does not end with a question mark; do not end the translation with one | （1）水上天地比冒险乐园少售出多少张票 | (1) How many fewer tickets did Water World sell than Advent… |
| error | 28 | p27_s7 | Keep the line breaks of the source: it has 0 line break(s), the translation has 4 | 北京—保定北京一石家庄北京—郑州北京一洛阳北京一西安 | Beijing–Baoding Beijing–Shijiazhuang Beijing–Zhengzhou Beij… |
| error | 29 | p28_s27 | Keep the line breaks of the source: it has 0 line break(s), the translation has 2 | 博物馆一邮局博物馆一学校博物馆一公园 | Museum–Post office Museum–School Museum–Park |
| error | 29 | p28_s5 | Keep the line breaks of the source: it has 0 line break(s), the translation has 2 | 武汉一九江武汉一芜湖武汉一南京 | Wuhan–Jiujiang Wuhan–Wuhu Wuhan–Nanjing |
| error | 30 | p29_s18 | Start the translation with the list marker "三、" exactly as in the source | 三、星期五行驶的里程数超过200千米，再·· | Wednesday and Friday he drove more than 200 km, then… |
| error | 31 | p30_s31 | The source ends with a question mark; end the translation with a question mark too | （2）星期一早上出发时里程表的读数是632千米，算一算，赵叔叔星期五晚上到家时里程表的读数是多少？ | (2) When he set off on Monday morning, the odometer read 63… |
| error | 33 | p32_s14 | Keep the line breaks of the source: it has 0 line break(s), the translation has 2 | 安多一那曲那曲一当雄当雄一拉萨 | Amdo–Nagqu Nagqu–Damxung Damxung–Lhasa |
| error | 33 | p32_s8 | Keep the line breaks of the source: it has 0 line break(s), the translation has 3 | 格尔木一安多格尔木一那曲格尔木一当雄格尔木一拉萨 | Golmud–Amdo Golmud–Nagqu Golmud–Damxung Golmud–Lhasa |
| error | 34 | p33_s1 | The source does not end with a question mark; do not end the translation with one | 小树有多少棵 | How Many Saplings? |
| error | 36 | p35_s0 | The source does not end with a question mark; do not end the translation with one | 需要多少钱 | How Much Money? |
| error | 41 | p40_s9 | The source does not end with a question mark; do not end the translation with one | （2）一双鞋比一副手套贵多 | (2) How much more do the shoes cost than the gloves? |
| error | 65 | p64_s28 | "(pieces)" is not a translation of a measure word: write the plural noun of the counted thing ((apples), (chicks), (sticks)) or, when the exercise does not name it, drop the parentheses | 种类昆虫标本/个植物标本/个 | Type Insect specimens (pieces) Plant specimens (pieces) |
| error | 66 | p65_s6 | The source ends with a question mark; end the translation with a question mark too | 算一算，张老师买矿泉水共花多少元？ | Work out how much Teacher Zhang spent on mineral water in a… |
| error | 71 | p70_s2 | The source ends with a question mark; end the translation with a question mark too | 说一说，关于年、月、日，你知道些什么？ | Say what you know about years, months and days. |
| error | 73 | p72_s19 | The source does not end with a question mark; do not end the translation with one | 谁最小，相差多 | who is the youngest, and how many days apart? |
| error | 73 | p72_s28 | The source ends with a question mark; end the translation with a question mark too | 你知道吗 | Did you know |
| error | 82 | p81_s10 | Remove the symbol(s) ○: they are not in the source (a picture in the book is not a symbol; leave it out rather than inventing one) | 用△标出父亲的休息日，用标出母亲的休息日。你发现了什 | Mark the father's days off with △ and the mother's days off… |
| error | 82 | p81_s12 | Remove the symbol(s) △ ○: they are not in the source (a picture in the book is not a symbol; leave it out rather than inventing one) | 同时标有和的日子有4号、8 | The days marked with both △ and ○ are the 4th, 8 |
| error | 82 | p81_s15 | Remove the symbol(s) √: they are not in the source (a picture in the book is not a symbol; leave it out rather than inventing one) | 再用，标出奇思的休息日。你又发现了什么？ | Then mark Qisi's days off with √. What else do you find? |
| error | 82 | p81_s16 | Remove the symbol(s) △ ○: they are not in the source (a picture in the book is not a symbol; leave it out rather than inventing one) | 同时标有、和√的日子有4号、24号。 | The days marked with △, ○ and √ are the 4th and 24th. |
| error | 83 | p82_s23 | The source ends with a question mark; end the translation with a question mark too | 你知道吗 | Did you know |
| error | 84 | p83_s24 | The source does not end with a question mark; do not end the translation with one | 每本笔记本3.15元就是3元15角吧 | A notebook is ¥3.15, so that's 3 yuan 15 jiao, right? |
| error | 84 | p83_s8 | Keep the line breaks of the source: it has 0 line break(s), the translation has 3 | 每本笔记本每支铅笔___元，每把尺子每支钢笔 | Each notebook Each pencil ___ yuan, is Each ruler Each pen |
| error | 85 | p84_s26 | Start the translation with the list marker "4." exactly as in the source | 4. 5元。 | ¥4.5. |
| error | 85 | p84_s29 | The source ends with a question mark; end the translation with a question mark too | 你知道吗 | Did you know |
| error | 86 | p85_s10 | Start the translation with the list marker "5." exactly as in the source | 5. 10元 | ¥5.10 |
| error | 86 | p85_s4 | Start the translation with the list marker "1." exactly as in the source | 1. 80元 | ¥1.80 |
| error | 87 | p86_s10 | Keep the line breaks of the source: it has 0 line break(s), the translation has 4 | 牙刷牙膏毛巾牙刷牙膏 | Toothbrush Toothpaste Towel Toothbrush Toothpaste |
| error | 87 | p86_s15 | Start the translation with the list marker "2." exactly as in the source | 2. 60元 | ¥2.60 |
| error | 87 | p86_s8 | Keep the line breaks of the source: it has 0 line break(s), the translation has 4 | 牙刷牙膏毛巾牙刷牙膏 | Toothbrush Toothpaste Towel Toothbrush Toothpaste |
| error | 87 | p86_s9 | Keep the line breaks of the source: it has 0 line break(s), the translation has 4 | 牙刷牙膏毛巾牙刷牙膏 | Toothbrush Toothpaste Towel Toothbrush Toothpaste |
| error | 89 | p88_s2 | The source ends with a question mark; end the translation with a question mark too | 说一说，你是怎么算的？ | Tell us how you worked it out. |
| error | 89 | p88_s26 | Start the translation with the list marker "7." exactly as in the source | 7. 5元+0.4元 | ¥7.5+0.4 |
| error | 90 | p89_s5 | Start the translation with the list marker "1." exactly as in the source | 1. 6元不到2元12.8元不到13元不会超过15元。 | ¥1.6 is less than ¥2, and ¥12.8 is less than ¥13, so it won… |
| error | 91 | p90_s33 | Start the translation with the list marker "6." exactly as in the source | 6. 50元 | ¥6.50 |
| error | 91 | p90_s34 | Start the translation with the list marker "4." exactly as in the source | 4. 80元 | ¥4.80 |
| error | 92 | p91_s12 | Start the translation with the list marker "1." exactly as in the source | 1. 41米。 | 1.41 m. |
| error | 94 | p93_s22 | Start the translation with the list marker "8." exactly as in the source | 8. 1元 | ¥8.1 |
| error | 94 | p93_s27 | Start the translation with the list marker "4." exactly as in the source | 4. 5元 | ¥4.5 |
| error | 94 | p93_s30 | Start the translation with the list marker "9." exactly as in the source | 9. 9元 | ¥9.9 |
| error | 94 | p93_s31 | Start the translation with the list marker "10." exactly as in the source | 10. 1元 | ¥10.1 |
| error | 95 | p94_s11 | The source ends with a question mark; end the translation with a question mark too | 说一说，这些书的价格分别是几元几角几分？ | Say what each book costs in yuan, jiao and fen. |
| error | 95 | p94_s18 | Start the translation with the list marker "4." exactly as in the source | 4. 70元 | ¥4.70 |
| error | 96 | p95_s4 | Start the translation with the list marker "2." exactly as in the source | 2. 50元 | ¥2.50 |
| error | 99 | p98_s25 | Start the translation with the list marker "1." exactly as in the source | 1. 8元 | ¥1.8 |
| error | 99 | p98_s27 | Start the translation with the list marker "12." exactly as in the source | 12. 1元 | ¥12.1 |
| error | 101 | p100_s8 | Keep the line breaks of the source: it has 0 line break(s), the translation has 3 | 写作业：9:00~9:30义务劳动：10：00~11：00吃午饭：11：30~12:00做游戏：14:00~15:30 | Homework: 9:00~9:30 Volunteer work: 10:00~11:00 Lunch: 11:3… |
| error | 103 | p102_s0 | The source does not end with a question mark; do not end the translation with one | 本学期你学到了什么 | What have you learned this term? |

### `glossary` — 13 errors, 0 warnings

| Severity | Page | Segment | Message | Source | Translation |
|---|---|---|---|---|---|
| error | 20 | p19_s2 | Glossary: translate "个位" as "ones" | 2.右面这两幅图分别是机灵狗在哪个位置看到的？把位置的编号填 | 2. From which position does Clever Dog see each picture on … |
| error | 26 | p25_s14 | Glossary: translate "算一算" as "Calculate" | 1.说一说，再列式算一算 | 1. Discuss, then write a number sentence and solve. |
| error | 27 | p26_s14 | Glossary: translate "算式" as "number sentence" | 6.达·芬奇是文艺复兴时期有名的画家、科学家，留下了许多名画和科学研究成果。你知道他出生于哪一年吗？将下图中得数在40… | 6. Leonardo da Vinci was a famous painter and scientist of … |
| error | 31 | p30_s31 | Glossary: translate "算一算" as "Calculate" | （2）星期一早上出发时里程表的读数是632千米，算一算，赵叔叔星期五晚上到家时里程表的读数是多少？ | (2) When he set off on Monday morning, the odometer read 63… |
| error | 45 | p44_s12 | Glossary: translate "竖式" as "vertical form" | 这些题都能用竖式除法来算吗？该怎样写呢？ | Can all these be worked out with long division? How do we s… |
| error | 48 | p47_s30 | Glossary: translate "算一算" as "Calculate" | （2）算一算李叔叔每天行驶的里程数，哪一天最多？哪一天 | (2) Work out how far Uncle Li drove each day. Which day did… |
| error | 55 | p54_s0 | Glossary: translate "算一算" as "Calculate" | 6.看一看，算一算正方形的边长是多少厘米。 | 6. Look and work out the side length of the square in centi… |
| error | 56 | p55_s12 | Glossary: translate "个位" as "ones" | 十位个位 | T O |
| error | 56 | p55_s12 | Glossary: translate "十位" as "tens" | 十位个位 | T O |
| error | 66 | p65_s6 | Glossary: translate "算一算" as "Calculate" | 算一算，张老师买矿泉水共花多少元？ | Work out how much Teacher Zhang spent on mineral water in a… |
| error | 73 | p72_s5 | Glossary: translate "统计" as "statistics" | 5.统计本班同学在哪个月出生的人数最多，并制作今年这个月的月历 | 5. Find out which month the most classmates were born in, a… |
| error | 80 | p79_s10 | Glossary: translate "连一连" as "Match" | 还可以用字母来表示帽子和裤子。你能试着连一连吗？ | We can also use letters for the hats and trousers. Can you … |
| error | 102 | p101_s1 | Glossary: translate "个位" as "ones" | 1.下面四幅图分别是机灵狗站在哪个位置看到的？在（）里标出 | 1. Where was Clever Dog standing to see each picture below?… |

### `layout_fit` — 88 errors, 46 warnings

| Severity | Page | Segment | Message | Source | Translation |
|---|---|---|---|---|---|
| error | 3 | p2_s11 | Shorten the translation to at most 6 characters so it fits the original box (the current translation of 8 characters overflows its box; the minimum allowed size is 55%) | 笑笑 | Xiaoxiao |
| error | 3 | p2_s11 | Shorten the translation to at most 6 characters so it fits the original box (the current translation of 8 characters overflows its box; the minimum allowed size is 55%) | 笑笑 | Xiaoxiao |
| error | 3 | p2_s19 | Shorten the translation to at most 17 characters so it fits the original box (the current translation of 20 characters overflows its box; the minimum allowed size is 55%) | 科技馆200米 | Science Museum 200 m |
| error | 3 | p2_s19 | Shorten the translation to at most 17 characters so it fits the original box (the current translation of 20 characters overflows its box; the minimum allowed size is 55%) | 科技馆200米 | Science Museum 200 m |
| error | 9 | p8_s0 | Shorten the translation to at most 14 characters so it fits the original box (the current translation of 17 characters overflows its box; the minimum allowed size is 55%) | 买文具 | Buying Stationery |
| error | 9 | p8_s0 | Shorten the translation to at most 14 characters so it fits the original box (the current translation of 17 characters overflows its box; the minimum allowed size is 55%) | 买文具 | Buying Stationery |
| error | 12 | p11_s0 | Shorten the translation to at most 15 characters so it fits the original box (the current translation of 18 characters overflows its box; the minimum allowed size is 55%) | 过河 | Crossing the River |
| error | 12 | p11_s0 | Shorten the translation to at most 15 characters so it fits the original box (the current translation of 18 characters overflows its box; the minimum allowed size is 55%) | 过河 | Crossing the River |
| error | 16 | p15_s7 | Shorten the translation to at most 8 characters so it fits the original box (the current translation of 10 characters overflows its box; the minimum allowed size is 55%) | 20只 | 20 monkeys |
| error | 16 | p15_s7 | Shorten the translation to at most 8 characters so it fits the original box (the current translation of 10 characters overflows its box; the minimum allowed size is 55%) | 20只 | 20 monkeys |
| error | 17 | p16_s14 | Shorten the translation to at most 5 characters so it fits the original box (the current translation of 8 characters overflows its box; the minimum allowed size is 55%) | 笑笑 | Xiaoxiao |
| error | 17 | p16_s14 | Shorten the translation to at most 5 characters so it fits the original box (the current translation of 8 characters overflows its box; the minimum allowed size is 55%) | 笑笑 | Xiaoxiao |
| error | 17 | p16_s16 | Shorten the translation to at most 6 characters so it fits the original box (the current translation of 9 characters overflows its box; the minimum allowed size is 55%) | 妙想 | Miaoxiang |
| error | 17 | p16_s16 | Shorten the translation to at most 6 characters so it fits the original box (the current translation of 9 characters overflows its box; the minimum allowed size is 55%) | 妙想 | Miaoxiang |
| error | 19 | p18_s3 | Shorten the translation to at most 5 characters so it fits the original box (the current translation of 10 characters overflows its box; the minimum allowed size is 55%) | 牙常 | Toothpaste |
| error | 19 | p18_s3 | Shorten the translation to at most 5 characters so it fits the original box (the current translation of 10 characters overflows its box; the minimum allowed size is 55%) | 牙常 | Toothpaste |
| error | 21 | p20_s10 | Shorten the translation to at most 8 characters so it fits the original box (the current translation of 10 characters overflows its box; the minimum allowed size is 55%) | 四(2) | Class 4(2) |
| error | 21 | p20_s10 | Shorten the translation to at most 8 characters so it fits the original box (the current translation of 10 characters overflows its box; the minimum allowed size is 55%) | 四(2) | Class 4(2) |
| error | 21 | p20_s4 | Shorten the translation to at most 6 characters so it fits the original box (the current translation of 7 characters overflows its box; the minimum allowed size is 55%) | 一 班班站 | Class 1 |
| error | 21 | p20_s4 | Shorten the translation to at most 6 characters so it fits the original box (the current translation of 7 characters overflows its box; the minimum allowed size is 55%) | 一 班班站 | Class 1 |
| error | 23 | p22_s0 | Shorten the translation to at most 14 characters so it fits the original box (the current translation of 17 characters overflows its box; the minimum allowed size is 55%) | 运白菜 | Shipping Cabbages |
| error | 23 | p22_s0 | Shorten the translation to at most 14 characters so it fits the original box (the current translation of 17 characters overflows its box; the minimum allowed size is 55%) | 运白菜 | Shipping Cabbages |
| error | 25 | p24_s4 | Shorten the translation to at most 8 characters so it fits the original box (the current translation of 10 characters overflows its box; the minimum allowed size is 55%) | 亮亮 | Liangliang |
| error | 25 | p24_s4 | Shorten the translation to at most 8 characters so it fits the original box (the current translation of 10 characters overflows its box; the minimum allowed size is 55%) | 亮亮 | Liangliang |
| error | 28 | p27_s18 | Shorten the translation to at most 9 characters so it fits the original box (the current translation of 12 characters overflows its box; the minimum allowed size is 55%) | 石家庄 | Shijiazhuang |
| error | 28 | p27_s18 | Shorten the translation to at most 9 characters so it fits the original box (the current translation of 12 characters overflows its box; the minimum allowed size is 55%) | 石家庄 | Shijiazhuang |
| error | 29 | p28_s23 | Shorten the translation to at most 9 characters so it fits the original box (the current translation of 11 characters overflows its box; the minimum allowed size is 55%) | 邮局 | Post office |
| error | 29 | p28_s23 | Shorten the translation to at most 9 characters so it fits the original box (the current translation of 11 characters overflows its box; the minimum allowed size is 55%) | 邮局 | Post office |
| error | 31 | p30_s26 | Shorten the translation to at most 7 characters so it fits the original box (the current translation of 9 characters overflows its box; the minimum allowed size is 55%) | 星期三 | Wednesday |
| error | 31 | p30_s26 | Shorten the translation to at most 7 characters so it fits the original box (the current translation of 9 characters overflows its box; the minimum allowed size is 55%) | 星期三 | Wednesday |
| error | 38 | p37_s0 | Shorten the translation to at most 10 characters so it fits the original box (the current translation of 12 characters overflows its box; the minimum allowed size is 55%) | 丰收了 | Harvest Time |
| error | 38 | p37_s0 | Shorten the translation to at most 10 characters so it fits the original box (the current translation of 12 characters overflows its box; the minimum allowed size is 55%) | 丰收了 | Harvest Time |
| error | 40 | p39_s0 | Shorten the translation to at most 12 characters so it fits the original box (the current translation of 14 characters overflows its box; the minimum allowed size is 55%) | 植树 | Planting Trees |
| error | 40 | p39_s0 | Shorten the translation to at most 12 characters so it fits the original box (the current translation of 14 characters overflows its box; the minimum allowed size is 55%) | 植树 | Planting Trees |
| error | 51 | p50_s13 | Shorten the translation to at most 5 characters so it fits the original box (the current translation of 7 characters overflows its box; the minimum allowed size is 55%) | 测量 | Measure |
| error | 51 | p50_s13 | Shorten the translation to at most 5 characters so it fits the original box (the current translation of 7 characters overflows its box; the minimum allowed size is 55%) | 测量 | Measure |
| error | 54 | p53_s20 | Shorten the translation to at most 10 characters so it fits the original box (the current translation of 12 characters overflows its box; the minimum allowed size is 55%) | 长宽 | Length Width |
| error | 54 | p53_s20 | Shorten the translation to at most 10 characters so it fits the original box (the current translation of 12 characters overflows its box; the minimum allowed size is 55%) | 长宽 | Length Width |
| error | 54 | p53_s27 | Shorten the translation to at most 5 characters so it fits the original box (the current translation of 9 characters overflows its box; the minimum allowed size is 55%) | 周长 | Perimeter |
| error | 54 | p53_s27 | Shorten the translation to at most 5 characters so it fits the original box (the current translation of 9 characters overflows its box; the minimum allowed size is 55%) | 周长 | Perimeter |
| error | 58 | p57_s0 | Shorten the translation to at most 18 characters so it fits the original box (the current translation of 21 characters overflows its box; the minimum allowed size is 55%) | 去游乐园 | To the Amusement Park |
| error | 58 | p57_s0 | Shorten the translation to at most 18 characters so it fits the original box (the current translation of 21 characters overflows its box; the minimum allowed size is 55%) | 去游乐园 | To the Amusement Park |
| error | 61 | p60_s25 | Shorten the translation to at most 13 characters so it fits the original box (the current translation of 15 characters overflows its box; the minimum allowed size is 55%) | 海洋馆龙 | Aquarium Dragon |
| error | 61 | p60_s25 | Shorten the translation to at most 13 characters so it fits the original box (the current translation of 15 characters overflows its box; the minimum allowed size is 55%) | 海洋馆龙 | Aquarium Dragon |
| error | 62 | p61_s20 | Shorten the translation to at most 9 characters so it fits the original box (the current translation of 11 characters overflows its box; the minimum allowed size is 55%) | 新站 | New Station |
| error | 62 | p61_s20 | Shorten the translation to at most 9 characters so it fits the original box (the current translation of 11 characters overflows its box; the minimum allowed size is 55%) | 新站 | New Station |
| error | 62 | p61_s6 | Shorten the translation to at most 9 characters so it fits the original box (the current translation of 11 characters overflows its box; the minimum allowed size is 55%) | 新站 | New Station |
| error | 62 | p61_s6 | Shorten the translation to at most 9 characters so it fits the original box (the current translation of 11 characters overflows its box; the minimum allowed size is 55%) | 新站 | New Station |
| error | 63 | p62_s4 | Shorten the translation to at most 6 characters so it fits the original box (the current translation of 8 characters overflows its box; the minimum allowed size is 55%) | 新城 | New Town |
| error | 63 | p62_s4 | Shorten the translation to at most 6 characters so it fits the original box (the current translation of 8 characters overflows its box; the minimum allowed size is 55%) | 新城 | New Town |
| error | 63 | p62_s5 | Shorten the translation to at most 6 characters so it fits the original box (the current translation of 8 characters overflows its box; the minimum allowed size is 55%) | 古城 | Old Town |
| error | 63 | p62_s5 | Shorten the translation to at most 6 characters so it fits the original box (the current translation of 8 characters overflows its box; the minimum allowed size is 55%) | 古城 | Old Town |
| error | 66 | p65_s3 | Shorten the translation to at most 8 characters so it fits the original box (the current translation of 10 characters overflows its box; the minimum allowed size is 55%) | 24瓶 | 24 bottles |
| error | 66 | p65_s3 | Shorten the translation to at most 8 characters so it fits the original box (the current translation of 10 characters overflows its box; the minimum allowed size is 55%) | 24瓶 | 24 bottles |
| error | 70 | p69_s3 | Shorten the translation to at most 26 characters so it fits the original box (the current translation of 33 characters overflows its box; the minimum allowed size is 55%) | D2031北京西一郑州东 | D2031 Beijing West–Zhengzhou East |
| error | 70 | p69_s3 | Shorten the translation to at most 26 characters so it fits the original box (the current translation of 33 characters overflows its box; the minimum allowed size is 55%) | D2031北京西一郑州东 | D2031 Beijing West–Zhengzhou East |
| error | 70 | p69_s6 | Shorten the translation to at most 17 characters so it fits the original box (the current translation of 20 characters overflows its box; the minimum allowed size is 55%) | 单元二单元三单元 | Unit 1 Unit 2 Unit 3 |
| error | 70 | p69_s6 | Shorten the translation to at most 17 characters so it fits the original box (the current translation of 20 characters overflows its box; the minimum allowed size is 55%) | 单元二单元三单元 | Unit 1 Unit 2 Unit 3 |
| error | 73 | p72_s12 | Shorten the translation to at most 6 characters so it fits the original box (the current translation of 7 characters overflows its box; the minimum allowed size is 55%) | ）月 | ) month |
| error | 73 | p72_s12 | Shorten the translation to at most 6 characters so it fits the original box (the current translation of 7 characters overflows its box; the minimum allowed size is 55%) | ）月 | ) month |
| error | 81 | p80_s9 | Shorten the translation to at most 10 characters so it fits the original box (the current translation of 12 characters overflows its box; the minimum allowed size is 55%) | 少年宫 | Youth Palace |
| error | 81 | p80_s9 | Shorten the translation to at most 10 characters so it fits the original box (the current translation of 12 characters overflows its box; the minimum allowed size is 55%) | 少年宫 | Youth Palace |
| error | 83 | p82_s23 | Shorten the translation to at most 10 characters so it fits the original box (the current translation of 12 characters overflows its box; the minimum allowed size is 55%) | 你知道吗 | Did you know |
| error | 83 | p82_s23 | Shorten the translation to at most 10 characters so it fits the original box (the current translation of 12 characters overflows its box; the minimum allowed size is 55%) | 你知道吗 | Did you know |
| error | 84 | p83_s15 | Shorten the translation to at most 6 characters so it fits the original box (the current translation of 8 characters overflows its box; the minimum allowed size is 55%) | 分 | ____ fen |
| error | 84 | p83_s15 | Shorten the translation to at most 6 characters so it fits the original box (the current translation of 8 characters overflows its box; the minimum allowed size is 55%) | 分 | ____ fen |
| error | 85 | p84_s10 | Shorten the translation to at most 12 characters so it fits the original box (the current translation of 15 characters overflows its box; the minimum allowed size is 55%) | 方便面 | instant noodles |
| error | 85 | p84_s10 | Shorten the translation to at most 12 characters so it fits the original box (the current translation of 15 characters overflows its box; the minimum allowed size is 55%) | 方便面 | instant noodles |
| error | 85 | p84_s11 | Shorten the translation to at most 11 characters so it fits the original box (the current translation of 13 characters overflows its box; the minimum allowed size is 55%) | 矿泉水 | mineral water |
| error | 85 | p84_s11 | Shorten the translation to at most 11 characters so it fits the original box (the current translation of 13 characters overflows its box; the minimum allowed size is 55%) | 矿泉水 | mineral water |
| error | 88 | p87_s9 | Shorten the translation to at most 12 characters so it fits the original box (the current translation of 14 characters overflows its box; the minimum allowed size is 55%) | 元角 | yuan ____ jiao |
| error | 88 | p87_s9 | Shorten the translation to at most 12 characters so it fits the original box (the current translation of 14 characters overflows its box; the minimum allowed size is 55%) | 元角 | yuan ____ jiao |
| error | 90 | p89_s0 | Shorten the translation to at most 11 characters so it fits the original box (the current translation of 13 characters overflows its box; the minimum allowed size is 55%) | 寄书 | Posting Books |
| error | 90 | p89_s0 | Shorten the translation to at most 11 characters so it fits the original box (the current translation of 13 characters overflows its box; the minimum allowed size is 55%) | 寄书 | Posting Books |
| error | 91 | p90_s1 | Shorten the translation to at most 15 characters so it fits the original box (the current translation of 18 characters overflows its box; the minimum allowed size is 55%) | 儿童故事 | Children's Stories |
| error | 91 | p90_s1 | Shorten the translation to at most 15 characters so it fits the original box (the current translation of 18 characters overflows its box; the minimum allowed size is 55%) | 儿童故事 | Children's Stories |
| error | 91 | p90_s28 | Shorten the translation to at most 10 characters so it fits the original box (the current translation of 15 characters overflows its box; the minimum allowed size is 55%) | 瓜子 | Sunflower seeds |
| error | 91 | p90_s28 | Shorten the translation to at most 10 characters so it fits the original box (the current translation of 15 characters overflows its box; the minimum allowed size is 55%) | 瓜子 | Sunflower seeds |
| error | 94 | p93_s33 | Shorten the translation to at most 42 characters so it fits the original box (the current translation of 86 characters overflows its box; the minimum allowed size is 55%) | 一说。 | What are the prices of these three items in yuan, jiao and … |
| error | 94 | p93_s33 | Shorten the translation to at most 42 characters so it fits the original box (the current translation of 86 characters overflows its box; the minimum allowed size is 55%) | 一说。 | What are the prices of these three items in yuan, jiao and … |
| error | 95 | p94_s20 | Shorten the translation to at most 6 characters so it fits the original box (the current translation of 7 characters overflows its box; the minimum allowed size is 55%) | 1月 | Month 1 |
| error | 95 | p94_s20 | Shorten the translation to at most 6 characters so it fits the original box (the current translation of 7 characters overflows its box; the minimum allowed size is 55%) | 1月 | Month 1 |
| error | 100 | p99_s5 | Shorten the translation to at most 8 characters so it fits the original box (the current translation of 10 characters overflows its box; the minimum allowed size is 55%) | 147人 | 147 people |
| error | 100 | p99_s5 | Shorten the translation to at most 8 characters so it fits the original box (the current translation of 10 characters overflows its box; the minimum allowed size is 55%) | 147人 | 147 people |
| error | 101 | p100_s14 | Shorten the translation to at most 12 characters so it fits the original box (the current translation of 14 characters overflows its box; the minimum allowed size is 55%) | 化京帅 | Hua Jing Shuai |
| error | 101 | p100_s14 | Shorten the translation to at most 12 characters so it fits the original box (the current translation of 14 characters overflows its box; the minimum allowed size is 55%) | 化京帅 | Hua Jing Shuai |
| error | 109 | p108_s0 | Shorten the translation to at most 5 characters so it fits the original box (the current translation of 8 characters overflows its box; the minimum allowed size is 55%) | 附页 | Appendix |
| error | 109 | p108_s0 | Shorten the translation to at most 5 characters so it fits the original box (the current translation of 8 characters overflows its box; the minimum allowed size is 55%) | 附页 | Appendix |
| warning | 3 | p2_s20 | The translation overflows its box and was rendered at 20% of the original size; even a much shorter text would not fit, check this box in the preview | 200米 | 200m |
| warning | 3 | p2_s20 | The translation overflows its box and was rendered at 20% of the original size; even a much shorter text would not fit, check this box in the preview | 200米 | 200m |
| warning | 3 | p2_s22 | The translation overflows its box and was rendered at 32% of the original size; even a much shorter text would not fit, check this box in the preview | 学校 | School |
| warning | 3 | p2_s22 | The translation overflows its box and was rendered at 32% of the original size; even a much shorter text would not fit, check this box in the preview | 学校 | School |
| warning | 3 | p2_s23 | The translation overflows its box and was rendered at 17% of the original size; even a much shorter text would not fit, check this box in the preview | 150米 | 150m |
| warning | 3 | p2_s23 | The translation overflows its box and was rendered at 17% of the original size; even a much shorter text would not fit, check this box in the preview | 150米 | 150m |
| warning | 9 | p8_s16 | The translation overflows its box and was rendered at 53% of the original size; even a much shorter text would not fit, check this box in the preview | 作 | essay |
| warning | 9 | p8_s16 | The translation overflows its box and was rendered at 53% of the original size; even a much shorter text would not fit, check this box in the preview | 作 | essay |
| warning | 9 | p8_s23 | The translation overflows its box and was rendered at 51% of the original size; even a much shorter text would not fit, check this box in the preview | 元） | yuan) |
| warning | 9 | p8_s23 | The translation overflows its box and was rendered at 51% of the original size; even a much shorter text would not fit, check this box in the preview | 元） | yuan) |
| warning | 11 | p10_s2 | The translation overflows its box and was rendered at 39% of the original size; even a much shorter text would not fit, check this box in the preview | 绿 | Green |
| warning | 11 | p10_s2 | The translation overflows its box and was rendered at 39% of the original size; even a much shorter text would not fit, check this box in the preview | 绿 | Green |
| warning | 21 | p20_s11 | The translation overflows its box and was rendered at 41% of the original size; even a much shorter text would not fit, check this box in the preview | 班 | Class 1 |
| warning | 21 | p20_s11 | The translation overflows its box and was rendered at 41% of the original size; even a much shorter text would not fit, check this box in the preview | 班 | Class 1 |
| warning | 27 | p26_s10 | The translation overflows its box and was rendered at 30% of the original size; even a much shorter text would not fit, check this box in the preview | 票 | tickets |
| warning | 27 | p26_s10 | The translation overflows its box and was rendered at 30% of the original size; even a much shorter text would not fit, check this box in the preview | 票 | tickets |
| warning | 34 | p33_s9 | The translation overflows its box and was rendered at 37% of the original size; even a much shorter text would not fit, check this box in the preview | 答： | Answer: |
| warning | 34 | p33_s9 | The translation overflows its box and was rendered at 37% of the original size; even a much shorter text would not fit, check this box in the preview | 答： | Answer: |
| warning | 43 | p42_s12 | The translation overflows its box and was rendered at 41% of the original size; even a much shorter text would not fit, check this box in the preview | 小东 | Xiaodong |
| warning | 43 | p42_s12 | The translation overflows its box and was rendered at 41% of the original size; even a much shorter text would not fit, check this box in the preview | 小东 | Xiaodong |
| warning | 48 | p47_s13 | The translation overflows its box and was rendered at 36% of the original size; even a much shorter text would not fit, check this box in the preview | 郑州 | Zhengzhou |
| warning | 48 | p47_s13 | The translation overflows its box and was rendered at 36% of the original size; even a much shorter text would not fit, check this box in the preview | 郑州 | Zhengzhou |
| warning | 50 | p49_s10 | The translation overflows its box and was rendered at 33% of the original size; even a much shorter text would not fit, check this box in the preview | 110米 | 110 m |
| warning | 50 | p49_s10 | The translation overflows its box and was rendered at 33% of the original size; even a much shorter text would not fit, check this box in the preview | 110米 | 110 m |
| warning | 50 | p49_s11 | The translation overflows its box and was rendered at 50% of the original size; even a much shorter text would not fit, check this box in the preview | 90米 | 90 m |
| warning | 50 | p49_s11 | The translation overflows its box and was rendered at 50% of the original size; even a much shorter text would not fit, check this box in the preview | 90米 | 90 m |
| warning | 50 | p49_s12 | The translation overflows its box and was rendered at 43% of the original size; even a much shorter text would not fit, check this box in the preview | 75米 | 75 m |
| warning | 50 | p49_s12 | The translation overflows its box and was rendered at 43% of the original size; even a much shorter text would not fit, check this box in the preview | 75米 | 75 m |
| warning | 50 | p49_s13 | The translation overflows its box and was rendered at 55% of the original size; even a much shorter text would not fit, check this box in the preview | 75米 | 75 m |
| warning | 50 | p49_s13 | The translation overflows its box and was rendered at 55% of the original size; even a much shorter text would not fit, check this box in the preview | 75米 | 75 m |
| warning | 51 | p50_s12 | The translation overflows its box and was rendered at 46% of the original size; even a much shorter text would not fit, check this box in the preview | 估计 | Estimate |
| warning | 51 | p50_s12 | The translation overflows its box and was rendered at 46% of the original size; even a much shorter text would not fit, check this box in the preview | 估计 | Estimate |
| warning | 51 | p50_s5 | The translation overflows its box and was rendered at 49% of the original size; even a much shorter text would not fit, check this box in the preview | 18米 | 18 m |
| warning | 51 | p50_s5 | The translation overflows its box and was rendered at 49% of the original size; even a much shorter text would not fit, check this box in the preview | 18米 | 18 m |
| warning | 53 | p52_s7 | The translation overflows its box and was rendered at 38% of the original size; even a much shorter text would not fit, check this box in the preview | 32米 | 32 m |
| warning | 53 | p52_s7 | The translation overflows its box and was rendered at 38% of the original size; even a much shorter text would not fit, check this box in the preview | 32米 | 32 m |
| warning | 62 | p61_s28 | The translation overflows its box and was rendered at 42% of the original size; even a much shorter text would not fit, check this box in the preview | 答： | Answer: |
| warning | 62 | p61_s28 | The translation overflows its box and was rendered at 42% of the original size; even a much shorter text would not fit, check this box in the preview | 答： | Answer: |
| warning | 84 | p83_s10 | The translation overflows its box and was rendered at 53% of the original size; even a much shorter text would not fit, check this box in the preview | 元 | yuan |
| warning | 84 | p83_s10 | The translation overflows its box and was rendered at 53% of the original size; even a much shorter text would not fit, check this box in the preview | 元 | yuan |
| warning | 84 | p83_s13 | The translation overflows its box and was rendered at 54% of the original size; even a much shorter text would not fit, check this box in the preview | 元 | yuan |
| warning | 84 | p83_s13 | The translation overflows its box and was rendered at 54% of the original size; even a much shorter text would not fit, check this box in the preview | 元 | yuan |
| warning | 84 | p83_s18 | The translation overflows its box and was rendered at 42% of the original size; even a much shorter text would not fit, check this box in the preview | 元 | yuan |
| warning | 84 | p83_s18 | The translation overflows its box and was rendered at 42% of the original size; even a much shorter text would not fit, check this box in the preview | 元 | yuan |
| warning | 90 | p89_s29 | The translation overflows its box and was rendered at 42% of the original size; even a much shorter text would not fit, check this box in the preview | 角 | jiao |
| warning | 90 | p89_s29 | The translation overflows its box and was rendered at 42% of the original size; even a much shorter text would not fit, check this box in the preview | 角 | jiao |

### `llm_review` — 49 errors, 106 warnings

| Severity | Page | Segment | Message | Source | Translation |
|---|---|---|---|---|---|
| error | 1 | p0_s5 | Reviewer (terminology): "Volume 1" is acceptable, but textbook convention is "First Volume" for 上册. | 上册 | Volume 1 |
| error | 1 | p0_s6 | Reviewer (untranslated): The source 北京师范大学出 is truncated; the English "Beijing Normal University Press" adds the missing part but is otherwise fine. | 北京师范大学出 | Beijing Normal University Press |
| error | 3 | p2_s15 | Reviewer (meaning): The source label 北U (North/Beijing U) was changed to NU, altering the label's meaning. | 北U | NU |
| error | 8 | p7_s2 | Reviewer (terminology): "儿童票" is "children's ticket"; "child tickets" is acceptable but "children's tickets" is more natural. Suggested translation: "(1) Taoqi has ¥50. How much change should he get after buying 8 children's tickets?" | （1）淘气有50元，买8张儿童票应找回多少元？ | (1) Taoqi has ¥50. How much change should he get after buyi… |
| error | 21 | p20_s4 | Reviewer (omission): The source 一 班班站 contains more than 'Class 1'; the trailing fragment is dropped. Suggested translation: "Class 1" | 一 班班站 | Class 1 |
| error | 28 | p27_s1 | Reviewer (meaning): '里程表' means 'mileage table', not 'odometer table'. The table shows distances/mileage, so 'odometer table' is a mistranslation. Suggested translation: "Below is the mileage table of the major stations along the "Beijing–Xi'an" line." | 下面是“北京一西安”沿线各大站的火车里程表。 | Below is the train odometer table of the major stations alo… |
| error | 28 | p27_s13 | Reviewer (number): Source says '1464米' but translation says '1464 km'; the unit differs from the source. Suggested translation: "1464 km" | 1464米 | 1464 km |
| error | 28 | p27_s26 | Reviewer (number): The source says 8134米 (metres), but the context (adjacent labels 813千米, 689千米) and the number 8134 suggest the intended label is 813 km; regardless, the translation must match the source exactly: 8134 m, not 813 km. The translation states 8134 m which is correct; no finding. | 8134米 | 8134 m |
| error | 29 | p28_s4 | Reviewer (terminology): 航程 means "voyage distance/sailing distance"; "Distance/km" loses the nautical sense but is acceptable as a table header. However the same unit label 路程/米 on p28_s26 is "Distance/m". Using different words for different Chinese terms is fine; no finding. | 航程/千米 | Distance/km |
| error | 35 | p34_s2 | Reviewer (omission): The Chinese "40个" includes the measure word naming the counted items (fruits), but the translation drops the noun, unlike the parallel item "20 fruits". Suggested translation: "40 fruits" | 40个 | 40 |
| error | 35 | p34_s20 | Reviewer (untranslated): The source "茶茶茶茶" is four tea characters standing for cups of tea; the translation leaves the Chinese character 茶 untranslated and just repeats the English word without the picture context. Suggested translation: "tea tea tea tea" | 茶茶茶茶 | tea tea tea tea |
| error | 38 | p37_s1 | Reviewer (meaning): The measure word '根' (carrots) is dropped. The source labels a quantity of carrots as '60 根'; the translation should be 'Exactly 60 carrots' rather than 'Exactly 60'. Suggested translation: "Exactly 60 carrots" | 正好60根 | Exactly 60 |
| error | 38 | p37_s2 | Reviewer (meaning): 'on average' is slightly misleading for '平均' here; the intended meaning is 'evenly/fairly' (each rabbit gets the same number). 'How many carrots does each rabbit get?' is natural and accurate. Suggested translation: "How many carrots does each rabbit get?" | 平均每只小兔能得到多少根胡萝卜？ | How many carrots does each rabbit get on average? |
| error | 40 | p39_s6 | Reviewer (omission): The source "每班分到12棵" is about each class getting 12 saplings, but the translation says "each class gets 12 saplings" — this is actually correct. Wait, re-check: source says 先分3捆，再分剩下的6棵，每班分到12棵。 The translation is fine. No finding. | 先分3捆，再分剩下的6棵，每班分到12棵。 | First share out 3 bundles, then share out the remaining 6 s… |
| error | 51 | p50_s10 | Reviewer (meaning): The source continuation "长是多少。" means "...how long the perimeter is"; the translation "of the figures you make" adds "you make" and changes the meaning. Suggested translation: "How long is the perimeter?" | 长是多少。 | of the figures you make. |
| error | 51 | p50_s9 | Reviewer (number): The sentence is cut mid-word in the source ("图形周") and the translation supplies an extra "of the figures", duplicating the continuation in p50_s10; the fragment must not be completed with words not present. Suggested translation: "5. Use 4 small squares with a side length of 1 cm to make 3 figures of different shapes, and tell the perimeter of the figures" | 5.用4个边长是1厘米的小正方形拼出3种不同形状的图形，说说拼成的图形周 | 5. Use 4 small squares with a side length of 1 cm to make 3… |
| error | 52 | p51_s8 | Reviewer (number): Source "3×4=12（厘米）"; translation keeps numbers, but the sentence "All 4 sides are 3 cm" is fine. No numeric problem. (Re-reported only if the 3 cm is wrong.) | 4条边都是3厘米，边长乘4就可以了。3×4=12（厘米） | All 4 sides are 3 cm, so just multiply the side length by 4… |
| error | 53 | p52_s2 | Reviewer (terminology): Unit word "metres" (British) vs "meters" used in p50_s0 and labels "m" — inconsistent spelling. Suggested translation: "What is the perimeter of the basketball court in meters?" | 篮球场的周长是多少米？ | What is the perimeter of the basketball court in metres? |
| error | 60 | p59_s14 | Reviewer (terminology): "hard-seat cars" is an awkward rendering of 硬座车厢; "hard-seat carriages" or "hard-seat coaches" reads more naturally in a textbook. Suggested translation: "How many people can 7 hard-seat carriages carry? Calculate and fill in." | 7节硬座车厢可乘多少人？算一算，填一填。 | How many people can 7 hard-seat cars carry? Calculate and f… |
| error | 61 | p60_s33 | Reviewer (meaning): The translation reverses the source sentence structure and breaks it into a question; the source completes the previous sentence: "tickets in total need how much money?". Suggested translation: "tickets in total, how much money do they need?" | 票共需要多少元？ | tickets in total, how much do they need? |
| error | 61 | p60_s4 | Reviewer (omission): The measure word 个 is dropped; in this context it names mushrooms, and other items of the same label write "46 mushrooms". Suggested translation: "46 mushrooms" | 46个 | 46 |
| error | 63 | p62_s7 | Reviewer (omission): The place-name label '光明镇' means 'Guangming Town'; the word 'Town' is missing. Suggested translation: "Guangming Town" | 光明镇 | Guangming |
| error | 66 | p65_s5 | Reviewer (meaning): The source runs the two statements together ("24×2比50小" followed by "50×3=150"); the translation inserts "and" between them, which is fine, but the source's "24×2比50小" should not be linked as if it were part of the same thought. More importantly, the amount should use the currency symbol, not the word "yuan". Suggested translation: "24×2 is less than 50; 50×3=150, so ¥150 is enough." | 24×2比50小50×3=150，150元够了 | 24×2 is less than 50, and 50×3=150, so ¥150 is enough |
| error | 73 | p72_s18 | Reviewer (meaning): "谁最大" here means who is the oldest (whose birthday comes earliest), not who is the largest; 比一比 asks to compare the birthdays. Suggested translation: "(3) Mark the birthdays of classmates born in this month on it, and compare: who is the oldest," | （3）把在这个月出生的同学的生日标在上面，比一比，谁最大， | (3) Mark the birthdays of classmates born in this month on … |
| error | 73 | p72_s2 | Reviewer (terminology): 说一说 is a discussion prompt; "Discuss." is fine, but for consistency with textbook glossary style the standard rendering is "Talk about it." (no glossary pair exists for 说一说, so either is acceptable; keep consistent). Suggested translation: "4. Talk about it." | 4.说一说。 | 4. Discuss. |
| error | 73 | p72_s21 | Reviewer (meaning): “猜生日” means “Guess the birthday” in the sense of guessing when it is, not which event; “Guess the birthday” is slightly off, better “Guess the birthday(s)” or “Guess when the birthday is.” Suggested translation: "6. Guess the birthday." | 6.猜生日。 | 6. Guess the birthday. |
| error | 74 | p73_s1 | Reviewer (meaning): “直目” is not a standard term and the translation “Straight eye” is likely a mistranslation; this may be a typo for a different phrase, but without context, it is questionable. | 直目 | Straight eye |
| error | 74 | p73_s10 | Reviewer (number): The translation inserts an answer blank “___” and “p.m.” that are not in the source; the source reads “15时就是下午” and should not add a blank. Suggested translation: "15:00 is in the afternoon" | 15时就是下午 | 15:00 is ___ p.m. |
| error | 76 | p75_s14 | Reviewer (untranslated): The vertical label 课第第午 is garbled in the source (likely '下午课' etc.); the translation 'Morning Periods' invents meaning not present and mixes morning/afternoon, misleading students. Suggested translation: "Afternoon Periods" | 课第第午 | Morning Periods |
| error | 76 | p75_s17 | Reviewer (untranslated): The vertical label 第第午 is garbled; 'Morning' does not correspond to the source characters and would mislead. Suggested translation: "Afternoon" | 第第午 | Morning |
| error | 79 | p78_s12 | Reviewer (terminology): 想一想 is a recurring instructional label; the glossary does not fix a term, but 'Think' is acceptable; other items use 'Think' consistently. No change needed. | 想一想 | Think |
| error | 83 | p82_s15 | Reviewer (omission): "再" (again) is omitted; the instruction is to try another group again. Suggested translation: "Try another group again." | 换另一组再试试。 | Try another group. |
| error | 84 | p83_s1 | Reviewer (terminology): "Stationery" drops the noun "store"; the heading is the name "Stationery Store". Suggested translation: "Stationery Store" | 文具店 | Stationery |
| error | 84 | p83_s49 | Reviewer (meaning): The source reads "元8角1分" (1 yuan, 8 jiao, 1 fen); the translation renders "yuan 8 jiao 1 ... fen" leaving the leading "1" as a stray number before fen. Suggested translation: "¥1.81" | 元8角1332.56.0分 | yuan 8 jiao 1 332.56.0 fen |
| error | 85 | p84_s22 | Reviewer (meaning): 伍角 means 'five jiao' (¥0.5), but the translation gives ¥0.5 with no indication of the jiao unit; it should name the amount in jiao. Suggested translation: "5 jiao" | 伍角 | ¥0.5 |
| error | 85 | p84_s24 | Reviewer (number): 7.15元 is 7 yuan and 15 fen, not '7 yuan 15 jiao'; the second part is misread. Suggested translation: "¥7.15 is 7 yuan 15 fen." | 7.15元是7元15角。 | ¥7.15 is 7 yuan 15 jiao. |
| error | 85 | p84_s25 | Reviewer (number): The source amount 3元2分 is written as '3 yuan 2 fen'; the translation drops '3'. Suggested translation: "3 yuan 2 fen is" | 3元2分就是 | 3 yuan 2 fen is |
| error | 85 | p84_s27 | Reviewer (number): The source amount 4角5分 is written as '4 jiao 5 fen'; the translation drops '4'. Suggested translation: "4 jiao 5 fen is" | 4角5分就是 | 4 jiao 5 fen is |
| error | 86 | p85_s22 | Reviewer (meaning): The source says 4.9元 is '4 yuan and more' and 5.1元 is '5 yuan and more'; the translation adds 'a little' and changes the comparison. Suggested translation: "¥4.9 is more than ¥4, ¥5.1 is more than ¥5. 4 is smaller than 5, so ¥4.9 is cheaper." | 4.9元是4元多，5.1元是5元多。4比5小，所以4.9元便宜。 | ¥4.9 is a little more than ¥4, ¥5.1 is a little more than ¥… |
| error | 87 | p86_s16 | Reviewer (number): No issue; ¥2.40 matches the source. | 2.40元 | ¥2.40 |
| error | 87 | p86_s31 | Reviewer (number): ¥0.8 matches the source amount; fine. | 0.8元 | ¥0.8 |
| error | 88 | p87_s13 | Reviewer (omission): The source heading is "答：业" (Answer: Ye / likely "Answer:" plus a stray character); the translation drops the character, but if it is part of the answer label it should be preserved. The heading "Answer:" alone may lose content. Suggested translation: "Answer: 业" | 答：业 | Answer: |
| error | 90 | p89_s26 | Reviewer (number): Stray minus sign and duplicated equals signs: '10 jiao − -4 jiao = =6 jiao' instead of '10 jiao − 4 jiao = 6 jiao'. Suggested translation: "10 jiao − 4 jiao = 6 jiao" | 10角-4角=6角 | 10 jiao − -4 jiao = =6 jiao |
| error | 91 | p90_s2 | Reviewer (meaning): 'Animals' is a loose rendering of 动物世界 ('Animal World'); the book title loses its sense but does not mislead. Suggested translation: "Animal World" | 动物世界 | Animals |
| error | 92 | p91_s16 | Reviewer (terminology): 1角 rendered as 'jiao' rather than the money convention; but as a unit fraction example, consistency is needed. Suggested translation: "1 jiao is 0.1 yuan. 1 dm is 0.1 m." | 1角是0.1元。1分米是0.1米。 | 1 jiao is 0.1 yuan. 1 dm is 0.1 m. |
| error | 100 | p99_s11 | Reviewer (number): The source starts with the enumerator (1), which the translation keeps, but the item is also placed under the 'label' context; no issue. Actually the enumerator is preserved—no finding. | （1）一瓶墨水多少元？ | (1) How much is a bottle of ink? |
| error | 100 | p99_s23 | Reviewer (untranslated): The placeholder ⟦0⟧ from the source is missing; the source contains '无锡⟦0⟧上海' where ⟦0⟧ stands for a figure/blank, but the translation keeps the raw numbers '396.38.0' without the placeholder. Suggested translation: "Wuxi ⟦0⟧ Shanghai" | 无锡396.38.0上海 | Wuxi 396.38.0 Shanghai |
| error | 101 | p100_s14 | Reviewer (untranslated): The source '化京帅' is garbled/OCR text, but the translation 'Hua Jing Shuai' invents a name not present; it should be left as the source proper name or handled as OCR garbage. This is a proper name, so pinyin is acceptable, but the characters do not correspond. No reliable fix. | 化京帅 | Hua Jing Shuai |
| error | 109 | p108_s15 | Reviewer (meaning): "川11" is a scan artifact/misread, not the province name Sichuan plus the number 11; it should be treated as a fragment of the calendar grid (likely part of a month/weekday label), not translated as "Sichuan". Suggested translation: "11" | 川11 | Sichuan 11 |
| warning | 6 | p5_s21 | Reviewer (format): Money must be written with the currency symbol; the answer blank unit should read (¥). Suggested translation: "3×4=12 (¥)" | 3x4=12（元） | 3x4=12 (yuan) |
| warning | 6 | p5_s23 | Reviewer (format): Money must be written with the currency symbol; the answer blank unit should read (¥). Suggested translation: "12+6=18 (¥)" | 12+6=18（元） | 12+6=18 (yuan) |
| warning | 7 | p6_s10 | Reviewer (format): Money must be written with the currency symbol; the answer blank unit should read (¥). Suggested translation: "20−12=8 (¥)" | 20-12=8（元） | 20-12=8 (yuan) |
| warning | 7 | p6_s17 | Reviewer (grammar): "说一说" here means to explain in words, not necessarily to discuss. Suggested translation: "1. Explain in words, then write a number sentence and calculate." | 1.说一说，再列式算一算。 | 1. Discuss, then write a number sentence and calculate. |
| warning | 7 | p6_s9 | Reviewer (format): Money must be written with the currency symbol; the answer blank unit should read (¥). Suggested translation: "3×4=12 (¥)" | 3×4=12（元） | 3×4=12 (yuan) |
| warning | 9 | p8_s27 | Reviewer (format): The answer blank unit （元） should follow the bare-unit convention: 'yuan' without the currency symbol is correct, but the parentheses are kept; fine. | 10÷5=2（元） | 10÷5=2 (yuan) |
| warning | 11 | p10_s28 | Reviewer (format): Currency must be written with the symbol before the number: 20元 => ¥20. Suggested translation: "Landscape pictures ¥20 per set" | 风景图片每套20元 | Landscape pictures 20 yuan per set |
| warning | 11 | p10_s29 | Reviewer (format): Currency must be written with the symbol before the number: 2元 => ¥2. Suggested translation: "Flower pictures ¥2 each" | 鲜花图片每张2元 | Flower pictures 2 yuan each |
| warning | 11 | p10_s30 | Reviewer (format): Currency must be written with the symbol before the number: 3元 => ¥3. Suggested translation: "Animal pictures ¥3 each" | 动物图片每张3元 | Animal pictures 3 yuan each |
| warning | 13 | p12_s21 | Reviewer (format): The enumerator '(3)' must be followed by a space. Suggested translation: "(3) In the group gymnastics performance, how many patterns can 36 people form?" | （3）团体操表演中，36人能组成多少个图案？ | (3)In the group gymnastics performance, how many patterns c… |
| warning | 14 | p13_s21 | Reviewer (format): Money amounts must be written with the currency symbol before the number: '¥2', not '2 yuan'. Suggested translation: "¥2" | 2元 | 2 yuan |
| warning | 16 | p15_s10 | Reviewer (grammar): 'With the situation' is awkward; 'In context' is more natural. Suggested translation: "(3) In context, say what the number sentences below mean, and calculate." | （3）结合情境说说下面算式表示的意思，并算一算。 | (3) With the situation, say what the number sentences below… |
| warning | 16 | p15_s12 | Reviewer (format): Heading should be in Title Case: 'Math Game'. Suggested translation: "8. Math Game" | 8.数学游戏 | 8. Math game |
| warning | 17 | p16_s12 | Reviewer (grammar): 'Which classmate sees each of the four pictures below?' is acceptable but 'Which classmate sees each photo below?' flows better; meaning unchanged. Suggested translation: "Which classmate sees each of the four pictures below? Think first, then look." | 下面四幅图分别是哪位同学看到的？先想一想，再看一看。 | Which classmate sees each of the four pictures below? Think… |
| warning | 22 | p21_s14 | Reviewer (format): Missing space after the enumerator '(3)'. Suggested translation: "(3) If you buy only one of each item, which three items qualify for a gift pack? Calculate." | （3）如果每种商品只买一个，买哪三种商品能获得大礼包？算一算。 | (3)If you buy only one of each item, which three items qual… |
| warning | 26 | p25_s19 | Reviewer (grammar): Measure word '个' after a number should drop the parentheses or use the counted noun; '(jumps)' is introduced though the source only has the measure word. Suggested translation: "75" | 75个 | 75 (jumps) |
| warning | 26 | p25_s20 | Reviewer (grammar): Measure word '个' after a number should drop the parentheses; '(jumps)' is not in the source. Suggested translation: "23" | 23个 | 23 (jumps) |
| warning | 27 | p26_s12 | Reviewer (format): Labeled as heading but context is a paragraph; minor format inconsistency. | （2）冒险乐园和卡通世界一共售出多少张票？ | (2) How many tickets did Adventure Park and Cartoon World s… |
| warning | 28 | p27_s0 | Reviewer (format): 'Odometer (1)' is a section title; should follow Title Case style: 'Odometer (1)'. Suggested translation: "Odometer (1)" | 里程表（一） | Odometer (1) |
| warning | 28 | p27_s14 | Reviewer (format): Source has a typo '干米' but translation correctly gives 'km'; no meaning change. Suggested translation: "277 km" | 277干米 | 277 km |
| warning | 28 | p27_s16 | Reviewer (format): The Chinese place name 北京 is translated ("Beijing"); per the stated convention, proper names are written in pinyin, so the Chinese label form should be kept. Suggested translation: "北京" | 北京 | Beijing |
| warning | 28 | p27_s17 | Reviewer (format): The Chinese place name 保定 is translated ("Baoding"); per the stated convention, proper names are written in pinyin, so the Chinese label form should be kept. Suggested translation: "保定" | 保定 | Baoding |
| warning | 28 | p27_s18 | Reviewer (format): The Chinese place name 石家庄 is translated ("Shijiazhuang"); per the stated convention, proper names are written in pinyin, so the Chinese label form should be kept. Suggested translation: "石家庄" | 石家庄 | Shijiazhuang |
| warning | 28 | p27_s30 | Reviewer (format): Two separate city labels (Zhengzhou and Luoyang) are run together without a separator, making it look like one name. Suggested translation: "Zhengzhou Luoyang" | 郑州洛阳 | Zhengzhou Luoyang |
| warning | 29 | p28_s28 | Reviewer (grammar): "How many metres" uses British spelling; align with "meters". Suggested translation: "(2) It is 990 m from the museum to the cinema. How many meters is it from the park to the cinema?" | （2）博物馆到电影院一共990米，公园到电影院有多少米？ | (2) It is 990 m from the museum to the cinema. How many met… |
| warning | 29 | p28_s8 | Reviewer (grammar): British spelling "kilometres"; use "kilometers" for consistency with the rest of the materials. Suggested translation: "(1) How many kilometers is it from Jiujiang to Wuhu? Draw it and calculate." | （1）九江到芜湖有多少千米？画一画，算一算。 | (1) How many kilometres is it from Jiujiang to Wuhu? Draw i… |
| warning | 31 | p30_s20 | Reviewer (grammar): "Taoqi's family drove" shifts to the simple past; the narrative context of a trip description reads better in the present perfect. Suggested translation: "3. Taoqi's family has driven to the ancient capital for a trip. Their home is 1000 km from the ancient capital. They drove 255 km on the first day, 240 km on the second day, and 305 km on the third day." | 3.淘气一家开车去古都旅游。他家距古都1000千米，第一天行驶255千米，第二天行驶240千米，第三天行驶305千米。 | 3. Taoqi's family drove to the ancient capital for a trip. … |
| warning | 32 | p31_s1 | Reviewer (grammar): "Talk about it" is awkward for a textbook instruction addressed to pupils. Suggested translation: "1. Discuss and calculate." | 1.说一说，算一算。 | 1. Talk about it and calculate. |
| warning | 32 | p31_s28 | Reviewer (grammar): Slightly unnatural imperative for a textbook instruction. Suggested translation: "4. Calculate and fill in the blanks." | 4.算一算，填一填。 | 4. Calculate and fill in. |
| warning | 36 | p35_s13 | Reviewer (format): The source label '答' (Answer) lacks the colon found in '答：' (p35_s25, p37_s8). The translation style should be consistent; using 'Answer:' with a colon is the standard form. Suggested translation: "Answer:" | 答 | Answer |
| warning | 37 | p36_s1 | Reviewer (format): The source has no punctuation between '圈一圈' and '算一算'; a comma or 'and' is acceptable for readability. 'Circle and calculate' is fine, but keeping the comma style would match 'Circle, calculate'. | 1.圈一圈，算一算 | 1. Circle and calculate |
| warning | 44 | p43_s10 | Reviewer (format): The source is a sentence ending with a period, not a heading; translating it in Title Case changes its register. Suggested translation: "Talk about what you see." | 说一说你看到了什么。 | Talk About What You See |
| warning | 49 | p48_s11 | Reviewer (format): The source is vertical text '厘米' used as a unit label; 'cm' is correct per the abbreviation convention. Suggested translation: "cm" | 厘米 | cm |
| warning | 50 | p49_s10 | Reviewer (format): Source context is a heading/label written as a bare quantity; translation fine, but no capitalization issue arises. No action needed — reported only if heading casing convention applies. | 110米 | 110 m |
| warning | 50 | p49_s2 | Reviewer (format): Unit style inconsistency: the source uses 米 and other items in the set use "(m)" after equations, but here the unit is written as "560 m" — check consistency with the rest of the page. | 560米 | 560 m |
| warning | 51 | p50_s11 | Reviewer (grammar): "Estimate, Measure" — both activities should be linked naturally; comma splice reads oddly in a textbook instruction. Suggested translation: "6. Estimate and Measure" | 6.估一估，量一量 | 6. Estimate, Measure |
| warning | 53 | p52_s10 | Reviewer (format): The sentence is split across items p52_s10/p52_s11 and the translation of p52_s11 begins lowercase and lacks the article "the"; as a continuation it should read "the square's side length?". Suggested translation: "4. Taoqi used a piece of string 40 cm long to make a square. Do you know" | 4.淘气用一根40厘米长的绳子围成了一个正方形，你知道这个正方 | 4. Taoqi used a piece of string 40 cm long to make a square… |
| warning | 53 | p52_s11 | Reviewer (grammar): Sentence continuation should begin with the article: "the square's side length?" Suggested translation: "the square's side length?" | 形的边长是多少吗？ | square's side length? |
| warning | 53 | p52_s3 | Reviewer (grammar): "How many meters long is the fence?" is acceptable, but glossary unit style is "m"; also source has a typo 篱色 for 篱笆. Consider "How long is the fence (in m)?" Suggested translation: "How long is the fence in meters?" | 篱色长多少米？ | How many meters long is the fence? |
| warning | 54 | p53_s19 | Reviewer (format): The table headers "Square / side / perimeter" run together without separators; they should be separated. Suggested translation: "Square side perimeter" | 正方形边长周长 | Square side perimeter |
| warning | 56 | p55_s1 | Reviewer (format): Heading title case: "Ants Doing Exercises" is acceptable, but "Doing Exercises" is a literal rendering of 做操; consider "Ants Doing Morning Exercises" only if consistent. Title case is fine as is. | 蚂蚁做操 | Ants Doing Exercises |
| warning | 57 | p56_s15 | Reviewer (format): The two column labels are run together without a separator; the source lists them as separate column headings. Suggested translation: "Large vehicle passenger count Small vehicle passenger count" | 大车乘客数小车乘客数 | Large vehicle passenger count Small vehicle passenger count |
| warning | 57 | p56_s18 | Reviewer (grammar): Plural not used after a numeral: '2 vest' should be '2 vests'. Suggested translation: "(2) Lele's mother bought 2 vests and 1 sweater for the family. How much did she spend in total?" | （2）乐乐妈妈给家人买了2件马甲和1件毛衣，一共花了多少元？ | (2) Lele's mother bought 2 vest and 1 sweater for the famil… |
| warning | 58 | p57_s5 | Reviewer (format): Money must be written with the yuan symbol before the amount, not spelled out. Suggested translation: "¥12 each Electric train:" | 每人12元电动火车： | 12 yuan each Electric train: |
| warning | 58 | p57_s9 | Reviewer (format): Money must be written with the yuan symbol before the amount, not spelled out. Suggested translation: "¥6 each" | 每人6元 | 6 yuan each |
| warning | 61 | p60_s27 | Reviewer (format): Money must be written in Chinese yuan with the currency symbol before the number: 15元 => ¥15, 8元 => ¥8. Suggested translation: "Adult ticket ¥15 Student ticket ¥8" | 成人票15元学生票8元 | Adult ticket 15 yuan Student ticket 8 yuan |
| warning | 62 | p61_s23 | Reviewer (format): "kilometres" uses British spelling while elsewhere "km" is used; consistency preferred, though not a meaning change. Suggested translation: "How many kilometers is it from Taoqi's home to Grandma's home in total?" | 淘气家到奶奶家一共有多少千米？ | How many kilometres is it from Taoqi's home to Grandma's ho… |
| warning | 65 | p64_s28 | Reviewer (format): A parenthesised measure word after a column label is written with the counted noun, not '(pieces)'; write 'Insect specimens' and 'Plant specimens'. Suggested translation: "Type Insect specimens Plant specimens" | 种类昆虫标本/个植物标本/个 | Type Insect specimens (pieces) Plant specimens (pieces) |
| warning | 66 | p65_s10 | Reviewer (format): Currency amounts must be written with ¥ before the number; a bare unit label with no amount is written "yuan". Here the amount 72 is present. Suggested translation: "24×3=¥72" | 24×3=72（元） | 24×3=72 (yuan) |
| warning | 66 | p65_s18 | Reviewer (format): Label reads awkwardly as a reversed noun-number pair; in a label context "45 chickens" is more natural English. Suggested translation: "45 chickens" | 鸡45只 | Chickens 45 |
| warning | 66 | p65_s19 | Reviewer (format): Two vertical labels should be kept as separate stacked labels, not run together on one line. Suggested translation: "Ducks Geese" | 鸭鹅 | Ducks Geese |
| warning | 67 | p66_s16 | Reviewer (format): Label reads awkwardly as a reversed noun-number pair; "30 birch trees" is more natural. Suggested translation: "30 birch trees" | 桦树30棵 | Birch trees 30 |
| warning | 67 | p66_s17 | Reviewer (grammar): "Each layer has 12." is ambiguous; the source refers to 12 pigeons per layer, but the omitted object should at least read naturally. Suggested translation: "Each layer has 12." | 每层有12只。 | Each layer has 12. |
| warning | 68 | p67_s9 | Reviewer (grammar): "How many chicks in total?" lacks a verb. Suggested translation: "How many chicks are there in total?" | 一共有多少只小鸡？ | How many chicks in total? |
| warning | 69 | p68_s0 | Reviewer (grammar): "Forest doctor" is a literal translation of a Chinese exercise title; a natural textbook rendering would be "Forest Doctor" with title case. Suggested translation: "6. Forest Doctor" | 6.森林医生。 | 6. Forest doctor. |
| warning | 70 | p69_s18 | Reviewer (grammar): "What do you find?" is unnatural; a textbook prompt asks what the student discovers/notices and should be a complete sentence. Suggested translation: "14. Calculate. What do you notice?" | 14.算一算，你发现了什么？ | 14. Calculate. What do you find? |
| warning | 70 | p69_s19 | Reviewer (grammar): Word order "write two similar number sentences and calculate" is awkward; better to say calculate them and discuss. Suggested translation: "Write two similar number sentences and calculate them, then discuss the reasoning with your partner." | 再写两个类似的算式算一算，和同伴讨论一下其中的道理。 | Write two similar number sentences and calculate, then disc… |
| warning | 70 | p69_s6 | Reviewer (format): The source is three separate unit labels (一单元 二单元 三单元, i.e. "Unit 1 Unit 2 Unit 3"); the translation is fine, but the spacing reflects three stacked labels and should be preserved as such. Suggested translation: "Unit 1 Unit 2 Unit 3" | 单元二单元三单元 | Unit 1 Unit 2 Unit 3 |
| warning | 71 | p70_s15 | Reviewer (grammar): Missing final punctuation after "partner". Suggested translation: "Look, memorize, and tell your partner." | 看一看，记一记，并与同伴说一说 | Look, memorize, and tell your partner |
| warning | 73 | p72_s1 | Reviewer (grammar): Sentence is missing terminal punctuation in a textbook label. Suggested translation: "1996 is a leap year." | 1996年是润年 | 1996 is a leap year |
| warning | 73 | p72_s10 | Reviewer (format): The placeholder-like fragment "）年（" rendered as ") year (" keeps the closing parenthesis first; in English the blank order should read "( ) year ( )". Suggested translation: "( ) year ( )" | ）年（ | ) year ( |
| warning | 73 | p72_s12 | Reviewer (format): "）月" rendered as ") month" begins with a stray closing parenthesis; it should present the blank as "( ) month". Suggested translation: "( ) month" | ）月 | ) month |
| warning | 73 | p72_s20 | Reviewer (grammar): “the third to last day” is awkward; standard wording is “the third-to-last day” or “the third day from the end.” Suggested translation: "My birthday is the third-to-last day of the year." | 我的生日是一年的倒数第三天。 | My birthday is the third to last day of the year. |
| warning | 74 | p73_s15 | Reviewer (grammar): “__ h __ min.” is acceptable, but the source uses a dash “—” which could be preserved as a blank; minor style issue. | 第二次取信到第三次取信间隔时—分。 | The interval from the second collection to the third collec… |
| warning | 76 | p75_s26 | Reviewer (grammar): 'Which times on the right might they each have seen?' is awkward; 'each' should be placed to read naturally. Suggested translation: "In the second period in the morning, Xiaolan and Guli both looked at a clock. Which times on the right might each of them have seen?" | 上午第二节课，小兰和古丽都看了一下表，她们看到的可能分别是右面哪个时刻？ | In the second period in the morning, Xiaolan and Guli both … |
| warning | 78 | p77_s0 | Reviewer (format): The trailing code '308.0.0' appears attached to the heading; it is likely a page/section code, not part of the title. Keep the heading as 'Math Is Fun' and the code separately. Suggested translation: "Math Is Fun 308.0.0" | 数学好玩308.0.0 | Math Is Fun 308.0.0 |
| warning | 80 | p79_s8 | Reviewer (grammar): The source sentence ends without a period; the translation adds one, which is an acceptable minor punctuation normalization. No change needed. | 笑笑这样表示各种搭配方法，你能看懂吗？和同学交流 | Xiaoxiao shows the various matching methods like this. Can … |
| warning | 83 | p82_s9 | Reviewer (format): Stray middle dot (·) is misplaced and appears as punctuation noise; the source's trailing mark should follow the sentence. Suggested translation: "12 is 1 more than 11, and 18 is 7 more than 11." | 12比11多1，18比11多7· | 12 is 1 more than 11, 18 is 7· more than 11 |
| warning | 84 | p83_s0 | Reviewer (format): A heading beginning with a bare Chinese numeral is a unit heading; the translation should read "Unit 8" with the unit title in Title Case, without the stray digit placeholder string. Suggested translation: "Unit 8 Understanding Decimals" | 八332.1.0认识小数 | Unit 8 332.1.0 Understanding Decimals |
| warning | 84 | p83_s25 | Reviewer (format): "1 jiao" and "5 fen" must be written as yuan amounts with the symbol (¥3.15), not spelled out. Suggested translation: "No, it should be ¥3.15." | 不，应该是3元1角5分 | No, it should be 3 yuan 1 jiao 5 fen. |
| warning | 84 | p83_s34 | Reviewer (grammar): "贰圆" on a banknote is "¥2"; writing "Two yuan" spells out the unit contrary to the money convention. Suggested translation: "¥2" | 贰圆 | Two yuan |
| warning | 84 | p83_s45 | Reviewer (grammar): The question ends with "呢" and should read "Is this ¥2.40 or ¥2.04?"; meaning is fine but the question mark placement is correct — no error. Suggested translation: "Is this ¥2.40 or ¥2.04?" | 这是2.40元还是2.04元呢？ | Is this ¥2.40 or ¥2.04? |
| warning | 84 | p83_s47 | Reviewer (grammar): "贰圆" is a ¥2 banknote; spelling out "Two yuan" violates the money convention. Suggested translation: "¥2" | 贰圆 | Two yuan |
| warning | 84 | p83_s51 | Reviewer (format): "¥8.1" should be written with two decimal places as "¥8.10" to match the decimal-place convention. Suggested translation: "¥8.10" | 8.1元 | ¥8.1 |
| warning | 84 | p83_s9 | Reviewer (grammar): "元，是" is rendered awkwardly; it should read "yuan, that is". Suggested translation: "yuan, that is" | 元，是 | yuan, that is |
| warning | 86 | p85_s0 | Reviewer (format): The heading 货比三家 is a unit heading and should be in Title Case. Suggested translation: "Shop Around" | 货比三家 | Shop Around |
| warning | 86 | p85_s15 | Reviewer (format): Money amounts should use the yuan symbol before the number in sentences; the source has 1.80元 and 1.8元, so use ¥1.80 and ¥1.8. Suggested translation: "¥1.80 is 1 yuan 8 jiao, and can also be written as ¥1.8." | 1.80元是1元8角，也可以写成1.8元。 | 1.80 yuan is 1 yuan 8 jiao, and can also be written as ¥1.8. |
| warning | 86 | p85_s29 | Reviewer (format): Money amounts should use the yuan symbol before the number in sentences; the source has 1.8元, 1.9元 and 2元. Suggested translation: "¥1.8 and ¥1.9 are both less than ¥2; Dingding Stationery Shop's erasers are the most expensive." | 1.8元和1.9元都不到2元，丁丁文具店的橡皮最贵。 | 1.8 yuan and 1.9 yuan are both less than 2 yuan; Dingding S… |
| warning | 87 | p86_s24 | Reviewer (format): The enumerator "2." is kept, which is correct; no problem. | 2.谁多？谁少？ | 2. Which is more? Which is less? |
| warning | 87 | p86_s29 | Reviewer (format): The enumerator "3." is kept; no problem. | 3.在 | 3. In |
| warning | 87 | p86_s30 | Reviewer (grammar): A fragment; no problem. | <”或 | <" or |
| warning | 87 | p86_s39 | Reviewer (grammar): "3 kinds of goods" is acceptable; no problem. | 4.到商店调查3种商品的价格，做好记录。与同学比一比同一种商 | 4. Visit a shop and find the prices of 3 kinds of goods. Ke… |
| warning | 87 | p86_s40 | Reviewer (grammar): The source fragment is the continuation "品的价格。"; the translation repeats "prices of goods." as a separate line, losing the continuation but not changing meaning. Suggested translation: "prices of goods." | 品的价格。 | prices of goods. |
| warning | 87 | p86_s6 | Reviewer (grammar): The adjective "Towel" is used as a shop or item label; labels are usually written in Title Case and the noun should be used as given. Suggested translation: "Towel" | 毛巾 | Towel |
| warning | 88 | p87_s0 | Reviewer (grammar): The title "存零用钱" means "Saving Pocket Money"; "Saving Money" omits "pocket". Suggested translation: "Saving Pocket Money" | 存零用钱 | Saving Money |
| warning | 90 | p89_s29 | Reviewer (format): The bare unit 角 after the blank should keep the unit label consistent; 'jiao' alone is acceptable but should match the yuan/jiao column label style used elsewhere. Suggested translation: "jiao" | 角 | jiao |
| warning | 94 | p93_s43 | Reviewer (format): Money amounts are written with the currency symbol before the number, in sentences and labels alike: 50元 => ¥50, 18.6元 => ¥18.6. Suggested translation: "¥50 − ¥18.6 =" | 50元一18.6元= | 50 yuan − 18.6 yuan = |
| warning | 95 | p94_s16 | Reviewer (format): Money amounts must be written with the currency symbol before the number (¥6.50), not spelled as 'yuan'. Suggested translation: "¥6.50" | 6.50元 | 6.50 yuan |
| warning | 95 | p94_s17 | Reviewer (format): Money amounts must be written with the currency symbol before the number (¥3.40). Suggested translation: "¥3.40" | 3.40元 | 3.40 yuan |
| warning | 95 | p94_s24 | Reviewer (format): Money amounts must be written with the currency symbol before the number (¥30.2). Suggested translation: "¥30.2" | 30.2元 | 30.2 yuan |
| warning | 95 | p94_s25 | Reviewer (format): Money amounts must be written with the currency symbol before the number (¥61.0). Suggested translation: "¥61.0" | 61.0元 | 61.0 yuan |
| warning | 95 | p94_s28 | Reviewer (format): Money amounts must be written with the currency symbol before the number (¥26.7). Suggested translation: "¥26.7" | 26.7元 | 26.7 yuan |
| warning | 95 | p94_s29 | Reviewer (format): Money amounts must be written with the currency symbol before the number (¥20.4). Suggested translation: "¥20.4" | 20.4元 | 20.4 yuan |
| warning | 95 | p94_s32 | Reviewer (format): Money amount should be ¥ (currency symbol before the number): 'work out the total in yuan' must use ¥. Suggested translation: "(2) Ask your family about this month's phone bill and work out the total in ¥" | （2）调查你的家人这个月的电话费支出情况，算算一共是多少元 | (2) Ask your family about this month's phone bill and work … |
| warning | 95 | p94_s34 | Reviewer (format): Money amounts must be written with the currency symbol before the number (¥0.80). Suggested translation: "¥0.80" | 0.80元 | 0.80 yuan |
| warning | 95 | p94_s35 | Reviewer (format): Money amounts must be written with the currency symbol before the number (¥2.90). Suggested translation: "¥2.90" | 2.90元 | 2.90 yuan |
| warning | 95 | p94_s36 | Reviewer (format): Money amount must be written with the currency symbol (¥20), not '20 yuan'. Suggested translation: "(2) I have ¥20. Is it enough for a pair of sneakers and a sun hat?" | （2）我有20元，买一双旅游鞋和一顶太阳帽，够吗？ | (2) I have 20 yuan. Is it enough for a pair of sneakers and… |
| warning | 95 | p94_s38 | Reviewer (format): Money amounts must be written with the currency symbol before the number (¥3.40). Suggested translation: "¥3.40" | 3.40元 | 3.40 yuan |
| warning | 95 | p94_s39 | Reviewer (format): Money amounts must be written with the currency symbol before the number (¥20.30). Suggested translation: "¥20.30" | 20.30元 | 20.30 yuan |
| warning | 95 | p94_s40 | Reviewer (format): Money amounts must be written with the currency symbol before the number (¥15.60). Suggested translation: "¥15.60" | 15.60元 | 15.60 yuan |
| warning | 96 | p95_s5 | Reviewer (format): Money amount must be written with the currency symbol (¥3.00). Suggested translation: "¥3.00" | 3.00元 | 3.00 yuan |
| warning | 96 | p95_s6 | Reviewer (format): Money amount must be written with the currency symbol (¥2.80). Suggested translation: "¥2.80" | 2.80元 | 2.80 yuan |
| warning | 97 | p96_s16 | Reviewer (grammar): The final clause 'and what do you find?' is a question fused onto an imperative sentence; should be a separate question. Suggested translation: "1. Choose a desk, the teacher's desk or another object in the classroom. Look at it from different positions and talk about it with a partner. What do you find?" | 1.在教室里选择一张课桌、讲台或其他物体，从不同位置看一看，与同伴说一说，你发现了什么？ | 1. Choose a desk, the teacher's desk or another object in t… |
| warning | 101 | p100_s7 | Reviewer (format): The source blank （） is translated as '()' which is acceptable, but the unit 分 is rendered as 'minutes' with the blank before it; fine—no finding. | 笑笑写作业用了（）分。 | Xiaoxiao spent () minutes doing her homework. |
| warning | 109 | p108_s5 | Reviewer (format): The source separates the weekday labels with a space (二 四五六); the translation drops it, losing the original spacing/omitted-day layout. Suggested translation: "Tue Thu Fri Sat" | 二 四五六 | Tue Thu Fri Sat |
| warning | 109 | p108_s8 | Reviewer (format): Source has a space between 二 and 四五六; the translation removes it. Suggested translation: "Tue Thu Fri Sat" | 二 四五六 | Tue Thu Fri Sat |

### `numbers` — 1 error, 0 warnings

| Severity | Page | Segment | Message | Source | Translation |
|---|---|---|---|---|---|
| error | 34 | p33_s6 | Number "2" from the source is missing in the translation; keep every number exactly as written in the source | 2回×3=60 | 20×3=60 |

### `image_text` — 0 errors, 2 warnings

| Severity | Page | Segment | Message | Source | Translation |
|---|---|---|---|---|---|
| warning | 43 | p42_i168_27 | The text '（2）一棵松树与一棵柳树比，' was left in the source language (inline pictograms the OCR cannot read (left in the picture)): the line is built around symbols or pictures the OCR could not read - check the page in the preview | （2）一棵松树与一棵柳树比， |  |
| warning | 43 | p42_i168_27 | The text '（2）一棵松树与一棵柳树比，' was left in the source language (inline pictograms the OCR cannot read (left in the picture)): the line is built around symbols or pictures the OCR could not read - check the page in the preview | （2）一棵松树与一棵柳树比， |  |

### `length_ratio` — 0 errors, 1 warning

| Severity | Page | Segment | Message | Source | Translation |
|---|---|---|---|---|---|
| warning | 6 | p5_s16 | The translation looks too short: 5 characters for 9 translatable source characters (ratio 0.56, about 2.60 expected); check that nothing was omitted | （3元）3元）3元 | ¥3 ¥3 ¥3 |
