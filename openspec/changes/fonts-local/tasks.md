# Tasks: fonts-local

> 每条完成后勾选；验收标准是可验证的判定，不是描述。

- [ ] 1. 字体选型与许可审查：确定入库清单（至少 Cascadia Code、JetBrains Mono
  的 latin 子集）。
  验收：每份字体附 OFL 许可文本；清单记录在 `assets/fonts/README`。
- [ ] 2. 子集化：pyftsubset（或等价工具）生成 woff2。
  验收：每文件约 ≤100KB；覆盖 ASCII + 常用标点。
- [ ] 3. 入库与 @font-face：字体 + LICENSE 进 `assets/fonts/`；
  `references/html-templates.md` 模板改用 @font-face。
  验收：主机未装等宽字体时模板仍正确渲染。
- [ ] 4. 回退栈声明：`local()` 平台栈 + 中文回退在模板中显式声明并注释。
  验收：移除仓库字体后回退生效，无布局崩溃。
- [ ] 5. 跨平台复现验证。
  验收：同一 example 源在三平台渲染，等宽字符宽度一致；
  `chrome_probe.py` 探针数值不因平台漂移。
- [ ] 6. 文档与归档：更新 `docs/terminal-screenshot.md` 与 SKILL.md 字体小节；
  spec delta 合并进 `openspec/specs/terminal-screenshot/spec.md`
  （替换"字体（现状基线）"条目）。
  验收：文档与实现一致；tasks 全勾。
