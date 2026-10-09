# auto-research

问题驱动的研究实验工作流 skill：可检验问题 → 可证伪实验协议 → 证据台账
（claims/references ledger）登记 → 离线一致性审计 → 跨会话交接。无实验数据时
产出真实方案与待验证稿，不编造数字、引用或结果。

A problem-driven research-experiment skill: falsifiable protocols, an evidence
ledger (claims/references), an offline consistency audit script, and clean
cross-session handoff. Never invents results.

## 组成 / Components

| 件 / Part | 作用 / Role |
|-----------|-------------|
| `scripts/research_audit.py` | `init` 建最小记录 / `audit` 一致性核对；退出码 0/1/2；纯标准库 |
| `assets/` | PROJECT_CONTEXT / ROADMAP / HANDOFF 三模板 + ledger-schema.json |
| `references/` | running（S0-S8 阶段与运行规则）、experiments（协议/泄漏/统计）、ledger-schema（台账用法） |

## 用法 / Usage

```text
python skills/auto-research/scripts/research_audit.py init --root <项目目录> --topic <主题>
python skills/auto-research/scripts/research_audit.py audit --root <项目目录>
```

audit 核对：重复 ID、引用状态与核查笔记、证据路径越界、TeX cite key、
登记数字（mean/std/sum/count + scale + tolerance）、提交候选门（五项检查
证据齐全）。结构核对 ≠ 科学正确，真实核验不可省。

自治边界：不创建定时任务/后台监控/自行唤醒；授权与凭据不跨会话继承。
详细规则见 `skills/auto-research/SKILL.md`。
