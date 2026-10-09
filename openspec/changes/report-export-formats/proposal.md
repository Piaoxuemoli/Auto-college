# Proposal: report-export-formats

- 议题：T4 实验报告导出格式（见 `docs/roadmap.md`）
- 状态：draft（roadmap 默认建议：md + docx 双交付，pdf 按需）

## 为什么

当前"需要时用官方 docx/pdf skill 导出"没有格式矩阵：交付什么、何时给 pdf、
导出失败怎么回退，全靠临场判断，交付质量不可控。

## 做什么

- 默认交付：md + docx 双交付（docx 兼容性最好，交作业场景刚需）；
- pdf 按需：用户明确要求时导出；实现路径等 T5 结论——公式层若走 OMML/docx，
  则 pdf 优先 docx→pdf；引入 LaTeX 管线后可选 LaTeX 直出；
- md-only 快速路径：草稿/迭代预览场景只交付 md，不触发导出；
- 回退：docx 导出失败时交付 md + 失败说明，不阻断。

## 取舍

- 不默认三格式全交付：pdf 体积/时间成本高，多数场景用不上；
- pdf 路径不提前锁死：与 T5 联动，避免返工；
- 不自研导出：继续依赖官方 docx/pdf skill，本仓库只定义契约与验收。
