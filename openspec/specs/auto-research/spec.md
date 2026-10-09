# auto-research — 能力基线

> 只描述当前已实现且为真的系统。改动走 `openspec/changes/`，归档时才合并进本文。

## Purpose

问题驱动的研究实验工作流 skill：从可检验问题出发，用可证伪实验区分解释，
用证据台账（ledger）登记引用、主张与数字，支撑可复现、可交接的科研过程。
无实验数据时产出真实方案与待验证稿，不编造结果。skill 间互相独立，
不引用其他 skill。

## Requirements

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
