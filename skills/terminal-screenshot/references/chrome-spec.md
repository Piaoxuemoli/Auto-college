# Chrome Fidelity Spec — 顶部栏官方精确规格

顶部栏（标题栏 + 标签栏）是终端伪造最易穿帮的区域。本文件给出官方来源的
精确数值，所有带窗口框架的模板必须遵守。来源见文末。

## Windows 11 标题栏（官方：Microsoft Learn titlebar-design）

| 元素 | 规格 |
|------|------|
| 标题栏高度 | **32px** |
| 窗口图标 | 16×16px，距左边缘 16px，垂直居中（32px 栏时上下各 8px） |
| 标题字体 | Segoe UI Variable（无则 Segoe UI），caption 样式，距图标 16px |
| Caption 按钮 | 全出血背板（full bleed，无圆角无内边距的整块命中区），宽 **46px** × 高 **32px**，锚定右缘 |
| Caption 图标字形（Segoe Fluent Icons） | 最小化 **E921** ChromeMinimize；最大化 **E922** ChromeMaximize（圆角矩形描边）；还原 **E923** ChromeRestore（双层圆角矩形）；关闭 **E8BB** ChromeClose（×） |
| 状态 | 未激活时所有元素半透明 |

正确写法（Windows 主机上无头浏览器可直接使用系统字体）：

```html
<span style="font-family:'Segoe Fluent Icons','Segoe MDL2 Assets'">&#xE921;</span>
```

非 Windows 渲染主机用 CSS 绘制回退（描边 1px、E922 是圆角外框、E923 双层框），
禁止使用文字 `+ ─ □ ×` 冒充。

## Windows Terminal 标签栏（官方实现：microsoft/terminal + WinUI TabView）

| 元素 | 规格 |
|------|------|
| 标签高度 | **34px**（WinUI TabView 默认，含上下内边距） |
| 标签图标 | 16×16px（profile 图标，如 PowerShell 徽标） |
| 标签文字 | 12px Segoe UI，未激活标签文字 #999 系，激活标签 #FFF 系 |
| 新建标签按钮 | Segoe Fluent Icons **E710**（Add），约 28×28 命中区，紧随最后一个标签 |
| 下拉按钮 | Segoe Fluent Icons **E70D**（ChevronDown），约 28×28，紧随新建按钮 |
| 激活标签 | 悬浮于标签条之上（底部贴合内容区），背景与终端内容区同色 |
| Caption 按钮 | 同上表 Windows 11 规格（Terminal 标题栏即系统标题栏融合标签） |

## macOS 红绿灯（逆向工程 SVG，CC0，已存 assets/macos-traffic-lights/）

| 元素 | 规格 |
|------|------|
| 按钮直径 | **12px**（@1x；macOS 26 Tahoe 起略大） |
| 中心间距 | **20px**（红→黄→绿，红最靠左） |
| 距窗口边缘 | 中心距左缘约 20px、距顶缘约 20px（标题栏高 28px） |
| 结构 | 主体填充色 + **1px 更深的描边环**（关键细节，见 SVG 的双 path） |
| 现代配色（Big Sur+） | 关闭 `#FF5F57`/描边 `#E0443E`；最小化 `#FEBC2E`/`#D89E24`；缩放 `#28C840`/`#1AAA29` |
| 旧版配色（Yosemite era，SVG 原值） | `#ED6A5F`/`#E24B41`；`#F6BE50`/`#E1A73E`；`#61C555`/`#2DAC2F` |
| 未激活窗口 | 三键灰色 `#DDDDDD`/`#D1D0D2`（0-all-three-nofocus.svg） |
| hover 符号 | 键内 × − + 深色符号（截图默认 rest 态，不显示符号） |

模板中直接内联 assets 里的 SVG（等比缩放到 12px）优于 CSS 圆形手画。

## macOS Terminal 窗口造型（无需任何 Apple 版权素材）

