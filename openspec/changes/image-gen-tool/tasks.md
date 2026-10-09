# Tasks: image-gen-tool

> 待其他工作区实现后勾选；验收标准是可验证的判定，不是描述。

- [ ] 1. 配置 schema 与样例：`~/.auto-college/image-gen.json` 字段定义 +
  `image-gen.example.json` 入库。
  验收：example 不含真实 key；schema 注明各字段必填性。
- [ ] 2. 适配层脚本：`scripts/image_gen.py` 读配置 → OpenAI-compatible 调用 →
  落盘 outputs/ → 返回路径。
  验收：对任一兼容服务真调通一次；超时/HTTP 错误有清晰报错与退出码。
- [ ] 3. 降级路径：无配置时输出结构化 prompt 模板。
  验收：无配置运行不报错，产出可复用的 prompt 文件。
- [ ] 4. 安全审查。
  验收：全仓库（含模板/文档/示例/日志样例）无任何真实 api_key；
  错误信息中的 key 片段打码。
- [ ] 5. skill 集成：lab-report 需要插图（装置图/流程图）时调用，
  失败/缺配置走文字替代。
  验收：一条端到端样本报告含生成插图；缺配置场景流程不中断。
- [ ] 6. 文档与归档：更新 `docs/`；spec delta 合并进对应 specs 基线。
  验收：文档与实现一致；tasks 全勾。
