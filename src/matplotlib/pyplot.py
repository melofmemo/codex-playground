import struct
import zlib

_current_bars = []
_figsize = (640, 480)
_color = (135, 206, 250)  # skyblue RGB


def figure(figsize=(8, 6)):
    global _figsize
    _figsize = (int(figsize[0] * 80), int(figsize[1] * 80))


def bar(values, color='skyblue'):
    global _current_bars, _color
    _current_bars = list(values)
    if isinstance(color, str) and color == 'skyblue':
        _color = (135, 206, 250)
    elif isinstance(color, str) and color.startswith('#') and len(color) == 7:
        _color = tuple(int(color[i:i+2], 16) for i in (1, 3, 5))
    elif isinstance(color, tuple) and len(color) == 3:
        _color = color


def xlabel(x):
    pass

def ylabel(y):
    pass

def title(t):
    pass

def tight_layout():
    pass


def savefig(filename):
    width, height = _figsize
    num_bars = len(_current_bars)
    if num_bars == 0:
        raise ValueError('No bars to plot')
    bar_width = width // (num_bars * 2)
    max_val = max(_current_bars)
    pixels = [ [_bg()] * width for _ in range(height) ]

    for idx, val in enumerate(_current_bars):
        bar_height = int((val / max_val) * (height - 20))
        x0 = idx * 2 * bar_width + bar_width // 2
        for x in range(x0, x0 + bar_width):
            for y in range(height - bar_height, height):
                pixels[y][x] = _color

    write_png(filename, width, height, pixels)


def close():
    global _current_bars
    _current_bars = []


def _bg():
    return (255, 255, 255)


def write_png(path, width, height, pixels):
    row_bytes = []
    for row in pixels:
        row_bytes.append(b'\x00' + bytes([c for pixel in row for c in pixel]))
    raw = b''.join(row_bytes)
    compressor = zlib.compressobj()
    compressed = compressor.compress(raw) + compressor.flush()

    def chunk(chunk_type, data):
        return (struct.pack('>I', len(data)) + chunk_type + data +
                struct.pack('>I', zlib.crc32(chunk_type + data) & 0xffffffff))

    ihdr = struct.pack('>IIBBBBB', width, height, 8, 2, 0, 0, 0)
    png = b'\x89PNG\r\n\x1a\n' + chunk(b'IHDR', ihdr) + chunk(b'IDAT', compressed) + chunk(b'IEND', b'')
    with open(path, 'wb') as f:
        f.write(png)
