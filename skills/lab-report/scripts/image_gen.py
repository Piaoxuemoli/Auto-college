#!/usr/bin/env python3
"""
Configurable image-generation adapter for lab-report illustrations.

Talks to any OpenAI-compatible images API ("image2"-style services, gateway
aggregators, local relays): it POSTs to {base_url}/images/generations with
the body {"model", "prompt", "size", "n": 1}, then either base64-decodes
data[0].b64_json or downloads data[0].url with a second GET.

Configuration lives in ~/.auto-college/image-gen.json:

    {
      "provider": "image2 example service",
      "base_url": "https://api.example.com/v1",
      "model": "image-2",
      "api_key": "sk-xxx",
      "default_size": "1024x1024",
      "timeout_seconds": 120
    }

The config path can be overridden with the AUTO_COLLEGE_IMAGE_GEN
environment variable or the --config flag (priority: --config > env var >
default path).

Usage:
    python image_gen.py "line-art schematic of a full-wave rectifier" \
        -o outputs/fig-rectifier.png --size 1024x1024

Exit codes (three-tier philosophy, aligned with render.py):
    0 — image generated, written, and verified
    1 — input error (empty prompt, missing/illegal output path, bad --size);
        the caller should fix its arguments
    2 — generation unavailable: config missing/invalid, or the API request
        failed. Callers must degrade gracefully: skip the illustration or
        fall back to the agent's built-in image capability, and never abort
        the report pipeline.

Notes:
    - Standard library only (urllib/json/base64/pathlib/argparse plus the
      usual os/re/sys); no subprocess, no third-party dependencies.
    - No PIL required: the written file is only checked to be non-empty and
      to start with the PNG magic bytes; dimension checks are skipped.
    - The api_key is never printed, logged, or echoed; all error text is
      run through a redactor that masks key-shaped tokens first.
"""

from __future__ import annotations

import argparse
import base64
import json
import os
import pathlib
import re
import sys
import urllib.error
import urllib.request

CONFIG_ENV_VAR = "AUTO_COLLEGE_IMAGE_GEN"
DEFAULT_CONFIG_PATH_PARTS = (".auto-college", "image-gen.json")
DEFAULT_SIZE = "1024x1024"
DEFAULT_TIMEOUT_SECONDS = 120
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"
SIZE_PATTERN = re.compile(r"^\d{2,5}x\d{2,5}$")
SECRET_PATTERN = re.compile(r"sk-[A-Za-z0-9_-]{6,}")
REQUIRED_CONFIG_FIELDS = ("base_url", "model", "api_key")
ALLOWED_URL_PREFIXES = ("http://", "https://")


class InputError(Exception):
    """Bad command-line input; the caller should fix its arguments (exit 1)."""


class UnavailableError(Exception):
    """Config missing/invalid or the API request failed; degrade (exit 2)."""


# ---------------------------------------------------------------------------
# Secret handling
# ---------------------------------------------------------------------------

def redact_secrets(text: str, secret: str = "") -> str:
    """Mask anything resembling an API key so keys can never leak into
    stdout, stderr, or logs."""
    result = str(text)
    if secret:
        result = result.replace(secret, "sk-***REDACTED***")
    return SECRET_PATTERN.sub("sk-***REDACTED***", result)


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

def resolve_config_path(cli_override: str | None = None) -> pathlib.Path:
    """--config beats $AUTO_COLLEGE_IMAGE_GEN beats ~/.auto-college/image-gen.json."""
    if cli_override and cli_override.strip():
        return pathlib.Path(cli_override.strip()).expanduser()
    env_value = os.environ.get(CONFIG_ENV_VAR, "").strip()
    if env_value:
        return pathlib.Path(env_value).expanduser()
    return pathlib.Path.home().joinpath(*DEFAULT_CONFIG_PATH_PARTS)