| 元素 | 规格 |
|------|------|
| 标题栏高度 | **28px**（标准无工具栏 titlebar） |
| 红绿灯 | 见上节：12px、间距 20px、中心 ~20,20px、1px 描边环 |
| 窗口标题 | 居中，系统字体（SF Pro 回退 -apple-system/Helvetica）13px semibold |
| 标题栏配色 | 深色主题下标题栏与内容区同色融合（Terminal 偏好设置"使用系统主题"时）；亮色主题浅灰 `#ECECEC` 带 1px 底部分隔线 |
| 窗口圆角/阴影 | 圆角 ~10px；阴影 `0 22px 70px 4px rgba(0,0,0,.56)` 系 |
| 图标 | 默认标题栏**无图标**（居中标题文字即可），避免使用 Apple 版权图标 |

macOS Chrome 的全部素材需求已由 CC0 红绿灯 SVG + 系统字体 + CSS 覆盖。

## GNOME Terminal / Ubuntu（libadwaita 造型）

| 元素 | 规格 |
|------|------|
| Headerbar 高度 | **47px**（上下 6px padding + 35px 控件高度） |
| Headerbar 配色 | 暗色 `#303030` 系（`@headerbar_bg_color`），与窗口背景接近但有区分；底部无边框（libadwaita 风格下与内容融合） |
| 窗口圆角 | **12px**（libadwaita `window { border-radius: 12px }`），headerbar 顶角随之圆角 |
| 汉堡菜单 | headerbar **右侧**，16×16 三条圆头线（`assets/symbolic/open-menu-symbolic.svg`） |
| 新标签按钮 | 汉堡左侧 `+`（Breeze/GTK 风格细十字） |
| 标签药丸（pill） | 圆角全圆角胶囊，内嵌 16px 终端字形（`assets/symbolic/utilities-terminal-symbolic.svg`）+ 标签文字；激活药丸底色与内容区分 |
| 标题 | headerbar 居中，13px bold（Cantarell 回退 system-ui） |
| 服务器/SSH 场景 | 桌面 Linux 截图才用 GNOME chrome；远程 SSH 仍按"本地终端 chrome + 远程提示符"原则 |

注意：Ubuntu 22.04+ 的 gnome-terminal headerbar 可通过 dconf
(`/org/gnome/terminal/legacy/headerbar`) 切换菜单/标签按钮，默认含汉堡菜单与
标签药丸；渲染前与用户确认或采默认布局。

## KDE Konsole / xterm

报告场景较少见：Konsole 用 Breeze 造型（标签条 + `+`/分屏图标，LGPL 资产需随附许可）；
xterm 无窗口装饰细节要求（纯 X 标题栏，通常渲染为无边框片段即可）。

## CRT / 其他预设

复古预设无系统 chrome 规格约束，保持模板既有样式即可。

## 容差（渲染验证用）

- 尺寸类（px）：±1px（@1x）
- 颜色类：ΔE ≤ 5 或 RGB 欧氏距离 ≤ 20
- 对齐类（垂直居中、底边贴合）：±1px
- 字形：必须是官方字形或其 CSS 等价绘制，禁止任意替换符号

## 来源 / Sources

- Microsoft Learn — Windows app title bar（32px、16×16 图标、E921/E922/E923/E8BB、full bleed）
  https://learn.microsoft.com/en-us/windows/apps/design/basics/titlebar-design
- microsoft/terminal（MIT）与 WinUI TabView 默认模板（34px 标签、16px 图标、12px 文字、E710/E70D）
  https://github.com/microsoft/terminal · https://github.com/microsoft/microsoft-ui-xaml
- macOS traffic lights 逆向 SVG（CC0）
  https://github.com/lwouis/macos-traffic-light-buttons-as-SVG
- libadwaita headerbar（47px 默认、`@headerbar_bg_color` ≈ #303030、窗口 12px 圆角）
  https://gitlab.gnome.org/GNOME/libadwaita/-/issues/207 ·
  https://discourse.gnome.org/t/how-to-reduce-height-of-gtk-headerbars/3034
- gnome-terminal headerbar（汉堡菜单/标签药丸，Ubuntu dconf 开关）
  https://gitlab.gnome.org/GNOME/gnome-terminal/-/issues/44 ·
  https://unix.stackexchange.com/questions/747356/terminal-hamburger-menu
- 社区测量的 Win11 caption 按钮 46×32 命中区（非官方文档值，但与系统一致）
