#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Generate the original LDAP Browser icons with the Python standard library."""

from math import hypot
from pathlib import Path
from struct import pack
from textwrap import dedent
from zlib import compress, crc32

ICON_DIRECTORY = Path(__file__).resolve().parent
REPOSITORY = ICON_DIRECTORY.parent.parent
BACKGROUND = (15, 51, 49)
BRANCH = (178, 240, 204)
NODE = (237, 252, 221)
NODE_POSITIONS = ((26, 31), (48, 24), (70, 31), (48, 72))
PALETTE = ((0, 0, 0), BACKGROUND, BRANCH, NODE)
LICENSE = dedent("""\
    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        https://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
""")


def render(size):
    """Rasterize a rounded tile and directory tree on a 96-unit canvas."""
    samples = 4 if size <= 128 else 1
    scale = 96 / (size * samples)
    pixels = bytearray()
    for row in range(size):
        for column in range(size):
            colors = []
            for sy in range(samples):
                for sx in range(samples):
                    x = (column * samples + sx + 0.5) * scale
                    y = (row * samples + sy + 0.5) * scale
                    if hypot(max(abs(x - 48) - 25, 0), max(abs(y - 48) - 25, 0)) > 17:
                        continue
                    if any((x - nx) ** 2 + (y - ny) ** 2 <= 7 ** 2
                           for nx, ny in NODE_POSITIONS):
                        color = NODE
                    elif (46 <= x <= 50 and 24 <= y <= 72
                          or 26 <= x <= 70 and 46 <= y <= 50
                          or (24 <= x <= 28 or 68 <= x <= 72) and 31 <= y <= 50):
                        color = BRANCH
                    else:
                        color = BACKGROUND
                    colors.append(color)
            if colors:
                pixels.extend(round(sum(channel) / len(colors)) for channel in zip(*colors))
                pixels.append(round(255 * len(colors) / samples ** 2))
            else:
                pixels.extend((0, 0, 0, 0))
    return pixels


def png_chunk(kind, data):
    return pack(">I", len(data)) + kind + data + pack(">I", crc32(kind + data))


def png(size, pixels):
    stride = size * 4
    rows = b"".join(b"\0" + pixels[start:start + stride]
                    for start in range(0, len(pixels), stride))
    header = pack(">IIBBBBB", size, size, 8, 6, 0, 0, 0)
    return (b"\x89PNG\r\n\x1a\n" + png_chunk(b"IHDR", header)
            + png_chunk(b"IDAT", compress(rows, 9)) + png_chunk(b"IEND", b""))


def write_icns(images):
    types = ((16, b"icp4"), (32, b"icp5"), (64, b"icp6"), (128, b"ic07"),
             (256, b"ic08"), (512, b"ic09"), (1024, b"ic10"))
    entries = b"".join(kind + pack(">I", len(images[size]) + 8) + images[size]
                       for size, kind in types)
    path = ICON_DIRECTORY / "macosx" / "ldap-browser.icns"
    path.write_bytes(b"icns" + pack(">I", len(entries) + 8) + entries)


def palette_index(pixel):
    if pixel[3] < 128:
        return 0
    return min(range(1, len(PALETTE)), key=lambda index: sum(
        (a - b) ** 2 for a, b in zip(pixel, PALETTE[index])))


def icon_bitmap(size, pixels, depth):
    """Encode the uncompressed DIB format required by the Eclipse launcher brander."""
    pixel_data = bytearray()
    mask = bytearray()
    for row in reversed(range(size)):
        start = row * size * 4
        mask_bits = 0
        for index in range(start, start + size * 4, 4):
            r, g, b, a = pixels[index:index + 4]
            if depth == 32:
                pixel_data.extend((b, g, r, a))
            else:
                pixel_data.append(palette_index((r, g, b, a)))
            mask_bits = (mask_bits << 1) | (a < 128)
        mask_stride = (size + 31) // 32 * 4
        mask.extend((mask_bits << (mask_stride * 8 - size)).to_bytes(mask_stride, "big"))
    palette = b""
    if depth == 8:
        palette = b"".join(bytes((b, g, r, 0)) for r, g, b in PALETTE).ljust(1024, b"\0")
    header = pack("<IIIHHIIIIII", 40, size, size * 2, 1, depth, 0, len(pixel_data), 0, 0, 0, 0)
    return header + palette + pixel_data + mask


def write_ico(pixels):
    # Match the Windows launcher's resource sizes and color depths.
    variants = ((24, 8), (32, 32), (32, 8), (48, 32), (48, 8), (16, 32), (16, 8))
    directory = bytearray(pack("<HHH", 0, 1, len(variants)))
    offset = len(directory) + 16 * len(variants)
    bitmaps = []
    for size, depth in variants:
        bitmap = icon_bitmap(size, pixels[size], depth)
        directory.extend(pack("<BBBBHHII", size, size, 0, 0, 1, depth, len(bitmap), offset))
        bitmaps.append(bitmap)
        offset += len(bitmap)
    path = ICON_DIRECTORY / "windows" / "ldap-browser.ico"
    path.write_bytes(directory + b"".join(bitmaps))


def write_xpm(size, pixels):
    keys = " .+*"
    symbols = [keys[palette_index(pixels[index:index + 4])] for index in range(0, len(pixels), 4)]
    entries = [f"{size} {size} 4 1", "  c None"]
    entries.extend(f"{symbol} c #{r:02X}{g:02X}{b:02X}"
                   for symbol, (r, g, b) in zip(keys[1:], PALETTE[1:]))
    entries.extend("".join(symbols[start:start + size])
                   for start in range(0, len(symbols), size))
    body = ",\n".join(f'"{entry}"' for entry in entries)
    path = ICON_DIRECTORY / "linux" / "ldap-browser.xpm"
    path.write_text("/* XPM */\n/*\n" + LICENSE + "*/\nstatic char *ldap_browser_xpm[] = {\n" + body + "\n};\n",
                    encoding="ascii")


def main():
    window_sizes = (16, 32, 48, 64, 128)
    pixels = {size: render(size) for size in (16, 24, 32, 48, 64, 128, 256, 512, 1024)}
    images = {size: png(size, rgba) for size, rgba in pixels.items()}
    window_directory = REPOSITORY / "plugins" / "rcp" / "resources" / "icons" / "window"
    for size in window_sizes:
        (window_directory / f"ldap-browser_{size}x{size}.png").write_bytes(images[size])
    write_icns(images)
    write_ico(pixels)
    write_xpm(48, pixels[48])


if __name__ == "__main__":
    main()
