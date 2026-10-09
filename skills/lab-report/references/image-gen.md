# Image Generation Reference

Configurable adapter (`scripts/image_gen.py`) for generating illustration
images for lab reports through any OpenAI-compatible images API. Python
standard library only; no third-party dependencies, no PIL required.

## Configuration

The adapter reads a single local JSON config. Default path:
`~/.auto-college/image-gen.json`. The path can be overridden with the
`AUTO_COLLEGE_IMAGE_GEN` environment variable or the `--config` flag
(priority: `--config` > env var > default path).

```json
{
  "provider": "image2 example service",
  "base_url": "https://api.example.com/v1",
  "model": "image-2",
  "api_key": "sk-xxx",
  "default_size": "1024x1024",
  "timeout_seconds": 120
}
```

| Field | Required | Default | Meaning |
|-------|----------|---------|---------|
| `provider` | no | `OpenAI-compatible images API` | Display name used in log lines only |
| `base_url` | yes | — | API root; the script POSTs to `{base_url}/images/generations`. Use HTTPS. |
| `model` | yes | — | Model name, e.g. `image-2` |
| `api_key` | yes | — | Bearer token; stored only in this local file |
| `default_size` | no | `1024x1024` | Used when `--size` is omitted |
| `timeout_seconds` | no | `120` | Per-request timeout for both the POST and the image download GET |

## Supported services

Any service that exposes an OpenAI-compatible images endpoint:
`POST {base_url}/images/generations` with body `{"model","prompt","size","n":1}`.
This covers "image2"-class image models behind OpenAI-compatible gateways,
aggregator platforms, and self-hosted relays. The response must contain
either `data[0].b64_json` (preferred; base64-decoded locally) or
`data[0].url` (downloaded with a second GET). Services that return neither
shape are not supported.

## Usage

```bash
python lab-report/scripts/image_gen.py \
    "clean line-art schematic of a full-wave bridge rectifier, white background" \
    -o outputs/2026-10-09/fig-rectifier.png --size 1024x1024
```

- Output must be a `.png` path; parent directories are created as needed.
- Output paths containing `..` are rejected before anything is written.
- The result is verified without PIL: the file must be non-empty and start
  with the PNG magic bytes. Dimension checks are intentionally skipped so
  the script stays dependency-free.

## Exit codes and graceful degradation

| Exit | Meaning | Caller action |
|------|---------|---------------|
| 0 | Image generated and verified | Embed the PNG in the report |
| 1 | Input error: empty prompt, missing/illegal output path, bad `--size` | Fix the command line |
| 2 | Generation unavailable: config missing/invalid, or the API request failed | Degrade gracefully; never abort the report flow |

Degradation path (same philosophy as the terminal-screenshot `render.py`
tiers): when the script exits 2 — for example, no
`~/.auto-college/image-gen.json` exists yet — the report pipeline simply
continues without the illustration. Mark the illustration slot as
“未生成 (not generated)” with a one-line placeholder caption, or fall back
to the agent's built-in image generation capability if available. A missing
illustration must never block or crash report generation.

## Security notes

- The `api_key` lives only in the local config file under `~/.auto-college/`.
  Never commit it to the repository, paste it into a report, or expose it in
  shell history or screenshots.
- The script never prints, logs, or echoes the key; all error messages pass
  through a redactor that masks `sk-…`-shaped tokens.
- Image downloads are restricted to `http(s)` URLs returned by the API; the
  API key is not attached to download requests.
- Output paths are validated (`..`-free, `.png` suffix, not an existing
  directory) before any file is written.
