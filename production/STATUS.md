# 进度存档 / Status — 2026-11-08 凌晨（暂停，等下周继续）

十二册北师大版小学数学（一年级上 g1_1 … 六年级下 g6_2）英译的重建进度。这份文件说明三件事：
**已经做了什么、还没做什么、下周按什么顺序做**。

背景：2026-11-06 容器被重置，当时的工作文件全部丢失，只剩之前交付在 `deliveries` 分支上的 PDF。
所以从 11-06 起整套流程是**重做的**：重新识别、重新机器翻译、把旧检查版的英文对回去、重新校对。
现在所有中间结果都存进了 git，**不会再因为重置丢失**。恢复方法见第 2 节。

---

## 1. 东西都存在哪里

| 内容 | 位置 | 说明 |
|---|---|---|
| 程序（`mathtrans/`）和生产工具（`production/`，含本文件） | 分支 `claude/gracious-ride-64zqsv` | |
| 每册的全部修改（`corr_*.json`，应用顺序记在 `times.json`）、未处理问题（`flags_*.json`）、第一阶段原始结果（`segments_base.json.gz`、`qa_report_base.json`）、OCR 缓存 | 分支 `work-state`，目录 `proof/<册>/`、`ocr_cache/` | 用 `production/save_state.sh` 推送，12 册都在，最新提交 `d03d398` |
| 交付的英文书（全分辨率）和 QA 报告 | 分支 `deliveries`，文件名 `Mathematics Grade N Volume M.pdf` | g1_1、g1_2 是这次重建后的新版，其余 10 册还是 11-06 之前的旧检查版 |
| 后记页 | 运行 `production/afterword_en.py <册…>`，从仓库里的 `afterword_vols.json` 生成 | 不用存档，随时能重新生成 |
| 源 PDF（中文扫描件） | Google Drive，ID 在 `production/common.py` 的 `DRIVE_IDS` | 容器重置后要重新下载到 `$BNU_WORK/books/<册>.pdf` |

存档里每册的内容（2026-11-08 核对过）：

| 册 | 原始结果 | 修改文件数 | flag 文件 |
|---|---|---|---|
| g1_1 | ✓ | 42 | ✓ |
| g1_2 | ✓ | 41 | ✓ |
| g2_1 | ✓ | 25 | ✓ |
| g2_2 | ✓ | 15 | ✓（只有校对员写的 flag，见第 3 节） |
| g3_1 – g6_2（8 册） | ✓ | 1（`corr_000_recovered.json`，找回的检查版英文） | — |

---

## 2. 下周开工：先检查环境，需要时恢复

```bash
cd /home/user/math-material-translation
git pull origin claude/gracious-ride-64zqsv
ls /tmp/piptest/real/proof 2>/dev/null   # 有 12 个目录：容器没被重置，直接干活
```

**如果容器被重置了**（`/tmp/piptest/real` 不存在）：

```bash
pip install -r requirements.txt -r production/requirements.txt   # PyMuPDF 必须是 1.28.2
bash production/restore_state.sh            # 从 work-state 恢复修改（连同顺序）、原始结果和 OCR 缓存，并挂上 deliveries
# 源 PDF：按 production/common.py 的 DRIVE_IDS 从 Google Drive 下载到 /tmp/piptest/real/books/<册>.pdf
#   （用 Google Drive 连接器的 download_file_content，或请用户上传）
python3 production/afterword_en.py g1_1 g1_2 g2_1 g2_2 g3_1 g3_2 g4_1 g4_2 g5_1 g5_2 g6_1 g6_2   # 后记页
for c in g1_1 g1_2 g2_1 g2_2; do PYTHONPATH=. python3 production/apply_corrections.py $c; done      # 重新渲染
```

恢复已经验证过：恢复后应用修改，得到的书和原来逐段完全一样。

DeepSeek 密钥作为网络凭据存在环境里（api.deepseek.com），代码里用 `DEEPSEEK_API_KEY=proxy-injected`。
12 册的第一阶段都已完成，下周**不再需要 DeepSeek**。

---

## 3. 每册现在的状态

