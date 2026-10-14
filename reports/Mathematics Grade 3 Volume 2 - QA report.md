# QA report

**Result:** QA FAILED after 3 rounds: 189 errors, 110 warnings (1800.1 s); proofread: 334 corrections applied; output file checks: 0 error(s)

**Document:** 数学 (zh → en, 113 page(s), 1575 translatable segment(s))

**Checks run:** `completeness`, `placeholders`, `numbers`, `untranslated`, `target_script`, `glossary`, `length_ratio`, `formatting`, `layout_fit`, `image_text`, `llm_review`, `output_checks`

## Rounds

| Round | Errors | Warnings | Re-translated | Passed | Duration |
|---|---|---|---|---|---|
| 1 | 338 | 284 | 291 segment(s) | no | 413.6 s |
| 2 | 252 | 336 | 223 segment(s) | no | 401.4 s |
| 3 | 228 | 352 | 0 segment(s) | no | 185.2 s |

- Round 1: llm_review ×458, layout_fit ×90, glossary ×32, formatting ×18, image_text ×8, untranslated ×6, length_ratio ×4, completeness ×3, numbers ×3
- Round 2: llm_review ×471, layout_fit ×72, glossary ×27, image_text ×8, formatting ×5, untranslated ×4, completeness ×1
- Round 3: llm_review ×481, layout_fit ×62, formatting ×10, image_text ×8, glossary ×7, placeholders ×6, untranslated ×5, completeness ×1

## Final issues (299)

### `completeness` — 41 errors, 0 warnings

| Severity | Page | Segment | Message | Source | Translation |
|---|---|---|---|---|---|
| error | 6 | p5_s23 | The segment has no translation; translate the complete source text | 到 |  |
| error | 9 | p8_s7 | The segment has no translation; translate the complete source text | 女★★ |  |
| error | 9 | p8_s9 | The segment has no translation; translate the complete source text | 分成行。 |  |
| error | 22 | p21_s2 | The segment has no translation; translate the complete source text | 百科 |  |
| error | 22 | p21_s3 | The segment has no translation; translate the complete source text | 百科 |  |
| error | 22 | p21_s4 | The segment has no translation; translate the complete source text | 百科 |  |
| error | 24 | p23_s5 | The translation "?" contains no words; translate the complete source text | ？个 | ? |
| error | 25 | p24_s13 | The translation "?" contains no words; translate the complete source text | ？个 | ? |
| error | 25 | p24_s14 | The segment has no translation; translate the complete source text | 个 |  |
| error | 25 | p24_s5 | The translation "¥?" contains no words; translate the complete source text | ？元 | ¥? |
| error | 25 | p24_s6 | The translation "¥?" contains no words; translate the complete source text | ？元 | ¥? |
| error | 43 | p42_s28 | The segment has no translation; translate the complete source text | 表示出来， |  |
| error | 45 | p44_s1 | The segment has no translation; translate the complete source text | 先再我 |  |
| error | 46 | p45_s7 | The translation "¥?" contains no words; translate the complete source text | ？元 | ¥? |
| error | 49 | p48_s8 | The segment has no translation; translate the complete source text | 萬大学 |  |
| error | 51 | p50_s15 | The segment has no translation; translate the complete source text | 牙膏 |  |
| error | 52 | p51_s3 | The segment has no translation; translate the complete source text | 苹果和1 |  |
| error | 52 | p51_s4 | The segment has no translation; translate the complete source text | 梨，还买了一个50___的煮鸡蛋。 |  |
| error | 52 | p51_s6 | The segment has no translation; translate the complete source text | 重吧，会说 |  |
| error | 53 | p52_s7 | The segment has no translation; translate the complete source text | 元 |  |
| error | 61 | p60_s4 | The segment has no translation; translate the complete source text | ）平方厘米）平方分米 |  |
| error | 61 | p60_s6 | The segment has no translation; translate the complete source text | ）平方分米）平方米 |  |
| error | 65 | p64_s9 | The segment has no translation; translate the complete source text | 艺术节 |  |
| error | 71 | p70_s14 | The segment has no translation; translate the complete source text | 到 |  |
| error | 71 | p70_s15 | The translation "." contains no words; translate the complete source text | 的 | . |
| error | 71 | p70_s5 | The segment has no translation; translate the complete source text | VWm |  |
| error | 73 | p72_s11 | The segment has no translation; translate the complete source text | 0三二 |  |
| error | 78 | p77_s2 | The segment has no translation; translate the complete source text | 0号 |  |
| error | 84 | p83_s16 | The segment has no translation; translate the complete source text | 33号34号35号36号37号38号39号40号32号33号34号35号36号37号38号39号 |  |
| error | 85 | p84_s16 | The segment has no translation; translate the complete source text | 下正 |  |
| error | 86 | p85_s10 | The segment has no translation; translate the complete source text | 第三小组138142 |  |
| error | 86 | p85_s11 | The segment has no translation; translate the complete source text | 第六小组138132147 |  |
| error | 86 | p85_s6 | The segment has no translation; translate the complete source text | 第-小组139142140140135146 |  |
| error | 86 | p85_s7 | The segment has no translation; translate the complete source text | 第四小组139137136138151 |  |
| error | 86 | p85_s8 | The segment has no translation; translate the complete source text | 第二小组129140 |  |
| error | 86 | p85_s9 | The segment has no translation; translate the complete source text | 第五小组135 |  |
| error | 88 | p87_s11 | The segment has no translation; translate the complete source text | 12.8元 |  |
| error | 89 | p88_s14 | The segment has no translation; translate the complete source text | 京帅汇 |  |
| error | 90 | p89_s27 | The segment has no translation; translate the complete source text | 十 |  |
| error | 92 | p91_s4 | The translation "¥?" contains no words; translate the complete source text | ？元 | ¥? |
| error | 102 | p101_s8 | The segment has no translation; translate the complete source text | 帅 |  |

### `formatting` — 27 errors, 2 warnings

