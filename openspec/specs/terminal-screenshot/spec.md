# terminal-screenshot — 能力基线

> 只描述当前已实现且为真的系统。改动走 `openspec/changes/`，归档时才合并进本文。

## Purpose

把终端命令输出渲染成与实机无异的 PNG 证据截图。核心原则：让真实终端引擎处理
着色与排版，手写 HTML 颜色只作最后回退。

## Requirements

### Requirement: 三档渲染架构

按内容性质分档，工具缺失自动降级，不打断调用方工作流：

| 档 | 工具 | 适用 |
|----|------|------|
| Tier 1 | freeze `--execute` | 本机可真实执行的命令（物理级真实） |
| Tier 2 | termframe + `ansi_builder.py` `--spec` | 伪造内容（GPU 服务器、SSH 远程） |
| Tier 3 | HTML 模板 `--html` | 外部工具不可用的全平台回退 |

#### Scenario: 伪造 GPU 服务器会话

- **WHEN** 用户提供 session spec JSON（preset/user/host/path/commands）
- **THEN** 走 Tier 2 输出 PNG；SVG 栅格化不可用时交付 SVG

#### Scenario: 工具缺失

- **WHEN** freeze 与 termframe 均不可用，且自动安装（brew/go/scoop/cargo）失败
- **THEN** 退出码 2，调用方跳过截图继续任务

### Requirement: 会话画像（preset）

preset 取值：`ssh` / `root` / `zsh` / `powershell` / `cmd` / `crt`。
提示符语法必须精确：PowerShell `PS ...>`、zsh `%`、Linux `user@host:path$` /
`root#`。SSH 场景用本地终端 chrome + 远程提示符，不凭空造"服务器 GUI"。

### Requirement: chrome 官方规格

顶部栏三类平台严格按 `references/chrome-spec.md`：

- Windows：32px 标题栏 + 46×32 caption 按钮（Segoe Fluent Icons 字形）；
- macOS Terminal：28px 标题栏 + 红绿灯 12px、间距 20px；
- GNOME：47px headerbar + 12px 窗口圆角 + 汉堡菜单。

图标只用 CC0 资产（`assets/macos-traffic-lights/`、`assets/symbolic/`），
不引入 Apple / Yaru 版权资产。

### Requirement: chrome 校验协议

模板完成后按 `references/chrome-validation.md` 校验通过才算交付：
`scripts/chrome_probe.py` 像素探针（先跑数字）+ 多模态模型对照
`assets/golden/` 实机金标准（再看图），输出结构化报告。

#### Scenario: 新模板交付

- **WHEN** 新平台/新样式 HTML 模板完成
- **THEN** 探针数值与规格一致，多模态对照无 BLOCK 级差异，方可合入

### Requirement: 舞台背景

带窗口的截图必须悬浮在桌面壁纸上，不纯色贴边。程序化预设：
`win11-bloom` / `win11-dark` / `macos-gradient` / `plain-dark` / `plain-light`，
或 `custom` 引用真实壁纸图片；阴影与圆角匹配对应 OS。
短 Linux/服务器输出渲染为无边框证据片段（无舞台），除非含 SSH 登录过程或
用户明确要求完整窗口。

### Requirement: 示例可复现

三平台示例源文件在 `references/example-*.html`，命令行可重渲染出 `example*.png`。

#### Scenario: 重渲染示例

- **WHEN** 运行 `render.py --html references/example-powershell.html --name example`
- **THEN** 产出与仓库示例一致的 PNG

### Requirement: 退出码与输出

- 退出码：0 成功 / 1 输入错误 / 2 无工具可跳过；
- 输出 `outputs/YYYY-MM-DD/HHMMSS-<slug>/`，含 PNG 及对应源文件
  （.ansi/.svg/.html），交付时报目录路径。

### Requirement: 字体（现状基线，待 fonts-local 变更替换）

HTML 模板使用平台字体栈：Windows Cascadia Mono/Consolas + 微软雅黑回退；
macOS SF Mono/Menlo + PingFang SC；Linux JetBrains Mono/Ubuntu Mono +
Noto Sans CJK，保证中文输出不错位。
