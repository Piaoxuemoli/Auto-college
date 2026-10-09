# Spec Delta: research-skills-distill

本提案新增三个 capability，归档时分别建 `openspec/specs/auto-research/spec.md`、
`openspec/specs/paper-writing/spec.md`、`openspec/specs/group-meeting-prep/spec.md`。
三个 skill 互相独立：SKILL.md 与 references 不含跨 skill 路径引用，任一可单独
安装使用。

## Capability: auto-research

## ADDED Requirements

### Requirement: 项目初始化与拒绝覆盖

`scripts/research_audit.py init --root <项目目录> --topic <主题>` 创建最小记录：
RUN_STATE.json、PROJECT_CONTEXT.md、ROADMAP.md、ledger/claims.jsonl、
ledger/references.jsonl 及 paper/experiments/results/figures/reviews 目录。

#### Scenario: 新项目

- **WHEN** 目标目录无任何状态文件
- **THEN** 初始化成功，RUN_STATE phase=S0、deliverable_level=plan、
  autostart=false，退出码 0

#### Scenario: 已有状态

- **WHEN** 任一状态文件已存在
- **THEN** 拒绝覆盖并报错，退出码 2

### Requirement: 证据登记一致性核对

`audit` 子命令核对：重复 ID、引用状态（verified/partial/unresolved/excluded）
与验证笔记存在性、证据路径（项目相对、不越界）、常见 TeX cite key 与 literal
input/include、claims 登记数值（dotted key + where 筛选 + identity/mean/std/
sum/count + scale + tolerance）。输出 JSON 到 stdout。

#### Scenario: 登记一致

- **WHEN** 所有检查通过
- **THEN** `structural_consistency_passed=true`，退出码 0

#### Scenario: 发现不一致

- **WHEN** 存在 issue（如未核实引用、数字不匹配、证据文件缺失）
- **THEN** issues 逐项列出，退出码 1

#### Scenario: 输入错误

- **WHEN** ledger 缺失或 JSON 损坏
- **THEN** 报错，退出码 2

### Requirement: 提交候选门

deliverable_level=submission_candidate 要求：稿件存在、claims 非空且有
primary 主张且均为 supported、五项检查（scientific/citation/numeric/
compilation/visual）各自有证据笔记或有理由的 not_applicable。空项目
`submission_gate_recorded` 恒为 false。

#### Scenario: 空计划

- **WHEN** 刚初始化的项目运行 audit
- **THEN** 一致性可通过，但 submission_gate_recorded=false

#### Scenario: 检查缺项

- **WHEN** submission_candidate 有 pending/failed 且无 not_applicable 理由
- **THEN** 记 issue，退出码 1

### Requirement: 实验协议先于主测试

主要测试前冻结：实验单位、排除规则、数据划分、预处理拟合范围、基线信息
权限、预算、选参规则、统计估计量、失败处理。train/validation/test 独立，
按来源分组防泄漏；最终测试集不用于挑方法/种子/checkpoint。

#### Scenario: 结果与假设冲突

- **WHEN** 主实验结果反对原假设
- **THEN** 依次排查实现/测量、对照公平、假设本身；允许形成负结果或边界
  结论；不以加模块、辩护或收窄命题维护预设结论

### Requirement: 自治边界

skill 不创建定时任务/后台监控/自行唤醒；授权不跨会话继承；凭据不打包。
audit 发现 `autostart≠false` 记 issue。

#### Scenario: 状态文件被置 autostart=true

- **WHEN** 运行 audit
- **THEN** 记 issue："autostart must be false"

## Capability: paper-writing

## ADDED Requirements

### Requirement: 引用逐条核对

每条引用核对标题、作者顺序、年份、venue、卷期页码/文章号、DOI、预印本
版本与撤稿情况；状态机 verified/partial/unresolved/excluded；verified 须附
实际核查笔记。某篇存在不等于支持当前句子，需记录支撑的段落/图号/页码。
核对机制为纯流程规则（BibTeX + 核查笔记），不依赖外部脚本或其他 skill。

#### Scenario: 引用无法核实

- **WHEN** 关键字段无法对回原出版来源
- **THEN** 状态不标 verified；替换引用时重查整句是否仍被支持，必要时重写主张

