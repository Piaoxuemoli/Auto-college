# AGENTS.md

任何进入本仓库工作的 agent 从这里开始。

- 项目一句话：agent 中立的 skill 集合——terminal-screenshot（终端输出 →
  逼真 PNG 证据截图）+ lab-report（实验报告流程），详见 README.md。
- 先读 `openspec/project.md`：skill 目录规范、文档风格、中性标识、提交信息、
  安全钩子共存等仓库约定。
- 议题跟踪：进行中的变更提案在 `openspec/changes/<id>/`（proposal + tasks +
  spec delta）；`docs/roadmap.md` 是议题索引与决策记录（T1-T7 与 Epic）。
- 能力基线：`openspec/specs/<capability>/spec.md` 只描述当前为真的系统；
  改动先走 changes/ 提案，实现完成、验收通过后归档合并回 specs/。
- 输出产物目录（`skills/*/outputs/`）已 gitignored：生成物只写这里，
  不改 skill 源码目录。
- 不要提交个人标识：示例用户名一律 `dev`，本地配置目录一律 `~/.auto-college`；
  任何文件不得含真实用户名/主机名/个人标识/api_key 等凭据。
- 未经用户明确要求，不执行 git commit/push。
