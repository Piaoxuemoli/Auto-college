# lab-report

实验报告精简流程 skill：本地信息复用 → 材料分类 → 执行实验（截图证据用
terminal-screenshot）→ 十段式模板成稿 → DOCX 导出。不编造实验结果，危险命令必须确认。

A streamlined lab-report skill: reusable local profile → material classification →
execute with terminal-screenshot evidence → ten-section template → DOCX export.
Never invents results; destructive commands always require confirmation.

## 流程 / Workflow

| 路径 / Path | 适用 / Use case |
|-------------|-----------------|
| `standard-executable` | 材料含可执行命令 → 执行实验并记录 / materials include runnable commands |
| `data-provided` | 用户已有数据、截图、日志 / user already has data |
| `paper-only` | 理论/总结类报告 / theoretical writeup |

1. **建档**：`python lab-report/scripts/profile_config.py status` 读取
   `~/.qoobee-skills/lab-report/profile.json`（缺什么问什么，只问一次）。
   自建 `outputs/<experiment-name>/`（含 `screenshots/`、`raw_outputs/`）。
2. **分类**：能推断不询问（见上表）。
3. **执行**（仅 standard-executable）：普通命令失败可跳过并在交付时说明；
   运行证据统一用 **terminal-screenshot** skill 生成，存入 `screenshots/`。
4. **成稿**：课程模板（`scripts/course_templates.py get/save`，存于
   `~/.qoobee-skills/lab-report/course_templates.json`）→ 用户模板 → 内置十段式
   默认模板（`references/report-template-zh.md` / `-en.md`）。需要时用官方
   docx/pdf skill 导出。

## 使用 / Usage

> "帮我写一份实验报告，实验手册是 lab3.pdf"

> "整理 ./lab3-materials，按计算机网络课程模板写实验报告，最后导出 Word"

## 文件结构 / File Structure

```
lab-report/
├── SKILL.md                      # 要求 + 流程 / requirements & workflow
├── references/
│   ├── report-template-zh.md     # 中文十段式模板 / Chinese 10-section template
│   └── report-template-en.md     # 英文模板 / English template
├── scripts/
│   ├── profile_config.py         # 本地信息缓存 / local profile cache
│   ├── course_templates.py       # 课程模板记忆 / course template memory
│   └── index_source_files.py     # 材料目录索引 / material indexing
└── outputs/                      # 用户输出（gitignored）/ outputs (gitignored)
```

## 依赖 / Dependencies

- **terminal-screenshot** — 运行证据截图 / run-evidence screenshots
- Anthropic official `docx` / `pdf` skills — 材料读取与导出 / reading & export
- Python 3

## 许可证 / License

MIT
