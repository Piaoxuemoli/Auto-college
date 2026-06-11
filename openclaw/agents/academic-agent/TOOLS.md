# TOOLS.md — academic-agent

## 路径基点

所有路径均相对于 Auto-college 项目根目录。

## Skill 清单

| Skill | 路径 | 场景域 |
|:---|:---|:---|
| lab-report | `skills/lab-report/SKILL.md` | 实验报告 |
| coursework-helper | `skills/coursework-helper/SKILL.md` | 课程作业（PPT/小论文/读书报告/演讲稿） |
| paper-writer | `skills/paper-writer/SKILL.md` | 学术论文 |
| study-index | `skills/study-index/SKILL.md` | 复习资料/开卷考试速查 |

## 工作区路径

| 用途 | 路径 |
|:---|:---|
| 当前会话根目录 | `workspace/{session_id}/` |
| 学业产物根目录 | `workspace/{session_id}/academic/` |
| 实验报告产物 | `workspace/{session_id}/academic/lab-report/` |
| 课程作业产物 | `workspace/{session_id}/academic/coursework/` |
| 学术论文产物 | `workspace/{session_id}/academic/paper/` |
| 复习资料产物 | `workspace/{session_id}/academic/study-index/` |

## 关键脚本路径

| 脚本 | 所属 Skill | 用途 |
|:---|:---|:---|
| `skills/lab-report/scripts/check_official_skills.py` | lab-report | 检查依赖 |
| `skills/lab-report/scripts/init_output_dir.py` | lab-report | 初始化输出目录 |
| `skills/lab-report/scripts/course_templates.py` | lab-report | 课程模板管理 |
| `skills/coursework-helper/scripts/init_output_dir.py` | coursework-helper | 初始化输出目录 |
| `skills/paper-writer/scripts/init_output_dir.py` | paper-writer | 初始化输出目录 |
| `skills/paper-writer/scripts/check_paper.py` | paper-writer | 论文检查 |
| `skills/study-index/scripts/extract_content.py` | study-index | 内容提取 |
| `skills/study-index/scripts/compile_handbook.py` | study-index | 手册编译 |
| `skills/study-index/scripts/export_pdf.py` | study-index | PDF 导出 |

## 外部服务

| 服务 | 访问方式 | 用途 |
|:---|:---|:---|
| python-pptx | Python 包 | PPT 生成 |
| python-docx | Python 包 | Word 导出 |
| PyMuPDF | Python 包 | PDF 处理 |
| Playwright | 可选 | 终端截图/PPT 预览 |
