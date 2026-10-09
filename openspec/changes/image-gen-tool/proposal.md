# Proposal: image-gen-tool

- 议题：T6 图片生成 tool 可配置接入（见 `docs/roadmap.md`）
- 状态：proposed（roadmap 倾向形态 ③）

## 为什么

报告需要示意图（实验装置、流程图）时，目前只能靠文字描述或外部制图。
用户各有自己的图片生成 API（image2 类服务），需要一个统一、可配置的接入层。

## 做什么

形态 ③——配置驱动 + 优雅降级：

- `~/.auto-college/image-gen.json`：provider / base_url / model / api_key，
  OpenAI-compatible 格式优先（多数服务兼容）；
- 统一适配层 `scripts/image_gen.py`：读配置 → 调 API → 图片存
  `outputs/<exp>/assets/` → 返回路径；
- 无配置时降级：只产出结构化 prompt 模板（供 agent 平台原生 image tool
  或用户手动使用）；
- skill（lab-report 为主）需要插图时调用；缺配置或调用失败不阻断主流程。

## 取舍

- 不只做 ②（等平台原生 image tool）：能力受平台节奏限制；
- 不只做 ①（纯配置）：没配置的用户直接不可用；
- 安全红线：api_key 只存本地配置文件（gitignore 范围），模板/文档/仓库任何
  落盘物绝不出现 key；日志与错误信息打码。
