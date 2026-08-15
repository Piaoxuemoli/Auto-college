# Terminal Types & Color Schemes Reference

This catalog documents terminal types for the terminal-screenshot skill. Each entry
includes hex colors, CSS classes, CRT effects, and window chrome style.

---

## 1. Green Phosphor CRT (P1)

The iconic "hacker terminal." Used in IBM 3270, DEC VT100, early oscilloscopes.

| Property | Value |
|----------|-------|
| Background | `#0A0A0A` (slightly lifted black for glow effect) |
| Foreground | `#33FF33` |
| Bold/Bright | `#66FF66` |
| Dim | `#1A991A` |
| ANSI Black | `#000000` |
| ANSI Red | `#33FF33` (monochrome — all colors map to green variants) |
| Prompt color | `#33FF33` |
| Cursor | `#33FF33` block |

**CRT Effects CSS:**
- Scanlines: `repeating-linear-gradient(0deg, rgba(0,0,0,0.15) 0px, rgba(0,0,0,0.15) 1px, transparent 1px, transparent 3px)`
- Text glow: `text-shadow: 0 0 3px rgba(51,255,51,0.5), 0 0 8px rgba(51,255,51,0.2)`
- Vignette: `radial-gradient(ellipse at center, transparent 60%, rgba(0,0,0,0.4) 100%)`
- Screen curvature: subtle `border-radius: 8px` on the screen element

**Window Chrome:** CRT monitor bezel — dark gray frame around the screen, with a small
label text below (e.g., "IBM 3270 TERMINAL").

**CSS classes:** `terminal-crt-green`, `crt-scanlines`, `crt-glow`, `crt-vignette`

---

## 2. Amber Phosphor CRT (P3)

Warmer, retro feel. Used in DEC VT220, ADM-3A terminals.

| Property | Value |
|----------|-------|
| Background | `#0A0A0A` |
| Foreground | `#FFB000` |
| Bold/Bright | `#FFCC33` |
| Dim | `#996600` |
| Prompt color | `#FFB000` |
| Cursor | `#FFB000` block |

**CRT Effects CSS:** Same structure as green phosphor, with amber colors:
- Text glow: `text-shadow: 0 0 3px rgba(255,176,0,0.5), 0 0 8px rgba(255,176,0,0.2)`

**Window Chrome:** Same CRT monitor bezel, label "ADM-3A TERMINAL" or "VT220".

**CSS classes:** `terminal-crt-amber`, `crt-scanlines`, `crt-glow-amber`, `crt-vignette`

---

## 3. White Phosphor CRT (P4)

Later-generation monochrome CRT. Clean, high-contrast look.

| Property | Value |
|----------|-------|
| Background | `#0A0A0A` |
| Foreground | `#E0E0E0` |
| Bold/Bright | `#FFFFFF` |
| Dim | `#888888` |
| Prompt color | `#E0E0E0` |
| Cursor | `#FFFFFF` block |

**CRT Effects CSS:**
- Text glow: `text-shadow: 0 0 2px rgba(224,224,224,0.4), 0 0 6px rgba(224,224,224,0.15)`
- Scanlines: same pattern, slightly lighter

**CSS classes:** `terminal-crt-white`, `crt-scanlines`, `crt-glow-white`, `crt-vignette`

---

## 4. Remote Linux SSH Server Session

This is the default for experiment reports, lab reports, GPU output, CI logs, and anything
that looks like real work on a remote machine. A server does not have its own special GUI
in the screenshot; it appears inside a local terminal window through SSH.

| Property | Value |
|----------|-------|
| Background | `#0B1020` or `#111827` for a modern ops terminal |
| Foreground | `#D1D5DB` |
| Prompt user | `#7DD3FC` cyan |
| Prompt host | `#A78BFA` violet |
| Prompt path | `#FBBF24` amber |
| Root prompt | `#F87171` red, ending in `#` |
| Command | `#F9FAFB` |
| Output | `#D1D5DB` |
| Dim metadata | `#6B7280` |
| Success | `#34D399` |
| Warning | `#FBBF24` |
| Error/Stderr | `#F87171` |

**Prompt grammar:**
- Normal user: `ubuntu@gpu-a100-01:~/train$`
- Root shell: `root@prod-api-02:/var/log#`
- Conda/env prefix: `(base) ubuntu@gpu-a100-01:~/project$`
- SSH entry should look like:
  `PS C:\Users\dev> ssh ubuntu@gpu-a100-01`
  then remote prompt begins on following lines.

**Window Chrome:** Use the local host terminal chrome if known. If the user is on Windows,
use Windows Terminal with a tab title like `ubuntu@gpu-a100-01`. If the user is on macOS,
use Terminal.app with a centered title like `ubuntu@gpu-a100-01 — ssh — 100x30`. If unknown,
use a neutral GNOME-style frame.

**CSS classes:** `terminal-ssh-server`, `ssh-titlebar`, `ssh-prompt`, `user`, `host`, `path`,
`env`, `ok`, `warn`, `err`, `dim`

