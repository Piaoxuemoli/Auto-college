# Proposal: report-templates-catalog

- 议题：T1 实验报告模板选择（见 `docs/roadmap.md`）
- 状态：proposed（roadmap 倾向方案 ②）

## 为什么

内置十段式中英文模板 + 课程模板记忆已可用，但模板选择逻辑散在 SKILL.md 里：
缺"多模板候选 + 用户偏好记忆"，换课程/学科就要临场手写模板，无法沉淀。

## 做什么

模板目录化（roadmap 方案 ②）：

- 建 `skills/lab-report/templates/` 目录，按学科/课程分文件（`*.md` +
  frontmatter 元数据：name / scope / language / sections）；
- 选择顺序：课程模板（现有 course_templates 记忆）→ 用户偏好 → 学科默认 →
  内置默认；
- 加载时按需读取单个文件；SKILL.md 只保留选择决策表，不再内嵌模板正文。

## 取舍

- 放弃 ③ 模板 DSL（frontmatter 声明章节 + 生成器渲染）：当前规模下成本高于
  收益，Markdown 即模板已经够用；
- 放弃 ① 纯现状：无法沉淀学科差异，与 Epic"可迁移工作流"目标不符；
- 迁移期 `references/report-template-*.md` 原位保留（向后兼容），归档任务里
  再决定是否移除。
