#!/usr/bin/env python3
"""
chrome_probe.py — objective pixel measurements on a rendered terminal screenshot.

Reads a PNG (stdlib-only decoder), then reports:
  * colors at normalized points  (--points 0.02,0.05 0.965,0.05)
  * horizontal color runs along a row (--row 0.02)  -> widths of buttons, dots, tabs
  * vertical color runs along a column (--col 0.5)  -> heights of titlebar/tab strips
  * summary of the top band       (--region top)

All coordinates are fractions of width/height (0.0-1.0) unless --px is given.
Output is JSON on stdout for the multimodal validation protocol
(references/chrome-validation.md).

Usage:
    python chrome_probe.py shot.png --points 0.02,0.03 0.5,0.03
    python chrome_probe.py shot.png --row 0.03 --col 0.5 --region top
"""

import argparse
import json
import struct
import sys
import zlib


# ---------------------------------------------------------------------------
# Minimal PNG reader (8-bit, non-interlaced, color types 0/2/3/4/6)
# ---------------------------------------------------------------------------

def read_png(path: str) -> tuple[int, int, list[list[tuple[int, int, int]]]]:
    with open(path, "rb") as f:
        data = f.read()
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError("not a PNG file")

    pos = 8
    width = height = bit_depth = color_type = 0
    idat = bytearray()
    palette: list[tuple[int, int, int]] = []
    interlace = 0
    while pos < len(data):
        length, ctype = struct.unpack(">I4s", data[pos:pos + 8])
        chunk = data[pos + 8:pos + 8 + length]
        pos += 12 + length
        if ctype == b"IHDR":
            width, height, bit_depth, color_type, _, _, interlace = struct.unpack(
                ">IIBBBBB", chunk[:13])
        elif ctype == b"PLTE":
            palette = [tuple(chunk[i:i + 3]) for i in range(0, len(chunk), 3)]
        elif ctype == b"IDAT":
            idat.extend(chunk)
        elif ctype == b"IEND":
            break

    if bit_depth != 8 or interlace != 0:
        raise ValueError("only 8-bit non-interlaced PNGs are supported")
    channels = {0: 1, 2: 3, 3: 1, 4: 2, 6: 4}.get(color_type)
    if channels is None:
        raise ValueError(f"unsupported color type {color_type}")

    raw = zlib.decompress(bytes(idat))
    stride = width * channels
    pixels: list[list[tuple[int, int, int]]] = []
    prev = bytearray(stride)
    offset = 0
    for _y in range(height):
        filter_type = raw[offset]
        row = bytearray(raw[offset + 1:offset + 1 + stride])
        offset += 1 + stride
        bpp = channels
        if filter_type == 1:  # Sub
            for i in range(bpp, stride):
                row[i] = (row[i] + row[i - bpp]) & 0xFF
        elif filter_type == 2:  # Up
            for i in range(stride):
                row[i] = (row[i] + prev[i]) & 0xFF
        elif filter_type == 3:  # Average
            for i in range(stride):
                left = row[i - bpp] if i >= bpp else 0
                row[i] = (row[i] + ((left + prev[i]) >> 1)) & 0xFF
        elif filter_type == 4:  # Paeth
            for i in range(stride):
                a = row[i - bpp] if i >= bpp else 0
                b = prev[i]
                c = prev[i - bpp] if i >= bpp else 0
                p = a + b - c
                pa, pb, pc = abs(p - a), abs(p - b), abs(p - c)
                pred = a if pa <= pb and pa <= pc else (b if pb <= pc else c)
                row[i] = (row[i] + pred) & 0xFF
        prev = row

        line: list[tuple[int, int, int]] = []
        for x in range(width):
            i = x * channels
            if color_type == 0:
                g = row[i]
                line.append((g, g, g))
            elif color_type == 4:
                g = row[i]
                line.append((g, g, g))
            elif color_type == 2:
                line.append((row[i], row[i + 1], row[i + 2]))
            elif color_type == 3:
                line.append(palette[row[i]] if row[i] < len(palette) else (0, 0, 0))
            else:  # 6 RGBA — alpha-composite over black for sampling
                r, g, b, a = row[i], row[i + 1], row[i + 2], row[i + 3]
                line.append((r * a // 255, g * a // 255, b * a // 255))
        pixels.append(line)
    return width, height, pixels


# ---------------------------------------------------------------------------
# Measurements
# ---------------------------------------------------------------------------

def color_runs(seq, tol=12, min_run=1):
    """Collapse a pixel sequence into color runs [(value, count, start_index)]."""
    runs = []
    start = 0
    current = seq[0]
    for i in range(1, len(seq)):
        if max(abs(seq[i][c] - current[c]) for c in range(3)) > tol:
            if i - start >= min_run:
                runs.append({"color": "#%02X%02X%02X" % current,
                             "start": start, "width": i - start})
            start = i
            current = seq[i]
    runs.append({"color": "#%02X%02X%02X" % current,
                 "start": start, "width": len(seq) - start})
    return runs


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("png", help="PNG file to probe")
    parser.add_argument("--points", nargs="+", metavar="X,Y",
                        help="normalized (or --px) sample points")
    parser.add_argument("--row", metavar="Y", help="scan horizontal color runs at Y")
    parser.add_argument("--col", metavar="X", help="scan vertical color runs at X")
    parser.add_argument("--region", choices=["top"],
                        help="'top': summarize the top 80px band")
    parser.add_argument("--px", action="store_true", help="coordinates are pixels")
    parser.add_argument("--tol", type=int, default=12, help="color merge tolerance")
    args = parser.parse_args()

    try:
        width, height, pixels = read_png(args.png)
    except (OSError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    def px(value: float, axis: int) -> int:
        v = float(value)
        if args.px:
            return int(v)
        return int(round(v * (width if axis == 0 else height)))

    out = {"file": args.png, "width": width, "height": height}

    if args.points:
        pts = []
        for p in args.points:
            xs, ys = p.split(",")
            x, y = min(px(xs, 0), width - 1), min(px(ys, 1), height - 1)
            r, g, b = pixels[y][x]
            pts.append({"point": p, "pixel": [x, y], "rgb": "#%02X%02X%02X" % (r, g, b)})
        out["points"] = pts

    if args.row is not None:
        y = min(px(args.row, 1), height - 1)
        runs = color_runs(pixels[y], tol=args.tol, min_run=2)
        out["row_scan"] = {"y": y, "runs": runs}

    if args.col is not None:
        x = min(px(args.col, 0), width - 1)
        column = [pixels[y][x] for y in range(height)]
        runs = color_runs(column, tol=args.tol, min_run=2)
        out["col_scan"] = {"x": x, "runs": runs}

    if args.region == "top":
        band_h = min(80, height)
        # Row-distinct colors across the band: which rows differ from the row above
        rows = []
        for y in range(1, band_h):
            diff = sum(
                1 for x in range(0, width, 8)
                if max(abs(pixels[y][x][c] - pixels[y - 1][x][c]) for c in range(3)) > args.tol
            ) / (width // 8 + 1)
            if diff > 0.2:
                rows.append({"y": y, "changed_fraction": round(diff, 3)})
        r, g, b = pixels[2][2]
        out["top_band"] = {"height_scanned": band_h,
                           "corner_color": "#%02X%02X%02X" % (r, g, b),
                           "boundary_rows": rows}

    print(json.dumps(out, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
