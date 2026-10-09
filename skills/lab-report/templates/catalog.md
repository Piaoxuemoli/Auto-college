# 实验报告模板目录 / Report Template Catalog

成稿时按本目录选模板：命中即按需读取单个模板文件，不预加载全部。

## 选择顺序（任一环节缺失则安全落到下一级，最终内置默认兜底，成稿不中断）

1. **课程模板**：`scripts/course_templates.py get --course <课程名>` 命中
   （记忆存于 `~/.auto-college/lab-report/course_templates.json`）；
2. **用户模板**：用户本次指定的模板路径，或本目录中的课程自定义模板文件；
3. **学科默认**：本目录 scope 匹配当前学科的模板（暂无条目，预留扩展）；
4. **内置默认**：按报告语言取 `report-template-zh.md` / `report-template-en.md`。

## 模板索引

| 文件 | name | language | scope（适用场景） | sections（章节结构概要） | 来源 |
|------|------|----------|------------------|------------------------|------|
| `report-template-zh.md` | 默认中文实验报告模板 | zh | 无课程/学科模板命中时的中文默认 | 十段式：名称、项目名称、目的、内容、器材、步骤、数据结果分析、结论、心得、改进建议 | 内置默认 |
| `report-template-en.md` | Default English Lab Report Template | en | 无课程/学科模板命中时的英文默认 | 10 sections: name, project, objective, content, equipment, procedure, results & analysis, conclusion, reflections, suggestions | 内置默认 |
| `computer-network-template.md` | 计算机网络实验报告模板（演示学科模板） | zh | 计算机网络课程实验 | 十段式 + 网络拓扑/IP 规划表（五）+ 捕获数据分析字段（七） | 学科默认（演示） |

## 课程自定义模板

- 课程自定义模板同样存放到本目录，命名 `<course-slug>-template.md`
  （slug 规则同 `course_templates.py`：小写，非字母/数字/汉字转为 `-`），
  并在上方索引表追加一行（来源：课程自定义）；
- 或直接使用课程方提供的任意路径模板（`course_templates.py save
  --course <课程名> --template-path <路径>` 登记，引用其提供路径）；
- 课程模板优先级最高；若其缺章节，用内置默认模板对应章节补齐。
