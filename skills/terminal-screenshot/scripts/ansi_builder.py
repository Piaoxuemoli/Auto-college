#!/usr/bin/env python3
"""
Build realistic ANSI-escaped terminal session text for fake/forged terminal content.

The output is plain text with truecolor SGR escape sequences, ready to be piped
into a real terminal emulator renderer such as `termframe` (stdin) so that all
coloring, spacing, and cursor styling is produced by a genuine terminal engine
instead of hand-written HTML spans.

Session spec (JSON):
    {
      "preset": "ssh" | "root" | "zsh" | "powershell" | "cmd" | "crt",
      "user": "ubuntu", "host": "gpu-a100-01", "path": "~/train",
      "commands": [
        {"cmd": "nvidia-smi", "output": ["...", "..."]},
        {"cmd": "python train.py", "output": ["epoch 1 ..."]}
      ]
    }

CLI:
    python ansi_builder.py spec.json [-o session.ansi]     # write ANSI file
    python ansi_builder.py spec.json | termframe -o out.png
"""

import argparse
import json
import pathlib
import sys

RESET = "\x1b[0m"
BOLD = "\x1b[1m"
DIM = "\x1b[2m"


def fg(hex_color: str) -> str:
    """Truecolor foreground SGR from #rrggbb."""
    h = hex_color.lstrip("#")
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    return f"\x1b[38;2;{r};{g};{b}m"


# Prompt palettes per preset. Colors mirror the presets documented in
# references/terminal-types.md so ANSI output and HTML fallback look alike.
PRESETS = {
    # Ubuntu/bash default: green user@host, blue path
    "ssh": {
        "user": "#8AE234", "host": "#8AE234", "path": "#729FCF",
        "symbol": "$", "cmd": "#D3D7CF", "default": "#D3D7CF",
    },
    # root shell: red user@host
    "root": {
        "user": "#EF2929", "host": "#EF2929", "path": "#729FCF",
        "symbol": "#", "cmd": "#D3D7CF", "default": "#D3D7CF",
    },
    # macOS zsh: green user@host, cyan path, % prompt
    "zsh": {
        "user": "#5AF78E", "host": "#5AF78E", "path": "#57C7FF",
        "symbol": "%", "cmd": "#F1F1F1", "default": "#CCCCCC",
    },
    # PowerShell 7: "PS path>" prompt with yellow path
    "powershell": {
        "user": "#CCCCCC", "host": "#CCCCCC", "path": "#E5E510",
        "symbol": ">", "prefix": "PS ", "cmd": "#FFFFFC", "default": "#CCCCCC",
    },
    # cmd.exe: plain "C:\\path>" prompt, monochrome
    "cmd": {
        "user": "#CCCCCC", "host": "#CCCCCC", "path": "#CCCCCC",
        "symbol": ">", "prefix": "", "cmd": "#CCCCCC", "default": "#CCCCCC",
    },
    # Green phosphor CRT: monochrome green
    "crt": {
        "user": "#33FF33", "host": "#33FF33", "path": "#33FF33",
        "symbol": "$", "cmd": "#66FF66", "default": "#33FF33",
    },
}


def build_prompt(spec: dict, palette: dict) -> str:
    preset = spec.get("preset", "ssh")
    path = spec.get("path", "~")
    if preset in ("ssh", "root", "crt"):
        return (
            f"{BOLD}{fg(palette['user'])}{spec.get('user', 'user')}"
            f"@{spec.get('host', 'host')}{RESET}"
            f":{fg(palette['path'])}{path}{RESET}"
            f"{palette['symbol']} "
        )
    if preset == "zsh":
        return (
            f"{fg(palette['user'])}{spec.get('user', 'user')}"
            f"@{spec.get('host', 'macbook')}{RESET} "
            f"{fg(palette['path'])}{path.rsplit('/', 1)[-1] or '/'}{RESET} "
            f"{palette['symbol']} "
        )
    # powershell / cmd
    prefix = palette.get("prefix", "")
    return f"{prefix}{fg(palette['path'])}{path}{RESET}{palette['symbol']} "


def render_session(spec: dict) -> str:
    preset = spec.get("preset", "ssh")
    palette = PRESETS.get(preset, PRESETS["ssh"])
    default = fg(palette["default"])
    lines = []
    for i, entry in enumerate(spec.get("commands", [])):
        if i > 0:
            lines.append("")
        lines.append(build_prompt(spec, palette) + f"{default}{entry.get('cmd', '')}{RESET}")
        for out in entry.get("output", []):
            lines.append(f"{default}{out}{RESET}")
    return "\n".join(lines) + "\n"


def main():
    parser = argparse.ArgumentParser(description="Build ANSI terminal session text.")
    parser.add_argument("spec", help="Session spec JSON file")
    parser.add_argument("-o", "--output", help="Output .ansi file (default: stdout)")
    args = parser.parse_args()

    try:
        spec = json.loads(pathlib.Path(args.spec).read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        print(f"ERROR: cannot read spec: {exc}", file=sys.stderr)
        sys.exit(1)

    text = render_session(spec)
    if args.output:
        # Keep writes inside the current working directory; no parent escapes.
        if ".." in args.output.replace("\\", "/").split("/"):
            print(f"ERROR: output path must stay inside the working directory: {args.output}",
                  file=sys.stderr)
            sys.exit(1)
        pathlib.Path(args.output).write_text(text, encoding="utf-8")
        print(f"OK: {args.output}")
    else:
        sys.stdout.buffer.write(text.encode("utf-8"))


if __name__ == "__main__":
    main()
