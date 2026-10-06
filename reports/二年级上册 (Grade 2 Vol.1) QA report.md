# QA report

**Result:** QA FAILED after 3 rounds: 262 errors, 109 warnings (1884.7 s); proofread: 954 corrections applied; output file checks: 0 error(s)

**Document:** 数学 (zh → en, 119 page(s), 1856 translatable segment(s))

**Checks run:** `completeness`, `placeholders`, `numbers`, `untranslated`, `target_script`, `glossary`, `length_ratio`, `formatting`, `layout_fit`, `image_text`, `llm_review`, `output_checks`

## Rounds

| Round | Errors | Warnings | Re-translated | Passed | Duration |
|---|---|---|---|---|---|
| 1 | 535 | 307 | 391 segment(s) | no | 500.1 s |
| 2 | 278 | 339 | 255 segment(s) | no | 467.1 s |
| 3 | 274 | 300 | 0 segment(s) | no | 159.2 s |

- Round 1: llm_review ×589, layout_fit ×81, untranslated ×79, target_script ×43, formatting ×19, glossary ×19, completeness ×7, image_text ×2, length_ratio ×2, placeholders ×1
- Round 2: llm_review ×513, layout_fit ×78, formatting ×8, untranslated ×4, completeness ×3, placeholders ×3, image_text ×2, length_ratio ×2, numbers ×2, glossary ×1, target_script ×1
- Round 3: llm_review ×479, layout_fit ×69, completeness ×7, formatting ×4, glossary ×3, untranslated ×3, image_text ×2, length_ratio ×2, placeholders ×2, target_script ×2, numbers ×1

## Final issues (371)

### `completeness` — 12 errors, 0 warnings

| Severity | Page | Segment | Message | Source | Translation |
|---|---|---|---|---|---|
| error | 8 | p7_s14 | The translation "−" contains no words; translate the complete source text | 一 | − |
| error | 17 | p16_s22 | The translation "=" contains no words; translate the complete source text | 合 | = |
| error | 30 | p29_s5 | The translation "?" contains no words; translate the complete source text | 吗？ | ? |
| error | 67 | p66_s15 | The translation "." contains no words; translate the complete source text | 根。 | . |
| error | 67 | p66_s17 | The translation "." contains no words; translate the complete source text | 本。 | . |
| error | 74 | p73_s19 | The translation "." contains no words; translate the complete source text | 倍 | . |
| error | 75 | p74_s20 | The translation "." contains no words; translate the complete source text | 倍 | . |
| error | 75 | p74_s24 | The translation "." contains no words; translate the complete source text | 倍 | . |
| error | 111 | p110_s39 | The segment has no translation; translate the complete source text | 中 |  |
| error | 115 | p114_s6 | The segment has no translation; translate the complete source text | 张飞关羽 |  |
| error | 115 | p114_s8 | The segment has no translation; translate the complete source text | 兵 |  |
| error | 117 | p116_s7 | The translation "___" contains no words; translate the complete source text | 次 | ___ |

### `formatting` — 45 errors, 0 warnings

