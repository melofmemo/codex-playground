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
    margin_l, margin_r, margin_t, margin_b = 100, 120, 80, 80
    plot_w = width - margin_l - margin_r
    plot_h = height - margin_t - margin_b

    dates = [d for d, _ in prices]
    values = [v for _, v in prices]

    sma7 = moving_average(values, 7)
    sma30 = moving_average(values, 30)

    vmin = min(values)
    vmax = max(values)
    vrange = vmax - vmin
    # Add some padding to price range
    vmin -= vrange * 0.05
    vmax += vrange * 0.05

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

    def draw_line(x0: int, y0: int, x1: int, y1: int, color: Tuple[int, int, int], dashed=False, thickness=1):
        dx = abs(x1 - x0)
        dy = -abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx + dy
        
        if dashed:
            dash_length = 6
            gap_length = 4
            dash_counter = 0
            draw_pixel = True
        
        while True:
            if not dashed or draw_pixel:
                if thickness == 1:
                    set_pixel(x0, y0, color)
                else:
                    # Draw a thicker line by setting pixels in a small radius
                    for tx in range(-thickness//2, thickness//2 + 1):
                        for ty in range(-thickness//2, thickness//2 + 1):
                            set_pixel(x0 + tx, y0 + ty, color)
            
            if dashed:
                dash_counter = (dash_counter + 1) % (dash_length + gap_length)
                draw_pixel = dash_counter < dash_length
                
            if x0 == x1 and y0 == y1:
                break
            e2 = 2 * err
            if e2 >= dy:
                err += dy
                x0 += sx
            if e2 <= dx:
                err += dx
                y0 += sy
                
    def draw_rect(x0: int, y0: int, width: int, height: int, color: Tuple[int, int, int], fill=True):
        if fill:
            for y in range(y0, y0 + height):
                for x in range(x0, x0 + width):
                    set_pixel(x, y, color)
        else:
            # Just draw the outline
            draw_line(x0, y0, x0 + width - 1, y0, color)  # Top
            draw_line(x0, y0 + height - 1, x0 + width - 1, y0 + height - 1, color)  # Bottom
            draw_line(x0, y0, x0, y0 + height - 1, color)  # Left
            draw_line(x0 + width - 1, y0, x0 + width - 1, y0 + height - 1, color)  # Right

    # Simple text drawing function
    def draw_simple_text(x: int, y: int, text: str, color: Tuple[int, int, int], scale=1):
        """Draw text using simple line segments for basic letters.
        This is a very basic implementation to avoid complex font rendering."""
        
        letter_width = 6 * scale
        letter_spacing = 1 * scale
        current_x = x
        
        for char in text:
            if char == ' ':
                current_x += letter_width + letter_spacing
                continue
            
            # Draw very simple shapes for letters
            # This is a super simplified version that just draws some distinctive
            # shapes for common letters
            if char.lower() == 't':  # T shape
                mid = current_x + letter_width // 2
                draw_line(current_x, y, current_x + letter_width, y, color, thickness=scale)
                draw_line(mid, y, mid, y + letter_width, color, thickness=scale)
            elif char.lower() == 's':  # S shape
                draw_line(current_x + letter_width, y, current_x, y, color, thickness=scale)
                draw_line(current_x, y, current_x, y + letter_width//2, color, thickness=scale)
                draw_line(current_x, y + letter_width//2, current_x + letter_width, y + letter_width//2, color, thickness=scale)
                draw_line(current_x + letter_width, y + letter_width//2, current_x + letter_width, y + letter_width, color, thickness=scale)
                draw_line(current_x + letter_width, y + letter_width, current_x, y + letter_width, color, thickness=scale)
            elif char.lower() == 'l':  # L shape
                draw_line(current_x, y, current_x, y + letter_width, color, thickness=scale)
                draw_line(current_x, y + letter_width, current_x + letter_width, y + letter_width, color, thickness=scale)
            elif char.lower() == 'a':  # A shape
                draw_line(current_x, y + letter_width, current_x + letter_width//2, y, color, thickness=scale)
                draw_line(current_x + letter_width//2, y, current_x + letter_width, y + letter_width, color, thickness=scale)
                draw_line(current_x + letter_width//4, y + letter_width//2, current_x + 3*letter_width//4, y + letter_width//2, color, thickness=scale)
            elif char.lower() == 'p':  # P shape
                draw_line(current_x, y, current_x, y + letter_width, color, thickness=scale)
                draw_line(current_x, y, current_x + letter_width, y, color, thickness=scale)
                draw_line(current_x + letter_width, y, current_x + letter_width, y + letter_width//2, color, thickness=scale)
                draw_line(current_x + letter_width, y + letter_width//2, current_x, y + letter_width//2, color, thickness=scale)
            elif char.lower() == 'r':  # R shape
                draw_line(current_x, y, current_x, y + letter_width, color, thickness=scale)
                draw_line(current_x, y, current_x + letter_width, y, color, thickness=scale)
                draw_line(current_x + letter_width, y, current_x + letter_width, y + letter_width//2, color, thickness=scale)
                draw_line(current_x + letter_width, y + letter_width//2, current_x, y + letter_width//2, color, thickness=scale)
                draw_line(current_x, y + letter_width//2, current_x + letter_width, y + letter_width, color, thickness=scale)
            elif char.lower() == 'i':  # I shape
                mid = current_x + letter_width // 2
                draw_line(current_x, y, current_x + letter_width, y, color, thickness=scale)
                draw_line(mid, y, mid, y + letter_width, color, thickness=scale)
                draw_line(current_x, y + letter_width, current_x + letter_width, y + letter_width, color, thickness=scale)
            elif char.lower() == 'c':  # C shape
                draw_line(current_x + letter_width, y, current_x, y, color, thickness=scale)
                draw_line(current_x, y, current_x, y + letter_width, color, thickness=scale)
                draw_line(current_x, y + letter_width, current_x + letter_width, y + letter_width, color, thickness=scale)
            elif char.lower() == 'e':  # E shape
                draw_line(current_x, y, current_x, y + letter_width, color, thickness=scale)
                draw_line(current_x, y, current_x + letter_width, y, color, thickness=scale)
                draw_line(current_x, y + letter_width//2, current_x + letter_width*3//4, y + letter_width//2, color, thickness=scale)
                draw_line(current_x, y + letter_width, current_x + letter_width, y + letter_width, color, thickness=scale)
            elif char.lower() == 'b':  # B shape
                draw_line(current_x, y, current_x, y + letter_width, color, thickness=scale)
                draw_line(current_x, y, current_x + letter_width*3//4, y, color, thickness=scale)
                draw_line(current_x + letter_width*3//4, y, current_x + letter_width, y + letter_width//4, color, thickness=scale)
                draw_line(current_x + letter_width, y + letter_width//4, current_x + letter_width*3//4, y + letter_width//2, color, thickness=scale)
                draw_line(current_x, y + letter_width//2, current_x + letter_width*3//4, y + letter_width//2, color, thickness=scale)
                draw_line(current_x + letter_width*3//4, y + letter_width//2, current_x + letter_width, y + letter_width*3//4, color, thickness=scale)
                draw_line(current_x + letter_width, y + letter_width*3//4, current_x + letter_width*3//4, y + letter_width, color, thickness=scale)
                draw_line(current_x, y + letter_width, current_x + letter_width*3//4, y + letter_width, color, thickness=scale)
            elif char.lower() == 'u':  # U shape
                draw_line(current_x, y, current_x, y + letter_width*3//4, color, thickness=scale)
                draw_line(current_x, y + letter_width*3//4, current_x + letter_width//2, y + letter_width, color, thickness=scale)
                draw_line(current_x + letter_width//2, y + letter_width, current_x + letter_width, y + letter_width*3//4, color, thickness=scale)
                draw_line(current_x + letter_width, y + letter_width*3//4, current_x + letter_width, y, color, thickness=scale)
            elif char.lower() == 'g':  # G shape
                draw_line(current_x + letter_width, y, current_x, y, color, thickness=scale)
                draw_line(current_x, y, current_x, y + letter_width, color, thickness=scale)
                draw_line(current_x, y + letter_width, current_x + letter_width, y + letter_width, color, thickness=scale)
                draw_line(current_x + letter_width, y + letter_width, current_x + letter_width, y + letter_width//2, color, thickness=scale)
                draw_line(current_x + letter_width, y + letter_width//2, current_x + letter_width//2, y + letter_width//2, color, thickness=scale)
            elif char.lower() == 'n':  # N shape
                draw_line(current_x, y, current_x, y + letter_width, color, thickness=scale)
                draw_line(current_x, y, current_x + letter_width, y + letter_width, color, thickness=scale)
                draw_line(current_x + letter_width, y + letter_width, current_x + letter_width, y, color, thickness=scale)
            elif char.lower() == 'd':  # D shape
                draw_line(current_x, y, current_x, y + letter_width, color, thickness=scale)
                draw_line(current_x, y, current_x + letter_width*2//3, y, color, thickness=scale)
                draw_line(current_x + letter_width*2//3, y, current_x + letter_width, y + letter_width//3, color, thickness=scale)
                draw_line(current_x + letter_width, y + letter_width//3, current_x + letter_width, y + letter_width*2//3, color, thickness=scale)
                draw_line(current_x + letter_width, y + letter_width*2//3, current_x + letter_width*2//3, y + letter_width, color, thickness=scale)
                draw_line(current_x, y + letter_width, current_x + letter_width*2//3, y + letter_width, color, thickness=scale)
            elif char.lower() == '7':  # 7 shape
                draw_line(current_x, y, current_x + letter_width, y, color, thickness=scale)
                draw_line(current_x + letter_width, y, current_x + letter_width//2, y + letter_width, color, thickness=scale)
            elif char.lower() == '3':  # 3 shape
                draw_line(current_x, y, current_x + letter_width, y, color, thickness=scale)
                draw_line(current_x + letter_width, y, current_x + letter_width, y + letter_width//2, color, thickness=scale)
                draw_line(current_x + letter_width//2, y + letter_width//2, current_x + letter_width, y + letter_width//2, color, thickness=scale)
                draw_line(current_x + letter_width, y + letter_width//2, current_x + letter_width, y + letter_width, color, thickness=scale)
                draw_line(current_x + letter_width, y + letter_width, current_x, y + letter_width, color, thickness=scale)
            elif char.lower() == '0':  # 0 shape
                draw_line(current_x, y, current_x + letter_width, y, color, thickness=scale)
                draw_line(current_x, y, current_x, y + letter_width, color, thickness=scale)
                draw_line(current_x, y + letter_width, current_x + letter_width, y + letter_width, color, thickness=scale)
                draw_line(current_x + letter_width, y, current_x + letter_width, y + letter_width, color, thickness=scale)
            elif char.lower() == 'm':  # M shape
                draw_line(current_x, y, current_x, y + letter_width, color, thickness=scale)
                draw_line(current_x, y, current_x + letter_width//2, y + letter_width//2, color, thickness=scale)
                draw_line(current_x + letter_width//2, y + letter_width//2, current_x + letter_width, y, color, thickness=scale)
                draw_line(current_x + letter_width, y, current_x + letter_width, y + letter_width, color, thickness=scale)
            elif char.lower() == 'v':  # V shape
                draw_line(current_x, y, current_x + letter_width//2, y + letter_width, color, thickness=scale)
                draw_line(current_x + letter_width//2, y + letter_width, current_x + letter_width, y, color, thickness=scale)
            elif char.lower() == '-':  # - shape
                draw_line(current_x, y + letter_width//2, current_x + letter_width, y + letter_width//2, color, thickness=scale)
            elif char.lower() == ':':  # : shape
                dot_size = max(1, scale)
                for dx in range(-dot_size, dot_size+1):
                    for dy in range(-dot_size, dot_size+1):
                        set_pixel(current_x + letter_width//2 + dx, y + letter_width//3 + dy, color)
                        set_pixel(current_x + letter_width//2 + dx, y + letter_width*2//3 + dy, color)
            elif char.lower() == '(':  # ( shape
                draw_line(current_x + letter_width*2//3, y, current_x + letter_width//3, y + letter_width//3, color, thickness=scale)
                draw_line(current_x + letter_width//3, y + letter_width//3, current_x + letter_width//3, y + letter_width*2//3, color, thickness=scale)
                draw_line(current_x + letter_width//3, y + letter_width*2//3, current_x + letter_width*2//3, y + letter_width, color, thickness=scale)
            elif char.lower() == ')':  # ) shape
                draw_line(current_x + letter_width//3, y, current_x + letter_width*2//3, y + letter_width//3, color, thickness=scale)
                draw_line(current_x + letter_width*2//3, y + letter_width//3, current_x + letter_width*2//3, y + letter_width*2//3, color, thickness=scale)
                draw_line(current_x + letter_width*2//3, y + letter_width*2//3, current_x + letter_width//3, y + letter_width, color, thickness=scale)
            else:
                # For any other character, draw a simple vertical line
                draw_line(current_x + letter_width//2, y, current_x + letter_width//2, y + letter_width, color, thickness=scale)
            
            current_x += letter_width + letter_spacing
            
        return current_x  # Return the ending x position

    # Grid lines (light gray)
    grid_color = (220, 220, 220)
    # Vertical grid lines (every month)
    month_positions = []
    prev_month = None
    for idx, date in enumerate(dates):
        if prev_month is None or date.month != prev_month:
            x = scale_x(idx)
            draw_line(x, margin_t, x, height - margin_b, grid_color, dashed=True)
            month_positions.append((idx, date))
            prev_month = date.month
    
    # Horizontal grid lines
    num_h_lines = 5
    for i in range(num_h_lines + 1):
        y_val = vmin + (vmax - vmin) * i / num_h_lines
        y = scale_y(y_val)
        draw_line(margin_l, y, width - margin_r, y, grid_color, dashed=True)

    # axes
    draw_line(margin_l, margin_t, margin_l, height - margin_b, (0, 0, 0), thickness=2)
    draw_line(margin_l, height - margin_b, width - margin_r, height - margin_b, (0, 0, 0), thickness=2)

    # Draw price ticks on Y-axis
    for i in range(num_h_lines + 1):
        y_val = vmin + (vmax - vmin) * i / num_h_lines
        y = scale_y(y_val)
        draw_line(margin_l - 5, y, margin_l, y, (0, 0, 0), thickness=2)
    
    # Draw month ticks on X-axis
    for idx, date in month_positions:
        x = scale_x(idx)
        draw_line(x, height - margin_b, x, height - margin_b + 5, (0, 0, 0), thickness=2)

    # data series
    colors = [(0, 0, 255), (0, 150, 0), (200, 0, 0)]  # Blue, Green, Red
    series = [values, sma7, sma30]
    for color, series_values in zip(colors, series):
        prev_x = prev_y = None
        for idx, val in enumerate(series_values):
            if val != val:  # NaN check
                continue
            x = scale_x(idx)
            y = scale_y(val)
            if prev_x is not None:
                draw_line(prev_x, prev_y, x, y, color, thickness=2)
            prev_x, prev_y = x, y
    
    # Add title at the top
    title_y = margin_t - 40
    draw_simple_text(margin_l, title_y, "TESLA STOCK PRICE CHART", (0, 0, 0), scale=2)
    
    # Draw legend with colored boxes and simple text
    legend_x = width - margin_r + 20
    legend_y = margin_t + 30
    legend_box_size = 15
    legend_spacing = 30
    
    # Price line (Blue)
    draw_rect(legend_x, legend_y, legend_box_size, legend_box_size, colors[0])
    draw_simple_text(legend_x + legend_box_size + 10, legend_y + 5, "PRICE", (0, 0, 0))
    
    # 7-day SMA (Green)
    legend_y += legend_spacing
    draw_rect(legend_x, legend_y, legend_box_size, legend_box_size, colors[1])
    draw_simple_text(legend_x + legend_box_size + 10, legend_y + 5, "7-DAY SMA", (0, 0, 0))
    
    # 30-day SMA (Red)
    legend_y += legend_spacing
    draw_rect(legend_x, legend_y, legend_box_size, legend_box_size, colors[2])
    draw_simple_text(legend_x + legend_box_size + 10, legend_y + 5, "30-DAY SMA", (0, 0, 0))
    
    # Label axes
    x_label_y = height - margin_b + 40
    draw_simple_text(width // 2 - 30, x_label_y, "DATE", (0, 0, 0), scale=2)
    
    y_label_x = margin_l - 70
    y_label_y = margin_t + plot_h // 2
    draw_simple_text(y_label_x, y_label_y, "PRICE", (0, 0, 0), scale=2)
    
    # Draw a border around the plot area
    draw_rect(margin_l, margin_t, plot_w, plot_h, (0, 0, 0), fill=False)

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
    # Chart legend information file
    legend_text = """# TSLA Stock Price Chart Legend

## Lines:
- Blue: TSLA Stock Price
- Green: 7-day Simple Moving Average (SMA)
- Red: 30-day Simple Moving Average (SMA)

The chart shows 6 months of price data with monthly tick marks on the x-axis.
"""
    with open("site_src/assets/chart_legend.md", "w") as f:
        f.write(legend_text)
    
    data = read_prices("data/tsla_prices.csv")
    if not data:
        return
    last_date = data[-1][0]
    cutoff = last_date - dt.timedelta(days=30 * 6)
    filtered = [item for item in data if item[0] >= cutoff]
    draw_chart(filtered, "site_src/assets/price_sma.png")


if __name__ == "__main__":
    main()
