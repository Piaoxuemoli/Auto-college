# Export Guide — 导出格式 / 数学公式 / 图片嵌入

成稿与导出阶段的实现规范：交付格式决策（T4）、数学公式 OMML 转换（T5）、
图片嵌入与图注（T3）。供 report-writer 与导出步骤遵循。

## 导出格式决策矩阵（T4）

默认交付 `final_report.md` + `final_report.docx` 双格式；pdf 仅按需。

| 交付格式 | 何时选择 | 实现路径 |
|---------|---------|---------|
| **md + docx**（默认） | 用户未指定格式时的常规交付 | md 为源；docx 用官方 docx skill 从 md 生成 |
| **+ pdf**（按需） | 用户明确要 pdf，或课程要求 PDF 提交 | 优先 docx→pdf 转换（版式保真）；无转换能力时用官方 pdf skill 从内容重排 |
| **md-only**（快速路径） | 草稿预览、报告仍需多轮修改、仅内部查看 | 直接交付 `final_report.md`，跳过 docx/pdf 管线 |

决策规则：

- 用户未指定 → md + docx；课程模板指定格式 → 模板优先。
- 决策写入 `report_context.json` 的 `delivery_formats`；实际交付与决策不一致时，
  在 `delivery_manifest.json` 的 `warnings` 中说明原因。

## 数学公式（T5，公式层）

源文件 `final_report.md` 规范：

- 行内公式用 `$...$`，块级公式用 `$$...$$`（独立成行），LaTeX 语法**原样保留**，
  不转义、不预渲染成图片或 HTML。
- 需要编号时用 `\tag{N}`，编号与报告章节对齐。

导出 DOCX 时转为 OMML（Word 原生公式对象）：

**路径 A — 官方 docx skill（优先）**
- 用 docx skill 的 OOXML 能力将 `$...$` / `$$...$$` 转为 `<m:oMath>` /
  `<m:oMathPara>` 插入 `document.xml`。
- 行内公式保持段内样式；块级公式独立成段、居中。

**路径 B — pandoc 回退**（无 docx skill，或路径 A 公式转换失败）
```bash
pandoc final_report.md -o final_report.docx
```
pandoc 自动将 LaTeX 数学转为 OMML，无需额外参数。

**失败回退**：两条路径都失败时不阻塞交付——公式以代码字体原样嵌入（保留
`$...$` 定界符），并在交付说明（`delivery_manifest.json` 的 `warnings`）中注明
"公式未转 OMML，以 LaTeX 源码呈现"。md 源文件始终保有可编辑的 LaTeX 公式，
事后可重试导出。

## 图片嵌入规范（T3）

格式与尺寸：

- 截图与插图统一 **PNG**；其他格式（JPG/WebP 等）嵌入前先转 PNG。
- 显示宽度上限 **16cm（6.3in）**；超宽图按比例缩放到限内，不拉伸变形。
- 单图体积 >2MB 时先用 PIL 压缩到阈值内再嵌入：
  ```python
  from PIL import Image
  img = Image.open("fig.png")
  img.save("fig.png", optimize=True)  # 必要时先 img.thumbnail((w, h)) 降采样
  ```

路径与引用：

- 图片存放于 `outputs/<experiment-name>/screenshots/`；报告 md 用相对路径引用
  （如 `screenshots/step1.png`），保证输出目录整体可迁移。
- 导出 docx 时按同一相对路径定位嵌入；docx 与 md 放在同一输出目录。

图注：

- 格式 `图 N-M 中文说明`：N 为实验步骤章节号（对应模板"六、实验步骤"的步骤 N），
  M 为该步骤内的图片序号，如 `图 3-2 并行向量加法核函数输出`。
- 图注单独成行、居中，位于图片正下方；导出 docx 时设为宋体 10.5pt（五号）、
  不加粗（md 源中即普通文本行，样式在导出时施加）。
- 正文引用写法：如图 3-2 所示。
- 英文报告图注用 `Figure N-M: caption`（Times New Roman 10.5pt 居中不加粗），
  正文引用 `as shown in Figure 3-2`。

插图来源：

- 运行证据截图统一由 **terminal-screenshot** skill 生成，存入 `screenshots/`。
- 原理示意图等非截图插图，若环境具备图片生成能力，遵循
  `references/image-gen.md` 的规范生成后同样按本节嵌入；不具备则改用文字或
  表达式说明，不编造图片。
