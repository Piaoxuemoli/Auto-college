# Spec Delta: image-gen-tool

## ADDED Requirements

### Requirement: 可配置图片生成

用户可在 `~/.auto-college/image-gen.json` 配置 provider/base_url/model/api_key；
统一适配层以 OpenAI-compatible 格式调用；产物入 outputs/ 并返回路径；
无配置时降级输出结构化 prompt 模板，不阻断流程。
api_key 只存本地配置，任何入库文件与日志不得出现。

#### Scenario: 已配置

- **WHEN** 配置存在且 skill 需要插图
- **THEN** 生成图片存 `outputs/<exp>/assets/`，报告可引用

#### Scenario: 未配置

- **WHEN** 无配置文件
- **THEN** 输出 prompt 模板供外部使用，报告流程继续

#### Scenario: 泄漏防护

- **WHEN** 生成日志或错误输出
- **THEN** api_key 打码；仓库任何文件不含 key
