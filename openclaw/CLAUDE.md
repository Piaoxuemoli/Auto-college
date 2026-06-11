# CLAUDE.md — Auto-college 项目指引

This file provides guidance to Claude Code / Cursor when working with code in this repository.

## Project Overview

**Auto-college** 是一套面向电子科技大学（UESTC）学生的 AI 助手系统，覆盖学业辅助、校园信息查询、校园生活服务等场景。项目采用 OpenClaw 多 Agent 架构（Supervisor 模式）：主 Agent 统一入口，子 Agent 按领域分工。

**核心设计原则**：Agent 配置层独立（`openclaw/`），Skills 能力层共享（`skills/`），运行时数据隔离（`workspace/`）。

## Architecture

### Three-Layer Separation

| Layer | Path | Git Status | Purpose |
|-------|------|-----------|---------|
| **Agent 配置** | `openclaw/agents/`, `openclaw/openclaw-agents.yaml` | Committed | Agent 角色定义、约束、路由、通讯模板，只读 |
| **Skills 能力** | `skills/` | Committed | 6 个完整 Skill 定义（`SKILL.md` + 子代理 + 脚本），只读 |
| **运行时数据** | `workspace/` | Gitignored | 会话产物、输出文件、用户偏好、运行时记忆 |

### Main Agent

`uestc-assistant` 是唯一主入口，负责：

1. 意图识别：判断闲聊、校园事实、学业任务、校园生活、工具请求等。
2. 轻量直查：直接执行 `search-info`、`terminal-screenshot`。
3. 专家调度：通过 `AgentDispatch.yaml` 派单给 SubAgent。
4. 结果验收：按 `AgentResult.yaml` 校验状态、产物、风险、下一步。
5. 修正闭环：按 `AgentSessionPatch.yaml` 最多修正 2 轮。
6. 结果融合：给用户交付结论、依据、风险、产物路径、下一步。

### Agent Files

每个 Agent 由一组 `.md` 文件定义，存放在 `openclaw/agents/{name}/` 下：

| File | Purpose | Required |
|------|---------|----------|
| `AGENTS.md` | 完整系统提示：身份、约束、Skill 注册、路由表、执行闭环 | 所有 Agent |
| `TOOLS.md` | 工具路径配置、Skill 清单、工作区路径 | 所有 Agent |
| `SOUL.md` | 人格特质、核心信念、气质 | 仅主 Agent |
| `IDENTITY.md` | 自我介绍、能力蓝图、使用方式 | 仅主 Agent |
| `BOOTSTRAP.md` | 启动初始化步骤与降级策略 | 仅主 Agent |
| `MEMORY.md` | 只读种子知识与运行时记忆格式说明 | 仅主 Agent |
| `USER.md` | 只读用户偏好格式说明 | 仅主 Agent |
| `HEARTBEAT.md` | Agent 健康检查协议 | 仅主 Agent |

### Available Agents

- **`uestc-assistant`（成电小助手）**：主入口 Agent。直接执行轻量 Skill，复杂任务委派子 Agent。
- **`academic-agent`（学业助手）**：实验报告、课程作业、学术论文、复习资料。编排 `lab-report` / `coursework-helper` / `paper-writer` / `study-index`。
- **`campus-info-agent`（校园信息助手）**：深度校园信息检索、教师深度检索、学院全景、实验室调研、招生信息。
- **`life-agent`（校园生活助手）**：食堂、宿舍、交通、社团、活动、校历。当前为框架预留，Skills 待扩展。

### Skills

6 个 Skill 定义在 `skills/` 目录下，每个 Skill 有 `SKILL.md` 定义完整执行流程：

- **`lab-report`**：实验报告自动化。
- **`coursework-helper`**：通识课作业、PPT、讲稿、交付包。
- **`paper-writer`**：学术论文路由、写作辅助、导出。
- **`search-info`**：高校信息查询。
- **`study-index`**：课程资料速查手册。
- **`terminal-screenshot`**：终端截图生成。

### Agent 通讯模板

`openclaw/agents/_shared/` 下维护 Agent 间通讯协议：

| 模板 | 用途 |
|------|------|
| `AgentDispatch.yaml` | 主 Agent → 子 Agent 派单 |
| `AgentResult.yaml` | 子 Agent → 主 Agent 返回结果 |
| `AgentSessionPatch.yaml` | 主 Agent → 子 Agent 修正/补充指令 |

## Common Commands

```bash
# 初始化 workspace
mkdir -p workspace/_state

# 检查 Python3 环境
python3 --version

# 检查 Node.js 环境
node --version

# 安装常用 Python 依赖（按需）
pip3 install python-pptx python-docx PyMuPDF Pillow
```

## Critical Constraints

### 框架保护

1. **NEVER** 在运行时修改 `openclaw/agents/` 下的任何文件。
2. **NEVER** 在运行时修改 `skills/` 下的任何 `SKILL.md` 文件。
3. 所有运行时工作只在 `workspace/` 下进行。
4. `workspace/` 目录不提交 Git。
5. `MEMORY.md` / `USER.md` 是只读模板；运行时记忆写入 `workspace/_state/`。

### 学术诚信约束

1. **NEVER** 代写整篇论文或学术不端内容；可辅助润色、结构化、格式化、文献整理。
2. **NEVER** 编造实验数据、实验结果。
3. 所有 AI 辅助生成的学业产物必须提醒用户自行核验并按课程要求标注。
4. **NEVER** 替用户做选课、退课、提交作业等实际操作决策。

### 校园信息约束

1. **NEVER** 编造老师信息、课程内容、成绩规则、招生政策等校园事实。
2. 校园信息优先标注来源（URL + 查询时间）。
3. 找不到来源时标注「未记录 / 未找到 / 待确认」。
4. **NEVER** 泄露私人手机号、身份证号、私人邮箱、学号等个人隐私。

### Git Rules

- `workspace/` 目录不提交 Git。
- 运行时状态文件不提交 Git。
- Agent 配置更新应作为显式开发变更提交，不应由运行时 Agent 自动修改。
