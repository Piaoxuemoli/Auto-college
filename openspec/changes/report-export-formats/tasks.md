# Tasks: report-export-formats

> 待其他工作区实现后勾选；验收标准是可验证的判定，不是描述。

- [ ] 1. 交付矩阵定稿：md/docx/pdf 的默认与按需规则写入本提案并同步 roadmap T4。
  验收：矩阵覆盖"默认交付 / 用户要求 / 草稿迭代"三类场景。
- [ ] 2. docx 双交付链路。
  验收：standard-executable 与 data-provided 各出一份样本报告，
  md 与 docx 内容一致、图片完整（依赖 T3）。
- [ ] 3. pdf 路径决策：结合 T5 结论二选一（docx→pdf 或 LaTeX 直出）。
  验收：决策 + 理由记录进 roadmap T4；出一份 pdf 样本。
- [ ] 4. md-only 快速路径。
  验收：用户要草稿时只产 md，不触发导出。
- [ ] 5. 失败回退。
  验收：docx 导出失败场景下交付 md + 失败原因说明。
- [ ] 6. 文档与归档：更新 `docs/lab-report.md`；spec delta 合并进
  `openspec/specs/lab-report/spec.md`。
  验收：文档与实现一致；tasks 全勾。
