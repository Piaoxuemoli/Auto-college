# JetBrains Mono (self-hosted)

Self-hosted fallback so HTML templates (Tier 3) render with a consistent
Linux/SSH-terminal monospace face on any host (Linux presets such as GNOME
Terminal / SSH sessions list it first).

- Source: https://github.com/JetBrains/JetBrainsMono
- Version: **2.304** (release `v2.304`, files taken from `fonts/webfonts/`)
- License: SIL Open Font License 1.1 — see `OFL.txt` (copyright The JetBrains
  Mono Project Authors)

## Files

| File | Kind | Weight |
|------|------|--------|
| `JetBrainsMono-Regular.woff2` | static | 400 |
| `JetBrainsMono-Bold.woff2` | static | 700 |
| `JetBrainsMono-Italic.woff2` | static | 400 italic |

See the "Local fonts" section in `references/html-templates.md` for the
`@font-face` snippet and font-priority rules.

## CJK note

No CJK subset is bundled (font size would dwarf the whole skill). Chinese
text keeps falling through to the platform system stack (e.g. Noto Sans CJK /
Microsoft YaHei / PingFang SC) after the monospace face.
