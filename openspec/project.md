# Project Conventions — Auto-college

任何进入本仓库的 agent / 贡献者先读本文。目标："结构即方法"——不依赖
openspec CLI，靠本约定 + 纯 Markdown 即可运作规格驱动流程。

## 仓库定位

agent 中立的 skill 集合：terminal-screenshot（终端输出 → 逼真 PNG 证据截图）
与 lab-report（实验报告流程）。详见 README.md。

## 目录与流程总览

```
openspec/
├── project.md                  # 本文：仓库约定
├── specs/<capability>/spec.md  # 能力基线：当前已实现且为真的规格
└── changes/<change-id>/        # 变更提案（进行中的工作）
    ├── proposal.md             # 为什么 / 做什么 / 取舍
    ├── tasks.md                # 带验收标准的任务清单（可勾选、可验证）
    └── spec.md                 # 规格增量片段（ADDED/MODIFIED Requirements）
```

变更流程：

1. 新需求/议题 → 建 `changes/<id>/`（proposal + tasks + spec delta），
   不动 `specs/`；
2. 实现过程中逐条勾选 tasks，验收标准逐项核实后才能勾；
3. 全部完成后把 spec delta 合并进对应 `specs/<capability>/spec.md`，
   删除 change 目录（归档），并在 `docs/roadmap.md` 变更记录追加一行。

`specs/` 永远只描述"当前为真"的系统；提案期的设计不提前写入基线。
议题源头与决策记录在 `docs/roadmap.md`（T1-T7 与 Epic），`changes/` 是其执行态。

## Skill 目录规范

```
skills/<name>/
├── SKILL.md        # skill 指令（frontmatter: name / description）
├── scripts/        # 可执行脚本（Python，pathlib + file:/// URL 跨平台）
├── references/     # 文档型参考（模板、规格、校验协议）
├── assets/         # 静态素材（附许可说明，只用可再分发资产，如 CC0/OFL）
├── configs/        # 工具配置（如 freeze-base.json）
└── outputs/        # 生成物，gitignored，不入库
```

## 文档风格

- 中文为主，关键术语保留英文（tier、preset、chrome、profile、spec 等）；
  README 与 `docs/*.md` 保持现有双语节奏，不逐句翻译。
- 简洁不啰嗦：先结论后细节，能用表格不用长段落。

## 中性标识

- 示例用户名一律 `dev`；本地配置目录一律 `~/.auto-college`。
- 任何文件不得出现真实用户名 / 主机名 / 个人标识 / 凭据；提交前自查。

## 提交信息

Conventional commits：`feat:` / `fix:` / `docs:` / `chore:` / `refactor:`，
一行说清意图，正文可选。

## 与安全钩子共存

- 文件修改一律用编辑工具（Write/Edit）；Bash 内 printf/sed 重定向写文件
  会被安全钩子拦截，不要尝试绕过。
- 运行产物只写入 gitignored 的 `outputs/` 目录，不改 skill 源码目录。
