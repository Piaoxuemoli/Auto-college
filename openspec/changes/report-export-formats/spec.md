# Spec Delta: report-export-formats

## ADDED Requirements

### Requirement: 导出格式矩阵

默认 md + docx 双交付；pdf 用户要求时按需（路径随 T5 结论）；
草稿/迭代场景 md-only；导出失败回退交付 md + 说明。

#### Scenario: 默认交付

- **WHEN** 报告成稿且用户未指定格式
- **THEN** 交付 `final_report.md` 与同名 docx

#### Scenario: 导出失败

- **WHEN** docx 导出环节失败
- **THEN** 交付 md 并附失败原因，流程不中断
