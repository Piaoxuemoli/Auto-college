# 验证记录 — research-skills-distill

日期：2026-10-10。环境：Windows + Git Bash + Python 3.14.4（PYTHONUTF8=1）。

## 构建与复制保真

- 三个 skill 落地 `skills/auto-research/`、`skills/paper-writing/`、
  `skills/group-meeting-prep/`，符合 `openspec/project.md` 目录规范。
- `research_audit.py` 与四个 assets（ledger-schema.json + 三模板）与源包
  逐字节 cmp 一致（IDENTICAL ×5）。
- frontmatter：三个 SKILL.md 的 name/description 齐全且 name == 目录名
  （对安装副本逐个解析验证）。

## audit 实测矩阵（11/11 符合预期）

夹具与产物在 `skills/auto-research/outputs/audit-matrix/`（gitignored）。

| 编号 | 用例 | 预期 | 实际 |
| --- | --- | --- | --- |
| T1 | init 新项目 | exit 0 | exit 0，phase=S0、autostart=false |
| T2 | 已有状态再 init | exit 2 | exit 2，拒绝覆盖 |
| T3 | 空计划 audit | exit 0 且 gate=false | 符合 |
| T4 | 证据文件缺失 | exit 1 | "Missing evidence for c1" |
| T5a | mean×scale=90 核对 | exit 0，matches=true | actual 90.0 / reported 90 |
| T5b | value=91 数字不符 | exit 1 | "Number mismatch for c1" |
| T7 | TeX 未核实 cite key | exit 1 | "Unknown or unverified manuscript citation: foo2024" |
| T8 | 越界证据路径 `../` | exit 1 | "Evidence path escapes the project" |
| T9 | unit_id_key 重复统计单位 | exit 1 | "Repeated unit IDs" |
| T10 | 损坏 JSONL | exit 2 | JSON 解析报错 |
| T11 | verified 无核查笔记 + 提交门缺检查 | exit 1 | 7 项 issue 全部列出 |

中文主题"矩阵测试课题"经 init 落盘无乱码（PYTHONUTF8=1）。

## 去耦与中性化

- 去耦扫描：三个目录互 grep 其他 skill 名称，输出为空；各 skill 仅引用
  自身目录内文件。
- 中性扫描：源包品牌词、个人站点域名、真实用户名、个人硬件描述、
  api_key 字面量，输出为空。
- 干跑（均为结构演练，非真实研究）：
  - auto-research：p1 项目 init → 登记一条 verified 引用（含核查笔记）+
    一条 literature 主张 → audit exit 0 → 按模板写出 HANDOFF.md；
  - paper-writing：最近邻矩阵条目、填入真实路径的只读审稿提示词、
    去 AI 味改写一例（`outputs/dry-run/README.md`）；
  - group-meeting-prep：两个配图需求的路由判定（含未配置生图时的不生成
    判定）+ 四段备注骨架（`outputs/dry-run/README.md`）。

## 安装与发现

- 结构安装演练两处：`~/.auto-college/skill-validation/skills/` 与
  `<repo>/.zcode/skills/`（ZCode 工作区发现目录，gitignored），
  diff -r 与 skills/ 源一致。
- **未覆盖**：新会话内的真实发现与触发——本会话 skill 列表在启动时已加载，
  无法热验证；其他 agent 环境（Claude/Cursor）未实装。

## 未覆盖项（诚实声明）

- 真实科研任务的端到端使用（本批次为结构、脚本与流程演练）。
- 生图门禁的真实路由核实（本机未配置 image-gen.json，按设计走不生成分支）。
- 新会话发现性确认（task 7 因此保持未勾）。
