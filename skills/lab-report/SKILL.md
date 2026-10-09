---
name: lab-report
description: >
  Write experiment and lab reports from source materials (lab manuals, PPT, Word, PDF).
  Use when the user needs a lab report, experiment report, 实验报告, 课程报告,
  or any structured writeup based on experiment procedures.
---

# Lab Report — 要求与流程

**要求**：根据用户材料（讲义/PPT/Word/PDF/数据/截图/日志）产出一份结构完整、数据真实、
语言与用户一致的实验报告。禁止编造实验结果——没有的数据标注"未提供"或询问用户。
危险命令（删除、提权、格式化等）任何模式下都必须先确认。

## 流程

1. **建档**：运行 `scripts/profile_config.py status` 读取本地学生信息（存于
   `~/.auto-college/lab-report/profile.json`，缺什么问什么，只问一次）。
   自建输出目录 `outputs/<experiment-name>/`（含 `screenshots/`、`raw_outputs/`）；
   多文件输入用 `scripts/index_source_files.py` 生成清单。
   有课程模板时用 `scripts/course_templates.py get/save` 复用。
2. **分类**（能推断就不问）：
   - `standard-executable`：材料含可执行命令 → 执行实验，记录 `run_log.md` 与 `raw_outputs/`；
   - `data-provided`：用户已有数据/截图 → 直接进入写作；
   - `paper-only`：理论/总结类 → 无需执行。
3. **执行**（仅 standard-executable）：普通命令失败可跳过并在交付时说明；
   运行证据截图统一用 **terminal-screenshot** skill 生成，存入 `screenshots/`。
4. **成稿**：按 `templates/catalog.md` 选模板（课程模板优先，内置 zh/en 十段式
   默认兜底）写 `final_report.md`；默认交付 **md + docx**，pdf 按需。
   数学公式保留 LaTeX 源（行内 `$...$`、块级 `$$...$$`），导出 docx 时转 OMML。
   图片统一 PNG、宽 ≤16cm、图注"图 N-M 说明"（宋体 10.5pt 居中），>2MB 先压缩。
   公式与图片规范详见 `references/export-guide.md`。

## 输出

全部产物放 `outputs/<experiment-name>/`（gitignored），不得写入 skill 源码目录。
依赖：Python（scripts）、terminal-screenshot（截图）、官方 pdf/docx skill（读写与导出）。