一本书的完整流程如下，g1_1 和 g1_2 就是这样做完的：

1. 第一阶段：OCR 识别 + DeepSeek 机器翻译
2. 找回检查版英文（`recover_english.py`）
3. 准备校对材料：渲染 → `han_left.py` → `leftover_items.py` → `make_proof_pack.py`
4. **第 1 遍校对**（`proofread_pass.js` pass 1：一个 agent 校对，另一个独立复核）
5. 应用修改
6. **修 flag**（`flags_fix.js`）
7. **标题标签审查**（`labels_items.py` → `labels_review.js`）
8. **第 2 遍校对**（pass 2）。经验表明必须做，第 1 遍后还会剩下版面问题
9. 我亲自看几页，修个别页
10. 交付（`deliver.sh`），并在聊天里发压缩版

| 册 | 1 翻译 | 2 找回 | 3 准备 | 4 第 1 遍 | 6 修 flag | 7 标题标签 | 8 第 2 遍 | 10 交付 |
|---|---|---|---|---|---|---|---|---|
| 一上 g1_1 | ✓ | 622 段 | ✓ | ✓ | ✓ 20/23 | ✓ | ✓ | **✓** `751855b` |
| 一下 g1_2 | ✓ | 693 段 | ✓ | ✓ | ✓ 23/25 | ✓ | ✓ | **✓** `6c1340a` |
| 二上 g2_1 | ✓ | 1066 段 | ✓ | ✓ 848 处 | ✓ 26/28 | **待做**（`labels.json` 已生成，1483 项） | **待做** | 待做 |
| 二下 g2_2 | ✓ | 993 段 | ✓（旧版面） | **只做了一半**：14 批都写了修改（851 处，全部能应用），但复核一批都没跑 | 待做 | 待做 | 待做 | 待做 |
| 三上 g3_1 | ✓ | 1136 段 | ✓ 已做好：109 页，108 处问题，9 处题目偏小 | 待做 | | | | |
| 三下 g3_2 | ✓ | 975 段 | 做到一半停了，要重做 | 待做 | | | | |
| 四上 g4_1 | ✓ | 1097 段 | 待做 | | | | | |
| 四下 g4_2 | ✓ | 1184 段 | 待做 | | | | | |
| 五上 g5_1 | ✓ | 1228 段 | 待做 | | | | | |
| 五下 g5_2 | ✓ | 1125 段 | 待做 | | | | | |
| 六上 g6_1 | ✓ | 1310 段 | 待做 | | | | | |
| 六下 g6_2 | ✓ | 1232 段 | 待做 | | | | | |

g1_1、g1_2 还剩一些已知的小问题，原书在这些地方也没有空间，所以保持原样：

- 书封面上 4–6 磅的手写书名
- 桌牌、站牌、牙膏管上的小字
- 弧形拱门上的"儿童乐园"
- 几处擦字后的淡痕
- g1_2 第 27 页云朵图标前的小点（图标裁剪时自带的）

---

## 4. 下周按这个顺序做

**一次只跑一个校对类 workflow**（用户要求；几个一起跑也会互相抢 CPU）。
准备工作（渲染、OCR 检查、校对材料）不耗 token，可以同时在后台跑。

1. **g2_2：补做第 1 遍的复核。** 14 个 `corr_p1_*.json` 都还没复核过。
   - 推荐做法：先重新渲染、重做校对材料（它现在的校对材料是 11-08 版面修正之前做的），再跑一遍 **pass 2**，复核和第 2 遍一起完成。
   - 25 条 flag 在 `proof/g2_2/flags_p1.json`，都是校对员写的，没经过复核。
   - 之后照流程走第 6–10 步。
2. **g2_1：**
   - 先跑 `labels_review.js`，参数：`{"chunks":[{"code":"g2_1","title":"二年级上册","from":1,"to":40},{"code":"g2_1","title":"二年级上册","from":41,"to":80},{"code":"g2_1","title":"二年级上册","from":81,"to":118}]}`
   - 再重新渲染、重做校对材料，跑 pass 2，看几页，交付
