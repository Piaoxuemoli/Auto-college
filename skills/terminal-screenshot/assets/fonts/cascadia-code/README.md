# Cascadia Code / Cascadia Mono (self-hosted)

Self-hosted fallback so HTML templates (Tier 3) render with the real Windows
Terminal font on any host, even when Cascadia is not installed locally.

- Source: https://github.com/microsoft/cascadia-code
- Version: **2407.24** (release `v2407.24`, asset `CascadiaCode-2407.24.zip`,
  extracted from the release zip's `woff2/` directory)
- License: SIL Open Font License 1.1 — see `OFL.txt` (copyright Microsoft
  Corporation, Reserved Font Name "Cascadia Code")

## Files

| File | Kind | Weight axis |
|------|------|-------------|
| `CascadiaMono.woff2` | variable font, upright | wght 200–700 (default 400) |
| `CascadiaMonoItalic.woff2` | variable font, italic | wght 200–700 |
| `CascadiaCode.woff2` | variable font, upright, programming ligatures | wght 200–700 |
| `CascadiaCodeItalic.woff2` | variable font, italic, ligatures | wght 200–700 |

Windows Terminal's default face is **Cascadia Mono** (no ligatures), so
terminal-transcript templates should list `'Cascadia Mono'` before
`'Cascadia Code'`; see the "Local fonts" section in
`references/html-templates.md` for the `@font-face` snippet.

Not carrying: Nerd Fonts (NF) and Powerline (PL) variants (about 1 MB per
file each); the NF glyph set is not needed for transcript rendering.

## CJK note

No CJK subset is bundled (font size would dwarf the whole skill). Chinese
text keeps falling through to the platform system stack (e.g. Microsoft
YaHei / PingFang SC / Noto Sans CJK) after the monospace face.
