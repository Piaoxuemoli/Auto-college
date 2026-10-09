# Spec Delta: latex-math-support

## ADDED Requirements

### Requirement: 数学公式

MD 成稿保留 LaTeX 源（`$...$` 行内、`$$...$$` 独立行）；docx 导出用 OMML
转换为原生公式对象；转换失败的公式保留源码文本并显式说明，不静默丢弃。

#### Scenario: 导出含公式的 docx

- **WHEN** 成稿含行内与独立公式并导出 docx
- **THEN** 公式为原生 OMML 对象，视觉与源语义一致

#### Scenario: 不支持的公式

- **WHEN** 某公式 OMML 转换失败
- **THEN** 该处保留 LaTeX 源码，交付说明列出未渲染公式