---

## 5. Windows Terminal PowerShell 7

Use for local Windows commands and PowerShell transcripts. This preset should feel like
Windows 11 Terminal running PowerShell 7, not a Linux terminal with a `PS>` string pasted in.

| Property | Value |
|----------|-------|
| Background | `#0C0C0C` |
| Foreground | `#CCCCCC` |
| Tab/titlebar | `#202020` / active tab `#0C0C0C` |
| Accent | `#0078D4` or PowerShell blue `#3B78FF` |
| Prompt | `#F2F2F2` |
| Path in prompt | `#F9F1A5` |
| Command token | `#F9F1A5` |
| Parameter token | `#9CDCFE` |
| String token | `#CE9178` |
| Number token | `#B5CEA8` |
| Comment token | `#6A9955` |
| Error/Stderr | `#F14C4C` |

**Prompt grammar:**
- `PS C:\Users\dev\Desktop\projects>`
- `PS C:\Users\dev\Desktop\projects [master ≡]>` when git context is useful
- Continuation prompt: `>>`

**Window Chrome:** Windows Terminal tab strip with a PowerShell icon/title, plus `+`, dropdown
chevron, and Windows caption buttons. Use Cascadia Mono first.

**CSS classes:** `terminal-windows-pwsh`, `win-titlebar`, `win-tab`, `ps-command`,
`ps-param`, `ps-string`, `ps-number`, `ps-comment`, `cursor`

---

## 6. macOS Terminal zsh

Use for local macOS development commands. The screenshot should look like Terminal.app or
iTerm-style zsh, with traffic-light controls and a prompt ending in `%`.

| Property | Value |
|----------|-------|
| Background | `#1D1F21` |
| Foreground | `#C5C8C6` |
| Titlebar | `#2D2D2D` |
| Prompt user/host | `#81A2BE` |
| Prompt path | `#B5BD68` |
| Command | `#FFFFFF` |
| Output | `#C5C8C6` |
| Dim metadata | `#7C7C7C` |
| Error/Stderr | `#CC6666` |

**Prompt grammar:**
- `dev@MacBook-Pro projects %`
- `MacBook-Pro:projects dev$` only when the content clearly comes from older bash
- For Homebrew, Xcode, and launchctl screenshots, prefer zsh `%`.

**Window Chrome:** macOS traffic lights at left, centered title text, subtle 1px separator,
Menlo/SF Mono font stack.

**CSS classes:** `terminal-macos-zsh`, `macos-titlebar`, `mac-prompt`, `mac-userhost`,
`mac-path`, `cursor`

---

## 7. Modern Dark Terminal (GNOME / generic Linux)

Clean, professional. The default for most server screenshots.

| Property | Value |
|----------|-------|
| Background | `#1E1E1E` |
| Foreground | `#D4D4D4` |
| Bold/Bright | `#FFFFFF` |
| Prompt (user@host) | `#569CD6` (blue) |
| Prompt ($) | `#D4D4D4` |
| Command | `#D4D4D4` |
| Output | `#CCCCCC` |
| Error/Stderr | `#F44747` (red) |
| ANSI Black | `#000000` |
| ANSI Red | `#CD3131` |
| ANSI Green | `#0DBC79` |
| ANSI Yellow | `#E5E510` |
| ANSI Blue | `#2472C8` |
| ANSI Magenta | `#BC3FBC` |
| ANSI Cyan | `#11A8CD` |
| ANSI White | `#E5E5E5` |
| ANSI Bright Black | `#666666` |
| ANSI Bright Red | `#F14C4C` |
| ANSI Bright Green | `#23D18B` |
| ANSI Bright Yellow | `#F5F543` |
| ANSI Bright Blue | `#3B8EEA` |
| ANSI Bright Magenta | `#D670D6` |
| ANSI Bright Cyan | `#29B8DB` |
| ANSI Bright White | `#FFFFFF` |

**Effects:** None (clean modern rendering).

**Window Chrome:** GNOME-style — dark title bar with subtle border, no traffic light buttons.

**CSS classes:** `terminal-modern-dark`, `terminal-gnome`

---

## 8. macOS Terminal Pro

Apple's default Terminal.app dark theme.

| Property | Value |
|----------|-------|
| Background | `#1E1E1E` |
| Foreground | `#D4D4D4` |
| Selection | `#264F78` |
| ANSI Black | `#000000` |
| ANSI Red | `#C91B00` |
| ANSI Green | `#00C600` |
| ANSI Yellow | `#C7C400` |
| ANSI Blue | `#0225C7` |
| ANSI Magenta | `#CA30C7` |
| ANSI Cyan | `#00C5C7` |
| ANSI White | `#C7C7C7` |
| ANSI Bright Black | `#676767` |
| ANSI Bright Red | `#FF6D67` |
| ANSI Bright Green | `#5FF967` |
| ANSI Bright Yellow | `#FEFB67` |
| ANSI Bright Blue | `#6871FF` |
| ANSI Bright Magenta | `#FF76FF` |
| ANSI Bright Cyan | `#5FFDCF` |
| ANSI Bright White | `#FEFB67` |

