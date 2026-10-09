# Spec Delta: agent-neutral-install

## ADDED Requirements

### Requirement: agent 中立安装

`setup.js` 按环境自动选择安装目录：`.claude` → Claude Code，`.cursor` →
Cursor，命令行/未知环境 → `.agent/skills`（不存在则新建）。

#### Scenario: 未知环境安装

- **WHEN** 在无 `.claude` / `.cursor` 的环境运行 setup.js
- **THEN** skills 安装到 `.agent/skills/`，目录按需创建
