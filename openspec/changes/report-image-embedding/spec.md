# Spec Delta: report-image-embedding

## ADDED Requirements

### Requirement: 图片嵌入规范

报告图片统一：编号式图注（图 1-1 / Figure 1-1）、相对路径引用、最大宽度约束、
超阈值自动压缩（原图留 `raw_outputs/`）、图片缺失时图注占位回退。

#### Scenario: 导出 DOCX

- **WHEN** 成稿含截图且执行 docx 导出
- **THEN** 图片以约束宽度嵌入，图注编号连续且正确

#### Scenario: 图片缺失

- **WHEN** 引用的截图文件不存在
- **THEN** 交付物保留图注与占位说明，导出不失败
