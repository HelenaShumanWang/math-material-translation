# QA report

**Result:** QA FAILED after 3 rounds: 179 errors, 141 warnings (1838.8 s); proofread: 728 corrections applied; output file checks: 0 error(s)

**Document:** 数学 (zh → en, 113 page(s), 1602 translatable segment(s))

**Checks run:** `completeness`, `placeholders`, `numbers`, `untranslated`, `target_script`, `glossary`, `length_ratio`, `formatting`, `layout_fit`, `image_text`, `llm_review`, `output_checks`

## Rounds

| Round | Errors | Warnings | Re-translated | Passed | Duration |
|---|---|---|---|---|---|
| 1 | 333 | 308 | 300 segment(s) | no | 462.7 s |
| 2 | 259 | 282 | 228 segment(s) | no | 391.8 s |
| 3 | 244 | 324 | 0 segment(s) | no | 173.1 s |

- Round 1: llm_review ×486, layout_fit ×90, glossary ×30, formatting ×18, image_text ×11, untranslated ×3, completeness ×2, length_ratio ×1
- Round 2: llm_review ×416, layout_fit ×72, untranslated ×14, glossary ×11, image_text ×11, formatting ×7, target_script ×7, length_ratio ×2, completeness ×1
- Round 3: llm_review ×467, layout_fit ×69, image_text ×11, glossary ×6, formatting ×5, untranslated ×5, completeness ×3, numbers ×1, placeholders ×1

## Final issues (320)

### `completeness` — 10 errors, 0 warnings

| Severity | Page | Segment | Message | Source | Translation |
|---|---|---|---|---|---|
| error | 23 | p22_s14 | The translation "?" contains no words; translate the complete source text | ？字 | ? |
| error | 23 | p22_s29 | The translation "?" contains no words; translate the complete source text | ？字 | ? |
| error | 24 | p23_s5 | The translation "?" contains no words; translate the complete source text | ？个 | ? |
| error | 25 | p24_s13 | The translation "?" contains no words; translate the complete source text | ？个 | ? |
| error | 25 | p24_s5 | The translation "¥?" contains no words; translate the complete source text | ？元 | ¥? |
| error | 25 | p24_s6 | The translation "¥?" contains no words; translate the complete source text | ？元 | ¥? |
| error | 46 | p45_s7 | The translation "¥?" contains no words; translate the complete source text | ？元 | ¥? |
| error | 71 | p70_s14 | The translation "." contains no words; translate the complete source text | 的 | . |
| error | 90 | p89_s27 | The translation "+" contains no words; translate the complete source text | 十 | + |
| error | 92 | p91_s4 | The translation "¥?" contains no words; translate the complete source text | ？元 | ¥? |

### `formatting` — 23 errors, 2 warnings

| Severity | Page | Segment | Message | Source | Translation |
|---|---|---|---|---|---|
| error | 9 | p8_s15 | The source ends with a question mark; end the translation with a question mark too | 猜一猜，可能有多少颗珠子？ | Guess how many beads there might be. |
| error | 9 | p8_s8 | Keep the symbol(s) ○ ★×2 of the source in the translation, at the matching position | 一共75颗★32.15.0，分成行，平一共96个○32.16.0，每行有均每行颗★。32.17.0 | 75 32.15.0 in all, in ___ rows, ___ 32.17.0 in each row… |
| error | 19 | p18_s2 | The source ends with a question mark; end the translation with a question mark too | 每页放5张，估一估，这些邮票大约能放多少页？ | With 5 stamps on each page, estimate about how many pages t… |
| error | 19 | p18_s5 | The source ends with a question mark; end the translation with a question mark too | 算一算，能放多少页？ | Calculate how many pages can be filled. |
| error | 20 | p19_s4 | The source ends with a question mark; end the translation with a question mark too | （2）算一算，能剪出多少根跳绳？ | (2) Calculate how many skipping ropes can be cut. |
| error | 20 | p19_s9 | The source ends with a question mark; end the translation with a question mark too | （1）算一算，需要多少块展板？ | (1) Work out how many display boards are needed. |
| error | 32 | p31_s6 | The source ends with a question mark; end the translation with a question mark too | 说一说，铅笔和三角尺怎样才能平移到图③的位置？ | Discuss how the pencil and the set square can be translated… |
| error | 33 | p32_s10 | The source ends with a question mark; end the translation with a question mark too | 分别需要进行怎样的平移？ | each need to be translated. |
| error | 49 | p48_s1 | The source does not end with a question mark; do not end the translation with one | 有多重 | How heavy? |
| error | 50 | p49_s28 | The source ends with a question mark; end the translation with a question mark too | 5. 1千克的棉花和1千克的盐比较，哪个重些？说说你是怎么想的？ | 5. Compare 1 kg of cotton with 1 kg of salt. Which is heavi… |
| error | 51 | p50_s0 | The source does not end with a question mark; do not end the translation with one | 1吨有多重 | How Heavy Is 1 Tonne? |
| error | 51 | p50_s1 | The source ends with a question mark; end the translation with a question mark too | 猜猜我有多重？ | Guess how heavy I am! |
| error | 59 | p58_s11 | The source does not end with a question mark; do not end the translation with one | 6.一块面积是72平方分米的长方形台布，长9分米，它的宽是多少 | 6. A rectangular tablecloth has an area of 72 square decime… |
| error | 60 | p59_s6 | The source ends with a question mark; end the translation with a question mark too | 说一说，你是怎么想的？ | Explain your thinking. |
| error | 61 | p60_s1 | The source ends with a question mark; end the translation with a question mark too | 1.与同伴说一说，你是如何得到1平方米=100平方分米、1平方分米=100平方厘米的？ | 1. Tell your partner how you get 1 square metre =100 square… |
| error | 73 | p72_s8 | The source ends with a question mark; end the translation with a question mark too | 你知道吗 | Did you know |
| error | 77 | p76_s9 | The source does not end with a question mark; do not end the translation with one | 谁大谁小 | which is larger? |
| error | 94 | p93_s15 | Keep the line breaks of the source: it has 0 line break(s), the translation has 2 | 2时=（）分3吨=（）千克30角=（）元 | 2 h = () min 3 t = () kg 30 jiao = () yuan |
| error | 95 | p94_s16 | Keep the line breaks of the source: it has 0 line break(s), the translation has 3 | 出发站北京北京北京 | From Beijing Beijing Beijing |
| error | 95 | p94_s19 | Keep the line breaks of the source: it has 0 line break(s), the translation has 2 | 耗时5时55分4时48分 | Time taken 5 h 55 min 4 h 48 min |
| error | 101 | p100_s3 | The source does not end with a question mark; do not end the translation with one | 2.举例说一说哪些运动是平移，哪些是旋转。 | 2. Give examples. Which movements are translations, and whi… |
| error | 101 | p100_s7 | The source does not end with a question mark; do not end the translation with one | 1.说一说下图中哪些运动是平移，哪些是旋转 | 1. Which movements below are translations, and which are ro… |
| error | 105 | p104_s0 | The source does not end with a question mark; do not end the translation with one | 本学期你学到了什么 | What did you learn this term? |
| warning | 12 | p11_s2 | The source does not end with a exclamation mark; do not end the translation with one | 个桃子也没有 | Not a single peach! |
| warning | 51 | p50_s1 | The source does not end with a exclamation mark; do not end the translation with one | 猜猜我有多重？ | Guess how heavy I am! |

### `glossary` — 22 errors, 0 warnings

