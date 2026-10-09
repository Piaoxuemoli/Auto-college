# Spec Delta: report-templates-catalog

## ADDED Requirements

### Requirement: 模板目录（templates catalog）

实验报告模板集中于 `skills/lab-report/templates/`，每个模板带 frontmatter 元数据
（name/scope/language/sections），`INDEX.md` 为唯一索引；加载时按需读取单个文件。

#### Scenario: 按需加载

- **WHEN** 成稿需要模板
- **THEN** 按"课程模板 → 用户偏好 → 学科默认 → 内置默认"顺序解析，命中即加载

#### Scenario: 无匹配

- **WHEN** 课程/学科/偏好均无记录
- **THEN** 落到内置十段式默认模板，成稿流程不中断

### Requirement: 用户模板偏好记忆

模板选择结果持久化于 `~/.auto-college/lab-report/`，同课程后续报告默认复用。

#### Scenario: 二次报告

- **WHEN** 同一课程再次成稿且用户未指定模板
- **THEN** 默认使用上次选择的模板
