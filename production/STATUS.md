# 进度存档 / Status — 2026-11-07

十二册北师大版小学数学英译的重建进度。容器重置后所有工作文件丢失，正在"一本一本"重建到最好质量。
下周从这里继续。

## 存在哪里

| 内容 | 位置 |
|---|---|
| 程序和生产工具（含本文件） | 分支 `claude/gracious-ride-64zqsv`：`mathtrans/`、`production/` |
| 每册的校对修改、未处理问题（flags）、第一阶段原始结果、OCR 缓存、后记文本 | 分支 `work-state`（`production/save_state.sh` 推送） |
| 已交付的英文书（上一版，经过检查） | 分支 `deliveries`：`Mathematics Grade N Volume M.pdf` |

容器再被重置也不怕：`production/restore_state.sh` 从 `work-state` 恢复全部修改（连同应用顺序）、原始结果和
OCR 缓存。已验证：恢复后应用修改，得到的书与现在的逐段完全相同（4425 段，文字和位置都一样）。

## 各册状态

| 册 | 第一阶段（OCR+机翻） | 找回检查版英文 | 第 1 遍校对 | 后续 | 交付 |
|---|---|---|---|---|---|
| 一上 g1_1 | ✓ | 622 段 | ✓ 14 批，校对+复核；共 1962 条修改全部生效，0 条被拒 | 待：25 条 flag、标题标签统一审查 | 预览版已发（未上 deliveries） |
| 一下 g1_2 | ✓ | 693 段 | — | — | 旧版 |
| 二上 g2_1 | ✓ | 1066 段 | — | — | 旧版 |
| 二下 g2_2 | ✗ DeepSeek 服务故障中断（已修复程序，需重跑；OCR 已缓存） | — | — | — | 旧版 |
| 三上 g3_1 | 停工时正在运行（见文末） | — | — | — | 旧版 |
| 三下 g3_2 – 六下 g6_2 | 未开始 | — | — | — | 旧版（g6_2 是重置前的最新质量版） |

g1_1 第 1 遍后的自动检查：2 个错误、506 个警告（第 1 遍校对前是 61 个错误）。剩下的问题在
`work-state:proof/g1_1/flags_p1.json`，主要是：

- 绿点小标题字号偏小（第 28、72、83、85 页）：渲染器把它们和气泡标签归为同类、按最小的定字号。
  这是程序问题，要改 `mathtrans/layout.py` 的同类标签匹配，不是逐条改文字。
- 第 84 页一个拆分段落顺序反了（拆分时行的顺序）。
- 第 67 页公交站牌：竖排文字有的向上读、有的向下读。
- 很小的位置放不下正常字号：书本封面、桌牌、站牌、小气泡（第 18、26、49、56、63、72、98、104 页），
  目前只能缩小或者保留。
- 目录第 3、7 单元的写法不一致（"Addition and Subtraction (1)" 和 "Add and Subtract (2)"）。
- 小标题大小写不统一（"Talk About It" 和 "Talk about it and fill in."）：交给标题标签审查。

## 本周做了什么

1. 生产工具全部写回仓库（`production/`，README 有每一步），以后不会再因重置丢失。
2. 程序修复（都有测试，全部测试通过；LibreOffice 那一项本容器跑不了，单独跳过）：
   - Python 3.13 下的 OCR：rapidocr 3 适配，固定用 PP-OCRv4 模型；修了"裁剪识别后整页识别不到字"的问题。
   - PyMuPDF 固定 1.28.2（交付版用的版本；2.1 会改变排版）。
   - DeepSeek 服务降级时返回 200 加空内容 "null"，以前会让整册中断，现在会重试（`ff99c85`）。
   - 英式拼写统一、黑板文字区加宽、每册英文后记（12 册都已排好）。
3. 存档：`save_state.sh` 也保存 flags；新增 `restore_state.sh`，恢复已验证。
4. g1_1 完整走完第 1 遍校对（28 个 agent：每批一个校对、一个独立复核）。

## 下周继续（按顺序）

```bash
cd /home/user/math-material-translation
pip install -r requirements.txt -r production/requirements.txt
# 如果容器被重置：恢复（源 PDF 先按 production/common.py 的 DRIVE_IDS 从 Google Drive 下载到 $BNU_WORK/books/）
bash production/restore_state.sh
# DeepSeek 密钥已作为网络凭据保存（api.deepseek.com），代码里用 DEEPSEEK_API_KEY=proxy-injected
```

1. **g1_1 收尾**：先修渲染器的同类标签字号问题，再跑 `workflows/flags_fix.js`
   （参数 `{volumes: [{code: "g1_1", title: "一年级上册", flags: <flags_p1.json 的 flags>}]}`）
   和 `workflows/labels_review.js`。然后 `cycle.sh g1_1`：交付到 deliveries，并在聊天里发压缩版。
2. **g1_2、g2_1**：`apply_corrections.py`，`han_left.py > han.txt`，`leftover_items.py`，`make_proof_pack.py`，
   跑 `proofread_pass.js`（pass 1），再走第 1 步的收尾流程。
3. **g2_2**：重跑第一阶段（`--skip-pages 2`，见 README 第 1 步），其余同上。
4. **g3_1 起**：每册第一阶段约 30–60 分钟（大部分时间在 DeepSeek 翻译和 QA 轮次）。可以在前一册校对时就在后台跑。
5. 每一步之后都跑 `save_state.sh`。

重置前在旧版里手工修过、需要再修一次的地方：g3_1 车票和气泡，g2_2 方格，g6_2 路名，g2_1 气泡，
g4_1 "做一做"，g2_2 标签，g5_1 "知识窗"底板（用 paint 修正重画）。

## 提醒

- 请更换以前在对话里用过的 Anthropic 和 DeepSeek 密钥（新的 DeepSeek 密钥已作为环境凭据保存，不在任何文件里）。
- 仓库是**公开**的，`deliveries` 分支里是整本教材扫描的英文版，请决定是否改为私有。

## 停工时的状态

g3_1 第一阶段：停工时正在排版和 QA 轮次（翻译已完成）。如果它在容器回收前跑完，原始结果已经存进
`work-state`；没有的话，下周重跑（OCR 已缓存）。
