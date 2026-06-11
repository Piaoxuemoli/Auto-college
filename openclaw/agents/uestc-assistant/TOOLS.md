# TOOLS.md — 成电小助手

## 1. 路径基点

所有路径均相对于 Auto-college 项目根目录 `${AUTO_COLLEGE_ROOT}`。

| 类型 | 路径 | 读写策略 |
|:---|:---|:---|
| Agent 配置层 | `openclaw/agents/` | 只读 |
| Skill 能力层 | `skills/` | 只读 |
| 运行时工作区 | `workspace/` | 可读写 |
| 全局运行时状态 | `workspace/_state/` | 可读写 |
| 当前会话目录 | `workspace/{session_id}/` | 可读写 |

## 2. 主 Agent 自身 Skill

| Skill | 路径 | 触发场景 | 输出位置 |
|:---|:---|:---|:---|
| `search-info` | `skills/search-info/SKILL.md` | 高校信息轻量查询：老师、学院、领导、实验室 | `workspace/{session_id}/campus-info/` |
| `terminal-screenshot` | `skills/terminal-screenshot/SKILL.md` | 终端/命令行截图生成 | `workspace/{session_id}/outputs/` |

执行纪律：

1. 命中 Skill 后先读取对应 `SKILL.md`。
2. 按 Skill 自身流程执行，不跳阶段。
3. 正式产物必须写入当前会话目录。
4. 回复用户时给出产物路径、风险和下一步。

## 3. 可调度 SubAgent

| Agent | workspace 路径 | 核心职责 | 默认输出 |
|:---|:---|:---|:---|
| `academic-agent` | `openclaw/agents/academic-agent/` | 实验报告、课程作业、论文、PPT、复习资料 | `workspace/{session_id}/academic/` |
| `campus-info-agent` | `openclaw/agents/campus-info-agent/` | 深度校园信息检索、导师筛选、学院全景 | `workspace/{session_id}/campus-info/` |
| `life-agent` | `openclaw/agents/life-agent/` | 食堂、宿舍、交通、社团、活动、校历 | `workspace/{session_id}/life/` |

调度纪律：

- 只能调度 `openclaw-agents.yaml` 中 `uestc-assistant.subagents.allowAgents` 声明的 Agent。
- 派单必须使用 `openclaw/agents/_shared/AgentDispatch.yaml` 字段契约。
- 结果必须按 `AgentResult.yaml` 校验。
- 修正必须按 `AgentSessionPatch.yaml`，同一 session 最多 2 轮。

## 4. 工作区结构

| 用途 | 路径 |
|:---|:---|
| 当前会话根 | `workspace/{session_id}/` |
| 通用输出 | `workspace/{session_id}/outputs/` |
| 学业产物 | `workspace/{session_id}/academic/` |
| 校园信息产物 | `workspace/{session_id}/campus-info/` |
| 校园生活产物 | `workspace/{session_id}/life/` |
| 会话状态 | `workspace/{session_id}/state/session.md` |
| 全局校园知识 | `workspace/_state/memory.md` |
| 用户长期偏好 | `workspace/_state/user-preferences.md` |
| Agent 通讯模板 | `openclaw/agents/_shared/` |
| Agent 注册表 | `openclaw/openclaw-agents.yaml` |

## 5. 子 Agent Skill 映射

### `academic-agent`

| Skill | 路径 | 能力 |
|:---|:---|:---|
| `lab-report` | `skills/lab-report/SKILL.md` | 实验报告自动化 |
| `coursework-helper` | `skills/coursework-helper/SKILL.md` | 通识课作业、PPT、讲稿、交付包 |
| `paper-writer` | `skills/paper-writer/SKILL.md` | 学术论文路由、写作辅助、导出 |
| `study-index` | `skills/study-index/SKILL.md` | 课程资料速查手册 |

### `campus-info-agent`

| Skill | 路径 | 能力 |
|:---|:---|:---|
| `search-info`（深度模式） | `skills/search-info/SKILL.md` | 多源校园信息检索、证据整理 |

### `life-agent`

| Skill | 路径 | 状态 |
|:---|:---|:---|
| 生活信息 Skill | — | 待扩展 |

## 6. 外部信息源

| 信息源 | 用途 | 输出要求 |
|:---|:---|:---|
| UESTC 官网与学院官网 | 校园事实验证 | 标注 URL 与查询时间 |
| 公开通知页面 | 校历、活动、政策 | 标注发布时间或抓取时间 |
| 用户上传材料 | 学业和个人任务依据 | 只在当前会话内使用 |
| 搜索引擎 / 网页抓取 | 补充公开信息 | 优先交叉验证，不确定则标注待确认 |
