"""Generate a stock price chart using only the Python standard library.

The original version of this script used pandas and matplotlib, but those
packages are unavailable in the execution environment.  This rewrite
implements a very small PNG renderer so we can still produce a chart for
``site_src/assets/price_sma.png``.
"""

from __future__ import annotations

import csv
import datetime as dt
import struct
import zlib
from typing import Iterable, List, Tuple


def read_prices(path: str) -> List[Tuple[dt.date, float]]:
    """Return a list of (date, close) tuples sorted by date."""
    records: List[Tuple[dt.date, float]] = []
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                date = dt.datetime.strptime(row["Date"], "%m/%d/%Y").date()
                close = float(row["Close"].replace(",", ""))
            except Exception:
                continue
            records.append((date, close))
    records.sort(key=lambda x: x[0])
    return records


def moving_average(values: Iterable[float], window: int) -> List[float]:
    """Simple moving average implementation."""
    result: List[float] = []
    queue: List[float] = []
    total = 0.0
    for v in values:
        queue.append(v)
        total += v
        if len(queue) > window:
            total -= queue.pop(0)
        if len(queue) == window:
            result.append(total / window)
        else:
            result.append(float("nan"))
    return result


def draw_chart(prices: List[Tuple[dt.date, float]], out_path: str) -> None:
    width, height = 1200, 700
    margin_l, margin_r, margin_t, margin_b = 70, 40, 40, 60
    plot_w = width - margin_l - margin_r
    plot_h = height - margin_t - margin_b

    dates = [d for d, _ in prices]
    values = [v for _, v in prices]

    sma7 = moving_average(values, 7)
    sma30 = moving_average(values, 30)

    vmin = min(values)
    vmax = max(values)

    def scale_x(idx: int) -> int:
        return margin_l + int(idx / (len(values) - 1) * plot_w)

    def scale_y(val: float) -> int:
        frac = (val - vmin) / (vmax - vmin) if vmax > vmin else 0
        return height - margin_b - int(frac * plot_h)

    # white background
    row = [255, 255, 255] * width
    pixels = [row[:] for _ in range(height)]

    def set_pixel(x: int, y: int, color: Tuple[int, int, int]):
        if 0 <= x < width and 0 <= y < height:
            i = x * 3
            pixels[y][i:i + 3] = list(color)

    def draw_line(x0: int, y0: int, x1: int, y1: int, color: Tuple[int, int, int]):
        dx = abs(x1 - x0)
        dy = -abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx + dy
        while True:
            set_pixel(x0, y0, color)
            if x0 == x1 and y0 == y1:
                break
            e2 = 2 * err
            if e2 >= dy:
                err += dy
                x0 += sx
            if e2 <= dx:
                err += dx
                y0 += sy

    # axes
    draw_line(margin_l, margin_t, margin_l, height - margin_b, (0, 0, 0))
    draw_line(margin_l, height - margin_b, width - margin_r, height - margin_b, (0, 0, 0))

    # data series
    colors = [(0, 0, 255), (0, 150, 0), (200, 0, 0)]
    series = [values, sma7, sma30]
    for color, series_values in zip(colors, series):
        prev_x = prev_y = None
        for idx, val in enumerate(series_values):
            if val != val:  # NaN check
                continue
            x = scale_x(idx)
            y = scale_y(val)
            if prev_x is not None:
                draw_line(prev_x, prev_y, x, y, color)
            prev_x, prev_y = x, y

    # encode PNG (unfiltered, RGB)
    raw = b"".join(b"\x00" + bytes(row) for row in pixels)
    compressed = zlib.compress(raw, 9)

    def chunk(tag: bytes, data: bytes) -> bytes:
        return struct.pack(">I", len(data)) + tag + data + struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF)

    ihdr = struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0)
    png_bytes = b"".join([
        b"\x89PNG\r\n\x1a\n",
        chunk(b"IHDR", ihdr),
        chunk(b"IDAT", compressed),
        chunk(b"IEND", b""),
    ])
    with open(out_path, "wb") as f:
        f.write(png_bytes)


def main() -> None:
    data = read_prices("data/tsla_prices.csv")
    if not data:
        return
    last_date = data[-1][0]
    cutoff = last_date - dt.timedelta(days=30 * 6)
    filtered = [item for item in data if item[0] >= cutoff]
    draw_chart(filtered, "site_src/assets/price_sma.png")


if __name__ == "__main__":
    main()
