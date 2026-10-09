# Tasks: research-skills-distill

> 验收标准是可验证的判定，不是描述。全部在本地完成；验证通过前不 commit、
> 不改 setup.js / README。

- [x] 1. `auto-research` 落地：`skills/auto-research/`（SKILL.md +
  `scripts/research_audit.py` 原样复制 + `assets/templates/` ×3 +
  `references/` 下 running / experiments / ledger-schema 等篇），符合
  `openspec/project.md` 目录规范。
  验收：SKILL.md frontmatter 含 name/description 且 name 与目录名一致；
  SKILL.md 引用的脚本/模板相对路径在实际布局下全部存在。
- [x] 2. `paper-writing` 落地：`skills/paper-writing/`（SKILL.md +
  `references/` 下 literature / writing / review / delivery 四篇）。
  验收：同任务 1 的 frontmatter 与路径检查；自带论文图原则极简版；
  引用核对为纯流程规则（BibTeX + 核查笔记），不依赖台账脚本。
- [x] 3. `group-meeting-prep` 落地：`skills/group-meeting-prep/`（SKILL.md +
  `references/` 下 figure-routing / statistical-figures / editable-slides /
  meeting-conventions 等篇）。
  验收：同任务 1 的 frontmatter 与路径检查；生图门禁已参数化——无硬编码
  模型名，指向 `~/.auto-college/image-gen.json` 配置约定。
- [x] 4. **去耦检查**：grep 三个 skill 的 SKILL.md 与 references，无跨 skill
  相对路径引用；任一 skill 单独复制到空目录可独立阅读执行。
  验收：跨 skill 引用扫描为空；三个 skill 各做一次独立触发演练，入口行为
  与各自 SKILL.md 一致。
- [x] 5. `research_audit.py` 本地实测矩阵（Windows，注意 Python UTF-8 模式）：
  init 成功 / 已有状态拒绝覆盖 / 空计划 submission_gate=false / 不一致退出 1 /
  均值+scale 数值核对通过与失败两例 / 未核实 TeX cite key / 越界证据路径 /
  重复 unit_id / 坏输入退出 2。toy 项目放 `skills/auto-research/outputs/`
  （gitignored）。
  验收：各例退出码与 JSON 字段符合预期。
- [x] 6. 中性标识扫描：从源包提取品牌词与个人站点域名作为扫描模式
  （模式清单只存本地，不写入入库文件），grep 三个新目录无品牌词、
  个人域名、真实用户名 / 主机名 / 个人硬件描述 / 个人路径 / api_key 字面量。
  验收：扫描输出为空。
- [ ] 7. 安装与发现验证：复制到本机目标环境的 skill 目录（`.claude/skills` /
  `.cursor/skills` / `.agent/skills`，按实际环境），新会话可发现、可按
  description 触发。
  验收：三个 skill 在目标环境可见。
  （2026-10-10 部分完成：结构安装与 frontmatter 解析已通过，已装入
  `<repo>/.zcode/skills/` 与 `~/.auto-college/skill-validation/skills/`；
  新会话可见性与触发待确认，见 VALIDATION.md）
- [x] 8. 模拟任务干跑（不实际做科研、不实际生图）：
  auto-research 走 init → 登记一条 verified 引用 + 一条主张 → audit 通过 →
  写 HANDOFF；paper-writing 对一段已有材料产出最近邻矩阵条目、只读审稿
  提示词、去 AI 味段落改写一例；group-meeting-prep 对两个配图需求走路由表
  给出路线判定、产出一页四段备注骨架。
  验收：流程无断点；产物与各自 SKILL.md 承诺一致；发现的问题修订后复测。
- [x] 9. 验证记录：结果写入本目录 `VALIDATION.md`。
  验收：每项任务有实测证据；明确列出未覆盖项。
