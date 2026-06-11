# TOOLS.md — life-agent

## 路径基点

所有路径均相对于 Auto-college 项目根目录。

## Skill 清单

| Skill | 路径 | 状态 | 说明 |
|:---|:---|:---|:---|
| （预留） | — | 规划中 | 食堂/宿舍/交通/社团/活动/校历 |

> 当前无专属 Skill，可使用搜索工具提供基本校园生活信息。

## 工作区路径

| 用途 | 路径 |
|:---|:---|
| 当前会话根目录 | `workspace/{session_id}/` |
| 校园生活产物根目录 | `workspace/{session_id}/life/` |
| 食堂信息 | `workspace/{session_id}/life/dining_info.md` |
| 住宿出行 | `workspace/{session_id}/life/living_info.md` |
| 社团活动 | `workspace/{session_id}/life/activity_info.md` |
| 校历日程 | `workspace/{session_id}/life/calendar_info.md` |

## 外部服务

| 服务 | 访问方式 | 用途 |
|:---|:---|:---|
| UESTC 官网 | `*.uestc.edu.cn` | 校历、通知、活动信息 |
| web_search | 工具 | 校园生活信息搜索 |
| web_fetch | 工具 | 网页内容抓取 |

## 扩展接口

后续新增校园生活 Skill 时，在此注册 Skill 路径和场景映射。