| Severity | Page | Segment | Message | Source | Translation |
|---|---|---|---|---|---|
| error | 9 | p8_s15 | The source ends with a question mark; end the translation with a question mark too | 猜一猜，可能有多少颗珠子？ | Guess how many beads there might be. |
| error | 9 | p8_s8 | Keep the symbol(s) ○ ★×2 of the source in the translation, at the matching position | 一共75颗★32.15.0，分成行，平一共96个○32.16.0，每行有均每行颗★。32.17.0 | 75 32.15.0 in all, in ___ rows, ___ 32.17.0 in each row… |
| error | 19 | p18_s2 | The source ends with a question mark; end the translation with a question mark too | 每页放5张，估一估，这些邮票大约能放多少页？ | With 5 stamps on each page, estimate about how many pages t… |
| error | 19 | p18_s5 | The source ends with a question mark; end the translation with a question mark too | 算一算，能放多少页？ | Calculate how many pages can be filled. |
| error | 20 | p19_s4 | The source ends with a question mark; end the translation with a question mark too | （2）算一算，能剪出多少根跳绳？ | (2) Calculate how many skipping ropes can be cut. |
| error | 32 | p31_s6 | The source ends with a question mark; end the translation with a question mark too | 说一说，铅笔和三角尺怎样才能平移到图③的位置？ | Explain how the pencil and the set square can be moved to t… |
| error | 33 | p32_s10 | The source ends with a question mark; end the translation with a question mark too | 分别需要进行怎样的平移？ | each need to be translated. |
| error | 41 | p40_s3 | The source ends with a question mark; end the translation with a question mark too | （2）算一算，这所学校有多少名学生？ | (2) Calculate how many students the school has. |
| error | 49 | p48_s1 | The source does not end with a question mark; do not end the translation with one | 有多重 | How heavy? |
| error | 50 | p49_s28 | The source ends with a question mark; end the translation with a question mark too | 5. 1千克的棉花和1千克的盐比较，哪个重些？说说你是怎么想的？ | 5. Which is heavier, 1 kg of cotton or 1 kg of salt? Explai… |
| error | 51 | p50_s0 | The source does not end with a question mark; do not end the translation with one | 1吨有多重 | How Heavy Is 1 Tonne? |
| error | 51 | p50_s1 | The source ends with a question mark; end the translation with a question mark too | 猜猜我有多重？ | Guess my weight! |
| error | 53 | p52_s1 | The source does not end with a question mark; do not end the translation with one | 什么是面积 | What Is Area? |
| error | 59 | p58_s11 | The source does not end with a question mark; do not end the translation with one | 6.一块面积是72平方分米的长方形台布，长9分米，它的宽是多少 | 6. A rectangular tablecloth has an area of 72 square decime… |
| error | 59 | p58_s6 | Keep the line breaks of the source: it has 0 line break(s), the translation has 2 | 数学书封面教室的地面家里一个房间的地面 | Maths book cover Classroom floor Floor of a room at home |
| error | 60 | p59_s6 | The source ends with a question mark; end the translation with a question mark too | 说一说，你是怎么想的？ | Explain your thinking. |
| error | 61 | p60_s1 | The source ends with a question mark; end the translation with a question mark too | 1.与同伴说一说，你是如何得到1平方米=100平方分米、1平方分米=100平方厘米的？ | 1. Tell your partner how you worked out that 1 square metre… |
| error | 61 | p60_s3 | Keep the line breaks of the source: it has 0 line break(s), the translation has 2 | 3平方分米=（500平方厘米=（20平方分米=（ | 3 dm² = () cm² 500 cm² = () dm² 20 dm² = () m² |
| error | 61 | p60_s5 | Keep the line breaks of the source: it has 0 line break(s), the translation has 2 | 2平方米=（400平方分米=（）平方厘米1000平方分米=（）平方米 | 2 m² = () dm² 400 dm² = () cm² 1000 dm² = () m² |
| error | 64 | p63_s9 | Keep the line breaks of the source: it has 0 line break(s), the translation has 2 | 边长/厘米周长/厘米面积/平方厘米 | Side length/cm Perimeter/cm Area/cm² |
| error | 77 | p76_s9 | The source does not end with a question mark; do not end the translation with one | 谁大谁小 | which is larger? |
| error | 87 | p86_s28 | The source does not end with a question mark; do not end the translation with one | （4）小组合作，调查自己班同学的睡眠时间，并作出图来，与 | (4) In groups, survey your own class's sleep times, make a … |
| error | 94 | p93_s15 | Keep the line breaks of the source: it has 0 line break(s), the translation has 2 | 2时=（）分3吨=（）千克30角=（）元 | 2 h = () min 3 t = () kg 30 jiao = () yuan |
| error | 95 | p94_s16 | Keep the line breaks of the source: it has 0 line break(s), the translation has 3 | 出发站北京北京北京 | From Beijing Beijing Beijing |
| error | 95 | p94_s19 | Keep the line breaks of the source: it has 0 line break(s), the translation has 2 | 耗时5时55分4时48分 | Duration 5 h 55 min 4 h 48 min |
| error | 101 | p100_s7 | The source does not end with a question mark; do not end the translation with one | 1.说一说下图中哪些运动是平移，哪些是旋转 | 1. Which movements below are translations, and which are ro… |
| error | 105 | p104_s0 | The source does not end with a question mark; do not end the translation with one | 本学期你学到了什么 | What did you learn this term? |
| warning | 12 | p11_s2 | The source does not end with a exclamation mark; do not end the translation with one | 个桃子也没有 | Not a single peach! |
| warning | 51 | p50_s1 | The source does not end with a exclamation mark; do not end the translation with one | 猜猜我有多重？ | Guess my weight! |

### `glossary` — 50 errors, 0 warnings

