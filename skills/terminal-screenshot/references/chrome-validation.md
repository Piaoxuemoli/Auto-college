# Chrome Fidelity Validation Protocol — 交给多模态模型执行

目的：用多模态视觉模型把"顶部栏与官方一致"变成可测量、可复核的判定，
替代人眼主观感觉。执行者按本协议逐项测量并输出结构化报告。

## 0. 金标准（golden references）准备

每个平台准备 **2 张真实截图**（用户实机截取，放 `assets/golden/`）：

- `golden-win-terminal.png`：真实 Windows Terminal（默认主题，一个 PowerShell 标签），
  窗口悬浮在默认壁纸上，100% 缩放（非 HiDPI 或注明 DPI）。
- `golden-macos-terminal.png`：真实 macOS Terminal（默认主题）。
- `golden-linux-terminal.png`：真实 Ubuntu gnome-terminal（默认主题，含汉堡菜单）。

金标准只在首次准备；若 OS 大版本变化（如 macOS Tahoe 按钮变大）需重新截取。

## 1. 待验渲染（DUT, device under test）

用 example 源文件渲染（可复现）：

```bash
python scripts/render.py --html references/example-powershell.html --name dut-win
```

macOS 模板从 `references/html-templates.md` Template M1 构建后同样渲染。

## 2. 客观探针（先跑数字，再看图）

```bash
python scripts/chrome_probe.py <png> --region top --points 0.02,0.03 0.965,0.03
```

探针输出顶栏区域的关键像素颜色与宽度跳变（见脚本 --help）。多模态模型
先读探针 JSON 获得客观测量值，再进行视觉比对——**数字优先，视觉复核**。

> 坐标提示：归一化坐标基于**整张画布**（含舞台 padding）。舞台 padding 为
> 48px 时窗口内容从 y≈48 开始；用 `--px` 加窗口偏移定位标题栏行更省事。

## 3. 逐项测量清单（对照 references/chrome-spec.md）

### Windows Terminal DUT

| # | 项目 | 方法 | 通过标准 |
|---|------|------|---------|
| W1 | 标题栏/标签条总高 | 探针垂直扫描色带高度 | 标签 34px ±1，caption 区 32px ±1 |
| W2 | caption 按钮命中区 | 探针水平扫描 hover 背板边界或目测三等分 | 每钮 46px ±1 宽 |
| W3 | 最小化图标形态 | 视觉 | 官方 E921 等价：居中水平细线，非文字 `─` |
| W4 | 最大化图标形态 | 视觉 | E922 等价：圆角外框（非方角），非文字 `□` |
| W5 | 关闭图标形态 | 视觉 | E8BB 等价：标准 ×，线宽一致 |
| W6 | 新建标签按钮 | 视觉 | E710 等价十字，居中于 ~28px 命中区 |
| W7 | 下拉按钮 | 视觉 | E70D 等价下尖角，与 W6 同高 |
| W8 | 标签图标 | 视觉 | 16×16 profile 图标（PowerShell 徽标），清晰非模糊 |
| W9 | 标签文字 | 视觉 | 12px Segoe UI 观感，激活 #FFF/未激活 #999 系 |
| W10 | 激活标签底部 | 探针/视觉 | 与内容区无缝贴合（同色），无 1px 错位线 |
| W11 | 与金标准整体对比 | 并排目测 | 无"一眼假"差异项；列出全部差异及严重度 |

### macOS Terminal DUT

| # | 项目 | 方法 | 通过标准 |
|---|------|------|---------|
| M1 | 红绿灯直径 | 探针色带宽度 | 12px ±1 |
| M2 | 中心间距 | 探针色带中心距 | 20px ±1 |
| M3 | 距窗口左上角 | 探针/目测 | 中心 ~20,20px ±2 |
| M4 | 颜色 | 探针取样 | 三键现代配色 ΔE≤5 或 RGB 距 ≤20 |
| M5 | 1px 描边环 | 视觉（放大 4×裁剪） | 每键外缘有更深的 1px 环 |
| M6 | 标题栏高度 | 探针 | 28px ±1 |
| M7 | 与金标准整体对比 | 并排目测 | 同 W11 |

### GNOME / Ubuntu Terminal DUT（Template: Modern Dark GNOME 系）

| # | 项目 | 方法 | 通过标准 |
|---|------|------|---------|
| L1 | Headerbar 高度 | 探针垂直扫描 | 47px ±1 |
| L2 | 窗口圆角 | 视觉（放大 4× 裁剪角部） | 12px ±1，顶角贴 headerbar |
| L3 | Headerbar 配色 | 探针取样 | 暗色 #303030 系，RGB 距 ≤20 |
| L4 | 汉堡菜单 | 视觉 | 16px 三条圆头线，headerbar 右侧，居中于 ~35px 命中区 |
| L5 | 新标签按钮 | 视觉 | 细十字 `+`，与汉堡同排等高 |
| L6 | 标签药丸 | 视觉 | 全圆角胶囊 + 16px 终端字形 + 文字，激活态底色区分 |
| L7 | 标题 | 视觉 | 居中 13px bold（Cantarell 观感） |
| L8 | 与金标准整体对比 | 并排目测 | 同 W11 |

macOS DUT 除 M1-M7 外加验：窗口圆角 ~10px、阴影观感、标题居中 13px semibold、
标题栏与内容区同色融合（深色主题）。

## 4. 输出格式（逐项填，禁止跳过）

```yaml
dut: <png 路径>
golden: <金标准路径>
probe: <探针 JSON 摘要>
items:
  - id: W1
    measured: "35px"
    verdict: pass|fail
    evidence: "探针：y=40..75 色带 #1F1F1F"
  - id: W4
    measured: "方角方框（CSS border 无 border-radius）"
    verdict: fail
    fix: "Template P1 .cap-max 增加 border-radius:1px"
overall: pass|fail
top_fixes: [按影响排序的修复建议]
```

## 5. 迭代闭环

1. 执行者按报告 `fix` 修改 `references/html-templates.md` / `example-powershell.html`
2. 重新渲染 DUT → 重跑探针 + 全部 fail 项复验
3. 直到 overall: pass；所有 fail→pass 的修改需在报告中留痕

## 6. 人工 review 节点（最后收尾）

评审人只看三处：
- **金标准真实性**：截图确为实机 100% 缩放，主题默认；
- **W11/M7 整体对比**：并排图无系统性差异（间距、字重、图标族）；
- **规格漂移**：修复未破坏 chrome-spec.md 的硬性数值（46×32、34px、12px/20px）。