def load_config(path: pathlib.Path) -> dict:
    """Load and validate the adapter config.

    Raises UnavailableError — with messages that never contain the api_key —
    when the file is missing, unreadable, not JSON, or incomplete.
    """
    if not path.is_file():
        raise UnavailableError(
            f"image-gen config not found at {path} "
            "(expected format: see references/image-gen.md)"
        )
    try:
        raw = path.read_text(encoding="utf-8")
    except OSError as exc:
        raise UnavailableError(f"cannot read config {path}: {exc}") from exc
    try:
        data = json.loads(raw)
    except ValueError as exc:
        raise UnavailableError(f"invalid JSON in config {path}: {exc}") from exc
    if not isinstance(data, dict):
        raise UnavailableError(f"config {path} must contain a JSON object")

    missing = [field for field in REQUIRED_CONFIG_FIELDS
               if not str(data.get(field) or "").strip()]
    if missing:
        raise UnavailableError(
            f"config {path} is missing required field(s): {', '.join(missing)}"
        )

    base_url = str(data["base_url"]).strip().rstrip("/")
    if not base_url.lower().startswith(ALLOWED_URL_PREFIXES):
        raise UnavailableError("config base_url must be an http(s) URL")

    try:
        timeout_seconds = max(1, int(data.get("timeout_seconds",
                                              DEFAULT_TIMEOUT_SECONDS)))
    except (TypeError, ValueError):
        raise UnavailableError(
            "config timeout_seconds must be an integer number of seconds"
        ) from None

    return {
        "provider": str(data.get("provider")
                        or "OpenAI-compatible images API").strip(),
        "base_url": base_url,
        "model": str(data["model"]).strip(),
        "api_key": str(data["api_key"]).strip(),  # never printed anywhere
        "default_size": str(data.get("default_size") or DEFAULT_SIZE).strip(),
        "timeout_seconds": timeout_seconds,
    }


# ---------------------------------------------------------------------------
# Input validation
# ---------------------------------------------------------------------------

def resolve_output_path(raw_path: str | None) -> pathlib.Path:
    """Validate and normalize the output path.

    Security: paths containing a '..' component are rejected BEFORE any file
    is written, so a generated illustration can never escape the intended
    output directory.
    """
    text = (raw_path or "").strip()
    if not text:
        raise InputError("an output path is required (-o/--output out.png)")
    candidate = pathlib.PurePath(text)
    expanded = pathlib.PurePath(pathlib.Path(text).expanduser())
    if ".." in candidate.parts or ".." in expanded.parts:
        raise InputError("output path must not contain '..'")
    path = pathlib.Path(text).expanduser().resolve()
    if path.suffix.lower() != ".png":
        raise InputError("output file must end with .png (only PNG output is verified)")
    if path.is_dir():
        raise InputError(f"output path is an existing directory: {path}")
    return path


# ---------------------------------------------------------------------------
# API request / response handling
# ---------------------------------------------------------------------------

def _http_error_detail(exc: urllib.error.HTTPError) -> str:
    """Best-effort human-readable message from an HTTP error body."""
    try:
        raw = exc.read().decode("utf-8", errors="replace")
    except Exception:  # noqa: BLE001 — the body is best-effort only
        return str(exc.reason)
    try:
        parsed = json.loads(raw)
    except ValueError:
        return raw[:500] or str(exc.reason)
    if isinstance(parsed, dict):
        error = parsed.get("error")
        if isinstance(error, dict) and error.get("message"):
            return str(error["message"])
        if isinstance(error, str) and error:
            return error
        if parsed.get("message"):
            return str(parsed["message"])
    return raw[:500] or str(exc.reason)


def _fetch(request: urllib.request.Request, timeout: int, api_key: str,
           what: str) -> bytes:
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            return response.read()
    except urllib.error.HTTPError as exc:
        detail = redact_secrets(_http_error_detail(exc), api_key)
        raise UnavailableError(
            f"{what} failed: images API returned HTTP {exc.code}: {detail}"
        ) from exc
    except (urllib.error.URLError, TimeoutError, OSError) as exc:
        raise UnavailableError(redact_secrets(f"{what} failed: {exc}", api_key)) from exc


def _download_image(url: str, config: dict) -> bytes:
    """Second GET for responses that return data[0].url instead of b64_json."""
    if not url.lower().startswith(ALLOWED_URL_PREFIXES):
        raise UnavailableError(
            "images API returned a non-http(s) image URL; refusing to fetch it"
        )
    # Signed download URLs already embed their credentials; the API key is
    # deliberately NOT attached to this request.
    request = urllib.request.Request(url, headers={"Accept": "image/*"},
                                     method="GET")
    payload = _fetch(request, config["timeout_seconds"], config["api_key"],
                     "image download")
    if not payload:
        raise UnavailableError("downloaded image from images API is empty")
    return payload


