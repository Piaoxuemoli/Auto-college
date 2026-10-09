# Proposal: agent-neutral-install

- 议题：T7 安装目录策略（见 `docs/roadmap.md`）
- 状态：implemented（2026-10-08 实现完毕，roadmap T7 已标 done）

## 为什么

仓库是 agent 中立的 skill 集合，安装器却默认绑定 Claude 生态目录，
Cursor / 其他 agent 用户安装后无法生效。

## 做什么

`setup.js` 按环境自动检测安装目录：检测到 `.claude` → Claude Code；
`.cursor` → Cursor；命令行/未知环境默认 `.agent/skills`（不存在则新建），
不再假设 Claude。README 安装说明同步。

## 取舍

- 检测优先级"已知环境 > 中立默认"，不做询问交互：安装应零交互、可脚本化；
- 遗留：安装提示中"引导 agent 自检环境"的交互话术待补，作为日常维护小项
  跟踪，不再单开 change。
