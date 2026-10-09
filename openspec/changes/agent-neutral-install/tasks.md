# Tasks: agent-neutral-install

> 已实现（2026-10-08），全部勾选。

- [x] 1. 环境检测逻辑：`setup.js` 检测 `.claude` / `.cursor`，
  命令行/未知环境默认 `.agent/skills`（缺则新建）。
  验收：三种环境路径各验证一次，安装目录正确。
- [x] 2. README 同步：安装小节不再假设单一 agent 生态。
  验收：README 安装说明与 setup.js 行为一致。
- [x] 3. 决策记录：roadmap T7 状态 `done`，含决策 + 理由。
  验收：`docs/roadmap.md` T7 条目完整。
