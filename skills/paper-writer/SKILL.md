---
name: paper-writer
description: >
  学术论文路由器：收集需求、起 router-agent 调度 233 个专业 skills、
  三代理流水线（调度→写作→导出）。主 agent 不加载任何 skill 内容。
  Use when the user mentions 小论文, 课程论文, IEEE, 论文写作, 学术论文,
  文献综述, literature review, paper writing, scientific paper, 研究报告.
---

# Paper Writer Router

三代理流水线：主 agent 收集需求 → router-agent 匹配 skills → writer-agent 写论文 → export-agent 检查导出。

## 工作流程

### Step 1: 收集需求

从用户输入中提取以下参数（缺失的用默认值）：

| 参数 | 默认值 | 说明 |
|------|--------|------|
| topic | （必填） | 论文主题 |
| paper_name | （自动生成） | 输出目录名，英文短横线格式 |
| paper_type | 课程论文 | 课程论文 / 小论文 / 研究报告 / 文献综述 |
| lang | English | 论文写作语言：English / 中文 / 双语 |
| author | 不写 | 署名信息（姓名、学号、院系），空则不写 |
| target_words | 1500 | 正文字数目标（不含参考文献） |
| format | IEEE 单栏 | 排版格式：IEEE 单栏 / APA / MLA / 自定义 |
| citation_style | IEEE | 引用风格：IEEE 数字 [1] / APA / MLA / Chicago |
| min_refs | 不限 | 最少参考文献数 |
| deadline | 不限 | 截止时间（可选） |
| plagiarism_check | 常规 | 查重要求：常规 / AIGC / 两者 |
| extra | （无） | 其他特殊要求 |

如果用户输入中缺少关键参数（topic），先问清楚再继续。

### Step 2: 初始化目录

```bash
python paper-writer/scripts/init_output_dir.py "<paper_name>" \
    --target-words <target_words> \
    --lang <lang> \
    --author "<author>"
```

### Step 3: 起 router-agent

使用 Agent 工具创建 router-agent，传入需求参数和输出目录。

router-agent 会：
1. 读 skill-catalog.md 匹配领域 skills
2. 选取工具 skills
3. 组装 skill 路径列表
4. 起 writer-agent（带 skill 列表）

writer-agent 会：
1. 按列表加载 skills
2. 文献检索 → 大纲 → 撰写论文
3. 起 export-agent（检查 + Mermaid 渲染 + DOCX 导出）

```
起 router-agent，传入以下信息：

你是论文写作调度器。请按以下要求调度论文写作任务。

## 需求参数
- 主题: <topic>
- 论文类型: <paper_type>
- 语种: <lang>
- 署名: <author>
- 目标字数: <target_words>
- 格式: <format>
- 引用风格: <citation_style>
- 最少文献数: <min_refs>
- 查重要求: <plagiarism_check>
- 其他: <extra>

## 输出目录
paper-writer/outputs/<paper_name>/

请读取 paper-writer/agents/router-agent.md 了解你的工作流程。
```

### Step 4: 报告结果

全部子代理完成后，向用户报告：
- 输出文件位置
- 字数 / 文献数等统计数据
- 检查结果（是否有 warning）
- 如果有 deadline，提醒用户

## 三代理架构

```
主 agent (SKILL.md)
  │  收集需求 + 初始化目录
  │
  └─→ router-agent（调度器）
        │  读 catalog → 匹配领域 → 选工具 → 组装 skill 列表
        │
        └─→ writer-agent（写手）
              │  加载 skills → 文献检索 → 大纲 → 撰写 → 引用
              │
              └─→ export-agent（导出员）
                    check_paper.py → 修复 → render_mermaid.py → docx skill 导出 DOCX
```

## 重要原则

- **主 agent 不读 skill-catalog.md**
- **主 agent 不读任何 skills/<name>/SKILL.md**
- **主 agent 只负责收集需求 + 起 router-agent + 报告结果**
- **router-agent 只做匹配调度，不读 skill 内容**
- **writer-agent 按需加载 skills，只写论文**
- **export-agent 独立负责检查和导出**
