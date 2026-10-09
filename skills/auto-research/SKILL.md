---
name: auto-research
description: >
  Run problem-driven research experiments with falsifiable protocols and an evidence ledger.
  Use when the user needs 科研项目启动/续接, 实验设计与协议, 证据台账,
  登记引用与主张, 核对论文数字, or 科研交接. Does not auto-start background tasks or submit externally.
---

# Auto Research — 研究实验工作流

**定位**：问题驱动的研究实验工作流——从可检验问题出发，用可证伪实验区分解释，
用证据台账（ledger）登记引用、主张与数字，支撑可复现、可交接的科研过程。
具体项目与现有证据优先；不用通用流程覆盖现成研究逻辑。禁止编造结果：没有数据时做方案或明确标注待验证。

## 启动与续接

仅在用户当前主动请求中执行。先读项目内 `PROJECT_CONTEXT.md`、`ROADMAP.md`、
`ledger/`（claims.jsonl / references.jsonl）与原始结果，核实当前阶段后继续下一项真正推进结论的工作；
**已有项目不重新初始化**。新项目运行（脚本路径以本 skill 目录为基准）：

```text
python scripts/research_audit.py init --root <项目目录> --topic <主题>
```

先简明说明中心问题、现有证据、当前阶段和本轮交付。能从文件推断的信息自行取得并记录。

## 决策准绳

1. 问题和机制先行：说明输入、输出、形状、条件与可证伪预测，方法、实验接回同一中心问题。
2. 查最近邻并核对原文后判断创新；高引经典与最新可靠研究互补，真实适配比头衔重要。
3. 小规模验证后扩大：实验单位、划分、预算公平、选择规则和结论释放严格，出现实际问题才增加防护。
4. 结果与假设冲突时重审假设，保留负结果；不以加模块、辩护或收窄命题维护预设结论。

## 阶段与通过条件（详见 references/running.md）

| 阶段 | 动作 | 下一阶段依据 |
| --- | --- | --- |
| S0 接手 | 读 context、roadmap、源文件日志 | 缺口、版本与下一问题明确 |
| S1 定题 | 可检验问题、最近邻、差异价值 | 主张可证伪，测量与关键对照可实现 |
| S2 精读 | 原文、补充、官方代码、数据协议 | 机制与复现缺口能解释 |
| S3 协议 | 指标、单位、划分、对照、预算、失败、选择规则 | 决定性实验区分主张和替代解释 |
| S4 试验 | toy、小试、实现检查、资源估算 | 代码工作，协议有识别力 |
| S5 验证 | 主实验、消融、边界、鲁棒性、不确定性 | 主张有原始证据，失败有记录 |
| S6 成文 | 证据大纲、结果、引言、图引 | 完整论证和每个数字的来源 |
| S7 审阅 | 科学、引用、数字、编译、视觉检查 | 主要问题关闭，结论范围准确 |
| S8 交付 | 成品、源码、复现、状态、交接 | 可打开、能运行、未完成项明确 |

## 按工作读参考

| 工作 | 参考 |
| --- | --- |
| 实验设计、公平与泄漏、统计核对、领域识别问题 | [references/experiments.md](references/experiments.md) |
| 运行规则、自主推进循环、收敛停止、状态衔接、协作算力 | [references/running.md](references/running.md) |
| 台账格式、audit 用法与退出码、提交候选门 | [references/ledger-schema.md](references/ledger-schema.md) |

## 自治边界

不创建 cron、heartbeat、定时器、后台监控，任务结束后不自行唤醒；新会话需用户新指令。
旧会话的账户、密钥、服务器与对外授权不跨会话继承。新增付费资源、公开数据、发邮件、
对外发布需用户明确授权；资源不足时记录缺口并推进独立可做部分。失败可形成否定结果、
边界结论或真实待验证稿；不以刷到 accept 为停止条件。

## 核对与交付

执行 `python scripts/research_audit.py audit --root <项目目录>` 核对登记、证据、cite key
与登记数字（用法与退出码见 references/ledger-schema.md）。**结构核对≠科学正确**：文献真实性、
实验公平、推导与统计仍需真实核验。每次结束更新 PROJECT_CONTEXT.md、ROADMAP.md 与引用库；
交接写清已完成、失败、待验证、成品路径和重跑命令。提交候选须通过科学、引用、数字、编译、
视觉检查，缺项准确标注当前级别。
