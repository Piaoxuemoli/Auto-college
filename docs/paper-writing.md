# paper-writing

从真实材料与证据出发的科研调研、论文精读、成文、审稿与交付工作流 skill。
没有的数据、引用或结果不编造；未验证部分明确标注。自包含：引用核对为纯
流程规则（BibTeX + 核查笔记），不依赖其他 skill 或外部脚本。

A self-contained literature-to-delivery skill: source search and per-citation
verification, deep paper/code reading, claim-first writing with de-AI checks,
read-only independent review, and four honest delivery levels.

## 流程线 / Workflow

| 阶段 / Stage | 参考 / Reference | 产出 / Output |
|--------------|------------------|---------------|
| 调研：检索、引用核对 | `references/literature.md` | 最近邻矩阵、verified 引用 |
| 精读：论文与代码 | `references/literature.md` | 机制与代码对应、复现核对 |
| 成文：去重与去 AI 味 | `references/writing.md` | 证据主线完整的真实稿件 |
| 审稿：评估与迭代 | `references/review.md` | 定位意见、修复映射 |
| 交付：层级、打包、交接 | `references/delivery.md` | 成品、源文件、可续接状态 |

## 要点 / Highlights

- 引用状态机 `verified / partial / unresolved / excluded`，verified 须附核查笔记；
  替换引用时重查整句是否仍被支持。
- 去 AI 味四项检查（删除/异议/对比/位置测试）；措辞强度跟证据走
  （shows / supports / is consistent with / remains untested）。
- 只读独立审稿：冻结包 + 严重度定位到文件/页/节/公式/图/表/日志；
  同一对话内的角色审阅标为自审。
- 交付四级：研究方案 / 阶段稿 / 完整稿 / 提交候选——不存在承诺录用的层级。

详细规则见 `skills/paper-writing/SKILL.md`。
