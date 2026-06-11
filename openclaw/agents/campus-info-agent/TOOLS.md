# TOOLS.md — campus-info-agent

## 路径基点

所有路径均相对于 Auto-college 项目根目录。

## Skill 清单

| Skill | 路径 | 说明 |
|:---|:---|:---|
| search-info（深度模式） | `skills/search-info/SKILL.md` | 高校信息深度检索 |

## 关键脚本路径

| 脚本 | 用途 |
|:---|:---|
| `skills/search-info/scripts/search_teacher.py` | 教师信息抓取器（零依赖 Python 网页抓取） |
| `skills/search-info/scripts/init_output_dir.py` | 输出目录初始化 |

## 工作区路径

| 用途 | 路径 |
|:---|:---|
| 当前会话根目录 | `workspace/{session_id}/` |
| 校园信息产物根目录 | `workspace/{session_id}/campus-info/` |
| 教师信息卡片 | `workspace/{session_id}/campus-info/{姓名}_teacher_card.md` |
| 学院全景 | `workspace/{session_id}/campus-info/{学院名}_college_panorama.md` |
| 实验室信息 | `workspace/{session_id}/campus-info/{实验室名}_lab_info.md` |
| 招生信息 | `workspace/{session_id}/campus-info/admission_info.md` |

## 外部服务

| 服务 | 访问方式 | 用途 |
|:---|:---|:---|
| UESTC 官网 | `*.uestc.edu.cn` | 首选官方信息来源 |
| Google Scholar | `scholar.google.com` | 教师学术信息补充 |
| 研招网 | `yz.chsi.com.cn` | 招生政策信息 |
| web_search | 工具 | 通用搜索 |
| web_fetch | 工具 | 网页内容抓取 |
