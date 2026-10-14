# English translations of the 北师大版 primary-school mathematics textbooks

Twelve volumes (grades 1-6, 上册 and 下册), translated from Chinese into English by the `mathtrans`
pipeline on branch `claude/gracious-ride-64zqsv`: OCR of the scanned pages, DeepSeek translation with
a textbook glossary and conventions, three automatic QA rounds, editable English text laid over the
cleaned page images, and a page-by-page proofreading pass in which every translated page was compared
with its Chinese source (picture against picture) and the corrections were applied before export
("Fixes" below). Page layout, pictures and colours are kept. The QR-code page (page 2 of the print
edition) is left out, so each English volume has one page fewer than the print edition.

To download a file: open it, then use **Download raw file** (the download icon at the top right).

| Volume | | Pages | Size | Fixes | File | QA report |
|---|---|---|---|---|---|---|
| 一年级上册 | Grade 1 Vol.1 | 108 | 45 MB | 366 | [Mathematics Grade 1 Volume 1.pdf](Mathematics%20Grade%201%20Volume%201.pdf) | [QA report](reports/Mathematics%20Grade%201%20Volume%201%20-%20QA%20report.md) |
| 一年级下册 | Grade 1 Vol.2 | 98 | 38 MB | 293 | [Mathematics Grade 1 Volume 2.pdf](Mathematics%20Grade%201%20Volume%202.pdf) | [QA report](reports/Mathematics%20Grade%201%20Volume%202%20-%20QA%20report.md) |
| 二年级上册 | Grade 2 Vol.1 | 119 | 44 MB | 441 | [Mathematics Grade 2 Volume 1.pdf](Mathematics%20Grade%202%20Volume%201.pdf) | [QA report](reports/Mathematics%20Grade%202%20Volume%201%20-%20QA%20report.md) |
| 二年级下册 | Grade 2 Vol.2 | 108 | 38 MB | 93 | [Mathematics Grade 2 Volume 2.pdf](Mathematics%20Grade%202%20Volume%202.pdf) | [QA report](reports/Mathematics%20Grade%202%20Volume%202%20-%20QA%20report.md) |
| 三年级上册 | Grade 3 Vol.1 | 110 | 41 MB | 95 | [Mathematics Grade 3 Volume 1.pdf](Mathematics%20Grade%203%20Volume%201.pdf) | [QA report](reports/Mathematics%20Grade%203%20Volume%201%20-%20QA%20report.md) |
| 三年级下册 | Grade 3 Vol.2 | 112 | 39 MB | 105 | [Mathematics Grade 3 Volume 2.pdf](Mathematics%20Grade%203%20Volume%202.pdf) | [QA report](reports/Mathematics%20Grade%203%20Volume%202%20-%20QA%20report.md) |
| 四年级上册 | Grade 4 Vol.1 | 115 | 42 MB | 118 | [Mathematics Grade 4 Volume 1.pdf](Mathematics%20Grade%204%20Volume%201.pdf) | [QA report](reports/Mathematics%20Grade%204%20Volume%201%20-%20QA%20report.md) |
| 四年级下册 | Grade 4 Vol.2 | 117 | 39 MB | 821 | [Mathematics Grade 4 Volume 2.pdf](Mathematics%20Grade%204%20Volume%202.pdf) | [QA report](reports/Mathematics%20Grade%204%20Volume%202%20-%20QA%20report.md) |
| 五年级上册 | Grade 5 Vol.1 | 125 | 40 MB | 910 | [Mathematics Grade 5 Volume 1.pdf](Mathematics%20Grade%205%20Volume%201.pdf) | [QA report](reports/Mathematics%20Grade%205%20Volume%201%20-%20QA%20report.md) |
| 五年级下册 | Grade 5 Vol.2 | 111 | 34 MB | 852 | [Mathematics Grade 5 Volume 2.pdf](Mathematics%20Grade%205%20Volume%202.pdf) | [QA report](reports/Mathematics%20Grade%205%20Volume%202%20-%20QA%20report.md) |
| 六年级上册 | Grade 6 Vol.1 | 117 | 38 MB | 1002 | [Mathematics Grade 6 Volume 1.pdf](Mathematics%20Grade%206%20Volume%201.pdf) | [QA report](reports/Mathematics%20Grade%206%20Volume%201%20-%20QA%20report.md) |
| 六年级下册 | Grade 6 Vol.2 | 119 | 43 MB | 774 | [Mathematics Grade 6 Volume 2.pdf](Mathematics%20Grade%206%20Volume%202.pdf) | [QA report](reports/Mathematics%20Grade%206%20Volume%202%20-%20QA%20report.md) |

## Known limitations

These are the kinds of imperfection the proofreading pass could not fix by changing text; the QA report
of each volume lists the automatic findings per page for a human check.

- Lines that the OCR split into fragments (around answer blanks, inline pictures or fractions) are
  translated fragment by fragment; the pieces read correctly together but may be set in different sizes,
  and a fraction or picture kept at its fixed place can land mid-sentence in the reflowed English.
- Labels in very narrow cells stay in Chinese or are small: place-value columns of counting frames,
  game tiles, coin and banknote inscriptions, map place names, table headers that span several cells.
- Characters the OCR did not detect stay in Chinese (text under the watermark, very small or decorative
  text, hand-written posters and notes, which are kept as pictures on purpose).
- Erasing is pixel-based: a stroke of an erased character, a bracket of an answer blank or a red
  highlighted term occasionally remains next to the English.
- Formula details the OCR cannot represent (repeating-decimal dots, superscripts, arrows, fraction bars)
  may be simplified in the line that carries them; numbers and formulas themselves are kept.
- Sentences built around small pictures (用○表示…) are set with the picture inline where it was found,
  otherwise without it or left in Chinese; this mostly affects grades 1-2.
