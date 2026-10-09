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

成稿按 `templates/catalog.md` 选模板，顺序：课程模板（`scripts/course_templates.py`
get/save，存 `~/.auto-college/lab-report/course_templates.json`）→ 用户模板 →
学科默认（如 `templates/computer-network-template.md`）→ 内置默认
（`templates/report-template-zh.md` / `-en.md`，十段式）。任一环节缺失安全落下一级。

### Requirement: 输出目录

全部产物放 `outputs/<experiment-name>/`（含 `screenshots/`、`raw_outputs/`，
gitignored），不得写入 skill 源码目录。多文件输入用
`scripts/index_source_files.py` 生成清单。

### Requirement: 导出与公式

- 默认交付 **md + docx** 双格式，pdf 按需（docx→pdf 优先，官方 pdf skill 备选），
  草稿迭代可 md-only；docx 失败时交付 md + 失败原因说明；
- 数学公式：源 MD 保留 `$...$` / `$$...$$`，docx 导出转 OMML（官方 docx skill
  优先，pandoc 回退，双失败以代码字体呈现并在交付说明注明）；
- 图片：统一 PNG、宽 ≤16cm、图注 `图 N-M 说明`（zh）/ `Figure N-M: caption`（en）
  居中 10.5pt 不加粗、相对路径引用 `screenshots/`、>2MB 先压缩、缺图用占位说明。
  细则见 `references/export-guide.md`。

### Requirement: 图片生成适配层

插图（装置图/流程图）可由 `scripts/image_gen.py` 生成：配置
`~/.auto-college/image-gen.json`（schema 见 `references/image-gen.md` 与
`configs/image-gen.example.json`），任何 OpenAI-compatible images API 均可。
退出码 0/1/2 对齐三档哲学；`--emit-prompt` 无配置时产出可复用 prompt 文件
（exit 0）；api_key 全程脱敏、绝不入库。
