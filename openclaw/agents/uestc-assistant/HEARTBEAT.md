# HEARTBEAT — 成电小助手健康检查协议

## 1. 检查频率

- 新 Session 启动时执行一次。
- 每次派单前执行轻量检查：注册表、目标 Agent、通讯模板。
- 每次正式产物交付前执行产物路径检查。

## 2. 健康状态

| 状态 | 含义 | 用户可感知影响 |
|:---|:---|:---|
| `healthy` | 核心配置、Skills、SubAgents、workspace 均可用 | 全能力可用 |
| `degraded` | 部分 Skill / SubAgent / 依赖不可用 | 可降级完成部分任务 |
| `unavailable` | workspace 不可写或核心配置不可读 | 只能答疑，不能生成正式产物 |

## 3. 检查项

| 检查项 | 通过条件 | 失败状态 | 失败处理 |
|:---|:---|:---|:---|
| Agent 注册表 | `openclaw/openclaw-agents.yaml` 可读，主 Agent 存在 | unavailable | 停止派单，报告配置缺失 |
| 主 Agent 文件 | `AGENTS.md`、`TOOLS.md` 可读 | unavailable | 停止执行正式任务 |
| SubAgent 配置 | 3 个子 Agent 的 `AGENTS.md` + `TOOLS.md` 可读 | degraded | 禁用缺失 Agent |
| 通讯模板 | 3 个 shared YAML 模板可读 | degraded | 禁用派单，仅轻量直查 |
| Skills 可读 | 6 个 `SKILL.md` 可读 | degraded | 禁用缺失 Skill |
| Python3 | `python3 --version` 可用 | degraded | 禁用相关脚本，给安装建议 |
| Node.js | `node --version` 可用 | degraded | 禁用 PPT / Node 相关流程 |
| workspace 可写 | `workspace/` 可创建并写入 | unavailable | 不生成产物 |
| 状态区可写 | `workspace/_state/` 可创建并写入 | degraded | 不沉淀长期记忆 |

## 4. 心跳输出格式

```yaml
status: healthy | degraded | unavailable
summary: "一句话说明当前可用能力"
checks:
  registry: pass | fail
  main_agent_files: pass | fail
  subagents:
    academic-agent: pass | fail | disabled
    campus-info-agent: pass | fail | disabled
    life-agent: pass | fail | disabled
  templates: pass | fail
  skills:
    search-info: pass | fail
    terminal-screenshot: pass | fail
    lab-report: pass | fail
    coursework-helper: pass | fail
    paper-writer: pass | fail
    study-index: pass | fail
  runtimes:
    python3: pass | fail | skipped
    node: pass | fail | skipped
  workspace: pass | fail
  state_store: pass | fail | skipped
next_actions:
  - "可执行的修复建议"
artifacts:
  - "相关路径或日志路径"
```

## 5. 派单前快速检查

派单前必须确认：

```yaml
target_agent_registered: true
target_agent_allowed: true
dispatch_template_readable: true
session_id_ready: true
workspace_ready: true
```

任一项失败时，不派单，改为说明阻塞原因与安全下一步。
