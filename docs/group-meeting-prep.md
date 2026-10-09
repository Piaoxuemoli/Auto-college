# group-meeting-prep

职责先行的科研配图与组会/汇报 PPT skill：每张图先回答一个明确科学问题，
再按路由表选工具路线；产出真实统计图、可编辑机制图与组会汇报 PPT。

A responsibility-first figure and slide-deck skill: every figure answers one
explicit question before a tool route is chosen; real statistical figures,
editable mechanism diagrams, and group-meeting PPT conventions.

## 路由表摘要 / Routing digest

| 图类型 / Figure type | 默认路线 / Default route |
|----------------------|--------------------------|
| 实验曲线、统计、频谱、热图 | 原始数据 + 标准绘图库 |
| 论文原图引用 | 原文 PDF 与图注；记录来源 |
| 有高质量参照的可编辑图 | 原生对象复刻或复用 |
| 无参照的架构/机制图 | 内容规格 → 查论文参照 → 适配；仍缺构图才考虑合规生图 |
| 3D 几何、坐标、波束 | 代码/仿真生成演示 |

## 生图门禁 / Image-gen gate

仅在可信配置确认实际路由为项目指定模型时才调用生图；提示词字样、工具名、
输出质量都不证明路由。配置走 `~/.auto-college/image-gen.json`
（provider/base_url/model/api_key），无配置即不生成、不降级。
生成图只作构图参考，不制造实验数据或论文证据。

## 组会规范 / Meeting conventions

最新反馈稿为基准；公式用原生公式对象（Office Math）；备注推荐四段结构
（讲稿 → 公式变量解释 → 深入阐述 → 一篇真实近邻论文）；首版 V1.0、反馈后
递增主版本、同轮试修不递增；新增组件 `noGrp=0` 或省略。

验收四维：科学、视觉、编辑能力、指定文件行为分别查。
详细规则见 `skills/group-meeting-prep/SKILL.md`。