| Severity | Page | Segment | Message | Source | Translation |
|---|---|---|---|---|---|
| error | 20 | p19_s9 | Glossary: translate "算一算" as "Calculate" | （1）算一算，需要多少块展板？ | (1) How many display boards are needed? |
| error | 24 | p23_s1 | Glossary: translate "算一算" as "Calculate" | 1.说一说，再列式算一算。 | 1. Discuss, then write a number sentence and solve. |
| error | 52 | p51_s13 | Glossary: translate "算一算" as "Calculate" | 你知道这头大象有多重吗？算一算。 | How heavy is this elephant? Work it out. |
| error | 53 | p52_s17 | Glossary: translate "面积" as "area" | 格的面积。 | squares. |
| error | 54 | p53_s7 | Glossary: translate "积分" as "integral" | 5.（1）数一数，下面图案的面积分别等于多少个方格的面积？ | 5. (1) Count: how many squares is the area of each pattern … |
| error | 56 | p55_s10 | Glossary: translate "练习" as "exercise" | （2）练习本的面积约2 | (2) A notebook: about 2 |
| error | 56 | p55_s10 | Glossary: translate "面积" as "area" | （2）练习本的面积约2 | (2) A notebook: about 2 |
| error | 56 | p55_s12 | Glossary: translate "面积" as "area" | （4）单人床的面积约2 | (4) A single bed: about 2 |
| error | 57 | p56_s5 | Glossary: translate "积分" as "integral" | 下面两个长方形的面积分别是多少？摆一摆 | What is the area of each rectangle below? Use squares. |
| error | 58 | p57_s1 | Glossary: translate "算一算" as "Calculate" | 估一估，下面每个图形的面积是多大？再实际量一量，算一算。 | Estimate the area of each figure below. Then measure and wo… |
| error | 58 | p57_s9 | Glossary: translate "算一算" as "Calculate" | 1.用1平方厘米的纸片摆一摆，算一算附页3中图2的面积，并与同伴说一说你的方法。 | 1. Lay 1-square-centimetre paper squares on figure 2 in App… |
| error | 63 | p62_s3 | Glossary: translate "已知" as "given" | 已知正方形的周长是16厘米，它的面积是多少？ | A square has a perimeter of 16 centimetres. What is its are… |
| error | 68 | p67_s7 | Glossary: translate "比一比" as "Compare" | 我们列表比一比吧 | Let's use a table |
| error | 70 | p69_s11 | Glossary: translate "个位" as "ones" | 2.妙想号在哪个位置？与同伴交流你的想法。 | 2. Where is Miaoxiang? Share your ideas with your partner. |
| error | 70 | p69_s7 | Glossary: translate "个位" as "ones" | 1.淘气号在哪个位置？与同伴交流你的想法。 | 1. Where is Taoqi? Share your ideas with your partner. |
| error | 74 | p73_s11 | Glossary: translate "正方形" as "square" | 占这些小正方形的 | still take up |
| error | 87 | p86_s2 | Glossary: translate "比一比" as "Compare" | 身高比一比。 | height when he started school. |
| error | 88 | p87_s20 | Glossary: translate "个位" as "ones" | 千位百位十位个位 | Th H T O |
| error | 88 | p87_s20 | Glossary: translate "十位" as "tens" | 千位百位十位个位 | Th H T O |
| error | 88 | p87_s20 | Glossary: translate "千位" as "thousands" | 千位百位十位个位 | Th H T O |
| error | 88 | p87_s20 | Glossary: translate "百位" as "hundreds" | 千位百位十位个位 | Th H T O |
| error | 88 | p87_s21 | Glossary: translate "个位" as "ones" | 千位百位十位个位 | Th H T O |
| error | 88 | p87_s21 | Glossary: translate "十位" as "tens" | 千位百位十位个位 | Th H T O |
| error | 88 | p87_s21 | Glossary: translate "千位" as "thousands" | 千位百位十位个位 | Th H T O |
| error | 88 | p87_s21 | Glossary: translate "百位" as "hundreds" | 千位百位十位个位 | Th H T O |
| error | 88 | p87_s22 | Glossary: translate "个位" as "ones" | 千位百位十位个位 | Th H T O |
| error | 88 | p87_s22 | Glossary: translate "十位" as "tens" | 千位百位十位个位 | Th H T O |
| error | 88 | p87_s22 | Glossary: translate "千位" as "thousands" | 千位百位十位个位 | Th H T O |
| error | 88 | p87_s22 | Glossary: translate "百位" as "hundreds" | 千位百位十位个位 | Th H T O |
| error | 88 | p87_s23 | Glossary: translate "个位" as "ones" | 千位百位十位个位 | Th H T O |
| error | 88 | p87_s23 | Glossary: translate "十位" as "tens" | 千位百位十位个位 | Th H T O |
| error | 88 | p87_s23 | Glossary: translate "千位" as "thousands" | 千位百位十位个位 | Th H T O |
| error | 88 | p87_s23 | Glossary: translate "百位" as "hundreds" | 千位百位十位个位 | Th H T O |
| error | 89 | p88_s2 | Glossary: translate "个位" as "ones" | 千位百位十位个位 | Th H T O |
| error | 89 | p88_s2 | Glossary: translate "十位" as "tens" | 千位百位十位个位 | Th H T O |
| error | 89 | p88_s2 | Glossary: translate "千位" as "thousands" | 千位百位十位个位 | Th H T O |
| error | 89 | p88_s2 | Glossary: translate "百位" as "hundreds" | 千位百位十位个位 | Th H T O |
| error | 96 | p95_s10 | Glossary: translate "直角" as "right angle" | 2.分别折出一个直角、钝角和锐角，并用三角尺验证 | 2. Fold a right, an obtuse and an acute angle; check with a… |
| error | 96 | p95_s10 | Glossary: translate "钝角" as "obtuse angle" | 2.分别折出一个直角、钝角和锐角，并用三角尺验证 | 2. Fold a right, an obtuse and an acute angle; check with a… |
| error | 96 | p95_s8 | Glossary: translate "直角" as "right angle" | 锐角直角 | acute right |
| error | 96 | p95_s8 | Glossary: translate "锐角" as "acute angle" | 锐角直角 | acute right |
| error | 96 | p95_s9 | Glossary: translate "钝角" as "obtuse angle" | 钝角 | obtuse |
| error | 97 | p96_s2 | Glossary: translate "找一找" as "Find" | 2.在右面的星座中，用红笔描出5个角，在其中找一找锐角或钝角。 | 2. In the constellation on the right, trace 5 angles in red… |
| error | 97 | p96_s2 | Glossary: translate "锐角" as "acute angle" | 2.在右面的星座中，用红笔描出5个角，在其中找一找锐角或钝角。 | 2. In the constellation on the right, trace 5 angles in red… |
| error | 98 | p97_s11 | Glossary: translate "面积" as "area" | 面的面积太麻烦了 | with it is too much trouble. |
| error | 99 | p98_s10 | Glossary: translate "积分" as "integral" | 2.下面图形的周长和面积分别是多少？（每个小格子边长1厘米） | 2. What are the perimeter and area of the figures below? (E… |
| error | 100 | p99_s10 | Glossary: translate "积分" as "integral" | 8.将一张边长为20厘米的正方形纸，剪成4个完全一样的小正方形纸片，每个小正方形的周长和面积分别是多少？ | 8. Cut a square of paper with side length 20 cm into 4 iden… |
| error | 100 | p99_s13 | Glossary: translate "面积" as "area" | （1）花坛的面积是多少平方米？ | (1) How many square metres is the flower bed? |
| error | 100 | p99_s15 | Glossary: translate "面积" as "area" | （2）小路的面积是多少平方米？ | (2) How many square metres is the path? |
| error | 103 | p102_s22 | Glossary: translate "统计" as "statistics" | 3.根据统计的结果说一说你的发现 | 3. Say what you found out from the results. |

### `layout_fit` — 28 errors, 16 warnings

| Severity | Page | Segment | Message | Source | Translation |
|---|---|---|---|---|---|
| error | 3 | p2_s14 | Shorten the translation to at most 25 characters so it fits the original box (the current translation of 30 characters overflows its box; the minimum allowed size is 55%) | 人的身高和体重有关系吗？ | Are height and weight related? |
| error | 3 | p2_s14 | Shorten the translation to at most 25 characters so it fits the original box (the current translation of 30 characters overflows its box; the minimum allowed size is 55%) | 人的身高和体重有关系吗？ | Are height and weight related? |
| error | 6 | p5_s1 | Shorten the translation to at most 12 characters so it fits the original box (the current translation of 15 characters overflows its box; the minimum allowed size is 55%) | 分桃子 | Sharing Peaches |
| error | 6 | p5_s1 | Shorten the translation to at most 12 characters so it fits the original box (the current translation of 15 characters overflows its box; the minimum allowed size is 55%) | 分桃子 | Sharing Peaches |
| error | 8 | p7_s0 | Shorten the translation to at most 12 characters so it fits the original box (the current translation of 15 characters overflows its box; the minimum allowed size is 55%) | 分橘子 | Sharing Oranges |
| error | 8 | p7_s0 | Shorten the translation to at most 12 characters so it fits the original box (the current translation of 15 characters overflows its box; the minimum allowed size is 55%) | 分橘子 | Sharing Oranges |
| error | 21 | p20_s13 | Shorten the translation to at most 21 characters so it fits the original box (the current translation of 30 characters overflows its box; the minimum allowed size is 55%) | 书架二退 | Bookcase 2: Shelves 1, 2, 3, 4 |
| error | 21 | p20_s13 | Shorten the translation to at most 21 characters so it fits the original box (the current translation of 30 characters overflows its box; the minimum allowed size is 55%) | 书架二退 | Bookcase 2: Shelves 1, 2, 3, 4 |
| error | 31 | p30_s0 | Shorten the translation to at most 20 characters so it fits the original box (the current translation of 24 characters overflows its box; the minimum allowed size is 55%) | 平移和旋转 | Translation and Rotation |
| error | 31 | p30_s0 | Shorten the translation to at most 20 characters so it fits the original box (the current translation of 24 characters overflows its box; the minimum allowed size is 55%) | 平移和旋转 | Translation and Rotation |
| error | 40 | p39_s20 | Shorten the translation to at most 5 characters so it fits the original box (the current translation of 7 characters overflows its box; the minimum allowed size is 55%) | 答： | Answer: |
| error | 40 | p39_s20 | Shorten the translation to at most 5 characters so it fits the original box (the current translation of 7 characters overflows its box; the minimum allowed size is 55%) | 答： | Answer: |
| error | 41 | p40_s24 | Shorten the translation to at most 11 characters so it fits the original box (the current translation of 13 characters overflows its box; the minimum allowed size is 55%) | 你知道吗 | Did you know? |
| error | 41 | p40_s24 | Shorten the translation to at most 11 characters so it fits the original box (the current translation of 13 characters overflows its box; the minimum allowed size is 55%) | 你知道吗 | Did you know? |
| error | 51 | p50_s0 | Shorten the translation to at most 18 characters so it fits the original box (the current translation of 21 characters overflows its box; the minimum allowed size is 55%) | 1吨有多重 | How Heavy Is 1 Tonne? |
| error | 51 | p50_s0 | Shorten the translation to at most 18 characters so it fits the original box (the current translation of 21 characters overflows its box; the minimum allowed size is 55%) | 1吨有多重 | How Heavy Is 1 Tonne? |
| error | 51 | p50_s17 | Shorten the translation to at most 19 characters so it fits the original box (the current translation of 23 characters overflows its box; the minimum allowed size is 55%) | 一桶食用油 | A bottle of cooking oil |
| error | 51 | p50_s17 | Shorten the translation to at most 19 characters so it fits the original box (the current translation of 23 characters overflows its box; the minimum allowed size is 55%) | 一桶食用油 | A bottle of cooking oil |
| error | 61 | p60_s18 | Shorten the translation to at most 11 characters so it fits the original box (the current translation of 13 characters overflows its box; the minimum allowed size is 55%) | 你知道吗 | Did you know? |
| error | 61 | p60_s18 | Shorten the translation to at most 11 characters so it fits the original box (the current translation of 13 characters overflows its box; the minimum allowed size is 55%) | 你知道吗 | Did you know? |
| error | 67 | p66_s4 | Shorten the translation to at most 7 characters so it fits the original box (the current translation of 9 characters overflows its box; the minimum allowed size is 55%) | 48人 | 48 people |
| error | 67 | p66_s4 | Shorten the translation to at most 7 characters so it fits the original box (the current translation of 9 characters overflows its box; the minimum allowed size is 55%) | 48人 | 48 people |
| error | 69 | p68_s17 | Shorten the translation to at most 15 characters so it fits the original box (the current translation of 19 characters overflows its box; the minimum allowed size is 55%) | 淘气笑笑奇思 | Taoqi Xiaoxiao Qisi |
| error | 69 | p68_s17 | Shorten the translation to at most 15 characters so it fits the original box (the current translation of 19 characters overflows its box; the minimum allowed size is 55%) | 淘气笑笑奇思 | Taoqi Xiaoxiao Qisi |
| error | 73 | p72_s8 | Shorten the translation to at most 11 characters so it fits the original box (the current translation of 13 characters overflows its box; the minimum allowed size is 55%) | 你知道吗 | Did you know? |
| error | 73 | p72_s8 | Shorten the translation to at most 11 characters so it fits the original box (the current translation of 13 characters overflows its box; the minimum allowed size is 55%) | 你知道吗 | Did you know? |
| error | 79 | p78_s0 | Shorten the translation to at most 14 characters so it fits the original box (the current translation of 17 characters overflows its box; the minimum allowed size is 55%) | 吃西瓜 | Eating Watermelon |
| error | 79 | p78_s0 | Shorten the translation to at most 14 characters so it fits the original box (the current translation of 17 characters overflows its box; the minimum allowed size is 55%) | 吃西瓜 | Eating Watermelon |
| warning | 21 | p20_s29 | The translation overflows its box and was rendered at 41% of the original size; even a much shorter text would not fit, check this box in the preview | 答： | Answer: |
| warning | 21 | p20_s29 | The translation overflows its box and was rendered at 41% of the original size; even a much shorter text would not fit, check this box in the preview | 答： | Answer: |
| warning | 32 | p31_s9 | The translation overflows its box and was rendered at 51% of the original size; even a much shorter text would not fit, check this box in the preview | 图 | Figure |
| warning | 32 | p31_s9 | The translation overflows its box and was rendered at 51% of the original size; even a much shorter text would not fit, check this box in the preview | 图 | Figure |
| warning | 36 | p35_s16 | The translation overflows its box and was rendered at 41% of the original size; even a much shorter text would not fit, check this box in the preview | 答： | Answer: |
| warning | 36 | p35_s16 | The translation overflows its box and was rendered at 41% of the original size; even a much shorter text would not fit, check this box in the preview | 答： | Answer: |
| warning | 57 | p56_s11 | The translation overflows its box and was rendered at 24% of the original size; even a much shorter text would not fit, check this box in the preview | 图 | Figure |
| warning | 57 | p56_s11 | The translation overflows its box and was rendered at 24% of the original size; even a much shorter text would not fit, check this box in the preview | 图 | Figure |
| warning | 57 | p56_s12 | The translation overflows its box and was rendered at 37% of the original size; even a much shorter text would not fit, check this box in the preview | 图 | Figure |
| warning | 57 | p56_s12 | The translation overflows its box and was rendered at 37% of the original size; even a much shorter text would not fit, check this box in the preview | 图 | Figure |
| warning | 77 | p76_s0 | The translation overflows its box and was rendered at 50% of the original size; even a much shorter text would not fit, check this box in the preview | 和 | and |
| warning | 77 | p76_s0 | The translation overflows its box and was rendered at 50% of the original size; even a much shorter text would not fit, check this box in the preview | 和 | and |
| warning | 87 | p86_s24 | The translation overflows its box and was rendered at 51% of the original size; even a much shorter text would not fit, check this box in the preview | 人数 | Number |
| warning | 87 | p86_s24 | The translation overflows its box and was rendered at 51% of the original size; even a much shorter text would not fit, check this box in the preview | 人数 | Number |
| warning | 100 | p99_s14 | The translation overflows its box and was rendered at 43% of the original size; even a much shorter text would not fit, check this box in the preview | 15米 | 15 m |
| warning | 100 | p99_s14 | The translation overflows its box and was rendered at 43% of the original size; even a much shorter text would not fit, check this box in the preview | 15米 | 15 m |

### `llm_review` — 33 errors, 76 warnings

| Severity | Page | Segment | Message | Source | Translation |
|---|---|---|---|---|---|
| error | 17 | p16_s0 | Reviewer (meaning): 练习一 is not 'Exercise 1'; the glossary gives 练习 => 'exercise', and here it is the section heading that follows each unit's lesson content. The other items translate 练一练 as 'Practice', so 'Exercise' is inconsistent as well; also 'Exercise 1' would be mistaken for exercise 1 in the lesson. Suggested translation: "Practice" | 练习一 | Exercise 1 |
| error | 17 | p16_s3 | Reviewer (omission): The source label is only '100个' (a measure word with no noun). The counted object is added; acceptable in context, but the source does not name pine cones in this label. | 100个 | 100 pine cones |
| error | 17 | p16_s5 | Reviewer (omission): The source has 先圈一圈，再列式计算; the translation drops 先 'first'. Minor, but 'First circle, then write a number sentence.' matches the source more closely. Suggested translation: "First circle, then write a number sentence." | 先圈一圈，再列式计算。 | Circle first, then write a number sentence. |
| error | 18 | p17_s22 | Reviewer (omission): The source fragment '212个。' stands alone; the translation adds 'characters'. Context (a typing contest) makes it reasonable, but it is an addition. | 212个。 | 212 characters. |
| error | 19 | p18_s0 | Reviewer (meaning): 'Stamps' is a reasonable title for 集邮 (stamp collecting), but the heading is a title of an activity about collecting stamps; 'Collecting Stamps' would be more faithful as a heading. Suggested translation: "Collecting Stamps" | 集邮 | Stamps |
| error | 20 | p19_s19 | Reviewer (omission): The item is a sentence fragment relying on the following item; '在' is left as 'In' with nothing after it, but the source '在' continues into the next line ('...里填上'). The translation drops the continuation, producing an incomplete fragment. Suggested translation: "4. In" | 4.在 | 4. In |
| error | 23 | p22_s14 | Reviewer (number): Source asks for an unknown number of 字 (characters), but translation says "words"; elsewhere 字 is rendered as characters. Suggested translation: "? characters" | ？字 | ? words |
| error | 23 | p22_s15 | Reviewer (number): Same as p22_s14: 字 should be characters, not words. Suggested translation: "? characters" | ？字 | ? words |
| error | 23 | p22_s16 | Reviewer (meaning): "列式" means set up an expression/number sentence; translation is acceptable, but consistency with 字/words issue. No error here. | 你能列式解决问题吗？ | Can you write a number sentence to solve the problem? |
| error | 23 | p22_s20 | Reviewer (number): Source unit 字 (characters) rendered as (words). Suggested translation: "170×3=510 (characters)" | 170×3=510（字） | 170×3=510 (words) |
| error | 23 | p22_s29 | Reviewer (number): ？字 should be ? characters. Suggested translation: "? characters" | ？字 | ? words |
| error | 27 | p26_s2 | Reviewer (untranslated): 囍 is a decorative symmetry symbol/picture kept exactly as in source; acceptable. | 囍 | 囍 |
| error | 27 | p26_s8 | Reviewer (untranslated): 囍 kept as symbol; acceptable. | 囍 | 囍 |
| error | 28 | p27_s0 | Reviewer (terminology): "Practice" matches glossary; no change. | 练一练 | Practice |
| error | 31 | p30_s0 | Reviewer (terminology): 'Translation' here means the geometric transformation; this is correct terminology, but the glossary does not list it. No finding. Actually 'Translation and Rotation' is the standard term. | 平移和旋转 | Translation and Rotation |
| error | 53 | p52_s10 | Reviewer (meaning): '量出每边的长度，再加起来就能比较了' is Xiaoxiao's wrong method of comparing perimeter. The translation is correct in meaning. | 量出每边的长度，再加起来就能比较了。 | Measure the length of each side, then add them up to compar… |
| error | 53 | p52_s5 | Reviewer (untranslated): '民' is a Chinese character used as a picture example; keeping it is acceptable as it is a proper symbol/character. | 民 | 民 |
| error | 56 | p55_s7 | Reviewer (untranslated): "目目" is a Chinese character fragment left untranslated (it is a picture/caption label). | 目目 | 目目 |
| error | 70 | p69_s3 | Reviewer (omission): The model names 淘气号 and 乐乐号 include 号 (No.); the translation drops it, changing the names of the models. Suggested translation: "Taoqi No. and Lele No. are both placed on the left side of the cabinet, and Taoqi No. is above Lele No." | 淘气号和乐乐号都放在柜子的左侧，淘气号在乐乐号的上面。 | Taoqi and Lele are both placed on the left side of the cabi… |
| error | 71 | p70_s13 | Reviewer (omission): The sentence is split: 我是这样得到...的; the translation renders 到 as "got" separately, producing a duplicated/incorrect fragment. Suggested translation: "This is how I got" | 我是这样得 | This is how I got |
| error | 71 | p70_s22 | Reviewer (terminology): 四分之三 as a fraction reading should be "three fourths" (or "3/4"); "three-quarters" is a hyphenated British form and inconsistent with the fraction reading convention. Suggested translation: "Read as: three fourths" | 读作：四分之三 | Read as: three-quarters |
| error | 81 | p80_s12 | Reviewer (terminology): 'math question' is fine; for consistency with textbook style consider 'mathematical question'. | （3）请你再提出一个数学问题，并试着回答。 | (3) Please ask another math question and try to answer it. |
| error | 83 | p82_s5 | Reviewer (meaning): 'of the original square?' is a fragment left over after the meaning was merged into the previous line; it duplicates and distorts the question about the fraction. |  |  |
| error | 84 | p83_s0 | Reviewer (number): The source heading contains an embedded figure/journal code '332.1.0'; the digits are garbled in the translation. Keep the source digits exactly as they appear. Suggested translation: "Unit 7 Organizing and Presenting Data332.1.0" | 七 数据的整理和表332.1.0示 | Unit 7 Organizing and Presenting Data332.1.0 |
| error | 84 | p83_s12 | Reviewer (terminology): A measure word after a number names the counted objects; 个 here counts girls wearing size 32, so it should be rendered as the counted noun, not dropped. Suggested translation: "Size 32: 1 girl" | 32号：1个 | Size 32: 1 |
| error | 90 | p89_s3 | Reviewer (terminology): "Little Shop" is an invented name for 小小商店; a more standard rendering is "Little Store" or "Xiaoxiao Shop", but not a meaning error. Suggested translation: "Little Store bought 200 balls in total" | 小小商店共进了200个球 | Little Shop bought 200 balls in total |
| error | 93 | p92_s18 | Reviewer (omission): The unit /条 ('boats') in the label is dropped; the label reads only "Small boats". Suggested translation: "Small boats/boats" | 小船/条 | Small boats |
| error | 98 | p97_s13 | Reviewer (terminology): '树叶一周的长度' means the distance around the edge of the leaf; 'distance around' is acceptable but 'The length around a leaf' matches the source more exactly. Suggested translation: "The length around a leaf is the perimeter of the leaf." | 树叶一周的长度是树叶的周长 | The distance around a leaf is the perimeter of the leaf. |
| error | 99 | p98_s16 | Reviewer (meaning): '护栏长多少米' asks for the length of the fence (the perimeter), not 'how many metres long is the fence' phrased as a separate 'Put a fence' instruction; also 'Put a fence around' is imperative whereas the source continues the question. Suggested translation: "What is the area of this lawn in square metres? If a fence is put around the lawn, how many metres long is the fence?" | 这块草地的面积是多少平方米？在草地四周围上护栏，护栏长多少米？ | What is the area of this lawn in square metres? Put a fence… |
| error | 101 | p100_s0 | Reviewer (terminology): 图形的运动 is a unit/section title; "Motion of Shapes" is acceptable but the standard term for this topic is "Movement of Figures"; keep Title Case. Suggested translation: "Movement of Figures" | 图形的运动 | Motion of Shapes |
| error | 101 | p100_s6 | Reviewer (terminology): 巩固与应用 is translated inconsistently: here "Consolidate and Apply" but later "Consolidation and Application". Use one form throughout. Suggested translation: "Consolidate and Apply" | 巩固与应用 | Consolidate and Apply |
| error | 102 | p101_s0 | Reviewer (terminology): 连一连 is rendered "Match", which matches the glossary; the label context is fine, but keep consistent capitalization. Suggested translation: "3. Match." | 3.连一连。 | 3. Match. |
| error | 103 | p102_s2 | Reviewer (terminology): 养殖场 is "farm" but the diagram label is used as a place name; capitalize consistently with other labels. Suggested translation: "Farm" | 养殖场 | Farm |
| warning | 7 | p6_s5 | Reviewer (grammar): Starts with lower-case 'say', an incomplete sentence fragment. |  |  |
| warning | 10 | p9_s5 | Reviewer (format): The source ellipsis "·····" should be rendered as "..." with three dots; the single ellipsis character is acceptable but the trailing six-dot style is not preserved. Suggested translation: "888 ÷ 6 must be greater than 100, so the quotient is certainly a three-digit number..." | 888÷6肯定比100大，商一定是个三位数····· | 888÷6 must be greater than 100, so the quotient is certainl… |
| warning | 10 | p9_s7 | Reviewer (grammar): The sentence is missing spacing and article usage before the figure reference; a cleaner textbook wording is needed. Suggested translation: "Using the figure below, explain what each step of the vertical form means." | 结合下图说一说竖式每一步的意思。 | Using the figure below, explain what each step of the verti… |
| warning | 12 | p11_s1 | Reviewer (grammar): "Talk about it and think" leaves the second verb without an object and is awkward for a textbook instruction. Suggested translation: "Talk about it and think about it." | 说一说，想一想 | Talk about it and think |
| warning | 16 | p15_s11 | Reviewer (format): Heading/title capitalization is inconsistent: "Watering Flowers" capitalizes a non-title word in an exercise item; exercise labels are not titles. Suggested translation: "7. Watering flowers" | 7.浇花 | 7. Watering Flowers |
| warning | 17 | p16_s25 | Reviewer (style): 'Forest Doctor.' is a literal rendering of the activity name 森林医生 (a 'find the mistakes' exercise). Understandable but unnatural as an English exercise title; a clearer rendering would help students know what to do. Suggested translation: "5. Be a Forest Doctor." | 5.森林医生。 | 5. Forest Doctor. |
| warning | 19 | p18_s15 | Reviewer (format): 答： is an answer label, not a heading; the translation should match p18_s10 ('Answer:') rather than being labelled a heading. The text itself is correct. Suggested translation: "Answer:" | 答： | Answer: |
| warning | 20 | p19_s11 | Reviewer (format): Enumerator '3.' should be kept at the start, which it is, but the sentence is fine; no real problem. However the translation capitalizes 'First' after '3.' which is acceptable. No finding. |  |  |
| warning | 26 | p25_s18 | Reviewer (grammar): The English imperative "Buy prizes with ¥100" is an acceptable rendering; no change needed. | 8.用100元买奖品。 | 8. Buy prizes with ¥100. |
| warning | 26 | p25_s21 | Reviewer (format): Currency formatting follows the convention (¥15); no change. | 15元 | ¥15 |
| warning | 26 | p25_s22 | Reviewer (format): Label casing: "Pencil case" is fine. | 文具盒 | Pencil case |
| warning | 26 | p25_s23 | Reviewer (format): Label casing: "Pencil" is fine. | 铅笔 | Pencil |
| warning | 26 | p25_s24 | Reviewer (format): Label casing: "Pen" is fine. | 钢笔 | Pen |
| warning | 26 | p25_s26 | Reviewer (format): Currency formatting follows the convention (¥6); no change. | 6元 | ¥6 |
| warning | 26 | p25_s27 | Reviewer (format): Currency formatting follows the convention (¥1); no change. | 1元 | ¥1 |
| warning | 26 | p25_s28 | Reviewer (format): Currency formatting follows the convention (¥8); no change. | 8元 | ¥8 |
| warning | 26 | p25_s29 | Reviewer (format): Currency formatting follows the convention (¥2); no change. | 2元 | ¥2 |
| warning | 27 | p26_s4 | Reviewer (grammar): Translation reads naturally; no change. | 这些图形从中间分开，两边一样。 | When these shapes are divided in the middle, both sides are… |
| warning | 27 | p26_s5 | Reviewer (grammar): Translation reads naturally; no change. | 怎么知道“两边一样”？ | How do you know that "both sides are the same"? |
| warning | 27 | p26_s6 | Reviewer (grammar): Translation reads naturally; no change. | 利用附页1中图1折一折，看一看。 | Fold and look at Figure 1 on Appendix page 1. |
| warning | 29 | p28_s2 | Reviewer (grammar): "Fold in half" fine. | 对折 | Fold in half |
| warning | 29 | p28_s3 | Reviewer (grammar): "Cut out a pattern with scissors" fine. | 用剪刀剪出图案 | Cut out a pattern with scissors |
| warning | 29 | p28_s4 | Reviewer (grammar): "Unfold" fine. | 展开 | Unfold |
| warning | 32 | p31_s1 | Reviewer (grammar): '移一移，描一描' means move then trace; 'Move and trace.' is acceptable. | 移一移，描一描。 | Move and trace. |
| warning | 32 | p31_s6 | Reviewer (grammar): '平移到图③的位置' means 'be translated to the position of figure ③'; 'moved' loses the precise transformation term but is acceptable. Suggested translation: "Explain how the pencil and the set square can be translated to the position of figure ③." | 说一说，铅笔和三角尺怎样才能平移到图③的位置？ | Explain how the pencil and the set square can be moved to t… |
| warning | 34 | p33_s12 | Reviewer (format): The source lacks a final period; the translation also lacks one. Consistency of punctuation; not misleading. Suggested translation: "50×10 is 10 groups of 50, which is 500." | 50×10就是10个50，是500 | 50×10 is 10 groups of 50, which is 500 |
| warning | 40 | p39_s11 | Reviewer (grammar): Awkward wording; 'in vertical form' is more natural than 'using the vertical form'. Suggested translation: "Calculate in vertical form···" | 用竖式计算··· | Calculate using the vertical form··· |
| warning | 45 | p44_s11 | Reviewer (grammar): The source contains a typo '坚式' (should be '竖式'), but the translation correctly handles it as 'vertical form'; no action needed on meaning, but the typo is not carried over. Acceptable. Suggested translation: "Why is the vertical form of division different from that of addition, subtraction and multiplication?" | 为什么除法坚式和加、减、乘法的形式不一样呢？ | Why is the vertical form of division different from that of… |
| warning | 46 | p45_s7 | Reviewer (format): The source '？元' means '? yuan', a question mark for an unknown amount. The translation '¥?' places the currency symbol before the question mark, which follows the convention for known amounts but here the amount is unknown. Acceptable style, but '? yuan' might be clearer. No change needed. Suggested translation: "? yuan" | ？元 | ¥? |
| warning | 47 | p46_s6 | Reviewer (grammar): '森林医生' literally means 'Forest Doctor', which is a metaphor for finding errors; the literal translation may confuse students, but it preserves the source. Acceptable as is. Suggested translation: "7. Forest Doctor." | 7.森林医生。 | 7. Forest Doctor. |
| warning | 49 | p48_s0 | Reviewer (format): Unit heading should use the English comma or "and"? The rule for bare-numeral unit headings says "Unit 4 Addition and Subtraction"; here the list of topics needs the standard separator, and the heading should be in Title Case. Suggested translation: "Unit 4 Kilograms, Grams, and Tons" | 四 千克、克、吨 | Unit 4 Kilograms, Grams, Tons |
| warning | 49 | p48_s16 | Reviewer (format): Spacing around the equal sign is inconsistent; use spaces on both sides. Suggested translation: "1 kg = 1000 g" | 1千克=1000克 | 1 kg =1000 g |
| warning | 51 | p50_s20 | Reviewer (format): The empty answer blank '（）' must be kept exactly as it stands; here it was reduced to '()' losing the blank. Suggested translation: "Weighs 3 ( )" | 重3（） | Weighs 3 () |
| warning | 51 | p50_s21 | Reviewer (format): The empty answer blank '（）' must be kept exactly as it stands; here it was reduced to '()'. Suggested translation: "Weighs 2 ( )" | 重2（） | Weighs 2 () |
| warning | 51 | p50_s22 | Reviewer (format): The answer blank '（' must be preserved as an opening parenthesis blank. Suggested translation: "Weighs 50 (" | 重50（ | Weighs 50 ( |
| warning | 51 | p50_s23 | Reviewer (format): The answer blank '（' must be preserved as an opening parenthesis blank. Suggested translation: "Weighs 250 (" | 重250（ | Weighs 250 ( |
| warning | 51 | p50_s7 | Reviewer (format): Spacing around the equal sign is inconsistent. Suggested translation: "1 t = 1000 kg" | 1吨=1000千克 | 1 t =1000 kg |
| warning | 59 | p58_s8 | Reviewer (format): Inconsistent abbreviation: 'dm' here while the rest of the page uses 'decimeters'. Suggested translation: "5 decimeters" | 5分米 | 5 dm |
| warning | 62 | p61_s6 | Reviewer (format): The measurement blank “（）” is kept as “()” but should be placed after “2” before “long”: “A jump rope is about 2 () long.”, not changing the position of the blank. Suggested translation: "(1) A jump rope is about 2 () long." | （1）一根跳绳长约2（）。 | (1) A jump rope is about 2 () long. |
| warning | 70 | p69_s8 | Reviewer (format): The circled numbers ① and ③ were kept but ② was replaced with a comma; the source has ①, ②, ③ written as ①，，③ (a typo for ①, ②, ③). Keep the circled enumerators. Suggested translation: "Taoqi No. is on the left side of the cabinet, so it could be in position ①, ② or ③" | 淘气号放在柜子的左侧，它可能在①，，③的位置 | Taoqi is on the left side of the cabinet, so it could be in… |
| warning | 74 | p73_s0 | Reviewer (format): Heading 分一分 （二） should follow the unit convention; "Divide (2)" is acceptable but Chinese textbooks use "Divide (II)" or "Divide (2)". Leaving as is; no error. | 分一分 （二） | Divide (2) |
| warning | 77 | p76_s10 | Reviewer (format): The ellipsis should keep its five-dot form as in the source (·····) or the standard three dots; minor style inconsistency. Suggested translation: "In Grade 5, we will learn more..." | 五年级时，我们还会再学习的····· | In Grade 5, we will learn more... |
| warning | 77 | p76_s5 | Reviewer (punctuation): The task says to report only real problems; separate labels 'and' are fragments and cannot be judged. No problem. | 和 | and |
| warning | 77 | p76_s6 | Reviewer (punctuation): Duplicate label fragment; no issue detected. | 和 | and |
| warning | 77 | p76_s8 | Reviewer (punctuation): Duplicate label fragment; no issue detected. | 和 | and |
| warning | 78 | p77_s0 | Reviewer (format): Source is a section label 练一练; the glossary maps 练一练 to 'Practice', which matches, but this is fine. | 练一练 | Practice |
| warning | 81 | p80_s3 | Reviewer (format): Sentences p80_s3–p80_s6 are label fragments ending in 的 followed by a fraction in the figure; the fraction should be retained if present. | 红星占全部星星的 | Red stars make up |
| warning | 82 | p81_s0 | Reviewer (format): 'Color and compare' for 涂一涂，比一比 is acceptable; keep consistent with p77_s1 'Color and compare'. | 5.涂一涂，比一比。 | 5. Color and compare. |
| warning | 84 | p83_s13 | Reviewer (grammar): '再接着画下去' means 'continue drawing', and '你看懂了吗？' is 'Do you understand how she did it?'; 'Continue the drawing' slightly shifts the action. Suggested translation: "This is how Miaoxiang did it. Do you understand? Continue drawing." | 妙想是这样做的，你看懂了吗？再接着画下去。 | This is how Miaoxiang did it. Do you understand? Continue t… |
| warning | 84 | p83_s18 | Reviewer (grammar): The Chinese uses an ellipsis (···) after 'smallest is'; the translation keeps the ellipsis but joins with 'and', reading slightly awkwardly. Meaning is preserved. Suggested translation: "The largest boys' shoe size is 38 and the smallest is ···" | 男生鞋最大号码是38号最小号码是··· | The largest boys' shoe size is 38 and the smallest is ··· |
| warning | 85 | p84_s12 | Reviewer (format): The source uses a full-width opening bracket '(' while other items use '（'; the translation uses a half-width '(' which is consistent enough. Minor inconsistency only. Suggested translation: "(2) How many people voted in total?" | (2）一共有多少人投票？ | (2) How many people voted in total? |
| warning | 85 | p84_s14 | Reviewer (format): Tally-mark symbol 正 is a counting symbol; the leading 'T' is an artifact of the scan. Keeping '正' is correct per convention; no change needed. | T正 | T正 |
| warning | 85 | p84_s15 | Reviewer (format): Tally-mark 正 kept verbatim as required; the preceding 'T' artifact is retained. No change needed. | T正正 | T正正 |
| warning | 85 | p84_s17 | Reviewer (format): Tally-mark 正 kept verbatim; the 'T' artifact is retained. No change needed. | T正 | T正 |
| warning | 85 | p84_s6 | Reviewer (format): The source glyph string '336.6.0' is preserved verbatim, which is correct as a placeholder-like artifact; no change needed. Flagging only for the missing full stop spacing convention (×代表1票) is fine. | 336.6.0（×代表1票） | 336.6.0 (× stands for 1 vote) |
| warning | 86 | p85_s3 | Reviewer (grammar): 本句与 p85_s2 拼接为完整句；'the class can still buy' 与源 '还' 相符。No change needed. |  |  |
| warning | 87 | p86_s10 | Reviewer (format): Time labels: standard textbook style writes times as '7:00' and '7:30' rather than '7 h 7 h 30 min'. Suggested translation: "7:00 7:30" | 7时7时30分 | 7 h 7 h 30 min |
| warning | 87 | p86_s11 | Reviewer (format): Time labels should be written in colon form, e.g. '8:00'. Suggested translation: "8:00" | 8时 | 8 h |
| warning | 87 | p86_s12 | Reviewer (format): Time labels should be written in colon form, e.g. '8:30'. Suggested translation: "8:30" | 8时30分 | 8 h 30 min |
| warning | 87 | p86_s13 | Reviewer (format): Time labels should be written in colon form, e.g. '9:00'. Suggested translation: "9:00" | 9时 | 9 h |
| warning | 87 | p86_s14 | Reviewer (format): Time labels should be written in colon form, e.g. '9:30'. Suggested translation: "9:30" | 9时30分 | 9 h 30 min |
| warning | 87 | p86_s15 | Reviewer (format): Time labels should be written in colon form, e.g. '10:00 10:30 11:00'. Suggested translation: "10:00 10:30 11:00" | 10时10时30分11时 | 10 h 10 h 30 min 11 h |
| warning | 87 | p86_s27 | Reviewer (grammar): "thoughts about the survey results?" is fine, but combined with the previous fragment the question reads awkwardly; use "what do you think about the survey results?" Suggested translation: "what do you think about the survey results?" |  |  |
| warning | 93 | p92_s21 | Reviewer (format): The four plan labels run together in the source; the translation also runs them together, which is acceptable, but separating them improves readability. No change to meaning. Suggested translation: "Plan 1 Plan 2 Plan 3 Plan 4" | 方案1方案2方案3方案4 | Plan 1 Plan 2 Plan 3 Plan 4 |
| warning | 94 | p93_s16 | Reviewer (format): Similarly, '6 jiao = () fen' involves jiao and fen, not yuan; the bare unit labels 'fen' and 'jiao' are appropriate. No change needed. | 5分=（）秒 4000克=（）千克 6角=（）分 | 5 min = () s 4000 g = () kg 6 jiao = () fen |
| warning | 94 | p93_s3 | Reviewer (format): The trailing ellipsis dots '····' are rendered as spaced dots '····'; this is a minor formatting deviation that does not change the meaning. Suggested translation: "Which quantities are in the information above? Which are units of mass, and which are ····" | 上面的信息中有哪些量？哪些是质量单位，哪些是···· | Which quantities are in the information above? Which are un… |
| warning | 96 | p95_s13 | Reviewer (grammar): "How did you decide?" is fine, though "How do you tell?" is closer to 你是怎样判断的. No meaning change. | 3.哪个图形是长方形？哪个是正方形？你是怎样判断的？ | 3. Which shape is a rectangle? Which is a square? How did y… |
| warning | 97 | p96_s5 | Reviewer (grammar): The sentence is split across segments and its wording ('Can you tell from the dialogue below') is stiff and misses '判断' being completed by the next segment; a connector would read better. Suggested translation: "Taoqi and Xiaoxiao put a piece of coloured paper in an envelope. From the dialogue below, can you tell" | 淘气和笑笑在信封里装了一张彩色纸，你能根据下面的对话判断这张纸的形状吗？ | Taoqi and Xiaoxiao put a sheet of coloured paper in an enve… |
| warning | 98 | p97_s12 | Reviewer (grammar): Repetitive 'what ... is and what ... is' is unidiomatic; smoother phrasing is preferable. Suggested translation: "2. Give examples to explain what perimeter and area are." | 2.举例说一说什么是周长，什么是面积。 | 2. Give examples to explain what perimeter is and what area… |
| warning | 98 | p97_s21 | Reviewer (format): Spacing in the formula is inconsistent with the source ('(4+3) ×2'); keep the source's '（4+3）×2'. Suggested translation: "(4+3)×2=14 (cm)" | （4+3）×2=14（厘米） | (4+3) ×2=14 (cm) |
| warning | 99 | p98_s17 | Reviewer (format): Bare unit label 米 in a figure should be 'm' as in the translation — acceptable; no change needed. | 米 | m |
| warning | 99 | p98_s3 | Reviewer (grammar): 'A big tree is about 8 () tall' is fine, but the bracket must remain an answer blank; consistent blank style ( ___ ) would be clearer than '()'. | （1）一棵大树高约8（）。 | (1) A big tree is about 8 () tall. |
| warning | 100 | p99_s12 | Reviewer (grammar): "A narrow path" adds the adjective "narrow", which is not in the source; also the number "9." should be kept at the start and the wording can be closer to the original. Suggested translation: "9. A path 1 m wide is laid around a rectangular flower bed." | 9.在一个长方形的花坛四周，铺上宽1米的小路。 | 9. A narrow path 1 m wide is laid around a rectangular flow… |
| warning | 102 | p101_s4 | Reviewer (format): Place labels should be consistent in capitalization; 公园 as a place name here is fine as "Park" but check consistency with other labels. Suggested translation: "Park" | 公园 | Park |
| warning | 103 | p102_s21 | Reviewer (format): Tally mark 正 is kept correctly; "正T" combines the tally character with a letter T, which should stay as in the source. Suggested translation: "正T" | 正T | 正T |
| warning | 103 | p102_s23 | Reviewer (grammar): Ellipsis style "···" is acceptable but should match the book's convention ("..." or "……"). Suggested translation: "Our class has more boys than girls..." | 我们班男生比女生多··· | Our class has more boys than girls··· |

### `numbers` — 1 error, 0 warnings

| Severity | Page | Segment | Message | Source | Translation |
|---|---|---|---|---|---|
| error | 61 | p60_s11 | Number "420004" from the source is missing in the translation; keep every number exactly as written in the source | （3）篮球场的面积大约是420（），也就是420004.谁说得对？ | (3) The area of the basketball court is about 420 (), that … |

### `target_script` — 1 error, 0 warnings

| Severity | Page | Segment | Message | Source | Translation |
|---|---|---|---|---|---|
| error | 28 | p27_s6 | Only 0% of the letters in the translation are in the English script; write the whole translation in English (formulas, variable names, units and proper names copied from the source excepted) | 江山美如画 | 江山美如画 |

### `untranslated` — 8 errors, 0 warnings

| Severity | Page | Segment | Message | Source | Translation |
|---|---|---|---|---|---|
| error | 27 | p26_s2 | 1 letter(s) of the source script remain untranslated ("囍"); translate all text into English | 囍 | 囍 |
| error | 27 | p26_s8 | 1 letter(s) of the source script remain untranslated ("囍"); translate all text into English | 囍 | 囍 |
| error | 28 | p27_s6 | 5 letter(s) of the source script remain untranslated ("江山美如画"); translate all text into English | 江山美如画 | 江山美如画 |
| error | 53 | p52_s5 | 1 letter(s) of the source script remain untranslated ("民"); translate all text into English | 民 | 民 |
| error | 56 | p55_s7 | 2 letter(s) of the source script remain untranslated ("目目"); translate all text into English | 目目 | 目目 |
| error | 61 | p60_s19 | 2 letter(s) of the source script remain untranslated ("幂", "积"); translate all text into English | 在古代，为了确定农业收成，计算税收，必须丈量土地，由此对面积产生了认识。中国古代形象地用“幂”字或“积”字来表示面积。 | In ancient times, people had to measure land to work out ha… |
| error | 61 | p60_s20 | 2 letter(s) of the source script remain untranslated ("幂", "积"); translate all text into English | 幂：遮盖物品的方形布；积：积累。你能理解这两个字的意思吗？ | 幂 (mì): a square cloth for covering things; 积 (jī): to pile… |
| error | 65 | p64_s18 | 1 letter(s) of the source script remain untranslated ("世"); translate all text into English | 把汉字“世”与“2010”完美结合。 | It neatly combines the character “世” (shì) with "2010". |

### `image_text` — 0 errors, 16 warnings

| Severity | Page | Segment | Message | Source | Translation |
|---|---|---|---|---|---|
| warning | 15 | p14_i56_8 | The text '200÷2=100,502比' was left in the source language (inline pictograms the OCR cannot read (left in the picture)): the line is built around symbols or pictures the OCR could not read - check the page in the preview | 200÷2=100,502比 |  |
| warning | 15 | p14_i56_8 | The text '200÷2=100,502比' was left in the source language (inline pictograms the OCR cannot read (left in the picture)): the line is built around symbols or pictures the OCR could not read - check the page in the preview | 200÷2=100,502比 |  |
| warning | 30 | p29_i116_7 | The text '做一做。画“”' was left in the source language (unreadable symbol in quotes (left in the picture)): the line is built around symbols or pictures the OCR could not read - check the page in the preview | 做一做。画“” |  |
| warning | 30 | p29_i116_7 | The text '做一做。画“”' was left in the source language (unreadable symbol in quotes (left in the picture)): the line is built around symbols or pictures the OCR could not read - check the page in the preview | 做一做。画“” |  |
| warning | 62 | p61_i244_1 | The text '1.用红色描出图形的边线，用蓝色涂出图形的面。' was left in the source language (inline pictograms the OCR cannot read (left in the picture)): the line is built around symbols or pictures the OCR could not read - check the page in the preview | 1.用红色描出图形的边线，用蓝色涂出图形的面。 |  |
| warning | 62 | p61_i244_1 | The text '1.用红色描出图形的边线，用蓝色涂出图形的面。' was left in the source language (inline pictograms the OCR cannot read (left in the picture)): the line is built around symbols or pictures the OCR could not read - check the page in the preview | 1.用红色描出图形的边线，用蓝色涂出图形的面。 |  |
| warning | 73 | p72_i288_21 | The text '记号“”表示分' was left in the source language (unreadable symbol in quotes (left in the picture)): the line is built around symbols or pictures the OCR could not read - check the page in the preview | 记号“”表示分 |  |
| warning | 73 | p72_i288_21 | The text '记号“”表示分' was left in the source language (unreadable symbol in quotes (left in the picture)): the line is built around symbols or pictures the OCR could not read - check the page in the preview | 记号“”表示分 |  |
| warning | 77 | p76_i304_0 | The text '比大小' was left in the source language (inline pictograms the OCR cannot read (left in the picture)): the line is built around symbols or pictures the OCR could not read - check the page in the preview | 比大小 |  |
| warning | 77 | p76_i304_0 | The text '比大小' was left in the source language (inline pictograms the OCR cannot read (left in the picture)): the line is built around symbols or pictures the OCR could not read - check the page in the preview | 比大小 |  |
| warning | 77 | p76_i304_20 | The text '我出题你来比' was left in the source language (inline pictograms the OCR cannot read (left in the picture)): the line is built around symbols or pictures the OCR could not read - check the page in the preview | 我出题你来比 |  |
| warning | 77 | p76_i304_20 | The text '我出题你来比' was left in the source language (inline pictograms the OCR cannot read (left in the picture)): the line is built around symbols or pictures the OCR could not read - check the page in the preview | 我出题你来比 |  |
| warning | 87 | p86_i344_43 | The text '三（2）班的同学对比，两个班同学的睡眠时间有什么不同吗？' was left in the source language (inline pictograms the OCR cannot read (left in the picture)): the line is built around symbols or pictures the OCR could not read - check the page in the preview | 三（2）班的同学对比，两个班同学的睡眠时间有什么不同吗？ |  |
| warning | 87 | p86_i344_43 | The text '三（2）班的同学对比，两个班同学的睡眠时间有什么不同吗？' was left in the source language (inline pictograms the OCR cannot read (left in the picture)): the line is built around symbols or pictures the OCR could not read - check the page in the preview | 三（2）班的同学对比，两个班同学的睡眠时间有什么不同吗？ |  |
| warning | 102 | p101_i404_18 | The text '的面。' was left in the source language (inline pictograms the OCR cannot read (left in the picture)): the line is built around symbols or pictures the OCR could not read - check the page in the preview | 的面。 |  |
| warning | 102 | p101_i404_18 | The text '的面。' was left in the source language (inline pictograms the OCR cannot read (left in the picture)): the line is built around symbols or pictures the OCR could not read - check the page in the preview | 的面。 |  |