**Effects:** None (clean modern rendering).

**Window Chrome:** macOS title bar with red/yellow/green traffic light buttons on the left,
title text centered ("username — -zsh — 80x24"), dark background `#323233`.

**CSS classes:** `terminal-macos-pro`, `macos-titlebar`

---

## 9. Windows Terminal Campbell

Microsoft's default Windows Terminal dark theme.

| Property | Value |
|----------|-------|
| Background | `#0C0C0C` |
| Foreground | `#CCCCCC` |
| Selection | `#264F78` |
| ANSI Black | `#0C0C0C` |
| ANSI Red | `#C50F1F` |
| ANSI Green | `#13A10E` |
| ANSI Yellow | `#C19C00` |
| ANSI Blue | `#0037DA` |
| ANSI Magenta | `#881798` |
| ANSI Cyan | `#3A96DD` |
| ANSI White | `#CCCCCC` |
| ANSI Bright Black | `#767676` |
| ANSI Bright Red | `#E74856` |
| ANSI Bright Green | `#16C60C` |
| ANSI Bright Yellow | `#F9F1A5` |
| ANSI Bright Blue | `#3B78FF` |
| ANSI Bright Magenta | `#B4009E` |
| ANSI Bright Cyan | `#61D6D6` |
| ANSI Bright White | `#F2F2F2` |

**Effects:** None (clean modern rendering).

**Window Chrome:** Windows Terminal style — dark title bar with a tab ("PowerShell" or "bash"),
minimize/maximize/close buttons on the right. Tab has a colored underline accent.

**CSS classes:** `terminal-windows-campbell`, `win-titlebar`, `win-tab`

---

## 10. Solarized Dark

Ethan Schoonover's carefully balanced, eye-friendly scheme.

| Property | Value |
|----------|-------|
| Background | `#002B36` |
| Foreground | `#839496` |
| Bold | `#93A1A1` |
| ANSI Red | `#DC322F` |
| ANSI Green | `#859900` |
| ANSI Yellow | `#B58900` |
| ANSI Blue | `#268BD2` |
| ANSI Magenta | `#D33682` |
| ANSI Cyan | `#2AA198` |

**Effects:** None.

**Window Chrome:** Usually macOS or GNOME frame.

**CSS classes:** `terminal-solarized-dark`

---

## 11. xterm (Classic Light)

Original X11 terminal — white background, black text. Useful for "clean print" screenshots.

| Property | Value |
|----------|-------|
| Background | `#FFFFFF` |
| Foreground | `#000000` |
| Prompt | `#000000` |

**Effects:** None.

**Window Chrome:** Minimal X11 window frame or none.

**CSS classes:** `terminal-xterm-light`

---

## Auto-Detection Heuristics

When the user does not explicitly specify a terminal type, apply these rules in order:

```
1. Content contains an explicit PowerShell prompt (`PS C:\...>`, `PS /...>`), PowerShell
   cmdlets (`Get-ChildItem`, `Set-ExecutionPolicy`, `Invoke-WebRequest`), or Windows paths
   with PowerShell syntax
   → Windows Terminal PowerShell 7

2. Content contains macOS commands (`brew`, `xcodebuild`, `launchctl`, `pbcopy`,
   `~/Library`) or a zsh prompt ending in `%`
   → macOS Terminal zsh

3. Content contains SSH, `user@host:path$`, `sudo`, `systemctl`, `apt`, `journalctl`,
   CUDA/GPU keywords (`nvidia-smi`, `nvcc`, `torchrun`, `deepspeed`, `Tesla`, `A100`)
   → Remote Linux SSH Server Session

4. Content contains Windows `cmd.exe` commands (`dir`, `ipconfig`, `netstat`, `chkdsk`)
   without PowerShell syntax
   → Windows Terminal Campbell with cmd tab title

5. Content is a simple "ls -la", "cat file", or small bash output
   → If retro/hacker context: Green Phosphor CRT
   → Otherwise: Remote Linux SSH Server Session for reports, Modern Dark Terminal for generic docs

6. User is writing an experiment report, technical documentation, or lab report
   → Remote Linux SSH Server Session unless the prompt clearly indicates Windows/macOS local work

7. Explicit user request overrides all heuristics
```

## Font Stack

Use a platform-specific stack instead of one universal fallback:

- Windows Terminal / PowerShell: `'Cascadia Mono', 'Cascadia Code', 'Consolas', 'Microsoft YaHei UI', monospace`
- macOS Terminal: `'SF Mono', 'Menlo', 'Monaco', 'PingFang SC', monospace`
- Linux / SSH: `'JetBrains Mono', 'Ubuntu Mono', 'DejaVu Sans Mono', 'Consolas', 'Microsoft YaHei', monospace`
- CRT presets: `'IBM Plex Mono', 'Consolas', 'Courier New', monospace`

Use CJK fallback only after the terminal font so Chinese output renders while Latin command
text keeps the right terminal proportions.
