# HTML Templates for Terminal Screenshots

Production-ready HTML/CSS templates. Every template includes scrollbar suppression
and realistic terminal proportions (80-column width, tight line-height).

---

## Mandatory Base CSS

Every template MUST include this at the top of its `<style>` block:

```css
html, body {
  overflow: hidden;           /* never show scrollbars */
  margin: 0; padding: 0;
}
::-webkit-scrollbar { display: none; }
* { scrollbar-width: none; -ms-overflow-style: none; }
```

---

## High-Fidelity Presets

Use these presets before the older generic templates. They encode the real visual cues
that make PowerShell, macOS zsh, and SSH server sessions recognizable: native chrome,
platform font stack, prompt grammar, token colors, tab/title text, and cursor treatment.

---

## Template P1: Windows Terminal PowerShell 7

Best for local Windows and PowerShell transcripts.

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head><meta charset="UTF-8">
<style>
  html, body { overflow: hidden; margin: 0; padding: 0; }
  html { background: #202020; }
  ::-webkit-scrollbar { display: none; }
  * { scrollbar-width: none; -ms-overflow-style: none; box-sizing: border-box; }

  body {
    background: #202020; margin: 0; padding: 28px 22px;
    font-family: 'Cascadia Mono','Cascadia Code','Consolas','Microsoft YaHei UI',monospace;
  }
  .window {
    width: 940px; margin: 0 auto; overflow: hidden; border-radius: 8px;
    background: #0c0c0c; border: 1px solid #303030;
    box-shadow: 0 18px 50px rgba(0,0,0,0.55);
  }
  .titlebar {
    height: 38px; background: #202020; display: flex; align-items: center;
    border-bottom: 1px solid #303030; user-select: none;
  }
  .tabs { display: flex; align-items: center; flex: 1; min-width: 0; height: 100%; }
  .tab {
    height: 32px; min-width: 168px; padding: 0 14px; margin-left: 8px; align-self: flex-end;
    background: #0c0c0c; color: #f2f2f2; display: flex; align-items: center; gap: 9px;
    border: 1px solid #303030; border-bottom: 0; border-radius: 6px 6px 0 0;
    font: 12px/1 'Segoe UI','Microsoft YaHei UI',sans-serif; position: relative;
  }
  .tab::after {
    content: ''; position: absolute; left: 10px; right: 10px; bottom: 0;
    height: 2px; background: #0078d4; border-radius: 2px 2px 0 0;
  }
  .ps-icon {
    width: 16px; height: 16px; border-radius: 3px; background: #012456;
    color: #f2f2f2; display: inline-flex; align-items: center; justify-content: center;
    font: 700 10px/1 'Segoe UI',sans-serif;
  }
  .tab-action {
    width: 36px; height: 34px; margin-left: 0; align-self: center;
    display: flex; align-items: center; justify-content: center;
    border-radius: 4px; position: relative;
  }
  .tab-action:hover { background: rgba(255,255,255,0.08); }
  .new-tab::before, .new-tab::after {
    content: ''; position: absolute; background: #c8c8c8; border-radius: 1px;
  }
  .new-tab::before { width: 12px; height: 1.5px; }
  .new-tab::after { width: 1.5px; height: 12px; }
  .chevron::before {
    content: ''; width: 7px; height: 7px; border-right: 1.6px solid #c8c8c8;
    border-bottom: 1.6px solid #c8c8c8; transform: translateY(-2px) rotate(45deg);
  }
  .caption-buttons { display: flex; align-self: stretch; margin-left: auto; }
  .caption-btn {
    width: 46px; height: 38px; display: flex; align-items: center; justify-content: center;
    position: relative;
  }
  .caption-btn:hover { background: rgba(255,255,255,0.08); }
  .caption-btn.close:hover { background: #c42b1c; }
  .caption-btn::before, .caption-btn::after {
    content: ''; position: absolute; box-sizing: border-box;
  }
  .caption-btn.minimize::before {
    width: 10px; height: 1.2px; background: #c8c8c8;
  }
  .caption-btn.maximize::before {
    width: 10px; height: 10px; border: 1.3px solid #c8c8c8;
  }
  .caption-btn.close::before, .caption-btn.close::after {
    width: 12px; height: 1.3px; background: #d8d8d8;
  }
  .caption-btn.close::before { transform: rotate(45deg); }
  .caption-btn.close::after { transform: rotate(-45deg); }
  .body {
    padding: 15px 18px 17px; min-height: 120px;
    background: #0c0c0c; color: #cccccc; white-space: pre-wrap;
    font-size: 13.5px; line-height: 1.42; letter-spacing: 0;
  }
  .prompt { color: #f2f2f2; }
  .ps-path { color: #f9f1a5; }
  .ps-command { color: #f9f1a5; }
  .ps-param { color: #9cdcfe; }
  .ps-string { color: #ce9178; }
  .ps-number { color: #b5cea8; }
  .ps-comment { color: #6a9955; }
  .output { color: #cccccc; }
  .dim { color: #767676; }
  .stderr, .err { color: #f14c4c; }
  .ok { color: #16c60c; }
  .cursor {
    display: inline-block; width: 7px; height: 15px; margin-left: 1px;
    background: #cccccc; vertical-align: -2px;
  }
</style></head>
<body>
<div class="window">
  <div class="titlebar">
    <div class="tabs">
      <div class="tab"><span class="ps-icon">&gt;_</span><span>PowerShell</span></div>
      <div class="tab-action new-tab" aria-label="New tab"></div>
      <div class="tab-action chevron" aria-label="Tab menu"></div>
    </div>
    <div class="caption-buttons">
      <span class="caption-btn minimize" aria-label="Minimize"></span>
      <span class="caption-btn maximize" aria-label="Maximize"></span>
      <span class="caption-btn close" aria-label="Close"></span>
    </div>
  </div>
  <div class="body">
<span class="prompt">PS <span class="ps-path">C:\Users\qoobee\Desktop\Qoobee-skills</span>&gt;</span> <span class="ps-command">Get-ChildItem</span> <span class="ps-param">-Force</span>
<span class="output">    Directory: C:\Users\qoobee\Desktop\Qoobee-skills

Mode                 LastWriteTime         Length Name
----                 -------------         ------ ----
d----           4/30/2026  10:42 AM                terminal-screenshot
-a---           4/30/2026  10:10 AM           1420 README.md</span>
<span class="prompt">PS <span class="ps-path">C:\Users\qoobee\Desktop\Qoobee-skills</span>&gt;</span><span class="cursor"></span>
  </div>
</div>
</body></html>
```

Formatting notes:
- Keep PowerShell prompts as `PS <path>>`; do not convert them to `$`.
- Syntax-highlight cmdlets/commands, parameters, strings, numbers, and comments.
- Use Windows date spacing and `Directory:` layout for `Get-ChildItem` output.

---

## Template M1: macOS Terminal zsh

Best for local macOS development commands.

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head><meta charset="UTF-8">
<style>
  html, body { overflow: hidden; margin: 0; padding: 0; }
  html { background: #2b2b2b; }
  ::-webkit-scrollbar { display: none; }
  * { scrollbar-width: none; -ms-overflow-style: none; box-sizing: border-box; }

  body {
    background: #2b2b2b; margin: 0; padding: 30px 22px;
    font-family: 'SF Mono','Menlo','Monaco','PingFang SC',monospace;
  }
  .window {
    width: 860px; margin: 0 auto; overflow: hidden; border-radius: 10px;
    background: #1d1f21; box-shadow: 0 20px 52px rgba(0,0,0,0.48);
    border: 1px solid rgba(255,255,255,0.08);
  }
  .titlebar {
    height: 34px; background: linear-gradient(#3a3a3a, #2d2d2d);
    display: grid; grid-template-columns: 86px 1fr 86px; align-items: center;
    border-bottom: 1px solid rgba(0,0,0,0.55);
  }
  .traffic { display: flex; gap: 8px; padding-left: 13px; }
  .dot { width: 12px; height: 12px; border-radius: 50%; box-shadow: inset 0 0 0 1px rgba(0,0,0,0.18); }
  .red { background: #ff5f57; } .yellow { background: #febc2e; } .green { background: #28c840; }
  .title {
    color: #b7b7b7; text-align: center; font: 12px/1 -apple-system,'SF Pro Text','PingFang SC',sans-serif;
    letter-spacing: -0.01em;
  }
  .body {
    padding: 15px 17px 18px; min-height: 126px;
    color: #c5c8c6; background: #1d1f21; white-space: pre-wrap;
    font-size: 13px; line-height: 1.45; letter-spacing: -0.01em;
  }
  .prompt { color: #c5c8c6; }
  .mac-userhost { color: #81a2be; }
  .mac-path { color: #b5bd68; }
  .cmd { color: #ffffff; }
  .output { color: #c5c8c6; }
  .dim { color: #7c7c7c; }
  .stderr, .err { color: #cc6666; }
  .ok { color: #b5bd68; }
  .warn { color: #f0c674; }
  .cursor {
    display: inline-block; width: 7px; height: 14px; margin-left: 1px;
    background: #c5c8c6; vertical-align: -2px;
  }
</style></head>
<body>
<div class="window">
  <div class="titlebar">
    <div class="traffic"><span class="dot red"></span><span class="dot yellow"></span><span class="dot green"></span></div>
    <div class="title">qoobee — zsh — 100x30</div>
    <div></div>
  </div>
  <div class="body">
<span class="prompt"><span class="mac-userhost">qoobee@MacBook-Pro</span> <span class="mac-path">Qoobee-skills</span> %</span> <span class="cmd">brew services list</span>
<span class="output">Name          Status  User   File
mongodb       none
redis         started qoobee ~/Library/LaunchAgents/homebrew.mxcl.redis.plist</span>
<span class="prompt"><span class="mac-userhost">qoobee@MacBook-Pro</span> <span class="mac-path">Qoobee-skills</span> %</span><span class="cursor"></span>
  </div>
</div>
</body></html>
```

Formatting notes:
- Prefer `%` for zsh. Use `$` only for older bash transcripts.
- macOS paths often use `~/Library`, `/opt/homebrew`, `/Applications`, and `MacBook-Pro`.
- Keep traffic-light buttons muted and title text centered; oversized controls make it look fake.

---

## Template S1: Remote Linux SSH Server Session

Best for lab reports, GPU/ML output, deployment logs, and remote Linux commands. It uses
a local terminal frame around a remote prompt.

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head><meta charset="UTF-8">
<style>
  html, body { overflow: hidden; margin: 0; padding: 0; }
  html { background: #1f2937; }
  ::-webkit-scrollbar { display: none; }
  * { scrollbar-width: none; -ms-overflow-style: none; box-sizing: border-box; }

  body {
    background: #1f2937; margin: 0; padding: 28px 22px;
    font-family: 'JetBrains Mono','Ubuntu Mono','DejaVu Sans Mono','Consolas','Microsoft YaHei',monospace;
  }
  .window {
    width: 960px; margin: 0 auto; overflow: hidden; border-radius: 9px;
    background: #0b1020; border: 1px solid rgba(148,163,184,0.18);
    box-shadow: 0 20px 56px rgba(0,0,0,0.5);
  }
  .titlebar {
    height: 36px; background: #111827; display: flex; align-items: center;
    border-bottom: 1px solid rgba(148,163,184,0.16); padding: 0 12px;
  }
  .title-left { display: flex; align-items: center; gap: 8px; color: #9ca3af; font: 12px/1 'Segoe UI','Ubuntu',sans-serif; }
  .status-dot { width: 8px; height: 8px; border-radius: 50%; background: #34d399; box-shadow: 0 0 8px rgba(52,211,153,0.55); }
  .title { flex: 1; text-align: center; color: #9ca3af; font: 12px/1 'Segoe UI','Ubuntu',sans-serif; }
  .body {
    padding: 16px 18px 19px; min-height: 130px; background: #0b1020;
    color: #d1d5db; white-space: pre-wrap; font-size: 13.5px; line-height: 1.42;
  }
  .prompt { color: #d1d5db; }
  .env { color: #34d399; }
  .user { color: #7dd3fc; }
  .host { color: #a78bfa; }
  .path { color: #fbbf24; }
  .root { color: #f87171; }
  .cmd { color: #f9fafb; }
  .output { color: #d1d5db; }
  .dim { color: #6b7280; }
  .ok { color: #34d399; }
  .warn { color: #fbbf24; }
  .stderr, .err { color: #f87171; }
  .ansi-blue { color: #60a5fa; }
  .ansi-cyan { color: #22d3ee; }
  .cursor {
    display: inline-block; width: 7px; height: 15px; margin-left: 1px;
    background: #d1d5db; vertical-align: -2px;
  }
</style></head>
<body>
<div class="window">
  <div class="titlebar">
    <div class="title-left"><span class="status-dot"></span><span>ssh</span></div>
    <div class="title">ubuntu@gpu-a100-01: ~/train</div>
    <div style="width:52px"></div>
  </div>
  <div class="body">
<span class="prompt"><span class="env">(base)</span> <span class="user">ubuntu</span>@<span class="host">gpu-a100-01</span>:<span class="path">~/train</span>$</span> <span class="cmd">nvidia-smi</span>
<span class="output">Thu Apr 30 10:48:21 2026
+-----------------------------------------------------------------------------+
| NVIDIA-SMI 550.54.15    Driver Version: 550.54.15    CUDA Version: 12.4     |
| GPU  Name        Persistence-M| Bus-Id        Disp.A | Volatile Uncorr. ECC |
|   0  NVIDIA A100-SXM4-40GB    On | 00000000:81:00.0 Off |                    0 |
+-----------------------------------------------------------------------------+</span>
<span class="prompt"><span class="env">(base)</span> <span class="user">ubuntu</span>@<span class="host">gpu-a100-01</span>:<span class="path">~/train</span>$</span><span class="cursor"></span>
  </div>
</div>
</body></html>
```

Formatting notes:
- Preserve ASCII tables exactly; `nvidia-smi`, `df -h`, `top`, `kubectl`, and compiler output
  lose realism if whitespace is reflowed.
- Do not use macOS or Windows prompt grammar for remote Linux. The prompt should expose
  `user@host:path$` or `root@host:path#`.
- If the screenshot includes the initial SSH command from Windows/macOS, show one local
  prompt first, then switch to the remote prompt after the connection banner.

---

## Template A: Modern Dark Terminal with GNOME Window Frame

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head><meta charset="UTF-8">
<style>
  html, body { overflow: hidden; margin: 0; padding: 0; }
  html { background: #2a2a2a; }
  ::-webkit-scrollbar { display: none; }
  * { scrollbar-width: none; -ms-overflow-style: none; }

  body {
    background: #2a2a2a; margin: 0; padding: 28px 20px;
    font-family: 'Consolas','Courier New','Microsoft YaHei',monospace;
  }
  .window {
    background: #1e1e1e; border-radius: 8px; overflow: hidden;
    box-shadow: 0 6px 24px rgba(0,0,0,0.5); border: 1px solid #3c3c3c;
    width: 740px; margin: 0 auto;
  }
  .titlebar {
    background: #2d2d2d; padding: 7px 14px; display: flex; align-items: center;
    border-bottom: 1px solid #3c3c3c;
  }
  .titlebar-text {
    color: #999; font-size: 11px; text-align: center; flex: 1;
    font-family: -apple-system,'Segoe UI','Microsoft YaHei',sans-serif;
  }
  .body {
    padding: 14px 18px; font-size: 14px; line-height: 1.4;
    white-space: pre-wrap; color: #d4d4d4;
  }
  .prompt { color: #569cd6; }
  .cmd { color: #d4d4d4; }
  .output { color: #cccccc; }
  .stderr { color: #f44747; }
  .highlight { color: #569cd6; font-weight: bold; }
</style></head>
<body>
<div class="window">
  <div class="titlebar">
    <span class="titlebar-text">a2023080901018@server:~</span>
  </div>
  <div class="body">
    <!-- CONTENT HERE -->
  </div>
</div>
</body></html>
```

---

## Template B: macOS Terminal Pro

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head><meta charset="UTF-8">
<style>
  html, body { overflow: hidden; margin: 0; padding: 0; }
  html { background: #2a2a2a; }
  ::-webkit-scrollbar { display: none; }
  * { scrollbar-width: none; -ms-overflow-style: none; }

  body {
    background: #2a2a2a; margin: 0; padding: 28px 20px;
    font-family: 'Consolas','Courier New','Microsoft YaHei',monospace;
  }
  .window {
    background: #1e1e1e; border-radius: 8px; overflow: hidden;
    box-shadow: 0 6px 24px rgba(0,0,0,0.5);
    width: 740px; margin: 0 auto;
  }
  .titlebar {
    background: #323233; padding: 9px 14px; display: flex; align-items: center;
    gap: 8px;
  }
  .dot { width: 12px; height: 12px; border-radius: 50%; flex-shrink: 0; }
  .dot.red    { background: #ff5f57; }
  .dot.yellow { background: #febc2e; }
  .dot.green  { background: #28c840; }
  .titlebar-text {
    flex: 1; text-align: center; color: #999; font-size: 11px;
    font-family: -apple-system,'SF Pro Text','Microsoft YaHei',sans-serif;
  }
  .body {
    padding: 14px 18px; font-size: 14px; line-height: 1.4;
    white-space: pre-wrap; color: #d4d4d4;
  }
  .prompt { color: #569cd6; }
  .cmd { color: #d4d4d4; }
  .output { color: #cccccc; }
  .stderr { color: #f44747; }
  .highlight { color: #569cd6; font-weight: bold; }
</style></head>
<body>
<div class="window">
  <div class="titlebar">
    <span class="dot red"></span>
    <span class="dot yellow"></span>
    <span class="dot green"></span>
    <span class="titlebar-text">username — -zsh — 80x24</span>
  </div>
  <div class="body">
    <!-- CONTENT HERE -->
  </div>
</div>
</body></html>
```

---

## Template C: Windows Terminal (optimized)

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head><meta charset="UTF-8">
<style>
  html, body { overflow: hidden; margin: 0; padding: 0; }
  html { background: #2a2a2a; }
  ::-webkit-scrollbar { display: none; }
  * { scrollbar-width: none; -ms-overflow-style: none; }

  body {
    background: #2a2a2a; margin: 0; padding: 28px 20px;
    font-family: 'Consolas','Courier New','Microsoft YaHei',monospace;
  }
  .window {
    background: #0c0c0c; border-radius: 8px; overflow: hidden;
    box-shadow: 0 6px 24px rgba(0,0,0,0.55);
    border: 1px solid #3c3c3c;
    width: 740px; margin: 0 auto;
  }
  .titlebar {
    background: #202020; display: flex; align-items: stretch;
    border-bottom: 1px solid #3c3c3c; height: 32px;
  }
  .tabs-area { display: flex; align-items: stretch; flex: 1; }
  .tab {
    background: #0c0c0c; color: #cccccc; padding: 0 14px; font-size: 12px;
    display: flex; align-items: center; border-right: 1px solid #3c3c3c;
    border-bottom: 1px solid #0c0c0c; gap: 6px;
    font-family: 'Segoe UI',-apple-system,'Microsoft YaHei',sans-serif;
  }
  .tab-active-line { background: #16c60c; height: 2px; align-self: flex-end; }
  .caption-buttons { display: flex; align-items: stretch; flex-shrink: 0; }
  .caption-btn {
    width: 46px; display: flex; align-items: center; justify-content: center;
    color: #888; font-size: 10px; font-family: 'Segoe UI',sans-serif;
  }
  .body {
    padding: 14px 18px; font-size: 14px; line-height: 1.4;
    white-space: pre-wrap; background: #0c0c0c; color: #cccccc;
  }
  .prompt { color: #569cd6; }
  .cmd { color: #cccccc; }
  .output { color: #aaaaaa; }
  .stderr { color: #f44747; }
  .highlight { color: #569cd6; font-weight: bold; }
</style></head>
<body>
<div class="window">
  <div class="titlebar">
    <div class="tabs-area">
      <div class="tab">
        <span>&gt;_</span><span>PowerShell</span>
      </div>
    </div>
    <div class="caption-buttons">
      <span class="caption-btn minimize" aria-label="Minimize"></span>
      <span class="caption-btn maximize" aria-label="Maximize"></span>
      <span class="caption-btn close" aria-label="Close"></span>
    </div>
  </div>
  <div class="body">
    <!-- CONTENT HERE -->
  </div>
</div>
</body></html>
```

---

## Template D: Green Phosphor CRT with Monitor Bezel

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head><meta charset="UTF-8">
<style>
  html, body { overflow: hidden; margin: 0; padding: 0; }
  html { background: #2a2a2a; }
  ::-webkit-scrollbar { display: none; }
  * { scrollbar-width: none; -ms-overflow-style: none; }

  body {
    background: #2a2a2a; margin: 0; padding: 28px 20px;
    font-family: 'Consolas','Courier New','Microsoft YaHei',monospace;
  }
  .monitor {
    background: #3a3a3a; padding: 22px 22px 32px 22px; border-radius: 10px;
    box-shadow: 0 8px 32px rgba(0,0,0,0.5); display: inline-block;
  }
  .screen {
    background: #0a0a0a; padding: 18px 22px; border-radius: 6px;
    position: relative; overflow: hidden;
  }
  .screen::before {
    content: '';
    position: absolute; top:0; left:0; right:0; bottom:0;
    background: repeating-linear-gradient(
      0deg,
      rgba(0,0,0,0.12) 0px, rgba(0,0,0,0.12) 1px,
      transparent 1px, transparent 3px
    );
    pointer-events: none; z-index: 1;
  }
  .screen::after {
    content: '';
    position: absolute; top:0; left:0; right:0; bottom:0;
    background: radial-gradient(ellipse at center, transparent 55%, rgba(0,0,0,0.5) 100%);
    pointer-events: none; z-index: 2;
  }
  .content {
    position: relative; z-index: 0; font-size: 14px; line-height: 1.4;
    white-space: pre-wrap; color: #33ff33;
    text-shadow: 0 0 2px rgba(51,255,51,0.5), 0 0 6px rgba(51,255,51,0.15);
  }
  .monitor-label {
    text-align: center; color: #888; font-size: 9px; margin-top: 10px;
    letter-spacing: 2px;
    font-family: -apple-system,'Segoe UI','Microsoft YaHei',sans-serif;
  }
  .content .prompt { color: #33ff33; }
  .content .cmd { color: #66ff66; }
  .content .output { color: #33ff33; }
  .content .stderr { color: #ff5555; }
</style></head>
<body>
<div class="monitor">
  <div class="screen">
    <div class="content">
      <!-- CONTENT HERE -->
    </div>
  </div>
  <div class="monitor-label">IBM 3270 TERMINAL</div>
</div>
</body></html>
```

---

## Template E: Amber Phosphor CRT

Same structure as Template D with amber colors:

```css
.content { color: #ffb000;
  text-shadow: 0 0 2px rgba(255,176,0,0.5), 0 0 6px rgba(255,176,0,0.15); }
.content .prompt { color: #ffb000; }
.content .cmd { color: #ffcc33; }
.content .output { color: #ffb000; }
.content .stderr { color: #ff4444; }
```

Monitor label: `DEC VT220`

---

## Template F: No Window Frame (inline snippet)

For small outputs (<40 lines) — no window chrome, just the terminal content.

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head><meta charset="UTF-8">
<style>
  html, body { overflow: hidden; margin: 0; padding: 0; }
  html { background: #2a2a2a; }
  ::-webkit-scrollbar { display: none; }
  * { scrollbar-width: none; -ms-overflow-style: none; }

  body {
    background: #2a2a2a; margin: 0; padding: 28px 20px;
    font-family: 'Consolas','Courier New','Microsoft YaHei',monospace;
  }
  .terminal {
    background: #1e1e1e; color: #d4d4d4; padding: 16px 20px; border-radius: 6px;
    font-size: 14px; line-height: 1.4; white-space: pre-wrap;
    display: inline-block;
  }
  .prompt { color: #569cd6; }
  .cmd { color: #d4d4d4; }
  .output { color: #cccccc; }
  .stderr { color: #f44747; }
  .highlight { color: #569cd6; font-weight: bold; }
</style></head>
<body>
<div class="terminal">
<!-- CONTENT HERE -->
</div>
</body></html>
```

---

## Content Formatting

| Class | Usage | Example |
|-------|-------|---------|
| `.prompt` | Shell prompt (`$`, `>`, `#`) | `<span class="prompt">$ </span>` |
| `.cmd` | User-typed command | `<span class="cmd">nvprof ./a.out</span>` |
| `.output` | Standard output | `<span class="output">PASSED</span>` |
| `.stderr` | Error/warning output | `<span class="stderr">warning: ...</span>` |
| `.highlight` | Titles, key values | `<span class="highlight">=== Step 1 ===</span>` |

For multi-command sessions, separate blocks with a blank line in the pre-formatted text.
For ASCII tables (nvidia-smi, nvprof), wrap the entire table in `.output`, preserving
exact whitespace and monospace alignment.

Use shell-specific token classes when available:

| Preset | Prompt Form | Important Classes |
|--------|-------------|-------------------|
| PowerShell 7 | `PS C:\path>` | `.ps-path`, `.ps-command`, `.ps-param`, `.ps-string`, `.ps-number` |
| macOS zsh | `user@MacBook-Pro folder %` | `.mac-userhost`, `.mac-path`, `.cmd` |
| SSH server | `user@host:~/path$` | `.env`, `.user`, `.host`, `.path`, `.root`, `.ok`, `.warn`, `.err` |

When the output already contains ANSI color intent, map it into semantic spans instead of
leaving raw escape codes in the screenshot. For example, a successful test result should
use `.ok`; warnings use `.warn`; stderr lines use `.stderr` or `.err`.

---

## Window Frame Decision

```
if user asks for "just content" or output is a tiny inline snippet:
    use No Frame (Template F)
elif line_count <= 6 and not has_startup_banner and not has_ssh_transition:
    use No Frame (Template F or shell-specific snippet styling)
elif is_linux_or_server_output and not has_ssh_transition and line_count <= 12:
    use shell-specific snippet styling, not a fake server window
elif preset in ["Windows Terminal PowerShell 7", "macOS Terminal zsh", "Remote Linux SSH Server"]:
    use high-fidelity frame (Template P1/M1/S1)
elif line_count > 40 or has_multiple_commands:
    use Frame (Template A/B/C/D)
else:
    use the matching high-fidelity preset if it helps authenticity; otherwise Template F
```

Chrome quality checks before render:
- In Windows Terminal templates, `.titlebar` should use `align-items: center`.
- `.tabs` should center neighboring controls and only bottom-align the active `.tab`.
- `.new-tab` and `.chevron` should have an explicit height matching the tab control area.
- If a screenshot has only one command and no startup/title context, remove the titlebar.

---

## Freeze-Style Stage (outer background / padding / radius / shadow)

Borrowed from charmbracelet/freeze and codeshot.io: a realistic screenshot is a
**windowed terminal floating on a stage**, never edge-to-edge. Wrap the terminal
window in a stage container on every framed template (Tier 3):

```css
/* Stage: the "desktop wallpaper" backdrop behind the terminal window */
.stage {
    min-height: 100vh;
    padding: 48px 56px;              /* breathing room around the window */
    display: flex;
    justify-content: center;
    align-items: flex-start;
    background: linear-gradient(135deg, #1b1e2b 0%, #151721 100%);
    /* solid alternative: background: #17181f; */
}
.window, .terminal {
    border-radius: 10px;             /* modern terminals are rounded */
    box-shadow: 0 16px 48px rgba(0, 0, 0, 0.45), 0 2px 8px rgba(0, 0, 0, 0.3);
    overflow: hidden;                /* clips children to the rounded corners */
}
```

Rules:
- The stage gradient must be subtle; it should read as a plain dark backdrop, not a poster.
- Set `<body>` background to the stage color, keep `html, body { overflow: hidden }`.
- Borderless evidence snippets (Template F) skip the stage and render edge-to-edge —
  they are embedded in reports, not floated on a desktop.
- Blinking cursor (framed interactive sessions only):
  `@keyframes blink { 50% { opacity: 0 } } .cursor { animation: blink 1.2s step-end infinite; }`
