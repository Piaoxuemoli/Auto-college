# lab-report — 能力基线

> 只描述当前已实现且为真的系统。改动走 `openspec/changes/`，归档时才合并进本文。

## Purpose

从用户材料（讲义/PPT/Word/PDF/数据/截图/日志）产出结构完整、数据真实、
语言与用户一致的实验报告。禁止编造实验结果——没有的数据标注"未提供"或询问
用户；危险命令（删除、提权、格式化等）任何模式下必须先确认。

## Requirements

### Requirement: 本地 profile 复用

学生信息存 `~/.auto-college/lab-report/profile.json`，
`scripts/profile_config.py status` 读取；缺什么问什么，只问一次。

#### Scenario: 首次建档

- **WHEN** profile.json 不存在或字段缺失
- **THEN** 询问用户补齐后落盘，后续会话不再重复询问

### Requirement: 三条报告路径

按材料分类，能推断不询问：

- `standard-executable`：材料含可执行命令 → 执行实验，记录 `run_log.md`
  与 `raw_outputs/`；
- `data-provided`：用户已有数据/截图/日志 → 直接进入写作；
- `paper-only`：理论/总结类 → 无需执行。

### Requirement: 运行证据截图

运行证据统一由 terminal-screenshot skill 生成，存
`outputs/<experiment-name>/screenshots/`。普通命令失败可跳过并在交付时说明。

### Requirement: 模板优先级

成稿模板顺序：课程模板（`scripts/course_templates.py` get/save，存
`~/.auto-college/lab-report/course_templates.json`）→ 用户模板 → 内置十段式
（`references/report-template-zh.md` / `-en.md`）。

### Requirement: 输出目录

全部产物放 `outputs/<experiment-name>/`（含 `screenshots/`、`raw_outputs/`，
gitignored），不得写入 skill 源码目录。多文件输入用
`scripts/index_source_files.py` 生成清单。

### Requirement: 导出

用户要求或模板需要时用官方 docx/pdf skill 导出（格式矩阵见
report-export-formats 变更）。
