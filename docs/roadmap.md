# Roadmap — TODO 与讨论进度

本文件是仓库唯一的议题跟踪文档：每个议题记录背景、候选方案、当前倾向与结论。
状态：`open`（未讨论）→ `discussing`（有候选方案）→ `decided`（已定结论）→ `done`（已实现）。
维护约定：讨论有新进展就更新对应条目；结论必须写"决策 + 理由"，不留口头共识。

## 已搁置

- **实机验证（M7 mac 金标准 / freeze·termframe 实测出图）**：暂不做。
  macOS 截图为非自由许可无法合法入库；外部渲染工具等实际使用时再装再验。

## 议题清单

### T1 实验报告模板选择 — `discussing`
现状：内置十段式中英文模板（`skills/lab-report/references/report-template-*.md`）+
课程模板记忆。问题：模板选择逻辑散在 SKILL.md 里，缺"多模板候选 + 用户偏好记忆"。
候选：①保持现状 ②模板目录化（templates/*.md 按学科/课程分文件，加载时按需选）
③模板 DSL（frontmatter 声明章节，生成器渲染）。
倾向：②——成本最低、可迁移性好，与 T6 工作流体系的"可迁移文档"目标一致。

### T2 截图 HTML 的字体 — `discussing`
现状：平台字体栈（Cascadia Mono/SF Mono/JetBrains Mono + 中文回退），渲染主机
缺字体时静默回退，字宽/观感漂移，跨平台可复现性受损。
候选：①自托管 woff2（Cascadia Code、JetBrains Mono 均为 OFL 许可，可入库）
②仅文档声明字体安装前置 ③Google Fonts CDN（离线不可用，排除）。
倾向：①——OFL 字体子集化后每平台 ~100KB，模板 `@font-face` 引用，彻底可复现。

### T3 实验报告图片嵌入 — `open`
现状：截图存 `outputs/<exp>/screenshots/`，MD 引用，DOCX 导出时靠官方 docx skill
插图。问题：未定义图注、编号、尺寸约束与失败回退。
待讨论点：图注格式（图1-1 式编号 vs 无编号）、自动压缩、中文图注字体。

### T4 实验报告导出格式 — `open`
候选：DOCX（官方 skill，兼容性最好）优先级是否保持；PDF 走 docx→pdf 还是
LaTeX（与 T5 联动）；是否提供 MD-only 快速路径。默认建议：md + docx 双交付，
pdf 按需。

### T5 LaTeX / 数学公式支持 — `open`
范围界定：报告内公式（`$...$` 渲染进 DOCX/PDF）vs 全文 LaTeX 模板（cspaper/实验
报告 LaTeX 类）两个层次。候选：①公式层：DOCX 用 OMML 转换（官方 skill 能力），
MD 保留 LaTeX 源 ②全文层：引入 pdf skill 的 LaTeX 管线做可选模板。
倾向：先①后②，公式是刚需，全文 LaTeX 是长尾。

### T6 图片生成 tool 可配置接入 — `discussing`
设想：用户可自由配置图片生成 API（如 image2 类服务），skill 需要插图（实验装置
示意图、流程图）时通过 tool 调用。
候选形态：①`~/.auto-college/image-gen.json` 配置 provider/base_url/model/api_key
+ 统一 `scripts/image_gen.py` 适配层（OpenAI-compatible 格式优先，多数服务兼容）
②等 agent 平台原生 image tool，只做 prompt 模板 ③两者都做：有配置走 ①，
否则降级 ②。
倾向：③——配置驱动 + 优雅降级，与三档渲染架构同一设计哲学。
安全问题：api_key 只存本地配置，模板/文档中绝不落盘。

### T7 安装目录策略 — `decided` → `done`（2026-10-08）
决策：安装器按环境自动检测（`.claude` → Claude Code，`.cursor` → Cursor）；
命令行/未知环境默认装 `.agent/skills`（不存在则新建），不再假设 Claude。
理由：仓库是 agent 中立的 skill 集合，不应绑定单一 agent 生态。
已实现：`setup.js` 已改；README 安装说明同步。**"交由 agent 依据环境自动配置"
的交互话术待补**（安装提示中引导 agent 自检环境）。

## 史诗（Epic）：个人工作流体系建设 — `discussing`

目标：在本仓库构筑一套**可迁移的个人工作流体系**——跨项目复用的文档化方法
（议题跟踪、规格驱动、验证闭环、多模态协作、安全钩子共存策略），并在日常
工作中持续验证迭代。

初步设计（待调研结论后定稿）：
- 方法选型：BMAD Method vs OpenSpec，调研进行中（结论稍后并入本文档）
- 最小落地：`docs/` 内议题文档（本文件）+ 变更提案模板 + 可迁移说明
- 验证方式：T1-T6 六个真实议题就是第一批工作负载，用它们跑通流程再抽象

### BMAD vs OpenSpec 调研结论 — `discussing`（待维护者拍板）

一句话定位：**BMAD** 是全生命周期敏捷 AI 开发框架（Analyst/PM/Architect/SM/Dev/QA
角色代理 + prd/architecture/story 工件，重规划）；**OpenSpec** 是轻量"人与 AI 的
契约层"（`openspec/` 下 project.md + specs/ + changes/ 提案驱动，纯 Markdown）。

| 维度 | BMAD (V6) | OpenSpec |
|---|---|---|
| 根目录 | `.bmad/` | `openspec/` |
| 核心工件 | agents/workflows/templates + prd、story | project.md、specs/、changes/{proposal,tasks} |
| 工具集成 | 按 IDE 生成文件（Cursor/Claude/Windsurf…） | 只靠 AGENTS.md + Markdown，任何 agent 零成本 |
| 单人维护 | 偏重（为团队协作设计） | 明显更优 |
| 可迁移 | 方法在框架里，升级即变 | 结构即方法，复制文件夹即迁移 |

**调研结论：OpenSpec 为主，吸收 BMAD 的 story 验收粒度。** 理由：①本仓库场景
"存量仓库 + 一批待议功能议题"与 change 提案模型一一对应；②议题多为中小特性，
BMAD 全流程过重；③可迁移诉求上 OpenSpec 结构即方法。

最小落地（若采纳）：`openspec init` → 两个 skill 各建 specs 基线 → T1/T3/T4/T5/T6
各建一个 change 文件夹（proposal.md + tasks.md）→ `openspec validate --strict`
做门槛。落地前 roadmap.md 保持唯一跟踪源，避免双轨。

来源：[BMAD-METHOD](https://github.com/bmad-code-org/BMAD-METHOD) ·
[BMAD docs](https://docs.bmad-method.org) ·
[OpenSpec](https://github.com/Fission-AI/OpenSpec) · [openspec.dev](https://openspec.dev)

## 变更记录

- 2026-10-08 建立；T7 决策并实现；清理本地 `.mimosa/`（已 gitignore）；
  BMAD vs OpenSpec 调研完成并入（倾向 OpenSpec 为主，待拍板）。
