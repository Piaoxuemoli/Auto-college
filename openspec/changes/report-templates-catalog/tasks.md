# Tasks: report-templates-catalog

> 每条完成后勾选；验收标准是可验证的判定，不是描述。

- [ ] 1. 建立目录与索引：`skills/lab-report/templates/` + `INDEX.md`。
  验收：目录存在；INDEX.md 列出全部模板及其 frontmatter 元数据
  （name/scope/language/sections）。
- [ ] 2. 迁移内置模板：十段式 zh/en 进入 catalog。
  验收：catalog 条目内容与 `references/report-template-*.md` 一致，frontmatter 合法。
- [ ] 3. 模板选择决策表：实现"课程模板 → 用户偏好 → 学科默认 → 内置默认"顺序。
  验收：SKILL.md（或脚本）实现该顺序；任一前置分支缺失时安全落到内置默认。
- [ ] 4. 用户偏好记忆：同课程二次报告默认命中上次选择。
  验收：偏好持久化于 `~/.auto-college/lab-report/`；重开会话后命中。
- [ ] 5. 首批学科模板（可选，不阻塞）：至少 1 个真实学科模板（如计算机网络）。
  验收：按新模板产出样本报告无结构缺段。
- [ ] 6. 文档与归档：更新 `docs/lab-report.md`；spec delta 合并进
  `openspec/specs/lab-report/spec.md`；roadmap.md 勾销 T1。
  验收：三处文档一致；tasks 全勾。
