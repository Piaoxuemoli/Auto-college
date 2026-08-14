---
name: terminal-screenshot
description: >
  Render terminal command outputs as realistic PNG screenshots. Use this skill whenever
  the user wants to "screenshot" a terminal command, generate terminal output images,
  visualize CLI results, create terminal-style screenshots for reports or documentation,
  or any time terminal output needs to be captured as an image. Also trigger proactively
  when the user is writing experiment reports, technical docs, or lab reports that would
  benefit from terminal evidence — suggest capturing the output as a screenshot.
---

# Terminal Screenshot — 三档渲染架构

把终端命令输出渲染成逼真 PNG。核心原则：**让真实终端引擎处理着色与排版**，
手写 HTML span 颜色只作最后回退。

## 决策表

| 内容性质 | 渲染档 | 命令 |
|---|---|---|
| 命令可在本机真实执行（git log、python xx.py 等本地操作） | **Tier 1** freeze 真实执行 | `python scripts/render.py --execute "<cmd>" --name <slug>` |
| 伪造内容（GPU 服务器、SSH 远程、不存在的结果） | **Tier 2** ANSI + termframe 真模拟器 | 先写 session spec JSON，`python scripts/render.py --spec spec.json --name <slug>` |
| freeze/termframe 均不可用 | **Tier 3** HTML → 无头浏览器 | 按 `references/html-templates.md` 写 HTML，`python scripts/render.py --html page.html --name <slug>` |

会话画像（Tier 2/3 用）：`PS C:\...>` → powershell 预设；`C:\...>` → cmd；
`%` 结尾提示符/brew → macOS zsh；`user@host:path$`/nvidia-smi/systemctl → SSH
（实验报告默认）；复古/游戏场景 → CRT。完整预设目录见 `references/terminal-types.md`。

## Tier 2 session spec 格式

```json
{
  "preset": "ssh", "user": "ubuntu", "host": "gpu-a100-01", "path": "~/train",
  "commands": [
    {"cmd": "nvidia-smi", "output": ["+-----------------------------------------------------------------------------+", "|  ...表格行...  |"]}
  ]
}
```

preset 取值：`ssh` / `root` / `zsh` / `powershell` / `cmd` / `crt`。
提示符配色由 `scripts/ansi_builder.py` 按预设自动生成（truecolor 转义序列）。

## 逼真度要点

- **Tier 1 物理真实**：freeze 真实执行并捕获 ANSI，字体度量/着色/间距无可挑剔，优先选它。
- **Tier 2 引擎真实**：termframe 是真正的终端模拟器，ANSI 着色、光标由引擎渲染；
  其 SVG 输出会自动用无头浏览器栅格化为 PNG（不可用时交付 SVG）。
- **提示符语法必须精确**：PowerShell `PS ...>`、zsh `%`、Linux `user@host:path$` / `root#`。
  SSH 场景用本地终端 chrome + 远程提示符，不要凭空造"服务器 GUI"。
- **短输出克制**：短 Linux/服务器输出渲染为无边框证据片段，除非内容含 SSH 登录过程
  或用户明确要完整终端窗口（Tier 3 质检会警告）。
- **工具缺失不打断流程**：render.py 会尝试自动安装（brew/go/scoop/cargo），
  全部失败退出码 2 —— 告知用户"本次跳过截图"并继续任务。

## 输出

`outputs/YYYY-MM-DD/HHMMSS-<slug>/`，含 PNG 及对应源文件（.ansi/.svg/.html），
交付时报目录路径。退出码：0 成功 / 1 输入错误 / 2 无工具可跳过。
