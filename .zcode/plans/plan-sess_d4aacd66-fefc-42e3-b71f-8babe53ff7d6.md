# 分支：`refactor/terminal-focus` — 聚焦终端伪造截图，引入开源渲染引擎

## 调研结论（设计依据）
- **freeze**（charmbracelet）：`--execute "cmd"` 真实执行捕获 ANSI 渲染，主题/padding/背景/圆角/阴影/窗口 chrome 全可配置（JSON config）——真实可执行命令的逼真度天花板。
- **termframe**：接受管道 stdin 的非交互终端模拟器，完整 ANSI（16/256/真彩色）+ iTerm2 主题集 + macOS/compact 窗口样式——**伪造内容**也能由真实模拟器引擎渲染着色，这是本方案的关键。
- 现有 skill 的手写 `<span>` 颜色模拟是主要失真来源，改为统一 ANSI 序列 + 真实引擎渲染。

## 1. 拉分支
`git checkout -b refactor/terminal-focus`

## 2. Skill 清理
- 删除 `skills/paper-writer/`、`skills/coursework-helper/`、`skills/study-index/` 及对应 docs。
- `skills/lab-report/` 压缩为 ≤60 行"要求 + 流程"版 SKILL.md，删除 agents/assets/evals 等重资产，保留 DOCX 导出脚本；docs 同步精简。

## 3. terminal-screenshot 重构（核心）
### 3.1 新渲染架构（三档）
`scripts/html_to_png.py` 改造为 `scripts/render.py` 统一入口，按内容选择渲染档位：
1. **Tier 1 — freeze 真实执行**：内容是本机可真实执行的命令（如 `git log`、`python train.py` 已有输出的重放）→ `freeze --execute` + 预置 JSON config（窗口样式、padding、背景、字体），输出物理级真实。
2. **Tier 2 — ANSI + 真实模拟器**：伪造内容（GPU 服务器、远程 SSH 等）→ 新增 `scripts/ansi_builder.py`，按预设（PowerShell/zsh/SSH/CRT）生成带真彩色 ANSI 转义序列的文本（提示符着色、输出着色、光标），管道喂给 termframe（优先，支持窗口样式+iTerm2 主题如 Campbell 匹配 Windows 观感）渲染 SVG/PNG。
3. **Tier 3 — HTML 回退**：外部工具不可用时走现有 HTML→Playwright 管线，保留并强化模板。
### 3.2 HTML 模板吸收 freeze 视觉体系
`references/html-templates.md` 增强：外圈可配置背景（纯色/渐变）、窗口 padding + 圆角 + 阴影、Windows Terminal 标签栏细节、macOS 红绿灯按钮、光标闪烁态——对齐 freeze/codeshot 的成品观感。
### 3.3 SKILL.md 精简
重写为决策表 + 短流程：判断内容性质（真实可执行？伪造？）→ 选渲染档位 → 选会话预设 → 生成 ANSI/HTML → 渲染 → 质检。去掉长篇政策段落。
### 3.4 工具自动配置
沿用现有 Phase A/B/C 思路：检测 freeze/termframe，缺失时尝试安装（brew/scoop/go install/cargo），失败降级下一档，不打断工作流。

## 4. 配套更新
README.md、setup.js、docs/terminal-screenshot.md 按新架构重写。

## 5. 验证
- Tier 1：本机 `freeze --execute "git log --oneline -5"` 出图。
- Tier 2：手工构造一段带 ANSI 的伪 SSH 输出走 termframe 出图。
- Tier 3：HTML 回退路径渲染对比图。
- `node setup.js` 干跑验证安装器。

## 6. 提交
分逻辑提交：清理 / lab-report 精简 / 渲染架构重构 / 模板视觉强化 / 文档。