### Requirement: 论文与代码精读

逐段提取原文主张、通俗解释和证据位置；代码对照追到预处理、张量形状、每层
操作、损失、优化、checkpoint 选择与指标；复现核对 commit、配置、环境、数据
版本、split、seed、运行命令与原始日志。

#### Scenario: 源码发现问题

- **WHEN** 公开实现存在缺陷
- **THEN** 结论限定为"当前公开实现存在问题"；无确切版本证据不断言论文
  全部结果有误

### Requirement: 论证成文与去 AI 味

先有研究论证再成文；一段只做一件事（主张→机制→证据→必要边界）；
去 AI 味四项检查（删除/异议/对比/位置测试）；引用、数据、论证、措辞四种
去重；措辞强度跟证据走（shows/supports/is consistent with/remains untested）。

#### Scenario: 无数据要求直出论文

- **WHEN** 用户要求成文但无实验数据
- **THEN** 交付待验证稿并明确标注未验证主张，不编造数字、引用或结果

### Requirement: 只读独立审稿

审稿基于冻结包（稿件、图表、BibTeX、协议、代码 commit、完整结果、重跑
入口）；评审只读，不改文件、不续跑研究；意见按 major/moderate/minor 定位到
文件/页/节/公式/图/表/日志。同一对话内的角色审阅标为自审。

#### Scenario: 审稿执行

- **WHEN** 发起独立审稿
- **THEN** 提供填入真实路径与目标标准的只读审稿提示词；输出按严重度排序
  的问题及证据位置；不引导"所有问题已解决"

### Requirement: 交付四级

研究方案 / 阶段稿 / 完整稿 / 提交候选四级，各有可宣称状态；不存在承诺录用
的层级；占位实验不得在标题、摘要、正文当作结论。

#### Scenario: 交付

- **WHEN** 任一级别交付
- **THEN** 附真实状态标注、成品路径、实际成功运行的重跑命令与未完成项

## Capability: group-meeting-prep

## ADDED Requirements

### Requirement: 图职责先行与路由

每张图先回答一个明确科学问题；按路由表选默认路线（实验曲线走原始数据+
标准绘图库；有高质量参照走原生复刻；无参照先查实际论文参照；仍缺构图才
考虑合规生图）。先冻结数据/科学内容，再决定图形。

#### Scenario: 实验曲线需求

- **WHEN** 数据已冻结
- **THEN** 由分析脚本从原始记录出图，不手抄数字；数值、聚合、单位、分母、
  轴与日志一致

### Requirement: 生图门禁

仅在可信配置确认实际路由为项目指定模型时才调用生图；提示词字样、工具名、
输出质量都不证明路由。路由未知或未配置则不生成，继续参照复刻或数据绘图。
生成图只作构图/插画参考，不制造实验数据、曲线、统计显著性或论文证据。
模型与接入走用户级配置文件约定（`~/.auto-college/image-gen.json`），无配置
即不生成。

#### Scenario: 路由未核实

- **WHEN** 无法确认实际生图模型路由
- **THEN** 不尝试生成，走参照/复刻/数据绘图替代路线

### Requirement: 可编辑图示验收

原生对象复刻/复用，不以扁平位图冒充可编辑；按完整包围盒缩放节点、字体、
线宽、箭头；新增/修改组件 `noGrp=0` 或省略；交付前检查裁切、遮挡、阅读
路径与指定文件行为。

#### Scenario: 原 PPT 新增页面

- **WHEN** 用户要求在指定文件新增 slide
- **THEN** 更新指定文件、保留旧版本；新增组件无 `noGrp="1"`/`true`

### Requirement: 组会汇报规范

以最新反馈稿为基准，保持标题、配色、字体、密度与图文比例；公式用演示
软件原生公式对象，不以纯文本或整图截图替代；备注推荐四段结构（讲稿 →
公式变量解释 → 深入阐述 → 一篇真实近邻论文）；正式交付递增主版本，
同轮内部试修不递增。

#### Scenario: 用户反馈后修订

- **WHEN** 用户在 V1.0 上给出 V1.1 反馈
- **THEN** 以反馈稿为基准修订，交付 V2.0，保留旧文件
