# terminal-screenshot

将终端命令输出渲染为逼真 PNG 截图。核心原则：**让真实终端引擎处理着色与排版**，
采用三档渲染架构（freeze 真实执行 → termframe 真模拟器渲染 ANSI → HTML 模板回退）。

Render terminal command output as realistic PNG screenshots via a three-tier
pipeline: real execution through [freeze](https://github.com/charmbracelet/freeze),
real-terminal-engine rendering of forged content through
[termframe](https://github.com/pambirus/termframe), and an HTML template fallback.

## 快速示例 / Quick Example

```bash
# Tier 1：真实执行本地命令（逼真度最高）
python terminal-screenshot/scripts/render.py --execute "git log --oneline -5" --name git-log

# Tier 2：伪造内容（如 GPU 服务器会话）—— 先写 session spec JSON
python terminal-screenshot/scripts/render.py --spec session.json --name gpu-ssh

# Tier 3：HTML 回退（freeze/termframe 不可用时）
python terminal-screenshot/scripts/render.py --html page.html --name legacy-shot
```

Tier 2 的 session spec 格式：

```json
{
  "preset": "ssh", "user": "ubuntu", "host": "gpu-a100-01", "path": "~/train",
  "commands": [
    {"cmd": "nvidia-smi", "output": ["+---------------------+", "|  ...  |"]}
  ]
}
```

preset 支持：`ssh` / `root` / `zsh` / `powershell` / `cmd` / `crt`。

![terminal-screenshot example](../skills/terminal-screenshot/example.png)

> Windows Terminal PowerShell 7 风格（HTML 回退管线，Playwright 生成）。
> Windows Terminal PowerShell 7 style via the HTML fallback pipeline.

## 三档渲染架构 / Three Tiers

| 档 | 工具 | 适用 | 逼真度来源 |
|----|------|------|-----------|
| Tier 1 | [freeze](https://github.com/charmbracelet/freeze) `--execute` | 本机可真实执行的命令 | 真实执行 + ANSI 捕获，字体度量/着色物理级真实 |
| Tier 2 | [termframe](https://github.com/pambirus/termframe) + `ansi_builder.py` | 伪造内容（GPU 服务器、SSH 远程等） | 真终端模拟器引擎渲染 truecolor ANSI，内置 iTerm2 主题与窗口样式 |
| Tier 3 | `html_to_png.py` HTML 模板 | 外部工具不可用 | 高保真模板 + freeze/codeshot 风格视觉（外圈背景/圆角/阴影） |

工具缺失时 render.py 自动尝试安装（brew / go / scoop / cargo），全部失败退出码 2，
调用方跳过截图继续工作流。

## 支持的终端画像 / Session Profiles

| 类型 / Type | 提示符 / Prompt | 备注 |
|-------------|----------------|------|
| Windows PowerShell 7 | `PS C:\...>` | 标签栏、窗口按钮 |
| Windows cmd | `C:\...>` | 单色简洁 |
| macOS zsh | `user@host dir %` | 红绿灯按钮 |
| Linux/SSH server | `user@host:path$` / `root#` | 实验报告默认；本地 chrome + 远程提示符 |
| CRT 复古终端 | `$`（绿色/琥珀荧光） | 扫描线、发光、暗角（仅 HTML 档） |

完整预设与检测规则见 `skills/terminal-screenshot/references/terminal-types.md`。

## 文件结构 / File Structure

```
terminal-screenshot/
├── SKILL.md                    # Skill 指令 / Skill instructions
├── example.png                 # 样例输出 / Sample output
├── outputs/                    # 生成物（git 忽略）/ generated outputs (gitignored)
├── configs/
│   └── freeze-base.json        # Tier 1 freeze 视觉配置 / freeze visual config
├── references/
│   ├── terminal-types.md       # 色板与检测规则 / palettes & detection rules
│   ├── html-templates.md       # HTML/CSS 模板（含 freeze 风格舞台样式）
│   ├── stage-backgrounds.md    # 程序化壁纸舞台预设 / procedural wallpaper stages
│   └── example-powershell.html # example.png 的可复现源文件 / reproducible source
└── scripts/
    ├── render.py               # 统一渲染入口 / unified three-tier entry
    ├── ansi_builder.py         # session spec → ANSI 转义序列 / spec → ANSI
    └── html_to_png.py          # Tier 3 HTML→PNG 回退管线 / fallback pipeline
```

## 真实背景 / Realistic Backdrops

带窗口的截图悬浮在桌面壁纸上（不再是纯色背景）：程序化 CSS 壁纸预设
`win11-bloom` / `win11-dark` / `macos-gradient` / `plain-dark` / `plain-light`，
或 `custom` 直接引用真实壁纸图片。窗口阴影与圆角按 OS 匹配。详见
`references/stage-backgrounds.md`。

## 跨平台 / Cross-Platform

- 工具安装链：freeze（brew/go/scoop）、termframe（brew/cargo/scoop）；
  Windows 无官方源时提示手动安装，Tier 3 回退全平台可用。
- HTML 模板使用平台专属字体栈（Cascadia Mono / SF Mono / JetBrains Mono + 中文回退）。
- 脚本统一 pathlib 与 `file:///` URL，Windows/macOS/Linux 一致。

## 许可证 / License

MIT