3. **g3_1：** 材料已经准备好，直接跑 pass 1，然后走第 5–10 步。
4. **g3_2 g4_1 g4_2 g5_1 g5_2 g6_1 g6_2：** 每册先在后台准备材料，再走完整流程。准备材料的命令（`<c>` 换成册名）：
   ```bash
   cd production && P=/tmp/piptest/real/proof/<c>
   PYTHONPATH=.. python3 apply_corrections.py <c> && PYTHONPATH=.. python3 han_left.py <c> > $P/han.txt 2>$P/han.err \
     && PYTHONPATH=.. python3 leftover_items.py <c> $P/han.txt && PYTHONPATH=.. python3 make_proof_pack.py <c> && bash save_state.sh <c>
   ```
5. **最后：12 册一起做跨册一致性检查**（`labels_review.js` 的 consistency 阶段，参数里放 12 册各一段），让同一个中文标签在全套书里译法一样。这一步可能会改到已经交付的册，改完要把那些册重新交付。
6. **每一步做完都运行 `bash production/save_state.sh <册>`。**

各步骤的命令和参数：

- **校对：** Workflow `production/workflows/proofread_pass.js`，参数 `{"pass":1或2,"batch":8,"volumes":[{"code":"g3_1","title":"三年级上册","pages":[...]}]}`。页码取 `proof/<册>/index.json` 里的 `pages`（第 2 页和最后一页不在里面）。
- **收集 flag：** 每次校对或修 flag 之后，从该 workflow 的 `journal.jsonl` 里取 check 阶段的 flags，存成 `proof/<册>/flags_p<N>.json`。
- **修 flag：** Workflow `production/workflows/flags_fix.js`，参数 `{"batch":3,"volumes":[{"code","title","flags":[{"page","issue"}]}]}`。
- **交付：** `bash production/deliver.sh <册>`。交付前先跑 `collisions.py <册>`（结果要是 0）和 `size_outliers.py <册>`。

每册大约用掉的 token（子 agent）：

| 步骤 | token |
|---|---|
| 第 1 遍校对 | 4–5M |
| 修 flag | 2–2.5M |
| 标题标签审查 | 0.8M |
| 第 2 遍校对 | 3–3.5M |
| **每册合计** | **约 10–12M** |

剩下 10 册约 100M 以上。

---

## 5. 重置前手工修过、这次要重新检查的地方

这些修改在 11-06 的重置里丢了，新一轮校对不一定会碰到同样的地方，做到那一册时要专门去看：

- g2_1：气泡
- g2_2：方格、标签
- g3_1：车票、气泡
- g4_1："做一做"
- g5_1："知识窗"底板：源 PDF 已经换回原版，要先用 paint 修正重画底板，再用 add 放英文
- g6_2：路名

---

## 6. 这几天改过的程序（都已提交，测试通过，对所有册都有效）

| 提交 | 改了什么 |
|---|---|
| `ff99c85` | DeepSeek 服务降级时会返回空内容，以前整册会因此中断；现在会自动重试 |
| `2a306bb`、`972ef53` | 字号匹配：绿点小标题、"Practice" 标签和编号题目不再被并到气泡、计数器格子标签、被图片隔开的句子片段这些小字号上 |
| `3702d76` | 从旧版找回的英文里有连字 ﬁ/ﬂ，现在改成普通字母；重写了丢失的 `labels_items.py` |
| `c774752` | 句末省略号统一为 "…" |
| `b40d223` | 拆分段落时各行的顺序和校对文件里列出的顺序统一（以前会对不上，有几行位置互换） |
| `9d33bee` | 同时运行的复核 agent 以前共用一个临时文件夹，修改会串到别的批次；现在各用各的 |
| `f6972f9` | 术语统一：竖式 = column method，数位 = Tens / Ones |
| `restore_state.sh` | 从存档恢复全部工作，已验证 |

---

## 7. 提醒

- 请更换以前在对话里贴过的 Anthropic 和 DeepSeek 密钥。新的 DeepSeek 密钥只存在环境凭据里，不在任何文件里。
- 仓库是**公开**的，`deliveries` 分支里是整本教材的英文版（含原书插图），请决定要不要改成私有。
