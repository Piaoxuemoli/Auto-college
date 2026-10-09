# Proposal: latex-math-support

- 议题：T5 LaTeX / 数学公式支持（见 `docs/roadmap.md`）
- 状态：draft（roadmap 倾向：先①公式层，后②全文层）

## 为什么

物理/算法类实验报告需要公式。当前 MD 里写 LaTeX 源，导出 docx 后公式是否
渲染取决于官方 skill 临场处理，无约定则交付质量不可控。

## 做什么

分两层，先①后②：

- ① 公式层（本 change 核心）：MD 内 `$...$`（行内）/ `$$...$$`（独立行）
  保留 LaTeX 源；docx 导出走 OMML 转换（官方 docx skill 能力）；
  pdf 路径与 T4 联动。
- ② 全文层（后置，另行 change）：引入官方 pdf skill 的 LaTeX 管线作可选模板
  （论文/实验报告 LaTeX 类），不并入默认流程。

## 取舍

- 公式是刚需、全文 LaTeX 是长尾：先①后②，②未立项前不在本仓库维护 LaTeX 模板；
- MD 保留 LaTeX 源而非预渲染图片：源可编辑、可 diff，导出端各自最优渲染；
- OMML 不可用/转换失败的公式：保留源码文本并在交付时说明，不静默丢公式。