| Severity | Page | Segment | Message | Source | Translation |
|---|---|---|---|---|---|
| error | 20 | p19_s9 | Glossary: translate "算一算" as "Calculate" | （1）算一算，需要多少块展板？ | (1) Work out how many display boards are needed. |
| error | 53 | p52_s17 | Glossary: translate "面积" as "area" | 格的面积。 | squares. |
| error | 54 | p53_s7 | Glossary: translate "积分" as "integral" | 5.（1）数一数，下面图案的面积分别等于多少个方格的面积？ | 5. (1) Count: how many squares is the area of each pattern … |
| error | 57 | p56_s5 | Glossary: translate "积分" as "integral" | 下面两个长方形的面积分别是多少？摆一摆 | What is the area of each rectangle below? Use squares. |
| error | 58 | p57_s1 | Glossary: translate "算一算" as "Calculate" | 估一估，下面每个图形的面积是多大？再实际量一量，算一算。 | Estimate the area of each figure below. Then measure and wo… |
| error | 58 | p57_s9 | Glossary: translate "算一算" as "Calculate" | 1.用1平方厘米的纸片摆一摆，算一算附页3中图2的面积，并与同伴说一说你的方法。 | 1. Lay 1-square-centimetre paper squares on figure 2 in App… |
| error | 63 | p62_s3 | Glossary: translate "已知" as "given" | 已知正方形的周长是16厘米，它的面积是多少？ | A square has a perimeter of 16 centimetres. What is its are… |
| error | 70 | p69_s11 | Glossary: translate "个位" as "ones" | 2.妙想号在哪个位置？与同伴交流你的想法。 | 2. Where is Miaoxiang? Share your idea with your partner. |
| error | 70 | p69_s7 | Glossary: translate "个位" as "ones" | 1.淘气号在哪个位置？与同伴交流你的想法。 | 1. Where is Taoqi? Share your idea with your partner. |
| error | 74 | p73_s11 | Glossary: translate "正方形" as "square" | 占这些小正方形的 | still takes up |
| error | 87 | p86_s2 | Glossary: translate "比一比" as "Compare" | 身高比一比。 | height when he started school. |
| error | 96 | p95_s10 | Glossary: translate "直角" as "right angle" | 2.分别折出一个直角、钝角和锐角，并用三角尺验证 | 2. Fold a right, an obtuse and an acute angle, then check t… |
| error | 96 | p95_s10 | Glossary: translate "钝角" as "obtuse angle" | 2.分别折出一个直角、钝角和锐角，并用三角尺验证 | 2. Fold a right, an obtuse and an acute angle, then check t… |
| error | 96 | p95_s8 | Glossary: translate "直角" as "right angle" | 锐角直角 | acute right |
| error | 96 | p95_s8 | Glossary: translate "锐角" as "acute angle" | 锐角直角 | acute right |
| error | 96 | p95_s9 | Glossary: translate "钝角" as "obtuse angle" | 钝角 | obtuse |
| error | 97 | p96_s2 | Glossary: translate "找一找" as "Find" | 2.在右面的星座中，用红笔描出5个角，在其中找一找锐角或钝角。 | 2. In the constellation on the right, trace 5 angles in red… |
| error | 97 | p96_s2 | Glossary: translate "锐角" as "acute angle" | 2.在右面的星座中，用红笔描出5个角，在其中找一找锐角或钝角。 | 2. In the constellation on the right, trace 5 angles in red… |
| error | 98 | p97_s11 | Glossary: translate "面积" as "area" | 面的面积太麻烦了 | desktop is too much trouble. |
| error | 99 | p98_s10 | Glossary: translate "积分" as "integral" | 2.下面图形的周长和面积分别是多少？（每个小格子边长1厘米） | 2. What are the perimeter and area of the figures below? (T… |
| error | 100 | p99_s10 | Glossary: translate "积分" as "integral" | 8.将一张边长为20厘米的正方形纸，剪成4个完全一样的小正方形纸片，每个小正方形的周长和面积分别是多少？ | 8. Cut a square piece of paper with side 20 cm into 4 ident… |
| error | 103 | p102_s22 | Glossary: translate "统计" as "statistics" | 3.根据统计的结果说一说你的发现 | 3. Say what you found out from the results. |

### `layout_fit` — 38 errors, 34 warnings

| Severity | Page | Segment | Message | Source | Translation |
|---|---|---|---|---|---|
| error | 4 | p3_s2 | Shorten the translation to at most 14 characters so it fits the original box (the current translation of 16 characters overflows its box; the minimum allowed size is 55%) | 图形的运动 | Motion of Shapes |
| error | 4 | p3_s2 | Shorten the translation to at most 14 characters so it fits the original box (the current translation of 16 characters overflows its box; the minimum allowed size is 55%) | 图形的运动 | Motion of Shapes |
| error | 4 | p3_s4 | Shorten the translation to at most 11 characters so it fits the original box (the current translation of 13 characters overflows its box; the minimum allowed size is 55%) | 售票处 | Ticket Office |
| error | 4 | p3_s4 | Shorten the translation to at most 11 characters so it fits the original box (the current translation of 13 characters overflows its box; the minimum allowed size is 55%) | 售票处 | Ticket Office |
| error | 6 | p5_s1 | Shorten the translation to at most 12 characters so it fits the original box (the current translation of 15 characters overflows its box; the minimum allowed size is 55%) | 分桃子 | Sharing Peaches |
| error | 6 | p5_s1 | Shorten the translation to at most 12 characters so it fits the original box (the current translation of 15 characters overflows its box; the minimum allowed size is 55%) | 分桃子 | Sharing Peaches |
| error | 12 | p11_s8 | Shorten the translation to at most 9 characters so it fits the original box (the current translation of 11 characters overflows its box; the minimum allowed size is 55%) | 306个 | 306 peaches |
| error | 12 | p11_s8 | Shorten the translation to at most 9 characters so it fits the original box (the current translation of 11 characters overflows its box; the minimum allowed size is 55%) | 306个 | 306 peaches |
| error | 16 | p15_s10 | Shorten the translation to at most 6 characters so it fits the original box (the current translation of 8 characters overflows its box; the minimum allowed size is 55%) | 商 | Quotient |
| error | 16 | p15_s10 | Shorten the translation to at most 6 characters so it fits the original box (the current translation of 8 characters overflows its box; the minimum allowed size is 55%) | 商 | Quotient |
| error | 21 | p20_s16 | Shorten the translation to at most 6 characters so it fits the original box (the current translation of 8 characters overflows its box; the minimum allowed size is 55%) | 25本 | 25 books |
| error | 21 | p20_s16 | Shorten the translation to at most 6 characters so it fits the original box (the current translation of 8 characters overflows its box; the minimum allowed size is 55%) | 25本 | 25 books |
| error | 41 | p40_s24 | Shorten the translation to at most 11 characters so it fits the original box (the current translation of 13 characters overflows its box; the minimum allowed size is 55%) | 你知道吗 | Did you know? |
| error | 41 | p40_s24 | Shorten the translation to at most 11 characters so it fits the original box (the current translation of 13 characters overflows its box; the minimum allowed size is 55%) | 你知道吗 | Did you know? |
| error | 45 | p44_s1 | Shorten the translation to at most 13 characters so it fits the original box (the current translation of 15 characters overflows its box; the minimum allowed size is 55%) | 先再我 | Estimate first, |
| error | 45 | p44_s1 | Shorten the translation to at most 13 characters so it fits the original box (the current translation of 15 characters overflows its box; the minimum allowed size is 55%) | 先再我 | Estimate first, |
| error | 49 | p48_s8 | Shorten the translation to at most 7 characters so it fits the original box (the current translation of 14 characters overflows its box; the minimum allowed size is 55%) | 萬大学 | Wan University |
| error | 49 | p48_s8 | Shorten the translation to at most 7 characters so it fits the original box (the current translation of 14 characters overflows its box; the minimum allowed size is 55%) | 萬大学 | Wan University |
| error | 61 | p60_s18 | Shorten the translation to at most 11 characters so it fits the original box (the current translation of 13 characters overflows its box; the minimum allowed size is 55%) | 你知道吗 | Did you know? |
| error | 61 | p60_s18 | Shorten the translation to at most 11 characters so it fits the original box (the current translation of 13 characters overflows its box; the minimum allowed size is 55%) | 你知道吗 | Did you know? |
| error | 65 | p64_s9 | Shorten the translation to at most 6 characters so it fits the original box (the current translation of 8 characters overflows its box; the minimum allowed size is 55%) | 艺术节 | Art Fest |
| error | 65 | p64_s9 | Shorten the translation to at most 6 characters so it fits the original box (the current translation of 8 characters overflows its box; the minimum allowed size is 55%) | 艺术节 | Art Fest |
| error | 67 | p66_s4 | Shorten the translation to at most 7 characters so it fits the original box (the current translation of 9 characters overflows its box; the minimum allowed size is 55%) | 48人 | 48 people |
| error | 67 | p66_s4 | Shorten the translation to at most 7 characters so it fits the original box (the current translation of 9 characters overflows its box; the minimum allowed size is 55%) | 48人 | 48 people |
| error | 69 | p68_s16 | Shorten the translation to at most 16 characters so it fits the original box (the current translation of 19 characters overflows its box; the minimum allowed size is 55%) | 淘气笑笑奇思 | Taoqi Xiaoxiao Qisi |
| error | 69 | p68_s16 | Shorten the translation to at most 16 characters so it fits the original box (the current translation of 19 characters overflows its box; the minimum allowed size is 55%) | 淘气笑笑奇思 | Taoqi Xiaoxiao Qisi |
| error | 69 | p68_s17 | Shorten the translation to at most 15 characters so it fits the original box (the current translation of 19 characters overflows its box; the minimum allowed size is 55%) | 淘气笑笑奇思 | Taoqi Xiaoxiao Qisi |
| error | 69 | p68_s17 | Shorten the translation to at most 15 characters so it fits the original box (the current translation of 19 characters overflows its box; the minimum allowed size is 55%) | 淘气笑笑奇思 | Taoqi Xiaoxiao Qisi |
| error | 73 | p72_s8 | Shorten the translation to at most 10 characters so it fits the original box (the current translation of 12 characters overflows its box; the minimum allowed size is 55%) | 你知道吗 | Did you know |
| error | 73 | p72_s8 | Shorten the translation to at most 10 characters so it fits the original box (the current translation of 12 characters overflows its box; the minimum allowed size is 55%) | 你知道吗 | Did you know |
| error | 79 | p78_s0 | Shorten the translation to at most 14 characters so it fits the original box (the current translation of 17 characters overflows its box; the minimum allowed size is 55%) | 吃西瓜 | Eating Watermelon |
| error | 79 | p78_s0 | Shorten the translation to at most 14 characters so it fits the original box (the current translation of 17 characters overflows its box; the minimum allowed size is 55%) | 吃西瓜 | Eating Watermelon |
| error | 89 | p88_s12 | Shorten the translation to at most 31 characters so it fits the original box (the current translation of 37 characters overflows its box; the minimum allowed size is 55%) | 千零五节。 | one thousand and five used batteries. |
| error | 89 | p88_s12 | Shorten the translation to at most 31 characters so it fits the original box (the current translation of 37 characters overflows its box; the minimum allowed size is 55%) | 千零五节。 | one thousand and five used batteries. |
| error | 89 | p88_s14 | Shorten the translation to at most 6 characters so it fits the original box (the current translation of 12 characters overflows its box; the minimum allowed size is 55%) | 京帅汇 | Jingshuaihui |
| error | 89 | p88_s14 | Shorten the translation to at most 6 characters so it fits the original box (the current translation of 12 characters overflows its box; the minimum allowed size is 55%) | 京帅汇 | Jingshuaihui |
| error | 103 | p102_s16 | Shorten the translation to at most 34 characters so it fits the original box (the current translation of 40 characters overflows its box; the minimum allowed size is 55%) | 分一组，下半年 | of the year in one group, second half... |
| error | 103 | p102_s16 | Shorten the translation to at most 34 characters so it fits the original box (the current translation of 40 characters overflows its box; the minimum allowed size is 55%) | 分一组，下半年 | of the year in one group, second half... |
| warning | 9 | p8_s7 | The translation overflows its box and was rendered at 21% of the original size; even a much shorter text would not fit, check this box in the preview | 女★★ | Girl ★★ |
| warning | 9 | p8_s7 | The translation overflows its box and was rendered at 21% of the original size; even a much shorter text would not fit, check this box in the preview | 女★★ | Girl ★★ |
| warning | 19 | p18_s15 | The translation overflows its box and was rendered at 45% of the original size; even a much shorter text would not fit, check this box in the preview | 答： | Answer: |
| warning | 19 | p18_s15 | The translation overflows its box and was rendered at 45% of the original size; even a much shorter text would not fit, check this box in the preview | 答： | Answer: |
| warning | 22 | p21_s2 | The translation overflows its box and was rendered at 27% of the original size; even a much shorter text would not fit, check this box in the preview | 百科 | Encyclopaedia |
| warning | 22 | p21_s2 | The translation overflows its box and was rendered at 27% of the original size; even a much shorter text would not fit, check this box in the preview | 百科 | Encyclopaedia |
| warning | 22 | p21_s3 | The translation overflows its box and was rendered at 24% of the original size; even a much shorter text would not fit, check this box in the preview | 百科 | Encyclopaedia |
| warning | 22 | p21_s3 | The translation overflows its box and was rendered at 24% of the original size; even a much shorter text would not fit, check this box in the preview | 百科 | Encyclopaedia |
| warning | 22 | p21_s4 | The translation overflows its box and was rendered at 28% of the original size; even a much shorter text would not fit, check this box in the preview | 百科 | Encyclopaedia |
| warning | 22 | p21_s4 | The translation overflows its box and was rendered at 28% of the original size; even a much shorter text would not fit, check this box in the preview | 百科 | Encyclopaedia |
| warning | 23 | p22_s23 | The translation overflows its box and was rendered at 41% of the original size; even a much shorter text would not fit, check this box in the preview | 答： | Answer: |
| warning | 23 | p22_s23 | The translation overflows its box and was rendered at 41% of the original size; even a much shorter text would not fit, check this box in the preview | 答： | Answer: |
| warning | 25 | p24_s14 | The translation overflows its box and was rendered at 51% of the original size; even a much shorter text would not fit, check this box in the preview | 个 | items |
| warning | 25 | p24_s14 | The translation overflows its box and was rendered at 51% of the original size; even a much shorter text would not fit, check this box in the preview | 个 | items |
| warning | 32 | p31_s9 | The translation overflows its box and was rendered at 44% of the original size; even a much shorter text would not fit, check this box in the preview | 图 | Figure |
| warning | 32 | p31_s9 | The translation overflows its box and was rendered at 44% of the original size; even a much shorter text would not fit, check this box in the preview | 图 | Figure |
| warning | 40 | p39_s20 | The translation overflows its box and was rendered at 41% of the original size; even a much shorter text would not fit, check this box in the preview | 答： | Answer: |
| warning | 40 | p39_s20 | The translation overflows its box and was rendered at 41% of the original size; even a much shorter text would not fit, check this box in the preview | 答： | Answer: |
| warning | 51 | p50_s15 | The translation overflows its box and was rendered at 32% of the original size; even a much shorter text would not fit, check this box in the preview | 牙膏 | Toothpaste |
| warning | 51 | p50_s15 | The translation overflows its box and was rendered at 32% of the original size; even a much shorter text would not fit, check this box in the preview | 牙膏 | Toothpaste |
| warning | 53 | p52_s5 | The translation overflows its box and was rendered at 44% of the original size; even a much shorter text would not fit, check this box in the preview | 民 | Citizen |
| warning | 53 | p52_s5 | The translation overflows its box and was rendered at 44% of the original size; even a much shorter text would not fit, check this box in the preview | 民 | Citizen |
| warning | 53 | p52_s7 | The translation overflows its box and was rendered at 53% of the original size; even a much shorter text would not fit, check this box in the preview | 元 | yuan |
| warning | 53 | p52_s7 | The translation overflows its box and was rendered at 53% of the original size; even a much shorter text would not fit, check this box in the preview | 元 | yuan |
| warning | 57 | p56_s11 | The translation overflows its box and was rendered at 37% of the original size; even a much shorter text would not fit, check this box in the preview | 图 | Figure |
| warning | 57 | p56_s11 | The translation overflows its box and was rendered at 37% of the original size; even a much shorter text would not fit, check this box in the preview | 图 | Figure |
| warning | 57 | p56_s12 | The translation overflows its box and was rendered at 51% of the original size; even a much shorter text would not fit, check this box in the preview | 图 | Figure |
| warning | 57 | p56_s12 | The translation overflows its box and was rendered at 51% of the original size; even a much shorter text would not fit, check this box in the preview | 图 | Figure |
| warning | 71 | p70_s13 | The translation overflows its box and was rendered at 39% of the original size; even a much shorter text would not fit, check this box in the preview | 到 | it: |
| warning | 71 | p70_s13 | The translation overflows its box and was rendered at 39% of the original size; even a much shorter text would not fit, check this box in the preview | 到 | it: |
| warning | 77 | p76_s0 | The translation overflows its box and was rendered at 50% of the original size; even a much shorter text would not fit, check this box in the preview | 和 | and |
| warning | 77 | p76_s0 | The translation overflows its box and was rendered at 50% of the original size; even a much shorter text would not fit, check this box in the preview | 和 | and |
| warning | 100 | p99_s14 | The translation overflows its box and was rendered at 43% of the original size; even a much shorter text would not fit, check this box in the preview | 15米 | 15 m |
| warning | 100 | p99_s14 | The translation overflows its box and was rendered at 43% of the original size; even a much shorter text would not fit, check this box in the preview | 15米 | 15 m |

### `llm_review` — 76 errors, 83 warnings

| Severity | Page | Segment | Message | Source | Translation |
|---|---|---|---|---|---|
| error | 17 | p16_s3 | Reviewer (omission): The translation adds 'pine cones', which is not in the source label '100个'; only the counted object named in context may be supplied, and here the label itself is just '100'. Suggested translation: "100" | 100个 | 100 pine cones |
| error | 17 | p16_s4 | Reviewer (omission): The translation adds 'pine cones', which is not in the source label '100个'. Suggested translation: "100" | 100个 | 100 pine cones |
| error | 18 | p17_s22 | Reviewer (meaning): The source '212个' is a bare count with no unit; 'characters' is inferred. Acceptable if the exercise is about typing, but adding a unit not in the source is a deviation. Suggested translation: "212" | 212个。 | 212 characters. |
| error | 18 | p17_s25 | Reviewer (meaning): The source '309个' is a bare count with no unit; 'characters' is inferred. Acceptable if the exercise is about typing, but adding a unit not in the source is a deviation. Suggested translation: "309" | 309个 | 309 characters |
| error | 19 | p18_s0 | Reviewer (terminology): Heading '集邮' means 'Stamp collecting'; the single word 'Stamps' loses the activity name. Suggested translation: "Stamp Collecting" | 集邮 | Stamps |
| error | 20 | p19_s19 | Reviewer (omission): The source ends with 在 ("in"), which continues in the next item; the translation's blank placement loses the structure and the following item's blank. The two items together form '在___里填上'>''<'或...'. Suggested translation: "4. In" | 4.在 | 4. In |
| error | 20 | p19_s3 | Reviewer (omission): The source has no blank before '米' (剪一根跳绳要米长的绳子), so the blank '____' is an addition, and the source's missing measure word makes the sentence read oddly; keep as source but do not insert a blank if the source has none. Suggested translation: "Cutting one skipping rope needs ____ m of rope." | 剪一根跳绳要米长的绳子。 | Cutting one skipping rope needs ____ m of rope. |
| error | 23 | p22_s20 | Reviewer (terminology): The measure word 字 after the equation should be written as the counted noun 'characters', not left in parentheses. Suggested translation: "170×3=510 characters" | 170×3=510（字） | 170×3=510 (characters) |
| error | 24 | p23_s3 | Reviewer (omission): The measure word 个 names the counted object and is dropped, but the label should keep the counted noun. Suggested translation: "120" | 120个 | 120 |
| error | 24 | p23_s5 | Reviewer (omission): The measure word 个 names the counted object and is dropped, losing the label's meaning. Suggested translation: "?" | ？个 | ? |
| error | 25 | p24_s10 | Reviewer (omission): The measure word 个 names the counted object and is dropped, losing the label's meaning. Suggested translation: "700" | 700个 | 700 |
| error | 25 | p24_s11 | Reviewer (omission): The measure word 个 names the counted object and is dropped, losing the label's meaning. Suggested translation: "240" | 240个 | 240 |
| error | 25 | p24_s12 | Reviewer (omission): The measure word 个 names the counted object and is dropped, losing the label's meaning. Suggested translation: "130" | 130个 | 130 |
| error | 25 | p24_s13 | Reviewer (omission): The measure word 个 names the counted object and is dropped, losing the label's meaning. Suggested translation: "?" | ？个 | ? |
| error | 25 | p24_s14 | Reviewer (terminology): A bare measure word 个 is the counted noun, not 'items'. Suggested translation: "items" | 个 | items |
| error | 30 | p29_s0 | Reviewer (terminology): '练一练' should be translated 'Practice' per glossary; it is correctly 'Practice', but the same term in p29_s5 must be consistent. No issue here. | 练一练 | Practice |
| error | 32 | p31_s13 | Reviewer (terminology): '涂一涂' should be 'Colour'/'Color' per glossary ('涂一涂' not in glossary; 'Color' US spelling preferred). Spelling inconsistent. Suggested translation: "2. Colour." | 2.涂一涂。 | 2. Colour. |
| error | 33 | p32_s5 | Reviewer (untranslated): Source '图:②' has a stray colon; the translation 'Figure ②' is correct, no issue. | 图:② | Figure ② |
| error | 33 | p32_s9 | Reviewer (untranslated): Source '和' ('and') is a fragment joining two figures; standalone 'and' is incomplete but matches source truncation. Acceptable but combine with p32_s8/p32_s10. Suggested translation: "and" | 和 | and |
| error | 41 | p40_s26 | Reviewer (untranslated): The source has an opening quotation mark before 视窗 that is unmatched in the translation. Suggested translation: "In Taiwan, China, a "window" is used to record mental calculation results." | 我国台湾用“视窗来记录心算结果。 | In Taiwan, China, a "window" is used to record mental calcu… |
| error | 41 | p40_s28 | Reviewer (meaning): The translation turns a sentence statement ('can also calculate') into a bare noun phrase; it should keep the sentence meaning. Suggested translation: "Multiplication can also be calculated by drawing lines" | 用画线方法也可计算乘法 | Multiplication by drawing lines |
| error | 43 | p42_s21 | Reviewer (terminology): "火炬号轮船" is a ship name; rendering it as "the ship Huoju" loses the ship-name marker "号" (compare the parallel "Hongqi" below). Suggest "The steamship Huoju Hao" or keep the conventional name form. Suggested translation: "(1) The ship Huoju Hao departed from Port C and traveled east for 12 hours. Is it east or west of Port A? How many kilometers is it from Port A?" | （1）火炬号轮船从丙港出发，向东行驶了12时后，在甲港的东面还是西面？距甲港多少千米？ | (1) The ship Huoju departed from Port C and traveled east f… |
| error | 43 | p42_s28 | Reviewer (omission): "表示出来，" is only partially rendered: the verb "表示出来" (show/indicate) is rendered, but the source label is a fragment ending in a comma; the translation "mark it," is an acceptable rendering of the meaning, but note the source lacks an object—no change needed beyond wording. This is actually fine; flagging only the trailing comma consistency. | 表示出来， | mark it, |
| error | 46 | p45_s4 | Reviewer (terminology): "说一说" is rendered "Discuss"; the recurring instruction pattern elsewhere is "Talk about" / "Say". Keep terminology consistent across items. Suggested translation: "2. Talk about it and calculate." | 2.说一说，算一算。 | 2. Discuss and calculate. |
| error | 49 | p48_s8 | Reviewer (meaning): 萬大学 is not a person's name; it is garbled text likely standing for a brand or label. Translating it as "Wan University" invents a name and misleads learners. | 萬大学 | Wan University |
| error | 53 | p52_s10 | Reviewer (terminology): "量出" corresponds to the glossary term "Measure"; "add them up" is fine, but "Measure the length of each side" could use "Measure" phrasing consistently. Suggested translation: "Measure the length of each side, then add them up to compare." | 量出每边的长度，再加起来就能比较了。 | Measure the length of each side, then add them up to compar… |
| error | 53 | p52_s3 | Reviewer (terminology): Chinese textbook book titles are conventionally rendered "Mathematics" rather than "Math". Suggested translation: "Mathematics" | 数学 | Math |
| error | 55 | p54_s16 | Reviewer (number): The source has '11平方米地面上大约可站12名同学' (about 12 students can stand on 1 square metre, the first '1' being part of '1平方米'); the translation changed it to '11 square metre'. Suggested translation: "Use newspaper to make a square of 1 square metre. About 12 students can stand on 1 square metre of ground." | 用报纸拼一个1平方米的正方形。11平方米地面上大约可站12名同学 | Use newspaper to make a square of 1 square metre. About 12 … |
| error | 55 | p54_s9 | Reviewer (untranslated): The scanned-page placeholder ⟦0⟧ (image/answer box) was dropped from the translation, and the text seems merged. It should be kept in place. Suggested translation: "⟦0⟧ This square has side length 1 cm, and its area is..." | 216.12.0这个正方形，它的边长是1厘米，它的面积是··· | 216.12.0 This square has side length 1 cm, and its area i… |
| error | 56 | p55_s7 | Reviewer (untranslated): '目目' is left untranslated. Suggested translation: "eye eyes" | 目目 | 目目 |
| error | 58 | p57_s5 | Reviewer (omission): '大约是多少' (about how much / what is it approximately) is not rendered; the question is reduced to 'Estimate the area'. Suggested translation: "Estimate about how much the area of the classroom is" | 估计教室的面积大约是多少 | Estimate the area of the classroom |
| error | 59 | p58_s2 | Reviewer (terminology): Column labels 长/宽/面积 in a table should be lowercase ('length', 'width', 'area') for consistency with the table-heading style used in the same exercise. Suggested translation: "length" | 长 | Length |
| error | 59 | p58_s3 | Reviewer (terminology): Table column label should be lowercase 'width'. Suggested translation: "width" | 宽 | Width |
| error | 59 | p58_s4 | Reviewer (terminology): Table column label should be lowercase 'area'. Suggested translation: "area" | 面积 | Area |
| error | 59 | p58_s5 | Reviewer (terminology): The glossary pair 周长 => perimeter is correct, but the translation capitalises the term; in this label context 'Perimeter' is acceptable as a heading, yet the same term elsewhere is lowercase. This is a minor consistency issue. | 周长 | Perimeter |
| error | 61 | p60_s0 | Reviewer (terminology): Glossary pair 练一练 => Practice matches; correct. | 练一练 | Practice |
| error | 61 | p60_s17 | Reviewer (untranslated): 'Maths' is British spelling; acceptable, but the book cover label 数学 could be 'Mathematics'. Minor. | 数学 | Maths |
| error | 65 | p64_s22 | Reviewer (terminology): “轴对称图形” is rendered as "figures with line symmetry"; the more standard wording for this figure type is "axially symmetric figures". Suggested translation: "You can use axially symmetric figures." | 可以运用轴对称图形。 | You can use figures with line symmetry. |
| error | 70 | p69_s10 | Reviewer (meaning): 'Coach' should be the Coach model. Suggested translation: "The Coach model is on the left side of the top row..." | 教练号在最上面一排左侧····· | Coach is on the left of the top row... |
| error | 70 | p69_s3 | Reviewer (meaning): 'Taoqi and Lele' translates the model names 淘气号/乐乐号; the reference is to the named models, not the children. Suggested translation: "The Taoqi model and the Lele model are both on the left side of the cabinet, and the Taoqi model is above the Lele model." | 淘气号和乐乐号都放在柜子的左侧，淘气号在乐乐号的上面。 | Taoqi and Lele are both on the left side of the cabinet, an… |
| error | 70 | p69_s6 | Reviewer (meaning): Model names 奇思号/教练号 are rendered as the children's names. Suggested translation: "The Qisi model is not placed next to the Coach model." | 奇思号没有放在教练号的旁边。 | Qisi is not next to Coach. |
| error | 70 | p69_s7 | Reviewer (meaning): 'Where is Taoqi?' drops 号 (the Taoqi model). Suggested translation: "1. Where is the Taoqi model? Share your idea with your partner." | 1.淘气号在哪个位置？与同伴交流你的想法。 | 1. Where is Taoqi? Share your idea with your partner. |
| error | 70 | p69_s8 | Reviewer (meaning): 'Taoqi' should be the Taoqi model; the source's garbled '①，，③' is rendered as ①②③ which is acceptable, but the model reference is wrong. Suggested translation: "The Taoqi model is on the left side of the cabinet, so it may be in position ①, ② or ③." | 淘气号放在柜子的左侧，它可能在①，，③的位置 | Taoqi is on the left side of the cabinet, so it may be in p… |
| error | 70 | p69_s9 | Reviewer (meaning): Both 淘气号 and 乐乐号 are model names, not the children. Suggested translation: "The Taoqi model is above the Lele model, so it may be in position ① or ②." | 淘气号在乐乐号的上面它可能在①，②的位置。 | Taoqi is above Lele, so it may be in position ① or ②. |
| error | 74 | p73_s0 | Reviewer (meaning): '分一分 （二）' is the title of the section '(2) Divide', not the imperative 'Divide (2)'; the numeral marks the second part of the lesson. Suggested translation: "Divide (2)" | 分一分 （二） | Divide (2) |
| error | 74 | p73_s5 | Reviewer (omission): The sentence ends with the character 分, which introduces the fraction that follows in the next fragment; this trailing character is omitted. Suggested translation: "I colored 3 small squares in each color, taking up" | 我每种颜色都涂了3个小正方形，分 | I colored 3 small squares in each color, |
| error | 85 | p84_s14 | Reviewer (number): The tally marks use the character 正, which must be kept exactly; an extra 'T' was added before 正 that does not appear in the source. Suggested translation: "正" | T正 | T 正 |
| error | 85 | p84_s15 | Reviewer (number): The tally marks use 正 which must be kept exactly; an extra 'T' was added before 正正 that does not appear in the source. Suggested translation: "正正" | T正正 | T 正正 |
| error | 85 | p84_s16 | Reviewer (untranslated): The source character '下' is untranslated; it should be rendered in English. Suggested translation: "down 正" | 下正 | 下 正 |
| error | 85 | p84_s17 | Reviewer (number): The tally marks use 正 which must be kept exactly; an extra 'T' was added before 正 that does not appear in the source. Suggested translation: "正" | T正 | T 正 |
| error | 85 | p84_s18 | Reviewer (number): The tally marks 正T are reordered and spaced as '正 T'; the source order must be preserved. Suggested translation: "正T" | 正T | 正 T |
| error | 85 | p84_s19 | Reviewer (number): The tally marks 正T are reordered and spaced as '正 T'; the source order must be preserved. Suggested translation: "正T" | 正T | 正 T |
| error | 85 | p84_s5 | Reviewer (terminology): 'favourite' is British spelling; ensure consistency with US 'favorite' used elsewhere in the material. Suggested translation: "2. Class 3(2) voted for their favorite farm animal. The voting record is shown below." | 2.三（2）班选举大家最喜欢的农场里的动物，选举记录如下图。 | 2. Class 3(2) voted for their favourite farm animal. The vo… |
| error | 85 | p84_s6 | Reviewer (number): The source contains the number string '336.6.0' which must be kept verbatim; the placeholder-like digits appear unchanged, but the multiplication/× marker '×代表1票' is correctly rendered. Verify the leading digits match the source exactly. | 336.6.0（×代表1票） | 336.6.0 (× means 1 vote) |
| error | 87 | p86_s28 | Reviewer (meaning): '调查自己班同学的睡眠时间' means 'survey your own class's classmates' sleep time', not 'your own class's sleep time'. Also '并作出图来，与' should be 'and draw a chart to ...'. Suggested translation: "(4) Work in groups, survey your own class's classmates' sleep time, and draw a chart to" | （4）小组合作，调查自己班同学的睡眠时间，并作出图来，与 | (4) Work in groups, survey your own class's sleep time, and… |
| error | 88 | p87_s24 | Reviewer (meaning): '举例说一说怎样比较数的大小' means 'Give examples to talk about how to compare numbers', not 'Give examples of how to compare numbers'. Suggested translation: "3. Give examples to talk about how to compare numbers." | 3.举例说一说怎样比较数的大小。 | 3. Give examples of how to compare numbers. |
| error | 90 | p89_s15 | Reviewer (untranslated): Column label 角 (jiao) is left as pinyin; only 元 is conventionally romanized as yuan for a bare unit label. Consistency with the money convention suggests keeping the label pair as-is, but 'jiao' is not an English word. | 元角 | yuan jiao |
| error | 90 | p89_s16 | Reviewer (untranslated): Column label 角 (jiao) is left as pinyin; 'jiao' is not an English word. | 元角 | yuan jiao |
| error | 90 | p89_s17 | Reviewer (untranslated): Column label 角 (jiao) is left as pinyin; 'jiao' is not an English word. | 元角 | yuan jiao |
| error | 90 | p89_s18 | Reviewer (untranslated): Column label 角 (jiao) is left as pinyin; 'jiao' is not an English word. | 元角 | yuan jiao |
| error | 91 | p90_s2 | Reviewer (meaning): '应该' expresses should/must; the translation is acceptable but slightly weakens the obligation in a textbook instruction. Suggested translation: "How much change should be given back?" | 应该找回多少元？ | How much change should be given? |
| error | 92 | p91_s26 | Reviewer (untranslated): Column label 角 (jiao) is left as pinyin; 'jiao' is not an English word. | 元角 | yuan jiao |
| error | 92 | p91_s27 | Reviewer (untranslated): Column label 角 (jiao) is left as pinyin; 'jiao' is not an English word. | 元角 | yuan jiao |
| error | 92 | p91_s28 | Reviewer (untranslated): Column label 角 (jiao) is left as pinyin; 'jiao' is not an English word. | 元角 | yuan jiao |
| error | 92 | p91_s29 | Reviewer (untranslated): Column label 角 (jiao) is left as pinyin; 'jiao' is not an English word. | 元角 | yuan jiao |
| error | 93 | p92_s21 | Reviewer (meaning): The four scheme labels run together without separators; the source lists them as distinct labels, so spacing/punctuation should make them readable. Suggested translation: "Plan 1 Plan 2 Plan 3 Plan 4" | 方案1方案2方案3方案4 | Plan 1 Plan 2 Plan 3 Plan 4 |
| error | 94 | p93_s3 | Reviewer (omission): The trailing "哪些是····" is left as dots instead of translating the unfinished question. Suggested translation: "What quantities are in the information above? Which are mass units, and which are ..." | 上面的信息中有哪些量？哪些是质量单位，哪些是···· | What quantities are in the information above? Which are mas… |
| error | 94 | p93_s8 | Reviewer (number): The source has an answer blank omitted in the translation: "重约2" ends with "2" followed by an answer blank, which is missing. Suggested translation: "(1) An elephant weighs about 2 ___" | （1）一头大象重约2 | (1) An elephant weighs about 2 |
| error | 95 | p94_s0 | Reviewer (number): The answer blank after "今年的2月有天" is missing: the source has an answer blank where the number of days should be filled in, translated as "has ___ days" — actually this is present as "days" with blank inserted; but the source also has a blank between 有 and 天 rendered correctly. No change needed. | 3.（1）今年的2月有天，是（平、闰）年。 | 3. (1) February of this year has ___ days; it is a (common,… |
| error | 99 | p98_s15 | Reviewer (untranslated): "sm..." appears to be a scanned fragment; if it is an abbreviation of a unit it should be rendered, otherwise kept as is. Kept verbatim, acceptable. | sm... | sm... |
| error | 100 | p99_s1 | Reviewer (terminology): "9平方分米" is written as "9 square decimetres"; the non-standard spelling "decimetres" (and non-abbreviated unit) is inconsistent with the abbreviation style used elsewhere (dm); better "9 dm²". Suggested translation: "6. A footpath is 27 m long and 3 m wide. It is paved with square tiles of area 9 dm². How many such tiles are needed?" | 6.一条人行道长27米，宽3米。用面积是9平方分米的正方形地砖铺路，需要这样的地砖多少块？ | 6. A footpath is 27 m long and 3 m wide. It is paved with s… |
| error | 101 | p100_s0 | Reviewer (terminology): 'Movement of Figures' is a literal rendering; the standard unit title is 'Motion of Figures' or 'Transformations of Figures'. Suggested translation: "Motion of Figures" | 图形的运动 | Movement of Figures |
| error | 102 | p101_s12 | Reviewer (omission): The sentence is incomplete: the source ends with '公园在邮局的' followed by a blank for direction; the translation truncates the blank entirely. Same issue applies to p101_s13 and p101_s14. Suggested translation: "The park is to the ___ of the post office," | 公园在邮局的 | The park is to the |
| error | 102 | p101_s13 | Reviewer (omission): The blank（面/方向）is missing; the source has an answer blank after each '面'. Suggested translation: "___ of the post office, and the cinema is to the ___ of the shop," | 面，电影院在商店的 | of the post office, and the cinema is to the |
| error | 102 | p101_s14 | Reviewer (omission): The blank after '商店在育英小学' is missing; also the trailing clause is truncated. Suggested translation: "___ of the shop, and the shop is to the ___ of Yuying Primary School," | 面，商店在育英小学 | of the shop, and the shop is to the |
| error | 103 | p102_s2 | Reviewer (terminology): 'Farm' is acceptable for 养殖场 but 'livestock farm' or 'breeding farm' is more precise; consistency with p102_s1 'farm' is fine. | 养殖场 | Farm |
| warning | 4 | p3_s5 | Reviewer (format): Unit headings beginning with a bare Chinese numeral should be rendered 'Unit 3 Multiplication'; a bare '3 Multiplication' is unnatural. Suggested translation: "Unit 3 Multiplication" | 三乘法 | 3 Multiplication |
| warning | 4 | p3_s7 | Reviewer (format): Unit heading begins with a bare Chinese numeral: should be 'Unit 4 Kilograms, Grams and Tonnes' rather than '4 Kilograms, Grams, Tonnes'. Suggested translation: "Unit 4 Kilograms, Grams and Tonnes" | 四千克、克、吨 | 4 Kilograms, Grams, Tonnes |
| warning | 5 | p4_s0 | Reviewer (format): Unit heading begins with a bare Chinese numeral: '5 Area' should be 'Unit 5 Area'. Suggested translation: "Unit 5 Area" | 五面积 | 5 Area |
| warning | 5 | p4_s3 | Reviewer (format): Unit heading begins with a bare Chinese numeral: '7 Organizing and Representing Data' should be 'Unit 7 ...'. Suggested translation: "Unit 7 Organizing and Representing Data ·80" | 七数据的整理和表示·80 | 7 Organizing and Representing Data ·80 |
| warning | 7 | p6_s3 | Reviewer (grammar): 'Share them and calculate' is choppy; better to render 分一分，算一算 as 'Share and calculate.' Suggested translation: "Share these blocks equally among 2 senior classes. How many does each class get? Share and calculate." | 把这些积木平均分给2个大班，每班分到多少块？分一分，算一算。 | Share these blocks equally among 2 senior classes. How many… |
| warning | 11 | p10_s4 | Reviewer (format): The source item 2 ends without a full stop; the translation matches, but for consistency with item 1 a period is expected in a textbook sentence. Minor. Suggested translation: "2. First estimate how many digits the quotient has, then calculate." | 2.先估一估商是几位数，再计算 | 2. First estimate how many digits the quotient has, then ca… |
| warning | 16 | p15_s19 | Reviewer (format): Missing space after the enumerator '(2)'. Suggested translation: "(2) Ask another division question and try to answer it." | (2）请你再提出一个除法问题，并尝试解答。 | (2) Ask another division question and try to answer it. |
| warning | 17 | p16_s2 | Reviewer (format): Missing space after the enumerator '(2)'. Suggested translation: "(2) 216 pine cones are put equally into 2 baskets. How many in each basket?" | （2） 216个松果，平均装到2个篮子中，每篮装多少个？ | (2) 216 pine cones are put equally into 2 baskets. How many… |
| warning | 20 | p19_s35 | Reviewer (format): Book title rendered with digits and comma; the Chinese book title is conventionally translated as a single phrase. Number is acceptable. Suggested translation: "100,000 Whys" | 十万个为什么 | 100,000 Whys |
| warning | 21 | p20_s13 | Reviewer (format): Source '书架二退' contains a scanning artifact '退'; the translation omits it, which is reasonable, but note the heading label may need 'Bookcase 2'. Suggested translation: "Bookcase 2" | 书架二退 | Bookcase 2 |
| warning | 24 | p23_s13 | Reviewer (format): The enumeration '(1)' should be followed by a space. Suggested translation: "(1) How much does it cost to buy 9 toy cars like this?" | （1）买9辆这样的玩具车需要多少元？ | (1) How much does it cost to buy 9 toy cars like this? |
| warning | 24 | p23_s6 | Reviewer (format): The enumeration '2.' should be kept at the start of the translation. Suggested translation: "2. Draw and calculate." | 2.画一画，算一算。 | 2. Draw and calculate. |
| warning | 27 | p26_s6 | Reviewer (grammar): 'Fold and look at' is awkward; the instruction uses two separate actions. Suggested translation: "Fold Figure 1 on Appendix page 1 and look." | 利用附页1中图1折一折，看一看。 | Fold and look at Figure 1 on Appendix page 1. |
| warning | 31 | p30_s1 | Reviewer (grammar): 'How do they all move?' is awkward; 'How does each of them move?' is more natural. Suggested translation: "How does each of them move? Can you divide them into two groups by the way they move?" | 它们都是怎么运动的？你能按运动方式把它们分成两类吗？ | How do they all move? Can you divide them into two groups b… |
| warning | 31 | p30_s2 | Reviewer (grammar): Missing serial comma consistency; 'clock hands' fine, but 'The steering wheel, pinwheel, and clock hands' preferred. Suggested translation: "The steering wheel, pinwheel, and clock hands are all turning." | 方向盘、风车和表针都在转动。 | The steering wheel, pinwheel and clock hands are all turnin… |
| warning | 31 | p30_s6 | Reviewer (grammar): Missing period at end of sentence. Suggested translation: "These are examples of translation." | 这些是平移现象 | These are examples of translation |
| warning | 31 | p30_s7 | Reviewer (grammar): Missing period at end of sentence. Suggested translation: "These are examples of rotation." | 这些是旋转现象 | These are examples of rotation |
| warning | 32 | p31_s5 | Reviewer (grammar): 'set square' is British; 'triangle ruler' or 'set square' both fine. Consistency needed with '三角尺'. Suggested translation: "Translate the set square left 2 squares." | 把三角尺向左平移2格。 | Translate the set square left 2 squares. |
| warning | 32 | p31_s6 | Reviewer (grammar): 'Discuss how the pencil and the set square can be translated' — 'Discuss' for 说一说 is acceptable (glossary says '说一说' => 'Discuss'), fine. | 说一说，铅笔和三角尺怎样才能平移到图③的位置？ | Discuss how the pencil and the set square can be translated… |
| warning | 33 | p32_s1 | Reviewer (grammar): 'Translate Figure ① left 5 squares' — 'left by 5 squares' or 'left 5 squares' both acceptable; fine. | （1）把图①向左平移5格； | (1) Translate Figure ① left 5 squares; |
| warning | 34 | p33_s2 | Reviewer (grammar): "tell how you calculated" is slightly informal and omits "and say"; better: "and explain how you calculated." Suggested translation: "Calculate, and explain how you calculated." | 算一算，并说说你是如何计算的。 | Calculate, and tell how you calculated. |
| warning | 34 | p33_s23 | Reviewer (grammar): "can you directly write" is an unidiomatic word order; "can you write ... directly" is preferred. Suggested translation: "Based on 16×3=48, can you write the results of the number sentences below directly?" | 根据16×3=48，你能直接写出下面算式的结果吗？ | Based on 16×3=48, can you directly write the results of the… |
| warning | 35 | p34_s9 | Reviewer (grammar): "directly write" is an unidiomatic word order; "write ... directly" is preferred. Suggested translation: "2. Based on 24×20=480, write the results of the number sentences below directly." | 2.根据24×20=480，直接写出下面算式的结果。 | 2. Based on 24×20=480, directly write the results of the nu… |
| warning | 39 | p38_s3 | Reviewer (format): Missing sentence-final punctuation (period) present in the source. Suggested translation: "(2) Circle and explain what each step of the vertical form means." | （2）圈一圈，并说一说竖式每一步的意思 | (2) Circle and explain what each step of the vertical form … |
| warning | 45 | p44_s11 | Reviewer (grammar): "除法坚式" is a typo for "除法竖式"; the translation "vertical form of division" is correct, but note the source typo should ideally be reflected consistently. No change needed to the English. | 为什么除法坚式和加、减、乘法的形式不一样呢？ | Why is the vertical form of division different from that of… |
| warning | 48 | p47_s14 | Reviewer (grammar): The question begins with a lowercase letter and is capitalized inconsistently; as the continuation of the exercise sentence it should start with a capital. Suggested translation: "How many metres did it run per minute?" | 每分跑多少米？ | how many metres did it run per minute? |
| warning | 50 | p49_s12 | Reviewer (grammar): The phrase "Fill in the suitable units in ()" is ungrammatical and misses the place where the units should be written; it should read "in the blanks" (or "in the brackets"). Suggested translation: "2. Fill in the blanks with suitable units." | 2.在（）里填上合适的单位。 | 2. Fill in the suitable units in (). |
| warning | 50 | p49_s19 | Reviewer (format): The answer blank in the source is the full-width parentheses （）; the translation uses half-width () without spacing, which is inconsistent with the rendering elsewhere and slightly unclear. Suggested translation: "4000 g = ( ) kg" | 4000克=（）千克 | 4000 g = () kg |
| warning | 50 | p49_s20 | Reviewer (format): Same as p49_s19: the answer blank should keep the parentheses with a space or use the full-width form as in the source. Suggested translation: "8000 g = ( ) kg" | 8000克=（）千克 | 8000 g = () kg |
| warning | 51 | p50_s12 | Reviewer (format): Two labels run together without a separator; a comma or semicolon would read better as a textbook label. Suggested translation: "Elevator weight limit 1000 kg, capacity 13 people." | 电梯限重1000千克限乘13人 | Elevator weight limit 1000 kg, capacity 13 people. |
| warning | 52 | p51_s6 | Reviewer (accuracy): "weighs, and can talk" is incomplete: 重吧 corresponds to 大象最少也有2吨重吧 and 会说 to 会说话的鹦鹉, so the fragment should read "heavy, and can talk". Suggested translation: "heavy, and can talk" | 重吧，会说 | weighs, and can talk |
| warning | 53 | p52_s5 | Reviewer (format): The single character 民 is a book-cover fragment; "Citizen" is an acceptable literal rendering, but it stands out as unrelated. Consider "the people" or leave as a proper book title element. Suggested translation: "Citizen" | 民 | Citizen |
| warning | 53 | p52_s9 | Reviewer (format): Missing sentence-final period in the translation; the source ends without punctuation after 试一试, but the first sentence should end cleanly. Suggested translation: "Compare: which figure has the larger area? Cut out figure 3 on appendix page 2 and try." | 比一比，哪个图形的面积大？剪下附页2中图3试一试 | Compare: which figure has the larger area? Cut out figure 3… |
| warning | 54 | p53_s2 | Reviewer (format): "Hands-on" is an abbreviation-like compressed heading; a fuller rendering is "Do it yourself." Suggested translation: "2. Do it yourself." | 2.动手做。 | 2. Hands-on. |
| warning | 54 | p53_s8 | Reviewer (format): The enumerator (2) should be kept at the start of the translation. Suggested translation: "(2) Can you design a pattern with the same area as figure ②? Draw it in figure 1 on appendix page 3." | （2）你能设计一个与图②面积相等的图案吗？在附页3图1中画一画。 | (2) Can you design a pattern with the same area as figure ②… |
| warning | 57 | p56_s3 | Reviewer (grammar): Wording is telegraphic; a natural textbook phrasing is preferable. Suggested translation: "3 in each row, exactly 2 rows, so the area is:" | 每排摆3个，正好摆2排，所以面积是： | 3 in each row, exactly 2 rows, so the area is: |
| warning | 57 | p56_s8 | Reviewer (format): Table header formatting: units should be separated from the labels consistently. Suggested translation: "length/cm\|width/cm" | 长/厘米\|宽/厘米 | length/cm\|width/cm |
| warning | 59 | p58_s10 | Reviewer (format): 'dm' abbreviation; see p58_s8. | 8分米 | 8 dm |
| warning | 59 | p58_s13 | Reviewer (format): The source is an exercise instruction; 'Think and draw' is acceptable, though 'Think, then draw' better reflects 想一想，画一画. Suggested translation: "8. Think, then draw" | 8.想一想，画一画 | 8. Think and draw |
| warning | 59 | p58_s6 | Reviewer (format): The source lists three items; the translation runs them together without separators. Adding commas or line breaks would improve readability. Suggested translation: "Cover of a maths book, floor of the classroom, floor of a room at home" | 数学书封面教室的地面家里一个房间的地面 | Cover of a maths book Floor of the classroom Floor of a roo… |
| warning | 59 | p58_s8 | Reviewer (format): The standard abbreviation for decimetre is 'dm', but 'dm' is not a listed standard unit abbreviation in the guidelines; 'decimetres' would be more consistent, though 'dm' is standard. Minor. | 5分米 | 5 dm |
| warning | 61 | p60_s10 | Reviewer (grammar): Source is truncated ('也就是6000'); translation matches. Acceptable. | （2）教室地面的面积大约是60（），也就是6000 | (2) The area of the classroom floor is about 60 (), that is… |
| warning | 61 | p60_s11 | Reviewer (grammar): Source is truncated ('也就是42000'); translation matches. Acceptable. | （3）篮球场的面积大约是420（），也就是42000 | (3) The area of the basketball court is about 420 (), that … |
| warning | 61 | p60_s12 | Reviewer (grammar): 'Who is right?' is fine; no issue. | 4.谁说得对？ | 4. Who is right? |
| warning | 61 | p60_s9 | Reviewer (grammar): The source has two blanks （） （）; translation keeps '()' which reads acceptably. Minor. | 黑板的面积大约是400（），也就是4（）。 | The area of the blackboard is about 400 (), that is, 4 (). |
| warning | 62 | p61_s6 | Reviewer (grammar): The blank should precede the unit phrase: 'is about () long' is ungrammatical; it should read 'is about () in length' or place the blank after 'long' as 'is about 2 () long' with the blank replacing the unit. The natural correction is 'A skipping rope is about 2 () long.' — but as written the blank is misplaced. Suggested translation: "A skipping rope is about 2 () long." | （1）一根跳绳长约2（）。 | (1) A skipping rope is about 2 () long. |
| warning | 64 | p63_s6 | Reviewer (grammar): 'The closer the length and width, the area...' is an incomplete comparative construction; wording should mirror 'the closer..., the ... the area'. Suggested translation: "The closer the length and width, the more the area..." | 长和宽越接近，面积.·· | The closer the length and width, the area... |
| warning | 71 | p70_s12 | Reviewer (format): The clause 我是这样得到 is split across items; 'This is how I got' should be joined with the following fragment. Suggested translation: "This is how I got" | 我是这样得 | This is how I got |
| warning | 71 | p70_s5 | Reviewer (format): Garbled source fragment 'VWm' kept verbatim; it likely stands for a small picture/box, but no placeholder is available, so a descriptive rendering would be clearer. | VWm | VWm |
| warning | 73 | p72_s6 | Reviewer (format): The isolated connector 和 is rendered as 'and'; in a label it is more naturally written with a capital 'And'. Suggested translation: "And" | 和 | and |
| warning | 75 | p74_s2 | Reviewer (format): The four-dot ellipsis '····' is kept as four middle dots; an ellipsis should be used. Suggested translation: "There are 5 ducks in total. I want to circle ..." | 一共有5只鸭子，我要圈出···· | There are 5 ducks in total. I want to circle ···· |
| warning | 75 | p74_s8 | Reviewer (grammar): British spelling 'Colour' versus American 'Color' elsewhere; inconsistent casing/spelling in exercise instructions. Suggested translation: "(1) Color and fill in" | （1）涂一涂，填一填 | (1) Colour and fill in |
| warning | 76 | p75_s6 | Reviewer (grammar): 'Boys make up' is incomplete; it should include a blank for the fraction, e.g. 'Boys make up ____'. Suggested translation: "Boys make up ____" | 男生占全部小朋友的 | Boys make up |
| warning | 77 | p76_s10 | Reviewer (format): The source uses an ellipsis with several dots (······); the translation uses three dots. Minor punctuation mismatch. Suggested translation: "In Grade 5 we will learn more…" | 五年级时，我们还会再学习的····· | In Grade 5 we will learn more... |
| warning | 77 | p76_s3 | Reviewer (grammar): 'Both divide the square into 4 equal parts' is awkward; 'Both are made by dividing the square into 4 equal parts' or 'Both squares are divided into 4 equal parts' reads better. Suggested translation: "Both are made by dividing the square into 4 equal parts; the more parts coloured, the larger the fraction." | 都是把正方形平均分成4份，涂的份数越多，这个分数就越大。 | Both divide the square into 4 equal parts; the more parts c… |
| warning | 77 | p76_s5 | Reviewer (format): The label context suggests this 'and' joins two fractions; as a standalone label it should keep initial capitalisation if it begins a line. Suggested translation: "and" | 和 | and |
| warning | 77 | p76_s6 | Reviewer (format): The label context suggests this 'and' joins two fractions; as a standalone label it should keep initial capitalisation if it begins a line. Suggested translation: "and" | 和 | and |
| warning | 77 | p76_s8 | Reviewer (format): The label context suggests this 'and' joins two fractions; as a standalone label it should keep initial capitalisation if it begins a line. Suggested translation: "and" | 和 | and |
| warning | 78 | p77_s1 | Reviewer (grammar): 'Colour' is British spelling; the source curriculum uses British spelling consistently, so this is fine, but 'compare' should be lowercase and consistent capitalization — minor style. | 1.涂一涂，比一比 | 1. Colour and compare |
| warning | 84 | p83_s0 | Reviewer (format): Source heading '七 数据的整理和表示' is a unit heading beginning with a bare numeral; per convention it should be 'Unit 7 Organizing and Presenting Data'. The translation includes a stray code '332.1.0' — keep as in source. Suggested translation: "Unit 7 Organizing and Presenting Data 332.1.0" | 七 数据的整理和表332.1.0示 | Unit 7 Organizing and Presenting Data332.1.0 |
| warning | 84 | p83_s11 | Reviewer (grammar): Continuation fragment; combined with p83_s9 it should read 'I put shoes of the same size together.' | 放在一起． | together. |
| warning | 84 | p83_s18 | Reviewer (format): The ellipsis '···' (3 dots) should be rendered as an English ellipsis '...' (three dots). Suggested translation: "The largest boys' shoe size is 38, the smallest is..." | 男生鞋最大号码是38号最小号码是··· | The largest boys' shoe size is 38, the smallest is... |
| warning | 86 | p85_s10 | Reviewer (format): Height numbers run together without separators. Suggested translation: "Group 3 138 142" | 第三小组138142 | Group 3 138142 |
| warning | 86 | p85_s11 | Reviewer (format): Height numbers run together without separators. Suggested translation: "Group 6 138 132 147" | 第六小组138132147 | Group 6 138132147 |
| warning | 86 | p85_s12 | Reviewer (format): Trailing interpunct '·' after 厘米 in the source is a stray mark; the translation drops it, which is acceptable. | 我发现第四小组有一个同学身高151厘米· | I found that one student in Group 4 is 151 cm tall. |
| warning | 86 | p85_s3 | Reviewer (grammar): Continuation fragment; combined with p85_s2: 'buy half-price tickets?'. | 能够买半价票吗？ | buy half-price tickets? |
| warning | 86 | p85_s6 | Reviewer (format): '第-小组' rendered as 'Group 1'; the hyphen-style dash in the source likely denotes '第一小组' (Group 1) and the numbers should be spaced for readability. Suggested translation: "Group 1 139 142 140 140 135 146" | 第-小组139142140140135146 | Group 1 139142140140135146 |
| warning | 86 | p85_s7 | Reviewer (format): Height numbers run together without separators; they should be spaced for readability. Suggested translation: "Group 4 139 137 136 138 151" | 第四小组139137136138151 | Group 4 139137136138151 |
| warning | 86 | p85_s8 | Reviewer (format): Height numbers run together without separators. Suggested translation: "Group 2 129 140" | 第二小组129140 | Group 2 129140 |
| warning | 87 | p86_s10 | Reviewer (format): The source label '7时7时30分' contains two adjacent time labels '7时' and '7时30分'; the translation merges them into '7 h 7 h 30 min' without a separator, which reads like a single malformed time. Suggested translation: "7 h 7 h 30 min" | 7时7时30分 | 7 h 7 h 30 min |
| warning | 93 | p92_s18 | Reviewer (format): Parallel label 'Number of big boats' omits the counted noun 'Number of ...'; should read consistently with the other column label. Suggested translation: "Number of small boats" | 小船/条 | Small boats |
| warning | 94 | p93_s16 | Reviewer (format): Line breaks inside one item preserved; no change needed. | 5分=（）秒 4000克=（）千克 6角=（）分 | 5 min = () s 4000 g = () kg 6 jiao = () fen |
| warning | 94 | p93_s9 | Reviewer (format): Full-width closing parenthesis and period handling; source has no period after the blank, minor inconsistency only. Suggested translation: "(2) A camel weighs about 420 ()" | (2）一头骆驼重约420（） | (2) A camel weighs about 420 () |
| warning | 96 | p95_s5 | Reviewer (format): The four shape names run together without separators; spacing should separate the list items. Suggested translation: "cube cuboid cylinder sphere" | 正方体长方体圆柱球 | cube cuboid cylinder sphere |
| warning | 96 | p95_s6 | Reviewer (format): The four shape names run together without separators; spacing should separate the list items. Suggested translation: "rectangle square triangle parallelogram" | 长方形正方形三角形平行四边形 | rectangle square triangle parallelogram |
| warning | 97 | p96_s3 | Reviewer (format): The instruction "连一连" (Match) should follow the glossary term "Match" and the sentence is fine. | 3.下面这些照片分别是坐在哪把椅子上看到的？连一连 | 3. Which chair was each of these photos taken from? Match t… |
| warning | 98 | p97_s1 | Reviewer (format): The sentence is split across items p97_s1 and p97_s2; the split point is preserved, which is fine. | 1.我们学过哪些长度单位、哪些面积单位？整理一下，并与同伴说 | 1. Which units of length and which units of area have we le… |
| warning | 100 | p99_s10 | Reviewer (grammar): Missing article after 'with side'; should read 'with a side of 20 cm' or 'with side length 20 cm'. Suggested translation: "8. Cut a square piece of paper with a side of 20 cm into 4 identical small square pieces. What are the perimeter and area of each small square?" | 8.将一张边长为20厘米的正方形纸，剪成4个完全一样的小正方形纸片，每个小正方形的周长和面积分别是多少？ | 8. Cut a square piece of paper with side 20 cm into 4 ident… |
| warning | 100 | p99_s13 | Reviewer (grammar): 'square metres' uses British spelling while item p100_s8 uses 'favourite', which is fine, but the material consistently uses 'metres'; keeping is acceptable. No meaning change. | （1）花坛的面积是多少平方米？ | (1) What is the area of the flower bed in square metres? |
| warning | 100 | p99_s6 | Reviewer (format): A figure label should not be capitalized mid-sentence style; label casing inconsistent with other labels (e.g., "living room"). Suggested translation: "living room" | 客厅 | Living room |
| warning | 102 | p101_s18 | Reviewer (format): The blank（）should be preserved as an answer blank, not rendered as empty parentheses '()'. Suggested translation: "Taoqi is to the ___ of Xiaoxiao; Xiaoxiao is to the ___ of Taoqi." | 淘气在笑笑的（）面；笑笑在淘气的（）面。 | Taoqi is to the () of Xiaoxiao; Xiaoxiao is to the () of Ta… |
| warning | 103 | p102_s23 | Reviewer (format): The source uses the Chinese ellipsis '···'; the translation uses spaced dots '···' style, which is acceptable, but direct speech is missing for a fill-in-style sentence. No meaning change. | 我们班男生比女生多··· | Our class has more boys than girls ··· |
| warning | 103 | p102_s8 | Reviewer (format): The blank（）should be preserved as an answer blank, not empty parentheses '()'. Suggested translation: "(4) The farm is to the ___ of the primary school." | （4）养殖场在小学的（）面。 | (4) The farm is to the () of the primary school. |

### `numbers` — 1 error, 0 warnings

| Severity | Page | Segment | Message | Source | Translation |
|---|---|---|---|---|---|
| error | 95 | p94_s0 | Number "2" from the source is missing in the translation; keep every number exactly as written in the source | 3.（1）今年的2月有天，是（平、闰）年。 | 3. (1) February of this year has ___ days; it is a (common,… |

### `placeholders` — 1 error, 0 warnings

| Severity | Page | Segment | Message | Source | Translation |
|---|---|---|---|---|---|
| error | 95 | p94_s0 | Placeholder problem: missing placeholders: ⟦2⟧. Keep every ⟦n⟧ placeholder of the source exactly once, unchanged, at the matching position (⟦2⟧ = "2") | 3.（1）今年的2月有天，是（平、闰）年。 | 3. (1) February of this year has ___ days; it is a (common,… |

### `target_script` — 1 error, 0 warnings

| Severity | Page | Segment | Message | Source | Translation |
|---|---|---|---|---|---|
| error | 28 | p27_s6 | Only 0% of the letters in the translation are in the English script; write the whole translation in English (formulas, variable names, units and proper names copied from the source excepted) | 江山美如画 | 江山美如画 |

### `untranslated` — 7 errors, 0 warnings

| Severity | Page | Segment | Message | Source | Translation |
|---|---|---|---|---|---|
| error | 27 | p26_s2 | 1 letter(s) of the source script remain untranslated ("囍"); translate all text into English | 囍 | 囍 |
| error | 27 | p26_s8 | 1 letter(s) of the source script remain untranslated ("囍"); translate all text into English | 囍 | 囍 |
| error | 28 | p27_s6 | 5 letter(s) of the source script remain untranslated ("江山美如画"); translate all text into English | 江山美如画 | 江山美如画 |
| error | 56 | p55_s7 | 2 letter(s) of the source script remain untranslated ("目目"); translate all text into English | 目目 | 目目 |
| error | 61 | p60_s19 | 2 letter(s) of the source script remain untranslated ("幂", "积"); translate all text into English | 在古代，为了确定农业收成，计算税收，必须丈量土地，由此对面积产生了认识。中国古代形象地用“幂”字或“积”字来表示面积。 | In ancient times, people had to measure land to work out ha… |
| error | 61 | p60_s20 | 2 letter(s) of the source script remain untranslated ("幂", "积"); translate all text into English | 幂：遮盖物品的方形布；积：积累。你能理解这两个字的意思吗？ | 幂 (mì): a square cloth for covering things; 积 (jī): to pile… |
| error | 65 | p64_s18 | 1 letter(s) of the source script remain untranslated ("世"); translate all text into English | 把汉字“世”与“2010”完美结合。 | It neatly combines the character “世” (shì) with "2010". |

### `image_text` — 0 errors, 22 warnings

| Severity | Page | Segment | Message | Source | Translation |
|---|---|---|---|---|---|
| warning | 15 | p14_i56_8 | The text '200÷2=100,502比' was left in the source language (inline pictograms the OCR cannot read (left in the picture)): the line is built around symbols or pictures the OCR could not read - check the page in the preview | 200÷2=100,502比 |  |
| warning | 15 | p14_i56_8 | The text '200÷2=100,502比' was left in the source language (inline pictograms the OCR cannot read (left in the picture)): the line is built around symbols or pictures the OCR could not read - check the page in the preview | 200÷2=100,502比 |  |
| warning | 30 | p29_i116_7 | The text '做一做。画“”' was left in the source language (unreadable symbol in quotes (left in the picture)): the line is built around symbols or pictures the OCR could not read - check the page in the preview | 做一做。画“” |  |
| warning | 30 | p29_i116_7 | The text '做一做。画“”' was left in the source language (unreadable symbol in quotes (left in the picture)): the line is built around symbols or pictures the OCR could not read - check the page in the preview | 做一做。画“” |  |
| warning | 49 | p48_i192_5 | The text '克可以用“kg”表示，克' was left in the source language (inline pictograms the OCR cannot read (left in the picture)): the line is built around symbols or pictures the OCR could not read - check the page in the preview | 克可以用“kg”表示，克 |  |
| warning | 49 | p48_i192_5 | The text '克可以用“kg”表示，克' was left in the source language (inline pictograms the OCR cannot read (left in the picture)): the line is built around symbols or pictures the OCR could not read - check the page in the preview | 克可以用“kg”表示，克 |  |
| warning | 62 | p61_i244_1 | The text '1.用红色描出图形的边线，用蓝色涂出图形的面。' was left in the source language (inline pictograms the OCR cannot read (left in the picture)): the line is built around symbols or pictures the OCR could not read - check the page in the preview | 1.用红色描出图形的边线，用蓝色涂出图形的面。 |  |
| warning | 62 | p61_i244_1 | The text '1.用红色描出图形的边线，用蓝色涂出图形的面。' was left in the source language (inline pictograms the OCR cannot read (left in the picture)): the line is built around symbols or pictures the OCR could not read - check the page in the preview | 1.用红色描出图形的边线，用蓝色涂出图形的面。 |  |
| warning | 71 | p70_i280_9 | The text '\ue000280.9.l\ue001表示，读' was left in the source language (inline pictograms the OCR cannot read (left in the picture)): the line is built around symbols or pictures the OCR could not read - check the page in the preview | 280.9.l表示，读 |  |
| warning | 71 | p70_i280_9 | The text '\ue000280.9.l\ue001表示，读' was left in the source language (inline pictograms the OCR cannot read (left in the picture)): the line is built around symbols or pictures the OCR could not read - check the page in the preview | 280.9.l表示，读 |  |
| warning | 73 | p72_i288_21 | The text '记号“”表示分' was left in the source language (unreadable symbol in quotes (left in the picture)): the line is built around symbols or pictures the OCR could not read - check the page in the preview | 记号“”表示分 |  |
| warning | 73 | p72_i288_21 | The text '记号“”表示分' was left in the source language (unreadable symbol in quotes (left in the picture)): the line is built around symbols or pictures the OCR could not read - check the page in the preview | 记号“”表示分 |  |
| warning | 77 | p76_i304_0 | The text '比大小' was left in the source language (inline pictograms the OCR cannot read (left in the picture)): the line is built around symbols or pictures the OCR could not read - check the page in the preview | 比大小 |  |
| warning | 77 | p76_i304_0 | The text '比大小' was left in the source language (inline pictograms the OCR cannot read (left in the picture)): the line is built around symbols or pictures the OCR could not read - check the page in the preview | 比大小 |  |
| warning | 77 | p76_i304_20 | The text '我出题你来比' was left in the source language (inline pictograms the OCR cannot read (left in the picture)): the line is built around symbols or pictures the OCR could not read - check the page in the preview | 我出题你来比 |  |
| warning | 77 | p76_i304_20 | The text '我出题你来比' was left in the source language (inline pictograms the OCR cannot read (left in the picture)): the line is built around symbols or pictures the OCR could not read - check the page in the preview | 我出题你来比 |  |
| warning | 87 | p86_i344_43 | The text '三（2）班的同学对比，两个班同学的睡眠时间有什么不同吗？' was left in the source language (inline pictograms the OCR cannot read (left in the picture)): the line is built around symbols or pictures the OCR could not read - check the page in the preview | 三（2）班的同学对比，两个班同学的睡眠时间有什么不同吗？ |  |
| warning | 87 | p86_i344_43 | The text '三（2）班的同学对比，两个班同学的睡眠时间有什么不同吗？' was left in the source language (inline pictograms the OCR cannot read (left in the picture)): the line is built around symbols or pictures the OCR could not read - check the page in the preview | 三（2）班的同学对比，两个班同学的睡眠时间有什么不同吗？ |  |
| warning | 88 | p87_i348_34 | The text '4.请分别画图表示' was left in the source language (inline pictograms the OCR cannot read (left in the picture)): the line is built around symbols or pictures the OCR could not read - check the page in the preview | 4.请分别画图表示 |  |
| warning | 88 | p87_i348_34 | The text '4.请分别画图表示' was left in the source language (inline pictograms the OCR cannot read (left in the picture)): the line is built around symbols or pictures the OCR could not read - check the page in the preview | 4.请分别画图表示 |  |
| warning | 102 | p101_i404_18 | The text '的面。' was left in the source language (inline pictograms the OCR cannot read (left in the picture)): the line is built around symbols or pictures the OCR could not read - check the page in the preview | 的面。 |  |
| warning | 102 | p101_i404_18 | The text '的面。' was left in the source language (inline pictograms the OCR cannot read (left in the picture)): the line is built around symbols or pictures the OCR could not read - check the page in the preview | 的面。 |  |
