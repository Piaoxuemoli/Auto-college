---
name: group-meeting-prep
description: >
  Prepare research figures and group-meeting / progress-report slide decks with a
  responsibility-first figure workflow: statistical figures from real data, editable
  mechanism diagrams, and meeting PPT conventions. Use when the user needs 组会,
  汇报, PPT 制作, 论文配图, 科研绘图, 统计图, 机制图, or 可编辑图 deliverables.
---

# Group Meeting Prep — 科研配图与组会/汇报 PPT

**定位**：职责先行的科研工作流——每张图先回答一个明确科学问题，再选图形与工具
路线；产出真实统计图、可编辑机制图与组会/汇报 PPT。禁止编造数据与证据。

## 图职责先行

每张图回答一个明确问题：方法如何工作、主要效果是什么、机制为何成立、条件在哪里、
系统对象如何连接。先冻结数据/科学内容，再决定图形；图号和 caption 与主张 ledger
对应，不能为美观改变科学关系。

路由表（验证口径详见 `references/figure-routing.md`）：

| 图类型 | 默认路线 |
| --- | --- |
| 实验曲线、统计、频谱、热图 | 原始数据 + 标准绘图库 |
| 论文原图引用 | 原文 PDF 与图注；记录来源 |
| 给了高质量参照的可编辑图 | 原生对象复刻或复用 |
| 无参照的科研架构/机制图 | 内容规格 → 查实际论文参照 → 适配；仍缺构图才考虑合规生图 |
| 原图增加节点/关系 | 沿用原样式，必要时整体重排 |
| 3D 几何、坐标、波束 | 代码/仿真生成演示 |
| 网页交互、SVG/Canvas 创意图 | 前端或代码直接实现 |

## 生图门禁

仅在可信配置确认实际路由为**项目指定模型**时才调用生图。提示词写型号、官网有
该模型、工具名字、输出质量都不证明实际路由；路由未知或未配置 → 不生成、不降级，
继续参照复刻或数据绘图。模型与接入走用户级配置 `~/.auto-college/image-gen.json`
（字段：`provider` / `base_url` / `model` / `api_key`），无配置即不生成。
生成图只提供构图/插画参考，不制造实验数据、曲线、统计显著性或论文证据。
提示规格与生成后核对见 `references/figure-routing.md`。

## 按任务读参考

| 任务 | 参考文件 |
| --- | --- |
| 配图路线选择、参照复刻、生图门禁与提示规格 | `references/figure-routing.md` |
| 真实统计图（多面板、轴/区间、caption、figure manifest） | `references/statistical-figures.md` |
| 可编辑图/PPT 验收（包围盒、noGrp、指定文件更新） | `references/editable-slides.md` |
| 组会汇报规范（基准稿、公式、备注、命名版本） | `references/meeting-conventions.md` |

## 验收清单

- **科学**：图回答的问题明确；数值、单位、区间、聚合与数据一致；无编造证据。
- **视觉**：真实尺寸下字体/线条可读；各面板尺度一致；密度与留白接近目标领域
  高水平图。
- **编辑能力**：节点、文字、连线为原生对象；新增/修改组件 `noGrp=0` 或省略；
  无扁平位图冒充逐项可编辑。
- **指定文件行为**：更新的是用户指定文件；旧版保留；命名/版本符合约定。

## 输出

全部产物放 `outputs/<topic>/`（gitignored），不得写入 skill 源码目录。
