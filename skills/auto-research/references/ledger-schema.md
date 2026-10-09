# 证据台账与核对脚本

`scripts/research_audit.py` 是离线核对工具（Python 3.9+ 标准库，不联网、不训练、不读账户、不自动运行）。它核对**登记的一致性**，不是科学正确性的裁判。记录格式的可读规格见 `assets/ledger-schema.json`。

## 用法与退出码

新项目初始化（已有状态则拒绝覆盖，退出码 2）：

```text
python scripts/research_audit.py init --root /your/project --topic "你的真实课题"
```

init 创建 `RUN_STATE.json`、`PROJECT_CONTEXT.md`、`ROADMAP.md`（后两者从 `assets/` 模板复制并写入主题）、空的 `ledger/claims.jsonl` 与 `ledger/references.jsonl`，以及 `paper/`、`experiments/`、`results/`、`figures/`、`reviews/` 目录。

一致性核对：

```text
python scripts/research_audit.py audit --root /your/project
```

| 退出码 | 含义 |
| --- | --- |
| 0 | init 成功，或 audit 登记一致性通过 |
| 1 | audit 发现不一致（`issues` 非空） |
| 2 | 输入或文件错误（如缺 ledger、状态已存在、JSON 解析失败） |

输出为 stdout 上的 JSON，含 `issues`、`warnings`、`numeric_checks`、`structural_consistency_passed` 与 `submission_gate_recorded`。检查项：重复 ID、引用状态与验证笔记、证据路径、常见 TeX cite key、literal `\input`/`\include` 文件存在性、登记数值、提交候选检查记录。

## references.jsonl 字段

| 字段 | 说明 |
| --- | --- |
| id | 唯一 citation key |
| title / authors / year / venue | 真实标题、按序作者、年份、发表场所或预印本库 |
| doi / url | 真实 DOI（如有）与一手来源 URL |
| status | `verified` \| `partial` \| `unresolved` \| `excluded` |
| checked_at | 实际核对的 ISO 日期 |
| verification_file | 验证笔记路径（如 `ledger/verification/actual-note.md`） |

`verified` 状态要求上述字段齐全且验证笔记文件真实存在。

## claims.jsonl 字段

| 字段 | 说明 |
| --- | --- |
| id / text | 唯一主张 ID 与主张文本 |
| role | `primary` \| `mechanism` \| `boundary` \| `background` |
| kind | `empirical` \| `theoretical` \| `literature` \| `proposal` |
| status | `supported` \| `refuted` \| `inconclusive` \| `untested` |
| reference_ids | 相关已验证引用 key |
| evidence_files | 项目相对路径的证据文件 |
| numbers | 登记数字规格列表（见下） |

约束：`empirical`/`theoretical` 主张标 `supported` 必须有证据文件；`literature` 主张标 `supported` 必须有已验证引用；`proposal` 不能标 `supported`。

## RUN_STATE.json 字段

| 字段 | 说明 |
| --- | --- |
| phase | 当前阶段 `S0`-`S8` |
| deliverable_level | `plan` \| `draft` \| `complete` \| `submission_candidate` |
| manuscript | 稿件路径（如 `paper/main.tex`） |
| checks | 五项检查状态：`scientific_review`、`citation_review`、`numeric_review`、`compilation`、`visual_review`，取值 `pending` \| `passed` \| `failed` \| `not_applicable` |
| check_evidence | 各检查的证据笔记路径（如 `reviews/actual-review.md`） |
| not_applicable_reasons | 标 `not_applicable` 时填写的真实理由 |
| next_action | 一个具体的待办动作 |
| autostart | 必须恒为 `false` |

## 数字规格（numbers 项）

数字源支持 JSON 单对象/对象列表与 JSONL。字段：

- `source_file`：项目相对路径的结果文件；
- `key`：dotted key（如 `metrics.acc`）定位数值；
- `where`：精确匹配筛选（如 `{"method": "A"}`），筛选后至少剩一行；
- `operation`：`identity`（恰好一行）| `mean` | `std`（样本标准差，至少两行）| `sum` | `count`；
- `scale`：单位换算系数（默认 1）；
- `value`：论文中如实出现的数字；
- `tolerance`：绝对容差（默认 1e-6，非负）；
- `unit_id_key`：可选，仅用于确实应该一行一个统计单位的聚合输入；选中行中该 key 重复即报错。不能用它把合法的重复测量误判为重复样本。较复杂分析先由经过验证的专用脚本导出汇总，再用 `identity` 核对。

例子：真实结果 JSONL 有三行 `{method: "A", subject: "S1", score: 0.8}` 等；数字规格中 `source_file` 指向该结果文件，`key` = `score`，`where` = `{"method": "A"}`，`operation` = `mean`，`scale` = 100，`value` 填论文中的百分数，`unit_id_key` = `subject`。记录里的 `value` 必须来自论文真实值，不能照抄本例创造结果。

## 提交候选门（submission_candidate）

空计划可以通过一致性，但 `submission_gate_recorded` 始终为 false。提交候选必须：

1. 有真实稿件文件、非空 claims、至少一个 primary 主张；
2. 所有 primary 主张状态为 `supported`；
3. 五项检查均为 `passed` 且有实际证据笔记，或为 `not_applicable` 且有理由记录。

该字段只说明登记要求满足，不能证明审阅者做对了，也不是录用或投稿授权。

## 限制清单

脚本不做以下任何事，仍需真实科学核验与全文数字覆盖检查：

- 不自动访问 DOI，不逐字段核 BibTeX；
- 不解析任意 TeX 宏（只覆盖 literal `\input`/`\include` 与常见 cite 命令，动态宏需人工审阅）；
- 不自动判断混杂、推导、统计单位和配图是否正确；
- 不证明所有正文数字均已登记。

不要为了获得通过制造验证笔记或把 `pending` 改成 `passed`。
