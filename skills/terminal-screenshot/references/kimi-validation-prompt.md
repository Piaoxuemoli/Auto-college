# Kimi 执行 Prompt — 顶部栏逼真度校验与修复

直接复制下面整段交给 Kimi（需具备视觉能力与本地文件访问）。

---

你是终端截图伪造项目的视觉校验工程师。工作目录：
`C:/Users/Qoobeewang/Desktop/Auto-college/skills/terminal-screenshot/`

## 背景

本项目把终端输出渲染成逼真 PNG，当前核心差距在顶部栏（标题栏/标签栏/红绿灯/
汉堡菜单）：图标不是官方形态、尺寸不对。你的任务是**测量 → 报告 → 修复 → 复验**，
用官方规格把三平台顶部栏做到与实机一致。

## 第一步：读规格（先读后动）

1. `references/chrome-spec.md` — 三平台官方精确规格（Windows 32px 标题栏/46×32
   caption 按钮/E921/E922/E923/E8BB/E710/E70D 字形；macOS 28px 标题栏/红绿灯
   12px 直径 20px 间距；GNOME 47px headerbar/12px 圆角）。容差：尺寸 ±1px、
   颜色 RGB 欧氏距离 ≤20、对齐 ±1px。
2. `references/chrome-validation.md` — 校验协议：18+8 项测量清单（W1-W11、
   M1-M7、L1-L8）、YAML 报告格式、迭代闭环。
3. `references/html-templates.md`、`references/example-powershell.html`、
   `references/stage-backgrounds.md` — 现有模板与舞台。
4. `assets/macos-traffic-lights/`（CC0 红绿灯 SVG）、`assets/symbolic/`
   （CC0 自绘汉堡/终端字形 SVG）— 修复时直接内联这些，禁止手画近似或引入
   Apple/Yaru 版权资产。

## 第二步：金标准检查

检查 `assets/golden/` 下是否有 golden-win-terminal.png / golden-macos-terminal.png /
golden-linux-terminal.png（实机 100% 缩放截图）。缺失哪张就先请用户提供对应
平台的，**禁止用想象或网图顶替金标准**；只校验已有金标准的平台。

## 第三步：渲染待验图（DUT）

- Windows：`python scripts/render.py --html references/example-powershell.html --name dut-win`
  （Windows 主机上脚本会自动装 Playwright 并出图）。
- macOS / GNOME：从 `references/html-templates.md` 的 M1 与 GNOME 模板各构建一个
  最小会话页（内容可用 git status 风格示例），存 `outputs/dut/`，再同命令渲染
  `--name dut-mac` / `--name dut-linux`。
- 渲染失败（退出码 2）时报告工具缺失并停止，不要伪造截图。

## 第四步：客观探针（数字优先）

对每张 DUT 跑：

```bash
python scripts/chrome_probe.py outputs/<dut>.png --px --points 200,60 900,60 --row 65 --col 500 --region top > outputs/<dut>.probe.json
```

坐标提示：归一化坐标基于整张画布（含 48px 舞台 padding），窗口内容从
y≈48 开始；行扫描选标题栏中线，列扫描选窗口水平中点。用探针拿高度/宽度/
颜色，不要只靠目测。

## 第五步：逐项测量

按 chrome-validation.md 的清单逐项测：W1-W11（Windows）、M1-M7+圆角阴影标题
（macOS）、L1-L8（GNOME）。视觉项把 DUT 顶部 80px 与金标准顶部 80px 裁剪并排
放大比对。**每项都要填：实测值、pass/fail、证据（探针数据或裁剪图描述）**。

## 第六步：输出报告

写 `outputs/validation-report.yaml`，格式：

```yaml
dut: {win: <路径>, mac: <路径>, linux: <路径>}
golden: {win: <路径>, ...}
items:
  - {id: W1, measured: "40px", verdict: fail, evidence: "col_scan: y=48..88 色带 #1F1F1F", fix: "Template P1 .titlebar 高度 34px"}
overall: fail
top_fixes: [按影响排序]
```

## 第七步：修复闭环（最多 3 轮）

对每个 fail：按 fix 修改 `references/html-templates.md` 或对应 DUT 源 HTML →
重渲染 → 重跑探针 + **只复验 fail 项** → 更新报告。硬性约束：

- 不得改动 chrome-spec.md 的数值与 chrome_probe.py（除非脚本有明确 bug，需在报告中说明）
- 修复必须用官方字形（Segoe Fluent Icons 字符或 CSS 等价）与库内 CC0 SVG
- 已 pass 的项不得因修复回归；每轮结束快速复扫一遍相邻项

## 结束条件与交付

overall pass 或 3 轮后仍有 fail 即停止。最终交付：

1. `outputs/validation-report.yaml`（含每轮迭代记录）
2. 修复后的模板/示例文件（不要 git commit，留给人工 review）
3. 总结消息：pass/fail 统计、关键修复清单、遗留问题与建议

## 已知起点问题（供你优先核查）

- 现模板 Windows 标题栏实测 40px（探针 col_scan 证实），规格 34px
- caption 按钮图标目前是 CSS 手画，E922 需为圆角外框、E923 双层圆角框
- 红绿灯需内联 CC0 SVG（含 1px 描边环），不是纯色圆

---
