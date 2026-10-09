# Roadmap — 议题索引与决策记录

> **跟踪源已迁移至 openspec/**：能力基线在 `openspec/specs/`（描述当前为真的
> 系统），仓库约定在 `openspec/project.md`。本文件保留为议题索引与决策记录；
> 归档的变更提案见 git 历史（`openspec/changes/<id>/`）。
> 状态：`open` → `discussing` → `decided` → `done`（已实现并归档）。

## 已搁置

- **实机验证（M7 mac 金标准 / freeze·termframe 实测出图 / fonts 三平台渲染）**：
  暂不做。macOS 截图非自由许可；外部渲染工具实际使用时再装再验；
  字体跨平台补验待 mac/linux 主机。

## 议题清单（T1-T7 于 2026-10-09 归档；T8 于 2026-10-10 归档）

### T1 实验报告模板选择 — `done`
决策：模板目录化。`templates/` + `catalog.md` 索引；优先级课程模板 → 用户 →
学科默认（首个学科模板 computer-network）→ 内置 zh/en；偏好持久化
`~/.auto-college/lab-report/course_templates.json`（save/get 跨进程命中已验）。

### T2 截图 HTML 的字体 — `done`
决策：自托管 OFL woff2。Cascadia v2407.24 + JetBrains Mono v2.304 入库
`assets/fonts/`，@font-face 三级优先（本地 → 系统栈 → 等宽），中文走系统回退；
SF Mono 非 OFL 不再分发。遗留：Cascadia 变量字体 >100KB 可再子集化；
mac/linux 主机渲染补验。

### T3 实验报告图片嵌入 — `done`（规则级）
决策：图注 `图 N-M 说明`（zh）/ `Figure N-M: caption`（en）居中 10.5pt 不加粗；
PNG、宽 ≤16cm、相对路径引用、>2MB 压缩、缺图占位。见 `references/export-guide.md`。
遗留：压缩阈值固定 2MB 未可配置；docx/pdf 样本级验证未产出。

### T4 实验报告导出格式 — `done`（规则级）
决策：默认 md + docx 双交付；pdf 按需走 docx→pdf（优先）或官方 pdf skill
（备选）——理由：避免为长尾 pdf 需求引入 LaTeX 全链路依赖；草稿迭代 md-only；
docx 失败交付 md + 失败说明。遗留：样本级双交付与 pdf 样本未产出。

### T5 LaTeX / 数学公式支持 — `done`（公式层）
决策：先公式层后全文层。源 MD 保留 `$...$`/`$$...$$`，docx 导出 OMML
（官方 skill 优先 / pandoc 回退 / 双失败代码字体+交付注明）；zh/en 模板已含
公式示例。**全文 LaTeX 模板暂缓**，出现真实需求再单开 change。
遗留：含公式样本 docx/pdf 未产出、失败公式场景未演练。

### T6 图片生成 tool 可配置接入 — `done`（适配层）
决策：配置驱动 + 优雅降级。`~/.auto-college/image-gen.json`（schema 见
`configs/image-gen.example.json`）+ `scripts/image_gen.py`（纯标准库，
OpenAI-compatible）；退出码 0/1/2；`--emit-prompt` 无配置产出可复用 prompt
文件；api_key 全程脱敏。遗留：真实服务首次调通与端到端样本报告待用户配置后补验。

### T7 安装目录策略 — `done`
决策：安装器环境自动检测（`.claude`/`.cursor`），未知环境默认 `.agent/skills`
自动新建；README 引导 agent 自检环境后安装。

### T8 上游科研工作流包提炼为本地 skill — `done`
决策：按用户指定路线拆为两套主线 + 组会准备层，skill 间去耦、无交叉引用：
auto-research（研究实验 + 状态台账/audit 脚本）、paper-writing（调研阅读
写作审稿交付）、group-meeting-prep（配图路由与组会汇报）。个人标识清洗
（品牌词/个人域名/会话统计口径/01-profile 史料剥离；生图模型参数化为
`~/.auto-college/image-gen.json` 配置）。验证：audit 脚本 11 例实测矩阵通过、
脚本与模板逐字节一致、去耦与中性扫描为空、三 skill 干跑产物齐全
（VALIDATION.md 随 changes 归档，git 历史留档）。
遗留：新会话发现性与真实科研端到端使用待确认（tasks 第 7 条未勾）。

## 史诗（Epic）：个人工作流体系建设 — 第一循环完成

目标：可迁移的个人工作流体系（议题跟踪、规格驱动、验证闭环、多模态协作、
安全钩子共存），在日常工作中持续验证迭代。

**第一循环（2026-10-08 → 10-09）已完成并验证**：roadmap 建档 → BMAD vs
OpenSpec 调研（结论：OpenSpec 为主 + BMAD story 验收粒度）→ openspec/ 落地 →
多子代理分区并行实现 T1-T7 → 人工分区 review + 视觉子智能体验收 →
spec delta 合并、changes 归档（本文件即是该循环的收尾产物）。
验证结论：提案→实现→验收→归档全链路可用；可迁移件 = `openspec/project.md`
约定 + specs/changes 结构 + 本 roadmap 模板。

### BMAD vs OpenSpec 调研结论 — `decided`（2026-10-09 拍板：OpenSpec）

一句话定位：**BMAD** 是全生命周期敏捷 AI 开发框架（角色代理 + prd/story 工件，
重规划）；**OpenSpec** 是轻量"人与 AI 的契约层"（project.md + specs/ + changes/
提案驱动，纯 Markdown）。

| 维度 | BMAD (V6) | OpenSpec |
|---|---|---|
| 单人维护 | 偏重（为团队设计） | 明显更优 |
| 工具集成 | 按 IDE 生成文件 | AGENTS.md + Markdown，任何 agent 零成本 |
| 可迁移 | 方法在框架里，升级即变 | 结构即方法，复制文件夹即迁移 |

来源：[BMAD-METHOD](https://github.com/bmad-code-org/BMAD-METHOD) ·
[OpenSpec](https://github.com/Fission-AI/OpenSpec) · [openspec.dev](https://openspec.dev)

## 变更记录

- 2026-10-10 T8 完成并归档：上游科研工作流包提炼为 auto-research /
  paper-writing / group-meeting-prep 三个互相独立的 skill（skills/），
  specs 三基线建立、changes 目录移除；README、setup.js、AGENTS.md、
  docs/ 同步。
- 2026-10-09 T1-T7 实现完成并归档（spec delta 合并进 specs 基线，changes 目录
  移除，git 历史留档）；视觉子智能体验收三平台示例（发现并修复 Windows 长命令
  裁切：正文改 pre-wrap）；image_gen 补 `--emit-prompt` 与示例配置；公式示例入
  zh/en 模板；Epic 第一循环闭环。
- 2026-10-09 OpenSpec 落地（project.md、两 specs 基线、T1-T7 七 changes、
  AGENTS.md）；本文件转为索引。
- 2026-10-08 建立；T7 决策并实现；BMAD vs OpenSpec 调研并入。
