# Tasks: report-image-embedding

> 待其他工作区实现后勾选；验收标准是可验证的判定，不是描述。

- [ ] 1. 图注与编号规范定稿。
  验收：规范写入本提案（或 references/）并同步 roadmap T3 结论；
  含中英模板的图注格式示例。
- [ ] 2. 引用路径约定。
  验收：MD 成稿中的图片引用在 md 交付与 docx 导出两条路径下均可解析。
- [ ] 3. 尺寸与压缩策略。
  验收：超限图片自动缩放/降采样；原图保留于 `raw_outputs/`；阈值可配置。
- [ ] 4. 导出链路验证。
  验收：官方 docx skill 导出的 DOCX 中图片、图注、编号完整；
  PDF 路径同验（依赖 T4 结论）。
- [ ] 5. 失败回退。
  验收：图片缺失时交付物含图注 + 占位说明，流程不中断。
- [ ] 6. 文档与归档：更新 `docs/lab-report.md`；spec delta 合并进
  `openspec/specs/lab-report/spec.md`。
  验收：文档与实现一致；tasks 全勾。