| Severity | Page | Segment | Message | Source | Translation |
|---|---|---|---|---|---|
| error | 4 | p3_s3 | Start the translation with the list marker "-" exactly as in the source | - 4 元 | ¥- 4 |
| error | 6 | p5_s1 | The source does not end with a question mark; do not end the translation with one | 谁的得分高 | Who Scores Higher? |
| error | 17 | p16_s12 | Keep the line breaks of the source: it has 0 line break(s), the translation has 4 | 能换_张能换能换能换和张 | = ___ notes = ___ notes = ___ notes = ___ notes and ___ not… |
| error | 17 | p16_s4 | Start the translation with the list marker "(2)" exactly as in the source | (2)买1盏元？你会怎样付钱？ | ((2)) To buy 1 yuan do you need? How would you pay? |
| error | 17 | p16_s4 | Keep the line breaks of the source: it has 0 line break(s), the translation has 2 | (2)买1盏元？你会怎样付钱？ | ((2)) To buy 1 yuan do you need? How would you pay? |
| error | 19 | p18_s10 | The source does not end with a question mark; do not end the translation with one | 贵多池 | costs how much more? |
| error | 21 | p20_s1 | The source does not end with a question mark; do not end the translation with one | 1.圈一圈，数一数一共有多少个 | 1. Circle and count. How many pandas are there in total? |
| error | 23 | p22_s11 | Remove the symbol(s) □×2: they are not in the source (a picture in the book is not a symbol; leave it out rather than inventing one) | (2) 2+2+2+2+2+2=12写成乘法算式:×□= | (2) 2+2+2+2+2+2=12 written as multiplication: □ × □ = □ |
| error | 34 | p33_s10 | Keep the line breaks of the source: it has 0 line break(s), the translation has 2 | —五得五二五一十三五十五 | 1 × 5 = 5 2 × 5 = 10 3 × 5 = 15 |
| error | 34 | p33_s15 | Keep the line breaks of the source: it has 0 line break(s), the translation has 4 | 五五六七八 | 4 × 5 = 5 × 5 = 5 × 6 = 5 × 7 = 5 × 8 = |
| error | 36 | p35_s12 | Keep the line breaks of the source: it has 0 line break(s), the translation has 3 | 二六二七二八二九 | 2×6= 2×7= 2×8= 2×9= |
| error | 36 | p35_s6 | Keep the line breaks of the source: it has 0 line break(s), the translation has 4 | 一二得二二二得四二三得六二四得二五 | 1 × 2 = 2 2 × 2 = 4 2 × 3 = 6 2 × 4 = 2 × 5 = |
| error | 37 | p36_s3 | Start the translation with the list marker "·" exactly as in the source | ·，9分别与2相乘，在得到的数上画圈 | ..., 9: multiply each number by 2 and circle the answers. |
| error | 40 | p39_s0 | The source does not end with a question mark; do not end the translation with one | 需要几个轮子 | How Many Wheels? |
| error | 40 | p39_s1 | Keep the line breaks of the source: it has 0 line break(s), the translation has 2 | 1辆车3个轮子2辆车6个轮子3辆车9个轮子 | 1 tricycle: 3 wheels 2 tricycles: 6 wheels 3 tricycles: 9 w… |
| error | 40 | p39_s15 | Keep the line breaks of the source: it has 0 line break(s), the translation has 2 | 三七三八三九 | 3×7= 3×8= 3×9= |
| error | 40 | p39_s6 | Keep the line breaks of the source: it has 0 line break(s), the translation has 3 | 一三得三二三得六三三得九三四 | 1 × 3 = 3 2 × 3 = 6 3 × 3 = 9 3 × 4 = |
| error | 41 | p40_s4 | Keep the line breaks of the source: it has 0 line break(s), the translation has 3 | 二八十六三九二十七四五二十三六十八 | 2 × 8 = 16 3 × 9 = 27 4 × 5 = 20 3 × 6 = 18 |
| error | 42 | p41_s18 | Start the translation with the list marker "四," exactly as in the source | 四, 14+14=28。 | 14+14=28. |
| error | 50 | p49_s7 | Keep the line breaks of the source: it has 0 line break(s), the translation has 2 | 爸爸妈妈淘气 | Dad Mom Taoqi |
| error | 53 | p52_s1 | The source does not end with a question mark; do not end the translation with one | 教室有多长 | How long is the classroom? |
| error | 55 | p54_s0 | The source does not end with a question mark; do not end the translation with one | 课桌有多长 | How long is the desk? |
| error | 56 | p55_s2 | Keep the line breaks of the source: it has 0 line break(s), the translation has 3 | 估计（）厘米（）厘米（）厘米 | Estimate () cm () cm () cm |
| error | 56 | p55_s3 | Keep the line breaks of the source: it has 0 line break(s), the translation has 3 | 测量（）厘米（）厘米（）厘米 | Measured () cm () cm () cm |
| error | 56 | p55_s4 | Keep the line breaks of the source: it has 0 line break(s), the translation has 2 | 铅笔长橡皮长文具盒长 | Pencil Eraser Pencil case |
| error | 57 | p56_s0 | The source does not end with a question mark; do not end the translation with one | 1米有多长 | How long is 1 metre? |
| error | 57 | p56_s14 | Keep the line breaks of the source: it has 0 line break(s), the translation has 2 | 门高约2黄瓜长约20李老师身高约175 | Door height: about 2 Cucumber length: about 20 Mr Li's heig… |
| error | 57 | p56_s15 | Keep the line breaks of the source: it has 0 line break(s), the translation has 2 | 一拆长约15橡皮长约3树高约10 | Hand span: about 15 Eraser length: about 3 Tree height: abo… |
| error | 58 | p57_s9 | The source does not end with a question mark; do not end the translation with one | 看看是多少厘米 | How many centimetres is it? |
| error | 63 | p62_s13 | Keep the line breaks of the source: it has 0 line break(s), the translation has 3 | 平均分成2份，每份有—平均分成3份，每份有—平均分成6份，每份有—平均分成9份，每份有— | Divide into 2 equal groups: each has ____ Divide into 3 equ… |
| error | 69 | p68_s16 | The source does not end with a question mark; do not end the translation with one | 3.（1）每6块橡皮装1盒，可以装 | 3. (1) 6 erasers fill 1 box. How many boxes can they fill? |
| error | 73 | p72_s3 | The source does not end with a question mark; do not end the translation with one | 说说你是怎么解决的。 | How did you solve it? |
| error | 76 | p75_s4 | Remove the symbol(s) ○: they are not in the source (a picture in the book is not a symbol; leave it out rather than inventing one) | 的个数是的 | number is ○ number × |
| error | 82 | p81_s1 | The source does not end with a question mark; do not end the translation with one | 有多少张贴画 | How many stickers? |
| error | 82 | p81_s15 | Keep the line breaks of the source: it has 0 line break(s), the translation has 3 | 六得二六三六四六 | 1 × 6 = 2 × 6 = 3 × 6 = 4 × 6 = |
| error | 84 | p83_s14 | Keep the line breaks of the source: it has 0 line break(s), the translation has 2 | 七七七上 | 4 × 7 = 5 × 7 = 6 × 7 = |
| error | 86 | p85_s4 | Keep the line breaks of the source: it has 0 line break(s), the translation has 3 | 球数／个买足球的钱／元买篮球的钱／元你能编出8和9的乘法口诀吗？ | Number of balls Cost of footballs (¥) Cost of basketballs (… |
| error | 95 | p94_s4 | Keep the line breaks of the source: it has 0 line break(s), the translation has 2 | 可以分成几组每组只数里最大能填几？ | Number of groups Number in each group What is the largest n… |
| error | 98 | p97_s21 | The source does not end with a question mark; do not end the translation with one | 20元能买几盒 | How many boxes for ¥20? |
| error | 103 | p102_s31 | Remove the symbol(s) △: they are not in the source (a picture in the book is not a symbol; leave it out rather than inventing one) | （1）每份有5个，有2份。 | (1) Each group has 5 △; there are 2 groups. |
| error | 103 | p102_s32 | Remove the symbol(s) □: they are not in the source (a picture in the book is not a symbol; leave it out rather than inventing one) | （2）先画18个，再把这些平均分成3份。 | (2) First draw 18 □, then divide them equally into 3 groups. |
| error | 103 | p102_s33 | Remove the symbol(s) ○: they are not in the source (a picture in the book is not a symbol; leave it out rather than inventing one) | (3）先画20个，再每4个1份圈一圈。 | (3) First draw 20 ○, then circle every 4 as 1 group. |
| error | 103 | p102_s34 | Keep the symbol(s) △ of the source in the translation, at the matching position | （4）先画3个△，再画，的个数是△的2倍。 | (4) First draw 3 △, then draw 2 times as many ○. |
| error | 103 | p102_s34 | Remove the symbol(s) ○: they are not in the source (a picture in the book is not a symbol; leave it out rather than inventing one) | （4）先画3个△，再画，的个数是△的2倍。 | (4) First draw 3 △, then draw 2 times as many ○. |
| error | 109 | p108_s0 | The source does not end with a question mark; do not end the translation with one | 本学期你学到了什么 | What have you learned this term? |

### `glossary` — 34 errors, 0 warnings

| Severity | Page | Segment | Message | Source | Translation |
|---|---|---|---|---|---|
| error | 9 | p8_s17 | Glossary: translate "统计" as "statistics" | 3.机灵狗不小心把订报刊的统计表弄脏了。 | 3. Clever Dog accidentally got the newspaper subscription t… |
| error | 14 | p13_s35 | Glossary: translate "练习" as "exercise" | 可以买1把尺子和1个练习本 | You can buy 1 ruler and 1 notebook. |
| error | 14 | p13_s7 | Glossary: translate "练习" as "exercise" | 练习本 | Notebook |
| error | 23 | p22_s10 | Glossary: translate "算式" as "number sentence" | （1） 4+4+4=12写成乘法算式： | (1) 4+4+4=12 written as multiplication: |
| error | 23 | p22_s11 | Glossary: translate "算式" as "number sentence" | (2) 2+2+2+2+2+2=12写成乘法算式:×□= | (2) 2+2+2+2+2+2=12 written as multiplication: □ × □ = □ |
| error | 23 | p22_s13 | Glossary: translate "算式" as "number sentence" | 5.把16页和17页的加法算式改写成乘法算式。 | 5. Rewrite the addition sentences on pages 16 and 17 as mul… |
| error | 23 | p22_s3 | Glossary: translate "算式" as "number sentence" | 加法算式： | Addition sentence: |
| error | 23 | p22_s4 | Glossary: translate "算式" as "number sentence" | 加法算式： | Addition sentence: |
| error | 23 | p22_s5 | Glossary: translate "算式" as "number sentence" | 乘法算式： | Multiplication sentence: |
| error | 23 | p22_s6 | Glossary: translate "算式" as "number sentence" | 乘法算式：×=88.7.088.7.1（88.7.2） | Multiplication: 88.7.0 × 88.7.1 = 88.7.2 () |
| error | 24 | p23_s3 | Glossary: translate "算式" as "number sentence" | 乘法算式是 | As multiplication: |
| error | 24 | p23_s9 | Glossary: translate "算式" as "number sentence" | 乘法算式是 | As multiplication: |
| error | 25 | p24_s10 | Glossary: translate "算式" as "number sentence" | 加法算式： | Addition sentence: |
| error | 25 | p24_s11 | Glossary: translate "算式" as "number sentence" | 加法算式： | Addition sentence: |
| error | 25 | p24_s12 | Glossary: translate "算式" as "number sentence" | 乘法算式： | Multiplication sentence: |
| error | 25 | p24_s13 | Glossary: translate "算式" as "number sentence" | 乘法算式： | Multiplication sentence: |
| error | 28 | p27_s12 | Glossary: translate "算式" as "number sentence" | 加法算式： | Addition sentence: |
| error | 28 | p27_s13 | Glossary: translate "算式" as "number sentence" | 加法算式： | Addition sentence: |
| error | 28 | p27_s14 | Glossary: translate "算式" as "number sentence" | 乘法算式： | Multiplication sentence: |
| error | 28 | p27_s15 | Glossary: translate "算式" as "number sentence" | 乘法算式： | Multiplication sentence: |
| error | 28 | p27_s16 | Glossary: translate "算式" as "number sentence" | 4.把加法算式改写成乘法算式。 | 4. Rewrite each addition sentence as a multiplication sente… |
| error | 38 | p37_s9 | Glossary: translate "找一找" as "Find" | 在你的课间活动中找一找，有没有能用乘法解决的问题？ | Look at your break-time activities. Are there any problems … |
| error | 45 | p44_s7 | Glossary: translate "算式" as "number sentence" | （3）算式5×3=15可以解决什 | (3) What problem can 5×3=15 |
| error | 48 | p47_s16 | Glossary: translate "算一算" as "Calculate" | 与同伴合作，再编一道类似的题目，并算一算。 | Work with a partner to make up a similar problem and solve … |
| error | 52 | p51_s0 | Glossary: translate "算式" as "number sentence" | 10.先把口诀补充完整，再根据口诀写出乘法算式。 | 10. Complete each times-table fact, then write its multipli… |
| error | 61 | p60_s11 | Glossary: translate "找一找" as "Find" | 找一找，生活中还有哪些地方用到米或厘米？ | Look around: where else in everyday life do we use metres o… |
| error | 61 | p60_s8 | Glossary: translate "找一找" as "Find" | 你知道“限高4米”是什么意思吗？在校园里找一找，4米有多高？ | Do you know what "Height limit 4 m" means? Look around your… |
| error | 71 | p70_s14 | Glossary: translate "算一算" as "Calculate" | 6.讲故事，并列算式算一算 | 6. Tell a story, write a number sentence and work it out |
| error | 88 | p87_s1 | Glossary: translate "算式" as "number sentence" | 找出乘数中有3的乘法算式，并完成下表。 | Find the multiplication sentences with 3 as a multiplier, a… |
| error | 88 | p87_s3 | Glossary: translate "算式" as "number sentence" | 这些算式乘数中都有3 | These all have 3 as a multiplier |
| error | 88 | p87_s4 | Glossary: translate "算式" as "number sentence" | 348.6.0这些算式的积都是18 | 348.6.0These all have a product of 18 |
| error | 98 | p97_s15 | Glossary: translate "倍数" as "multiple" | 的倍数 | times table |
| error | 98 | p97_s16 | Glossary: translate "倍数" as "multiple" | 8的倍数 | 8 times table |
| error | 102 | p101_s5 | Glossary: translate "找一找" as "Find" | 1.我们学了哪些长度单位？找一找，生活中有哪些物品的长度大约是1厘米，有哪些大约是1米？ | 1. What units of length have we learned? Look around: which… |

### `layout_fit` — 78 errors, 48 warnings

| Severity | Page | Segment | Message | Source | Translation |
|---|---|---|---|---|---|
| error | 3 | p2_s6 | Shorten the translation to at most 9 characters so it fits the original box (the current translation of 12 characters overflows its box; the minimum allowed size is 55%) | 我想一想 | Let Me Think |
| error | 3 | p2_s6 | Shorten the translation to at most 9 characters so it fits the original box (the current translation of 12 characters overflows its box; the minimum allowed size is 55%) | 我想一想 | Let Me Think |
| error | 7 | p6_s5 | Shorten the translation to at most 7 characters so it fits the original box (the current translation of 14 characters overflows its box; the minimum allowed size is 55%) | 奇思妙想 | Qisi Miaoxiang |
| error | 7 | p6_s5 | Shorten the translation to at most 7 characters so it fits the original box (the current translation of 14 characters overflows its box; the minimum allowed size is 55%) | 奇思妙想 | Qisi Miaoxiang |
| error | 8 | p7_s2 | Shorten the translation to at most 7 characters so it fits the original box (the current translation of 9 characters overflows its box; the minimum allowed size is 55%) | 25人 | 25 people |
| error | 8 | p7_s2 | Shorten the translation to at most 7 characters so it fits the original box (the current translation of 9 characters overflows its box; the minimum allowed size is 55%) | 25人 | 25 people |
| error | 13 | p12_s20 | Shorten the translation to at most 18 characters so it fits the original box (the current translation of 26 characters overflows its box; the minimum allowed size is 55%) | 姓名淘气笑笑奇思 | Name Taoqi, Xiaoxiao, Qisi |
| error | 13 | p12_s20 | Shorten the translation to at most 18 characters so it fits the original box (the current translation of 26 characters overflows its box; the minimum allowed size is 55%) | 姓名淘气笑笑奇思 | Name Taoqi, Xiaoxiao, Qisi |
| error | 14 | p13_s1 | Shorten the translation to at most 14 characters so it fits the original box (the current translation of 17 characters overflows its box; the minimum allowed size is 55%) | 买文具 | Buying Stationery |
| error | 14 | p13_s1 | Shorten the translation to at most 14 characters so it fits the original box (the current translation of 17 characters overflows its box; the minimum allowed size is 55%) | 买文具 | Buying Stationery |
| error | 14 | p13_s7 | Shorten the translation to at most 6 characters so it fits the original box (the current translation of 8 characters overflows its box; the minimum allowed size is 55%) | 练习本 | Notebook |
| error | 14 | p13_s7 | Shorten the translation to at most 6 characters so it fits the original box (the current translation of 8 characters overflows its box; the minimum allowed size is 55%) | 练习本 | Notebook |
| error | 16 | p15_s9 | Shorten the translation to at most 9 characters so it fits the original box (the current translation of 13 characters overflows its box; the minimum allowed size is 55%) | 民银行 | People's Bank |
| error | 16 | p15_s9 | Shorten the translation to at most 9 characters so it fits the original box (the current translation of 13 characters overflows its box; the minimum allowed size is 55%) | 民银行 | People's Bank |
| error | 19 | p18_s10 | Shorten the translation to at most 17 characters so it fits the original box (the current translation of 20 characters overflows its box; the minimum allowed size is 55%) | 贵多池 | costs how much more? |
| error | 19 | p18_s10 | Shorten the translation to at most 17 characters so it fits the original box (the current translation of 20 characters overflows its box; the minimum allowed size is 55%) | 贵多池 | costs how much more? |
| error | 22 | p21_s8 | Shorten the translation to at most 29 characters so it fits the original box (the current translation of 34 characters overflows its box; the minimum allowed size is 55%) | 人坐小飞机 | ___ people ride the little planes. |
| error | 22 | p21_s8 | Shorten the translation to at most 29 characters so it fits the original box (the current translation of 34 characters overflows its box; the minimum allowed size is 55%) | 人坐小飞机 | ___ people ride the little planes. |
| error | 28 | p27_s5 | Shorten the translation to at most 6 characters so it fits the original box (the current translation of 7 characters overflows its box; the minimum allowed size is 55%) | 格。 | spaces. |
| error | 28 | p27_s5 | Shorten the translation to at most 6 characters so it fits the original box (the current translation of 7 characters overflows its box; the minimum allowed size is 55%) | 格。 | spaces. |
| error | 32 | p31_s9 | Shorten the translation to at most 6 characters so it fits the original box (the current translation of 8 characters overflows its box; the minimum allowed size is 55%) | 赵云 | Zhao Yun |
| error | 32 | p31_s9 | Shorten the translation to at most 6 characters so it fits the original box (the current translation of 8 characters overflows its box; the minimum allowed size is 55%) | 赵云 | Zhao Yun |
| error | 34 | p33_s20 | Shorten the translation to at most 10 characters so it fits the original box (the current translation of 12 characters overflows its box; the minimum allowed size is 55%) | 三五九 | 3 × 5 = ____ |
| error | 34 | p33_s20 | Shorten the translation to at most 10 characters so it fits the original box (the current translation of 12 characters overflows its box; the minimum allowed size is 55%) | 三五九 | 3 × 5 = ____ |
| error | 51 | p50_s28 | Shorten the translation to at most 6 characters so it fits the original box (the current translation of 8 characters overflows its box; the minimum allowed size is 55%) | 赵云 | Zhao Yun |
| error | 51 | p50_s28 | Shorten the translation to at most 6 characters so it fits the original box (the current translation of 8 characters overflows its box; the minimum allowed size is 55%) | 赵云 | Zhao Yun |
| error | 52 | p51_s24 | Shorten the translation to at most 5 characters so it fits the original box (the current translation of 7 characters overflows its box; the minimum allowed size is 55%) | 7个 | 7 boxes |
| error | 52 | p51_s24 | Shorten the translation to at most 5 characters so it fits the original box (the current translation of 7 characters overflows its box; the minimum allowed size is 55%) | 7个 | 7 boxes |
| error | 66 | p65_s0 | Shorten the translation to at most 11 characters so it fits the original box (the current translation of 13 characters overflows its box; the minimum allowed size is 55%) | 分糖果 | Sharing Candy |
| error | 66 | p65_s0 | Shorten the translation to at most 11 characters so it fits the original box (the current translation of 13 characters overflows its box; the minimum allowed size is 55%) | 分糖果 | Sharing Candy |
| error | 66 | p65_s10 | Shorten the translation to at most 7 characters so it fits the original box (the current translation of 9 characters overflows its box; the minimum allowed size is 55%) | 生4 | Student 4 |
| error | 66 | p65_s10 | Shorten the translation to at most 7 characters so it fits the original box (the current translation of 9 characters overflows its box; the minimum allowed size is 55%) | 生4 | Student 4 |
| error | 68 | p67_s0 | Shorten the translation to at most 13 characters so it fits the original box (the current translation of 15 characters overflows its box; the minimum allowed size is 55%) | 分香蕉 | Sharing Bananas |
| error | 68 | p67_s0 | Shorten the translation to at most 13 characters so it fits the original box (the current translation of 15 characters overflows its box; the minimum allowed size is 55%) | 分香蕉 | Sharing Bananas |
| error | 69 | p68_s18 | Shorten the translation to at most 5 characters so it fits the original box (the current translation of 8 characters overflows its box; the minimum allowed size is 55%) | 块。 | erasers. |
| error | 69 | p68_s18 | Shorten the translation to at most 5 characters so it fits the original box (the current translation of 8 characters overflows its box; the minimum allowed size is 55%) | 块。 | erasers. |
| error | 72 | p71_s0 | Shorten the translation to at most 15 characters so it fits the original box (the current translation of 18 characters overflows its box; the minimum allowed size is 55%) | 小熊开店 | Little Bear's Shop |
| error | 72 | p71_s0 | Shorten the translation to at most 15 characters so it fits the original box (the current translation of 18 characters overflows its box; the minimum allowed size is 55%) | 小熊开店 | Little Bear's Shop |
| error | 74 | p73_s13 | Shorten the translation to at most 16 characters so it fits the original box (the current translation of 34 characters overflows its box; the minimum allowed size is 55%) | 倍。 | times as tall as the green pepper. |
| error | 74 | p73_s13 | Shorten the translation to at most 16 characters so it fits the original box (the current translation of 34 characters overflows its box; the minimum allowed size is 55%) | 倍。 | times as tall as the green pepper. |
| error | 74 | p73_s18 | Shorten the translation to at most 10 characters so it fits the original box (the current translation of 12 characters overflows its box; the minimum allowed size is 55%) | 的(4) | number × (4) |
| error | 74 | p73_s18 | Shorten the translation to at most 10 characters so it fits the original box (the current translation of 12 characters overflows its box; the minimum allowed size is 55%) | 的(4) | number × (4) |
| error | 74 | p73_s21 | Shorten the translation to at most 13 characters so it fits the original box (the current translation of 34 characters overflows its box; the minimum allowed size is 55%) | 倍。 | times as tall as the green pepper. |
| error | 74 | p73_s21 | Shorten the translation to at most 13 characters so it fits the original box (the current translation of 34 characters overflows its box; the minimum allowed size is 55%) | 倍。 | times as tall as the green pepper. |
| error | 74 | p73_s23 | Shorten the translation to at most 17 characters so it fits the original box (the current translation of 34 characters overflows its box; the minimum allowed size is 55%) | 倍。 | times as tall as the green pepper. |
| error | 74 | p73_s23 | Shorten the translation to at most 17 characters so it fits the original box (the current translation of 34 characters overflows its box; the minimum allowed size is 55%) | 倍。 | times as tall as the green pepper. |
| error | 75 | p74_s26 | Shorten the translation to at most 17 characters so it fits the original box (the current translation of 34 characters overflows its box; the minimum allowed size is 55%) | 倍。 | times as tall as the green pepper. |
| error | 75 | p74_s26 | Shorten the translation to at most 17 characters so it fits the original box (the current translation of 34 characters overflows its box; the minimum allowed size is 55%) | 倍。 | times as tall as the green pepper. |
| error | 75 | p74_s28 | Shorten the translation to at most 25 characters so it fits the original box (the current translation of 29 characters overflows its box; the minimum allowed size is 55%) | 数是的倍 | number is mouse number × ___. |
| error | 75 | p74_s28 | Shorten the translation to at most 25 characters so it fits the original box (the current translation of 29 characters overflows its box; the minimum allowed size is 55%) | 数是的倍 | number is mouse number × ___. |
| error | 75 | p74_s34 | Shorten the translation to at most 19 characters so it fits the original box (the current translation of 34 characters overflows its box; the minimum allowed size is 55%) | 倍。 | times as tall as the green pepper. |
| error | 75 | p74_s34 | Shorten the translation to at most 19 characters so it fits the original box (the current translation of 34 characters overflows its box; the minimum allowed size is 55%) | 倍。 | times as tall as the green pepper. |
| error | 76 | p75_s12 | Shorten the translation to at most 29 characters so it fits the original box (the current translation of 34 characters overflows its box; the minimum allowed size is 55%) | 倍。 | times as tall as the green pepper. |
| error | 76 | p75_s12 | Shorten the translation to at most 29 characters so it fits the original box (the current translation of 34 characters overflows its box; the minimum allowed size is 55%) | 倍。 | times as tall as the green pepper. |
| error | 76 | p75_s5 | Shorten the translation to at most 16 characters so it fits the original box (the current translation of 34 characters overflows its box; the minimum allowed size is 55%) | 倍。 | times as tall as the green pepper. |
| error | 76 | p75_s5 | Shorten the translation to at most 16 characters so it fits the original box (the current translation of 34 characters overflows its box; the minimum allowed size is 55%) | 倍。 | times as tall as the green pepper. |
| error | 84 | p83_s14 | Shorten the translation to at most 13 characters so it fits the original box (the current translation of 23 characters overflows its box; the minimum allowed size is 55%) | 七七七上 | 4 × 7 = 5 × 7 = 6 × 7 = |
| error | 84 | p83_s14 | Shorten the translation to at most 13 characters so it fits the original box (the current translation of 23 characters overflows its box; the minimum allowed size is 55%) | 七七七上 | 4 × 7 = 5 × 7 = 6 × 7 = |
| error | 86 | p85_s0 | Shorten the translation to at most 10 characters so it fits the original box (the current translation of 12 characters overflows its box; the minimum allowed size is 55%) | 买球 | Buying Balls |
| error | 86 | p85_s0 | Shorten the translation to at most 10 characters so it fits the original box (the current translation of 12 characters overflows its box; the minimum allowed size is 55%) | 买球 | Buying Balls |
| error | 86 | p85_s10 | Shorten the translation to at most 13 characters so it fits the original box (the current translation of 15 characters overflows its box; the minimum allowed size is 55%) | 五六 | 5 × 9 = 6 × 9 = |
| error | 86 | p85_s10 | Shorten the translation to at most 13 characters so it fits the original box (the current translation of 15 characters overflows its box; the minimum allowed size is 55%) | 五六 | 5 × 9 = 6 × 9 = |
| error | 86 | p85_s9 | Shorten the translation to at most 6 characters so it fits the original box (the current translation of 7 characters overflows its box; the minimum allowed size is 55%) | 三 | 3 × 9 = |
| error | 86 | p85_s9 | Shorten the translation to at most 6 characters so it fits the original box (the current translation of 7 characters overflows its box; the minimum allowed size is 55%) | 三 | 3 × 9 = |
| error | 88 | p87_s5 | Shorten the translation to at most 16 characters so it fits the original box (the current translation of 21 characters overflows its box; the minimum allowed size is 55%) | 乘数乘数 | Multiplier Multiplier |
| error | 88 | p87_s5 | Shorten the translation to at most 16 characters so it fits the original box (the current translation of 21 characters overflows its box; the minimum allowed size is 55%) | 乘数乘数 | Multiplier Multiplier |
| error | 98 | p97_s13 | Shorten the translation to at most 16 characters so it fits the original box (the current translation of 19 characters overflows its box; the minimum allowed size is 55%) | 3.送信。 | 3. Deliver letters. |
| error | 98 | p97_s13 | Shorten the translation to at most 16 characters so it fits the original box (the current translation of 19 characters overflows its box; the minimum allowed size is 55%) | 3.送信。 | 3. Deliver letters. |
| error | 99 | p98_s4 | Shorten the translation to at most 7 characters so it fits the original box (the current translation of 13 characters overflows its box; the minimum allowed size is 55%) | 54个 | 54 persimmons |
| error | 99 | p98_s4 | Shorten the translation to at most 7 characters so it fits the original box (the current translation of 13 characters overflows its box; the minimum allowed size is 55%) | 54个 | 54 persimmons |
| error | 99 | p98_s5 | Shorten the translation to at most 7 characters so it fits the original box (the current translation of 13 characters overflows its box; the minimum allowed size is 55%) | 54个 | 54 persimmons |
| error | 99 | p98_s5 | Shorten the translation to at most 7 characters so it fits the original box (the current translation of 13 characters overflows its box; the minimum allowed size is 55%) | 54个 | 54 persimmons |
| error | 105 | p104_s12 | Shorten the translation to at most 16 characters so it fits the original box (the current translation of 20 characters overflows its box; the minimum allowed size is 55%) | 少3个。 | 3 fewer than yellow. |
| error | 105 | p104_s12 | Shorten the translation to at most 16 characters so it fits the original box (the current translation of 20 characters overflows its box; the minimum allowed size is 55%) | 少3个。 | 3 fewer than yellow. |
| error | 105 | p104_s17 | Shorten the translation to at most 5 characters so it fits the original box (the current translation of 7 characters overflows its box; the minimum allowed size is 55%) | 爷爷 | Grandpa |
| error | 105 | p104_s17 | Shorten the translation to at most 5 characters so it fits the original box (the current translation of 7 characters overflows its box; the minimum allowed size is 55%) | 爷爷 | Grandpa |
| error | 115 | p114_s9 | Shorten the translation to at most 6 characters so it fits the original box (the current translation of 8 characters overflows its box; the minimum allowed size is 55%) | 赵云 | Zhao Yun |
| error | 115 | p114_s9 | Shorten the translation to at most 6 characters so it fits the original box (the current translation of 8 characters overflows its box; the minimum allowed size is 55%) | 赵云 | Zhao Yun |
| warning | 15 | p14_s16 | The translation overflows its box and was rendered at 37% of the original size; even a much shorter text would not fit, check this box in the preview | 元 | yuan. |
| warning | 15 | p14_s16 | The translation overflows its box and was rendered at 37% of the original size; even a much shorter text would not fit, check this box in the preview | 元 | yuan. |
| warning | 15 | p14_s18 | The translation overflows its box and was rendered at 39% of the original size; even a much shorter text would not fit, check this box in the preview | 元 | yuan. |
| warning | 15 | p14_s18 | The translation overflows its box and was rendered at 39% of the original size; even a much shorter text would not fit, check this box in the preview | 元 | yuan. |
| warning | 15 | p14_s19 | The translation overflows its box and was rendered at 47% of the original size; even a much shorter text would not fit, check this box in the preview | 角 | jiao |
| warning | 15 | p14_s19 | The translation overflows its box and was rendered at 47% of the original size; even a much shorter text would not fit, check this box in the preview | 角 | jiao |
| warning | 17 | p16_s17 | The translation overflows its box and was rendered at 46% of the original size; even a much shorter text would not fit, check this box in the preview | 张 | note |
| warning | 17 | p16_s17 | The translation overflows its box and was rendered at 46% of the original size; even a much shorter text would not fit, check this box in the preview | 张 | note |
| warning | 17 | p16_s20 | The translation overflows its box and was rendered at 54% of the original size; even a much shorter text would not fit, check this box in the preview | 张 | note |
| warning | 17 | p16_s20 | The translation overflows its box and was rendered at 54% of the original size; even a much shorter text would not fit, check this box in the preview | 张 | note |
| warning | 34 | p33_s15 | The translation overflows its box and was rendered at 17% of the original size; even a much shorter text would not fit, check this box in the preview | 五五六七八 | 4 × 5 = 5 × 5 = 5 × 6 = 5 × 7 = 5 × 8 = |
| warning | 34 | p33_s15 | The translation overflows its box and was rendered at 17% of the original size; even a much shorter text would not fit, check this box in the preview | 五五六七八 | 4 × 5 = 5 × 5 = 5 × 6 = 5 × 7 = 5 × 8 = |
| warning | 40 | p39_s10 | The translation overflows its box and was rendered at 49% of the original size; even a much shorter text would not fit, check this box in the preview | 三五 | 3×5= |
| warning | 40 | p39_s10 | The translation overflows its box and was rendered at 49% of the original size; even a much shorter text would not fit, check this box in the preview | 三五 | 3×5= |
| warning | 51 | p50_s27 | The translation overflows its box and was rendered at 18% of the original size; even a much shorter text would not fit, check this box in the preview | 兵 | Soldier |
| warning | 51 | p50_s27 | The translation overflows its box and was rendered at 18% of the original size; even a much shorter text would not fit, check this box in the preview | 兵 | Soldier |
| warning | 51 | p50_s29 | The translation overflows its box and was rendered at 42% of the original size; even a much shorter text would not fit, check this box in the preview | 兵 | Soldier |
| warning | 51 | p50_s29 | The translation overflows its box and was rendered at 42% of the original size; even a much shorter text would not fit, check this box in the preview | 兵 | Soldier |
| warning | 74 | p73_s2 | The translation overflows its box and was rendered at 38% of the original size; even a much shorter text would not fit, check this box in the preview | 有 | Zebras: |
| warning | 74 | p73_s2 | The translation overflows its box and was rendered at 38% of the original size; even a much shorter text would not fit, check this box in the preview | 有 | Zebras: |
| warning | 74 | p73_s4 | The translation overflows its box and was rendered at 41% of the original size; even a much shorter text would not fit, check this box in the preview | 有 | Zebras: |
| warning | 74 | p73_s4 | The translation overflows its box and was rendered at 41% of the original size; even a much shorter text would not fit, check this box in the preview | 有 | Zebras: |
| warning | 74 | p73_s5 | The translation overflows its box and was rendered at 16% of the original size; even a much shorter text would not fit, check this box in the preview | 有 | Zebras: |
| warning | 74 | p73_s5 | The translation overflows its box and was rendered at 16% of the original size; even a much shorter text would not fit, check this box in the preview | 有 | Zebras: |
| warning | 74 | p73_s6 | The translation overflows its box and was rendered at 31% of the original size; even a much shorter text would not fit, check this box in the preview | 有 | Zebras: |
| warning | 74 | p73_s6 | The translation overflows its box and was rendered at 31% of the original size; even a much shorter text would not fit, check this box in the preview | 有 | Zebras: |
| warning | 74 | p73_s8 | The translation overflows its box and was rendered at 27% of the original size; even a much shorter text would not fit, check this box in the preview | 有 | Zebras: |
| warning | 74 | p73_s8 | The translation overflows its box and was rendered at 27% of the original size; even a much shorter text would not fit, check this box in the preview | 有 | Zebras: |
| warning | 82 | p81_s4 | The translation overflows its box and was rendered at 3% of the original size; even a much shorter text would not fit, check this box in the preview | 8.1 80801818层8x81 | 8.1 80801818 8x81 |
| warning | 82 | p81_s4 | The translation overflows its box and was rendered at 3% of the original size; even a much shorter text would not fit, check this box in the preview | 8.1 80801818层8x81 | 8.1 80801818 8x81 |
| warning | 86 | p85_s8 | The translation overflows its box and was rendered at 36% of the original size; even a much shorter text would not fit, check this box in the preview | 四 | 4 × 9 = |
| warning | 86 | p85_s8 | The translation overflows its box and was rendered at 36% of the original size; even a much shorter text would not fit, check this box in the preview | 四 | 4 × 9 = |
| warning | 94 | p93_s6 | The translation overflows its box and was rendered at 37% of the original size; even a much shorter text would not fit, check this box in the preview | 房 | House |
| warning | 94 | p93_s6 | The translation overflows its box and was rendered at 37% of the original size; even a much shorter text would not fit, check this box in the preview | 房 | House |
| warning | 94 | p93_s7 | The translation overflows its box and was rendered at 33% of the original size; even a much shorter text would not fit, check this box in the preview | 间 | houses |
| warning | 94 | p93_s7 | The translation overflows its box and was rendered at 33% of the original size; even a much shorter text would not fit, check this box in the preview | 间 | houses |
| warning | 111 | p110_s48 | The translation overflows its box and was rendered at 44% of the original size; even a much shorter text would not fit, check this box in the preview | 角 | jiao |
| warning | 111 | p110_s48 | The translation overflows its box and was rendered at 44% of the original size; even a much shorter text would not fit, check this box in the preview | 角 | jiao |
| warning | 111 | p110_s50 | The translation overflows its box and was rendered at 47% of the original size; even a much shorter text would not fit, check this box in the preview | 角 | jiao |
| warning | 111 | p110_s50 | The translation overflows its box and was rendered at 47% of the original size; even a much shorter text would not fit, check this box in the preview | 角 | jiao |
| warning | 111 | p110_s52 | The translation overflows its box and was rendered at 47% of the original size; even a much shorter text would not fit, check this box in the preview | 角 | jiao |
| warning | 111 | p110_s52 | The translation overflows its box and was rendered at 47% of the original size; even a much shorter text would not fit, check this box in the preview | 角 | jiao |
| warning | 111 | p110_s54 | The translation overflows its box and was rendered at 48% of the original size; even a much shorter text would not fit, check this box in the preview | 角 | jiao |
| warning | 111 | p110_s54 | The translation overflows its box and was rendered at 48% of the original size; even a much shorter text would not fit, check this box in the preview | 角 | jiao |
| warning | 111 | p110_s9 | The translation overflows its box and was rendered at 53% of the original size; even a much shorter text would not fit, check this box in the preview | 中国 | China |
| warning | 111 | p110_s9 | The translation overflows its box and was rendered at 53% of the original size; even a much shorter text would not fit, check this box in the preview | 中国 | China |
| warning | 115 | p114_s4 | The translation overflows its box and was rendered at 33% of the original size; even a much shorter text would not fit, check this box in the preview | 兵 | Soldier |
| warning | 115 | p114_s4 | The translation overflows its box and was rendered at 33% of the original size; even a much shorter text would not fit, check this box in the preview | 兵 | Soldier |

### `llm_review` — 69 errors, 57 warnings

| Severity | Page | Segment | Message | Source | Translation |
|---|---|---|---|---|---|
| error | 5 | p4_s6 | Reviewer (untranslated): The stray Chinese character '产' is left untranslated/unresolved. | 产 | 产 |
| error | 7 | p6_s27 | Reviewer (number): The label "2000年" means the year 2000; dropping 年 removes the year marker. Suggested translation: "2000" | 2000年 | 2000 |
| error | 7 | p6_s29 | Reviewer (number): The label "2004年" means the year 2004; dropping 年 removes the year marker. Suggested translation: "2004" | 2004年 | 2004 |
| error | 7 | p6_s30 | Reviewer (number): The label "2008年" means the year 2008; dropping 年 removes the year marker. Suggested translation: "2008" | 2008年 | 2008 |
| error | 7 | p6_s32 | Reviewer (number): The label "2012年" means the year 2012; dropping 年 removes the year marker. Suggested translation: "2012" | 2012年 | 2012 |
| error | 10 | p9_s11 | Reviewer (number): The source uses the Chinese dash 一 as a placeholder for the answer; the translation replaced it with an invented blank "____", which is not in the source. Suggested translation: "Answer: The choir now has 一 people." | 答：合唱队现在有—人。 | Answer: The choir now has ____ people. |
| error | 12 | p11_s2 | Reviewer (meaning): The source says 彩笔帽 (marker/crayon caps), and the sentence ends with an exclamation mark; "made of marker pen caps" changes the material to the pens themselves rather than their caps. Suggested translation: "This butterfly is made of marker caps!" | 这只蝴蝶是用彩笔帽做成的。！ | This butterfly is made of marker pen caps! |
| error | 13 | p12_s13 | Reviewer (number): '第一小队' is 'the first team'; 'First team' is missing the ordinal 'the'. Suggested translation: "The first team" | 第一小队 | First team |
| error | 13 | p12_s14 | Reviewer (number): '第二小队' is 'the second team'; 'Second team' is missing 'the'. Suggested translation: "The second team" | 第二小队 | Second team |
| error | 13 | p12_s15 | Reviewer (number): '第三小队' is 'the third team'; 'Third team' is missing 'the'. Suggested translation: "The third team" | 第三小队 | Third team |
| error | 14 | p13_s15 | Reviewer (untranslated): The unit label '角' should be given as yuan amount or the unit as a word; 'jiao' is acceptable as a unit word but the source is a bare unit label and should follow the money convention. Suggested translation: "jiao" | 角 | jiao |
| error | 14 | p13_s17 | Reviewer (untranslated): Bare '角' unit label should be handled like the previous unit label; keeping 'jiao' is a free choice but inconsistent with the yuan convention for amounts. Suggested translation: "jiao" | 角 | jiao |
| error | 14 | p13_s19 | Reviewer (number): '1角=—' should use the money convention: ¥0.1 = —. Suggested translation: "¥0.1 = —" | 1角=— | 1 jiao = — |
| error | 14 | p13_s26 | Reviewer (terminology): '伍角' is the formal numeral '5 jiao'; the translation should match the value used elsewhere, ¥0.5. Suggested translation: "¥0.5" | 伍角 | 5 jiao |
| error | 14 | p13_s29 | Reviewer (terminology): '贰角' is the formal numeral '2 jiao'; should be ¥0.2 following money convention. Suggested translation: "¥0.2" | 贰角 | 2 jiao |
| error | 22 | p21_s10 | Reviewer (terminology): "Adding 2 4 times" is awkward wording; "Adding four 2s" is clearer. Suggested translation: "Adding four 2s can also be written as multiplication." | 4个2相加，也可以用乘法表示。 | Adding 2 4 times can also be written as multiplication. |
| error | 23 | p22_s7 | Reviewer (omission): The phrase '看图' (look at the picture) is omitted; source is '看图列出乘法算式'. Suggested translation: "2. Look at the picture and list the multiplication number sentences." | 2.看图列出乘法算式 | 2. Look at the picture and write multiplication number sent… |
| error | 27 | p26_s11 | Reviewer (terminology): '5个3' is better rendered as '5 threes' or '5 groups of 3' rather than '5 3s'. Suggested translation: "5 threes" | 5个3 | 5 3s |
| error | 27 | p26_s19 | Reviewer (terminology): '3个5' is better rendered as '3 fives' or '3 groups of 5' rather than '3 5s'. Suggested translation: "3 fives" | 3个5 | 3 5s |
| error | 27 | p26_s8 | Reviewer (terminology): '2个3' is better rendered as '2 threes' or '2 groups of 3' rather than '2 3s'. Suggested translation: "2 threes" | 2个3 | 2 3s |
| error | 27 | p26_s9 | Reviewer (terminology): '4个6' is better rendered as '4 sixes' or '4 groups of 6' rather than '4 6s'. Suggested translation: "4 sixes" | 4个6 | 4 6s |
| error | 34 | p33_s20 | Reviewer (number): The source "三五九" is an incomplete rhyme (3 × 5 = 9 is wrong; the exercise is to fill in the blank), but the translation writes "3 × 5 = ____", which is correct for an fill-in, yet the source shows 九 not a blank. If the source intends 三五____, the blank is right; otherwise 九 should appear. Suggested translation: "3 × 5 = ____" | 三五九 | 3 × 5 = ____ |
| error | 44 | p43_s8 | Reviewer (number): The source has a dash '—' (blank to fill in), not the numeral 1; the translation wrongly states '1 kittens'. Suggested translation: "Answer: There are ______ kittens on the boat in all." | 答：船上一共有—只小猫。 | Answer: There are 1 kittens on the boat in all. |
| error | 47 | p46_s0 | Reviewer (meaning): 'Find a new home' is a literal rendering; the exercise means matching items to their places (找新家). Suggested translation: "5. Find the new home for each." | 5.找新家。 | 5. Find a new home. |
| error | 50 | p49_s35 | Reviewer (omission): The object of the purchase (1 lamp priced 196.40 yuan) is missing; the amount and the noun were dropped, leaving only the empty placeholder. Suggested translation: "(2) Aunt Li buys 1 lamp for ¥196.40 and pays ¥50. How much change should she get?" | （2）李阿姨买1盏196.40.0，付了50元，应找回多少元？ | (2) Aunt Li buys 1 196.40.0 and pays ¥50. How much change… |
| error | 57 | p56_s7 | Reviewer (number): Duplicate equal sign: "1 m = =100 cm" has an extra "="; the source has only one. Suggested translation: "1 m = 100 cm; the metre can also be written as m." | 1米=100厘米，米可以用m表示。 | 1 m = =100 cm; the metre can also be written as m. |
| error | 57 | p56_s7 | Reviewer (terminology): "metre" should follow consistent spelling; acceptable, but 米 as unit may be better as "m". Minor. Suggested translation: "1 m = 100 cm; the metre can also be written as m." | 1米=100厘米，米可以用m表示。 | 1 m = =100 cm; the metre can also be written as m. |
| error | 58 | p57_s1 | Reviewer (meaning): Source asks "how tall are Xiaoming and Clever Dog respectively"; "respectively" omitted. Suggested translation: "Estimate: how tall are Xiaoming and Clever Dog respectively?" | 估一估，小明和机灵狗分别有多高？ | Estimate: how tall are Xiaoming and Clever Dog? |
| error | 58 | p57_s27 | Reviewer (number): The garbled digits '228.35.0' from the source are kept; the intended length should be 7 cm as in the cleaned source. Suggested translation: "7 cm" | 228.35.07厘米 | 228.35.07 cm |
| error | 61 | p60_s2 | Reviewer (omission): Omission of 量一量 (Measure) — the source lists three actions (做一做, 量一量), but only "Do it and measure" is given, dropping the quantifying action which belongs to a different unit. Suggested translation: "5. Do it and measure." | 5.做一做，量一量。 | 5. Do it and measure. |
| error | 65 | p64_s11 | Reviewer (meaning): Source says 圈一圈，算一算 ('Circle and calculate'); the translation has '算二算' rendered correctly but the source text itself is 算一算 — more importantly the meaning is fine; however the source's repeated 算 is rendered as 'calculate', which matches. This item is actually correct except '算二算' is a typo in the source, not the translation. No change needed. | 3.圈一圈，算二算。 | 3. Circle and calculate. |
| error | 68 | p67_s7 | Reviewer (meaning): The source gives the measure word 根 (for bananas) without naming bananas in parentheses; the context here is sticks/bamboo, and the translation invents "bananas". Suggested translation: "6" | 6（根） | 6 (bananas) |
| error | 72 | p71_s13 | Reviewer (meaning): The measure word 辆 is the counted noun (cars); it refers to the vehicles being bought, which is correct, but nothing determines that it should be 'cars' rather than the object sold—however the source only says '辆' and the translation supplies the counted noun, which is acceptable per the measure-word rule. No issue. | 辆 | cars |
| error | 73 | p72_s10 | Reviewer (number): '4棵。' means '4 trees.' — '棵' (the counted noun) was dropped, leaving only '4.' Suggested translation: "4 trees." | 4棵。 | 4. |
| error | 73 | p72_s16 | Reviewer (number): The rhyme 四九三十六 means 4 × 9 = 36; the translation is correct. No issue. | 四九三十六 | 4 × 9 = 36 |
| error | 75 | p74_s18 | Reviewer (omission): The answer blank after "spent" is omitted; the source leaves a blank for the amount. Suggested translation: "Answer: The fox spent ___" | 答：狐狸花了 | Answer: The fox spent |
| error | 75 | p74_s3 | Reviewer (meaning): '文具店' means 'Stationery Store'; 'Stationery' alone drops the noun. Suggested translation: "Stationery Store" | 文具店 | Stationery |
| error | 76 | p75_s21 | Reviewer (terminology): "大客车" is labeled "Large coach" at p75_s18 but rendered "The bus" here; inconsistent terminology. Suggested translation: "(1) The large coach has" | (1）大客车上有 | (1) The bus has |
| error | 79 | p78_s26 | Reviewer (meaning): 椰树 means "coconut tree" (marginal); "coconut palm" is acceptable but uses a more specialized term than the source. | 椰树 | Coconut palm |
| error | 92 | p91_s14 | Reviewer (omission): The source phrase '双臂平伸的长度身高' is a label pairing arm span length with height; the translation drops the connective relationship and reads as two separate items. Also should be 'Arm span length and height' or 'Arm span and height'—the meaning 'length of arms stretched out and height' is not fully captured because '双臂平伸的长度' = 'length of arms stretched out'. Suggested translation: "Arm span and height" | 双臂平伸的长度身高 | Arm span and height |
| error | 93 | p92_s10 | Reviewer (meaning): '卷尺测' means 'measure with a tape measure', not just 'Tape measure'. The translation omits the measurement action. Suggested translation: "Measure with a tape measure" | 卷尺测 | Tape measure |
| error | 93 | p92_s11 | Reviewer (meaning): '一宽' in vertical text label likely means 'one width' as a measurement label; translation '1 width' changes the numeral style but meaning is fine. However if source is part of '一宽' meaning 'width', translation okay. Keep as is. Suggested translation: "Width" | 一宽 | 1 width |
| error | 93 | p92_s3 | Reviewer (terminology): Glossary pairs '读一读' => 'Read'; '讲一讲' is rendered 'tell'. 'Read and tell' is acceptable but 'Read and talk' aligns with classroom instructions. Minor. Suggested translation: "Read and talk" | 读一读，讲一讲 | Read and tell |
| error | 93 | p92_s9 | Reviewer (meaning): '步测' means 'measure by pacing/step measurement', not 'Step'. The translation 'Step' loses the measurement meaning. Suggested translation: "Measure by pacing" | 步测 | Step |
| error | 94 | p93_s1 | Reviewer (terminology): Little birds vs birds; source '小鸟' = 'little birds'. Translation 'Birds' drops 'little'. Minor. Suggested translation: "Giraffe and Little Birds" | 长颈鹿与小鸟 | Giraffe and Birds |
| error | 94 | p93_s13 | Reviewer (omission): The source has a blank/answer space '要准备间房子' where '间' is the measure word with a blank before it; translation 'prepare ___ houses' adds a blank not in the source. The source has no underscore, the blank is implied by '间'. According to conventions, keep blanks exactly; this adds a blank. Also 'Answer: prepare houses.' should be 'Answer: prepare ___ houses.' if blank intended, but source shows no blank marker. The translation added '___'. Suggested translation: "Answer: prepare houses." | 答：要准备间房子。 | Answer: prepare ___ houses. |
| error | 94 | p93_s19 | Reviewer (terminology): Glossary: '算式' => 'number sentence'. Translation uses 'number sentence'—correct. | 怎么列式呢？ | How do we write the number sentence? |
| error | 94 | p93_s7 | Reviewer (terminology): Source '间' is a measure word for houses/rooms, here label for 'houses'. Translation 'houses' is fine but the label likely corresponds to the unit 'house'. Acceptable. | 间 | houses |
| error | 95 | p94_s0 | Reviewer (terminology): '试一试' = 'Try It' is acceptable; no glossary entry. Minor. | 试一试 | Try It |
| error | 95 | p94_s14 | Reviewer (terminology): Source '还剩下几根萝卜' = 'how many carrots are left'; translation correct. | 运走2篮，还剩下几根萝卜？ | After taking away 2 baskets, how many carrots are left? |
| error | 95 | p94_s17 | Reviewer (meaning): Source '搬4盆' = 'carry 4 pots'; translation 'carries 4 pots' fine. | （1）如果每人搬4盆，需要多少人？ | (1) If each person carries 4 pots, how many people are need… |
| error | 95 | p94_s18 | Reviewer (meaning): '平均每人搬几盆' = 'how many pots does each person carry on average'; translation correct. | （2）现在有6名同学，平均每人搬几盆？ | (2) There are 6 students now. How many pots does each perso… |
| error | 96 | p95_s2 | Reviewer (untranslated): Source '好好' is a name (Hao Hao) but appears as heading. Translation 'Hao Hao' is awkward; should be 'Haohao' per pinyin convention for children's names (e.g., Taoqi, Xiaoxiao). Suggested translation: "Haohao" | 好好 | Hao Hao |
| error | 97 | p96_s2 | Reviewer (meaning): Source '我身高7厘米' = 'I am 7 cm tall.' Translation correct. Note: likely a small animal, but translation fine. | 我身高7厘米 | I am 7 cm tall. |
| error | 97 | p96_s3 | Reviewer (number): Source mentions 4 pumpkins per basket (每筐能装4个南瓜); the translation omits the verb 能装 and renders it as 'holds 4 pumpkins', dropping the capacity nuance, but more importantly it omits 摘了54个柿子 context. Actually the main issue: 'Each basket holds 4 pumpkins' loses 'can hold' (能装). Suggested translation: "Each basket can hold 4 pumpkins..." | 每筐能装4个南瓜··· | Each basket holds 4 pumpkins... |
| error | 97 | p96_s6 | Reviewer (omission): Source '6个··' contains the measure word 个 after the number 6; the translation drops it entirely as '6...'. The counted object is unknown here, but the measure word should not simply vanish; per conventions drop only the parentheses form, not this instance. However, since context is a label with an unknown object, keeping '6' is acceptable. No finding. | 6个·· | 6... |
| error | 98 | p97_s14 | Reviewer (untranslated): Source 'cmrar' is a garbled/unclear label; the translation copies it verbatim as 'cmrar'. This appears to be a scanning artifact but should be handled as untranslated garbage. | cmrar | cmrar |
| error | 99 | p98_s14 | Reviewer (terminology): Source '全' likely means 'total/all'; translating as 'Total' is acceptable but context is a table label. No finding. | 全 | Total |
| error | 99 | p98_s4 | Reviewer (number): Source '54个' has no object named in this item; the translation adds 'persimmons'. While the broader context names persimmons, inventing the noun here is an addition not present in the source. Suggested translation: "54" | 54个 | 54 persimmons |
| error | 99 | p98_s5 | Reviewer (number): Source '54个' has no object; the translation adds 'persimmons', an addition absent from the source. Suggested translation: "54" | 54个 | 54 persimmons |
| error | 101 | p100_s8 | Reviewer (meaning): '二（1）班' means Grade 2, Class 1; the translation is correct, though 'Class 1, Grade 2' is the more standard English order. Suggested translation: "3. Talk about Class 1, Grade 2." | 3.说说二（1）班的事。 | 3. Talk about Grade 2, Class 1. |
| error | 107 | p106_s3 | Reviewer (number): The source uses a dash placeholder "—" for each blank length (火柴长—厘米，小刀长—厘米), which should be preserved as a blank, not doubled as four underscores. Suggested translation: "The screwdriver is __ cm long, the match is __ cm long, and the knife is __ cm long." | 螺丝刀长厘米，火柴长—厘米，小刀长—厘米。 | The screwdriver is ____ cm long, the match is ____ cm long,… |
| error | 111 | p110_s25 | Reviewer (meaning): The source bank name 中国民职行 appears to be a truncated/possibly misread fragment; translating it as "People's Bank of China" (中国人民银行) adds words not present in the source. | 中国民职行 | People's Bank of China |
| error | 111 | p110_s48 | Reviewer (untranslated): The bare label 角 is left as the romanization "jiao"; the target-language convention for a bare unit label without an amount is the English word. Suggested translation: "jiao" | 角 | jiao |
| error | 111 | p110_s50 | Reviewer (untranslated): The bare label 角 is left as the romanization "jiao"; the target-language convention for a bare unit label without an amount is the English word. Suggested translation: "jiao" | 角 | jiao |
| error | 111 | p110_s52 | Reviewer (untranslated): The bare label 角 is left as the romanization "jiao"; the target-language convention for a bare unit label without an amount is the English word. Suggested translation: "jiao" | 角 | jiao |
| error | 111 | p110_s54 | Reviewer (untranslated): The bare label 角 is left as the romanization "jiao"; the target-language convention for a bare unit label without an amount is the English word. Suggested translation: "jiao" | 角 | jiao |
| error | 111 | p110_s55 | Reviewer (untranslated): The bare label 角 is left as the romanization "jiao"; the target-language convention for a bare unit label without an amount is the English word. Suggested translation: "jiao" | 角 | jiao |
| error | 111 | p110_s57 | Reviewer (untranslated): The bare label 角 is left as the romanization "jiao"; the target-language convention for a bare unit label without an amount is the English word. Suggested translation: "jiao" | 角 | jiao |
| warning | 1 | p0_s5 | Reviewer (format): Volume label '上册' is conventionally translated 'Volume 1' (or 'Part 1'); 'Volume One' is inconsistent with the digit style used elsewhere. Suggested translation: "Volume 1" | 上册 | Volume One |
| warning | 4 | p3_s6 | Reviewer (format): Money '1元' should be written ¥1. Suggested translation: "¥1" | 1元 | 1 yuan |
| warning | 5 | p4_s10 | Reviewer (format): Money '6元' should be written ¥6. Suggested translation: "¥6 each" | 每个6元 | Each costs 6 yuan |
| warning | 6 | p5_s3 | Reviewer (format): Two names run together without separation; a separator or line break preserves the table layout. Suggested translation: "Taoqi · Xiaoxiao" | 淘气笑笑 | Taoqi Xiaoxiao |
| warning | 6 | p5_s8 | Reviewer (grammar): '他们谁说得对？' asks which of them is right, not simply 'Who is right?' Suggested translation: "Which of them is right?" | 他们谁说得对？ | Who is right? |
| warning | 9 | p8_s18 | Reviewer (format): The tally mark 正 in the source is a counting symbol and must be kept exactly as 正; the translation left it as the placeholder ⟦0⟧ only because the source shows 一班32.22.0二班三班四班, but the tally character is missing, and spacing merges the classes into one string. Suggested translation: "Class 1 正 Class 2 Class 3 Class 4" | 一班32.22.0二班三班四班 | Class 1 32.22.0 Class 2 Class 3 Class 4 |
| warning | 9 | p8_s25 | Reviewer (format): Heading should be in Title Case per the conventions. Suggested translation: "Math Game." | 数学游戏。 | Math game. |
| warning | 12 | p11_s3 | Reviewer (grammar): Number agreement: "three kinds of seeds" is acceptable, but the singular "seed" would fit the three-kind construction; check consistency with the following items. Suggested translation: "This owl is made of three kinds of seeds." | 这只猫头鹰是用三种瓜子做成的。 | This owl is made of three kinds of seeds. |
| warning | 13 | p12_s0 | Reviewer (format): Line breaks were lost: the item contains a newline and the translation does not. Suggested translation: "5. Harvesting Corn." | 5.收玉米。 | 5. Harvesting corn. |
| warning | 13 | p12_s20 | Reviewer (format): Table headers were flattened into a comma-separated list; headers should keep their separate labels. Suggested translation: "Name Taoqi Xiaoxiao Qisi" | 姓名淘气笑笑奇思 | Name Taoqi, Xiaoxiao, Qisi |
| warning | 14 | p13_s12 | Reviewer (grammar): '认一认' is the standard heading 'Recognise'; 'recognise' is correct but combined with 'fill in' should be parallel. Suggested translation: "Recognise and Fill In" | 认一认，填一填 | Recognise and fill in |
| warning | 14 | p13_s24 | Reviewer (grammar): Number agreement: '10张' means 10 notes, so it must be '10 notes'. Suggested translation: "10 notes" | 10张 | 10 note |
| warning | 14 | p13_s25 | Reviewer (grammar): Number agreement: '1 note' is fine, but 'note' should be singular; keep as '1 note'. Suggested translation: "1 note" | 1张 | 1 note |
| warning | 14 | p13_s30 | Reviewer (grammar): Number agreement: '3张' means 3 notes, so it must be '3 notes'. Suggested translation: "3 notes" | 3张 | 3 note |
| warning | 16 | p15_s21 | Reviewer (format): Currency amounts should use the ¥ symbol before the number per the convention: 贰角 (0.2 yuan) as ¥0.2. Suggested translation: "¥0.2" | 贰角 | Two jiao |
| warning | 16 | p15_s22 | Reviewer (format): Currency amount should use the ¥ symbol before the number: 伍角 as ¥0.5. Suggested translation: "¥0.5" | 伍角 | Five jiao |
| warning | 17 | p16_s27 | Reviewer (grammar): "Read and tell" is unnatural; "Read and discuss" fits 讲一讲 better. Suggested translation: "5. Read and discuss." | 5.读一读，讲一讲。 | 5. Read and tell. |
| warning | 17 | p16_s6 | Reviewer (format): Money must be written with ¥ before the number: 48元 => ¥48. Suggested translation: "¥48" | 48元 | 48 yuan |
| warning | 18 | p17_s7 | Reviewer (grammar): "bought 1 boxes" should be "bought 1 box". Suggested translation: "bought 1 box" | 买了1盒 | bought 1 boxes |
| warning | 20 | p19_s0 | Reviewer (format): Heading uses Title Case correctly; "Unit 3 Counting and Multiplication" is correct. | 三数一数与乘法 | Unit 3 Counting and Multiplication |
| warning | 22 | p21_s6 | Reviewer (format): "(people)" acceptable per measure word convention. | 2+2+2+2=8（人） | 2+2+2+2=8 (people) |
| warning | 24 | p23_s0 | Reviewer (format): Headings should be in Title Case: 'How Many Dots' is correct. No issue. | 有多少点子 | How Many Dots |
| warning | 25 | p24_s4 | Reviewer (format): The source '2.我说你摆' is an activity title; '2. I say, you arrange' is acceptable. No issue. | 2.我说你摆 | 2. I say, you arrange |
| warning | 25 | p24_s6 | Reviewer (format): 'I arrange 5 rows and 3 columns' — the source '我摆5行3列' is fine; no issue. | 我摆5行3列 | I arrange 5 rows and 3 columns |
| warning | 26 | p25_s0 | Reviewer (format): Headings should be in Title Case: 'Animal Party' is correct. No issue. | 动物聚会 | Animal Party |
| warning | 26 | p25_s11 | Reviewer (format): Money format is correct per convention: ¥6. No issue. | 6元 | ¥6 |
| warning | 26 | p25_s12 | Reviewer (format): Money format is correct per convention: ¥6. No issue. | 6元 | ¥6 |
| warning | 26 | p25_s13 | Reviewer (format): Money format is correct per convention: ¥6. No issue. | 6元 | ¥6 |
| warning | 26 | p25_s9 | Reviewer (format): The sentence 'Look and talk about it. What number sentences can you think of?' combines two clauses; the source '看一看说一说，你能想到哪些算式？' is one sentence. Minor. Suggested translation: "Look and talk about it. What number sentences can you think of?" | 看一看说一说，你能想到哪些算式？ | Look and talk about it. What number sentences can you think… |
| warning | 27 | p26_s24 | Reviewer (format): The source uses a full-width closing parenthesis '(2）'; the translation uses '(2)'. Not a meaning issue. Suggested translation: "(2) Please ask another math question and try to answer it." | (2）请你再提出一个数学问题，并尝试解答。 | (2) Please ask another math question and try to answer it. |
| warning | 35 | p34_s7 | Reviewer (grammar): "两人一组试一试" is an instruction to try in pairs; "Try it in pairs." is acceptable but "Try it in groups of two." is closer. Suggested translation: "Try it in groups of two." | 两人一组试一试。 | Try it in pairs. |
| warning | 42 | p41_s0 | Reviewer (format): 'Bear's Treat' is acceptable as a title, but the source names the character as '小熊' (Little Bear); keeping it as a title-cased heading is fine. No change to meaning. Suggested translation: "Bear's Treat" | 小熊请客 | Bear's Treat |
| warning | 44 | p43_s4 | Reviewer (grammar): "Calculate" stands alone awkwardly; a textbook would echo the source phrase 'calculate it'. Suggested translation: "How many kittens are there on the boat in all? Talk about it and calculate it." | 船上一共有多少只小猫？说一说，算一算。 | How many kittens are there on the boat in all? Talk about i… |
| warning | 44 | p43_s9 | Reviewer (grammar): Comma after the opening phrase reads better in a textbook than a period. Suggested translation: "Talk about it: what problem can the number sentence 2×6=12 solve?" | 说一说，算式2×6=12可以解决什么问题？ | Talk about it. What problem can the number sentence 2×6=12 … |
| warning | 48 | p47_s4 | Reviewer (format): Inconsistent class numbering: should read 'Class 2, Grade 2' like the neighbouring items. Suggested translation: "Class 2, Grade 2" | 二(2）班 | Class (2), Grade 2 |
| warning | 50 | p49_s1 | Reviewer (format): Heading/title should be in Title Case. Suggested translation: "1. Family Jump Rope Contest" | 1.家庭跳绳比赛 | 1. Family jump rope contest |
| warning | 54 | p53_s14 | Reviewer (grammar): The wording "about how many of their own head-lengths tall is each" is awkward; a textbook should phrase it more naturally. Suggested translation: "Estimate: about how many head-lengths tall is each of the two people below?" | 估一估，下面两个人的身高分别大约是各自的几个头长？ | Estimate: about how many of their own head-lengths tall is … |
| warning | 55 | p54_s12 | Reviewer (format): The Chinese ellipsis "···" is rendered as "..."; the trailing ellipsis style is inconsistent but does not change meaning. Suggested translation: "Usually, when measuring the length of an object, put one end at the 0 mark on the ruler…" | 通常，测量物体的长度时，要把一端对准尺子的0刻度··· | Usually, when measuring the length of an object, put one en… |
| warning | 55 | p54_s2 | Reviewer (grammar): "6 handspans long" renders 推 (handspan) but is acceptable wording; however 推 is a handspan measure word - fine. No change needed. | 课桌有6推长。 | The desk is 6 handspans long. |
| warning | 57 | p56_s5 | Reviewer (format): Source uses "..·" ellipsis; rendering as "..." is fine but the stray period in source. No change needed. | 该摆第14根了.·· | It is time to place the 14th stick... |
| warning | 58 | p57_s3 | Reviewer (format): Answer blank （） rendered as half-width "()". Suggested translation: "About （）cm tall" | 高约（）厘米 | About () cm tall |
| warning | 58 | p57_s5 | Reviewer (format): Answer blank （） rendered as half-width "()". Suggested translation: "About （）cm tall" | 高约（）厘米 | About () cm tall |
| warning | 62 | p61_s0 | Reviewer (format): The unit heading should be in Title Case; "Sharing and Division" is correct, but the bare Chinese numeral should map to "Unit 7" consistently (it does), so no change needed beyond noting format. Suggested translation: "Unit 7 Sharing and Division" | 七分一分与除法 | Unit 7 Sharing and Division |
| warning | 85 | p84_s23 | Reviewer (wording): The translation omits 在炼丹炉中 (in the alchemy furnace), changing the story detail. Suggested translation: "Sun Wukong spent 49 days in the alchemy furnace and gained his fiery golden eyes" | 孙悟空在炼丹炉中经过七七四十九天，炼成火眼金睛 | Sun Wukong spent 49 days in the alchemy furnace and gained … |
| warning | 93 | p92_s2 | Reviewer (format): The source label '我发现·' uses a Chinese ellipsis dot '·'; translation keeps a Latin middle dot. Minor format inconsistency, but acceptable. Suggested translation: "I find..." | 我发现· | I find · |
| warning | 93 | p92_s5 | Reviewer (grammar): The translation changes the structure slightly but keeps meaning; '数一数走了多少步' = 'count how many steps I take', fine. No error. | 我每步长约50厘米，上学时，数一数走了多少步，就能估计出我从家到学校有多远。我的身高是130厘米，如果我 | Each of my steps is about 50 cm long. When going to school,… |
| warning | 94 | p93_s14 | Reviewer (grammar): Source '造了几间房子' is a question 'How many houses did it build?' Translation adds 'The giraffe used 63 small wooden boards to build several houses.' which changes '几' from question to 'several'. Meaning altered. Suggested translation: "How many houses did the giraffe build with 63 small wooden boards?" | 长颈鹿用63块小木板造了几间房子？ | The giraffe used 63 small wooden boards to build several ho… |
| warning | 100 | p99_s12 | Reviewer (format): Spelling 'Colour' is British English; the rest of the material appears to use American English (e.g., 'colors'), so casing/variant should be consistent. Suggested translation: "7. Color." | 7.涂一涂。 | 7. Colour. |
| warning | 100 | p99_s16 | Reviewer (format): British spelling 'Colour' inconsistent with American English used elsewhere. Suggested translation: "Color the squares of the numbers they land on in different colors." | 分别把它们跳到的数所在的格子涂上不同的颜色。 | Colour the squares of the numbers they land on in different… |
| warning | 100 | p99_s2 | Reviewer (grammar): Imperative 'Buy' is acceptable but the sentence is a stated plan; a more natural textbook rendering would use 'I want to buy' or 'Buying' consistent with the surrounding dialogue. | 买6根跳绳和5个皮球。 | Buy 6 jump ropes and 5 balls. |
| warning | 101 | p100_s23 | Reviewer (grammar): '还可以' means 'There is also...' / 'Another way is...'; the bare 'Also' is incomplete and unnatural. Suggested translation: "There is also" | 还可以 | Also |
| warning | 101 | p100_s7 | Reviewer (format): Multiplication and division expressions should use the multiplication/division signs as in the source; using '×' and '÷' is fine, but note the source uses '8×7' and '35÷5'. No change needed; flagging only for consistency. | 2.说一说，画一画。8×7可以解决什么问题？35÷5呢？ | 2. Talk about it and draw a picture. What problems can 8×7 … |
| warning | 101 | p100_s9 | Reviewer (grammar): Comma splice: 'There are 40 students in the class, 22 are boys.' Should be joined with 'and' or a semicolon. Suggested translation: "There are 40 students in the class, and 22 are boys. How many are girls? Divide the girls equally into 6 groups. How many are in each group?" | 全班有40人，男生有22人，女生有多少人？把女生平均分成6个小组，每个小组有多少人？ | There are 40 students in the class, 22 are boys. How many a… |
| warning | 102 | p101_s11 | Reviewer (grammar): 'The nail of my thumb' does not convey that the nail itself has a length; English says 'my thumbnail'. Suggested translation: "My thumbnail is about 1 cm long." | 我拇指的指甲盖长度大约是1厘米。 | The nail of my thumb is about 1 cm long. |
| warning | 102 | p101_s6 | Reviewer (grammar): Word order is awkward; 'How long is each object below in centimeters?' is more natural textbook English. Suggested translation: "2. How long is each object below in centimeters?" | 2.下面物体的长各是多少厘米？ | 2. How many centimeters long is each object below? |
| warning | 104 | p103_s24 | Reviewer (format): The placeholder-like digit string '412.32.0' is kept, but the question mark should follow a space consistent with other label items; otherwise unchanged. Suggested translation: "412.32.0?" | 412.32.0吗？ | 412.32.0? |
| warning | 107 | p106_s10 | Reviewer (grammar): "实际估一估" means estimate in real life in the classroom; "estimate the actual heights" slightly shifts the meaning. Suggested translation: "In the classroom, estimate the real heights." | 在教室里，实际估一估。 | In the classroom, estimate the actual heights. |

### `numbers` — 20 errors, 0 warnings

| Severity | Page | Segment | Message | Source | Translation |
|---|---|---|---|---|---|
| error | 3 | p2_s5 | Number "5" from the source is missing in the translation; keep every number exactly as written in the source | 石广泉水一瓶1 元5角 | Mineral water ¥1.50 a bottle |
| error | 4 | p3_s2 | Number "5" from the source is missing in the translation; keep every number exactly as written in the source | 2元5角 | ¥2.50 |
| error | 4 | p3_s7 | Number "5" from the source is missing in the translation; keep every number exactly as written in the source | 5 角 | ¥0.50 |
| error | 14 | p13_s11 | Number "8" from the source is missing in the translation; keep every number exactly as written in the source | 9元8角 | ¥9.80 |
| error | 14 | p13_s3 | Number "1" from the source is missing in the translation; keep every number exactly as written in the source | 1角 | ¥0.10 |
| error | 14 | p13_s4 | Number "8" from the source is missing in the translation; keep every number exactly as written in the source | 8角 | ¥0.80 |
| error | 14 | p13_s5 | Number "5" from the source is missing in the translation; keep every number exactly as written in the source | 5角 | ¥0.50 |
| error | 14 | p13_s6 | Number "2" from the source is missing in the translation; keep every number exactly as written in the source | 1元2角 | ¥1.20 |
| error | 14 | p13_s8 | Number "2" from the source is missing in the translation; keep every number exactly as written in the source | 2角 | ¥0.20 |
| error | 14 | p13_s9 | Number "5" from the source is missing in the translation; keep every number exactly as written in the source | 6元5角 | ¥6.50 |
| error | 15 | p14_s41 | Number "5" from the source is missing in the translation; keep every number exactly as written in the source | 1元5角 | ¥1.50 |
| error | 18 | p17_s15 | Number "2" from the source is missing in the translation; keep every number exactly as written in the source | 1元2角 | ¥1.20 |
| error | 18 | p17_s16 | Number "8" from the source is missing in the translation; keep every number exactly as written in the source | 8角 | ¥0.80 |
| error | 18 | p17_s2 | Number "6" from the source is missing in the translation; keep every number exactly as written in the source | 6角 | ¥0.60 |
| error | 19 | p18_s12 | Number "5" from the source is missing in the translation; keep every number exactly as written in the source | 2元5角 | ¥2.50 |
| error | 19 | p18_s15 | Number "5" from the source is missing in the translation; keep every number exactly as written in the source | 1元5角 | ¥1.50 |
| error | 48 | p47_s12 | Number "8" from the source is missing in the translation; keep every number exactly as written in the source | 8角 | ¥0.80 |
| error | 48 | p47_s13 | Number "5" from the source is missing in the translation; keep every number exactly as written in the source | 1元5角 | ¥1.50 |
| error | 48 | p47_s14 | Number "5" from the source is missing in the translation; keep every number exactly as written in the source | 5角 | ¥0.50 |
| error | 101 | p100_s22 | Number "8" from the source is missing in the translation; keep every number exactly as written in the source | 怎样拿出12元8角？ | How can you pay ¥12.80? |

### `untranslated` — 4 errors, 0 warnings

| Severity | Page | Segment | Message | Source | Translation |
|---|---|---|---|---|---|
| error | 5 | p4_s6 | 1 letter(s) of the source script remain untranslated ("产"); translate all text into English | 产 | 产 |
| error | 16 | p15_s7 | 1 letter(s) of the source script remain untranslated ("中"); translate all text into English | 中 | 中 |
| error | 30 | p29_s3 | 1 letter(s) of the source script remain untranslated ("王"); translate all text into English | 王 | 王 |
| error | 31 | p30_s4 | 1 letter(s) of the source script remain untranslated ("中"); translate all text into English | 中 | 中 |

### `image_text` — 0 errors, 4 warnings

| Severity | Page | Segment | Message | Source | Translation |
|---|---|---|---|---|---|
| warning | 19 | p18_i72_13 | The text '比' was left in the source language (inline pictograms the OCR cannot read (left in the picture)): the line is built around symbols or pictures the OCR could not read - check the page in the preview | 比 |  |
| warning | 19 | p18_i72_13 | The text '比' was left in the source language (inline pictograms the OCR cannot read (left in the picture)): the line is built around symbols or pictures the OCR could not read - check the page in the preview | 比 |  |
| warning | 105 | p104_i416_19 | The text '比黄书包' was left in the source language (inline pictograms the OCR cannot read (left in the picture)): the line is built around symbols or pictures the OCR could not read - check the page in the preview | 比黄书包 |  |
| warning | 105 | p104_i416_19 | The text '比黄书包' was left in the source language (inline pictograms the OCR cannot read (left in the picture)): the line is built around symbols or pictures the OCR could not read - check the page in the preview | 比黄书包 |  |
