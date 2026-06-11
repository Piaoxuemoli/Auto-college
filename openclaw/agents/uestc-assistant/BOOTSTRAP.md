# BOOTSTRAP — 成电小助手启动初始化

每次新 Session 启动时，按序执行以下检查。启动检查只验证环境与目录，不修改 `openclaw/agents/` 或 `skills/`。

## 1. 读取核心配置

- [ ] 读取 `openclaw/openclaw-agents.yaml`，确认 `uestc-assistant` 为主入口。
- [ ] 读取 `openclaw/agents/uestc-assistant/AGENTS.md`。
- [ ] 按需读取 `SOUL.md`、`IDENTITY.md`、`TOOLS.md`。
- [ ] 确认可调度 SubAgent：`academic-agent`、`campus-info-agent`、`life-agent`。

## 2. 通讯模板检查

- [ ] `openclaw/agents/_shared/AgentDispatch.yaml` 存在且可读。
- [ ] `openclaw/agents/_shared/AgentResult.yaml` 存在且可读。
- [ ] `openclaw/agents/_shared/AgentSessionPatch.yaml` 存在且可读。

## 3. Skill 完整性检查

- [ ] `skills/search-info/SKILL.md` 存在且可读。
- [ ] `skills/terminal-screenshot/SKILL.md` 存在且可读。
- [ ] `skills/lab-report/SKILL.md` 存在且可读。
- [ ] `skills/coursework-helper/SKILL.md` 存在且可读。
- [ ] `skills/paper-writer/SKILL.md` 存在且可读。
- [ ] `skills/study-index/SKILL.md` 存在且可读。

## 4. 运行环境检查

- [ ] Python3 可用，建议版本 ≥ 3.8。
- [ ] pip 可用。
- [ ] Node.js 可用，建议版本 ≥ 16（用于 setup.js / PPT 引擎）。
- [ ] 当前 shell 对 `workspace/` 有写权限。

## 5. 工作区初始化

如不存在则创建：

```text
workspace/
workspace/_state/
workspace/{session_id}/
workspace/{session_id}/outputs/
workspace/{session_id}/academic/
workspace/{session_id}/campus-info/
workspace/{session_id}/life/
workspace/{session_id}/state/
```

运行时状态文件按需创建：

```text
workspace/_state/memory.md
workspace/_state/user-preferences.md
workspace/{session_id}/state/session.md
```

## 6. 启动降级策略

| 检查失败项 | 状态 | 处理方式 |
|:---|:---|:---|
| 非核心 Skill 缺失 | degraded | 禁用对应能力，其他能力继续 |
| SubAgent 配置缺失 | degraded | 不派单给该 Agent，说明原因 |
| 通讯模板缺失 | degraded | 禁用派单，保留轻量直查 |
| `workspace/` 不可写 | unavailable | 停止正式产物生成，只能答疑 |
| Python / Node 缺失 | degraded | 禁用依赖脚本的能力，给安装建议 |

## 7. 就绪输出格式

```yaml
status: healthy | degraded | unavailable
assistant: uestc-assistant
skills_available:
  - search-info
  - terminal-screenshot
  - lab-report
  - coursework-helper
  - paper-writer
  - study-index
subagents_available:
  - academic-agent
  - campus-info-agent
  - life-agent
workspace: workspace/{session_id}/
message: "成电小助手已就绪"
```
