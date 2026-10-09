# Proposal: fonts-local

- 议题：T2 截图 HTML 的字体（见 `docs/roadmap.md`）
- 状态：proposed（roadmap 倾向方案 ①）

## 为什么

HTML 模板依赖渲染主机已装字体，缺字体时静默回退 → 字宽/观感漂移，跨平台
可复现性受损；chrome 校验协议也会因字体差异产生假阳性/假阴性。

## 做什么

自托管 woff2（roadmap 方案 ①）：

- 选 OFL 许可等宽字体（Cascadia Code、JetBrains Mono），子集化后入库
  `skills/terminal-screenshot/assets/fonts/`（每平台约 100KB，附 LICENSE）；
- HTML 模板 `@font-face` 引用仓库内字体，`local()` 平台栈作回退；
- 中文继续走平台回退栈（中文字体体积过大不入库），在模板注释中显式声明。

## 取舍

- 排除 Google Fonts CDN：离线不可用；
- 排除"仅文档声明安装前置"：把可复现性外包给用户，不可靠；
- 中文不入库：子集化后体积仍过大，收益不成比例；接受中文回退的跨平台差异，
  校验协议对中文仅检查"不错位"而非像素一致。