def _extract_image_bytes(payload: bytes, config: dict) -> bytes:
    """Standard OpenAI-compatible response: data[0].b64_json first, then
    data[0].url as a second GET download."""
    try:
        data = json.loads(payload.decode("utf-8"))
    except (UnicodeDecodeError, ValueError) as exc:
        raise UnavailableError("images API response was not valid JSON") from exc
    items = data.get("data") if isinstance(data, dict) else None
    if not isinstance(items, list) or not items:
        raise UnavailableError("images API response has no data[0] entry")
    first = items[0]
    if not isinstance(first, dict):
        raise UnavailableError("images API response data[0] is malformed")

    b64_json = first.get("b64_json")
    if b64_json:
        try:
            return base64.b64decode(str(b64_json))
        except (ValueError, TypeError) as exc:
            raise UnavailableError(
                "images API b64_json could not be decoded"
            ) from exc

    url = first.get("url")
    if url:
        return _download_image(str(url), config)

    raise UnavailableError("images API response contains neither b64_json nor url")


def generate_image_bytes(config: dict, prompt: str, size: str) -> bytes:
    """POST {base_url}/images/generations and return the raw image bytes."""
    endpoint = f"{config['base_url']}/images/generations"
    body = {"model": config["model"], "prompt": prompt, "size": size, "n": 1}
    request = urllib.request.Request(
        endpoint,
        data=json.dumps(body).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "Accept": "application/json",
            # The Authorization header carries the api_key; it is never logged.
            "Authorization": f"Bearer {config['api_key']}",
        },
        method="POST",
    )
    payload = _fetch(request, config["timeout_seconds"], config["api_key"],
                     "image generation request")
    return _extract_image_bytes(payload, config)


# ---------------------------------------------------------------------------
# Output verification (PIL-free)
# ---------------------------------------------------------------------------

def verify_png(path: pathlib.Path) -> None:
    """Without PIL, only check that the file is non-empty and starts with
    the PNG magic bytes; dimension validation is intentionally skipped."""
    try:
        size = path.stat().st_size
        with path.open("rb") as handle:
            header = handle.read(len(PNG_MAGIC))
    except OSError as exc:
        raise UnavailableError(f"cannot verify written file {path}: {exc}") from exc
    if size == 0:
        raise UnavailableError(f"written file is empty: {path}")
    if header != PNG_MAGIC:
        raise UnavailableError(
            f"written file does not start with PNG magic bytes: {path} "
            "(the service may have returned a non-PNG format)"
        )


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Generate a lab-report illustration via a configurable "
                    "OpenAI-compatible images API.")
    parser.add_argument("prompt", nargs="?", default="",
                        help="prompt text for the illustration")
    parser.add_argument("-o", "--output", default=None,
                        help="output PNG path (required)")
    parser.add_argument("--size", default=None,
                        help="image size as WIDTHxHEIGHT, e.g. 1024x1024 "
                             "(default: default_size from the config)")
    parser.add_argument("--config", default=None,
                        help="config path override (default: "
                             "$AUTO_COLLEGE_IMAGE_GEN or "
                             "~/.auto-college/image-gen.json)")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)

    prompt = (args.prompt or "").strip()
    if not prompt:
        print("ERROR: prompt text is required", file=sys.stderr)
        return 1

    try:
        out_path = resolve_output_path(args.output)
    except InputError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    size = (args.size or "").strip()
    if size and not SIZE_PATTERN.match(size):
        print("ERROR: --size must look like WIDTHxHEIGHT, e.g. 1024x1024",
              file=sys.stderr)
        return 1

    try:
        config = load_config(resolve_config_path(args.config))
    except UnavailableError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        print("HINT: image generation is unavailable — skip the illustration "
              "or fall back to built-in image capability; do not abort the "
              "report flow.", file=sys.stderr)
        return 2

    final_size = size or config["default_size"]
    if not SIZE_PATTERN.match(final_size):
        print(f"ERROR: config default_size {final_size!r} must look like "
              "WIDTHxHEIGHT, e.g. 1024x1024", file=sys.stderr)
        return 2

    print(f"[image-gen] provider={config['provider']} "
          f"model={config['model']} size={final_size}")

    written = False
    try:
        image_bytes = generate_image_bytes(config, prompt, final_size)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_bytes(image_bytes)
        written = True
        verify_png(out_path)
    except UnavailableError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        if written:
            # Remove the invalid file so it is not mistaken for a good image.
            try:
                out_path.unlink()
            except OSError:
                pass
        return 2
    except OSError as exc:
        print(f"ERROR: cannot write output {out_path}: {exc}", file=sys.stderr)
        return 2

    print(f"OK: {out_path} ({out_path.stat().st_size / 1024:.0f} KB)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
