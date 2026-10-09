# Proposal: research-skills-distill

- 议题：T8 上游科研工作流包提炼为本地 skill（见 `docs/roadmap.md`）
- 状态：proposed（v2：按用户反馈改为"两套主线 + 组会准备层"，skill 间去耦）

## 为什么

源文件包（科研直出论文工作流 v1.0，2026-10-08；现置本地 `references/` 下，
gitignored 不入库）是一套自包含的工作流：1008 行单文件手册
（`AI_RESEARCH_HANDOFF.md`）+ Codex skill 目录（SKILL.md + 9 个阶段
references + 3 个状态模板 + `research_audit.py` 离线核对脚本）。其方法内核——
问题驱动、可证伪实验、证据台账、只读独立审稿、跨会话交接——与本仓库现有
terminal-screenshot / lab-report 互补，值得沉淀为本地 skill。

直接照搬不行：

1. **单体过大**：一次触发加载全流程，而多数任务只命中一个阶段；
2. **含个人标识与硬编码个人约束**：源包品牌前缀、个人站点域名、个人会话
   统计口径、生图模型硬门禁、组会命名约定——违反仓库中性标识约定
   （`openspec/project.md`、AGENTS.md）；
3. **用户明确要求**：新 skill 先本地做完验证，再谈入库与发布。

## 做什么

按用户指定的路线拆为**两套主线 + 组会准备层**，共 3 个 skill。
核心原则：**去耦**——SKILL.md 互不引用，各自独立触发、独立可用；
输入材料来自哪里都行，不假设其他 skill 在场。

| skill | 职责 | 来源章节 |
| --- | --- | --- |
| `auto-research` | 研究实验专精：决策准绳、S0-S8 运行规则、实验协议/泄漏控制/统计核对、状态台账（RUN_STATE + ledger + audit 脚本 + 模板）、自治边界、交接续接 | 02-running、04-experiments、09-helper、assets/、scripts/ |
| `paper-writing` | 调研阅读写作专精：检索策略与来源入口、引用逐条核对、论文与代码精读、论证成文、去 AI 味与去重、只读审稿迭代、交付层级与打包 | 03-literature、06-writing、07-review、08-delivery（不含组会节） |
| `group-meeting-prep` | 组会准备层：配图职责路由、统计图标准、参照复刻与生图门禁、可编辑图示验收、组会汇报规范（最新反馈稿基准、原生公式、四段备注、版本命名） | 05-figures、08 组会节 |

去耦的具体落实：

- 台账机制归属 auto-research（状态服务研究运行）；paper-writing 的引用核对
  是纯流程规则（BibTeX + 核查笔记），不依赖台账脚本；
- paper-writing 自带两行论文图原则（图呈现科学关系、caption 对应主张、
  数据脚本出图），完整视觉标准归 group-meeting-prep，写作不依赖配图 skill；
- 生图门禁走用户级配置文件 `~/.auto-college/image-gen.json` 约定（无配置则
  不生成），是文件约定而非 skill 间依赖；
- 验收含专门的去耦检查（tasks 第 4 条）。

清洗（不进入 skill）：

- 源包品牌前缀与个人站点域名、个人会话统计口径（索引数 / 消息数 /
  来源会话计数列）、01-profile 个人史料；
- 个人硬件/SSH 别名/账户史；`agents/openai.yaml`（Codex 专属，本仓库 skill
  无此目录）；
- `AI_RESEARCH_HANDOFF.md` 单文件版（skill 化后冗余；源包原样保留、不入库）；
- 生图模型硬编码 → 参数化为"项目配置的指定模型 + 可信路由核实后才生成"；
- 组会命名/四段备注约定 → 通用骨架（最新反馈稿为基准、主版本递增、
  备注推荐结构）。

`scripts/research_audit.py` 原样复制不改造（上游 `VALIDATION.md` 已有实测
记录，本地复测确认即可）。

## 取舍

- **v1 方案（research-ledger / research-paper / research-figures 互相引用）
  被用户否决**：跨 skill 引用耦合深，违背使用习惯；
- **不单列 ledger skill**：状态机制与研究运行一体，单列会造成三个 skill
  互相引用；并入 auto-research 后台账是该 skill 的内部机制；
- **论文图原则在 paper-writing 保留极简版**，完整视觉标准归
  group-meeting-prep：避免写作依赖配图；
- **本地验证通过前**：不更新 setup.js 的 SKILLS 列表与 README，不 commit；
  新 skill 目录以未提交状态留在工作区。
