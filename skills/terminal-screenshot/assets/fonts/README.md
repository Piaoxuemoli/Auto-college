# Self-hosted fonts (OFL)

本地自托管字体，供 HTML 模板 @font-face 引用，消除渲染主机字体缺失导致的观感漂移。
CJK 不子集化（体积过大），中文回退走系统字体栈。

| 目录 | 家族 | 版本 | 文件 | 许可 |
|------|------|------|------|------|
| cascadia-code/ | Cascadia Code / Mono（变量字体 wght 200-700 + Italic） | v2407.24 | 4×woff2（210-219KB each） | OFL（见目录内 OFL.txt） |
| jetbrains-mono/ | JetBrains Mono Regular/Bold/Italic | v2.304 | 3×woff2（92-96KB each） | OFL（见目录内 OFL.txt） |

来源：microsoft/cascadia-code、JetBrains/JetBrainsMono 官方 release。
已知偏差：Cascadia 变量字体单文件 >100KB 目标（含全字重）；如需瘦身可用
pyftsubset 子集化（后续优化项）。SF Mono 非 OFL 不可再分发，macOS 模板走系统栈。
