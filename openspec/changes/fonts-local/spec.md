# Spec Delta: fonts-local

## MODIFIED Requirements

### Requirement: 字体

HTML 模板自托管 woff2 等宽字体（OFL 许可，`assets/fonts/`，子集化约 100KB/
平台），`@font-face` 引用；`local()` 平台栈与中文回退栈显式声明。等宽字形
跨平台一致；中文允许平台回退但不得错位。

#### Scenario: 无字体主机渲染

- **WHEN** 渲染主机未安装 Cascadia/JetBrains Mono
- **THEN** 模板仍用仓库内字体渲染，字宽与有字体主机一致

#### Scenario: 字体资产缺失

- **WHEN** `assets/fonts/` 被移除
- **THEN** 回退到平台字体栈，渲染不失败
