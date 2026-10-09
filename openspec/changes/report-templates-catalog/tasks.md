# Tasks: report-templates-catalog

> 每条完成后勾选；验收标准是可验证的判定，不是描述。

- [x] 1. 建立目录与索引：`skills/lab-report/templates/` + `INDEX.md`。
  验收：目录存在；INDEX.md 列出全部模板及其 frontmatter 元数据
  （name/scope/language/sections）。
- [x] 2. 迁移内置模板：十段式 zh/en 进入 catalog。
  验收：catalog 条目内容与 `references/report-template-*.md` 一致，frontmatter 合法。
- [x] 3. 模板选择决策表：实现"课程模板 → 用户偏好 → 学科默认 → 内置默认"顺序。
  验收：SKILL.md（或脚本）实现该顺序；任一前置分支缺失时安全落到内置默认。
- [x] 4. 用户偏好记忆：同课程二次报告默认命中上次选择。
  验收：偏好持久化于 `~/.auto-college/lab-report/`；重开会话后命中。
- [ ] 5. 首批学科模板（可选，不阻塞）：至少 1 个真实学科模板（如计算机网络）。
  验收：按新模板产出样本报告无结构缺段。
- [ ] 6. 文档与归档：更新 `docs/lab-report.md`；spec delta 合并进
  `openspec/specs/lab-report/spec.md`；roadmap.md 勾销 T1。
  验收：三处文档一致；tasks 全勾。

## 未勾项原因 / Notes

- **任务 1/2 与 spec 的实现偏差**：索引文件采用 `templates/catalog.md`
  （而非 `INDEX.md`）；name/scope/language/sections 元数据承载于 catalog.md
  索引表列，模板文件本体未加 frontmatter——因迁移要求 `git mv` 原样保留
  `report-template-zh.md` / `-en.md` 内容不变。模板正文与原
  `references/report-template-*.md` 逐字节一致（git 重命名，无内容改动）。
- **任务 4 验证方式**：`course_templates.py` save 后新进程 get 命中
  （临时路径实测）；正式持久化位置为
  `~/.auto-college/lab-report/course_templates.json`。
- **任务 5 未勾**：需要真实课程模板材料（如计算机网络）制作并产出样本报告
  验证无结构缺段，本次未提供该材料；任务自身标注可选、不阻塞。
- **任务 6 未勾**：`docs/lab-report.md` 已更新，但 spec delta 合并进
  `openspec/specs/lab-report/spec.md` 与 `docs/roadmap.md` 勾销 T1 属归档阶段，
  且超出本次任务允许修改的文件范围（该两处对旧路径
  `references/report-template-*.md` 的引用随之在归档时一并更新）。
