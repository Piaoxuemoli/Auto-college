# Stage Backgrounds — 真实的终端外背景

真实截图从来不是"悬浮在纯色上的窗口"：终端窗口背后是一张**桌面壁纸**。
本文件定义程序化（纯 CSS、无图片资产、跨平台可复现）的壁纸预设，
以及使用真实壁纸图片的选项。

选择规则：

| 场景 | 舞台预设 |
|------|---------|
| Windows Terminal 截图（PowerShell/cmd） | `win11-bloom` 或 `win11-dark` |
| macOS Terminal 截图 | `macos-gradient` |
| Linux/GNOME 截图 | `plain-dark` 或发行版近似渐变 |
| 嵌入报告的证据片段（无窗口） | 不用舞台，边到边渲染 |
| 用户提供了自己的壁纸/要求极度真实 | `custom`（真实图片） |

## 预设

### win11-bloom — 仿 Windows 11 默认壁纸的抽象光晕

```css
.stage {
    padding: 48px 56px;
    display: flex;
    justify-content: center;
    background:
        radial-gradient(900px 600px at 68% 38%, rgba(120, 174, 255, 0.34), transparent 62%),
        radial-gradient(700px 500px at 34% 66%, rgba(64, 132, 224, 0.30), transparent 60%),
        radial-gradient(520px 380px at 52% 22%, rgba(171, 124, 255, 0.20), transparent 65%),
        linear-gradient(152deg, #0e1626 0%, #101b30 46%, #0b1220 100%);
}
```

### win11-dark — Windows 11 深色简洁壁纸

```css
.stage {
    padding: 48px 56px;
    display: flex;
    justify-content: center;
    background:
        radial-gradient(1100px 700px at 50% 120%, rgba(58, 92, 148, 0.28), transparent 65%),
        linear-gradient(180deg, #14181f 0%, #0f131a 100%);
}
```

### macos-gradient — 仿 macOS Sonoma/Big Sur 多彩渐变

```css
.stage {
    padding: 48px 56px;
    display: flex;
    justify-content: center;
    background:
        radial-gradient(800px 500px at 22% 18%, rgba(255, 158, 128, 0.22), transparent 60%),
        radial-gradient(900px 600px at 78% 30%, rgba(96, 160, 255, 0.26), transparent 62%),
        radial-gradient(700px 500px at 50% 88%, rgba(142, 112, 219, 0.22), transparent 60%),
        linear-gradient(160deg, #232737 0%, #1d2434 52%, #171c29 100%);
}
```

### plain-dark — 中性暗色（Linux/通用，最克制）

```css
.stage {
    padding: 48px 56px;
    display: flex;
    justify-content: center;
    background: #17181f;
}
```

### plain-light — 亮色桌面（浅色主题终端）

```css
.stage {
    padding: 48px 56px;
    display: flex;
    justify-content: center;
    background: #e9eaee;
}
```

### custom — 真实壁纸图片（最高真实度）

```css
.stage {
    padding: 48px 56px;
    display: flex;
    justify-content: center;
    background: url("file:///path/to/wallpaper.jpg") center/cover no-repeat;
}
```

用户提供的壁纸直接引用本地路径（仅渲染用，不拷入仓库）。

## 窗口与舞台的配合规则

1. **窗口阴影必须与 OS 匹配**：Windows 11 是柔和的大模糊阴影
   （`box-shadow: 0 16px 48px rgba(0,0,0,.45), 0 2px 8px rgba(0,0,0,.3)`）；
   macOS 是更贴身的阴影（`0 22px 70px 4px rgba(0,0,0,.56)` 附近，且窗口圆角
   约等于 macOS 系统窗口 10-12px）。
2. **壁纸上不要放任何图标/任务栏**——证据截图是窗口特写，不是全屏桌面；
   画蛇添足的任务栏反而暴露伪造。
3. **渐变必须退化为"背景感"**：光晕透明度保持在 0.2-0.35，被窗口遮挡大部分，
   只露出四周;一眼看去是"壁纸"，不是"海报"。
4. freeze（Tier 1）的 `--background` 只支持纯色舞台，用 `#1e1e2e` 类深色；
   需要壁纸级舞台时改用 Tier 3。

## 跨平台注意

- CSS 渐变由无头浏览器渲染，Windows/macOS/Linux 一致，无字体依赖。
- `custom` 壁纸路径 Windows 用 `file:///C:/...`，unix 用 `file:///home/...`。
- 亮色舞台（plain-light）配亮色终端预设（xterm Classic Light 等）。
